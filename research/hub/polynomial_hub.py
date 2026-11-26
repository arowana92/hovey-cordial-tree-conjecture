"""Injective integer labels at a prescribed zero hub, with polynomial span."""

from collections import deque
from math import gcd
from random import Random

from research.check_large_order_subdivision import children, compress
from research.hub.universal_hub import construct as small_certificate
from research.large_order_gap_paths import gap_path, prune
from research.large_order_subdivision import POSITIONS


DEPTH = 432


def bottom_fringe(tree, kids, deep, height=8):
    """Set aside a path or two arms in a rooted subtree of the indicated height."""
    top = deep
    for _ in range(height):
        top = tree[top]
    levels = [[top]]
    while levels[-1]:
        levels.append([w for v in levels[-1] for w in kids[v]])
    support = {v: [w for w in kids[v] if kids[w]] for level in levels for v in level}
    fork = next((v for level in reversed(levels) for v in level if len(support[v]) >= 2), None)
    if fork is None:
        chain = [tree[deep]]
        for _ in range(2):
            chain.append(tree[chain[-1]])
        chain.reverse()
    else:
        chains = []
        for v in support[fork]:
            arm = [v]
            while support[arm[-1]]:
                w, = support[arm[-1]]
                arm.append(w)
            chains.append(arm)
        chain = max(chains,key=len)

    if len(chain) >= 3:
        a,b,c = chain[-3:]
        d = kids[c][0]
        plus = [w for w in kids[b] if w != c]
        minus = [w for w in kids[c] if w != d]
        outside = [w for w in kids[a] if w != b]
        kind = "path-b"
        if len(plus) > len(minus):
            plus,minus = minus,plus
            kind = "path-c"
        boundary = tree[a]
    else:
        def arm(v):
            end = support[v][0] if support[v] else kids[v][0]
            return v,end,[w for w in kids[v] if w != end],kids[end]

        arms = [arm(w) for w in support[fork][:2]]
        arms.sort(key=lambda row:(len(row[3]),-len(row[2])))
        (a,b,left,plus),(c,d,right,minus) = arms
        outside = left+right
        kind, boundary = "arms",fork
    return kind,boundary,(a,b,c,d),plus,minus,outside


def trials(width, rng, spread=False):
    start = rng.randrange(width)
    step = 1
    if spread and width>1:
        step = rng.randrange(1,width)
        while gcd(step,width)!=1:
            step = 1+step%(width-1)
    return (1+(start+i*step)%width for i in range(width))


def add_transfer(labels, used, targets, path, p, s, t, width, rng, avoid_radius=-1):
    middle = (-(p+s+2*t))//3
    for j in trials(width,rng,spread=avoid_radius>=0):
        z = middle+j
        first = gap_path(p,s,z)
        values = first+gap_path(first[-1],z,t)
        moving = values[:7]+values[8:11]+values[12:]
        if (len(set(values))==14 and not used.intersection(values) and
                not targets.intersection(moving) and all(abs(x)>avoid_radius for x in values)):
            for v,x in zip(path,values):
                labels[v] = x
            used.update(values)
            return
    raise AssertionError("no injective transfer")


def elongate(labels, used, path, width, rng, avoid_radius=-1):
    a,b = labels[path[0]],labels[path[-1]]
    assert a and b and a+b
    left, right = [], []
    for _ in range((len(path)-2)//12):
        for u in trials(width,rng,spread=avoid_radius>=0):
            v = 4*u
            values = [pa*a+pb*b+cu*u+cv*v for pa,pb,cu,cv in POSITIONS]
            if len(set(values))==12 and not used.intersection(values) and all(abs(x)>avoid_radius for x in values):
                break
        else:
            raise AssertionError("no injective subdivision")
        used.update(values)
        left.append(values[0])
        right.append(values[1:])
        a,b = u,v
    internal = left+[x for tail in reversed(right) for x in tail]
    assert len(internal)==len(path)-2
    for w,x in zip(path[1:-1],internal):
        labels[w] = x


def seed_layout(tree, depth):
    kids = children(tree)
    live,_,_,chains = prune(tree,{0},depth)
    pins = {v for v in kids[0] if v in live}
    ids,small,holes = compress(tree,kids,live,pins)
    edges = {ids[j]:ids[small[j]] for j in range(1,len(ids))}
    for chain in chains:
        for v in chain[:3]:
            edges[v] = tree[v]
    return edges,chains,holes


def seed(tree, depth, rng):
    edges,chains,holes = seed_layout(tree,depth)
    small_kids = {v:[] for v in [0,*edges]}
    for v,p in edges.items():
        small_kids[p].append(v)
    labels = {0:0}
    queue = deque(small_kids[0])
    while queue:
        v = queue.popleft()
        labels[v] = 2*len(tree)+len(labels)
        queue.extend(small_kids[v])
    bills = {v:(labels[v],labels[v]+labels[p]) for v,p in edges.items() if p}
    special = [chain[1] for chain in chains]
    targets = {x for _,t in bills.values() for x in (t,-t)}
    used = set(labels.values())
    assert len(used)==len(labels) and len(targets)==2*len(bills) and not targets.intersection(used)
    width = 100*(len(tree)+1)
    special_set = set(special)
    jobs = special+[v for v in bills if v not in special_set]
    slots = (chain[i:i+14] for i in range(3,depth-10-13,14) for chain in chains)
    for job in jobs:
        block = next(slots)
        p = labels[tree[block[0]]]
        s,t = bills[job]
        assert len({0,p,s,t})==4
        add_transfer(labels,used,targets,block,p,s,t,width,rng)
    for path in holes:
        elongate(labels,used,path,width,rng)
    return labels, (len(bills),sum((len(path)-2)//12 for path in holes))


def first_layer(vertices, tree, labels):
    """Translate closed walks separately, keeping the residual endpoint above all labels."""
    bound = max(map(abs,labels.values()))
    if sum(labels[tree[v]] for v in vertices) < 0:
        for v in labels:
            labels[v] = -labels[v]

    positions,edges,where = [0],[],{0:0}
    cycles = []
    for v in sorted(vertices,key=lambda w:labels[tree[w]]):
        head = positions[-1]+labels[tree[v]]
        edges.append(v)
        if head in where:
            i = where[head]
            cycles.append(list(zip(edges[i:],positions[i:])))
            for x in positions[i+1:]:
                del where[x]
            del edges[i:]
            del positions[i+1:]
        else:
            where[head] = len(positions)
            positions.append(head)
    top = bound
    for cycle in cycles:
        shift = top+1-min(x for _,x in cycle)
        for v,x in cycle:
            labels[v] = shift+x
        top = max(labels[v] for v,_ in cycle)
    start = top+1-min(positions)
    for v,x in zip(edges,positions):
        labels[v] = start+x
    terminal = start+positions[-1]
    assert terminal > max(labels.values())
    return start,terminal,len(cycles)


def construct(tree, depth=DEPTH):
    """Return integer vertex labels, the omitted label and counts of the pieces used."""
    if not tree or tree[0]!=-1 or any(not 0<=p<v for v,p in enumerate(tree[1:],1)):
        raise ValueError("need a parent-before-child tree")
    kids = children(tree)
    order,levels = [],[[0]]
    while levels[-1]:
        order.extend(levels[-1])
        levels.append([w for v in levels[-1] for w in kids[v]])
    if len(levels)-2 <= 12:
        index = {v:i for i,v in enumerate(order)}
        bfs = [-1]+[index[tree[v]] for v in order[1:]]
        x,g,_ = small_certificate(bfs)
        return [x[index[v]] for v in range(len(tree))],g,("bounded height",0,0,0)
    kind,boundary,nodes,plus,minus,other = bottom_fringe(tree,kids,order[-1])
    removed = set([*nodes,*plus,*minus,*other])
    ids = [v for v in range(len(tree)) if v not in removed]
    index = {v:i for i,v in enumerate(ids)}
    reduced = [-1]+[index[tree[v]] for v in ids[1:]]
    partial,stats = seed(reduced,depth,Random(20261127))
    labels = {ids[v]:x for v,x in partial.items()}
    assert boundary not in labels
    group = [v for v in ids if v not in labels and tree[v] in labels]
    start,terminal,cycles = first_layer(group,tree,labels)
    while group:
        group = [w for v in group for w in kids[v] if w not in removed]
        for v in group:
            labels[v] = terminal
            terminal += labels[tree[v]]
    assert len(labels) == len(ids)
    p = labels[boundary]
    if kind == "arms":
        values = (-p-terminal,terminal,-p,-terminal)
    elif kind == "path-b":
        values = (-p-terminal,terminal,-terminal,-p)
    else:
        values = (-p-terminal,-terminal,terminal,-p-2*terminal)
    labels.update(zip(nodes,values))
    gap = start
    unmatched = other+minus[len(plus):]
    for v in sorted(unmatched,key=lambda w:labels[tree[w]]):
        gap -= labels[tree[v]]
        labels[v] = gap
    top = max(labels.values())
    for u,v in zip(plus,minus):
        labels[u] = top+1
        labels[v] = labels[u]+terminal
        top = labels[v]
    return [labels[v] for v in range(len(tree))],gap,(kind,*stats,cycles)

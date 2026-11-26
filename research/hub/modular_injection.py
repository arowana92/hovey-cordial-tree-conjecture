"""Injective rooted certificates directly in a cyclic group."""

from random import Random

from research.check_large_order_subdivision import children
from research.hub.polynomial_hub import bottom_fringe, construct as integer_certificate
from research.large_order_gap_paths import gap_path


def walks(vertices, tree, labels, k):
    """Decompose assigned jumps into simple cycles and a residual simple path."""
    positions, edges, where = [0], [], {0: 0}
    cycles = []
    for v in vertices:
        head = (positions[-1]+labels[tree[v]]) % k
        edges.append(v)
        if head in where:
            i = where[head]
            cycles.append(list(zip(edges[i:], positions[i:])))
            for x in positions[i+1:]:
                del where[x]
            del edges[i:]
            del positions[i+1:]
        else:
            where[head] = len(positions)
            positions.append(head)
    return cycles, list(zip(edges, positions)), positions[-1]


def candidates(k, rng):
    start = rng.randrange(k)
    for i in range(k):
        yield (start+i) % k


def place_cycle(cycle, occupied, k, rng):
    for shift in candidates(k, rng):
        row = {v: (shift+x) % k for v,x in cycle}
        if occupied.isdisjoint(row.values()):
            occupied.update(row.values())
            return row
    raise ValueError("no disjoint translate")


def specialize(forms, occupied, k, rng):
    """Select one parameter for a collection of distinct affine forms."""
    for x in candidates(k,rng):
        row = {v:(a*x+b)%k for v,(a,b) in forms.items()}
        if len(set(row.values()))==len(row) and occupied.isdisjoint(row.values()):
            return x,row
    raise ValueError("no parameter separates the affine labels")


def advance(front, path, tree, labels, occupied, k, rng):
    p = labels[tree[path[0]]]
    delta = sum(labels[tree[v]] for v in front)%k
    if not delta:
        cycles,residual,_ = walks(front,tree,labels,k)
        assert not residual
        for cycle in cycles:
            labels.update(place_cycle(cycle,occupied,k,rng))
        a = gap_path(p,0,0)
        b = gap_path(p,1,1)
        forms = {v:(j-i,i) for v,i,j in zip(path[:7],a,b)}
        mode = "neutral"
    else:
        # Include the first path site as the last jump. Its tail has a
        # nonzero intercept; this separates the two slope-two arrivals.
        first,*rest = path
        cycles,residual,end = walks([*front,first],tree,labels,k)
        forms = {v:(1,c) for v,c in residual}
        taken = {0,end} | {c for _,c in residual}
        for cycle in cycles:
            row = place_cycle(cycle,taken,k,rng)
            forms.update((v,(1,c)) for v,c in row.items())
        c = forms[first][1]
        assert c and end not in [b for _,b in forms.values()]
        a = gap_path(c,0,end)
        b = gap_path(1+c,1,1+end)
        forms.update((v,(j-i,i)) for v,i,j in zip(rest,a,b))
        mode = "residual" if first in dict(residual) else "cycle"
    assert len(set((a,b%k) for a,b in forms.values()))==len(forms)
    _,row = specialize(forms,occupied,k,rng)
    labels.update(row)
    occupied.update(row.values())
    return mode,len(cycles)


def finish(tree, kids, labels, fringe, k, rng, max_levels=12):
    kind, boundary, nodes, plus, minus, other = fringe
    removed = set(nodes) | set(plus) | set(minus) | set(other)
    group = [v for v,p in enumerate(tree) if v and v not in removed and v not in labels and p in labels]
    cycles, residual, delta = walks(group,tree,labels,k)
    forms = {v:(0,x) for v,x in labels.items()}
    intercepts = {delta} | {x for _,x in residual}
    for v,x in residual:
        forms[v] = (1,x)
    for cycle in cycles:
        row = place_cycle(cycle,intercepts,k,rng)
        forms.update((v,(1,x)) for v,x in row.items())

    def add(left, right):
        return left[0]+right[0], (left[1]+right[1])%k

    def neg(row):
        return -row[0], (-row[1])%k

    terminal = (1,delta)
    levels = 1
    while group:
        group = [w for v in group for w in kids[v] if w not in removed]
        if group:
            levels += 1
        for v in group:
            forms[v] = terminal
            terminal = add(terminal,forms[tree[v]])
    p = forms[boundary]
    assert p[0]>0 and 1<=levels<=max_levels
    a = neg(add(p,terminal))
    if kind == "arms":
        values = (a,terminal,neg(p),neg(terminal))
    elif kind == "path-b":
        values = (a,terminal,neg(terminal),neg(p))
    else:
        values = (a,neg(terminal),terminal,add(a,neg(terminal)))
    forms.update(zip(nodes,values))
    gap = (1,0)
    for v in sorted(other+minus[len(plus):],key=lambda w:forms[tree[w]][0]):
        gap = add(gap,neg(forms[tree[v]]))
        forms[v] = gap
    top = max(x[0] for x in forms.values())
    for u,v in zip(plus,minus):
        forms[u] = (top+1,0)
        forms[v] = add(forms[u],terminal)
        top = forms[v][0]

    rows = [forms[v] for v in range(len(tree))]
    assert len(set(rows))==len(tree)
    x,row = specialize(forms,set(),k,rng)
    return [row[v] for v in range(len(tree))],(gap[0]*x+gap[1])%k,levels,max(abs(a) for a,_ in rows)


def construct(tree, k, random_seed=20261127):
    if not tree or tree[0]!=-1 or any(not 0<=p<v for v,p in enumerate(tree[1:],1)):
        raise ValueError("need a parent-before-child tree")
    if k<len(tree):
        raise ValueError("modulus smaller than tree")
    rng = Random(random_seed)
    kids = children(tree)
    depth = [0]*len(tree)
    for v in range(1,len(tree)):
        depth[v] = depth[tree[v]]+1
    deep = max(range(len(tree)),key=depth.__getitem__)
    if depth[deep]<=4:
        values,gap,_ = integer_certificate(tree)
        labels = [x%k for x in values]
        if len(set(labels))<len(tree):
            raise ValueError("bounded-height certificate collides")
        return labels,gap%k,(0,0,0,0,depth[deep],0)

    fringe = bottom_fringe(tree,kids,deep,height=4)
    eligible = [True]*len(tree)
    for v in range(1,len(tree)):
        eligible[v] = eligible[tree[v]] and v!=fringe[1]
    # Store longest eligible paths by their next child.
    height = [0]*len(tree)
    next_child = [None]*len(tree)
    for v in reversed(range(1,len(tree))):
        p = tree[v]
        if eligible[v] and height[p]<height[v]+1:
            height[p],next_child[p] = height[v]+1,v

    labels = {0:0, **{v:i for i,v in enumerate((w for w in kids[0] if eligible[w]),1)}}
    occupied = set(labels.values())
    rounds = transfers = special_cycles = loops = 0
    while True:
        front = [v for v,p in enumerate(tree) if v and eligible[v] and v not in labels and p in labels]
        start = next((v for v in front if height[v]>=7), None)
        if start is None:
            break
        path = [start]
        while len(path)<8:
            path.append(next_child[path[-1]])
        front.remove(start)
        mode,cycles = advance(front,path,tree,labels,occupied,k,rng)
        rounds += 1
        transfers += mode!="neutral"
        special_cycles += mode=="cycle"
        loops += cycles
    values,gap,levels,coefficient = finish(tree,kids,labels,fringe,k,rng)
    return values,gap,(rounds,transfers,special_cycles,loops,levels,coefficient)

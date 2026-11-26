"""Two-site integer interval completions of polynomial width for arbitrary cores."""

from collections import deque
from random import Random

from research.hub.polynomial_hub import DEPTH, add_transfer, elongate, seed_layout, trials
from research.hub.two_hub_contraction import bound, compact_complete, remove_fillers
from research.hub.two_hubs import short_seed


def polynomial_bound(h):
    skeleton_constant = 800*(bound(73)+1)
    return 2**24*(skeleton_constant+1)*(h+1)**434


def forest_seed(tree, boundaries, h, w, rng):
    """All selected free vertices and actual boundary edges have equal histograms."""
    edges,chains,holes = seed_layout(tree,DEPTH)
    children = {v:[] for v in [0,*edges]}
    for v,p in edges.items():
        children[p].append(v)
    scale = h+w+1
    used,targets,labels,bills = set(),set(),{},{}
    queue = deque(children[0])
    while queue:
        v = queue.popleft()
        parent = edges[v]
        p = labels[parent] if parent else boundaries[v]
        assert parent or abs(p)<=w
        for j in trials(20*scale,rng):
            s = 4*scale+j
            t = s+p
            if s in used or s in targets:
                continue
            if p and (t in used or t in targets):
                continue
            labels[v] = s
            used.add(s)
            if p:
                targets.update((t,-t))
                bills[v] = s,t
            break
        else:
            raise AssertionError("no base label")
        queue.extend(children[v])

    special = [chain[1] for chain in chains]
    special_set = set(special)
    jobs = special+[v for v in bills if v not in special_set]
    slots = (chain[j:j+14] for j in range(3,DEPTH-10-13,14) for chain in chains)
    width = 256*(scale+1)
    for v in jobs:
        path = next(slots)
        p = labels[tree[path[0]]]
        s,t = bills[v]
        assert len({0,p,s,t})==4
        add_transfer(labels,used,targets,path,p,s,t,width,rng,avoid_radius=w)
    for path in holes:
        elongate(labels,used,path,width,rng,avoid_radius=w)
    return labels,(len(bills),sum((len(path)-2)//12 for path in holes))


def reflected(interval, labels):
    interval.lo,interval.hi = 1-interval.hi,1-interval.lo
    interval.blocks = [(1-p,2-b,2-a) for p,a,b in interval.blocks]
    return {v:1-x for v,x in labels.items()}


def boundary_order(graph, seeds):
    order,prev,depth = [],{v:None for v in seeds},{v:0 for v in seeds}
    queue = deque(seeds)
    while queue:
        v = queue.popleft()
        for w in graph[v]:
            if w not in prev:
                prev[w] = v
                depth[w] = depth[v]+1
                queue.append(w)
                order.append(w)
    return order,prev,depth


def complete(tree, a, b, protected=()):
    """Keep the path joining the two optional additional terminals in the initial skeleton."""
    if (not tree or tree[0]!=-1 or any(not 0<=p<v for v,p in enumerate(tree[1:],1))
            or a==b or not 0<=a<len(tree) or not 0<=b<len(tree)):
        raise ValueError("need a parent-before-child tree and two different vertices")
    graph = [[] for _ in tree]
    for v,p in enumerate(tree[1:],1):
        graph[v].append(p)
        graph[p].append(v)
    if len(protected) not in (0,2) or any(v not in range(len(tree)) for v in protected):
        raise ValueError("need zero or two extra path endpoints")
    _,prev,_ = boundary_order(graph,[a])
    path = [b]
    while path[-1]!=a:
        path.append(prev[path[-1]])
    path.reverse()
    hull = set(path)
    terminals = list(protected)
    if len(path)-1 in (2,4):
        short = short_seed(graph,path)
        if short is None:
            return None
        terminals.extend(short[1])
    for v in terminals:
        while v not in hull:
            hull.add(v)
            v = prev[v]
    outer,parent,depth = boundary_order(graph,sorted(hull))
    tip = outer[-1] if outer else a
    deep = depth[tip]>=4
    if deep:
        knee = parent[tip]
        boundary = parent[knee]
        v = boundary
        while v not in hull:
            hull.add(v)
            v = parent[v]
    order,_,_ = boundary_order(graph,[a])
    ids = [a]+[v for v in order if v in hull]
    index = {v:i for i,v in enumerate(ids)}
    skeleton = [-1]+[index[prev[v]] for v in ids[1:]]
    seq,interval,_ = compact_complete(skeleton,0,index[b])
    labels = dict(zip(ids,seq))
    w = interval.hi-interval.lo+1
    rounds = (0,0)
    flip = deep and labels[boundary]>0
    if deep:
        if flip:
            labels = reflected(interval,labels)
        radius = 2**19*(len(tree)+w+1)
        interval.fill(0,interval.hi+1,radius+1)
        interval.hi = radius
        labels[knee] = interval.child(labels[boundary])
        labels[tip] = interval.child(labels[knee])

        exterior,prev,_ = boundary_order(graph,labels)
        ext_index = {v:i for i,v in enumerate(exterior,1)}
        virtual = [-1]+[ext_index.get(prev[v],0) for v in exterior]
        boundaries = {ext_index[v]:labels[prev[v]] for v in exterior if prev[v] in labels}
        added,rounds = forest_seed(virtual,boundaries,len(tree),w,Random(17197))
        assert all(w<abs(x)<radius for x in added.values())
        remove_fillers(interval,set(added.values()))
        labels.update((exterior[i-1],x) for i,x in added.items())

    fringe,prev,depths = boundary_order(graph,labels)
    levels = max(depths.values())
    assert levels<=DEPTH
    for v in fringe:
        labels[v] = interval.child(labels[prev[v]])
    if flip:
        labels = reflected(interval,labels)
    return [labels[v] for v in range(len(tree))],interval,(w,*rounds,levels)

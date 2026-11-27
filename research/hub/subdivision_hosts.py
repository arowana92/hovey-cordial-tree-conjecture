"""Place missing weights on a long subdivision, or beyond the final vertex interval."""

from collections import deque

from research.hub.prescribed_paths import EIGHT, NINE, SINGLE, U, bridge, constant, join, paths, separate


def breadth_labels(order, edges, site):
    neighbors = [[] for _ in range(order)]
    for u,v in edges:
        neighbors[u].append(v)
        neighbors[v].append(u)
    labels = [None]*order
    labels[site] = 0
    queue = deque([site])
    next_label = 1
    while queue:
        u = queue.popleft()
        for v in neighbors[u]:
            if labels[v] is None:
                labels[v] = next_label
                next_label += 1
                queue.append(v)
    if next_label != order:
        raise ValueError("expected a connected graph")
    return labels


def greedy_labels(order, edges, charge, site):
    neighbors = [[] for _ in range(order)]
    for (u,v),b in zip(edges,charge):
        neighbors[u].append((v,b))
        neighbors[v].append((u,b))
    labels = [None]*order
    labels[site] = 0
    used,weights = {0},set()
    queue = deque([site])
    while queue:
        u = queue.popleft()
        for v,b in neighbors[u]:
            if labels[v] is not None:
                continue
            offset = labels[u]+b
            x = 1
            while x in used or x+offset in weights:
                x += 1
            labels[v] = x
            used.add(x)
            weights.add(x+offset)
            queue.append(v)
    if len(used)!=order:
        raise ValueError("expected a connected tree")
    return labels


def anchored_tree(order, edges, internal, site, offsets=None, initial=None):
    if len(edges)!=order-1 or len(internal)!=len(edges) or not 0<=site<order:
        raise ValueError("expected a tree, subdivision lengths and an original site")
    if any(L and L<76 for L in internal):
        raise ValueError("each subdivided edge requires at least 76 internal vertices")
    N = order+sum(internal)
    charge = [0]*len(edges) if offsets is None else list(offsets)
    if len(charge)!=len(edges) or any(L and b for L,b in zip(internal,charge)):
        raise ValueError("offsets are allowed on the retained edges")
    if initial is None:
        coarse = greedy_labels(order,edges,charge,site) if any(charge) else breadth_labels(order,edges,site)
    else:
        if len(initial)!=order or len(set(initial))!=order or initial[site]!=0:
            raise ValueError("prescribed labels must be distinct with zero at the padding site")
        coarse = list(initial)
    fixed = [(u,v) for (u,v),L in zip(edges,internal) if not L]
    sums = {coarse[u]+coarse[v]+b for (u,v),L,b in zip(edges,internal,charge) if not L}
    if len(sums)!=len(fixed):
        raise ValueError("the retained edge sums must be distinct")
    M = max(36*N, *(abs(x) for x in [*coarse,*sums]))
    g = -10*M
    anchors = sorted(sums-set(coarse)) + [g]
    capacity = [max(0,(L-76)//77) for L in internal]
    if sum(capacity)<len(anchors):
        raise ValueError("too few positions for the missing sums and the minimum")
    targets = iter(sorted((set(coarse)|set(anchors)) - sums - {g}))
    occupied = set(coarse)|set(anchors)
    labels = coarse.copy()
    actual = []
    for (u,v),L,cap in zip(edges,internal,capacity):
        if L==0:
            actual.append((u,v))
            continue
        count = min(cap,len(anchors))
        points,anchors = anchors[:count],anchors[count:]
        terminal = coarse[v]
        parent = coarse[u]
        path = [u]
        for i,end in enumerate([*points,terminal]):
            size = 76 if i<count else L-77*count
            rows = bridge(parent,end,next(targets),size,occupied,extreme=g)
            occupied.update(rows)
            if i<count:
                rows.append(end)
            path.extend(range(len(labels),len(labels)+len(rows)))
            labels.extend(rows)
            parent = end
        path.append(v)
        actual.extend(zip(path,path[1:]))
    assert next(targets,None) is None and not anchors
    return labels,actual


def high_bridge(p,q,w,L,occupied,M):
    """Realize a target just above 160M, keeping all internal labels below 160M."""
    if L<92 or not 160*M<w<=161*M:
        raise ValueError("expected a long path and a target in the exterior interval")
    used = set(occupied)
    prefix = []
    suffix = []
    def extend(rows,parent,table):
        block = separate(paths(table,constant(parent),U),used,[1],None)
        used.update(block)
        rows.extend(block)
        return block[-1]
    if p==0:
        p = extend(prefix,p,SINGLE)
    if q==0:
        q = extend(suffix,q,SINGLE)
    remainder = L-34-len(prefix)-len(suffix)
    nines = remainder%8
    eights = (remainder-9*nines)//8
    for table in [EIGHT]*eights+[NINE]*nines:
        p = extend(prefix,p,table)
    middle = join(EIGHT,p,EIGHT,q,w,used,[1,1,1],starts=[-60*M,-60*M,80*M])
    return [*prefix,*middle,*reversed(suffix)]


def graph_host(order,edges,internal,site):
    if len(edges)<order or len(internal)!=len(edges) or min(internal)<92:
        raise ValueError("expected a connected cyclic graph with all edges subdivided")
    N = order+sum(internal)
    M = 36*N
    labels = breadth_labels(order,edges,site)
    high = 160*M
    targets = [*labels,*range(high+1,high+1+len(edges)-order)]
    occupied = set(labels)
    actual = []
    for (u,v),w,L in zip(edges,targets,internal):
        if w<=high:
            block = bridge(labels[u],labels[v],w,L,occupied)
        else:
            block = high_bridge(labels[u],labels[v],w,L,occupied,M)
        path = [u,*range(len(labels),len(labels)+L),v]
        actual.extend(zip(path,path[1:]))
        occupied.update(block)
        labels.extend(block)
    return labels,actual,high

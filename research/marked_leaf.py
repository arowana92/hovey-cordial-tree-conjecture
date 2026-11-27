"""Construct an ordinary cordial labeling with a specified leaf in a highest-frequency bin."""

from collections import Counter

from .rainbow.generate import rainbow


def cut(graph, t):
    """Choose a leaf batch or the size-ordered suffix from a leaf centroid."""
    leaves = sorted(v for v,row in graph.items() if len(row) == 1)
    if len(leaves) >= t:
        return set(leaves[:t])
    start = next(v for v,row in graph.items() if len(row) > 1)
    parent, order = {start:None}, [start]
    for v in order:
        for w in graph[v]:
            if w != parent[v]:
                parent[w] = v
                order.append(w)
    counts = {v:int(len(row) == 1) for v,row in graph.items()}
    for v in reversed(order[1:]):
        counts[parent[v]] += counts[v]
    total = len(leaves)
    centroid = next(v for v in order if len(graph[v]) > 1 and
                    2*max([total-counts[v]]+[counts[w] for w in graph[v] if parent[w] == v]) <= total)

    parent, order = {centroid:None}, [centroid]
    children = {v:[] for v in graph}
    for v in order:
        for w in graph[v]:
            if w != parent[v]:
                parent[w] = v
                order.append(w)
                children[v].append(w)
    sizes = dict.fromkeys(graph,1)
    tips = {v:int(not row) for v,row in children.items()}
    for v in reversed(order[1:]):
        sizes[parent[v]] += sizes[v]
        tips[parent[v]] += tips[v]
    parts = children[centroid]
    chosen = next(({w} for w in parts if 3*tips[w] >= total),None)
    if chosen is None:
        chosen = set()
        subtotal = 0
        for w in parts:
            chosen.add(w)
            subtotal += tips[w]
            if 3*subtotal >= total:
                break
    outside = max((chosen,set(parts)-chosen),key=lambda group:sum(sizes[v] for v in group))
    stack = sorted(outside,key=sizes.get,reverse=True)
    walk = []
    while stack:
        v = stack.pop()
        walk.append(v)
        stack.extend(sorted(children[v],key=sizes.get,reverse=True))
    return set(walk[-t:])


def label(parent, m, mark=None):
    graph = {v:[] for v in range(len(parent))}
    for v,u in enumerate(parent[1:],1):
        graph[u].append(v)
        graph[v].append(u)
    if mark is not None and len(graph[mark]) > 1:
        raise ValueError("the marked vertex must be a leaf")

    steps = []
    while len(graph) > 1:
        n = len(graph)
        t = (n-1)%m
        if not t:
            v = mark if mark is not None else next(v for v,row in graph.items() if len(row) == 1)
            outside = {v}
        elif n <= m:
            outside = set(graph)-{next(iter(graph))}
        else:
            outside = cut(graph,t)
        queue = [(v,w) for v in sorted(outside) for w in graph[v] if w not in outside]
        roots = len(queue)
        for v,w in queue:
            queue.extend((x,v) for x in graph[v] if x != w)
        steps.append((queue,roots,t == 0))
        for v,w in queue[:roots]:
            graph[w].remove(v)
        for v in outside:
            del graph[v]
        if mark in outside:
            mark = None

    f = {next(iter(graph)):0}
    vertices, weights = Counter(f.values()), Counter()
    for queue,roots,fill_deficit in reversed(steps):
        if fill_deficit:
            (v,w), = queue
            deficit = min(range(m),key=weights.__getitem__)
            f[v] = (deficit-f[w])%m
        else:
            surplus = vertices.most_common(1)[0][0]
            local = {v:i for i,(v,_) in enumerate(queue)}
            links = [-1-(f[w]-surplus)%m if i < roots else local[w]
                     for i,(_,w) in enumerate(queue)]
            digits = rainbow(links,m)
            f.update((v,(x+surplus)%m) for (v,_),x in zip(queue,digits))
        for v,w in queue:
            vertices[f[v]] += 1
            weights[(f[v]+f[w])%m] += 1
    return [f[v] for v in range(len(parent))]

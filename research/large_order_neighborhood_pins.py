"""Bound the load at prescribed sites and extract disjoint depth-two trees."""

from collections import deque


def adjacency(parents):
    neighbors = [[] for _ in parents]
    for v in range(1, len(parents)):
        p = parents[v]
        neighbors[v].append(p)
        neighbors[p].append(v)
    return neighbors


def neighborhood_labels(parents, k, pins, degree):
    neighbors = adjacency(parents)
    exceptional = {v for v,ns in enumerate(neighbors) if sum(w in pins for w in ns) > degree}
    fixed = set(pins) | exceptional
    labels = [None] * len(parents)
    for v in fixed:
        labels[v] = pins.get(v, 0)
    vertex, edge = [0]*k, [0]*k
    for v in fixed:
        vertex[labels[v]] += 1
        if v and parents[v] in fixed:
            edge[(labels[v]+labels[parents[v]]) % k] += 1
    u = len(exceptional)
    d = degree+u+1
    threshold = max(2*u+2, 4*((len(parents)+k-1)//k)*(d+1))
    for root in range(len(parents)):
        if labels[root] is not None:
            continue
        queue = deque([root])
        while queue:
            v = queue.popleft()
            old = [labels[w] for w in neighbors[v] if labels[w] is not None]
            assert len(old) <= d
            x = next(x for x in range(k) if vertex[x] < threshold
                     and all(edge[(x+y) % k] < threshold for y in old))
            labels[v] = x
            vertex[x] += 1
            for y in old:
                edge[(x+y) % k] += 1
            queue.extend(w for w in neighbors[v] if labels[w] is None)
    return labels, threshold+d


def extract(parents, t):
    """Return t mutually nonadjacent depth-two trees when the counting hypothesis holds."""
    neighbors = adjacency(parents)
    leaves = {v for v,ns in enumerate(neighbors) if len(ns) == 1}
    rich = {v for v,ns in enumerate(neighbors) if v not in leaves
            and sum(w in leaves for w in ns) >= t}
    side = [0]*len(parents)
    for v in range(1,len(parents)):
        side[v] = 1-side[parents[v]]
    candidates = [[],[]]
    for v,ns in enumerate(neighbors):
        if v not in leaves and sum(w in rich for w in ns) >= 2*t-1:
            candidates[side[v]].append(v)
    centers = max(candidates,key=len)[:t]
    if len(centers) < t:
        return []
    chosen = set(centers)
    output = []
    for v in centers:
        private = [w for w in neighbors[v] if w in rich and
                   sum(y in chosen for y in neighbors[w]) == 1][:t]
        assert len(private) == t
        arms = [(w,[z for z in neighbors[w] if z in leaves][:t]) for w in private]
        output.append((v,arms))
    return output

"""Bound the load at prescribed sites and extract disjoint depth-two trees."""

from collections import Counter, deque
from math import isqrt


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
    size = 1 + isqrt(max(0,len(exceptional)-1))
    extra = {v for v,ns in enumerate(neighbors) if v not in pins
             and sum(w in exceptional for w in ns) > size}
    assert len(extra) <= size
    fixed = set(pins) | exceptional | extra
    labels = [None] * len(parents)
    for v in set(pins) | extra:
        labels[v] = pins.get(v, 0)
    order = sorted(exceptional, key=lambda v: (pins.get(parents[v], 0),v))
    for i,v in enumerate(order):
        labels[v] = (i//size) % k
    vertex, edge = [0]*k, [0]*k
    for v in fixed:
        vertex[labels[v]] += 1
        if v and parents[v] in fixed:
            edge[(labels[v]+labels[parents[v]]) % k] += 1
    d = degree + 2*size + 1
    average = (len(parents)+k-1)//k
    threshold = max(6*size+average+2, 4*average*(d+1))
    assert max(vertex+edge) <= threshold
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


def extract(parents, t, count=None):
    """Return count mutually nonadjacent trees with t arms and t leaves on each arm."""
    if count is None:
        count = t
    neighbors = adjacency(parents)
    leaves = {v for v,ns in enumerate(neighbors) if len(ns) == 1}
    rich = {v for v,ns in enumerate(neighbors) if v not in leaves
            and sum(w in leaves for w in ns) >= t}
    side = [0]*len(parents)
    for v in range(1,len(parents)):
        side[v] = 1-side[parents[v]]
    candidates = [[],[]]
    for v,ns in enumerate(neighbors):
        sons = sum(w in rich for w in ns)
        if v not in leaves and sons >= t:
            candidates[side[v]].append((sons,v))
    for group in candidates:
        centers = [v for _,v in sorted(group,reverse=True)[:2*count]]
        if len(centers) < count:
            continue
        seen = Counter(w for v in centers for w in neighbors[v] if w in rich)
        output = []
        for v in centers:
            private = [w for w in neighbors[v] if w in rich and seen[w] == 1][:t]
            if len(private) == t:
                arms = [(w,[z for z in neighbors[w] if z in leaves][:t]) for w in private]
                output.append((v,arms))
                if len(output) == count:
                    return output
    return []

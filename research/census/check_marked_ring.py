"""Check the sharp interval bound and complete marked 27- and 54-label trees."""
from collections import Counter
from math import gcd
from random import Random

from research.check_matching_expansion import check
from research.matching_expansion import matching_labels


def orbit_checks():
    tests = 0
    for k in range(2, 241):
        units = [u for u in range(1, k) if gcd(u, k) == 1]
        prime = next(d for d in range(2, k+1) if k % d == 0)
        limit = 2*k//prime
        worst = 0
        for d in range(1,k):
            orbit = sorted({u*d % k for u in units})
            largest = max(b-a for a,b in zip(orbit,orbit[1:]+[orbit[0]+k]))
            worst = max(worst,largest)
            tests += 1
        assert worst == limit
    return tests


def matching_check(labels, edges, mark, rng=None):
    graph = [[] for _ in labels]
    for a,b in edges:
        graph[a].append(b)
        graph[b].append(a)
    assert len(graph[mark]) == 1
    order = [0]
    visited = {0}
    parents = [-1]
    for i,v in enumerate(order):
        for u in graph[v]:
            if u not in visited:
                visited.add(u)
                parents.append(i)
                order.append(u)
    assert len(order) == len(labels)
    colors = [labels[v] for v in order]
    if rng is None:
        # Use both ports at each nonleaf. Each original leaf yields exactly one new leaf.
        joins = [(int(graph[order[p]][0]!=order[i]),int(graph[order[i]][0]!=order[p]))
                 for i,p in enumerate(parents[1:],1)]
    else:
        joins = [(rng.randrange(2),rng.randrange(2)) for _ in parents[1:]]
    lifted = matching_labels(parents,colors,joins,27)
    pair_edges = [(2*i,2*i+1) for i in range(len(labels))]
    external = [(2*parents[i]+a,2*i+b) for i,(a,b) in enumerate(joins,1)]
    check(lifted,pair_edges+external,54)
    pair = order.index(mark)
    used = {v for edge in external for v in edge}
    temporary = next(v for v in (2*pair,2*pair+1) if v not in used)
    edges_after = [(a-(a>temporary), b-(b>temporary))
                   for a,b in pair_edges+external if temporary not in (a,b)]
    check(lifted[:temporary]+lifted[temporary+1:],edges_after,54)
    if rng is None:
        leaves = sum(len(adj)==1 for adj in graph)
        for tree in (pair_edges+external,edges_after):
            assert sum(d==1 for d in Counter(v for e in tree for v in e).values())==leaves


def joins():
    # Replacing (0,1) on the 27-cycle by (13,15) preserves weight 1.
    ring = [(i,(i+1)%27) for i in range(1,27)] + [(13,15)]
    assert len({(a+b)%27 for a,b in ring}) == 27
    rng = Random(271154)
    trees = rescaled = matched = 0
    for s in range(23,28):
        for neighbor in range(1,s):
            for a,b in ((0,neighbor),(neighbor,0)):
                for edge in ((13,14),(14,15),(13,15)):
                    u,v = edge
                    edges = [(0,j) for j in range(1,s) if j != neighbor]
                    edges += [(s+x,s+y) for x,y in ring if (x,y) != edge]
                    edges += [(a,s+u),(b,s+v)]
                    for mark in (0,1):
                        scale = next(h for h in range(1,27) if gcd(h,27)==1 and
                                     (a+h*(mark-v)) % 27 < s)
                        labels = list(range(s)) + [(a+scale*(z-v)) % 27 for z in range(27)]
                        vertices,weights = check(labels,edges,27)
                        assert vertices[labels[s+mark]] == max(vertices)
                        assert vertices == [1+int(z<s) for z in range(27)]
                        assert weights == [1+int(1<=z<s) for z in range(27)]
                        trees += 1
                        rescaled += scale != 1
                        if trees % 7 == 0:
                            matching_check(labels,edges,s+mark,rng)
                            matched += 1
    return trees,rescaled,matched


if __name__ == "__main__":
    print("Nonzero unit orbits checked",orbit_checks())
    total,scaled,matched = joins()
    print(f"Actual marked insertions {total}, requiring a change from scale one {scaled}")
    print(f"Perfect and near-perfect matching pairs at 54 labels {matched}")

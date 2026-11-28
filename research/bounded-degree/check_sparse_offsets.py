"""Independently audit the reduction, both embedding moments and concrete blocks."""
from collections import Counter
from itertools import permutations, product
from math import log2
from random import Random

from check import adjacency
from sparse_offsets import reduction


def verify(edges, biases, cap, rng):
    k = len(edges) + 1
    clean, gap, pins, labels, few = reduction(edges, biases, cap, rng)
    graph = adjacency(k, clean)
    seen, frontier = {0}, [0]
    for v in frontier:
        for w in graph[v] - seen:
            seen.add(w)
            frontier.append(w)
    assert len(seen) == k and len(clean) == k-1 and max(map(len, graph)) <= cap+2
    assert all(labels[v] == x for v, x in pins.items()) and len(set(labels.values())) == len(labels)
    assert all(0 <= x < k for x in labels.values())
    assert (sum(labels.values())-sum(range(k))) % k == 0
    assert (sum(len(graph[v])*x for v, x in labels.items()) + gap-sum(range(k))) % k == 0
    for d, count in Counter(map(len, graph)).items():
        inside = sum(len(graph[v]) == d for v in labels)
        assert inside == count or min(inside, count-inside) >= 6
    bias = {frozenset(key): value for key, value in biases.items()}
    old = {frozenset(e) for e in edges}
    new = {frozenset(e) for e in clean}
    assert len(new) == len(old) == k-1
    assert all(p <= pins.keys() for p in (old ^ new) | bias.keys())
    for values in (pins, labels):
        def histogram(es, offsets):
            return Counter((sum(values[v] for v in pair)+offsets.get(pair, 0)) % k
                           for pair in es if pair <= values.keys())
        actual = histogram(old, bias)
        assert actual == histogram(new, {})
        assert gap not in actual and max(actual.values(), default=0) <= 1
    return few


def input_trees(k):
    paths = [(i-1, i) for i in range(1, k)]
    yield paths, []
    yield paths, [0]
    yield paths, [0, k-2]
    yield paths, [0, 1, 2, k//3, k//3+1, k-3, k-2]
    binary = [((i-1)//2, i) for i in range(1, k)]
    yield binary, [0, 1, 2, k//2, k-2]
    # Two adjacent branching vertices, one of which is incident with three offset edges.
    trunk = k-12
    double = paths[:trunk-1] + [(1+(i % 2), i) for i in range(trunk, k)]
    yield double, [0, 1, trunk-1, trunk+1, trunk+3]
    yield double, [0, trunk-2, *range(trunk-1, k-1)]


def literal_blocks():
    # All independent offsets on short three-edge shapes. Evaluate original sums
    # at every prefix for every choice of starting vertex and connected order.
    total = prefixes = 0
    for k in (5, 6, 7, 8):
        n = 4
        for edges in ([(0, 1), (1, 2), (2, 3)], [(0, 1), (0, 2), (0, 3)]):
            graph = adjacency(n, edges)
            orders = [p for p in permutations(range(n))
                      if all(graph[v].intersection(p[:i]) for i, v in enumerate(p) if i)]
            for offsets in product(range(k), repeat=n-2):
                bias = (0,) + offsets
                for x in permutations(range(k), n):
                    weights = [(x[a]+x[b]+h) % k for (a, b), h in zip(edges, bias)]
                    if len(set(weights)) == n-1:
                        break
                else:
                    raise AssertionError("no small rainbow base")
                for p in orders:
                    for i in range(1, n+1):
                        retained = set(p[:i])
                        vertex = Counter(x[v] for v in retained)
                        edge = Counter((x[u]+x[v]+h) % k for (u,v),h in zip(edges,bias)
                                       if u in retained and v in retained)
                        assert sum(edge.values()) == i-1
                        for hist in (vertex, edge):
                            vals = [hist[r] for r in range(k)]
                            assert max(vals)-min(vals) <= 1
                        prefixes += 1
                total += 1
    return total, prefixes


def interval_bound():
    # Every increasing rooted tree on at most nine vertices, all intervals of
    # its size-ordered preorder, including intervals ending midway through a child.
    tested = 0
    for n in range(2, 10):
        for parents in product(*(range(i) for i in range(1, n))):
            children = [[] for _ in range(n)]
            for v, parent in enumerate(parents, 1):
                children[parent].append(v)
            traversals = {}
            for v in reversed(range(n)):
                ordered = sorted(children[v], key=lambda w: len(traversals[w]))
                traversals[v] = [v] + [x for w in ordered for x in traversals[w]]
            order = traversals[0]
            for a in range(1, n):
                prefix = set(order[:a])
                boundary = set()
                for b in range(a, n):
                    p = parents[order[b]-1]
                    if p in prefix:
                        boundary.add(p)
                    assert len(boundary) <= 1 + int(log2(b-a+1))
                    tested += 1
    return tested


def multiblock_growth(rng):
    checked = blocks = 0
    for k in (5, 7):
        n = 5*k+3
        for _ in range(30):
            # This numbering is the independently prescribed connected order.
            parents = [None] + [rng.randrange(v) for v in range(1, n)]
            delta = [0] + [rng.randrange(k) for _ in range(1, n)]
            labels = []
            for start in range(0, n, k):
                if start:
                    counts = Counter((labels[v]+labels[parents[v]]+delta[v]) % k for v in range(1, start))
                    missing = min(range(k), key=lambda w: counts[w])
                    u = (missing-labels[parents[start]]-delta[start]) % k
                else:
                    u = rng.randrange(k)
                labels.append(u)
                stop = min(start+k, n)
                for perm in permutations(range(1, k), stop-start-1):
                    add = [(x+u) % k for x in perm]
                    trial = labels + add
                    actual = [(trial[v]+trial[parents[v]]+delta[v]) % k for v in range(start+1, stop)]
                    if len(set(actual)) == len(actual):
                        break
                else:
                    raise AssertionError("no compatible small block")
                labels.extend(add)
                blocks += 1
            vertices, weights = Counter(), Counter()
            for v, x in enumerate(labels):
                vertices[x] += 1
                if v:
                    weights[(x+labels[parents[v]]+delta[v]) % k] += 1
                for hist in (vertices, weights):
                    counts = [hist[j] for j in range(k)]
                    assert max(counts)-min(counts) <= 1
                checked += 1
    return blocks, checked


def main():
    rng = Random(27081991)
    modes = Counter()
    for k in (503, 625, 810, 1024):
        for edges, selected in input_trees(k):
            for _ in range(3):
                biases = {edges[i]: rng.randrange(1, k) for i in selected}
                perm = list(range(k))
                rng.shuffle(perm)
                def renamed(pair):
                    u, v = pair
                    return perm[u], perm[v]
                permuted = list(map(renamed, edges))
                rng.shuffle(permuted)
                modes[verify(permuted, {renamed(e):h for e,h in biases.items()}, 3, rng)] += 1
    total, prefixes = literal_blocks()
    blocks, grown = multiblock_growth(rng)
    print(f"preorder intervals={interval_bound()} multi-block steps={blocks} grown prefixes={grown}")
    print(f"degree cores with reserved leaves={modes[False]} with forced gap={modes[True]}")
    print(f"literal offset trees={total} checked connected prefixes={prefixes}")


if __name__ == "__main__":
    main()

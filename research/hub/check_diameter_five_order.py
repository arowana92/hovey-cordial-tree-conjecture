"""Exercise the high-core reduction on whole diameter-five trees modulo k."""

from collections import Counter
from itertools import product

from research.large_order_degree import attach_batch, balanced, counts


def check(k, h, left, extra):
    # Every branch parent has at least one exterior child. Center leaves are optional.
    core = [-1, 0] + [0]*left + [1]*(h-2-left)
    parents = core + [p for p in range(2, h) for _ in range(1+(p*extra) % 4)] + [0]*extra
    r = h % k
    omitted = list(range(h-r, h))
    kept = set(range(h-r))
    labels = [None]*len(parents)
    # Consecutive-sum caterpillar labeling by first occurrence in each part.
    left_edges = [(0, v) for v in kept if v >= 2 and core[v] == 0]
    right_edges = [(v, 1) for v in kept if v >= 2 and core[v] == 1]
    edges = left_edges + [(0, 1)] + right_edges
    order = list(dict.fromkeys(a for a, _ in edges)) + list(dict.fromkeys(b for _, b in edges))
    for i, v in enumerate(order):
        labels[v] = i % k
    vertices, weights = counts(parents, labels, k)
    assert len(set(vertices)) == 1 and weights.count(min(weights)) == 1
    exterior = list(range(h, len(parents)))
    first = omitted.pop() if omitted else exterior.pop()
    labels[first] = (weights.index(min(weights))-labels[parents[first]]) % k
    if omitted:
        eligible = [v for v in exterior if labels[parents[v]] is not None]
        take = eligible[:k-len(omitted)]
        assert len(take)+len(omitted) == k
        attach_batch(parents, labels, omitted+take, k)
        used = set(take)
        exterior = [v for v in exterior if v not in used]
    for i in range(0, len(exterior), k):
        attach_batch(parents, labels, exterior[i:i+k], k)
    assert None not in labels
    vertices = Counter(labels)
    edge_weights = Counter((labels[v]+labels[p]) % k for v, p in enumerate(parents) if v)
    assert all(balanced([freq[z] for z in range(k)]) for freq in (vertices, edge_weights))


if __name__ == "__main__":
    total = 0
    for k in range(2, 10):
        for h in range(max(k, 4), 3*k+2):
            for left, extra in product(range(1, h-2), (0, 3)):
                check(k, h, left, extra)
                total += 1
    print(f"Verified both residue histograms on {total} full diameter-five trees.")

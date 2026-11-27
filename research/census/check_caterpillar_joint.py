"""Verify attachments on the original edges and exhaustive boundary histograms."""

from collections import Counter
from itertools import permutations, product
from random import Random

from research.census.caterpillar_joint import extend


def shape(counts):
    spine = tuple(range(len(counts)))
    edges = list(zip(spine, spine[1:]))
    leaves = {}
    n = len(spine)
    for v, count in enumerate(counts):
        leaves[v] = list(range(n, n + count))
        edges.extend((v, u) for u in leaves[v])
        n += count
    return spine, leaves, edges, n


def check(tree, joint, c, d, k):
    spine, leaves, edges, n = tree
    base = {-1: k - 1, joint: c}
    labels = extend(spine, leaves, joint, base, d, k)
    assert all(labels[v] == val for v, val in base.items())
    vertices = [labels[v] for v in range(n) if v != joint]
    assert all(0 <= h < k for h in vertices)
    assert len(set(vertices)) == n - 1
    weights = Counter((labels[u] + labels[v]) % k for u, v in edges)
    bins = [weights[i] + int(i != d) for i in range(k)]
    assert max(bins) - min(bins) <= 1, (spine, leaves, joint, c, d, k, bins)
    return weights[d]


def main():
    counts_by_hit = Counter()
    for s in range(1, 5):
        for counts in product(range(3), repeat=s):
            tree = shape(counts)
            n = tree[-1]
            if n == 1:
                continue
            for k in range(n, n + 3):
                for v in range(n):
                    for c, d in product(range(k), repeat=2):
                        counts_by_hit[check(tree, v, c, d, k)] += 1
    rng = Random(1991)
    for _ in range(1000):
        tree = shape([rng.randrange(5) for _ in range(rng.randrange(2, 40))])
        n = tree[-1]
        k = rng.choice((n, n + 1, n + rng.randrange(70)))
        v, c, d = rng.randrange(n), rng.randrange(k), rng.randrange(k)
        counts_by_hit[check(tree, v, c, d, k)] += 1
    # A four-edge path rooted at its midpoint has no uniform increment mod 4.
    for tip1, left, right, tip2 in permutations(range(4)):
        assert len({(tip1 + left) % 4, left, right, (right + tip2) % 4}) < 4
    print("prescribed extensions by hits on the deficient residue", dict(counts_by_hit))
    print("all 24 assignments on the rooted four-edge path exclude uniform increments")


if __name__ == "__main__":
    main()

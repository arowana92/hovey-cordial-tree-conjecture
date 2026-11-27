"""Verify original rooted edges and compare the semigroup test to exhaustive search."""

from itertools import combinations
from math import isqrt

from research.census.prime_neutral import construct


def brute(k, a, b):
    values = set(range(k))
    for x in values:
        for y in values - {x}:
            available = values - {x, y}
            for left in combinations(available, a):
                L = set(left)
                for right in combinations(available - L, b):
                    R = set(right)
                    weights = ((values - L - R) | {(z + x) % k for z in L}
                               | {(z + y) % k for z in R})
                    if len(weights) == k:
                        return True
    return False


def main():
    good = bad = compared = 0
    for k in range(5, 132):
        if any(k % d == 0 for d in range(2, isqrt(k) + 1)):
            continue
        for a in range(1, k - 2):
            for b in range(1, k - a - 1):
                ordinary = k - a - b - 2
                h = ordinary + 2
                t = a + b
                rows = construct(a, b, ordinary)
                # Ordinary integer knapsack, independent of shortest paths on residues.
                target = t - h
                reached = {0}
                for i in range(target + 1):
                    if i in reached:
                        reached.update([i + a, i + b, i + h])
                assert (rows is None) == (target in reached)
                if k <= 11:
                    assert brute(k, a, b) == (rows is not None)
                    compared += 1
                if rows is None:
                    bad += 1
                    continue
                assert [i for i, _, _ in rows] == list(range(k))
                assert [p for _, p, _ in rows] == [-1, -1] + [0]*a + [1]*b + [-1]*ordinary
                labels = [z for _, _, z in rows]
                assert set(labels) == set(range(k))
                sums = {(z + (labels[parent] if parent != -1 else 0)) % k
                        for _, parent, z in rows}
                assert len(sums) == k
                good += 1
    print("verified uniform blocks", good, "semigroup exclusions", bad,
          "independent exhaustive searches", compared)


if __name__ == "__main__":
    main()

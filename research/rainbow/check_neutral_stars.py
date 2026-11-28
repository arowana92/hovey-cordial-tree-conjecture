"""Independent enumeration and literal histogram checks for neutral_stars."""
from collections import Counter
from itertools import product
from math import gcd
from random import Random

from .neutral_stars import build, criterion


def exhaustive(k, q):
    """Try every pair of centers and every possible split of the leaf multiset."""
    feasible = set()
    for x, y in product(range(k), repeat=2):
        capacity = [q - (z == x) - (z == y) for z in range(k)]
        for first in product(*(range(c + 1) for c in capacity)):
            edges = [0] * k
            edges[x] += 1  # first entering edge, with parent zero
            for z, n in enumerate(first):
                edges[(x + z) % k] += n
                edges[(y + z) % k] += capacity[z] - n
            if max(edges) <= q:
                missing = edges.index(q - 1)
                feasible.add((1 + sum(first), (missing - y) % k))
    return feasible


def recount(k, s, t, a, b, result):
    x, y, left, right = result
    assert 0 <= x < k and 0 <= y < k
    vertices = Counter([x, y])
    weights = Counter([(a+x) % k, (b+y) % k])
    for size, center, leaves in ((s, x, left), (t, y, right)):
        assert len(leaves) == k and min(leaves) >= 0 and sum(leaves) == size - 1
        for label, count in enumerate(leaves):
            vertices[label] += count
            weights[(label+center) % k] += count
    q = (s+t)//k
    assert all(vertices[i] == weights[i] == q for i in range(k))


def main():
    cells = rejected = corroborated = 0
    for k in range(1, 10):
        for q in range(1, 4 if k <= 6 else 3):
            feasible = exhaustive(k, q)
            for s, delta in product(range(1, q*k), range(k)):
                good = (s, delta) in feasible
                assert criterion(k, s, q*k-s, 0, delta) == good
                rejected += not good
                cells += 1
            corroborated += len(feasible)
    assert cells == rejected + corroborated
    print(f"Literal exhaustive decisions {cells}, positive {corroborated}, negative {rejected}")

    rng = Random(82413)
    built = missed = 0
    for k in range(1, 36):
        for q in (1, 2, 3, 4):
            for s, delta in product(range(1, q*k), range(k)):
                a = rng.randrange(-4*k, 4*k+1)
                t, b = q*k-s, a+delta
                witness = build(k, s, t, a, b)
                if witness is None:
                    if q == 1:
                        # Try both forced-center orientations literally.
                        assert not any(h != delta % k and ((s-1)*h+delta) % k == 0
                                       for h in range(1, k))
                        assert not any(h != -delta % k and ((t-1)*h-delta) % k == 0
                                       for h in range(1, k))
                    else:
                        assert k % 2 == 0 and s % 2 == t % 2 == delta % 2 == 1
                    missed += 1
                else:
                    recount(k, s, t, a, b, witness)
                    built += 1
    print(f"Constructed histograms {built}, independently checked exclusions {missed}")

    large = 0
    for k in (37, 60, 97, 128, 255, 270):
        for q in (1, 2, 3, 10**5):
            for _ in range(50):
                s = rng.randrange(1, q*k)
                a, b = (rng.randrange(-k, 2*k) for _ in range(2))
                witness = build(k, s, q*k-s, a, b)
                if witness is not None:
                    recount(k, s, q*k-s, a, b, witness)
                    large += 1
    print(f"Additional larger witnesses {large}")

    # At the same parent the one-period criterion simplifies arithmetically.
    for k in range(2, 200):
        for s in range(1, k):
            assert criterion(k, s, k-s, 0, 0) == (gcd(k, s*s-1) > 1)


if __name__ == "__main__":
    main()

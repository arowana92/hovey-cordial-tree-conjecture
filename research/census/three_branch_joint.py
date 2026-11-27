"""Uniform full blocks with exactly three positive grandchild populations."""

from math import gcd

from research.census.cyclic_neutral import connected


def construct(counts, ordinary):
    if len(counts) != 3 or min(counts) < 1 or ordinary < 0:
        raise ValueError("expected three positive branch sizes and nonnegative direct leaves")
    k = sum(counts) + ordinary + 3
    for zero in sorted(range(3), key=counts.__getitem__, reverse=True):
        left, right = [i for i in range(3) if i != zero]
        a, b = counts[left], counts[right]
        g = gcd(a, b)
        x, y = b // g, -a // g % k
        part = connected(k, x, y, a, b, True)
        if part is None:
            continue
        fixed, first, second = part
        reserve = sorted(set(fixed) - {x, y, 0})
        groups = {left: first, right: second, zero: reserve[:counts[zero]]}
        center = {left: x, right: y, zero: 0}
        rows = [(i, -1, center[i]) for i in range(3)]
        for parent in range(3):
            rows.extend((len(rows), parent, v) for v in groups[parent])
        rows.extend((len(rows), -1, v) for v in reserve[counts[zero]:])
        return rows
    raise AssertionError("no choice of zero center")


def main():
    from itertools import combinations_with_replacement
    from random import Random
    rng = Random(1991)
    def check(counts, ordinary, k=None):
        rows = construct(counts, ordinary)
        n = sum(counts) + ordinary + 3
        k = k or n
        assert [i for i, _, _ in rows] == list(range(n))
        assert [p for _,p,_ in rows] == ([-1]*3 + [p for p in range(3) for _ in range(counts[p])]
                                          + [-1]*ordinary)
        labels = [v % k for _, _, v in rows]
        weights = [(v + (labels[p] if p != -1 else 0)) % k for _,p,v in rows]
        expected = [i for i in range(k) for _ in range(n//k)]
        assert sorted(labels) == sorted(weights) == expected

    total = 0
    for a, b, c in combinations_with_replacement(range(1, 65), 3):
        for ordinary in (0, (a + b + c) % 7):
            check((a, b, c), ordinary)
            total += 1
    reduced = 0
    for _ in range(1000):
        counts = [rng.randrange(1, 70) for _ in range(3)]
        k = rng.randrange(2, 24)
        check(counts, (-sum(counts)-3) % k, k)
        reduced += 1
    print("uniform integer-order permutations", total, "divisor histogram checks", reduced)


if __name__ == "__main__":
    main()

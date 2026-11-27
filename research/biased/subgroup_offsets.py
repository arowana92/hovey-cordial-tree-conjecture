"""Exact allowed leaf-offset totals on a star mapped onto a subgroup."""

from collections import Counter
from functools import reduce
from itertools import permutations
from math import gcd
from random import Random


def moments(counts):
    s = len(counts)
    values = [a % s for a in counts]
    freq = Counter(values)
    total = s*(s-1)//2
    if s >= 3:
        for c in freq:
            if freq[c] != s-2:
                continue
            others = [(a-c) % s for a in values if a != c]
            if len(others) == 2 and sum(others) % s == 0 and gcd(others[0], s) == 1:
                return set(range(s)) - {total*c % s}
    g = reduce(gcd, (a-values[0] for a in values), s)
    return {(total*values[0]+i) % s for i in range(0, s, g)}


def constrained(counts, offsets, q):
    s = len(counts)
    k = q*s
    parents = [v for v, n in enumerate(counts) for _ in range(n)]
    free = tuple(i for i in range(k) if i % q)
    for core in permutations(range(0, k, q)):
        inside = {(core[0]+z) % k for z in core[1:]}
        for leaves in permutations(free):
            sums = {(z+core[v]+q*off) % k for z,v,off in zip(leaves, parents, offsets)}
            if len(inside | sums) == k-1:
                return True
    return False


def main():
    tested = actual = 0
    for s in range(2, 9):
        for q in (2, 3, 4):
            def partitions(left, n, low=0):
                if n == 1:
                    if left >= low:
                        yield (left,)
                else:
                    for j in range(low, left//n+1):
                        for tail in partitions(left-j, n-1, j):
                            yield (j,) + tail
            for row in partitions((q-1)*s, s):
                # Permuting the coefficient multiset is cheaper when many counts agree.
                expected = {sum(i*a for i,a in enumerate(vals)) % s for vals in set(permutations(row))}
                assert expected == moments(row)
                tested += 1
    rng = Random(1991)
    for s, q, limit in ((2,2,100),(3,2,200),(2,3,150),(4,2,200),(3,3,100)):
        for _ in range(limit):
            counts = [0]*s
            offsets = []
            for _ in range((q-1)*s):
                counts[rng.randrange(s)] += 1
                offsets.append(rng.randrange(s))
            assert constrained(counts, offsets, q) == ((-sum(offsets)) % s in moments(counts))
            actual += 1
    print("population multisets", tested, "decorated subgroup searches", actual)


if __name__ == "__main__":
    main()

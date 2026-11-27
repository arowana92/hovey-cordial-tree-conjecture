"""Independently check endpoint sums, including the entire histogram of the core."""

from collections import Counter
from functools import lru_cache
from itertools import permutations
from random import Random

from research.census.prime_joint import short_block, caterpillar
from research.rainbow.verify import rooted_shapes


@lru_cache(None)
def brute_named(vertices, edges):
    p = len(vertices)
    # Translation places the first vertex at zero.
    for other in permutations(range(1, p)):
        row = (0,) + other
        if len({(row[a] + row[b]) % p for a, b in edges}) == p - 1:
            return dict(zip(vertices, row))
    raise AssertionError("missing base")


def solve(edges, p):
    vertices = tuple(sorted({v for edge in edges for v in edge}))
    assert len(vertices) == p
    ix = {v: i for i, v in enumerate(vertices)}
    return brute_named(vertices, tuple(sorted((ix[a], ix[b]) for a, b in edges)))


def check(edges, joint, p, c, d, labels):
    assert labels[joint] == c and all(0 <= y < p for y in labels.values())
    assert set(labels) == {v for edge in edges for v in edge}
    free = Counter(y for v, y in labels.items() if v != joint)
    weights = Counter((labels[a] + labels[b]) % p for a, b in edges)
    for bins in ([free[i] for i in range(p)],
                 [weights[i] + int(i != d) for i in range(p)]):
        assert max(bins) - min(bins) <= 1


def main():
    small = long = 0
    for p in (2, 3, 5, 7):
        for n in range(2, p + 2):
            for par in rooted_shapes(n).values():
                edges = [(a, b) for b, a in enumerate(par) if a >= 0]
                for c in range(p):
                    for d in range(p):
                        res = short_block(edges, 0, p, c, d, solve)
                        check(edges, 0, p, c, d, res)
                        small += 1
    rng = Random(1991)
    for _ in range(1900):
        s = rng.randrange(1, 61)
        edges = [(v, v + 1) for v in range(s - 1)]
        n = s
        for v in range(s):
            for _ in range(rng.randrange(9)):
                edges.append((v, n))
                n += 1
        if not edges:
            continue
        p = rng.choice((2, 3, 5, 7, 11, 17, 29, 103))
        r, c, d = rng.randrange(n), rng.randrange(p), rng.randrange(p)
        check(edges, r, p, c, d, caterpillar(edges, r, p, c, d))
        long += 1
    print("prescribed rooted blocks", small, "arbitrary-order caterpillar attachments", long)


if __name__ == "__main__":
    main()

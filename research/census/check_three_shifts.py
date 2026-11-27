"""Compare prescribed cyclic displacement counts with direct matching enumeration."""

from collections import Counter
from itertools import combinations, permutations
from random import Random

from research.census.three_shifts import match


def possible(k, rows, cols, shifts):
    out = set()
    for perm in permutations(cols):
        jumps = [(b - a) % k for a, b in zip(rows, perm)]
        if set(jumps) <= set(shifts):
            out.add(tuple(jumps.count(s) for s in shifts))
    return out


def check(k, rows, cols, shifts, quotas, expected):
    result = match(k, rows, cols, shifts, quotas)
    assert (result is not None) == expected, (k, rows, cols, shifts, quotas, expected)
    if result is not None:
        assert set(result) == set(rows) and set(result.values()) == set(cols)
        count = Counter((w-v) % k for v, w in result.items())
        assert [count[s] for s in shifts] == list(quotas)


def main():
    exact = large = 0
    for k in range(3, 6):
        for n in range(k+1):
            masks = list(combinations(range(k), n))
            for R in masks:
                for C in masks:
                    for steps in combinations(range(k), 3):
                        good = possible(k, R, C, steps)
                        for a in range(n+1):
                            for b in range(n-a+1):
                                quotas = (n-a-b, a, b)
                                check(k, R, C, steps, quotas, quotas in good)
                                exact += 1
    rng = Random(1991)
    for k in range(6, 38):
        for _ in range(30):
            steps = tuple(rng.sample(range(k), 3))
            R = rng.sample(range(k), rng.randrange(1, min(k, 7)+1))
            C = rng.sample(range(k), len(R))
            good = possible(k, R, C, steps)
            a = rng.randrange(len(R)+1)
            b = rng.randrange(len(R)-a+1)
            other = (a, b, len(R)-a-b)
            for quotas in good | {other}:
                check(k, R, C, steps, quotas, quotas in good)
                exact += 1
            used = set()
            pairs = {}
            for v in rng.sample(range(k), k):
                options = [s for s in steps if (v+s) % k not in used]
                if options and rng.randrange(5):
                    s = rng.choice(options)
                    pairs[v] = (v+s) % k
                    used.add(pairs[v])
            counts = Counter((w-v) % k for v,w in pairs.items())
            check(k, pairs, used, steps, [counts[s] for s in steps], True)
            large += 1
    print("exact permutation comparisons", exact, "planted partial matchings", large)


if __name__ == "__main__":
    main()

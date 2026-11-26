"""Direct finite checks of the caterpillar and the two-parent lift criterion."""

from itertools import combinations, permutations, product
from math import comb, gcd


def caterpillar(k, s):
    labels = [a for a in range(k) for _ in range(s)]
    parents = [-1] + [0] * (len(labels) - 1)
    parents[s] = 1
    return parents, labels


def verify():
    for k in range(2, 13):
        for s in range(2, 13):
            parents, labels = caterpillar(k, s)
            weights = [(labels[i] + labels[p]) % k for i, p in enumerate(parents) if i]
            if ([labels.count(c) for c in range(k)] != [s] * k
                    or [weights.count(c) for c in range(k)] != [s - 1] + [s] * (k - 1)):
                raise ValueError((k, s, "base counts"))

    for k, s in ((2, 3), (3, 3), (3, 4)):
        n = k * s
        parents, _ = caterpillar(k, s)
        # Translate by a multiple of k to put the first zero vertex at zero.
        choices = [list(permutations(range(c, n, k))) for c in range(k)]
        choices[0] = [row for row in choices[0] if row[0] == 0]
        for fibers in product(*choices):
            labels = sum(fibers, ())
            weights = {(labels[i] + labels[parents[i]]) % n for i in range(1, n)}
            if len(weights) == n - 1:
                raise ValueError((k, s, "unexpected lift", labels))

    for s in range(2, 13):
        for shift in range(s):
            order = s // gcd(s, shift)
            for r in range(s + 1):
                actual = 0
                for subset in combinations(range(s), r):
                    weights = {(a + (shift if a in subset else 0)) % s for a in range(s)}
                    actual += len(weights) == s
                expected = 0 if r % order else comb(s // order, r // order)
                if actual != expected:
                    raise ValueError((s, shift, r, actual, expected))
    print("Verified 121 base labelings, three exhaustive lift searches, and two-parent counts through factor 12.")


if __name__ == "__main__":
    verify()

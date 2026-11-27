"""Recount actual endpoint sums and independently search small uniform blocks."""

from collections import Counter
from itertools import combinations

from research.census.two_branch_joint import block, neutral


def check(a, b, p, c, deficit, rows, exact=False):
    k = a + b + p + 2
    assert [v for v, _, _ in rows] == list(range(k))
    parents = [-1, -1] + [0] * a + [1] * b + [-1] * p
    assert [parent for _, parent, _ in rows] == parents
    labels = [value for _, _, value in rows]
    assert set(labels) == set(range(k))
    weights = Counter((value + (c if parent == -1 else labels[parent])) % k
                      for _, parent, value in rows)
    bins = [weights[i] + int(i != deficit) for i in range(k)]
    assert max(bins) - min(bins) == 1
    if exact:
        assert len(weights) == k


def brute(a, b):
    k = a + b + 2
    all_labels = set(range(k))
    for x in range(k):
        for y in all_labels - {x}:
            free = all_labels - {x, y}
            for left in combinations(free, a):
                sums = {x, y} | {(x + z) % k for z in left}
                sums.update((y + z) % k for z in free - set(left))
                if len(sums) == k:
                    return True
    return False


def main():
    tested = uniform = impossible = brute_checks = 0
    for k in range(2, 48):
        for a in range(k - 1):
            for b in range(k - 1 - a):
                p = k - 2 - a - b
                for d in range(k):
                    c = (7 * d + a + 3 * b) % k
                    deficit = (d + 2 * c) % k
                    check(a, b, p, c, deficit, block(a, b, p, c, deficit))
                    tested += 1
            b = k - 2 - a
            rows = neutral(a, b)
            if rows is None:
                impossible += 1
            else:
                check(a, b, 0, 0, 0, rows, True)
                uniform += 1
            if k <= 12:
                assert brute(a, b) == (rows is not None)
                brute_checks += 1
    print("prescribed full blocks", tested, "uniform constructions", uniform,
          "arithmetic exclusions", impossible, "exhaustive comparisons", brute_checks)


if __name__ == "__main__":
    main()

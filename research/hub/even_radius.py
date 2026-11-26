"""Independent finite checks for the subgroup criterion and even-radius formulas."""

from itertools import permutations
from math import gcd


def exceptional_tree(s, hub_count):
    """Produce the two integer-coordinate formulas as ordinary cyclic labels."""
    parents = [-1]
    labels = [0]

    def add(parent, parity, digit):
        x = digit % s
        parents.append(parent)
        labels.append(x if x % 2 == parity else x + s)
        return len(labels) - 1

    if hub_count == 0:
        for i in range(2, s - 1):
            branch = add(0, 0, i)
            add(branch, 1, i)
        fork = add(0, 0, -1)
        add(fork, 0, 1)
        add(fork, 1, -1)
        branch = add(0, 1, 0)
        add(branch, 1, 1)
    else:
        for i in range(1, s - 2):
            branch = add(0, 0, i)
            add(branch, 1, -2 * i - 3)
        fork = add(0, 1, -1)
        add(fork, 0, -1)
        add(fork, 1, 1)
        add(0, 0, -2)
        add(0, 1, -3)
    return parents, labels


def check_formulas():
    count = 0
    for s in range(3, 258, 2):
        for hub_count in (0, 1):
            parents, labels = exceptional_tree(s, hub_count)
            child_counts = [0] * len(labels)
            weights = []
            for i in range(1, len(labels)):
                p = parents[i]
                child_counts[p] += 1
                weights.append((labels[i] + labels[p]) % (2 * s))
            branches = sorted(child_counts[i] for i, p in enumerate(parents) if p == 0)
            expected = [0] * (2 * hub_count) + [1] * (s - 2 - hub_count) + [2]
            assert branches == expected and len(weights) == 2 * s - 1
            assert set(labels) == set(range(2 * s))
            missing, = set(range(2 * s)) - set(weights)
            assert (missing % 2, missing % s) == ((1, 2) if hub_count == 0 else (0, s - 1))
            count += 1
    return count


def partitions(total, minimum=1):
    if total == 0:
        yield ()
    for first in range(minimum, total + 1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


def has_zero_product(counts):
    """Store attainable sums for each subset of the digits used so far."""
    s = len(counts)
    reachable = {0: {0}}
    for m in counts:
        next_sums = {}
        for mask, sums in reachable.items():
            for h in range(s):
                bit = 1 << h
                if not mask & bit:
                    dest = next_sums.setdefault(mask | bit, set())
                    dest.update((v + m * h) % s for v in sums)
        reachable = next_sums
    return 0 in reachable[(1 << s) - 1]


def check_exceptions():
    profiles = 0
    for s in range(5, 12):
        for parts in partitions(s):
            exceptional = ((len(parts) == 2 and gcd(parts[0], s) == 1)
                           or (s % 2 == 0 and parts == (1,) * s)
                           or (s % 2 == 1 and parts == (1,) * (s - 2) + (2,)))
            counts = parts + (0,) * (s - len(parts))
            assert has_zero_product(counts) == (not exceptional), (s, counts)
            profiles += 1
    return profiles


def distributions(total, size):
    if size == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in distributions(total - first, size - 1):
            yield (first,) + rest


def check_subgroups():
    cases = 0
    families = ((2, (-1, 0)), (3, (-1, 0)), (4, (-1, 0)), (2, (-1, 0, 0)),
                (3, (-1, 0, 0)), (2, (-1, 0, 0, 0)), (2, (-1, 0, 1, 2)))
    for q, core in families:
        s = len(core)
        k = q * s
        subgroup = set(range(0, k, q))
        complement = set(range(k)) - subgroup
        for counts in distributions(k - s, s):
            expected = actual = False
            for perm in permutations(range(1, s)):
                # Translation by a subgroup element normalizes the root to zero.
                digits = (0,) + perm
                sums = {(digits[i] + digits[core[i]]) % s for i in range(1, s)}
                if len(sums) == s - 1 and sum(m*h for m, h in zip(counts, digits)) % s == 0:
                    expected = True
            # Exhaust cyclic labels in ordinary coordinates independently.
            for rest in permutations(sorted(subgroup - {0})):
                parents = (0,) + rest
                weights = {(parents[i] + parents[core[i]]) % k for i in range(1, s)}
                if len(weights) != s - 1:
                    continue
                shifts = [p for p, m in zip(parents, counts) for _ in range(m)]
                for leaves in permutations(sorted(complement)):
                    edges = weights | {(p+x) % k for p, x in zip(shifts, leaves)}
                    if len(edges) == k - 1:
                        actual = True
                        break
                if actual:
                    break
            assert actual == expected, (q, core, counts)
            cases += 1
    return cases


if __name__ == "__main__":
    print(f"{check_formulas()} cyclic labelings of the two exceptional shapes checked.")
    print(f"{check_exceptions()} leaf partitions checked by independent scalar-product search.")
    print(f"{check_subgroups()} subgroup cases checked by exhaustive ordinary labeling.")

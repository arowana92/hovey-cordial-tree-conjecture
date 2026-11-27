"""Check prescribed-core and uniform-attachment claims using actual edge sums."""

from collections import Counter
from itertools import permutations, product
from math import gcd
from random import Random

from research.biased.pinned_periods import extend, marked_periods, uniform_star


def balanced(values, k):
    counts = Counter(values)
    sizes = [counts[t] for t in range(k)]
    return max(sizes) - min(sizes) <= 1


def check_tree(k, parents, offsets, fixed):
    labels = extend(k, parents, offsets, fixed)
    assert all(0 <= x < k for x in labels) and len(labels) == len(parents)
    assert all(labels[v] == x % k for v, x in fixed.items())
    weights = [(labels[v] + labels[p] + offsets[v]) % k
               for v, p in enumerate(parents) if v]
    assert balanced(labels, k) and balanced(weights, k)


def tree_tests(rng):
    count = 0
    for k in range(1, 5):
        for skeleton in ([-1], [-1, 0], [-1, 0, 0], [-1, 0, 1]):
            h = len(skeleton)
            for biases in product(range(k), repeat=h-1):
                parents, offsets = list(skeleton), [0, *biases]
                for v in range(1, h):
                    for _ in range(k-1):
                        parents.append(skeleton[v])
                        offsets.append(offsets[v])
                # Give all original vertices children, including the root at h=1.
                for v in range(h):
                    if v not in parents:
                        parents.append(v)
                        offsets.append(v % k)
                while len(parents) < k*h:
                    parents.append(0)
                    offsets.append(0)
                for r in range(k):
                    for pins in product(range(k), repeat=h):
                        check_tree(k, parents, offsets, dict(enumerate(pins)))
                        count += 1
                    parents.append(r % h)
                    offsets.append((r+1) % k)
    for k in range(2, 31):
        for r in range(k):
            h = rng.randrange(2, 11)
            parents = [-1] + [rng.randrange(i) for i in range(1, h)]
            offsets = [0] + [rng.randrange(k) if r % 2 else 0 for _ in range(h-1)]
            fixed = {i: (0 if r % 3 == 0 else rng.randrange(-k, 2*k)) for i in range(h)}
            for v in range(1, h):
                for _ in range(k-1):
                    parents.append(parents[v])
                    offsets.append(offsets[v])
            for v in range(h):
                if v not in parents:
                    parents.append(v)
                    offsets.append(rng.randrange(k))
            while len(parents) < k*h or len(parents) % k != r:
                parents.append(rng.randrange(h))
                offsets.append(rng.randrange(k))
            check_tree(k, parents, offsets, fixed)
            count += 1
    # Here both inner edges draw the same effective shift. All supporting
    # leaves are at one parent, and the other has no exterior leaf.
    for k in range(2, 21):
        parents = [-1, 0, 1] + [0]*(2*k-2) + [2]*(k+1)
        check_tree(k, parents, [0]*len(parents), {0: 1, 1: 1, 2: 0})
        count += 1
    return count


def weights(k, labels, offsets, children):
    return [(x+b+(labels[0] if v in children else 0)) % k
            for v, (x, b) in enumerate(zip(labels, offsets))]


def check_star(k, offsets, children, brute=None):
    n = len(offsets)
    predicted = {x for x in range(k) if (len(children)*x+sum(offsets)) % k == 0}
    assert bool(predicted) == (sum(offsets) % gcd(len(children), k) == 0)
    if brute is not None:
        seen = {row[0] for row in brute if balanced(weights(k, row, offsets, children), k)}
        assert seen == predicted
    labels = uniform_star(k, offsets, iter(children))
    assert (labels is not None) == bool(predicted)
    if labels is not None:
        assert len(labels) == n and labels[0] in predicted
        assert balanced(labels, k) and balanced(weights(k, labels, offsets, children), k)
    for x in predicted:
        shifts = [b + (x if v in children else 0) for v, b in enumerate(offsets)]
        row = marked_periods(k, shifts, {0: x})
        assert row[0] == x and balanced(row, k) and balanced(weights(k, row, offsets, children), k)


def star_tests(rng):
    exhaustive = 0
    for k in range(1, 5):
        rows = list(permutations(range(k)))
        for offsets in product(range(k), repeat=k):
            for j in range(k):
                check_star(k, offsets, set(range(1, j+1)), rows)
                exhaustive += 1
    for k, q, samples in [(2, 2, 16), (2, 3, 40), (3, 2, 45), (4, 2, 14),
                          (5, 1, 120), (6, 1, 65), (7, 1, 12)]:
        n = k*q
        rows = sorted(set(permutations(tuple(range(k))*q)))
        for _ in range(samples):
            offsets = [rng.randrange(k) for _ in range(n)]
            children = set(rng.sample(range(1, n), rng.randrange(n)))
            check_star(k, offsets, children, rows)
            exhaustive += 1
    sampled = 0
    for k in range(2, 33):
        for rep in range(14):
            n = k*rng.randrange(1, 5)
            offsets = [rng.randrange(k) for _ in range(n)]
            children = set(rng.sample(range(1, n), rng.randrange(n)))
            if rep % 2:
                offsets[0] = -sum(offsets[1:])-len(children)*rng.randrange(k)
            check_star(k, offsets, children)
            sampled += 1
    return exhaustive, sampled


if __name__ == "__main__":
    rng = Random(0xC0AD1A1)
    print(f"{tree_tests(rng):,} prescribed tree labelings checked on actual edges", flush=True)
    direct, sampled = star_tests(rng)
    print(f"{direct:,} complete center-label comparisons with brute-force histograms")
    print(f"{sampled:,} additional uniform-attachment cases through modulus 32")

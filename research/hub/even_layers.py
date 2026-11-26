"""Construct and independently check integer labelings using two seeds per degree."""

import json
from collections import Counter
from itertools import combinations_with_replacement, product
from pathlib import Path

from .branch_levels import Labeling, layer_counts, verify_tree


SMALL_BANDS = (
    ([1], []),
    ([], [-1, 1]),
    ([-1, 1, 3], []),
    ([], [-3, -1, 1, 3]),
    ([1, -1, 1, 3], [-3, -3, 2, 2, -1, 3]),
)
SIX_LOWER = [1, -3, -1, 2, 4, 3]
DEGREES = (6, *range(38, 101, 2))


def parents(c):
    result = [1, -1, 3, -3, 2, 4]
    for r in range(6, c):
        result.append(-r if r % 2 == 0 else r + 1)
    return result


def large_bands(c):
    # In increasing vertex-label order, sigma indexes the corresponding weights.
    sigma = [i + p - 1 for i, p in enumerate(reversed(SIX_LOWER))]
    for r in range(6, c + 1):
        delta = [y - i for i, y in enumerate(sigma)]
        if r % 2 == 0:
            yield [1 + d for d in reversed(delta)], []
            sigma = [y + 1 for y in sigma] + [0]
        else:
            yield [], delta[::-1]
            sigma = [r] + sigma


def load_seeds():
    path = Path(__file__).with_name("even-layer-seeds.jsonl")
    seeds = {}
    for line in path.read_text().splitlines():
        c, extra, shifts = json.loads(line)
        assert (c, extra) not in seeds
        seeds[c, extra] = shifts
    assert set(seeds) == set(product(DEGREES, range(2)))
    return seeds


def build(counts, seeds):
    c = len(counts)
    assert c in DEGREES and min(counts) >= 1
    layers = layer_counts(counts)
    assert min(layers) >= 0
    p = parents(c)
    extra = layers[4] % 2
    shifts = seeds[c, extra]
    tree = Labeling(p)
    tree.lo = -sum(p) - extra * sum(p[:5])
    tree.hi = tree.lo + 2*c + 5*extra
    labels = sorted(set(range(tree.lo, tree.hi + 1)) - {0, *p})
    assert len(labels) == len(shifts)
    for x, parent in zip(labels, shifts):
        tree.children[parent].append(x)
    layers[-1] -= 1
    layers[4] = (layers[4] - extra) // 2
    for copies, bands in zip(layers, (*SMALL_BANDS, *large_bands(c))):
        for _ in range(copies):
            tree.two_bands(bands)
    return tree


def check_bands():
    p = parents(max(DEGREES))
    for r, (lower, upper) in enumerate((*SMALL_BANDS, *large_bands(len(p))), 1):
        assert Counter(lower + upper) == Counter(p[:r] * (2 if r == 5 else 1))
        assert sorted(i - v for i, v in enumerate(lower, 1)) == list(range(len(lower)))
        assert sorted(i - v for i, v in enumerate(upper, 1)) == list(range(1, len(upper)+1))


def check():
    check_bands()
    seeds = load_seeds()
    total = 0
    for c in DEGREES:
        # The two bare seeds and profiles exercising every translation rule.
        for step, extra in product((0, 1, 2), (0, 1)):
            counts = tuple(1 + step*(c-1-i) + extra*(i < 5) for i in range(c))
            tree = build(counts, seeds)
            assert verify_tree(tree, counts) == tree.lo
            total += 1
    for asc in combinations_with_replacement(range(1, 8), 6):
        counts = asc[::-1]
        tree = build(counts, seeds)
        assert verify_tree(tree, counts) == tree.lo
        total += 1
    print(f"Verified {len(seeds)} seeds, all bands through rank 100, and {total} integer tree labelings.")


if __name__ == "__main__":
    check()

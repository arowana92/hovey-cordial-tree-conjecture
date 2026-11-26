"""Construct consecutive integer label sets for radius-two trees and check the data."""

import json
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path


def records(name):
    return [json.loads(line) for line in Path(__file__).with_name(name).read_text().splitlines()]


PAIRS = {(a, b): bands for a, b, bands in records("odd-layer-pairs.jsonl")}
FOUR = {tuple(e): seed for e, seed in records("four-branch-seeds.jsonl")}


def prefix(rank):
    return tuple(i // 2 + 1 if i % 2 == 0 else -(i // 2 + 1) for i in range(rank))


def layer_counts(counts):
    return [x - y for x, y in zip(counts, counts[1:] + (0,))]


def fold(a):
    zig = [j // 2 if j % 2 == 0 else a - 1 - j // 2 for j in range(a)]
    return zig + [a + x for x in reversed(zig)]


class Labeling:
    def __init__(self, parents):
        self.children = {p: [] for p in parents}
        self.lo = min(0, *parents)
        self.hi = max(0, *parents)

    def upper_cycle(self, positions):
        for x, y in zip(positions, positions[1:] + positions[:1]):
            self.children[y - x].append(self.hi + 1 + x)
        self.hi += len(positions)

    def path(self, positions):
        # Depth increases toward smaller labels. Position 0 is the earlier hole.
        for x, y in zip(positions, positions[1:]):
            self.children[y - x].append(self.lo - y)
        self.lo -= len(positions) - 1

    def two_bands(self, bands):
        lower, upper = bands
        for x, p in enumerate(lower, 1):
            self.children[p].append(self.lo - x)
        self.lo -= len(lower)
        for x, p in enumerate(upper, 1):
            self.children[p].append(self.hi + len(upper) + 1 - x)
        self.hi += len(upper)


def odd_core(counts):
    c = len(counts)
    m = (c - 1) // 2
    tree = Labeling(prefix(c))
    tree.children[m + 1].append(-m - 1)
    tree.lo = -m - 1
    if m:
        tree.upper_cycle(fold(m))
    layers = layer_counts(counts)
    layers[-1] -= 1
    singles = []
    for rank, num in enumerate(layers, 1):
        a = rank // 2
        if rank == 1:
            tree.path(list(range(num + 1)))
        elif rank % 2 == 0:
            for _ in range(num):
                tree.upper_cycle(fold(a))
        else:
            for _ in range(num // 2):
                tree.upper_cycle(fold(a))
                tree.path(fold(a + 1) + [2 * a + 2])
            if num % 2:
                singles.append(a)
    for a, b in zip(singles[::2], singles[1::2]):
        tree.two_bands(PAIRS[a, b])
    if len(singles) % 2:
        tree.path(fold(singles[-1] + 1))
    return tree


def four_core(counts):
    e = layer_counts(counts)
    short = (min(4, e[0]), 0, *(v if v < 4 else 4 + v % 2 for v in e[2:]))
    lo, parents, shifts = FOUR[short]
    tree = Labeling(parents)
    tree.lo, tree.hi = lo, lo + 4 + len(shifts)
    labels = sorted(set(range(tree.lo, tree.hi + 1)) - {0, *parents})
    for x, p in zip(labels, shifts):
        tree.children[p].append(x)
    tree.path(list(range(e[0] - short[0] + 1)))
    for _ in range(e[1]):
        tree.upper_cycle([0, 1])
    for _ in range((e[2] - short[2]) // 2):
        tree.path([0, 1, 2, 5, 4, 3, 6])
    for _ in range((e[3] - short[3]) // 2):
        tree.path([0, 1, 2])
        base = tree.hi + 1
        for cycle in ([0, 3, 1], [2, 5, 4]):
            for x, y in zip(cycle, cycle[1:] + cycle[:1]):
                tree.children[y - x].append(base + x)
        tree.hi += 6
    return tree


def verify_tree(tree, counts):
    vertices = [0, *tree.children]
    edges = list(tree.children)
    for p, children in tree.children.items():
        vertices.extend(children)
        edges.extend(p + x for x in children)
    assert [len(tips) for tips in tree.children.values()] == list(counts)
    assert sorted(vertices) == list(range(tree.lo, tree.hi + 1))
    assert len(set(edges)) == len(edges) and set(edges) <= set(vertices)
    missing, = set(vertices) - set(edges)
    return missing


def verify_data():
    assert set(PAIRS) == set(combinations(range(1, 17), 2))
    for (a, b), (lower, upper) in PAIRS.items():
        assert len(lower) == a + b + 2 and len(upper) == a + b
        assert Counter(lower + upper) == Counter(prefix(2*a+1) + prefix(2*b+1))
        assert sorted(x-p for x, p in enumerate(lower, 1)) == list(range(len(lower)))
        assert sorted(x-p for x, p in enumerate(upper, 1)) == list(range(1, len(upper)+1))

    assert set(FOUR) == set(product(range(5), [0], range(6), range(1, 6)))
    for e, (lo, parents, shifts) in FOUR.items():
        counts = tuple(sum(e[i:]) for i in range(4))
        assert len(parents) == len(set(parents)) == 4 and 0 not in parents
        assert parents[:2] == [1, -1]
        if max(e[2:]) >= 4:
            assert parents == [1, -1, 3, -2]
        tree = four_core(counts)
        hole = verify_tree(tree, counts)
        if max(e) >= 4:
            assert hole == lo


def verify_constructions():
    checked = 0
    for c in (1, 3, 4, 5, 7, 9):
        for asc in combinations_with_replacement(range(1, 7), c):
            counts = asc[::-1]
            tree = four_core(counts) if c == 4 else odd_core(counts)
            verify_tree(tree, counts)
            checked += 1
    for c in range(11, 34, 2):
        for step in (1, 2, 3):
            counts = tuple(step * v for v in range(c, 0, -1))
            verify_tree(odd_core(counts), counts)
            checked += 1
    return checked


if __name__ == "__main__":
    verify_data()
    print(f"{len(PAIRS)} pairs of odd layers and {len(FOUR)} four-branch seeds verified.")
    print(f"{verify_constructions()} full integer tree labelings checked.")

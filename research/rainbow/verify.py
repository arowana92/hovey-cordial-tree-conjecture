"""Check rainbow witnesses, rooted shapes, and counts of boundary colorings."""

import argparse
import gzip
import json
from collections import Counter, defaultdict
from math import comb, gcd, prod
from pathlib import Path

from research.eight.verify import check_witnesses, components, require


def rooted_shapes(order):
    """Grow rooted trees by inserting one leaf at every existing vertex."""
    trees = {"()": (-1,)}
    for size in range(1, order):
        larger = {}
        for parents in trees.values():
            for parent in range(size):
                extended = parents + (parent,)
                larger[components(extended)[0][1]] = extended
        trees = larger
    return trees


def verify(path, k, centroid=False, grouped=False):
    if centroid:
        limit = max(leaves - (leaves + 2) // 3 for leaves in range(2, k - 1))
    else:
        limit = max(leaves - 1 - leaves // 4 for leaves in range(2, k - 1))
    trees = rooted_shapes(k)
    base = set()
    coverage = defaultdict(set)
    closed_counts = {}
    previous = None
    rows = 0
    units = [a for a in range(k) if gcd(k, a) == 1]
    with gzip.open(path, "rt", encoding="ascii") as source:
        for lineno, line in enumerate(source, 1):
            try:
                kind, parents, witnesses = json.loads(line)
                require(isinstance(parents, list), "expected parent vector")
                require(all(type(p) is int and -k <= p < i for i, p in enumerate(parents)),
                        "illegal parent")
                require(isinstance(witnesses, list) and len(witnesses) == 1,
                        "expected one witness")
                roots = components(parents)
                if kind == "base":
                    require(len(parents) == k and len(roots) == 1, "invalid base")
                    check_witnesses(kind, parents, witnesses, k)
                    base.add(roots[0][1])
                    continue
                require(kind == "rainbow" and len(parents) == k - 1, "invalid forest")
                labels, = witnesses
                require(isinstance(labels, list) and all(type(x) is int for x in labels)
                        and sorted(labels) == list(range(1, k)), "invalid vertex labels")
                weights = [(labels[i] + (labels[p] if p >= 0 else -1 - p)) % k
                           for i, p in enumerate(parents)]
                require(len(set(weights)) == k - 1, "repeated edge weight")
                shape = tuple(sorted(code for _, code in roots))
                if grouped and previous is not None and shape != previous:
                    closed_counts[previous] = len(coverage.pop(previous))
                    require(shape not in closed_counts, "shape appears in multiple groups")
                previous = shape
                for a in units:
                    pairs = sorted((code, a * color % k) for color, code in roots)
                    coverage[shape].add(tuple(c for _, c in pairs))
                rows += 1
            except (TypeError, ValueError, IndexError) as error:
                raise ValueError(f"record {lineno}: {error}") from error

    if grouped and previous is not None:
        closed_counts[previous] = len(coverage.pop(previous))
    require(base == set(trees), "base tree coverage failed")
    shapes_checked = all_colorings = 0
    for parents in trees.values():
        # Delete the dummy root. Its children become component roots.
        forest = tuple(p - 1 for p in parents[1:])
        leaves = len(forest) - len({p for p in forest if p >= 0})
        if leaves > limit:
            continue
        shape = tuple(sorted(code for _, code in components(forest)))
        # The colors on c identical components form a multiset of size c.
        count = prod(comb(k + c - 1, c) for c in Counter(shape).values())
        actual = closed_counts.pop(shape, 0) if grouped else len(coverage.pop(shape, set()))
        require(actual == count, f"shape {shape} covers {actual} of {count}")
        all_colorings += count
        shapes_checked += 1
    require(not coverage and not closed_counts, "unexpected forest shape")
    print(f"k={k}: {len(base)} base trees, {shapes_checked} forest shapes, "
          f"{rows} witness rows, {all_colorings} boundary colorings; leaf limit {limit}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modulus", type=int)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--centroid", action="store_true", help="use the leaf-centroid bound")
    parser.add_argument("--grouped", action="store_true",
                        help="release each forest shape after its consecutive records")
    args = parser.parse_args()
    if args.modulus < 5:
        parser.error("this reduction uses k >= 5")
    verify(args.certificate, args.modulus, args.centroid, args.grouped)

"""Generate base and rooted-forest rainbow witnesses as JSON Lines."""

import argparse
from itertools import combinations_with_replacement, groupby, product
from math import gcd

from research.eight.generate import emit, forests, parent_vector


def leaf_count(tree):
    return sum(leaf_count(child) for child in tree) if tree else 1


def boundary_orbits(forest, k):
    """Identify equal components and multiply all boundary labels by a unit."""
    sizes = [len(tuple(group)) for _, group in groupby(forest)]
    choices = [combinations_with_replacement(range(k), size) for size in sizes]
    units = [u for u in range(2, k) if gcd(u, k) == 1]
    for groups in product(*choices):
        for u in units:
            image = tuple(tuple(sorted(u * c % k for c in group)) for group in groups)
            if image < groups:
                break
        else:
            yield tuple(c for group in groups for c in group)


def rainbow(parents, k):
    labels = []

    def choose(available, weights):
        i = len(labels)
        if i == len(parents):
            return True
        p = parents[i]
        parent_label = -1 - p if p < 0 else labels[p]
        candidates = available
        while candidates:
            bit = candidates & -candidates
            candidates -= bit
            label = bit.bit_length() - 1
            weight = 1 << ((parent_label + label) % k)
            if weights & weight:
                continue
            labels.append(label)
            if choose(available - bit, weights | weight):
                return True
            labels.pop()
        return False

    if not choose((1 << k) - 2, 0):
        raise ValueError(f"No rainbow extension at modulus {k} for {parents}")
    return labels


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modulus", type=int)
    parser.add_argument("--centroid", action="store_true", help="use the leaf-centroid bound")
    args = parser.parse_args()
    k = args.modulus
    if k < 5:
        parser.error("this reduction uses k >= 5")
    for root in forests(k - 1):
        parents = parent_vector((root,), (0,))
        remaining = [p - 1 for p in parents[1:]]
        emit("base", parents, [[0] + rainbow(remaining, k)])
    limit = 2 * (k - 2) // 3 if args.centroid else k - 3 - (k - 2) // 4
    for forest in forests(k - 1):
        if sum(leaf_count(tree) for tree in forest) > limit:
            continue
        for colors in boundary_orbits(forest, k):
            parents = parent_vector(forest, colors)
            emit("rainbow", parents, [rainbow(parents, k)])


if __name__ == "__main__":
    main()

"""Generate base and rooted-forest rainbow witnesses as JSON Lines."""

import argparse
from functools import lru_cache
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


@lru_cache(maxsize=None)
def tree_size(tree):
    return 1 + sum(tree_size(child) for child in tree)


@lru_cache(maxsize=None)
def color_vectors(k, groups):
    units = [a for a in range(2, k) if gcd(a, k) == 1]
    return tuple(colors for colors in product(range(k), repeat=groups)
                 if all(colors <= tuple(a * c % k for c in colors) for a in units))


@lru_cache(maxsize=None)
def spine_vectors(k, gaps):
    feasible = []
    for colors in color_vectors(k, len(gaps)):
        runs = 1
        for i in range(1, len(gaps)):
            if colors[i] != colors[i - 1]:
                if gaps[i] < runs:
                    break
                runs += 1
        else:
            feasible.append(colors)
    return tuple(feasible)


def ordered_boundaries(forest, k, spine=False):
    """In a size-sorted traversal, a new boundary needs a larger component
    than all earlier groups combined."""
    group_of = [0] * len(forest)
    gaps = []
    mass = 0
    for i in sorted(range(len(forest)), key=lambda j: tree_size(forest[j])):
        size = tree_size(forest[i])
        if size > mass:
            gaps.append(size - mass)
        group_of[i] = len(gaps) - 1
        mass += size
    choices = spine_vectors(k, tuple(gaps)) if spine else color_vectors(k, len(gaps))
    for colors in choices:
        yield tuple(colors[g] for g in group_of)


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


def native_search(library, k):
    import ctypes
    from pathlib import Path

    solve = ctypes.CDLL(str(Path(library).resolve())).rainbow_witness
    vector = ctypes.c_int * (k - 1)
    solve.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    solve.restype = ctypes.c_int
    output = vector()

    def witness(parents, modulus):
        if len(parents) != k - 1 or modulus != k or not 2 <= k <= 63:
            raise ValueError("invalid native search dimensions")
        if solve(k, vector(*parents), output) != 1:
            raise ValueError(f"No native rainbow witness at modulus {k} for {parents}")
        return list(output)

    return witness


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modulus", type=int)
    parser.add_argument("--centroid", action="store_true", help="use the leaf-centroid bound")
    parser.add_argument("--ordered", action="store_true",
                        help="use size-ordered branches after the leaf-centroid cut")
    parser.add_argument("--spine", action="store_true", help="use the exact ordered-cut profile")
    parser.add_argument("--native", metavar="LIBRARY", help="optional compiled search.cpp")
    args = parser.parse_args()
    k = args.modulus
    if k < 5:
        parser.error("this reduction uses k >= 5")
    witness = native_search(args.native, k) if args.native else rainbow
    for root in forests(k - 1):
        parents = parent_vector((root,), (0,))
        remaining = [p - 1 for p in parents[1:]]
        emit("base", parents, [[0] + witness(remaining, k)])
    limit = 2 * (k - 2) // 3 if args.centroid or args.ordered or args.spine else k - 3 - (k - 2) // 4
    for forest in forests(k - 1):
        if sum(leaf_count(tree) for tree in forest) > limit:
            continue
        choices = (ordered_boundaries(forest, k, args.spine) if args.ordered or args.spine
                   else boundary_orbits(forest, k))
        for colors in choices:
            parents = parent_vector(forest, colors)
            emit("rainbow", parents, [witness(parents, k)])


if __name__ == "__main__":
    main()

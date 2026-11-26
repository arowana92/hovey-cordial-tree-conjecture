"""Generate JSON Lines on stdout. Use gzip -n to archive the stream."""

import argparse
import json
from functools import lru_cache
from itertools import permutations


@lru_cache(maxsize=None)
def forests(size):
    """A forest is a sorted tuple of trees. A tree is its forest of children."""
    if size == 0:
        return ((),)
    result = []
    for first_size in range(1, size + 1):
        for first in forests(first_size - 1):
            for rest in forests(size - first_size):
                if not rest or first <= rest[0]:
                    result.append((first,) + rest)
    return tuple(result)


def boundary_labels(forest, k, chosen=()):
    i = len(chosen)
    if i == len(forest):
        yield chosen
        return
    # Translate the color of one component of the first shape to zero.
    # Within each group of identical shapes we can then sort the colors.
    lower = chosen[-1] if i and forest[i] == forest[i - 1] else 0
    for color in range(lower, k if i else 1):
        yield from boundary_labels(forest, k, chosen + (color,))


def parent_vector(forest, colors):
    parents = []

    def visit(tree, parent):
        index = len(parents)
        parents.append(parent)
        for child in tree:
            visit(child, index)

    for tree, color in zip(forest, colors):
        visit(tree, -1 - color)
    return parents


def base_witness(parents, k):
    # Translation lets the first vertex take zero.
    for tail in permutations(range(1, k)):
        labels = (0,) + tail
        weights = {(labels[i] + labels[parents[i]]) % k for i in range(1, k)}
        if len(weights) == k - 1:
            return labels
    raise ValueError(f"No base witness for {parents}")


def extension_witnesses(parents, k):
    """Collect injections covering all possible deficient weights of the core."""
    target_set = (1 << k) - 1
    covered = 0
    witnesses = []
    labels = []

    def assign(used_labels, used_weights, doubled):
        nonlocal covered
        i = len(labels)
        if i == len(parents):
            # When weights are distinct, each present weight is a valid target.
            # When one repeats, only the repeated weight is a valid target.
            targets = doubled or used_weights
            if targets & ~covered:
                covered |= targets
                witnesses.append(tuple(labels))
            return
        parent = parents[i]
        boundary = -1 - parent if parent < 0 else labels[parent]
        for label in range(k):
            if covered == target_set:
                break
            label_bit = 1 << label
            weight_bit = 1 << ((boundary + label) % k)
            repeat = used_weights & weight_bit
            if used_labels & label_bit or (repeat and (doubled or covered & repeat)):
                continue
            labels.append(label)
            assign(used_labels | label_bit, used_weights | weight_bit, doubled | repeat)
            labels.pop()

    assign(0, 0, 0)
    if covered != target_set:
        raise ValueError(f"Extension failed for {parents}, target mask {covered}")
    return witnesses


def emit(kind, parents, witnesses):
    print(json.dumps([kind, parents, witnesses], separators=(",", ":")))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--modulus", type=int, default=8)
    k = parser.parse_args().modulus
    if k < 1:
        parser.error("the modulus must be positive")
    for children in forests(k - 1):
        parents = parent_vector((children,), (0,))
        emit("base", parents, [base_witness(parents, k)])
    for size in range(1, k + 1):
        for forest in forests(size):
            for colors in boundary_labels(forest, k):
                parents = parent_vector(forest, colors)
                emit("extension", parents, extension_witnesses(parents, k))


if __name__ == "__main__":
    main()

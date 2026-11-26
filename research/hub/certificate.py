"""Integer labelings for rooted trees to which arbitrary leaves may be added."""

import argparse
import gzip
import json
from pathlib import Path

from research.eight.generate import forests, parent_vector
from research.eight.verify import components, require
from research.rainbow.verify import rooted_shapes


def find_labels(parents, center):
    n = len(parents)
    full = (1 << n) - 1
    slots = [center]

    def assign(used, weights):
        i = len(slots)
        if i == n:
            return True
        # With the root's slot representing zero, edge slot = child slot + offset.
        offset = slots[parents[i]] - center
        available_weights = full ^ weights
        valid_slots = (available_weights >> offset if offset >= 0
                       else available_weights << -offset)
        candidates = (full ^ used) & valid_slots
        while candidates:
            bit = candidates & -candidates
            candidates -= bit
            slot = bit.bit_length() - 1
            slots.append(slot)
            if assign(used | bit, weights | (1 << (slot + offset))):
                return True
            slots.pop()
        return False

    if assign(1 << center, 0):
        return [a - center for a in slots]
    return None


def generate(n):
    for children in forests(n - 1):
        parents = parent_vector((children,), (0,))
        for center in reversed(range((n - 1) // 2 + 1)):
            labels = find_labels(parents, center)
            if labels is not None:
                print(json.dumps([parents, labels], separators=(",", ":")))
                break
        else:
            raise ValueError(f"No interval witness for {parents}")


def verify(n, path):
    required = set(rooted_shapes(n))
    count = 0
    with gzip.open(path, "rt", encoding="ascii") as src:
        for line in src:
            parents, labels = json.loads(line)
            require(len(parents) == n and parents[0] == -1 and
                    all(type(p) is int and 0 <= p < i for i, p in enumerate(parents) if i),
                    "invalid rooted tree")
            require(len(labels) == n and labels[0] == 0 and
                    all(type(a) is int for a in labels), "invalid integer labeling")
            vertices = set(labels)
            edges = {labels[i] + labels[parents[i]] for i in range(1, n)}
            require(len(vertices) == n and max(vertices) - min(vertices) == n - 1,
                    "labels do not fill an integer interval")
            require(len(edges) == n - 1 and edges <= vertices, "invalid edge sums")
            shape = components(parents)[0][1]
            require(shape in required, "unexpected or duplicate rooted tree")
            required.remove(shape)
            count += 1
    require(not required, "uncovered rooted tree")
    print(f"Verified integer labelings on all {count} rooted trees of order {n}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("order", type=int)
    parser.add_argument("--verify", type=Path, metavar="ARCHIVE")
    args = parser.parse_args()
    if args.order < 1:
        parser.error("positive order required")
    if args.verify:
        verify(args.order, args.verify)
    else:
        generate(args.order)

"""Verify witness histograms and coverage by leaf insertion. No search imports."""

import argparse
import gzip
import json
from itertools import product
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def components(parents):
    """Canonical parenthesis code of each rooted component, with boundary color."""
    children = [[] for _ in parents]
    roots = []
    for vertex in reversed(range(len(parents))):
        code = "(" + "".join(sorted(children[vertex])) + ")"
        parent = parents[vertex]
        if parent < 0:
            roots.append((-parent - 1, code))
        else:
            children[parent].append(code)
    return roots


def key(roots, shift, k):
    return tuple(sorted(((color + shift) % k, code) for color, code in roots))


def check_witnesses(kind, parents, witnesses, k):
    targets = set()
    require(witnesses, "missing witness")
    for labels in witnesses:
        require(isinstance(labels, list) and len(labels) == len(parents), "wrong witness length")
        require(all(type(x) is int and 0 <= x < k for x in labels), "invalid residue")
        vertices = [labels.count(i) for i in range(k)]
        require(max(vertices) == 1, "vertex labels must be distinct")
        edges = [0] * k
        for vertex, parent in enumerate(parents):
            if kind == "base" and vertex == 0:
                continue
            other = labels[parent] if parent >= 0 else -parent - 1
            edges[(labels[vertex] + other) % k] += 1
        if kind == "base":
            require(edges.count(0) == 1 and max(edges) <= 1, "invalid base edge counts")
        else:
            for deficit in range(k):
                # Core of order k has counts 0 at deficit and 1 elsewhere.
                # Every larger multiple adds the same constant to these counts.
                combined = [n + int(i != deficit) for i, n in enumerate(edges)]
                if min(combined) < 1 or max(combined) > 2:
                    continue
                if len(parents) == k:
                    require(combined.count(1) == 1, "invalid next deficit")
                targets.add(deficit)
    if kind == "extension":
        require(targets == set(range(k)), f"missing targets {set(range(k)) - targets}")


def verify(path, k):
    base_shapes = set()
    rows = [[] for _ in range(k + 1)]
    keys = [set() for _ in range(k + 1)]
    rows[0].append(())
    with gzip.open(path, "rt", encoding="ascii") as source:
        for number, line in enumerate(source, 1):
            try:
                kind, parents, witnesses = json.loads(line)
                require(kind in ("base", "extension"), "unknown record kind")
                require(isinstance(parents, list) and isinstance(witnesses, list), "expected lists")
                size = len(parents)
                require(1 <= size <= k, "invalid order")
                for vertex, p in enumerate(parents):
                    require(type(p) is int and -k <= p < vertex, "invalid parent")
                roots = components(parents)
                if kind == "base":
                    require(size == k and len(roots) == 1, "invalid base tree")
                check_witnesses(kind, parents, witnesses, k)
                if kind == "base":
                    base_shapes.add(roots[0][1])
                else:
                    rows[size].append(tuple(parents))
                    keys[size].update(key(roots, shift, k) for shift in range(k))
            except (ValueError, TypeError, IndexError) as error:
                raise ValueError(f"record {number}: {error}") from error

    # Any rooted k-vertex tree can be numbered with parents before children.
    # Enumerate every corresponding parent vector before testing its shape.
    for tail in product(*(range(i) for i in range(1, k))):
        code = components((-1,) + tail)[0][1]
        require(code in base_shapes, f"missing base tree {code}")
    print(f"Verified {len(base_shapes)} rooted base shapes at order {k}.")

    # Completeness by induction. Deleting a leaf either shortens a component
    # or removes a singleton. Reverse both operations at every possible parent.
    for size in range(1, k + 1):
        for smaller in rows[size - 1]:
            for parent in range(-k, size - 1):
                candidate = key(components(smaller + (parent,)), 0, k)
                require(candidate in keys[size], f"missing forest {candidate}")
        print(f"Order {size}: {len(rows[size])} rows, "
              f"{len(keys[size])} colored forests, all {k} targets verified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", nargs="?", type=Path,
                        default=Path(__file__).with_name("certificate.jsonl.gz"))
    parser.add_argument("--modulus", type=int, default=8)
    args = parser.parse_args()
    if args.modulus < 1:
        parser.error("the modulus must be positive")
    verify(args.certificate, args.modulus)

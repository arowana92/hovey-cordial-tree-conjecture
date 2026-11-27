"""Independent core recognition, exact seed checks, and coverage of every population."""

import argparse
from itertools import groupby
from math import factorial
from pathlib import Path

from research.hub.ranked_core_verify import check_coverage, check_record, read


def check_tree(edges, h):
    assert len(edges) == h-1 and tuple(sorted(set(edges))) == edges
    adjacency = [set() for _ in range(h)]
    for a, b in edges:
        assert 0 <= a < b < h
        adjacency[a].add(b)
        adjacency[b].add(a)
    reached = {0}
    for _ in range(h-1):
        reached.update(w for v in tuple(reached) for w in adjacency[v])
    assert len(reached) == h and 2 < max(map(len, adjacency)) < h-1


def verify(path, h):
    seen = set()
    rows = grid = double = largest = 0
    for key, group in groupby(read(path), key=lambda r: tuple(map(tuple, r[0]))):
        assert key not in seen
        seen.add(key)
        check_tree(key, h)
        cells = []
        for _, base, steps, witness in group:
            check_record(key, base, steps, witness)
            largest = max(largest, len(witness[1])+len(witness[2]))
            double += max(steps) > 1
            cells.append((base, steps))
            rows += 1
        grid += check_coverage(cells)
    # Cayley's formula, removing all labeled paths and all labeled stars.
    expected = h**(h-2) - factorial(h)//2 - h
    assert len(seen) == expected
    print(f"Order {h}: {expected} ranked cores, {rows} cells, {double} with repeated layers, "
          f"largest seed {largest}, {grid} coverage representatives.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("order", type=int, choices=(6, 7))
    parser.add_argument("certificate", type=Path, nargs="?")
    args = parser.parse_args()
    path = args.certificate or Path(__file__).with_name(f"ranked-cores-{args.order}.jsonl.gz")
    verify(path, args.order)

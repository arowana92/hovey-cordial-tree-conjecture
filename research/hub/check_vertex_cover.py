"""Check marked cores and count their geometries independently by bipartite Prüfer words."""

import argparse
from collections import Counter
from itertools import groupby, product
from math import factorial, prod
from pathlib import Path

from research.hub.ranked_core_verify import check_coverage, check_record, read


def expected(d, u):
    count = 0
    for multiplicities in product(range(u+1), repeat=d-1):
        if sum(multiplicities) != u:
            continue
        direct = d-1 - sum(i*n for i, n in enumerate(multiplicities, 1))
        if direct < 0:
            continue
        divisor = factorial(direct) * prod(factorial(n)*factorial(i)**n
                                           for i, n in enumerate(multiplicities, 1))
        term, rem = divmod(d**(u+direct-1) * factorial(d-1), divisor)
        assert rem == 0
        count += term
    return count


def check(path, d):
    seen = set()
    shapes = Counter()
    rows = grid = largest = 0
    for edges, records in groupby(read(path), key=lambda r: tuple(map(tuple, r[0]))):
        h = len(edges)+1
        u = h-d
        assert h >= 8 and 1 <= u <= d-1
        assert tuple(sorted(set(edges))) == edges
        adjacency = [set() for _ in range(h)]
        for i, j in edges:
            assert 0 <= i < j < h and i < d
            adjacency[i].add(j)
            adjacency[j].add(i)
        reached = {0}
        for _ in range(h-1):
            reached.update(w for v in tuple(reached) for w in adjacency[v])
        assert len(reached) == h and all(len(n) >= 2 for n in adjacency[d:])
        direct = tuple((i,j) for i,j in edges if j < d)
        junctions = tuple(sorted(tuple(sorted(n)) for n in adjacency[d:]))
        key = direct, junctions
        assert key not in seen
        seen.add(key)
        shapes[u] += 1
        cells = []
        for _, base, steps, witness in records:
            assert base[d:] == steps[d:] == [0]*u
            check_record(edges, base, steps, witness)
            cells.append((base[:d], steps[:d]))
            largest = max(largest, len(witness[1])+len(witness[2]))
            rows += 1
        grid += check_coverage(cells)
    for u in range(8-d, d):
        assert shapes[u] == expected(d, u)
    print(f"{d} sites: {sorted(shapes.items())} by junction count, {rows} cells, "
          f"largest seed {largest}, {grid} coverage representatives.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sites", type=int, choices=(5, 6))
    args = parser.parse_args()
    check(Path(__file__).with_name(f"vertex-cover-{args.sites}.jsonl.gz"), args.sites)

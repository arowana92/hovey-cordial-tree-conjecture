"""Certificates for unrestricted leaf counts on ranked double-star cores."""

import argparse
from itertools import combinations, groupby
import json
from pathlib import Path

from research.hub.ranked_core_cover import cover
from research.hub.ranked_core_generate import load_native
from research.hub.ranked_core_verify import check_coverage, check_record, read


def ranked_splits(h, a):
    for u in range(h):
        for v in range(h):
            if u == v or (2*a == h-2 and v < u):
                continue
            rest = set(range(h))-{u,v}
            for left in combinations(sorted(rest), a):
                edges = [(u,v)] + [(u,i) for i in left] + [(v,i) for i in rest-set(left)]
                yield tuple(sorted(tuple(sorted(e)) for e in edges))


def generate(h, library):
    for a in range(1, (h-2)//2+1):
        for edges in ranked_splits(h, a):
            rows = cover(library, edges)
            if rows is None:
                raise RuntimeError(f"no interval certificate for {edges}")
            for row in rows:
                print(json.dumps(row, separators=(",", ":")))


def verify(h):
    path = Path(__file__).with_name(f"double-core-{h}.jsonl.gz")
    seen = set()
    rows = representatives = largest = 0
    for edges, records in groupby(read(path), key=lambda r: tuple(map(tuple,r[0]))):
        assert len(edges) == h-1 and tuple(sorted(set(edges))) == edges and edges not in seen
        adjacency = [set() for _ in range(h)]
        for i,j in edges:
            assert 0 <= i < j < h
            adjacency[i].add(j)
            adjacency[j].add(i)
        u,v = [i for i,n in enumerate(adjacency) if len(n)>1]
        assert v in adjacency[u] and adjacency[u] | adjacency[v] == set(range(h))
        seen.add(edges)
        cells = []
        for _, base, steps, witness in records:
            check_record(edges, base, steps, witness)
            cells.append((base, steps))
            largest = max(largest, len(witness[1])+len(witness[2]))
            rows += 1
        representatives += check_coverage(cells)
    # Choose the unordered pair of centers, then a nonconstant binary assignment.
    assert len(seen) == h*(h-1)//2 * (2**(h-2)-2)
    print(f"Order {h}: {len(seen)} ranked double stars, {rows} cells, "
          f"largest seed {largest}, {representatives} coverage representatives.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("order", type=int, choices=(8,9))
    parser.add_argument("--generate", metavar="NATIVE_LIBRARY")
    args = parser.parse_args()
    if args.generate:
        generate(args.order, load_native(args.generate))
    else:
        verify(args.order)

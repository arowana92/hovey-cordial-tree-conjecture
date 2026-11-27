"""Generate marked nonleaf cores by their direct edges and junction neighborhoods."""

import argparse
from itertools import combinations
import json

from research.hub.ranked_core_cover import cover
from research.hub.ranked_core_generate import load_native


def parts(count, total, minimum=1):
    if not count:
        if total == 0:
            yield ()
        return
    for n in range(minimum, total//count+1):
        for tail in parts(count-1, total-n, n):
            yield (n,) + tail


def geometries(d, u):
    def grow(groups, previous, edges, pending, next_junction):
        if not pending:
            yield tuple(sorted(edges))
            return
        kind = pending[0]
        size, direct = kind
        for vertices in combinations(range(d), size):
            if previous is not None and kind == previous[0] and vertices <= previous[1]:
                continue
            touching = [group for group in groups if group.intersection(vertices)]
            if len(touching) != size:
                continue  # Two sites already connected would close a cycle.
            joined = [group for group in groups if group not in touching] + [set.union(*touching)]
            new_edges = [vertices] if direct else [(i, next_junction) for i in vertices]
            yield from grow(joined, (kind, vertices), edges+new_edges, pending[1:],
                            next_junction + int(not direct))

    for direct in range(d-u):
        for excess in parts(u, d-1-direct):
            slots = [(j+1, False) for j in excess] + [(2, True)]*direct
            yield from grow([{i} for i in range(d)], None, [], slots, d)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sites", type=int, choices=(5, 6))
    parser.add_argument("library")
    args = parser.parse_args()
    library = load_native(args.library)
    for u in range(8-args.sites, args.sites):
        for edges in geometries(args.sites, u):
            records = cover(library, edges, args.sites)
            if records is None:
                raise RuntimeError(f"no certificate found for {edges}")
            for record in records:
                print(json.dumps(record, separators=(",", ":")))


if __name__ == "__main__":
    main()

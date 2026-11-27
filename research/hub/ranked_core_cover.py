"""Cover all ranked leaf populations at one nonleaf-core order by interval seeds."""

import argparse
from functools import lru_cache
from itertools import permutations
import json

from research.hub.ranked_core_generate import load_native, seed
from research.rainbow.verify import rooted_shapes


def core_shapes(order):
    seen = set()
    for parents in rooted_shapes(order).values():
        adjacency = [[] for _ in parents]
        edges = []
        for v, p in enumerate(parents[1:], 1):
            adjacency[v].append(p)
            adjacency[p].append(v)
            edges.append((p, v))
        if max(map(len, adjacency)) in (2, order-1):
            continue  # Paths and stars have separate integer constructions.

        def encode(v, parent):
            return "(" + "".join(sorted(encode(w, v) for w in adjacency[v] if w != parent)) + ")"

        signature = min(encode(v, -1) for v in range(order))
        if signature not in seen:
            seen.add(signature)
            yield edges


def rankings(edges):
    order = len(edges)+1
    return sorted({tuple(sorted(tuple(sorted((p[v], p[w]))) for v, w in edges))
                   for p in permutations(range(order))})


def split(base, steps, i, periodic):
    other = list(base)
    other[i] += steps[i]
    refined = list(steps)
    refined[i] = 2*steps[i] if periodic else 0
    return ((base, tuple(refined)), (tuple(other), tuple(refined) if periodic else steps))


def cover(library, edges):
    h = len(edges)+1
    reserved = sum(sum(v in edge for edge in edges) == 1 for v in range(h))
    priority = [2, 4, *range(5, h), 3, 1, 0]

    @lru_cache(None)
    def attempt(base, steps):
        if h + reserved + sum(i*n for i, n in enumerate(base, 1)) > 62:
            return None
        return seed(library, edges, base, steps)

    def certified(cells):
        return [(edges, b, s, attempt(b, s)) for b, s in cells]

    def visit(base, steps):
        if attempt(base, steps) is not None:
            return certified([(base, steps)])
        options = []
        for i in priority:
            if not steps[i] or base[i] >= 2:
                continue
            children = split(base, steps, i, False)
            score = sum(attempt(*c) is not None for c in children)
            if score == 2:
                return certified(children)
            options.append((-score, 0, i, children))
        if all(o[0] == 0 for o in options) or sum(base) >= 4:
            for i in (j for j in priority if j > 0):
                if steps[i] != 1:
                    continue
                children = split(base, steps, i, True)
                score = sum(attempt(*c) is not None for c in children)
                if score == 2:
                    return certified(children)
                if score:
                    options.append((-score, 1, i, children))
        for _, _, _, children in sorted(options):
            first = visit(*children[0])
            if first is not None:
                second = visit(*children[1])
                if second is not None:
                    return first + second
        return None

    return visit((0,)*h, (1,)*h)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("order", type=int, choices=(6, 7))
    parser.add_argument("library")
    args = parser.parse_args()
    library = load_native(args.library)
    for shape in core_shapes(args.order):
        for edges in rankings(shape):
            records = cover(library, edges)
            if records is None:
                raise RuntimeError(f"seed search exhausted for {edges}")
            for record in records:
                print(json.dumps(record, separators=(",", ":")))


if __name__ == "__main__":
    main()

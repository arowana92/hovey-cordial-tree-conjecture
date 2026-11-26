"""Check all marked skeletons, path parities, population cells, and integer seeds."""

import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path

DATA = Path(__file__).with_name("marked-leaf-seeds.jsonl")


def required(m):
    keys = set()
    for h in range(m, 2*m-1):
        for edges in combinations(combinations(range(h), 2), h-1):
            neighbors = [set() for _ in range(h)]
            for u, v in edges:
                neighbors[u].add(v)
                neighbors[v].add(u)
            if any(len(s) < 3 for s in neighbors[m:]):
                continue
            reached = {0}
            for _ in range(h):
                reached.update(set().union(*(neighbors[v] for v in reached)))
            if len(reached) != h:
                continue
            names = list(range(h))
            canon = []
            for perm in permutations(range(m, h)):
                names[m:] = perm
                canon.append(tuple(sorted(tuple(sorted((names[u], names[v]))) for u, v in edges)))
            if tuple(edges) == min(canon):
                keys.update((m, tuple(edges), mask) for mask in range(1 << (h-1)))
    return keys


def expanded(edges, mask):
    result = []
    vertex = len(edges)+1
    for j, (u, v) in enumerate(edges):
        if mask & (1 << j):
            result.extend(((u, vertex), (vertex, v)))
            vertex += 1
        else:
            result.append((u, v))
    return result


def check_seed(m, edges, seed):
    lo, hi, f, parents = seed
    assert len(f) == len(set(f)) == len(edges)+1
    assert set(f) <= set(range(lo, hi+1))
    assert set(parents) <= set(f[:m])
    rows = sorted(set(range(lo, hi+1)) - set(f))
    assert len(rows) == len(parents)
    weights = [f[u]+f[v] for u, v in edges]
    weights += [x+p for x, p in zip(rows, parents)]
    assert sorted(weights) == list(range(lo+1, hi+1))
    if m == 3:
        assert f[:3] == [0, 2, -1]
    else:
        assert {0, 1} <= set(f[:4]) and min(f[:4]) < 0 and max(f[:4]) > 1
    return f[:m]


def check_cell(edges, node, simplex):
    if isinstance(node, dict):
        i, j = node["cut"]
        assert 0 <= i < j < 4 and len(node["children"]) == 2
        mid = tuple((x+y)/2 for x, y in zip(simplex[i], simplex[j]))
        parts = []
        for slot, child in zip((i, j), node["children"]):
            sub = simplex.copy()
            sub[slot] = mid
            parts.append(check_cell(edges, child, sub))
        return sum(n for n, eta in parts), min(eta for n, eta in parts)
    f = check_seed(4, edges, node)
    ratios = []
    for v in simplex:
        moment = sum(x*y for x, y in zip(f, v))
        slack = min(moment, 1-moment)
        assert slack >= 0
        if v[-1]:
            assert slack > 0
            ratios.append(slack/v[-1])
    assert ratios
    return 1, min(ratios)


def check(path=DATA):
    remaining = required(3) | required(4)
    rows, cells = Counter(), 0
    margins = []
    for line in path.read_text().splitlines():
        m, skeleton, mask, node = json.loads(line)
        key = (m, tuple(map(tuple, skeleton)), mask)
        assert key in remaining
        remaining.remove(key)
        rows[m] += 1
        edges = expanded(skeleton, mask)
        if m == 3:
            check_seed(3, edges, node)
        else:
            simplex = [tuple(Fraction(int(j < r), r) for j in range(4)) for r in range(1, 5)]
            size, eta = check_cell(edges, node, simplex)
            cells += size
            margins.append(eta)
    assert not remaining
    print(f"{rows[3]} three-site and {rows[4]} four-site geometries, "
          f"{cells} four-site cells, minimum slack factor {min(margins)}.")


if __name__ == "__main__":
    import sys
    check(Path(sys.argv[1]) if len(sys.argv) == 2 else DATA)

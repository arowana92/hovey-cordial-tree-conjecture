"""Regenerate the marked-site certificates from a C++17 shared library."""

import ctypes
import json
import sys
from itertools import accumulate, combinations, permutations, product
from math import gcd
from pathlib import Path


def prufer(code):
    degrees = [1+code.count(i) for i in range(len(code)+2)]
    edges = []
    for v in code:
        leaf = degrees.index(1)
        edges.append((leaf, v))
        degrees[leaf] -= 1
        degrees[v] -= 1
    edges.append(tuple(i for i, degree in enumerate(degrees) if degree))
    return edges


def skeletons(m):
    found = set()
    for h in range(m, 2*m-1):
        for code in product(range(h), repeat=h-2):
            if any(code.count(i) < 2 for i in range(m, h)):
                continue
            edges = prufer(code)
            alternatives = []
            for perm in permutations(range(m, h)):
                order = tuple(range(m)) + perm
                alternatives.append(tuple(sorted(tuple(sorted((order[u], order[v])))
                                                 for u, v in edges)))
            found.add(min(alternatives))
    return sorted(found)


def array(values):
    return (ctypes.c_int*len(values))(*values)


def search(library, edges, m, patterns):
    edges_array = array([x for edge in edges for x in edge])
    h = len(edges)+1
    out = (ctypes.c_int*100)()
    for radius, attempts in ((4, 1000), (6, 3000), (8, 12000), (10, 20000)):
        for f in patterns:
            if library.fit(h, m, radius, attempts, edges_array, array(f), out):
                lo, hi = out[:2]
                labels = out[2:2+h]
                parents = [out[2+h+x-lo] for x in range(lo, hi+1) if x not in labels]
                return [lo, hi, labels, parents]
    return None


def cover(witnesses, vertices):
    def is_good(seed, v):
        w = sum(x*y for x, y in zip(seed[2], v))
        return (0 < w < sum(v)) if all(v) else (0 <= w <= sum(v))

    common = [seed for seed in witnesses if all(is_good(seed, v) for v in vertices)]
    if common:
        return min(common, key=lambda seed: seed[1]-seed[0])

    def length(pair):
        a, b = (vertices[j] for j in pair)
        return sum((x/sum(a)-y/sum(b))**2 for x, y in zip(a, b))
    i, j = max(combinations(range(4), 2), key=length)
    a, b = vertices[i], vertices[j]
    v = tuple(x*sum(b)+y*sum(a) for x, y in zip(a, b))
    midpoint = tuple(x//gcd(*v) for x in v)
    parts = []
    for slot in (i, j):
        sub = vertices.copy()
        sub[slot] = midpoint
        parts.append(cover(witnesses, sub))
    return {"cut": [i, j], "children": parts}


def record(library, m, edges):
    if m == 3:
        return search(library, edges, 3, [(0, 2, -1)])
    patterns = [f for a in range(1, 5) for b in range(2, 5)
                for f in permutations((-a, 0, 1, b))]
    admissible = [f for f in patterns if 0 < sum(f) < 4
                  and all(0 <= x <= i for i, x in enumerate(accumulate(f), 1))]
    for choices in ([f for f in admissible if set(f) == {-1, 0, 1, 2}], admissible):
        seed = search(library, edges, 4, choices)
        if seed is not None:
            return seed
    witnesses = [seed for f in sorted(set(patterns))
                 if (seed := search(library, edges, 4, [f])) is not None]
    return cover(witnesses, [tuple(int(i < r) for i in range(4)) for r in range(1, 5)])


def main():
    library = ctypes.CDLL(str(Path(sys.argv[1]).resolve()))
    pointer = ctypes.POINTER(ctypes.c_int)
    library.fit.argtypes = [ctypes.c_int]*4 + [pointer]*3
    for m in (3, 4):
        for skeleton in skeletons(m):
            for mask in range(1 << len(skeleton)):
                edges = []
                v = len(skeleton)+1
                for j, (a, b) in enumerate(skeleton):
                    if mask & (1 << j):
                        edges.extend(((a, v), (v, b)))
                        v += 1
                    else:
                        edges.append((a, b))
                seed = record(library, m, edges)
                assert seed is not None
                print(json.dumps([m, skeleton, mask, seed], separators=(",", ":")))


if __name__ == "__main__":
    main()

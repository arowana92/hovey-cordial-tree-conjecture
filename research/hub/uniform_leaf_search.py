"""Regenerate the five-vertex labelings and their exact coverage certificate."""

import json
from fractions import Fraction
from functools import lru_cache, reduce
from itertools import combinations, permutations
from math import gcd

from .uniform_leaf_verify import CORES


def seed_for(labels, edges):
    weights = {labels[u] + labels[v] for u, v in edges}
    if len(weights) != 4:
        return None
    for padding in (0, 2):
        lo = min(min(labels), min(weights)-1) - padding
        hi = max(max(labels), max(weights)) + padding
        rows = sorted(set(range(lo, hi+1)) - set(labels))
        columns = set(range(lo+1, hi+1)) - weights
        matched = {}

        def assign(x, seen):
            for p in labels:
                y = x+p
                if y in columns and y not in seen:
                    seen.add(y)
                    if y not in matched or assign(matched[y], seen):
                        matched[y] = x
                        return True
            return False

        if all(assign(x, set()) for x in rows):
            pairs = sorted((x, y) for y, x in matched.items())
            return [lo, hi, [y-x for x, y in pairs]]
    return None


def primitive(v):
    divisor = reduce(gcd, v)
    return tuple(x//divisor for x in v)


def midpoint(a, b):
    return primitive(tuple(sum(b)*x + sum(a)*y for x, y in zip(a, b)))


def profile(apex, t, vertex):
    v = [t.numerator*x for x in vertex]
    v[apex] += (t.denominator-t.numerator)*sum(vertex)
    return primitive(v)


def search(edges):
    seeds = []
    for f in permutations(range(-4, 6), 5):
        if 0 in f and 1 in f:
            seed = seed_for(f, edges)
            if seed is not None:
                seeds.append((f, seed))
    seeds.sort(key=lambda row: (row[1][1]-row[1][0], row[0]))
    used = {}

    @lru_cache(None)
    def eligible(v):
        total = sum(v)
        corner = sum(x > 0 for x in v) == 1
        bits = bytearray((len(seeds)+7)//8)
        for i, (f, _) in enumerate(seeds):
            value = sum(x*y for x, y in zip(f, v))
            allowed = (0 <= value <= total) if corner else (0 < value < total)
            if allowed:
                bits[i//8] |= 1 << (i % 8)
        return int.from_bytes(bits, "little")

    @lru_cache(None)
    def distance(a, b):
        return sum((x/sum(a)-y/sum(b))**2 for x, y in zip(a, b))

    def cover(apex, start, stop, facet):
        mask = (1 << len(seeds)) - 1
        for t in (start, stop):
            for v in facet:
                mask &= eligible(profile(apex, t, v))
        if mask:
            best = (mask & -mask).bit_length() - 1
            return used.setdefault(best, len(used))

        a, b = max(combinations(range(4), 2), key=lambda ij: distance(facet[ij[0]], facet[ij[1]]))
        if float(stop-start)**2 >= distance(facet[a], facet[b]):
            mid = (start+stop)/2
            return ["t", cover(apex, start, mid, facet), cover(apex, mid, stop, facet)]
        left, right = facet.copy(), facet.copy()
        left[a] = right[b] = midpoint(facet[a], facet[b])
        return [a, b, cover(apex, start, stop, left), cover(apex, start, stop, right)]

    chambers = []
    for order in permutations(range(5)):
        facet = [tuple(int(i in order[:r]) for i in range(5)) for r in range(2, 6)]
        chambers.append(cover(order[0], Fraction(0), Fraction(1), facet))
    return {"seeds": [seeds[i] for i in used], "cover": chambers}


if __name__ == "__main__":
    records = [json.dumps(search(edges), separators=(",", ":")) for edges in CORES]
    print("[\n" + ",\n".join(records) + "\n]")

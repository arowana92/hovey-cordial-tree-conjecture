"""Independently reconstruct the centroid cases and test their allowed suffixes."""
from functools import lru_cache
from itertools import combinations

from research.rainbow.spine_counts import partitions, rooted


def numerical(n, leaves):
    return numerical_branches(n-1, leaves, leaves//2, n-28, 7 if leaves >= 14 else 6)


def numerical_branches(order, tips, cap, limit, budget=6):

    def visit(mass, left, previous, attainable, parts):
        if not mass:
            if not left:
                yield tuple(sorted(parts))
            return
        if not left or mass < left:
            return
        largest, tie = previous
        # Order branches by decreasing size. At most 'left' can still be added.
        for s in range((mass+left-1)//left, min(largest, mass)+1):
            lower = max(1, left-(mass-s))
            upper = min(cap, left, max(1, s-1), tie if s == largest else cap)
            for h in range(lower, upper+1):
                # Bit j of a mask means a subcollection has exactly j vertices.
                masks = attainable[:h] + tuple(attainable[a] | (attainable[a-h]<<s)
                                               for a in range(h, budget+1))
                if any(mask >> limit for mask in masks[h:]):
                    continue
                yield from visit(mass-s, left-h, (s, h), masks, parts+[(s, h)])

    return visit(order, tips, (limit-1, cap), (1,) + (0,)*budget, [])


@lru_cache(None)
def suffix_shapes(mass, cap):
    found = set()
    for sizes in partitions(mass):
        if len(sizes) > cap:
            continue

        def assign(i, left, current):
            if i == len(sizes):
                found.add(tuple(sorted(current)))
                return
            s = sizes[i]
            for h in rooted(s):
                if h + len(sizes)-i-1 <= left:
                    assign(i+1, left-h, current+[(s, h)])
        assign(0, cap, [])
    return found


def cut_test(target, proved, budget=6):

    @lru_cache(None)
    def covers(whole, z, cap):
        count = sum(h for s, h in whole)
        if count+cap <= budget:
            return True
        return all(count+sum(h for s, h in sub) <= budget or tuple(sorted(whole+sub)) in proved
                   for sub in suffix_shapes(z, cap))

    def found(parts):
        for i, (size, tips) in enumerate(parts):
            other = parts[:i]+parts[i+1:]
            for length in range(len(other)+1):
                for whole in combinations(other, length):
                    z = target - sum(s for s, h in whole)
                    if z == size and covers(tuple(sorted(whole+((size, tips),))), 0, 0):
                        return True
                    if 0 < z < size and (not whole or whole[0][0] >= min(size, z+min(tips,z))):
                        if covers(whole, z, tips):
                            return True
        return False

    return found


def check_geometry(n, leaves, proved):
    found = cut_test(n-28, proved, 7 if leaves >= 14 else 6)
    hard = set(numerical(n, leaves))
    for p in hard:
        assert found(p), f"uncovered case at order {n}: {p}"
    return hard

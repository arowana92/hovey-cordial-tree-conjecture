"""Construct a transversal for separate lists and shifts in a prime-order coset."""
from itertools import combinations
from math import isqrt


def local_assignment(k, rows, allowed, shifts):
    """Find distinct sources and destinations inside one input/output coset pair."""
    ordered = sorted(rows, key=lambda i: len(allowed[i]))
    result = {}

    def visit(j, used, images):
        if j == len(ordered):
            return True
        i = ordered[j]
        for x in sorted(allowed[i] - used):
            y = (x+shifts[i]) % k
            if y not in images:
                result[i] = x
                if visit(j+1, used | {x}, images | {y}):
                    return True
        return False

    if not visit(0, set(), set()):
        raise AssertionError("prime-coset matching failed")
    return result


def assign(k, p, lists, shifts, trace=None):
    if p < 2 or any(p % d == 0 for d in range(2, isqrt(p)+1)) or k <= 0 or k % p:
        raise ValueError("p must be a prime divisor of k")
    if len(lists) != len(shifts):
        raise ValueError("one shift is required per list")
    r = len(lists)
    step = k//p
    if len({s % step for s in shifts}) > 1:
        raise ValueError("shifts must lie in one coset")
    remaining = {i: {x % k for x in choices} for i, choices in enumerate(lists)}
    if any(len(a) < r for a in remaining.values()) or sum(len(a)==r for a in remaining.values()) >= p:
        raise ValueError("list sizes do not meet the theorem")
    result = [None]*r
    while remaining:
        r = len(remaining)
        origin = min(remaining[min(remaining)]) % step
        cell = set(range(origin, k, step))
        available = {i: cell & choices for i, choices in remaining.items()}
        full = [i for i, a in available.items() if len(a)==p]
        if len(full) < p:
            ranked = sorted(remaining, key=lambda i: -len(available[i]))
            h = max(j for j, i in enumerate(ranked, 1) if len(available[i]) >= j)
            selected = ranked[:h]
            placed = local_assignment(k, selected, available, shifts)
            mode = 'partial'
        else:
            tight = {i for i, a in remaining.items() if len(a)==r}
            almost = [i for i in tight if len(available[i])==p-1]
            pool = full + sorted(almost)
            if len(pool) >= 2*p-1:
                base = shifts[pool[0]]
                selected = next(block for block in combinations(pool[:2*p-1], p)
                                if sum((shifts[i]-base)//step for i in block) % p == 0)
                raw = local_assignment(k, selected, dict.fromkeys(selected, cell), shifts)
                translation = next(t for t in range(0, k, step)
                                   if all((raw[i]+t) % k in available[i] for i in selected))
                placed = {i: (raw[i]+translation) % k for i in selected}
                mode = 'full with partial list' if any(i in almost for i in selected) else 'full'
            else:
                # Give priority to tight full rows, since an unselected one
                # would lose p options when only p-1 rows are placed.
                selected = sorted(pool, key=lambda i: not (i in tight and i in full))[:p-1]
                placed = local_assignment(k, selected, available, shifts)
                mode = 'one vacant'
        if trace is not None:
            trace.append(mode)
        for i, x in placed.items():
            result[i] = x
            del remaining[i]
        for choices in remaining.values():
            choices.difference_update(cell)
        assert all(len(a) >= len(remaining) for a in remaining.values())
        assert sum(len(a)==len(remaining) for a in remaining.values()) < p
    return result

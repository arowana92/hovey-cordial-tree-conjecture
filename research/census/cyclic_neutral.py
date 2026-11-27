"""Uniform increments at two branching neighbors over every cyclic group."""

from heapq import heappop, heappush
from math import gcd


def connected(m, x, y, a, b, protect):
    """Three displacements on one orbit; optionally fix positions x and y."""
    h = m - a - b
    if h < 0 or (a * x + b * y) % m or (protect and h < 2):
        return None
    steps = ((y - x, h), (-y, a), (x, b))
    source = (2 * y - x) % m if protect else 0
    dist = [None] * m
    dist[source] = 0
    pending = [(0, source)]
    while pending:
        value, i = heappop(pending)
        if value != dist[i]:
            continue
        for step, cost in steps:
            j = (i + step) % m
            candidate = value + cost
            if dist[j] is None or candidate < dist[j]:
                dist[j] = candidate
                heappush(pending, (candidate, j))
    if protect and dist[x] != 2 * (a + b):
        return None
    fixed = [i for i in range(m) if h - dist[(i + y - x) % m] + dist[i] == m]
    left = [i for i in range(m) if a - dist[i] + dist[(i + y) % m] == m]
    right = sorted(set(range(m)) - set(fixed) - set(left))
    return fixed, left, right


def rows(x, y, left, right, direct):
    result = [(0, -1, x), (1, -1, y)]
    for parent, values in ((0, left), (1, right), (-1, direct)):
        for v in sorted(values):
            result.append((len(result), parent, v))
    return result


def construct(a, b, ordinary):
    if min(a, b) < 1 or ordinary < 0:
        raise ValueError("expected positive branch sizes and nonnegative direct leaves")
    k = a + b + ordinary + 2
    for size, other, flip in ((a, b, False), (b, a, True)):
        g = gcd(k, size)
        if g > 1:
            x = k // g
            moving = [i + j*x for i in range(1, size//g + 1) for j in range(g)]
            spare = sorted(set(range(k)) - {x, 0} - set(moving))
            if flip:
                return rows(0, x, spare[:other], moving, spare[other:])
            return rows(x, 0, moving, spare[:other], spare[other:])

    # Both populations are units. The sum of all displacements forces y from x.
    # Classify x by additive order; unit scaling identifies all choices of that order.
    for g in range(1, k):
        if k % g:
            continue
        m = k // g
        y = -a * pow(b, -1, m) % m
        if y == 1:
            continue
        choices = [(i, j) for i in range(min(a, m) + 1)
                   for j in range(min(b, m-i) + 1) if (i + j*y) % m == 0]
        # Nonzero cosets have no prescribed fixed position. Record one predecessor
        # per attainable pair for each number of completed cosets.
        levels = [{(0, 0): None}]
        for _ in range(1, g):
            fresh = {}
            for I, J in levels[-1]:
                for i, j in choices:
                    if I+i <= a and J+j <= b:
                        fresh.setdefault((I+i, J+j), (i, j))
            levels.append(fresh)
        for i, j in choices:
            target = a-i, b-j
            if target not in levels[-1]:
                continue
            first = connected(m, 1, y, i, j, True)
            if first is None:
                continue
            groups = [first]
            for prev in reversed(levels[1:]):
                I, J = target
                di, dj = prev[target]
                target = I-di, J-dj
                groups.append(connected(m, 1, y, di, dj, False))
            parts = [set(), set(), set()]
            for coset, group in enumerate(groups):
                for dest, values in zip(parts, group):
                    dest.update(coset + g*v for v in values)
            fixed, left, right = parts
            return rows(g, g*y, left, right, fixed - {g, g*y})
    return None

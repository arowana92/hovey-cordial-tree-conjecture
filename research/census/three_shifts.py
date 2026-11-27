"""Exact matching with three cyclic displacements, missing rows/columns and quotas."""

from collections import deque
from itertools import product
from math import gcd


def baseline(m, rows, cols, steps):
    """Find an unrestricted matching on the surviving rows and columns."""
    assigned = {}
    image = {}
    for start in sorted(rows):
        queue = deque([start])
        via = {start: None}
        aug = None
        while queue and aug is None:
            v = queue.popleft()
            for step in steps:
                w = (v + step) % m
                if w not in cols:
                    continue
                if w not in assigned:
                    aug = (v, w)
                    break
                other = assigned[w]
                if other not in via:
                    via[other] = (v, w)
                    queue.append(other)
        if aug is None:
            return None
        while aug is not None:
            v, w = aug
            image[v] = w
            assigned[w] = v
            aug = via[v]
    return image


def orbit(m, rows, cols, x, y, counts, ref):
    """The shifts 0,x,y generate the cyclic group of order m."""
    steps = (0, x, y)
    old = [sum((w - v) % m == step for v, w in ref.items()) for step in steps]
    differences = [c - b for c, b in zip(counts, old)]
    if (differences[1] * x + differences[2] * y) % m:
        return None
    constraints = []
    arcs = []
    for i in range(m):
        # (potential start, potential end, matching row) for each displacement.
        spec = ((i, (i+y-x) % m, i), (i, (i-y) % m, (i-y) % m),
                (i, (i+x) % m, (i+x-y) % m))
        for j, (u, v, row) in enumerate(spec):
            col = (row + steps[j]) % m
            upper = int(row in rows and col in cols)
            cost = differences[j] + m * int(ref.get(row) == col)
            constraints.append((u, v, cost))
            constraints.append((v, u, m * upper - cost))
            arcs.append((u, v, row, col, cost))
    # A single source preserves the residue of every path to a vertex.
    dist = [None] * m
    dist[0] = 0
    for _ in range(m):
        changed = False
        for u, v, weight in constraints:
            if dist[u] is not None:
                candidate = dist[u] + weight
                if dist[v] is None or candidate < dist[v]:
                    dist[v] = candidate
                    changed = True
        if not changed:
            break
    else:
        return None
    return {row: col for u, v, row, col, cost in arcs if cost + dist[u] - dist[v] == m}


def match(k, rows, columns, shifts, counts):
    """Match the two sets with exactly counts[i] pairs of displacement shifts[i]."""
    if len(shifts) != 3 or len(set(shifts)) != 3 or len(counts) != 3:
        raise ValueError("expected three distinct residues and their three counts")
    rows, columns = set(rows), set(columns)
    if len(rows) != len(columns) or sum(counts) != len(rows) or min(counts) < 0:
        return None
    if any(not 0 <= z < k for z in rows | columns | set(shifts)):
        raise ValueError("positions and shifts must be residues")
    offset = shifts[0]
    columns = {(v - offset) % k for v in columns}
    X, Y = ((s - offset) % k for s in shifts[1:])
    g = gcd(k, X, Y)
    m, x, y = k // g, X // g, Y // g
    levels = [{(0, 0): None}]
    for i in range(g):
        R = {v // g for v in rows if v % g == i}
        C = {v // g for v in columns if v % g == i}
        if len(R) != len(C):
            return None
        ref = baseline(m, R, C, (0, x, y))
        if ref is None:
            return None
        fresh = {}
        pairs = [(counts[1], counts[2])] if g == 1 else product(
            range(min(len(R), counts[1]) + 1), range(min(len(R), counts[2]) + 1))
        for a, b in pairs:
            h = len(R) - a - b
            if not 0 <= h <= counts[0]:
                continue
            result = orbit(m, R, C, x, y, (h, a, b), ref)
            if result is None:
                continue
            for A, B in levels[-1]:
                if A+a <= counts[1] and B+b <= counts[2]:
                    fresh.setdefault((A+a, B+b), ((A, B), result))
        if not fresh:
            return None
        levels.append(fresh)
    target = counts[1], counts[2]
    if target not in levels[-1]:
        return None
    result = {}
    for i in reversed(range(g)):
        target, part = levels[i+1][target]
        result.update((i+g*v, (i+g*w+offset) % k) for v, w in part.items())
    return result

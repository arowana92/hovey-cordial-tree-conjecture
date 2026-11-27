"""Guarded integer forest labels with bounded discrepancies and polynomial span."""

from random import Random

from research.hub.polynomial_hub import DEPTH
from research.hub.polynomial_two_hubs import forest_seed
from research.hub.star_repair import erasures


def balanced_order(jumps):
    """Alternate signs while possible, then finish in the only remaining direction."""
    positive = [v for v, p in jumps.items() if p > 0]
    negative = [v for v, p in jumps.items() if p < 0]
    order = [v for v, p in jumps.items() if p == 0]
    position = 0
    while positive and negative:
        v = (positive if position <= 0 else negative).pop()
        order.append(v)
        position += jumps[v]
    return order + positive + negative


def offsets_for_level(jumps):
    residual, cycles, end = erasures(balanced_order(jumps), jumps, 0, None)
    offsets = dict(residual)
    taken = set(offsets.values()) | {end}
    for cycle in cycles:
        # Each old value and cycle tail can forbid only one shift.
        for shift in range(len(cycle)*len(taken)+1):
            if all(a+shift not in taken for _, a in cycle):
                offsets.update((v, a+shift) for v, a in cycle)
                taken.update(a+shift for _, a in cycle)
                break
        else:
            raise AssertionError("integer cycle translation exhausted")
    return offsets, end


def guard_points(b, t):
    """Integer parent labels forbidden by a single guarded discrepancy."""
    points = {-b//j for j in (1, 2, 3) if b % j == 0}
    if t % 2 == 0:
        points.add(t//2)
    return points


def candidate(offsets, end, x, used, blocked):
    row = {v: x+a for v, a in offsets.items()}
    values = set(row.values())
    if not blocked.isdisjoint(values):
        return None
    reserve = set()
    pairs = []
    if end:
        t = x+end
        if not t or not x+2*t or t in blocked or -t in blocked or -t in values:
            return None
        guards = guard_points(x, t)
        if not guards.isdisjoint(used) or not guards.isdisjoint(values):
            return None
        pairs.append((x, t))
        reserve = guards | {t, -t}
    return row, values, reserve, pairs


def first_choice(layout, start, used, blocked):
    offsets, end = layout
    width = (len(offsets)+8)*(len(blocked)+8)+8*len(offsets)
    for x in range(start, start+width+1):
        result = candidate(offsets, end, x, used, blocked)
        if result is not None:
            return result
    raise AssertionError("integer translation exhausted")


def split_level(jumps, degrees):
    mass = sum(degrees.values())
    heavy = max(degrees, key=degrees.get)
    if 3*degrees[heavy] >= mass:
        return [v for v in jumps if v != heavy], [heavy], True
    order = balanced_order(jumps)
    prefix = 0
    for i, v in enumerate(order, 1):
        prefix += degrees[v]
        if 3*prefix >= mass:
            return order[:i], order[i:], False
    raise AssertionError("mass split exhausted")


def paired_trials(length, thickness, rng):
    yield 0, 0
    for _ in range(128):
        yield rng.randrange(length), rng.randrange(thickness)
    for z in range(length):
        for delta in range(thickness):
            yield z, delta


def centers(jumps, degrees, used, blocked, rng):
    if not any(degrees.values()):
        return [first_choice(offsets_for_level(jumps), 0, used, blocked)]
    left, right, heavy = split_level(jumps, degrees)
    first, second = [offsets_for_level({v: jumps[v] for v in part})
                     for part in (left, right)]
    m, n = sum(degrees[v] for v in left), sum(degrees[v] for v in right)
    if heavy:
        old = first_choice(first, 0, used, blocked)
        weighted = sum(degrees[v]*x for v, x in old[0].items())
        start = -weighted//n-second[0][right[0]]
        new = first_choice(second, start, used | old[1], blocked | old[1] | old[2])
        return [old, new]

    # Both masses lie between one and two thirds of their sum. Opposite
    # translations spread both groups while keeping the weighted sum small.
    a, b = [sum(degrees[v]*x for v, x in offsets.items())
            for offsets, end in (first, second)]
    length = 200*(len(jumps)+8)*(len(jumps)+len(blocked)+8)
    thickness = 100*(len(jumps)+8)
    for z, delta in paired_trials(length, thickness, rng):
        old = candidate(*first, -a//m+z, used, blocked)
        if old is None:
            continue
        x = -b//n-(m*z//n)+delta
        new = candidate(*second, x, used | old[1], blocked | old[1] | old[2])
        if new is not None:
            return [old, new]
    raise AssertionError("integer translations of two balanced groups exhausted")


def prepare(tree, boundaries, fixed, rng=None):
    """Use virtual vertex zero, with an actual integer parent label for each child.

    fixed contains occupied labels including the boundary labels. Return the free
    vertex labels, discrepancies (deficit, surplus), and neutral seed statistics.
    """
    if not tree or tree[0] != -1 or any(not 0 <= p < v for v, p in enumerate(tree[1:], 1)):
        raise ValueError("expected a parent-before-child forest with virtual root zero")
    fixed = set(fixed)
    if set(boundaries) != {v for v in range(1, len(tree)) if tree[v] == 0}:
        raise ValueError("expected one boundary label per virtual-root child")
    if not set(boundaries.values()) <= fixed:
        raise ValueError("boundary labels must be occupied")
    w = max(map(abs, fixed), default=0)
    h = len(tree)-1
    rng = rng or Random(804)
    labels, seed_stats = forest_seed(tree, boundaries, h, w, rng)
    used = fixed | set(labels.values())
    blocked = used.copy()
    kids = [[] for _ in tree]
    front = []
    for v in range(1, len(tree)):
        if v in labels:
            continue
        p = tree[v]
        kids[p].append(v)
        if not p or p in labels:
            front.append(v)
    bills = []
    levels = 0
    while front:
        levels += 1
        jumps = {v: labels[tree[v]] if tree[v] else boundaries[v] for v in front}
        degrees = {v: len(kids[v]) for v in front}
        for row, values, reserve, pairs in centers(jumps, degrees, used, blocked, rng):
            labels.update(row)
            used.update(values)
            blocked.update(values | reserve)
            bills.extend(pairs)
        front = [w for v in front for w in kids[v]]
    assert levels <= DEPTH
    return labels, bills, (*seed_stats, levels)

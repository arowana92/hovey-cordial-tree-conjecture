"""Consecutive integer sums after expanding labeled vertices into matched pairs."""


def interval_lift(parents, indices, joins):
    """Return a labeling, or None when the specified pair allocation cannot work."""
    m = len(parents)
    if m % 2 == 0 or sorted(indices) != list(range(m)):
        raise ValueError("the quotient needs a permutation of odd order")
    sums = [indices[p] + indices[i] for i, p in enumerate(parents) if i]
    if {z % m for z in sums} != set(range(m - 1)):
        raise ValueError("the quotient must omit weight -1")
    levels = []
    for z in sums:
        if z % 2:
            levels.append(1)
        elif z >= m + 1:
            levels.append(0)
        else:
            levels.append(2)
    for first in (0, 1):
        flips = [first]
        for i, ((left, right), level) in enumerate(zip(joins, levels), start=1):
            parent_bit = flips[parents[i]] ^ left
            child_bit = level - parent_bit
            if child_bit not in (0, 1):
                break
            flips.append(child_bit ^ right)
        if len(flips) == m:
            return [x + m * (port ^ flip)
                    for x, flip in zip(indices, flips) for port in (0, 1)]
    return None


def arm_tree(left_count, right_count):
    """Return ordinary edges and integer labels. Each arm is a two-edge path."""
    total = left_count + right_count
    h = total // 2
    if total % 2 or min(left_count, right_count) < h // 2:
        raise ValueError("arm counts outside the interval theorem")
    indices = [h]
    sides = []
    for j in range(1, h + 1):
        indices.extend((h - j, h + j))
        sides.extend((1, 0) if j % 2 == 0 else (None, None))
    left_free = left_count - h // 2
    for i, side in enumerate(sides):
        if side is None:
            sides[i] = int(left_free == 0)
            if left_free:
                left_free -= 1
    labels = interval_lift([-1] + [0] * total, indices, [(s, 0) for s in sides])
    assert labels is not None
    edges = [(0, 1)]
    for i, side in enumerate(sides, start=1):
        edges.extend(((side, 2*i), (2*i, 2*i + 1)))
    return edges, labels

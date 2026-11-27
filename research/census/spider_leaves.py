"""Label spiders with at most four legs longer than one, and related trees."""

from itertools import combinations

from .four_leaves import (DATA, assemble, colors, endpoint, fork, grow, kernel,
                          path_piece, reflect)


# Rows for S(2,2,t) with rank zero at the center. At t=7 the tip has deficiency 3.
CENTER_ZERO = {
    7: [0, 3, 1, 0, 2, 1, 5, 5, 4, 4, 3, 2],
    8: [0, 0, 1, 2, 2, 3, 4, 1, 5, 4, 6, 5, 3],
    9: [0, 1, 1, 4, 2, 0, 3, 2, 6, 6, 5, 5, 4, 3],
    10: [0, 0, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6, 7, 1, 4],
    11: [0, 0, 1, 2, 2, 3, 3, 6, 5, 5, 7, 7, 6, 1, 4, 4],
}

# Ordinary vertex labels for S(2,2,2,t). The least sum is the center label + 1.
UPPER = {
    2: [3, 8, 0, 1, 5, 2, 7, 4, 6],
    3: [4, 2, 9, 6, 7, 8, 1, 3, 5, 0],
    4: [6, 8, 0, 9, 4, 10, 1, 3, 7, 5, 2],
    6: [5, 10, 7, 11, 3, 1, 12, 2, 9, 0, 8, 4, 6],
}


def zero_leaves(piece, leaves, center, sides):
    """Retain rank zero at the center and fill the lowest opposite ranks."""
    vertices, row = piece
    m = len(leaves)
    new = [x + (m if sides[v] != sides[center] else 0) for v,x in zip(vertices,row)]
    return vertices + leaves, new + list(range(m))


def star(center, leaves):
    return [center] + leaves, [0] + list(range(len(leaves)))


def make_leaves(parents, center, n):
    start = len(parents)
    parents.extend([center] * n)
    return list(range(start, start+n))


def rank_zero_fork(arms, sides):
    """The arms are in order 2,2,t, with t=5 or t>=7."""
    t = len(arms[2])
    base = t if t <= 11 else (7 if t == 18 else 5)
    row = kernel((2,2,5),9,1) if base == 5 else CENTER_ZERO[base]
    ids = [0] + arms[0] + arms[1] + arms[2][:base]
    if t == base:
        return ids, row
    tail = arms[2][base:]
    widths = [sum(sides[v] == side for v in ids) for side in (0,1)]
    extra = [x + widths[sides[v]] for v,x in zip(tail, endpoint(t-base,3))]
    return ids + tail, row + extra


def spider(long_arms, leaves):
    """Return parent array and labels, numbering the direct leaves last."""
    if len(long_arms) > 4 or any(t < 2 for t in long_arms) or leaves < 0:
        raise ValueError("Expected up to four long arms and a nonnegative leaf count")
    parents, arms = fork(long_arms)
    free = make_leaves(parents,0,leaves)
    sides = colors(parents)
    if len(arms) <= 2:
        left, right = (arms + [[],[]])[:2]
        spine = left[::-1] + [0] + right
        return parents, assemble(sides, [star(v, free if v == 0 else []) for v in spine])
    for i,j in combinations(range(len(arms)),2):
        if len(arms[i]) == len(arms[j]) == 2:
            continue
        rest = [x for k,x in enumerate(arms) if k not in (i,j)]
        if len(rest) == 1:
            rest.append([])
        if len(rest[0]) == len(rest[1]) == 2:
            continue
        left = zero_leaves(path_piece(arms[i],0,arms[j],0), free, 0, sides)
        right = path_piece(rest[0],0,rest[1],0)
        return parents, assemble(sides, [reflect(left,sides),right])

    arms.sort(key=lambda arm: len(arm) != 2)
    t = len(arms[-1])
    if len(arms) == 3 or t in UPPER:
        row = DATA["intervals"]["s:2,2,2"] if len(arms) == 3 else UPPER[t]
        labels = [0] * len(parents)
        for v,x in zip([0] + sum(arms,[]), row):
            labels[v] = x
        for i,v in enumerate(free,len(row)):
            labels[v] = i
        return parents, labels
    left = rank_zero_fork([arms[0],arms[1],arms[3]], sides)
    left = zero_leaves(left,free,0,sides)
    right = [0] + arms[2], endpoint(3,0)
    return parents, assemble(sides, [reflect(left,sides),right])


def decorated_connector(a, b, c, d, leaf_counts):
    """Two arm paths joined by a spine with leaves at any of its vertices."""
    if (min(a,b,c,d) < 1 or (a,b) == (2,2) or (c,d) == (2,2)
            or len(leaf_counts) < 2 or min(leaf_counts) < 0):
        raise ValueError("Expected positive arms, admissible marked paths, and a nonempty connector")
    parents, (left_a,left_b,link) = fork((a,b,len(leaf_counts)-1))
    spine = [0] + link
    v = spine[-1]
    right_c,right_d = grow(parents,v,c),grow(parents,v,d)
    free = [make_leaves(parents,x,m) for x,m in zip(spine,leaf_counts)]
    sides = colors(parents)
    left = zero_leaves(path_piece(left_a,0,left_b,0),free[0],0,sides)
    right = zero_leaves(path_piece(right_c,v,right_d,0),free[-1],v,sides)
    middle = [star(x,leaves) for x,leaves in zip(spine[1:-1],free[1:-1])]
    return parents, assemble(sides, [reflect(left,sides)] + middle + [right])

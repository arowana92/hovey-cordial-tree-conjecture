"""Build the radius-two integer intervals and count actual vertices and edges."""

from collections import Counter
from fractions import Fraction
from itertools import combinations_with_replacement
from math import floor
from research.hub.branch_levels import odd_core, verify_tree
from research.hub.two_hubs import Completion, edge


def split(m):
    total = sum(m.values())
    moment = sum(p*n for p, n in m.items())
    if not 0 <= moment <= total:
        raise ValueError("parent mean outside the interval")
    if not moment or moment == total:
        return (m.copy(), {}) if not moment else ({}, m.copy())
    low = {p: Fraction(n*moment, total) for p, n in m.items()}
    take = moment
    high = {}
    for p in sorted(m, reverse=True):
        high[p] = min(take, m[p])
        take -= high[p]
    low_weight = sum(p*n for p, n in low.items())
    hi_weight = sum(p*n for p, n in high.items())
    ratio = (moment-low_weight)/(hi_weight-low_weight)
    lower = {p: (1-ratio)*n + ratio*high[p] for p, n in low.items()}
    return {p: m[p]-n for p, n in lower.items()}, lower


def weighted_tiles(counts, offset):
    parts = {p-offset: Fraction(n) for p, n in counts.items() if n}
    if 0 in parts:
        yield (0, 1, parts.pop(0))
    positives = [a for a in parts if a > 0]
    negatives = [-x for x in parts if x < 0]
    while positives and negatives:
        a, b = positives[-1], negatives[-1]
        copies = min(parts[a]/b, parts[-b]/a)
        parts[a] -= b*copies
        parts[-b] -= a*copies
        yield (a, b, copies)
        if not parts[a]:
            positives.pop()
        if not parts[-b]:
            negatives.pop()
    assert all(not n for n in parts.values())


def tile_list(counts, offset):
    for a, b, copies in weighted_tiles(counts, offset):
        yield a, b, int(copies)


def construct(populations):
    # First five branch populations correspond to 0, 1, -2, x and y.
    ordinary, *branches = populations
    total = sum(populations)
    tree = Completion([0, 2, 1], leaves=[(0, -1)], twig_edges=[(2, -2), (-2, 3)])
    tail = [tree.child(2) for _ in branches[5:]]
    partial = 2*ordinary + branches[1] - 2*branches[2] + sum(p*n for p, n in zip(tail, branches[5:]))
    x = min(tree.lo-2, floor(Fraction(total-2*partial-10*branches[4], 2*branches[3])))
    y = round(Fraction(total-2*partial-2*branches[3]*x, 2*branches[4]))
    assert y >= 5
    tree.extend(0, tree.lo-2-x)
    assert tree.child(2) == x
    tree.extend(y-1-tree.hi, 0)
    tree.edges.update((edge(2, y), edge(-2, y+2)))
    tree.leaf(0, y+1)
    tree.hi = y+2
    parents = [0, 1, -2, x, y, *tail]
    targets = dict(zip([2, *parents], populations))
    left = targets.copy()
    for hub, _ in tree.added:
        left[hub] -= 1
    left[-2] -= 2
    d = 2 + max(map(abs, targets))
    reserve = 8*(len(targets)+1)*d*d
    left[0] -= reserve
    left[1] -= reserve
    assert min(left.values()) >= 0
    lists = split(left)
    for offset, counts in enumerate(lists):
        for a, b, copies in tile_list(counts, offset):
            width = a+b
            for _ in range(copies):
                start = tree.hi+1 if not offset else tree.lo-width
                for i in range(width):
                    p = offset+((i+a) % width)-i
                    tree.edges.add(edge(p, start+i))
                    left[p] -= 1
                if offset:
                    tree.lo -= width
                else:
                    tree.hi += width
    for hub in (0, 1):
        left[hub] += reserve
    for p, n in tuple(left.items()):
        if p in (0, 1):
            continue
        for _ in range(n):
            tree.child(p)
            if p > 0:
                left[0] -= p-1
            else:
                left[1] += p
    assert min(left[0], left[1]) >= 0
    tree.extend(left[0], left[1])
    vertices, weights, degrees = set(), set(), Counter()
    for a, b in tree.edges:
        vertices.update((a, b))
        weights.add(a+b)
        degrees.update((a, b))
    n = total + len(parents)+1
    assert len(tree.edges) == n-1 and len(vertices) == n and len(weights) == n-1
    assert min(vertices) == tree.lo and max(vertices) == tree.hi == tree.lo+n-1
    assert min(weights) == tree.lo+1 and max(weights) == tree.hi
    assert degrees[2] == ordinary+len(parents)
    assert all(degrees[p] == count+1 for p, count in zip(parents, branches))
    assert all(edge(2, p) in tree.edges for p in parents)
    return n


def groups(caps):
    b = len(caps) if len(caps) % 2 else len(caps)-1
    remaining = list(caps[:b])
    blocks = []
    for i, a in enumerate(remaining):
        r = i+1
        layers = a-(remaining[i+1] if r < b else 1)
        if r == 1 or r % 2 == 0:
            blocks.extend([(r,)]*layers)
        else:
            blocks.extend([(r, r)]*(layers//2))
            if layers % 2:
                blocks.append((r-1,))
    return b, blocks


def grab(b, blocks, target):
    ranks = [b]
    need = target-b
    for group in blocks:
        take = min(need, sum(group))
        if take == sum(group):
            ranks.extend(group)
        elif len(group) == 1:
            ranks.append(take)
        else:
            first = min(take, group[0]-1)
            ranks.extend((first, take-first))
        need -= take
        if not need:
            break
    assert not need
    return tuple(sum(r > i for r in ranks) for i in range(b))


if __name__ == '__main__':
    tested = 0
    for c in range(1, 11):
        for profile in combinations_with_replacement(range(1, 5), c):
            caps = profile[::-1]
            b, blocks = groups(caps)
            high = b+sum(map(sum, blocks))
            assert (sum(caps[:b])-high)**2 <= sum(caps)
            for t in range(b, high+1):
                chosen = grab(b, blocks, t)
                assert sum(chosen) == t and all(x <= y for x, y in zip(chosen, caps))
                verify_tree(odd_core(chosen), chosen)
                tested += 1
    sizes = [construct(p) for p in ((7000, 12000, 11500, 4100, 6100, 5000),
                                    (10000, 68000, 66000, 28000, 22000, 21000, 17000, 15000))]
    print(f"{tested} trimmed diagrams; exact vertex and edge intervals at orders {sizes}")

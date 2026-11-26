"""Construct super edge-magic leaf extensions of arbitrary trees using three reservoirs."""

from collections import Counter, deque
from dataclasses import dataclass
from fractions import Fraction
from math import ceil

from .radius_threshold import split, weighted_tiles
from .two_hubs import Completion, edge


@dataclass(frozen=True)
class Block:
    offset: int  # 0 extends the upper end, 1 the lower end
    parents: tuple
    copies: int = 1


def partial_rotation(a, b, t, offset):
    """Retain t edges of a rotation and match the remaining positions in order."""
    n = a+b
    assert 0 <= t <= n//2
    m = n-t
    phase = 0
    if not offset and 2*((-m*a) % n) > n:
        phase = (m*a) % n
    keep = [i for i in range(n) if (m*(i+1)+phase)//n == (m*i+phase)//n]
    images = [(i+a) % n for i in keep]
    kept = set(keep)
    used = set(images)
    free_rows = (i for i in range(n) if i not in kept)
    free_columns = (i for i in range(n) if i not in used)
    perm = dict(zip(keep, images))
    perm.update(zip(free_rows, free_columns))
    return Block(offset, tuple(offset+perm[i]-i for i in range(n))), kept


def upper_child(tree, p):
    if p <= 0:
        return tree.child(p)
    x = tree.hi+1
    tree.edges.add(edge(p, x))
    for z in range(x+1, x+p+1):
        tree.leaf(-1, z)
    tree.hi = x+p
    return x


def make_seed(parents, counts, path, x, y):
    graph = [[] for _ in parents]
    for v in range(1, len(parents)):
        u = parents[v]
        graph[u].append(v)
        graph[v].append(u)
    assert len(set((*path, x, y))) == 5 and all(len(graph[v]) == 1 for v in (x, y))
    assert path[1] in graph[path[0]] and path[1] in graph[path[2]]
    tree = Completion([-1, 1, 0])
    labels = dict(zip(path, tree.path))
    queue = deque(path)
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in labels and v not in (x, y):
                labels[v] = upper_child(tree, labels[u])
                queue.append(v)
    p, q = labels[graph[x][0]], labels[graph[y][0]]
    return tune(tree, labels, counts, x, y, p, q)


def tune(tree, labels, counts, x, y, p, q):
    span = max(p-tree.lo, 1-tree.lo, tree.hi+1-min(0, q), 2-p, 2)
    labels[x], labels[y] = -span, span
    target = Fraction(sum(counts), 2)
    moment = sum(counts[v]*z for v, z in labels.items())
    mx, my = counts[x], counts[y]
    if my <= mx:
        steps = max(0, ceil((moment-target)/mx))
        labels[x] -= steps
        labels[y] += round((target-moment+steps*mx)/my)
    else:
        steps = max(0, ceil((target-moment)/my))
        labels[y] += steps
        labels[x] -= round((moment+steps*my-target)/mx)
    tree.extend(labels[y]-(tree.hi+1-min(q, 0)), 0)
    positive = upper_child(tree, q)
    assert positive == labels[y]
    if p > 0:
        tree.extend(0, tree.lo-p-labels[x])
        negative = tree.child(p)
        assert negative == labels[x]
    else:
        # On a lower block use the cycle 0 -> b -> b-a -> ... -> 0.
        a, b = 1-p, positive-1
        assert b >= a
        tree.extend(0, tree.lo-1-labels[x])
        base = tree.lo-b-1
        tree.leaf(positive, base)
        for i in range(1, b):
            tree.leaf(0 if i <= b-a else 1, base+i)
        tree.edges.add(edge(p, base+b))
        tree.lo = base
        assert base+b == labels[x]
    return tree, labels



def central_edge_seed(parents, counts):
    """The two centers have indices 0, 1. Every other core vertex is their child."""
    assert tuple(parents[:2]) == (-1, 0) and set(parents[2:]) == {0, 1}
    five = sorted(range(2, len(parents)), key=lambda v: -counts[v])[:5]
    assert len(five) == 5 and counts[five[-1]] > 0
    majority = Counter(parents[v] for v in five).most_common(1)[0][0]
    minority = 1-majority
    a = [v for v in five if parents[v] == majority]
    b = [v for v in five if parents[v] == minority]
    if b:
        labels = {majority: 2, minority: -2, a[0]: -1, a[1]: 0, b[0]: 1}
        tree = Completion([-1, 2, -2, 1], twig_edges=[(2, 0)])
    else:
        z = next(v for v in range(2, len(parents)) if parents[v] == minority)
        labels = {majority: 2, minority: -3, z: 3, a[0]: -1, a[1]: 0, a[2]: 1}
        tree = Completion([-1, 2, -3, 3], leaves=[(0, -2)], twig_edges=[(2, 0), (2, 1)])
    x = next(v for v in a if v not in labels)
    y = next(v for v in five if v != x and v not in labels)
    for v in range(2, len(parents)):
        if v not in labels and v not in (x, y):
            labels[v] = upper_child(tree, labels[parents[v]])
    return tune(tree, labels, counts, x, y, labels[parents[x]], labels[parents[y]])


def complete(seed, labels, counts):
    h = len(counts)
    d = 2+max(map(abs, labels.values()))
    k = 2*h+2
    guard = 4*k+2
    reserve = (4*k+h*(guard+4*k)+2)*d
    remaining = Counter({labels[i]: n for i, n in enumerate(counts)})
    remaining.subtract(p for p, _ in seed.added)
    working = remaining.copy()
    for p, n in ((-1, reserve), (0, reserve), (1, 2*reserve)):
        working[p] -= n
    if min(working.values()) < 0:
        raise ValueError("insufficient reservoir counts")
    working = {p: max(0, n-guard) for p, n in working.items()}
    blocks = []

    def use(block):
        if block.copies:
            blocks.append(block)
            for p, n in Counter(block.parents).items():
                remaining[p] -= n*block.copies

    for side, allocation in enumerate(split(working)):
        for a, b, coefficient in weighted_tiles(allocation, side):
            whole = int(coefficient)
            if a == 0:
                use(Block(side, (side,), whole))
                continue
            n = a+b
            shifts = (side+a,)*b + (side-b,)*a
            use(Block(side, shifts, whole))
            fraction = coefficient-whole
            t = int(fraction*n/2)
            if t:
                block, _ = partial_rotation(a, b, t, side)
                use(Block(block.offset, block.parents, 2))

    assert min(remaining.values()) >= 0
    for p in tuple(remaining):
        if p > 1:
            use(Block(1, (p,) + (0,)*(p-1), remaining[p]))
        elif p < 0:
            use(Block(0, (1,)*(-p) + (p,), remaining[p]))
    assert min(remaining.values()) >= 0
    use(Block(0, (0,), remaining[0]))
    use(Block(1, (1,), remaining[1]))
    assert not any(remaining.values())
    return blocks


def verify(parents, counts, tree, labels, blocks, expand=False):
    """Decode each permutation directly and count all actual attachment sites."""
    core = {edge(labels[v], labels[parents[v]]) for v in range(1, len(parents))}
    actual = tree.edges-core
    assert core <= tree.edges and actual == {edge(p, z) for p, z in tree.added}
    vertices = {z for e in tree.edges for z in e}
    assert len(tree.edges) == len(vertices)-1
    assert sorted(vertices) == list(range(tree.lo, tree.hi+1))
    assert sorted(p+z for p, z in tree.edges) == list(range(tree.lo+1, tree.hi+1))
    top, bottom = tree.hi, tree.lo
    frequencies = Counter(p for p, z in tree.added)
    label_set = set(labels.values())
    all_edges = set(tree.edges) if expand else None
    for block in blocks:
        offset, shifts, copies = block.offset, block.parents, block.copies
        assert copies >= 1 and set(shifts) <= label_set
        assert sorted(i+p-offset for i, p in enumerate(shifts)) == list(range(len(shifts)))
        for p, n in Counter(shifts).items():
            frequencies[p] += copies*n
        if expand:
            for j in range(copies):
                base = bottom-(j+1)*len(shifts) if offset else top+1+j*len(shifts)
                all_edges.update(edge(base+i, p) for i, p in enumerate(shifts))
        if offset:
            bottom -= copies*len(shifts)
        else:
            top += copies*len(shifts)
    n = len(counts)+sum(counts)
    assert top-bottom+1 == n
    assert all(frequencies[z] == counts[v] for v, z in labels.items())
    if expand:
        assert len(all_edges) == n-1
        assert {z for e in all_edges for z in e} == set(range(bottom, top+1))
        assert {x+y for x, y in all_edges} == set(range(bottom+1, top+1))
    return n


def check_rotations():
    checked = 0
    for a in range(1, 26):
        for b in range(1, 26):
            n = a+b
            for t in range(n//2+1):
                for offset in (0, 1):
                    block, kept = partial_rotation(a, b, t, offset)
                    shifts = block.parents
                    assert sorted(i+p-offset for i, p in enumerate(shifts)) == list(range(n))
                    assert len(kept) == t
                    assert abs(n*sum(i < b for i in kept)-t*b) < n
                    assert all(shifts[i] == offset+(a if i < b else -b) for i in kept)
                    assert all(shifts[i] in (-1, 0, 1) for i in set(range(n))-kept)
                    checked += 1
    return checked


if __name__ == "__main__":
    print(f"{check_rotations()} partial rotations verified.")
    # A fork and a longer core with side branches.
    fork = (-1, 0, 0, 0, 2)
    longer = (-1, 0, 1, 2, 3, 4, 2, 4, 7)
    cases = [
        (fork, (1, 0, 2), 3, 4, [50000, 50000, 50000, 45000, 38000]),
        (longer, (1, 2, 3), 5, 8, [0, 10**7, 2*10**7, 3*10**7, 40, 8*10**6, 0, 11, 12*10**6]),
        (longer, (1, 2, 3), 5, 8, [10**12]*9),
    ]
    cases.append((fork, (1, 0, 2), 4, 3, [50000, 50000, 50000, 86000, 22000]))
    for i, (parents, path, x, y, counts) in enumerate(cases):
        tree, labels = make_seed(parents, counts, path, x, y)
        blocks = complete(tree, labels, counts)
        print(f"Verified order {verify(parents, counts, tree, labels, blocks, expand=i == 0)}.")

    centers = (-1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1)
    for split_at in range(6):
        counts = [2, 0] + [10**11 if j < split_at else 1 for j in range(5)]
        counts += [10**11 if j < 5-split_at else 2 for j in range(5)]
        tree, labels = central_edge_seed(centers, counts)
        verify(centers, counts, tree, labels, complete(tree, labels, counts))
    print("Verified all six placements of five large branches across the central edge.")

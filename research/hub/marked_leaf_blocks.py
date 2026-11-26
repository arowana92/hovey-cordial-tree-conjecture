"""Integer interval permutations supported by the selected attachment sites."""

from collections import Counter, deque
from functools import lru_cache

from .many_leaf_parents import Block
from .uniform_leaf_construct import exact_blocks, rational_blocks


@lru_cache(None)
def insertion(anchors, p, side):
    """Return the parent list and the position of a specified new child at p."""
    d = p-side
    if d == 0:
        return (p,), 0
    steps = {z-side for z in anchors}
    if {-1, 1} <= steps:
        path = list(range(d, -1, -1)) if d > 0 else list(range(d, 1))
    else:
        assert 0 in steps and min(steps) < 0 < max(steps)
        assert 1 in steps or -1 in steps
        queue = deque([d])
        previous = {d: None}
        while 0 not in previous:
            x = queue.popleft()
            for step in sorted(steps):
                y = x+step
                if y not in previous:
                    previous[y] = x
                    queue.append(y)
        path = [0]
        while path[-1] != d:
            path.append(previous[path[-1]])
        path.reverse()
    # Cycle 0 -> d -> ... -> 0, with fixed positions in the unused gaps.
    lo, hi = min(path), max(path)
    parents = [side] * (hi-lo+1)
    parents[-lo] = p
    for x, y in zip(path, path[1:]):
        parents[x-lo] = side+y-x
    assert all(z in anchors for i, z in enumerate(parents) if i != -lo)
    return tuple(parents), -lo


def complete(counts, anchors):
    if 1 in anchors:
        return exact_blocks(counts)
    assert set(anchors) == {-1, 0, 2}
    h = len(counts)
    d = 1 + max(counts) - min(counts)
    size = max(len(insertion(anchors, p, 0)[0]) for p in counts)
    reserve = 8*((2*h+2)*d*size+1)
    work = Counter(counts)
    for p in anchors:
        work[p] -= reserve
    if min(work.values()) < 0:
        raise ValueError("insufficient triple reserve")
    moment = sum(p*n for p, n in work.items())
    if not 0 <= moment <= sum(work.values()):
        raise ValueError("moment outside the working interval")
    remaining = Counter(counts)
    residual = work.copy()
    blocks = []

    def use(side, parents, copies):
        if copies:
            assert copies > 0
            blocks.append(Block(side, parents, copies))
            for p, n in Counter(parents).items():
                remaining[p] -= copies*n

    for side, parents, coefficient in rational_blocks(work):
        whole = int(coefficient)
        use(side, parents, whole)
        for p, n in Counter(parents).items():
            residual[p] -= whole*n
    for p, amount in residual.items():
        parents, _ = insertion(anchors, p, 0)
        use(0, parents, amount)

    a, b, c = (remaining[p] for p in (-1, 0, 2))
    x = (2*a-c+2)//3
    y = a-2*x
    z = c-2*a+3*x
    use(0, (2, -1, -1), x)
    use(1, (2, 2, -1), y)
    use(1, (2, 0), z)
    use(0, (0,), b-z)
    assert not any(remaining.values())
    return blocks

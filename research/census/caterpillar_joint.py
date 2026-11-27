"""Attach a rooted caterpillar at its prescribed vertex on a balanced core."""

from research.census.caterpillar_leaf import staircase


def extend(spine, leaves, joint, core, deficit, k):
    """Return labels, preserving the entire core. The caterpillar has 1..k-1 edges."""
    ranks, _ = staircase(spine, leaves)
    A, B = ranks if joint in ranks[0] else ranks[::-1]
    a, b = len(A), len(B)
    t = a + b - 1
    if not 1 <= t < k:
        raise ValueError("expected between one and k-1 new edges")

    x = A[joint]
    p = core[joint] - x
    target = a + (deficit - 2 * p - a) % k
    # Include the representative k exactly when rank zero is the shared vertex.
    last = k - b + int(x == 0)
    start = min(target, last)
    values = dict(A)
    values.update((v, start + j) for v, j in B.items())
    if target - start >= t:
        # The uncovered residue is a-1. Starting at a puts the old weights
        # in [a,a+t-1]. Move the first row and, at full order, the last column.
        values.update((v, a + j) for v, j in B.items())
        first = next(v for v, i in A.items() if i == 0)
        values[first] = -1
        if t == k - 1:
            last_vertex = next(v for v, j in B.items() if j == b - 1)
            values[last_vertex] = 0

    return {**core, **{v: (p + i) % k for v, i in values.items()}}

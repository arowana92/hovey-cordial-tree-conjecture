"""Restore several leaf-decorated spine windows with a single final leaf walk."""

from itertools import chain
from random import Random

from research.hub.decorated_spine import leafy_layout, path_values
from research.hub.star_repair import erasures


def box(width, dimension):
    for index in range(width**dimension):
        coords = []
        for _ in range(dimension):
            index, digit = divmod(index, width)
            coords.append(1+digit)
        yield coords


def bare_row(layout, labels, target, coords):
    segments, marks, _ = layout
    x, g, *parameters = coords
    special = {'t': target, 'X': x, 'G': g}
    row = {v: special[name] for v, name in marks.items()}
    if 0 in row.values() or len(set(row.values())) != len(row):
        return None
    for (ids, left, right, weight), z in zip(segments, parameters):
        p = row[left] if left in row else labels[left]
        q = row[right] if right in row else labels[right]
        w = x if weight == 'X' else weight
        row.update(zip(ids, path_values(p, q, w, z, None)))
    return row


def restore(parents, labels, blocked, jobs, gap, rng=None):
    """A job is (kind, windows, deficit, surplus). Its surplus is reserved.

    All pruning has already been done. The input labels belong to the compressed
    tree. Jobs are active, all positive-uniform, or all zero-uniform.
    """
    if not jobs:
        return gap
    rng = rng or Random(175)
    delayed = []
    n = len(parents)+len(blocked)
    width = 10*(n+1)**2
    for i, (kind, windows, b, t) in enumerate(jobs):
        layout = leafy_layout(kind, windows, labels, b, gap, None)
        segments, _, backward = layout
        last = i == len(jobs)-1
        if last and delayed and not backward:
            raise ValueError("the last window needs controls for the deferred leaves")
        dimension = 2+len(segments)
        # The finite box suffices by affine avoidance. Try independent fast
        # samples first and retain an exhaustive fallback.
        trials = chain(([rng.randrange(1, width+1) for _ in range(dimension)]
                        for _ in range(200)), box(width, dimension))
        for coords in trials:
            row = bare_row(layout, labels, t, coords)
            if row is None:
                continue
            values = set(row.values())
            if len(values) != len(row) or not blocked.isdisjoint(values-{t}):
                continue
            g = coords[1]
            if not last or not backward:
                break
            order = backward[:2]+delayed+backward[2:]
            jumps = {v: (row[parents[v]] if parents[v] in row else labels[parents[v]])
                     for v in order}
            new_gap = g-sum(jumps.values())
            residual, cycles, end = erasures(reversed(order), jumps, new_gap, None)
            assert end == g
            forbidden = blocked | values
            if new_gap == g or any(a in forbidden for _, a in residual):
                continue
            row.update(residual)
            taken = forbidden | set(row.values())
            for cycle in cycles:
                for shift in range(len(taken)*len(cycle)+1):
                    if all(a+shift not in taken for _, a in cycle):
                        row.update((v, a+shift) for v, a in cycle)
                        taken.update(a+shift for _, a in cycle)
                        break
                else:
                    raise AssertionError("integer translation exhausted")
            g = new_gap
            break
        else:
            raise AssertionError("integer window specialization exhausted")
        labels.update(row)
        blocked.update(row.values())
        gap = g
        delayed.extend(backward)
    return gap

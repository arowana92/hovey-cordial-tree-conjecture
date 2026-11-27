"""Restore a bare segment, forcing an arbitrarily low omitted ordinary weight."""

from itertools import chain
from random import Random

from research.hub.decorated_spine import path_values
from research.hub.pendant_repair import neutral_arm
from research.hub.polynomial_hub import add_transfer


def choose(instantiate, base, width, blocked, rng):
    choices = chain((rng.randrange(width) for _ in range(50)), range(width))
    for shift in choices:
        values = instantiate(base+shift)
        if len(set(values)) == len(values) and blocked.isdisjoint(values):
            return values
    raise AssertionError("integer path specialization exhausted")


def restore(parents, labels, fixed, child, bills, gap, capacity, radius, rng=None):
    """Insert 53+14*capacity real vertices in the given compressed edge.

    fixed contains the occupied labels, including any leaves installed in a
    seed. Return the minimum, and a bound on labels outside the final 43 sites.
    """
    if capacity < len(bills) or not 0 < child < len(parents) or radius < 0:
        raise ValueError("invalid compressed edge or insufficient repair capacity")
    rng = rng or Random(619)
    parent = parents[child]
    left, right = labels[parent], labels[child]
    length = 53+14*capacity
    ids = list(range(len(parents), len(parents)+length))
    parents.extend([parent]+ids[:-1])
    parents[child] = ids[-1]
    used = set(fixed) | set(labels.values())
    targets = {u for _, t in bills for u in (t, -t)}
    width = 100*(len(used)+length+len(targets)+10)

    def neutral(segment, p):
        def row(z):
            return neutral_arm(p, z, len(segment)-7)
        constant = row(0)[-1]
        slope = row(1)[-1]-constant
        values = choose(row, -constant//slope, width, used | targets, rng)
        labels.update(zip(segment, values))
        used.update(values)

    neutral(ids[:10], left)
    for j in range(capacity):
        segment = ids[10+14*j:24+14*j]
        p = labels[parents[segment[0]]]
        if j < len(bills):
            b, t = bills[j]
            add_transfer(labels, used, targets, segment, p, b, t, width, rng)
        else:
            neutral(segment, p)

    p = labels[ids[-44]]
    protected_bound = max(map(abs, used))
    scale = 630*(1+2000*(protected_bound+width+abs(gap)+radius+1)//630)
    omission = -scale
    used.add(omission)
    qids = ids[-43:]
    labels[qids[21]] = omission
    for segment, a, c, weight, z in ((qids[:21], p, omission, gap, 12*scale//7),
                                     (qids[22:], omission, right, left+right, 10*scale//9)):
        values = choose(lambda u: path_values(a, c, weight, u, None), z, width, used, rng)
        labels.update(zip(segment, values))
        used.update(values)
    return omission, protected_bound

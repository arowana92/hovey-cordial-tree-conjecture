"""Extend a prescribed cordial core across a bridge to a marked caterpillar."""

from .caterpillar_joint import extend as joint_at_deficit
from .caterpillar_leaf import staircase


def padded(spine, leaves, order):
    """Extend the far end of a spine with fresh integer vertex identifiers."""
    spine = list(spine)
    leaves = {u: list(leaves[u]) for u in spine}
    used = set(spine).union(*leaves.values())
    for v in range(min(used)-1, min(used)-1-(order-len(used)), -1):
        spine.append(v)
        leaves[v] = []
    return spine, leaves, used


def gap_labels(low, high, gap, shift, k):
    labels = {u: (i + int(i >= gap) - gap + shift) % k for u, i in low.items()}
    labels.update((v, (len(low)+1+j-gap+shift) % k) for v, j in high.items())
    return labels


def short_bridge(spine, leaves, mark, parent, surplus, k):
    spine, leaves, keep = padded(spine, leaves, k-1)
    ranks, _ = staircase(spine, leaves)
    A, B = ranks if mark in ranks[0] else ranks[::-1]
    r, a = A[mark], len(A)
    c = (parent-surplus) % k
    for t in range(a+1):
        if (a-r-t-int(r >= t)) % k == c:
            labels = gap_labels(A, B, t, surplus, k)
            break
    else:
        t = (-1-r-c) % k
        assert t <= len(B)
        labels = gap_labels(B, A, t, surplus, k)
    return {u: labels[u] for u in keep}


def short_joint(spine, leaves, parent, surplus, k):
    """The existing joint is spine[0], with at most k-1 new vertices."""
    spine, leaves, keep = padded(spine, leaves, k)
    A, B = staircase(spine, leaves)[0]
    joint = spine[0]
    free = {u: i-1 for u, i in A.items() if u != joint}
    c = (parent-surplus) % k
    if c <= len(B):
        labels = gap_labels(B, free, len(B)-c, surplus, k)
    else:
        labels = gap_labels(free, B, k-1-c, surplus, k)
    labels[joint] = parent
    return {u: labels[u] for u in keep}


def plain(spine, leaves):
    (A, B), _ = staircase(spine, leaves)
    return {**A, **{v: len(A)+j for v, j in B.items()}}, len(A)-1


def translated(values, shift, k):
    return {v: (i+shift) % k for v, i in values.items()}


def uniform_bridge(spine, leaves, mark, parent, k):
    values, missing = plain(spine, leaves)
    return translated(values, parent+values[mark]-missing, k)


def peel(spine, leaves, k):
    """Strip k vertices from the start. Return remainder and a restoration record."""
    remaining = k
    branch = {}
    for i, u in enumerate(spine):
        row = leaves[u]
        if remaining <= len(row):
            branch[u] = row[:remaining]
            rest = {**leaves, u: row[remaining:]}
            return spine[i:], rest, (spine[:i+1][::-1], branch, u, None)
        branch[u] = row
        remaining -= 1+len(row)
        if remaining == 0:
            return spine[i+1:], leaves, (spine[:i+1], branch, spine[i+1], u)
    raise ValueError("cannot strip this many vertices while retaining a joint")


def size(spine, leaves):
    return sum(1+len(leaves[u]) for u in spine)


def attach(spine, leaves, mark, parent, special, k, *, surplus):
    """Return labels on the exterior (integer vertices). Parent includes any bridge offset.

    If surplus=True, special is the surplus vertex residue of an order-one core.
    Otherwise it is the deficient edge residue of an order-zero core.
    """
    spine = list(spine)
    leaves = {u: list(leaves[u]) for u in spine}
    if k == 1:
        return dict.fromkeys(set(spine).union(*leaves.values()), 0)
    pending = []
    center = mark if mark in leaves else next(u for u in spine if mark in leaves[u])
    for _ in range(2):
        arm = size(spine[:spine.index(center)], leaves)
        for _ in range(arm//k):
            spine, leaves, record = peel(spine, leaves, k)
            pending.append(record)
        spine.reverse()

    n = size(spine, leaves)
    if n % k == 0:
        values = uniform_bridge(spine, leaves, mark, parent, k)
    elif n < k:
        if surplus:
            values = short_bridge(spine, leaves, mark, parent, special, k)
        else:
            raw, _ = plain(spine, leaves)
            values = translated(raw, special-parent-raw[mark], k)
    else:
        # The first k vertices should contain the mark. Orient the shorter arm first.
        j = spine.index(center)
        if size(spine[:j], leaves) > size(spine[j+1:], leaves):
            spine.reverse()
        if mark != center:
            leaves[center] = [mark] + [v for v in leaves[center] if v != mark]
            if size(spine[:spine.index(center)], leaves) == k-1:
                # Both arms have k-1 vertices. The case without another leaf
                # has order 2k and was handled by the divisible bridge.
                row = leaves[center]
                leaves[center] = row[1:] + [mark]
                spine, leaves, record = peel(spine, leaves, k)
                pending.append(record)
                leaves[center] = [mark] + [v for v in leaves[center] if v != mark]

        # Traverse each spine vertex before its pendant leaves.
        remaining = k
        prefix = {}
        for i, joint in enumerate(spine):
            row = leaves[joint]
            count = min(remaining-1, len(row))
            prefix[joint] = row[:count]
            remaining -= count+1
            if remaining == 0:
                break
        values = uniform_bridge(spine[:i+1], prefix, mark, parent, k)
        leaves[joint] = row[count:]
        spine = spine[i:][::-1]
        free = size(spine, leaves)-1
        for _ in range(free//k):
            spine, leaves, record = peel(spine, leaves, k)
            pending.append(record)
        if free % k:
            spine.reverse()
            if surplus:
                values.update(short_joint(spine, leaves, values[joint], special, k))
            else:
                values.update(joint_at_deficit(spine, leaves, joint, values, special, k))

    for part, rows, site, port in reversed(pending):
        if port is None:
            raw, _ = plain(part, rows)
            assert raw[site] == 0
            values.update(translated(raw, values[site], k))
        else:
            values.update(uniform_bridge(part, rows, port, values[site], k))
    return values

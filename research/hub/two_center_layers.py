"""Integer labeling of two adjacent centers with separately ranked branches."""

from research.hub.matched_arms import interval_lift


def two_center_tree(left, right, direct=(0, 0)):
    """Each entry is the positive number of children at one branch parent."""
    counts = [sorted(left, reverse=True), sorted(right, reverse=True)]
    if any(n < 1 for side in counts for n in side) or min(direct) < 0:
        raise ValueError("invalid leaf counts")
    a, b = map(len, counts)
    h, odd = divmod(a + b, 2)
    difference = abs(a-h)
    rank = h if difference == 0 else h - 2*difference + 1
    if odd or rank < 0 or min(a, b) < rank:
        raise ValueError("unsupported branch counts")
    if any(c > 1 for side in counts for c in side[rank:]):
        raise ValueError("too many branches with additional children")
    if any(direct) and (rank < h or any(side and d >= side[-1]
                                         for side, d in zip(counts, direct))):
        raise ValueError("insufficient children for a layer that includes the center")

    m = 2*h + 1
    indices = [h]
    sides = []
    for j in range(h, 0, -1):
        indices.extend((h-j, h+j))
        if j % 2 == 0:
            sides.extend((1, 0))
        elif j > h-rank:
            sides.extend((0, 1))
        else:
            sides.extend((int(a < b), int(a < b)))
    assert sides.count(0) == a and sides.count(1) == b
    labels = interval_lift([-1] + [0]*(a+b), indices, [(s, 0) for s in sides])
    assert labels is not None and labels[0] == h
    edges = [(0, 1)]
    for i, side in enumerate(sides, start=1):
        edges.extend(((side, 2*i), (2*i, 2*i+1)))
    by_label = {label: i for i, label in enumerate(labels)}
    lo, hi = 0, 2*m-1

    for side, profile in enumerate(counts):
        extras = [n-1 for n in profile[:rank]]
        if rank == h:
            extras.append(direct[side])
        for r, current in enumerate(extras, start=1):
            next_count = extras[r] if r < len(extras) else 0
            lower = (r-h) % 2 == side
            for _ in range(current - next_count):
                start = lo-r if lower else hi+1
                top_parent = m+r-1 if lower else m+r-2
                for i in range(r):
                    parent = by_label[top_parent-2*i]
                    edges.append((parent, len(labels)))
                    labels.append(start+i)
                if lower:
                    lo -= r
                else:
                    hi += r
    return edges, labels

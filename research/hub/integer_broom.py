"""Move an occupied omitted edge weight to the minimum using a pendant broom."""

from research.hub.marked_leaf_blocks import insertion


def finish(occupied, gap, parent, count, anchors):
    """Return broom root, its children, and (parent, label) upper fillers.

    After this step any missing integers between the two extremes can be
    supplied by leaves at zero. The caller tracks their number by the span.
    """
    if gap not in occupied or parent not in occupied or count < 1 or 0 not in anchors:
        raise ValueError("expected an occupied gap and parent, and a nonempty broom")
    if set(anchors) == {0, 1}:
        if parent > 0:
            raise ValueError("the two-site seed needs its nonpositive orientation")
        band = (1,)*(-parent)+(parent,)
        slot = -parent
    else:
        band, slot = insertion(tuple(anchors), parent, 0)
    # Only the last tip must be below the old minimum. The band can use any
    # fresh positions, since its incoming sums permute precisely that band.
    start = max(slot+1, (gap-min(occupied))//count+1)
    width = (len(band)+count)*len(occupied)+len(band)*count
    for x in range(start, start+width+1):
        base = x-slot
        band_values = range(base, base+len(band))
        if any(v in occupied for v in band_values):
            continue
        tips = [gap-j*x for j in range(1, count+1)]
        if any(v in occupied or v in band_values for v in tips):
            continue
        fillers = [(p, base+i) for i, p in enumerate(band) if i != slot]
        return x, tips, fillers
    raise AssertionError("integer broom specialization exhausted")

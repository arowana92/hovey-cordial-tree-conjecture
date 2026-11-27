"""Parameter boxes that put the omitted weight below all spine and leaf labels."""

from research.hub.decorated_spine import SLOPES
from research.hub.integer_layers import balanced_order


# Leading coefficients, in units of N/630, on the two bridges incident to
# the mark G near -N. Independent arithmetic checks recompute both rows.
RIGHT_MARK = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 270, 90, 270, -270, 360, -90, -180, 90, -270, 360)
LEFT_MARK = (350, -280, 70, -210, 350, -140, 140, 210, 140, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


def extremal_mass(total, bound, length, error, external_drift=0):
    if total <= 2*bound:
        raise ValueError("the combined positive control total must exceed twice the largest slope")
    return 10*(bound+1)*(error*(1+length//total)+external_drift//total+1)


def plan(kind, windows, extras, layout, labels, parents, delayed, width, old_bound, external):
    segments, marks, backward = layout
    length = len(backward)+len(delayed)-len(external)
    position = drift = 0
    for v in external:
        position += labels[parents[v]]
        drift = max(drift, abs(position))
    guard_scale = 10**4*(1+width+old_bound)
    error = 10**5*guard_scale
    if kind == 'active':
        segments = list(segments)
        signs, jumps = [], {}
        for w in extras:
            path = [w.left]+w.spine+[w.right]
            if len(w.spine) != 21 or w.children:
                raise ValueError("each additional control must be a leaf-only bridge")
            total = sum(a*len(w.direct[v]) for v, a in zip(path[1:-1], SLOPES))
            if not total:
                path.reverse()
                total = sum(a*len(w.direct[v]) for v, a in zip(path[1:-1], SLOPES))
            if not total:
                raise ValueError("the additional bridge has no active orientation")
            sign = 1 if total > 0 else -1
            signs.append(sign)
            for v, a in zip(path[1:-1], SLOPES):
                jumps.update((leaf, sign*a) for leaf in w.direct[v])
            segments.append((path[1:-1], path[0], path[-1], labels[w.left]+labels[w.right]))
        scale = extremal_mass(sum(jumps.values()), max(map(abs, SLOPES)), length+len(jumps), error, drift)
        order = backward[:2]+delayed+backward[2:]+balanced_order(jumps)
        centers = [0]*(2+len(segments)-len(signs))+[s*scale for s in signs]
        return (segments, marks, backward), order, centers

    if kind != 'uniform' or extras:
        raise ValueError("expected a uniform final block or additional active bridges")
    w, = windows
    m = len(w.direct[w.spine[0]])
    scale = 630*(1+10000*(error*(1+length//max(1, m))+drift//max(1, m)+1)//630)
    centers = [0, -scale, -guard_scale, -guard_scale, 12*scale//7, 10*scale//9]
    if not backward:
        if delayed:
            raise ValueError("an empty final block cannot take delayed leaves")
        return layout, [], centers
    guard = {leaf for ids, *_ in segments[:2] for v in ids for leaf in w.direct[v]}
    coefficients = {w.spine[65]: -630}
    coefficients.update(zip(segments[2][0], RIGHT_MARK))
    coefficients.update(zip(segments[3][0], LEFT_MARK))
    middle = backward[2:-2]
    early = [v for v in middle if v in guard]
    other = [v for v in middle if v not in guard]
    jumps = {v: coefficients.get(parents[v], 0) for v in other}
    order = backward[:2]+early+delayed+balanced_order(jumps)+backward[-2:]
    return layout, order, centers

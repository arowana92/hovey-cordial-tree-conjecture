"""An integer certificate with the unused weight at an endpoint, at any root."""

from research.hub.branches import anchor_labels, children_of


def positive_part(parents, children, removed, boundary, separate=False):
    """Label the retained tree, optionally separating Y-p and L+Y-p."""
    labels = [None]*len(parents)
    labels[0] = 0
    for value, v in enumerate(children[0], 1):
        labels[v] = value
    y = 2*len(children[0])+1
    order = [v for v, p in enumerate(parents) if p > 0 and v not in removed]
    if separate and parents[boundary] != 0:
        path = [boundary]
        while parents[path[-1]] != 0:
            path.append(parents[path[-1]])
        head = path.pop()
        path.reverse()
        sibling = next(v for v in children[head] if v != path[0] and children[v])
        tip = sibling
        while children[tip]:
            tip = children[tip][0]
        first = [sibling, boundary] if len(path) == 1 else path
        first_set = set(first)
        order = first + [v for v in order if v not in first_set and v != tip] + [tip]
    terminal = y
    for v in order:
        labels[v] = terminal
        terminal += labels[parents[v]]
    return labels, y, terminal


def pairs(labels, left, right, length, above=True):
    values = [x for x in labels if x is not None]
    edge = max(values) if above else min(values)
    for u, v in zip(left, right):
        start = edge+1 if above else edge-length-1
        labels[u], labels[v] = start, start+length
        edge = start+length if above else start


def extend(labels, parents, leaves, gap):
    for v in leaves:
        gap -= labels[parents[v]]
        labels[v] = gap
    return gap


def endpoint(parents):
    """Return labels, the omitted endpoint and the proof case."""
    if not parents or parents[0] != -1 or any(
            not 0 <= p < v for v, p in enumerate(parents[1:], 1)):
        raise ValueError("expected parent-before-child order with root zero")
    children = children_of(parents)
    supports = [[v for v in group if children[v]] for group in children]
    if not supports[0]:
        return list(range(len(parents))), 0, "star"
    labels = anchor_labels(parents)
    if labels is not None:
        return labels, min(labels), "anchor"

    depths = [0]*len(parents)
    for v, p in enumerate(parents[1:], 1):
        depths[v] = depths[p]+1
    fork = max((v for v in range(1, len(parents)) if len(supports[v]) >= 2),
               key=depths.__getitem__)
    chains = []
    for v in supports[fork]:
        chain = [v]
        while supports[v]:
            v, = supports[v]
            chain.append(v)
        chains.append(chain)
    longest = max(chains, key=len)
    path = len(longest) >= 3
    if path:
        a, b, c = longest[-3:]
        d = children[c][0]
        boundary = parents[a]
        left = [v for v in children[b] if v != c]
        right = [v for v in children[c] if v != d]
        side = [v for v in children[a] if v != b]
    else:
        def arm(chain):
            a = chain[0]
            b = chain[1] if len(chain) == 2 else children[a][0]
            return a, b, [v for v in children[a] if v != b], children[b]

        arms = [arm(chain) for chain in chains]
        # Prefer a pair admitting an unpaired leaf. Otherwise all arms agree.
        arms.sort(key=lambda arm: (len(arm[3]), len(arm[2])))
        if any(arm[2] for arm in arms):
            i = next(i for i, arm in enumerate(arms) if arm[2])
            chosen = [arms[i], arms[(i+1) % len(arms)]]
        else:
            chosen = [arms[0], arms[-1]]
        chosen.sort(key=lambda arm: (len(arm[3]), -len(arm[2])))
        (a, b, sa, left), (c, d, sc, right) = chosen
        side = sa+sc
        boundary = fork

    four = [a, b, c, d]
    removed = set(four+left+right+side)
    if side or len(left) != len(right):
        labels, y, l = positive_part(parents, children, removed, boundary)
        p = labels[boundary]
        if path and len(left) > len(right):
            left, right = right, left
            vals = (-p-l, -l, l, -p-2*l)
        elif path:
            vals = (-p-l, l, -l, -p)
        else:
            vals = (-p-l, l, -p, -l)
        for v, value in zip(four, vals):
            labels[v] = value
        singles = sorted(side+right[len(left):], key=lambda v: labels[parents[v]])
        gap = extend(labels, parents, singles, y)
        pairs(labels, left, right, l, above=False)
        return labels, gap, "unpaired"

    if path:
        labels, y, l = positive_part(parents, children, removed, boundary, True)
        p = labels[boundary]
        for v, value in zip(four, (y-p, l, -l, l+y-p)):
            labels[v] = value
        pairs(labels, left, right, l)
        return labels, -l, "balanced path"

    if len(arms) >= 3:
        first, second, third = arms[:3]
        nodes = [v for arm in (first, second, third) for v in arm[:2]]
        leaves = [v for arm in (first, second, third) for v in arm[3]]
        labels, y, l = positive_part(parents, children, set(nodes+leaves), fork)
        p = labels[fork]
        for v, value in zip(nodes, (-p-l, l, l+y, -l, -p, p+l+y)):
            labels[v] = value
        gap = extend(labels, parents, third[3], -p-l)
        pairs(labels, first[3], second[3], l)
        return labels, gap, "three equal arms"

    direct = [v for v in children[fork] if v not in (a, c)]
    removed.update(direct)
    boundary = parents[fork]
    if boundary == 0:
        labels, y, l = positive_part(parents, children, removed, fork)
        if l == y:
            labels[0] = 0
            vals = (4, -3, 1, -2, 2)
            for v, value in zip([fork]+four, vals):
                labels[v] = value
            gap = extend(labels, parents, left+right+direct, -3)
            top = 4
            for v in children[0]:
                if v != fork:
                    top += 1
                    labels[v] = top
            return labels, gap, "single branch at hub"
        p = 3*l+1
        labels[fork] = p
        for v, value in zip(four, (y-l, l, -p, p+y-l)):
            labels[v] = value
        gap = extend(labels, parents, left+right+direct, -p)
        return labels, gap, "large fork label"

    removed.add(fork)
    labels, y, l = positive_part(parents, children, removed, boundary, True)
    p = labels[boundary]
    if p > y and not (left or direct):
        vals = (-l, l, y-p, l+y-p, p-l)
        kind = "bare fork"
    else:
        vals = (l, -l, y-p, y-p-l, p+l)
        kind = "five sites"
    for v, value in zip([fork]+four, vals):
        labels[v] = value
    alternating = [v for uv in zip(left, right) for v in uv]
    gap = extend(labels, parents, alternating+direct, -l)
    return labels, gap, kind

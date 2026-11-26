"""Construct an ordinary integer one-hub certificate on an arbitrary rooted tree."""

from research.hub.branches import anchor_labels, children_of


def construct(parents):
    """Return vertex labels, the missing edge weight, and the construction used."""
    if not parents or parents[0] != -1 or any(
            not 0 <= p < i for i, p in enumerate(parents[1:], 1)):
        raise ValueError("expected a rooted tree in parent-before-child order")
    children = children_of(parents)
    supports = [[v for v in group if children[v]] for group in children]
    if not supports[0]:
        return list(range(len(parents))), 0, "star"
    depths = [0]*len(parents)
    for v, p in enumerate(parents[1:], 1):
        depths[v] = depths[p]+1
    forks = [v for v in range(1, len(parents)) if len(supports[v]) >= 2]
    if not forks:
        labels = anchor_labels(parents)
        return labels, min(labels), "anchor"

    fork = max(forks, key=depths.__getitem__)

    def chain(v):
        path = [v]
        while supports[v]:
            v, = supports[v]
            path.append(v)
        return path

    arms = [chain(v) for v in supports[fork]]
    longest = max(arms, key=len)
    if len(longest) >= 3:
        a, b, c = longest[-3:]
        end = children[c][0]
        nodes = [a, b, c, end]
        plus_leaves = [v for v in children[b] if v != c]
        minus_leaves = [v for v in children[c] if v != end]
        other_leaves = [v for v in children[a] if v != b]
        positive, negative = b, c
        kind = "path"
        if len(plus_leaves) > len(minus_leaves):
            plus_leaves, minus_leaves = minus_leaves, plus_leaves
            positive, negative = c, b
        boundary = parents[a]
    else:
        def arm(v):
            end = supports[v][0] if supports[v] else children[v][0]
            side = [u for u in children[v] if u != end]
            return v, end, side, children[end]

        pair = [arm(v) for v in supports[fork][:2]]
        pair.sort(key=lambda item: (len(item[3]), -len(item[2])))
        (a, b, left, plus_leaves), (c, end, right, minus_leaves) = pair
        nodes = [a, b, c, end]
        other_leaves = left+right
        positive, negative = b, end
        kind = "two arms"
        boundary = fork

    removed = set(nodes+other_leaves+plus_leaves+minus_leaves)
    labels = [None]*len(parents)
    labels[0] = 0
    for x, v in enumerate(children[0], 1):
        labels[v] = x
    gap = terminal = len(children[0])+1
    for v, p in enumerate(parents):
        if p > 0 and v not in removed:
            labels[v] = terminal
            terminal += labels[p]

    p, length = labels[boundary], terminal
    if kind == "two arms":
        values = (-p-length, length, -p, -length)
    elif positive == b:
        values = (-p-length, length, -length, -p)
    else:
        values = (-p-length, -length, length, -p-2*length)
    for v, value in zip(nodes, values):
        labels[v] = value

    paired = len(plus_leaves)
    unmatched = other_leaves+minus_leaves[paired:]
    # The most negative remaining parent permits the first label to clear L.
    for leaf in sorted(unmatched, key=lambda v: labels[parents[v]]):
        gap -= labels[parents[leaf]]
        labels[leaf] = gap
    top = max(gap, length)
    for u, v in zip(plus_leaves, minus_leaves):
        labels[u] = top+1
        labels[v] = top+1+length
        top = labels[v]
    return labels, gap, kind

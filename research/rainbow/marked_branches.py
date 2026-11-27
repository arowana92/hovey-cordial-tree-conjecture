"""Construct marked-leaf labelings using terminal paths and cuts away from the mark."""

from collections import Counter


def rooted(graph, root):
    parent = {root: None}
    order = [root]
    for v in order:
        for w in graph[v]:
            if w not in parent:
                parent[w] = v
                order.append(w)
    return parent, order


def induced(graph, vertices):
    return {v: [w for w in graph[v] if w in vertices] for v in graph if v in vertices}


def terminal_paths(graph, joint):
    paths = []
    for w in graph[joint]:
        prev, v = joint, w
        path = [v]
        while len(graph[v]) == 2:
            prev, v = v, next(u for u in graph[v] if u != prev)
            path.append(v)
        if len(graph[v]) == 1:
            paths.append(path)
    return sorted(paths, key=len)


def edge_deficit(graph, labels, k):
    weights = Counter((labels[v] + labels[w]) % k
                      for v in graph for w in graph[v] if v < w)
    return min(range(k), key=weights.__getitem__)


def label(graph, mark, k, witness, steps):
    """Use an order-k rainbow solver. Here k >= 5 and graph has a certified base."""
    n = len(graph)
    if mark is None:
        mark = next(v for v in graph if len(graph[v]) <= 1)
    if len(graph[mark]) > 1:
        raise ValueError("the mark must be a leaf")
    if n == 1:
        return {mark: 0}
    if n <= k:
        parent, order = rooted(graph, mark)
        pos = {v: i-1 for i, v in enumerate(order)}
        links = [pos[parent[v]] for v in order[1:]]
        # The last BFS vertex is a leaf. Extend its arm before using the base.
        links.extend(range(n-2, k-2))
        digits = witness(links, k)
        steps["base"] += 1
        return dict(zip(order, [0] + digits))

    t = (n-1) % k
    if not t:
        core = induced(graph, graph.keys() - {mark})
        labels = label(core, None, k, witness, steps)
        labels[mark] = (edge_deficit(core, labels, k) - labels[graph[mark][0]]) % k
        steps["surplus leaf"] += 1
        return labels

    joints = [v for v in graph if len(graph[v]) >= 3] or [mark]
    for joint in joints:
        arms = terminal_paths(graph, joint)
        if sum(map(len, arms)) < t:
            continue
        pieces = []
        left = t
        for arm in reversed(arms):
            take = min(len(arm), left)
            old = joint if take == len(arm) else arm[-take-1]
            pieces.append((arm[-take:], old))
            left -= take
            if not left:
                break
        pieces.sort(key=lambda piece: len(piece[0]))
        outside = {v for path, _ in pieces for v in path}
        core = induced(graph, graph.keys() - outside)
        in_core = mark in core
        labels = label(core, mark if in_core else None, k, witness, steps)
        surplus = Counter(labels.values()).most_common(1)[0][0]
        links = []
        for path, old in pieces:
            start = len(links)
            links.append(-1 - (labels[old]-surplus) % k)
            links.extend(range(start, start+len(path)-1))
        links.extend(range(t-1, k-2))
        digits = witness(links, k)
        order = [v for path, _ in pieces for v in path]
        labels.update((v, (x+surplus) % k) for v, x in zip(order, digits))
        steps["retained mark" if in_core else "removed mark"] += 1
        return labels

    parent, order = rooted(graph, mark)
    sizes = dict.fromkeys(order, 1)
    for v in reversed(order[1:]):
        sizes[parent[v]] += sizes[v]
    child = next(v for v in order[1:] if sizes[v] % k == 0)
    descendants = {child}
    for v in order:
        if parent[v] in descendants:
            descendants.add(v)
    branch = induced(graph, descendants)
    rest = induced(graph, graph.keys() - descendants)
    labels = label(rest, mark, k, witness, steps)
    moving = label(branch, None, k, witness, steps)
    shift = labels[parent[child]] + moving[child] - edge_deficit(branch, moving, k)
    labels.update((v, (x+shift) % k) for v, x in moving.items())
    steps["divisible cut away from mark"] += 1
    return labels

"""Local attachments over a prime field, using a bijective rainbow base solver."""

from collections import defaultdict

from research.census.caterpillar_leaf import staircase


def adjacency(edges):
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    return graph


def short_block(edges, joint, p, c, deficit, solve):
    """Use solve(edges,p) on a p-vertex tree. Vertex names are nonnegative integers."""
    tree = list(edges)
    if not 1 <= len(tree) <= p:
        raise ValueError("expected 1..p edges")
    graph = adjacency(tree)
    leaf = next(v for v in graph if v != joint and len(graph[v]) == 1)
    parent = graph[leaf][0]
    original = set(graph)
    dummy = list(range(max(original) + 1, max(original) + 1 + p - len(tree)))
    tree.extend((parent, v) for v in dummy)
    graph = adjacency(tree)

    if len(graph[joint]) == p:
        labels = {v: i for i, v in enumerate(graph[joint])}
        labels[joint] = c
    elif (deficit - 2 * c) % p == 0:
        neighbor = graph[joint][0]
        base_edges = [(neighbor if a == joint else a, neighbor if b == joint else b)
                      for a, b in tree if {a, b} != {joint, neighbor}]
        base = solve(base_edges, p)
        labels = {v: (y + c - base[neighbor]) % p for v, y in base.items()}
        labels[joint] = c
    else:
        removed = next(v for v, adj in graph.items()
                       if v != joint and len(adj) == 1 and adj[0] != joint)
        base = solve([(a, b) for a, b in tree if removed not in (a, b)], p)
        difference = base[graph[removed][0]] - base[joint]
        scale = (deficit - 2 * c) * pow(difference % p, -1, p) % p
        labels = {v: (c + scale * (y - base[joint])) % p for v, y in base.items()}
        labels[removed] = c

    if dummy and all((labels[a] + labels[b]) % p != deficit for a, b in edges):
        twin = next(v for v in dummy if (labels[v] + labels[parent]) % p == deficit)
        labels[twin], labels[leaf] = labels[leaf], labels[twin]
    return {v: labels[v] for v in original}


def spine(edges):
    graph = adjacency(edges)
    inside = {v for v in graph if len(graph[v]) > 1}
    if not inside:
        return [min(graph)]
    v = min(u for u in inside if len(inside.intersection(graph[u])) <= 1)
    line = []
    previous = None
    while v is not None:
        line.append(v)
        onward = [w for w in graph[v] if w in inside and w != previous]
        if len(onward) > 1:
            raise ValueError("nonleaf vertices must form a path")
        previous, v = v, next(iter(onward), None)
    return line


def caterpillar_base(edges, p):
    graph = adjacency(edges)
    line = spine(edges)
    internal = set(line)
    leaves = {v: [w for w in graph[v] if w not in internal] for v in line}
    (A, B), _ = staircase(line, leaves)
    return {**A, **{v: len(A) + j for v, j in B.items()}}


def split_tail(edges, joint, count):
    """Remove count end edges, retaining the joint in the other piece."""
    line = spine(edges)
    graph = adjacency(edges)
    positions = set(line)
    anchor = joint if joint in positions else graph[joint][0]
    direct = {v: [w for w in graph[v] if w not in positions and w != joint] for v in line}
    middle = line.index(anchor)
    left = line[:middle]
    right = line[middle + 1:][::-1]
    side = max((left, right), key=lambda row: sum(1 + len(direct[v]) for v in row))
    order = side + [anchor]
    tail = []
    for i, v in enumerate(order):
        tail.extend((v, w) for w in direct[v][:count - len(tail)])
        if len(tail) == count:
            cut = v
            break
        if i + 1 == len(order):
            raise ValueError("neither end has enough edges")
        cut = order[i + 1]
        tail.append((v, cut))
        if len(tail) == count:
            break
    taken = {frozenset(edge) for edge in tail}
    rest = [edge for edge in edges if frozenset(edge) not in taken]
    return rest, cut, tail


def caterpillar(edges, joint, p, c, deficit):
    """Extend a balanced core across a caterpillar with any number of edges."""
    rest = list(edges)
    tails = []
    while len(rest) > p:
        count = len(rest) % p or p
        rest, cut, tail = split_tail(rest, joint, count)
        tails.append((cut, tail))
    labels = short_block(rest, joint, p, c, deficit, caterpillar_base)
    if not tails:
        return labels
    # Counts start with one of every old edge except at the deficient bin.
    bins = [int(i != deficit) for i in range(p)]
    def add_weights(piece):
        for u, v in piece:
            bins[(labels[u] + labels[v]) % p] += 1
    add_weights(rest)
    for cut, tail in reversed(tails):
        d = bins.index(min(bins))
        labels.update(short_block(tail, cut, p, labels[cut], d, caterpillar_base))
        add_weights(tail)
    return labels

"""Reduce a tree with sparse edge offsets to the bounded-degree embedding lemma."""
from collections import Counter
from functools import reduce
from math import gcd

from check import adjacency
from check_excess import choose_variables, expression
from partial_gap import build


def edge(u, v):
    return (u, v) if u < v else (v, u)


def closed(graph, vertices):
    blocked = set(vertices)
    for v in vertices:
        blocked.update(graph[v])
    return blocked


def reduction(edges, offsets, cap, rng):
    """Return the auxiliary tree, missing weight, prescribed labels and degree core."""
    k = len(edges) + 1
    graph = adjacency(k, edges)
    offsets = {edge(a, b): d % k for (a, b), d in offsets.items() if d % k}
    main = set(offsets)
    remaining = [row.copy() for row in graph]

    def cut(u, v):
        remaining[u].remove(v)
        remaining[v].remove(u)

    for u, v in main:
        cut(u, v)
    for u, row in enumerate(remaining):
        for v in sorted(row)[cap:]:
            cut(u, v)
            main.add(edge(u, v))

    fixed = {v for pair in main for v in pair}
    leaves = [v for v, row in enumerate(graph) if len(row) == 1]
    free = [v for v in leaves if v not in fixed]
    sparse_leaves = len(free) < 2
    reserved = leaves[:2] if sparse_leaves else free[:2]
    if sparse_leaves:
        fixed.update(v for v, row in enumerate(graph) if len(row) != 2)

    blocked = closed(graph, fixed | set(reserved))
    private = []
    for u, v in edges:
        if len(private) == len(main):
            break
        if u in blocked or v in blocked:
            continue
        private.append(edge(u, v))
        cut(u, v)
        blocked.update(closed(graph, (u, v)))
    if len(private) != len(main):
        raise ValueError("insufficient room for private edges")
    buffers = {v for pair in private for v in pair}
    fixed.update(buffers)
    blocked = closed(graph, fixed | set(reserved))

    component = {}
    pools = []
    for start in range(k):
        if start in component:
            continue
        i = len(pools)
        pools.append([])
        vertices = [start]
        component[start] = i
        for v in vertices:
            if v not in blocked:
                pools[i].append(v)
                blocked.update(graph[v])
            for w in sorted(remaining[v]):
                if w not in component:
                    component[w] = i
                    vertices.append(w)
    priority = sorted(range(len(pools)), key=lambda i: -len(pools[i]))
    root = next(v for v in range(k) if component[v] == priority[0])
    order = [root]
    parent = {root: None}
    for v in order:
        for w in sorted(graph[v]):
            if w not in parent:
                parent[w] = v
                order.append(w)
    assert len(order) == k

    def child(pair):
        a, b = pair
        return a if parent[a] == b else b

    # A relocated edge has the other member of its pair's original weight.
    cuts = main | set(private)
    targets = {}
    for first, second in zip(sorted(main), private):
        for old, assigned in ((first, second), (second, first)):
            r = child(old)
            targets[component[r]] = (r, assigned)
    kept = [(u, v) for u, v in edges if edge(u, v) not in cuts]
    sites = {}
    available = pools[priority[0]][:]
    for i in priority[1:]:
        r, assigned = targets[i]
        if not available:
            raise ValueError("insufficient room for fresh attachment sites")
        s = available.pop()
        kept.append((s, r))
        sites[s] = (assigned, r)
        available.extend(pools[i])

    late = set(reserved) if sparse_leaves else set()
    variables = [v for v in order if v in fixed - buffers - late] + sorted(buffers) + sorted(late)
    index = {v: i for i, v in enumerate(variables)}
    forms = {v: expression((i, 1)) for v, i in index.items()}
    for s, ((a, b), r) in sites.items():
        forms[s] = expression((index[a], 1), (index[b], 1), (index[r], -1),
                              constant=offsets.get(edge(a, b), 0))
    weights = [expression((index[a], 1), (index[b], 1), constant=offsets.get(edge(a, b), 0))
               for a, b in edges if a in fixed and b in fixed]
    if sparse_leaves:
        gap_form = expression(*[(index[v], 2-len(graph[v])) for v in fixed],
                              constant=-sum(range(k))-sum(offsets.values()))
        weights.append(gap_form)
    evaluate = choose_variables(list(forms.values()), weights, k, rng)
    pins = {v: evaluate(form) for v, form in forms.items()}
    if sparse_leaves:
        gap = evaluate(gap_form)
    else:
        degree = Counter(v for pair in kept for v in pair)
        divisor = reduce(gcd, (degree[v]-1 for v in range(k) if v not in pins), k)
        residue = -sum((degree[v]-1)*x for v, x in pins.items()) % divisor
        used = {evaluate(form) for form in weights}
        gap = next(w for w in range(residue, k, divisor) if w not in used)
    core = build(kept, pins, gap, rng)
    assert core is not None
    return kept, gap, pins, core, sparse_leaves

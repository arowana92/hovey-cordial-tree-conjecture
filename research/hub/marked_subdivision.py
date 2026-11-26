"""Extend a marked interval seed along several specified edges."""

from collections import Counter
from random import Random

from research.hub.marked_leaf_blocks import complete
from research.hub.marked_leaf_geometry import at_target, child_label, pad
from research.hub.polynomial_hub import elongate
from research.hub.two_hubs import edge


def lattice_stretch(tree, anchors, p, q, step):
    """Produce a three-edge path whose first new label is a negative multiple of step."""
    low = child_label(tree, anchors, p, 1)
    high = child_label(tree, anchors, q, 0)
    x = step * (min(-step, low-2, p+q-high) // step)
    y = p+q-x
    at_target(tree, anchors, p, 1, x)
    at_target(tree, anchors, q, 0, y)
    tree.edges.remove(edge(p, q))
    tree.edges.add(edge(x, y))
    return x, y


def inflate(graph, seed, jobs):
    """For each (u,v,count), insert 4+12*count original vertices on that edge."""
    tree, old_labels, anchors = seed
    graph = {v: set(neighbors) for v, neighbors in graph.items()}
    labels = old_labels.copy()
    step = max(anchors)
    if step < 2 or 0 not in anchors:
        raise ValueError("need an upper step of at least two and a zero anchor")
    paths = []
    for u, v, count in jobs:
        if v not in graph[u] or count < 0:
            raise ValueError("invalid subdivision job")
        graph[u].remove(v)
        graph[v].remove(u)
        p, q = labels[u], labels[v]
        x, y = lattice_stretch(tree, anchors, p, q, step)
        left, right = lattice_stretch(tree, anchors, x, y, step)
        paths.append((u, v, count, x, left, right, y))

    # Each lower block has a nonzero parent only at its first position.
    padding = (tree.lo-1) % step
    if padding == 1:
        padding += step
    pad(tree, anchors, padding, 1)
    assert tree.lo % step == 1
    protected = max(abs(tree.lo), abs(tree.hi)) // step
    used = set()
    next_id = max(graph)+1
    rng = Random(4729)
    for u, v, count, x, left, right, y in paths:
        positions = list(range(12*count+2))
        values = {positions[0]: x//step, positions[-1]: left//step}
        limit = 12*(len(used)+12*count+2*protected+1)+67
        elongate(values, used, positions, limit, rng, avoid_radius=protected)
        inside = [step*values[j] for j in positions[1:-1]]
        row = [x, *inside, left, right, y]
        prev = u
        for value in row:
            labels[next_id] = value
            graph[prev].add(next_id)
            graph[next_id] = {prev}
            prev = next_id
            next_id += 1
        graph[prev].add(v)
        graph[v].add(prev)
        if inside:
            tree.edges.remove(edge(x, left))
            tree.edges.update(edge(p, q) for p, q in zip([x]+inside, inside+[left]))

    required = {step*z for z in used}
    if required:
        tree.extend(max(0, max(required)-tree.hi), 0)
        while tree.lo > min(required):
            start = tree.lo-step
            for i in range(step):
                tree.leaf(step if i==0 else 0, start+i)
            tree.lo = start
        reclaimed = {v for p, v in tree.added if p==0 and v in required}
        assert reclaimed == required
        tree.added = [(p,v) for p,v in tree.added if v not in reclaimed]
        tree.edges.difference_update(edge(0,v) for v in reclaimed)
    return graph, (tree, labels, anchors)


def finish_marked(seed, populations):
    """Only the vertex labels of sites that actually receive leaves enter the reserve bound."""
    tree, labels, anchors = seed
    remaining = Counter({labels[v]: n for v,n in populations.items()})
    remaining.subtract(p for p,_ in tree.added)
    if min(remaining.values()) < 0:
        raise ValueError("the interval seed consumed more than the available leaves")
    return complete(remaining, anchors)

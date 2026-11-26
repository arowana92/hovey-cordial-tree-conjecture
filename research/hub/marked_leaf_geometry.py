"""Inflate parity representatives to arbitrary marked trees using only marked fillers."""

from collections import deque
from functools import lru_cache
from itertools import permutations
import json

from .marked_leaf_blocks import insertion
from .marked_leaf_verify import DATA
from .two_hubs import Completion, edge


@lru_cache(None)
def records():
    return {(m, tuple(map(tuple, edges)), mask): cert for m, edges, mask, cert
            in map(json.loads, DATA.read_text().splitlines())}


def steiner(graph, marks):
    result = {v: set(nbrs) for v, nbrs in graph.items()}
    todo = deque(v for v in graph if v not in marks and len(graph[v]) == 1)
    while todo:
        v = todo.popleft()
        u, = result.pop(v)
        result[u].remove(v)
        if len(result[u]) == 1 and u not in marks:
            todo.append(u)
    return result


def paths_between(tree, ordered):
    index = {v: i for i, v in enumerate(ordered)}
    paths = {}
    for i, u in enumerate(ordered):
        for v in tree[u]:
            path = [u, v]
            while path[-1] not in index:
                parent, tip = path[-2:]
                child, = tree[tip] - {parent}
                path.append(child)
            j = index[path[-1]]
            if i < j:
                paths[i, j] = path
    return paths


def terminal_records(node):
    if isinstance(node, dict):
        for child in node["children"]:
            yield from terminal_records(child)
    else:
        yield node


def child_label(tree, anchors, p, side):
    parents, slot = insertion(anchors, p, side)
    return (tree.lo-len(parents) if side else tree.hi+1) + slot


def attach(tree, anchors, p, side=0):
    parents, slot = insertion(anchors, p, side)
    base = tree.lo-len(parents) if side else tree.hi+1
    for i, a in enumerate(parents):
        if i == slot:
            tree.edges.add(edge(p, base+i))
        else:
            tree.leaf(a, base+i)
    if side:
        tree.lo = base
    else:
        tree.hi += len(parents)
    return base+slot


def pad(tree, anchors, width, side):
    if side == 0 or 1 in anchors:
        tree.extend(width if side == 0 else 0, width if side else 0)
        return
    assert width == 0 or width >= 2
    if width % 2:
        for j, p in enumerate((2, 2, -1)):
            tree.leaf(p, tree.lo-3+j)
        tree.lo -= 3
        width -= 3
    for _ in range(width//2):
        tree.leaf(2, tree.lo-2)
        tree.leaf(0, tree.lo-1)
        tree.lo -= 2


def at_target(tree, anchors, p, side, target):
    initial = child_label(tree, anchors, p, side)
    width = initial-target if side else target-initial
    assert width >= 0
    pad(tree, anchors, width, side)
    actual = attach(tree, anchors, p, side)
    assert actual == target


def stretch(tree, anchors, p, q):
    low = child_label(tree, anchors, p, 1)
    high = child_label(tree, anchors, q, 0)
    x = low-max(2, low+high-p-q)
    y = p+q-x
    at_target(tree, anchors, p, 1, x)
    at_target(tree, anchors, q, 0, y)
    tree.edges.remove(edge(p, q))
    tree.edges.add(edge(x, y))
    return x, y


def grow(graph, tree, labels, anchors):
    todo = deque(labels)
    while todo:
        u = todo.popleft()
        for v in sorted(graph[u]):
            if v not in labels:
                labels[v] = attach(tree, anchors, labels[u])
                todo.append(v)


def geometry_seed(graph, marks, counts=None):
    """Three marks are in label order 0,2,-1. Four are in decreasing population order."""
    hull = steiner(graph, set(marks))
    junctions = [v for v in hull if len(hull[v]) >= 3 and v not in marks]
    choices = []
    for perm in permutations(junctions):
        order = tuple(marks) + perm
        paths = paths_between(hull, order)
        choices.append((tuple(sorted(paths)), order, paths))
    skeleton, order, paths = min(choices, key=lambda row: row[:2])
    mask = sum((len(paths[key]) % 2) << j for j, key in enumerate(skeleton))
    m = len(marks)
    node = records()[m, skeleton, mask]

    def slack(seed):
        moment = sum(counts[v]*p for v, p in zip(marks, seed[2]))
        return min(moment, sum(counts[v] for v in marks)-moment)
    seed = max(terminal_records(node), key=slack) if m == 4 else node
    lo, hi, f, fillers = seed
    anchors = tuple(sorted(f[:m]))
    labels = dict(zip(order, f))
    next_id = len(order)
    segments, edges = {}, []
    for j, (u, v) in enumerate(skeleton):
        segment = [f[u], f[v]]
        if mask & (1 << j):
            segment.insert(1, f[next_id])
            next_id += 1
        segments[u, v] = segment
        edges.extend(zip(segment, segment[1:]))
    missing = sorted(set(range(lo, hi+1))-set(f))
    tree = Completion(edges[0], leaves=zip(fillers, missing), twig_edges=edges[1:])
    for key in skeleton:
        segment = segments[key]
        while len(segment) < len(paths[key]):
            x, y = stretch(tree, anchors, segment[0], segment[1])
            segment[1:1] = [x, y]
        labels.update(zip(paths[key], segment))
    grow(graph, tree, labels, anchors)
    return tree, labels, anchors

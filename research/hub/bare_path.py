"""Construct a rational hub labeling across a bare seven-edge path."""

from collections import Counter
from itertools import product

from research.hub.branches import children_of
from research.rainbow.verify import rooted_shapes


def bridge_labels(parents, path):
    """Return integer labels. The near endpoint must have positive even depth."""
    children = children_of(parents)
    if (len(path) != 8 or any(parents[v] != u for u, v in zip(path, path[1:]))
            or any(len(children[v]) != 1 for v in path[1:-1])):
        raise ValueError("expected a downward seven-edge path with bare interior")
    near, far = path[0], path[-1]
    stem = []
    v = near
    while v:
        stem.append(v)
        v = parents[v]
    if not stem or len(stem) % 2:
        raise ValueError("the near endpoint must have positive even depth")

    labels = [None] * len(parents)
    labels[0] = 0
    negative, positive = 0, 3 * len(children[0]) + 1
    labels[far] = positive
    for j, v in enumerate(children[0]):
        labels[v] = -(3 * j + 2)

    def grow(v):
        nonlocal negative, positive
        p = labels[parents[v]]
        if p > 0:
            negative -= p
            labels[v] = negative
        else:
            positive -= p
            labels[v] = positive

    for v in reversed(stem[:-1]):
        grow(v)
    omitted = set(path[1:-1])
    for v in range(1, len(parents)):
        if labels[v] is None and v not in omitted:
            grow(v)

    p, q, w = labels[near], labels[far], positive
    # Six times each vertex label, from the near side to the far side.
    internal = [-4*p-2*q, 2*(p-q), q-p+3*w, p-q+3*w, 2*(q-p), -2*p-4*q]
    answer = [6*x if x is not None else None for x in labels]
    for v, x in zip(path[1:-1], internal):
        answer[v] = x
    return answer


def verify(parents, path):
    labels = bridge_labels(parents, path)
    sums = [labels[i]+labels[p] for i, p in enumerate(parents) if i]
    if (labels[0] != 0 or len(set(labels)) != len(labels)
            or len(set(sums)) != len(sums) or not set(sums) < set(labels)):
        raise ValueError("vertex labels or endpoint sums failed")
    return labels


def example(left, right, depth):
    parents = [-1] + list(range(depth))
    for i, p in enumerate(left[1:], 1):
        parents.append(depth + p)
    path = [depth]
    for _ in range(7):
        parents.append(path[-1])
        path.append(len(parents)-1)
    for i, p in enumerate(right[1:], 1):
        parents.append(path[-1] + p)
    # An additional nontrivial branch at the hub tests both signs off the stem.
    index = len(parents)
    parents.extend([0, index, index+1, 0])
    return parents, path


def check_period(parents, labels, k):
    vertex = Counter(x % k for x in labels)
    edge = Counter((labels[i]+labels[p]) % k for i, p in enumerate(parents) if i)
    gap, = vertex.keys() - edge.keys()
    period = sorted(set(range(k))-vertex.keys()) + [gap] + sorted(edge)
    # Check all residues including empty ones at every extension.
    for x in period * 2:
        vertex[x] += 1
        edge[x] += 1
        for hist in (vertex, edge):
            values = [hist[i] for i in range(k)]
            if max(values) - min(values) > 1:
                raise ValueError("unbalanced leaf extension")


if __name__ == "__main__":
    small = [t for n in range(1, 6) for t in rooted_shapes(n).values()]
    count = 0
    for left, right, depth in product(small, small, (2, 4, 6, 8)):
        parents, path = example(left, right, depth)
        verify(parents, path)
        count += 1
    parents, path = example((-1, 0, 1), (-1, 0, 0), 2)
    labels = verify(parents, path)
    span = max(labels)-min(labels)
    for k in (span+1, span+2):
        check_period(parents, labels, k)
    print(f"{count} full-tree integer labelings; two leaf periods at {span+1} and {span+2}.")

"""Construct and check integer interval labelings after adding leaves at two hubs."""

from collections import deque
from functools import reduce
from itertools import permutations
from math import gcd
from random import Random

from research.rainbow.verify import rooted_shapes


def edge(x, y):
    return (min(x, y), max(x, y))


class Completion:
    def __init__(self, path, leaves=()):
        self.path = list(path)
        self.edges = {edge(x, y) for x, y in zip(path, path[1:])}
        self.added = []
        for hub, label in leaves:
            self.leaf(hub, label)
        self.lo = min(x for e in self.edges for x in e)
        self.hi = max(x for e in self.edges for x in e)

    def leaf(self, hub, label):
        self.edges.add(edge(hub, label))
        self.added.append((hub, label))

    def extend(self, at_zero, at_one):
        for x in range(self.hi + 1, self.hi + 1 + at_zero):
            self.leaf(0, x)
        self.hi += at_zero
        for x in range(self.lo - at_one, self.lo):
            self.leaf(1, x)
        self.lo -= at_one

    def child(self, p):
        if p > 0:
            x = self.lo - p
            for z in range(x + 1, self.lo):
                self.leaf(0, z)
            self.lo = x
        else:
            x = self.hi + 1 - p
            for z in range(self.hi + 1, x):
                self.leaf(1, z)
            self.hi = x
        self.edges.add(edge(p, x))
        return x

    def stretch(self):
        i = next(i for i, (p, q) in enumerate(zip(self.path, self.path[1:])) if p*q < 0)
        left, right = self.path[i:i+2]
        p, q = max(left, right), min(left, right)
        # Make p+q-x achievable by the upper-end rule before choosing x.
        needed = self.hi + 1 - q - (p + q - (self.lo - p))
        self.extend(0, max(0, needed))
        x = self.child(p)
        self.extend(p + q - x - (self.hi + 1 - q), 0)
        y = self.child(q)
        assert x + y == p + q
        self.edges.remove(edge(p, q))
        self.edges.add(edge(x, y))
        self.path[i+1:i+1] = [x, y] if left == p else [y, x]


def path_seed(distance):
    if distance <= 0 or distance in (2, 4):
        raise ValueError("expected distance 1, 3 or at least 5")
    if distance % 2:
        s = distance // 2
        zig = [i//2 if i % 2 == 0 else s-i//2 for i in range(s+1)]
        positions = zig + list(reversed(zig))
        return Completion([-z if i % 2 == 0 else 1+z for i, z in enumerate(positions)])
    result = Completion([0, 2, -1, 4, -4, 3, 1], [(0, -3), (0, -2)])
    for _ in range((distance - 6)//2):
        result.stretch()
    return result


def complete(parents, a, b):
    """Return original-vertex labels and the augmented tree, indexed by label."""
    graph = [[] for _ in parents]
    for i, p in enumerate(parents[1:], 1):
        graph[i].append(p)
        graph[p].append(i)
    prev = {a: None}
    todo = deque([a])
    while todo:
        v = todo.popleft()
        for w in graph[v]:
            if w not in prev:
                prev[w] = v
                todo.append(w)
    path = []
    v = b
    while v is not None:
        path.append(v)
        v = prev[v]
    path.reverse()
    result = path_seed(len(path)-1)
    labels = dict(zip(path, result.path))
    todo = deque(path)
    while todo:
        v = todo.popleft()
        for w in graph[v]:
            if w not in labels:
                labels[w] = result.child(labels[v])
                todo.append(w)
    return [labels[i] for i in range(len(parents))], result


def check(parents, a, b, labels, result):
    assert labels[a] == 0 and labels[b] == 1
    all_labels = labels + [x for _, x in result.added]
    assert sorted(all_labels) == list(range(result.lo, result.hi+1))
    assert all(hub in (0, 1) for hub, _ in result.added)
    tree_edges = [edge(labels[i], labels[p]) for i, p in enumerate(parents) if i]
    tree_edges += [edge(hub, x) for hub, x in result.added]
    assert set(tree_edges) == result.edges
    assert sorted(x+y for x, y in tree_edges) == list(range(result.lo+1, result.hi+1))


def feasible(rows):
    """Eliminate one variable from integer-coefficient real inequalities >= 0."""
    while rows and len(rows[0]) > 1:
        positive = [r for r in rows if r[0] > 0]
        negative = [r for r in rows if r[0] < 0]
        new = {r[1:] for r in rows if r[0] == 0}
        for p in positive:
            for n in negative:
                comb = [p[0]*y - n[0]*x for x, y in zip(p[1:], n[1:])]
                divisor = reduce(gcd, comb, 0) or 1
                new.add(tuple(x//divisor for x in comb))
        rows = list(new)
        if any(not any(r[:-1]) and r[-1] < 0 for r in rows):
            return False
    return all(r[-1] >= 0 for r in rows)


def excluded(distance):
    d = distance
    zero = (0,) * d
    one = zero[:-1] + (1,)
    variables = [tuple(int(i == j) for j in range(d)) for i in range(d-1)]
    vertices = [zero, *variables, one]
    sums = [tuple(x+y for x, y in zip(p, q)) for p, q in zip(vertices, vertices[1:])]

    def diff(x, y, minimum):
        return tuple(z-w-(minimum if j == d-1 else 0) for j, (z, w) in enumerate(zip(x, y)))

    cases = 0
    for order in permutations(vertices):
        if order.index(one) != order.index(zero) + 1:
            continue
        for weights in permutations(sums):
            rows = [r for x, y, w in zip(order, order[1:], weights)
                    for r in (diff(w, x, 1), diff(y, w, 0))]
            assert not feasible(rows), (order, weights)
            cases += 1
    return cases


if __name__ == "__main__":
    cases = 0
    for n in range(2, 10):
        for parents in rooted_shapes(n).values():
            labels, result = complete(parents, 0, 1)
            check(parents, 0, 1, labels, result)
            result.extend(2, 3)
            check(parents, 0, 1, labels, result)
            cases += 1
    rng = Random(901)
    for d in (1, 3, *range(5, 25)):
        for _ in range(6):
            parents = [-1, *range(d)]
            for i in range(d+1, d+9):
                parents.append(rng.randrange(i))
            labels, result = complete(parents, 0, d)
            check(parents, 0, d, labels, result)
            result.extend(rng.randrange(6), rng.randrange(6))
            check(parents, 0, d, labels, result)
            cases += 1
    print(f"{cases} completed trees, before and after further leaves at both hubs.")
    for d in (2, 4):
        print(f"Distance {d}: all {excluded(d)} ordered inequality systems infeasible.")

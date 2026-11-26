"""Construct the uniform-threshold seed and independently check the induction cases."""

import json
from collections import Counter, deque
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
from math import ceil
from random import Random

from .many_leaf_parents import make_seed, upper_child, verify
from .two_hubs import Completion, edge
from .uniform_leaf_construct import exact_blocks
from .uniform_leaf_verify import CERTIFICATE, CORES


@lru_cache(None)
def bounds(h):
    if h == 5:
        return 17, Fraction(1, 22)
    previous, eta = bounds(h-1)
    c = eta / (4*(previous+1))
    f = 2**(h+4)
    y = 2*f + ceil(2/c) + 4
    q = 2*(y+f)
    return max(2*previous, 2*q+h, h+ceil(16*f*q/c)), eta/2


@lru_cache(None)
def five_records():
    return json.loads(CERTIFICATE.read_text())


def five_seed(graph, counts):
    edges = {edge(u, v) for u in graph for v in graph[u]}
    total = sum(counts[v] for v in graph)
    rest = total - max(counts[v] for v in graph)
    for canon, record in zip(CORES, five_records()):
        for vertices in permutations(graph):
            if {edge(vertices[a], vertices[b]) for a, b in canon} != edges:
                continue
            for f, (lo, hi, fillers) in record["seeds"]:
                labels = dict(zip(vertices, f))
                moment = sum(counts[v]*labels[v] for v in graph)
                if 22*min(moment, total-moment) < rest:
                    continue
                missing = sorted(set(range(lo, hi+1)) - set(f))
                a, b = canon[0]
                tree = Completion([f[a], f[b]], leaves=zip(fillers, missing),
                                  twig_edges=[(f[u], f[v]) for u, v in canon[1:]])
                return tree, labels
    raise AssertionError("no five-vertex seed")


def rooted_order(graph):
    order = [next(iter(graph))]
    parent = {order[0]: -1}
    for u in order:
        for v in graph[u]:
            if v not in parent:
                parent[v] = u
                order.append(v)
    index = {v: i for i, v in enumerate(order)}
    return order, [-1] + [index[parent[v]] for v in order[1:]]


def choose_seed(graph, counts, trace):
    h = len(graph)
    if h == 5:
        trace.add("five")
        return five_seed(graph, counts)
    maximum = max(graph, key=counts.__getitem__)
    total = sum(counts[v] for v in graph)
    rest = total - counts[maximum]
    previous, eta = bounds(h-1)
    cutoff = eta / (4*(previous+1))
    leaves = [v for v in graph if len(graph[v]) == 1]
    lightest = min(leaves, key=counts.__getitem__)
    if counts[lightest] <= cutoff*rest:
        trace.add("light leaf")
        neighbor, = graph[lightest]
        reduced = {v: graph[v] - {lightest} for v in graph if v != lightest}
        tree, labels = choose_seed(reduced, counts, trace)
        labels[lightest] = tree.child(labels[neighbor])
        return tree, labels

    f = 2**(h+4)
    y = 2*f + ceil(2/cutoff) + 4
    if total >= 2*h*rest:
        if len(graph[maximum]) == h-1:
            trace.add("dominant star center")
            labels = {maximum: 0}
            labels.update((v, i) for i, v in enumerate(graph[maximum], 1))
            tree = Completion([0, 1], twig_edges=[(0, i) for i in range(2, h)])
            return tree, labels
        u, v = next((u, v) for u in graph[maximum] for v in graph[u] if v != maximum)
        q = max((q for q in leaves if q not in (maximum, u, v)), key=counts.__getitem__)
        tree = Completion([0, 1, -1])
        labels = {maximum: 0, u: 1, v: -1}
        queue = deque(labels)
        while queue:
            parent = queue.popleft()
            for child in graph[parent]:
                if child != q and child not in labels:
                    labels[child] = upper_child(tree, labels[parent])
                    queue.append(child)
        parent, = graph[q]
        p = labels[parent]
        # The proof uses y. Any smaller feasible label reaching moment >= rest works.
        partial = sum(counts[v]*z for v, z in labels.items())
        target = max(tree.hi+1-min(0, p), ceil(Fraction(rest-partial, counts[q])))
        assert target <= y
        moment = partial + counts[q]*target
        mandatory = total >= 2*(y+f)*rest
        if mandatory or (target <= 2*f and total-moment >= rest):
            assert min(moment, total-moment) >= rest
            trace.add("dominant vertex")
            tree.extend(target - (tree.hi+1-min(0, p)), 0)
            labels[q] = upper_child(tree, p)
            return tree, labels

    trace.add("two adjustable leaves")
    x, y_vertex = leaves[:2]
    order, parents = rooted_order(graph)
    inner = set(graph) - {x, y_vertex}
    path = next((a, b, c) for b in inner for a in graph[b] & inner
                for c in graph[b] & inner if a != c)
    tree, indexed = make_seed(parents, [counts[v] for v in order],
                              tuple(order.index(v) for v in path),
                              order.index(x), order.index(y_vertex))
    return tree, {order[i]: z for i, z in indexed.items()}


def check_case(parents, counts, trace):
    graph = {i: set() for i in range(len(parents))}
    for i, p in enumerate(parents[1:], 1):
        graph[i].add(p)
        graph[p].add(i)
    tree, labels = choose_seed(graph, counts, trace)
    total, rest = sum(counts), sum(counts)-max(counts)
    limit, eta = bounds(len(graph))
    moment = sum(counts[v]*z for v, z in labels.items())
    assert tree.hi-tree.lo+1 <= limit and min(moment, total-moment) >= eta*rest
    # Check the seed against the actual original tree, then scale the population
    # ray until the explicit completion can pay every filler. The seed stays fixed.
    spent = Counter(p for p, z in tree.added)
    d = 1+max(labels.values())-min(labels.values())
    reserve = (2*len(graph)+2)*d*d
    cost = max(abs(sum(p*n for p, n in spent.items())),
               abs(sum((1-p)*n for p, n in spent.items())))
    factor = max(1, ceil(Fraction(reserve+sum(spent.values()), min(counts))),
                 ceil(Fraction(reserve+cost, min(moment, total-moment))))
    scaled = [n*factor for n in counts]
    remaining = Counter({p: scaled[v] for v, p in labels.items()})
    remaining.subtract(spent)
    blocks = exact_blocks(remaining)
    verify(parents, scaled, tree, labels, blocks)


if __name__ == "__main__":
    trace = set()
    rng = Random(20261126)
    trials = 0
    for h in range(6, 15):
        for i in range(24):
            parents = [-1]+[rng.randrange(v) for v in range(1, h)]
            counts = [1000+rng.randrange(100) for _ in parents]
            if i % 3 == 0:
                counts[rng.randrange(h)] += (bounds(h)[0]+1)**2
            elif i % 3 == 1:
                counts[rng.randrange(h)] = 1
                counts = [n if n == 1 else n*(bounds(h)[0]+1)**2 for n in counts]
            check_case(parents, counts, trace)
            trials += 1
    check_case([-1]+[0]*7, [10**1000]+[1000]*7, trace)
    check_case([-1]+list(range(13)), [1000]*6+[10**1400]+[1000]*7, trace)
    assert trace == {"five", "light leaf", "dominant star center", "dominant vertex",
                     "two adjustable leaves"}
    print(f"{trials+2} reconstructed trees, all seed induction cases verified.")

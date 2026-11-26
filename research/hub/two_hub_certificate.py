"""Generate or verify integer gap witnesses for small cores with two marked hubs."""

import argparse
import ctypes
import gzip
import json
from pathlib import Path

from research.eight.verify import require
from research.hub.certificate import find_labels
from research.rainbow.verify import rooted_shapes


def graph_of(parents):
    graph = [[] for _ in parents]
    for i, p in enumerate(parents[1:], 1):
        graph[i].append(p)
        graph[p].append(i)
    return graph


def signature(graph, a, b):
    def code(v, parent, marked):
        children = sorted(code(w, v, marked) for w in graph[v] if w != parent)
        return ("[" if v == marked else "(") + "".join(children) + ("]" if v == marked else ")")
    return min(code(a, -1, b), code(b, -1, a))


def trimmed(graph, a, b):
    return not any(v not in (a, b) and len(ns) == 1 and ns[0] in (a, b)
                   for v, ns in enumerate(graph))


def caterpillar(graph, a, b):
    # One new leaf at each hub keeps both in the spine after deleting leaves.
    internal = {i for i, ns in enumerate(graph) if len(ns) > 1} | {a, b}
    return all(sum(w in internal for w in graph[v]) <= 2 for v in internal)


def by_marking(h):
    seen = set()
    for parents in rooted_shapes(h).values():
        graph = graph_of(parents)
        for b in range(1, h):
            if not trimmed(graph, 0, b):
                continue
            key = signature(graph, 0, b)
            if key not in seen:
                seen.add(key)
                if not caterpillar(graph, 0, b):
                    yield parents, 0, b


def by_insertion(limit):
    """Start each marked path independently; grow every side branch by leaves."""
    previous = {}
    for h in range(2, limit+1):
        path = (-1, *range(h-1))
        trees = {signature(graph_of(path), 0, h-1): (path, h-1)}
        for parents, b in previous.values():
            for p in range(h-1):
                larger = parents + (p,)
                key = signature(graph_of(larger), 0, b)
                trees.setdefault(key, (larger, b))
        required = set()
        simple = 0
        for key, (parents, b) in trees.items():
            graph = graph_of(parents)
            if trimmed(graph, 0, b):
                if caterpillar(graph, 0, b):
                    simple += 1
                else:
                    required.add(key)
        yield h, simple, required
        previous = trees


def leaf_thresholds(parents, labels):
    vertices = sorted(labels)
    weights = sorted(labels[v]+labels[p] for v, p in enumerate(parents) if v)
    gaps = list(zip(vertices, weights, vertices[1:]))
    require(all(l < w <= u for l, w, u in gaps), "invalid gap or repeated label")
    return sum(w-l-1 for l, w, _ in gaps), sum(u-w for _, w, u in gaps)


def strips(h, a, b, thresholds):
    for fixed, other, bound in ((a, b, thresholds[0]), (b, a, thresholds[1])):
        for j in range(max(0, 14-h), bound):
            yield fixed, other, j


def one_hub(parents, root):
    order = [root]
    ids = {root: 0}
    pp = [-1]
    graph = graph_of(parents)
    for v in order:
        for u in graph[v]:
            if u not in ids:
                ids[u] = len(order)
                order.append(u)
                pp.append(ids[v])
    for center in reversed(range((len(pp)-1)//2 + 1)):
        labels = find_labels(pp, center)
        if labels is not None:
            return [labels[ids[v]] for v in range(len(pp))]
    raise ValueError("no integer witness for residual one-hub core")


def generate(limit, library):
    search = ctypes.CDLL(str(library.resolve())).two_hub_seed
    vector = ctypes.POINTER(ctypes.c_int)
    search.argtypes = [ctypes.c_int]*5 + [vector, vector]
    search.restype = ctypes.c_int
    for h in range(2, limit+1):
        for parents, a, b in by_marking(h):
            output = (ctypes.c_int*h)()
            p = (ctypes.c_int*h)(*parents)
            for cap in range(14-h, 19-h):
                if any(search(h, a, b, k, cap, p, output) == 1
                       for k in range(h, h+2*cap+1)):
                    break
            else:
                raise ValueError(f"no short gap witness for {(parents, a, b)}")
            labels = list(output)
            thresholds = leaf_thresholds(parents, labels)
            extra = [[fixed, j, one_hub(parents + (fixed,)*j, other)]
                     for fixed, other, j in strips(h, a, b, thresholds)]
            print(json.dumps([parents, a, b, labels, extra], separators=(",", ":")))


def verify(limit, path):
    seen = {h: set() for h in range(2, limit+1)}
    total_strips = 0
    with gzip.open(path, "rt", encoding="ascii") as src:
        for line in src:
            p, a, b, labels, extra = json.loads(line)
            h = len(p)
            require(h in seen and p[0] == -1 and all(type(v) is int and 0 <= v < i
                    for i, v in enumerate(p) if i), "invalid parent vector")
            require(type(a) is int and type(b) is int and 0 <= a < h and 0 <= b < h
                    and a != b, "invalid marked vertices")
            require(len(labels) == h and all(type(x) is int for x in labels) and
                    labels[a] == 0 and labels[b] == 1, "invalid marked labels")
            A, B = leaf_thresholds(p, labels)
            needs = {(fixed, j): other for fixed, other, j in strips(h, a, b, (A, B))}
            for fixed, j, row in extra:
                require((fixed, j) in needs, "unexpected one-hub strip")
                root = needs.pop((fixed, j))
                aug = p + [fixed]*j
                require(len(row) == len(aug) and all(type(x) is int for x in row)
                        and row[root] == 0, "invalid one-hub labeling")
                S = set(row)
                W = {row[i]+row[v] for i, v in enumerate(aug) if i}
                require(len(S) == len(aug) and max(S)-min(S) < 18 and len(W) == len(aug)-1
                        and W <= S, "invalid one-hub interval or edge sums")
                total_strips += 1
            require(not needs, "missing residual one-hub strip")
            key = signature(graph_of(p), a, b)
            require(key not in seen[h], "duplicate two-hub case")
            seen[h].add(key)
    for h, simple, required in by_insertion(limit):
        require(seen[h] == required, f"coverage failed at order {h}")
        print(f"{h}: {simple} caterpillar families, {len(required)} interval witnesses")
    print(f"{total_strips} additional one-hub strips verified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("order", type=int, choices=range(2, 14))
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--verify", type=Path)
    action.add_argument("--library", type=Path)
    args = parser.parse_args()
    if args.verify:
        verify(args.order, args.verify)
    else:
        generate(args.order, args.library)

"""Check marked leaves and shortened matching/star expansions on their actual edges."""

from argparse import ArgumentParser
from collections import Counter
from random import Random

from research.matching_expansion import matching_labels, star_labels
from .generate import native_search
from .marked_branches import label


def tree(left, gap, right):
    parent = [-1]

    def append_path(start, length):
        for _ in range(length):
            parent.append(start)
            start = len(parent)-1
        return start

    second = append_path(0, gap)
    for v, arms in ((0, left), (second, right)):
        for length in arms:
            append_path(v, length)
    return parent


def check_histograms(labels, edges, k, mark=None):
    vertex = [0]*k
    edge = [0]*k
    for x in labels.values():
        assert 0 <= x < k
        vertex[x] += 1
    for u, v in edges:
        edge[(labels[u]+labels[v]) % k] += 1
    assert sum(edge)+1 == sum(vertex)
    assert max(vertex)-min(vertex) <= 1 and max(edge)-min(edge) <= 1
    if mark is not None:
        assert vertex[labels[mark]] == max(vertex)


def expansions(parent, digits, mark, m, rng):
    sizes = [2, rng.randrange(3, 10)]
    for size in sizes:
        joins = []
        for _ in parent[1:]:
            if size == 2:
                joins.append((rng.randrange(2), rng.randrange(2)))
            elif rng.randrange(2):
                joins.append((rng.randrange(1, size), rng.randrange(1, size)))
            else:
                joins.append((0, 0))
        if size == 2:
            full = matching_labels(parent, digits, joins, m)
        else:
            full = star_labels(parent, digits, joins, m, size)
        edges = [(i*size, i*size+j) for i in range(len(parent)) for j in range(1, size)]
        bridges = [(parent[i]*size+a, i*size+b) for i, (a, b) in enumerate(joins, 1)]
        ports = {v for e in bridges for v in e}
        removable = [mark*size+j for j in range(size) if mark*size+j not in ports
                     and (size == 2 or j != 0)]
        rng.shuffle(removable)
        labels = dict(enumerate(full))
        edges.extend(bridges)
        check_histograms(labels, edges, size*m)
        yield 1
        for v in removable:
            del labels[v]
            edges = [e for e in edges if v not in e]
            check_histograms(labels, edges, size*m)
            yield 1


def check(library, k, trials=48):
    rng = Random(199104+k)
    witness = native_search(library, k)
    steps = Counter()
    expanded = cases = 0
    for i in range(trials):
        # The long connector forces a divisible cut away from either marked end.
        if k <= 39 and i % 4 == 0:
            parent = tree([1, 2], 2*k+2, [1, 3])
        elif k <= 39 and i % 4 == 1:
            arms = lambda: [rng.randint(1, k//2+1) for _ in range(rng.randint(2, 5))]
            parent = tree(arms(), rng.randint(1, 2*k), arms())
        else:
            parent = tree([rng.randint(1, k+1) for _ in range(rng.randint(1, 8))], 0, [])
        edges = list(zip(parent[1:], range(1, len(parent))))
        graph = {v: [] for v in range(len(parent))}
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        leaves = [v for v in graph if len(graph[v]) == 1]
        for mark in rng.sample(leaves, min(2, len(leaves))):
            f = label(graph, mark, k, witness, steps)
            assert f.keys() == graph.keys()
            check_histograms(f, edges, k, mark)
            cases += 1
            if k % 2:
                expanded += sum(expansions(parent, [f[v] for v in graph], mark, k, rng))
    return cases, expanded, steps


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("library")
    parser.add_argument("moduli", type=int, nargs="+")
    args = parser.parse_args()
    total = Counter()
    for k in args.moduli:
        marked, expanded, steps = check(args.library, k)
        total.update(steps)
        total["marked trees"] += marked
        total["expanded trees"] += expanded
    print(dict(sorted(total.items())))

"""Expand a small certificate on 28-vertex caterpillars and count all 50 vertices."""
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from struct import iter_unpack

from research.rainbow.check_short_forests import colorings
from .check_typed_leaf_streams import records


def core(run):
    # Along this staircase each edge adds a new vertex and increases its sum by one.
    i = j = 0
    edges = [(0, 13)]
    for move in 'H'*run + 'V'*run + 'HV'*(12-run) + 'V':
        i += move == 'H'
        j += move == 'V'
        edges.append((i, 13+j))
    labels = list(range(27))
    weights = {(v+w) % 27 for v,w in edges}
    assert len(weights) == 26
    hole, = set(range(27)) - weights
    degrees = Counter(x for pair in edges for x in pair)
    parent = next(v for v in labels if degrees[v] > 1)
    surplus = (hole - labels[parent]) % 27
    edges.append((parent, 27))
    labels.append(surplus)
    labels = [(x-surplus) % 27 for x in labels]
    assert Counter(labels) == Counter(range(27)) + Counter([0])
    assert {(labels[v]+labels[w]) % 27 for v,w in edges} == set(range(27))
    return labels, edges


def check(path):
    cores = [core(r) for r in (4,5,6)]
    leaves = Counter()
    shapes = 0
    for _, _, payload, (parents, roots, sizes, _) in records(path):
        assert len(parents) == 22
        options = []
        for row in iter_unpack('22B', payload):
            assert len(set(row)) == 22 and all(0 < x < 27 for x in row)
            for u in range(1,27):
                if u % 3:
                    labels = tuple(u*x % 27 for x in row)
                    inside = {(labels[v]+labels[w]) % 27 for v,w in enumerate(parents) if w >= 0}
                    assert len(inside) == 22-len(roots)
                    options.append((labels, inside))
        for boundary in colorings(27,sizes):
            for labels, inside in options:
                entering = {(labels[v]+b) % 27 for v,b in zip(roots,boundary)}
                if len(inside | entering) == 22:
                    break
            else:
                raise AssertionError(('uncovered boundary', boundary))
            for old, edges in cores:
                ports = {v:old.index(b) for v,b in zip(roots,boundary)}
                joined = edges + [(ports[v] if w < 0 else 28+w, 28+v)
                                  for v,w in enumerate(parents)]
                coloring = old + list(labels)
                assert len(coloring) == 50 and len(joined) == 49
                vertex = Counter(coloring)
                edge = Counter((coloring[a]+coloring[b]) % 27 for a,b in joined)
                for histogram in (vertex,edge):
                    bins = [histogram[x] for x in range(27)]
                    assert max(bins)-min(bins) <= 1
                degree = Counter(x for pair in joined for x in pair)
                leaves[sum(n==1 for n in degree.values())] += 1
        shapes += 1
    assert shapes > 0
    print('sampled rooted forests', shapes, 'order-50 joins', sum(leaves.values()),
          'by leaf count', dict(sorted(leaves.items())))


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('stream', type=Path)
    check(parser.parse_args().stream)

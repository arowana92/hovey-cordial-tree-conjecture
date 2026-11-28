"""Expand a small certificate on 28-vertex caterpillars and count all vertices and weights."""
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from struct import iter_unpack

from research.rainbow.check_short_forests import colorings
from .check_typed_leaf_streams import records
from .check_marked_ring import matching_check


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


def check(path, order=50, limit=None, lift_leaves=None):
    if lift_leaves is None:
        lift_leaves = {53:15,54:14}.get(order)
    mass = order-28
    runs = (2,3,4) if order>=53 else (4,5,6)
    cores = [core(r) for r in runs]
    leaves = Counter()
    shapes = matches = 0
    for _, _, payload, (parents, roots, sizes, _) in records(path):
        if limit is not None and shapes>=limit:
            break
        assert len(parents) == mass
        options = []
        for row in iter_unpack(f'{mass}B', payload):
            assert len(set(row)) == mass and all(0 < x < 27 for x in row)
            for u in range(1,27):
                if u % 3:
                    labels = tuple(u*x % 27 for x in row)
                    inside = {(labels[v]+labels[w]) % 27 for v,w in enumerate(parents) if w >= 0}
                    assert len(inside) == mass-len(roots)
                    options.append((labels, inside))
        for boundary in colorings(27,sizes):
            for labels, inside in options:
                entering = {(labels[v]+b) % 27 for v,b in zip(roots,boundary)}
                if len(inside | entering) == mass:
                    break
            else:
                raise AssertionError(('uncovered boundary', boundary))
            for old, edges in cores:
                ports = {v:old.index(b) for v,b in zip(roots,boundary)}
                joined = edges + [(ports[v] if w < 0 else 28+w, 28+v)
                                  for v,w in enumerate(parents)]
                coloring = old + list(labels)
                assert len(coloring) == order and len(joined) == order-1
                vertex = Counter(coloring)
                edge = Counter((coloring[a]+coloring[b]) % 27 for a,b in joined)
                for histogram in (vertex,edge):
                    bins = [histogram[x] for x in range(27)]
                    assert max(bins)-min(bins) <= 1
                if order>=52:
                    vertex_bins = [old.count(c) for c in range(27)]
                    edge_bins = [1]*27
                    for u,v in joined[len(edges):]:
                        assert u<v
                        vertex_bins[coloring[v]] += 1
                        edge_bins[(coloring[u]+coloring[v])%27] += 1
                        for bins in (vertex_bins,edge_bins):
                            assert max(bins)-min(bins)<=1
                degree = Counter(x for pair in joined for x in pair)
                leaf_count = sum(n==1 for n in degree.values())
                leaves[leaf_count] += 1
                if order>=53 and leaf_count==lift_leaves and matches<24:
                    mark = next(v for v,d in degree.items()
                                if d==1 and vertex[coloring[v]]==max(vertex.values()))
                    matching_check(coloring,joined,mark)
                    matches += 1
        shapes += 1
    assert shapes > 0
    print('sampled rooted forests', shapes, f'order-{order} joins', sum(leaves.values()),
          'by leaf count', dict(sorted(leaves.items())))
    if order>=53:
        print('perfect and near-perfect matching lifts at 54 labels',matches, 'each')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('stream', type=Path)
    parser.add_argument('--order', type=int, choices=range(50,55), default=50)
    parser.add_argument('--sample',type=int,help='maximum number of rooted forests to expand')
    parser.add_argument('--lift-leaves',type=int,help='leaf count of the quotient trees to lift at orders 53 and 54')
    args = parser.parse_args()
    check(args.stream,args.order,args.sample,args.lift_leaves)

"""Reconstruct stretched cores, all induction cases, and completed tree labelings."""

from random import Random

from .many_leaf_parents import verify
from .marked_leaf_blocks import insertion
from .marked_leaf_construct import adjustable_seed, construct, dominant_seed, finish
from .marked_leaf_geometry import geometry_seed, records
from .marked_leaf_verify import expanded
from .two_hubs import edge


def graph_of(edges):
    graph = {}
    for u, v in edges:
        graph.setdefault(u, set()).add(v)
        graph.setdefault(v, set()).add(u)
    return graph


def check_seed(graph, marked, seed):
    tree, labels, anchors = seed
    assert set(labels) == set(graph) and len(set(labels.values())) == len(graph)
    marked_labels = {labels[v] for v in marked}
    required = {edge(labels[u], labels[v]) for u in graph for v in graph[u]}
    fillers = {edge(p, v) for p, v in tree.added}
    assert set(anchors) <= marked_labels
    assert len(fillers) == len(tree.added) and all(p in marked_labels for p, v in tree.added)
    assert required.isdisjoint(fillers) and tree.edges == required | fillers
    vertices = list(labels.values()) + [v for _, v in tree.added]
    assert sorted(vertices) == list(range(tree.lo, tree.hi+1))
    assert sorted(u+v for u, v in tree.edges) == list(range(tree.lo+1, tree.hi+1))


def check_insertions():
    n = 0
    for anchors in [(-1, 0, 2)] + [(-a, 0, 1, b) for a in range(1, 6) for b in range(2, 7)]:
        for p in range(-40, 41):
            for side in (0, 1):
                parents, slot = insertion(anchors, p, side)
                assert parents[slot] == p
                assert all(q in anchors for i, q in enumerate(parents) if i != slot)
                assert sorted(q+i-side for i, q in enumerate(parents)) == list(range(len(parents)))
                n += 1
    return n


def check_geometries():
    n = 0
    for m, skeleton, mask in records():
        edges = list(expanded(skeleton, mask))
        # Stretch one real edge by four and grow an unmarked side path.
        i = (mask+sum(u for u, v in edges)) % len(edges)
        u, v = edges.pop(i)
        h = len(edges)+2
        path = [u]+list(range(h, h+4))+[v]
        edges.extend(zip(path, path[1:]))
        edges.extend([(h+1, h+4), (h+4, h+5)])
        graph = graph_of(edges)
        marks = list(range(m))
        counts = {v: (5-v)**3 for v in marks}
        seed = geometry_seed(graph, marks, counts)
        check_seed(graph, marks, seed)
        if m == 4:
            moment = sum(counts[v]*seed[1][v] for v in marks)
            assert min(moment, sum(counts.values())-moment) >= min(counts.values())
        n += 1
    return n


def check_final(graph, counts, seed, blocks, expand=False):
    order = [min(graph)]
    parent = {order[0]: None}
    for u in order:
        for v in sorted(graph[u]):
            if v not in parent:
                parent[v] = u
                order.append(v)
    index = {v: i for i, v in enumerate(order)}
    parents = [-1]+[index[parent[v]] for v in order[1:]]
    tree, labels, _ = seed
    verify(parents, [counts.get(v, 0) for v in order], tree,
           {index[v]: p for v, p in labels.items()}, blocks, expand=expand)


def check_populations():
    rng = Random(1618033)
    trials = 0
    for h in range(6, 13):
        for i in range(6):
            graph = graph_of([(v, rng.randrange(v)) for v in range(1, h)])
            sites = set(rng.sample(range(h), min(h, 5+i%3)))
            counts = {v: rng.randrange(10, 30) for v in sites}
            for method in (adjustable_seed, dominant_seed):
                if method is dominant_seed:
                    counts[min(sites)] = 10**80
                seed = method(graph, sites, counts, 10**6)
                assert seed is not None
                check_seed(graph, sites, seed)
                moment = sum(counts[v]*seed[1][v] for v in sites)
                mass = sum(counts.values())
                rest = mass-max(counts.values())
                slack = min(moment, mass-moment)
                if method is adjustable_seed:
                    assert 4*slack >= mass
                else:
                    assert slack >= rest
                scaled = {v: n*10**30 for v, n in counts.items()}
                blocks = finish(seed, scaled)
                check_final(graph, scaled, seed, blocks)
                trials += 1
            ranked = sorted(sites)
            for j in (0, 1, 2):
                populations = {v: 10**30 for v in ranked}
                for k in range(j+1):
                    populations[ranked[k]] += (4-k)*10**105
                result = construct(graph, populations, coordinate_limit=5000)
                assert result is not None
                seed, blocks = result
                check_final(graph, populations, seed, blocks)
                trials += 1

    graph = graph_of([(0, 3), (3, 1), (1, 4), (1, 2)])
    populations = {0: 50000, 1: 40000, 2: 30000}
    seed, blocks = construct(graph, populations)
    check_final(graph, populations, seed, blocks, expand=True)
    return trials+1


if __name__ == "__main__":
    print(f"{check_insertions()} insertion permutations, {check_geometries()} stretched geometries, "
          f"{check_populations()} completed tree profiles verified.")

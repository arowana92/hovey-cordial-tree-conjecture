"""Recount original edges and labels independently of the caterpillar decomposition."""

from random import Random

from .surplus_caterpillar import attach


def shape(counts):
    spine = list(range(len(counts)))
    leaves = {}
    edges = list(zip(spine, spine[1:]))
    n = len(spine)
    for u, count in enumerate(counts):
        leaves[u] = list(range(n, n+count))
        edges.extend((u, v) for v in leaves[u])
        n += count
    return spine, leaves, edges, n


def histogram(values, k):
    bins = [0]*k
    for x in values:
        assert 0 <= x < k
        bins[x] += 1
    return bins


def verify(data, mark, parent, k, special, surplus):
    spine, leaves, edges, n = data
    labels = attach(spine, leaves, mark, parent, special, k, surplus=surplus)
    assert set(labels) == set(range(n))
    vertices = histogram(labels.values(), k)
    weights = histogram(((labels[u]+labels[v]) % k for u, v in edges), k)
    weights[(parent+labels[mark]) % k] += 1
    if surplus:
        vertices[special] += 1
    else:
        weights[special] -= 1
    for bins in (vertices, weights):
        assert max(bins)-min(bins) <= 1, (data, mark, parent, special, surplus, k, bins)
    return labels


def compositions(n):
    if n == 0:
        yield []
    for first in range(1, n+1):
        for tail in compositions(n-first):
            yield [first-1] + tail


def exhaustive():
    total = 0
    for n in range(1, 10):
        for counts in compositions(n):
            data = shape(counts)
            for k in {max(2, n//2), n+1}:
                for mark in range(n):
                    for parent in range(k):
                        for surplus in (False, True):
                            verify(data, mark, parent, k, 0, surplus)
                            total += 1
    return total


def special_cases():
    total = 0
    for k in range(2, 49):
        # Two arms of k-1 with a marked central leaf. Also large central
        # stars and arms that cut through a group of siblings on either side.
        for a, b, middle in [(k-1, k-1, 1), (k-1, k-1, 2),
                             (2*k-1, 3*k-1, 2*k+3), (3*k+1, k+2, 2)]:
            data = shape([a-1, middle, b-1])
            mark = data[1][1][0]
            for parent in range(k):
                for surplus in (False, True):
                    verify(data, mark, parent, k, (3*parent+1) % k, surplus)
                    total += 1
    return total


def whole_trees():
    rng = Random(8101991)
    for _ in range(3000):
        k = rng.randint(1, 100)
        surplus = bool(rng.randrange(2))
        order = k*rng.randint(1, 4)+int(surplus)
        shift = rng.randrange(k)
        core = [(shift+i//2+(i%2)*((order+1)//2)) % k for i in range(order)]
        site = rng.randrange(order)
        offset = rng.randrange(k)
        core_edges = [(core[i-1]+core[i]) % k for i in range(1, order)]
        bins = histogram(core if surplus else core_edges, k)
        special = bins.index(max(bins) if surplus else min(bins))
        counts = [rng.randrange(1+k//3) for _ in range(rng.randint(1, 25))]
        data = shape(counts)
        mark = rng.randrange(data[3])
        labels = verify(data, mark, (core[site]+offset) % k, k, special, surplus)
        all_weights = core_edges + [(labels[u]+labels[v]) % k for u, v in data[2]]
        all_weights.append((core[site]+offset+labels[mark]) % k)
        for items in (core+list(labels.values()), all_weights):
            bins = histogram(items, k)
            assert max(bins)-min(bins) <= 1
    return 3000


if __name__ == "__main__":
    print(f"{exhaustive()} exhaustive marked extensions through order nine", flush=True)
    print(f"{special_cases()} two-arm boundary cases", flush=True)
    print(f"{whole_trees()} whole trees with translated cores and bridge offsets")

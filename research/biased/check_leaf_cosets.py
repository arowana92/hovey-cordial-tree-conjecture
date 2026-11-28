"""Independent palette enumeration and actual-edge verification."""
from functools import lru_cache, reduce
from itertools import combinations, product
from math import gcd
from random import Random

from .leaf_cosets import choose_labels, fixed_core, uniform_forest


def recount(k, parents, boundaries, populations, labels, tables):
    vertices, weights = [0]*k, [0]*k
    for v, p in enumerate(parents):
        vertices[labels[v] % k] += 1
        if p >= 0 or v in boundaries:
            a = labels[p] if p >= 0 else boundaries[v]
            weights[(a+labels[v]) % k] += 1
        row = tables.get(v, [])
        assert sum(row) == populations[v] and all(x >= 0 for x in row)
        for z, count in enumerate(row):
            vertices[z] += count
            weights[(labels[v]+z) % k] += count
    assert max(vertices)-min(vertices) <= 1 and max(weights)-min(weights) <= 1
    if boundaries:
        assert vertices == weights and len(set(vertices)) == 1


@lru_cache(None)
def palette_differences(k, index, extra):
    def quotient_vectors(size):
        rows = set()
        for subset in combinations(range(k), size):
            bins = [0]*index
            for z in subset:
                bins[z % index] += 1
            rows.add(tuple(bins))
        return rows
    return {tuple(x-y for x, y in zip(a, b))
            for a in quotient_vectors(extra+1) for b in quotient_vectors(extra)}


def possible_palettes(k, parents, labels, sizes):
    sites = [v for v, n in enumerate(sizes) if n]
    base = labels[sites[0]]
    d = reduce(gcd, (labels[v]-base for v in sites), k)
    delta = [0]*d
    for v, p in enumerate(parents):
        delta[labels[v] % d] += 1
        if p >= 0:
            delta[(labels[p]+labels[v]-base) % d] -= 1
    return tuple(delta) in palette_differences(k, d, (len(parents)+sum(sizes)-1) % k)


def literal_two_sites(k, parents, labels, sizes):
    # Enumerate the final vertex histogram, then every possible allocation to site 0.
    n = len(parents)+sum(sizes)
    low, extra = divmod(n, k)
    for subset in combinations(range(k), extra):
        demand = [low+(z in subset)-labels.count(z) for z in range(k)]
        for prefix in product(*(range(min(sizes[0], a)+1) for a in demand[:-1])):
            last = sizes[0]-sum(prefix)
            if not 0 <= last <= demand[-1]:
                continue
            left = list(prefix) + [last]
            edges = [0]*k
            for v, p in enumerate(parents):
                if p >= 0:
                    edges[(labels[p]+labels[v]) % k] += 1
            for z, a in enumerate(left):
                edges[(labels[0]+z) % k] += a
                edges[(labels[1]+z) % k] += demand[z]-a
            if max(edges)-min(edges) <= 1:
                return True
    return False


def main():
    rng = Random(917052)
    yes = no = 0
    for k in range(1, 13):
        for _ in range(380):
            r = rng.randrange(2, 12)
            parents = [-1] + [rng.randrange(i) for i in range(1, r)]
            labels = [rng.randrange(k) for _ in parents]
            sizes = [0]*r
            for v in rng.sample(range(r), rng.randint(1, r)):
                sizes[v] = 4*k*r+rng.randrange(2*k+1)
            result = fixed_core(k, parents, labels, sizes)
            assert (result is not None) == possible_palettes(k, parents, labels, sizes)
            if result is None:
                no += 1
            else:
                recount(k, parents, {}, sizes, labels, result)
                yes += 1
    print(f"Independent balanced-palette enumeration: {yes} completions, {no} exclusions")

    literal = misses = 0
    for k in (2, 3):
        parents = [-1, 0, 1, 2]
        for labels in product(range(k), repeat=4):
            for residue in range(k):
                sizes = [16*k, 16*k+residue, 0, 0]
                result = fixed_core(k, parents, labels, sizes)
                exact = literal_two_sites(k, parents, list(labels), sizes)
                assert exact == (result is not None)
                literal += 1
                misses += not exact
    print(f"Literal two-site leaf allocations: {literal} decisions, {misses} exclusions")

    yes = no = 0
    for k in list(range(1, 43)) + [60, 72, 105, 210]:
        for _ in range(100):
            r = rng.randrange(3, 11)
            parents = [-1] + [rng.randrange(-1, i) for i in range(1, r)]
            boundaries = {v: rng.randrange(k) for v, p in enumerate(parents) if p < 0}
            sites = rng.sample(range(r), rng.randint(3, r))
            sizes = [0]*r
            for v in sites:
                sizes[v] = k*(3*r+rng.randrange(20)) + rng.randrange(k)
            sizes[sites[-1]] += (-r-sum(sizes)) % k
            pins = {v: rng.randrange(k) for v in range(r)
                    if v not in sites[:2] and rng.randrange(3)}
            coeff = [parents.count(v)+sizes[v] for v in range(r)]
            d = reduce(gcd, (a for v, a in enumerate(coeff) if v not in pins), k)
            good = (sum(boundaries.values())+sum(coeff[v]*z for v, z in pins.items())) % d == 0
            result = uniform_forest(k, parents, boundaries, sizes, pins)
            assert good == (result is not None)
            if good:
                labels, tables = result
                assert all(labels[v] == z for v, z in pins.items())
                recount(k, parents, boundaries, sizes, labels, tables)
                yes += 1
            else:
                no += 1
    print(f"Uniform forests on actual edges: {yes} completions, {no} gcd exclusions")

    linear = 0
    for k in range(1, 7):
        for a, b, c, target in product(range(k), repeat=4):
            pins = {2: (a+c) % k}
            expected = any((a*x+b*y+c*pins[2]+target) % k == 0 and
                           gcd(k, x-pins[2], y-pins[2]) == 1
                           for x, y in product(range(k), repeat=2))
            assignment = choose_labels(k, [a, b, c], target, [0, 1, 2], pins)
            assert (assignment is not None) == expected
            linear += 1
    print(f"Exhaustive simultaneous moment and generation decisions: {linear}")


if __name__ == "__main__":
    main()

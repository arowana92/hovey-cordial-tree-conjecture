"""Compare exact one-site projections to direct labelings, including failed pinned cases."""

from collections import Counter
from itertools import permutations, product
import islpy as isl

from .core_spectra import capacity, interval_holes, modular_holes


def admissible(hist, k):
    values = [hist[r] for r in range(k)]
    return max(values)-min(values) <= 1


def test_capacities():
    n = 0
    parents = (-1, 0, 1, 1)
    for k in (2, 3, 4):
        for tail in product(range(k), repeat=3):
            f = (0,)+tail
            vertices = Counter(f)
            edges = Counter((f[v]+f[p]) % k for v, p in enumerate(parents) if v)
            for leaves in range(6):
                qv, qe = (4+leaves)//k, (3+leaves)//k
                limits = [capacity(vertices[i], edges[i], qv, qe) for i in range(k)]
                expected = (all(lo <= hi for lo, hi in limits)
                            and sum(lo for lo, hi in limits) <= leaves <= sum(hi for lo, hi in limits))
                observed = False
                for extra in product(range(k), repeat=leaves):
                    counts = Counter(extra)
                    if admissible(vertices+counts, k) and admissible(edges+counts, k):
                        observed = True
                        break
                assert observed == expected
                n += 1
    return n


def points_modular(parents, pins, k, leaves):
    full = tuple(parents)+(0,)*leaves
    labels = [0]*len(full)
    fixed = dict([(0, 0), *pins])
    if max(fixed.values()) >= k:
        return False
    for v, x in fixed.items():
        labels[v] = x
    free = [v for v in range(len(full)) if v not in fixed]
    for xs in product(range(k), repeat=len(free)):
        for v, x in zip(free, xs):
            labels[v] = x
        if admissible(Counter(labels), k):
            weights = Counter((labels[v]+labels[p]) % k for v, p in enumerate(full) if v)
            if admissible(weights, k):
                return True
    return False


def points_interval(parents, pins, leaves):
    full = tuple(parents)+(0,)*leaves
    n = len(full)
    for f in permutations(range(n)):
        sums = [f[v]+f[p] for v, p in enumerate(full) if v]
        if len(set(sums)) == n-1 and max(sums)-min(sums) == n-2:
            shift = 1-min(sums)
            if all(f[v]+shift == value for v, value in pins):
                return True
    return False


def test_projections():
    path = (-1, 0, 1, 2)
    diagonal = isl.Set("{ [k,m] : k=m+4 }")
    even = isl.Set("{ [k,m] : k=m+4 and k >= 4 and k mod 2 = 0 }")
    assert modular_holes(path, [(1, 1)], diagonal).is_equal(even)
    star = (-1, 0, 1, 1, 1)
    mod_six = isl.Set("{ [m] : m >= 0 and m mod 6 = 3 }")
    assert interval_holes(star, [(0, 2)]).is_equal(mod_six)
    n = 0
    for parents in ((-1, 0), (-1, 0, 1), (-1, 0, 0), path, (-1, 0, 1, 0)):
        h = len(parents)
        for pins in ([], [(1, 1)], [(1, 0)]):
            holes = modular_holes(parents, pins)
            for k in range(2, 5):
                for m in range(4):
                    if h+m > (h-1)*k:
                        continue
                    point = isl.Set(f"{{ [k,m] : k={k} and m={m} }}")
                    assert holes.intersect(point).is_empty() == points_modular(parents, pins, k, m)
                    n += 1
    for parents in ((-1, 0), path, star):
        for pins in ([], [(0, 2)], [(0, 0), (1, -1)]):
            holes = interval_holes(parents, pins)
            for m in range(4):
                point = isl.Set(f"{{ [m] : m={m} }}")
                assert holes.intersect(point).is_empty() == points_interval(parents, pins, m)
                n += 1
    return n


if __name__ == "__main__":
    print(f"{test_capacities()} fixed-core histogram tests, {test_projections()} direct projected "
          "membership tests, and two exact infinite spectra verified.")

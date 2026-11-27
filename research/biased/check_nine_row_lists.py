"""Prove the nine-row list bound and compare two exact forest expansions."""

from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from itertools import permutations
from math import gcd

from research.eight.generate import forests, parent_vector
from research.eight.verify import components
from research.rainbow.verify import rooted_shapes
from .forest_exterior import exterior_evaluator
from .forest_grid import forest_coefficient
from .forest_subsets import coefficient_table


def signature(parents):
    return tuple(sorted(code for _, code in components(parents)))


def catalog(r):
    cases = []
    for forest in forests(r):
        parents = tuple(parent_vector(forest, (0,)*len(forest)))
        cases.append((forest, parents, signature(parents)))
    grown = {}
    for parents in rooted_shapes(r+1).values():
        row = tuple(p-1 for p in parents[1:])
        grown[signature(row)] = row
    assert len(grown) == len(cases) == len({code for _, _, code in cases})
    assert set(grown) == {code for _, _, code in cases}
    return cases, grown


def table(cases, grown, e, prime, independent):
    r = len(cases[0][1])
    evaluate = coefficient_table(r, e, prime)
    values = [evaluate(forest) for forest, _, _ in cases]
    if independent:
        forward = exterior_evaluator(r, e, prime)
        assert all(forward(grown[code]) == v for (_, _, code), v in zip(cases, values))
    return values


def main(independent=True):
    for r in range(1,6):
        cases, _ = catalog(r)
        for e in (0,2):
            forward = exterior_evaluator(r, e)
            backward = coefficient_table(r, e)
            for forest, parents, _ in cases:
                assert forward(parents) == backward(forest) == forest_coefficient(parents, e)

    cases, grown = catalog(9)
    assert len(cases) == 719
    first, second = (table(cases, grown, Fraction(z,2), None, independent) for z in (-11,-9))
    common = [gcd(a.numerator,b.numerator) for a,b in zip(first,second)]
    assert 0 not in common
    primes = set()
    for value in common:
        divisor = 2
        while divisor*divisor <= value:
            while value % divisor == 0:
                primes.add(divisor)
                value //= divisor
            divisor += 1
        if value > 1:
            primes.add(value)
    exceptions = {p:[i for i,g in enumerate(common) if g % p == 0] for p in primes if p > 20}
    assert {p: len(rows) for p,rows in exceptions.items()} == {23:1,29:1,31:1}
    print("719 half-integer coefficient pairs checked. Exceptional primes above 20 are 23, 29, 31.", flush=True)

    # Small prime characteristics can divide a transfer factorial, so use
    # the actual nonnegative forbidden sizes for every forest.
    for p in (11,13,17,19):
        e = (p-11)//2
        a,b = (table(cases, grown, h, p, independent) for h in (e,e+1))
        exceptions[p] = [i for i,(x,y) in enumerate(zip(a,b)) if not (x or y)]
    counts = Counter()
    for p, rows in sorted(exceptions.items()):
        e = (p-11)//2
        backward = coefficient_table(9,e,p)
        forward = exterior_evaluator(9,e,p)
        for i in rows:
            forest, parents, _ = cases[i]
            for high, low in permutations(range(9),2):
                shifts = [0]*9
                shifts[high], shifts[low] = 1,-1
                value = forward(parents, shifts)
                assert value == backward(forest, shifts)
                if value:
                    counts[p] += 1
                    break
            else:
                raise AssertionError((p,parents))
    assert dict(counts) == {11:9, 13:2, 17:1, 23:1, 29:1, 31:1}
    print("All 15 exceptional forest/prime pairs verified with shifted exponents.", flush=True)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--single-expansion", action="store_true",
                        help="skip the second full table calculation")
    main(not parser.parse_args().single_expansion)

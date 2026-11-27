"""Verify integer polynomial certificates for one spare choice in each leaf list."""

from collections import defaultdict
from functools import lru_cache
from itertools import combinations, permutations
import json
from math import factorial
from operator import itemgetter
from pathlib import Path
from random import Random

from .check_spare_lists import verify_choice


def reduced(terms):
    least = tuple(map(min,zip(*terms)))
    return {tuple(x-y for x,y in zip(exponent,least)): n for exponent,n in terms.items()}


def check_orbits(r, record):
    """Use the signed determinant and keep the sum of coefficients on each orbit."""
    perms = list(permutations(range(r)))
    signs = {p:(-1)**sum(i>j for i,j in combinations(p,2)) for p in perms}

    @lru_cache(None)
    def coefficient(b):
        terms = {}
        for p in perms:
            q = tuple(i-j for i,j in zip(b,p))
            if q in signs:
                terms[p] = signs[p]*signs[q]
        return reduced(terms)

    sums = defaultdict(int)
    for b,shift,factor in record["terms"]:
        assert len(b) == len(shift) == r and min(b) >= 0 and max(b) <= r
        assert sum(b) == r*(r-1) and min(shift) >= 0
        for p,value in coefficient(tuple(b)).items():
            exponent = tuple(sorted(i+j for i,j in zip(p,shift)))
            sums[exponent] += factor*value
    target = (record["power"],)*r
    assert {exp:v for exp,v in sums.items() if v} == {target:record["scale"]}


def vandermonde(r):
    terms = {(0,)*r:1}
    for i,j in combinations(range(r),2):
        product = defaultdict(int)
        for exponent,c in terms.items():
            for v,sign in ((j,1),(i,-1)):
                increased = list(exponent)
                increased[v] += 1
                product[tuple(increased)] += sign*c
        terms = {key:c for key,c in product.items() if c}
    return terms


def check_expansion(r, record):
    """Multiply the linear factors, then expand every variable permutation."""
    delta = vandermonde(r)
    pieces = defaultdict(int)
    for b,shift,factor in record["terms"]:
        raw = {}
        for q,c in delta.items():
            p = tuple(x-y for x,y in zip(b,q))
            if p in delta:
                raw[p] = c*delta[p]
        for exp,c in reduced(raw).items():
            power = tuple(x+y for x,y in zip(exp,shift))
            pieces[power] += factor*c
    unsymmetrized = [(p,c) for p,c in pieces.items() if c]
    full = defaultdict(int)
    for order in permutations(range(r)):
        permute = itemgetter(*order)
        for power,c in unsymmetrized:
            full[permute(power)] += c
    assert {p:c for p,c in full.items() if c} == {
        (record["power"],)*r:factorial(r)*record["scale"]}


def main():
    data = json.loads(Path(__file__).with_name("spare-leaf-identities.json").read_text())
    assert set(data) == set(map(str,range(2,7)))
    random = Random(1991)
    instances = 0
    for text,record in data.items():
        r = int(text)
        assert record["scale"] > 0 and record["power"] >= 0
        check_orbits(r,record)
        check_expansion(r,record)
        for k in range(r+1,41):
            for _ in range(20):
                shifts = [random.randrange(k) for _ in range(r)]
                lists = [tuple(random.sample(range(k),r+1)) for _ in range(r)]
                verify_choice(k,shifts,lists)
                instances += 1
        print(f"{r} rows: {len(record['terms'])} certificate terms passed both exact expansions",flush=True)
    print(f"{instances} separate-list cyclic assignments checked",flush=True)


if __name__ == "__main__":
    main()

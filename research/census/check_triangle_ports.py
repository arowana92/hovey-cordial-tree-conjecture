"""Rebuild the triangle counts by edge inclusion-exclusion and gcds of minors."""

from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations
from math import gcd, prod

from .square_ports import signatures


@lru_cache(40000)
def det(matrix):
    if not matrix:
        return 1
    return sum((-1)**j * x * det(tuple(row[:j]+row[j+1:] for row in matrix[1:]))
               for j,x in enumerate(matrix[0]) if x)


@lru_cache(None)
def invariant(matrix):
    width = len(matrix[0])
    last = 1
    factors = []
    for size in range(1,min(len(matrix),width)+1):
        divisor = 0
        for rows in combinations(matrix,size):
            for cols in combinations(range(width),size):
                minor = tuple(tuple(row[j] for j in cols) for row in rows)
                divisor = gcd(divisor,det(minor))
                if divisor == last:
                    break
            if divisor == last:
                break
        if not divisor:
            break
        factors.append(divisor//last)
        last = divisor
    return width-len(factors),tuple(d for d in factors if d>1)


def canonical(sig):
    free, factors = sig
    d = 1
    result = []
    for size in range(1,len(factors)+1):
        new = gcd(*(prod(subset) for subset in combinations(factors,size)))
        result.append(new//d)
        d = new
    return free,tuple(x for x in result if x>1)


def verify(graph, port):
    actual = graph[:]
    target = [(i,) for i in range(4)]
    if port is not None:
        u,v = actual.pop(port)
        actual.extend([(u,4),(v,5)])
        target.append((4,5))
    total = Counter()
    pairs = tuple(combinations(range(4),2))
    for mask in range(64):
        blocks = list(range(4))
        for j,(u,v) in enumerate(pairs):
            if mask & (1<<j):
                a,b = blocks[u],blocks[v]
                blocks = [a if x==b else x for x in blocks]
        names = sorted(set(blocks)-{blocks[0]})
        positions = [-1 if x==blocks[0] else names.index(x) for x in blocks]
        if port is not None:
            positions += [len(names),len(names)+1]
        width = max(positions)+1
        for image in permutations(target):
            equations = []
            for source,dest in zip(actual,image):
                row = [0]*width
                for sign,entries in [(1,source),(-1,dest)]:
                    for v in entries:
                        index = positions[v]
                        if index>=0:
                            row[index] += sign
                equations.append(tuple(row))
            matrix = tuple(equations)
            augmented = matrix if port is None else matrix+(tuple([0]*len(names)+[1,-1]),)
            total[invariant(matrix),invariant(augmented)] += (-1)**bin(mask).count("1")
    expected = Counter()
    for (source,fixed),mult in signatures(graph,port).items():
        expected[canonical(source),canonical(fixed)] += mult
    assert {k:v for k,v in total.items() if v} == {k:v for k,v in expected.items() if v}


if __name__ == "__main__":
    graph = [(0,1),(1,2),(2,3),(3,1)]
    for port in (None,1,2):
        verify(graph,port)
    print("all three integer-matrix inventories agree")

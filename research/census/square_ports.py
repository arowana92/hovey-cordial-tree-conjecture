"""Compute port feasibility at arbitrary moduli from a fixed unicyclic graph."""

from collections import Counter
from functools import lru_cache
from itertools import permutations
from math import factorial, gcd, prod


def partitions(n):
    """Restricted growth strings for partitions of the marked vertex set."""
    def extend(row):
        if len(row) == n:
            yield tuple(row)
        else:
            for block in range(max(row)+2):
                yield from extend(row+[block])
    yield from extend([0])


def diagonal(rows):
    """Unimodular row and column operations suffice without ordering the factors."""
    matrix = [list(row) for row in rows]
    height, width = len(matrix), len(matrix[0])
    factors = []
    for i in range(min(height,width)):
        pivot = next(((r,c) for r in range(i,height) for c in range(i,width)
                      if matrix[r][c]), None)
        if pivot is None:
            break
        r,c = pivot
        matrix[i],matrix[r] = matrix[r],matrix[i]
        for row in matrix:
            row[i],row[c] = row[c],row[i]
        while True:
            r = next((j for j in range(i+1,height) if matrix[j][i]), None)
            if r is not None:
                q = matrix[r][i]//matrix[i][i]
                matrix[r] = [a-q*b for a,b in zip(matrix[r],matrix[i])]
                if matrix[r][i]:
                    matrix[i],matrix[r] = matrix[r],matrix[i]
                continue
            c = next((j for j in range(i+1,width) if matrix[i][j]), None)
            if c is None:
                break
            q = matrix[i][c]//matrix[i][i]
            for row in matrix:
                row[c] -= q*row[i]
            if matrix[i][c]:
                for row in matrix:
                    row[i],row[c] = row[c],row[i]
        factors.append(abs(matrix[i][i]))
    return width-len(factors), tuple(sorted(d for d in factors if d!=1))


@lru_cache(None)
def kernel(k, signature):
    free, factors = signature
    return k**free * prod(gcd(k,d) for d in factors)


def signatures(edges, port):
    """Vertex 0 is the leaf parent. Use port=None to leave the graph closed."""
    n = len(edges)
    assert sorted({v for edge in edges for v in edge}) == list(range(n))
    opened = port is not None
    if opened:
        u,v = edges[port]
        actual = edges[:port]+edges[port+1:]+[(n,u),(n+1,v)]
    else:
        actual = edges
    table = Counter()
    for partition in partitions(n):
        mobius = prod((-1)**(size-1)*factorial(size-1)
                     for size in Counter(partition).values())
        blocks = max(partition)
        width = blocks + 2*int(opened)
        def vector(sites):
            row = [0]*width
            for index in sites:
                if index<n:
                    block = partition[index]
                    if block:
                        row[block-1] += 1
                else:
                    row[blocks+index-n] += 1
            return row
        weights = [vector(edge) for edge in actual]
        target = [vector([v]) for v in range(n)]
        if opened:
            target.append(vector([n,n+1]))
        for images in permutations(target):
            system = [[a-b for a,b in zip(left,right)] for left,right in zip(weights,images)]
            source = diagonal(system)
            fixed = diagonal(system+[[0]*blocks+[1,-1]]) if opened else source
            table[source,fixed] += mobius
    return {key:n for key,n in table.items() if n}


def matches(table, k, h=0):
    order = k//gcd(k,h)
    total = 0
    for (source,fixed), coefficient in table.items():
        fiber = kernel(k,fixed)
        if (kernel(k,source)//fiber) % order == 0:
            total += coefficient*fiber
    return total


if __name__ == "__main__":
    square = [(0,1),(1,2),(2,3),(3,0)]
    tables = [signatures(square,port) for port in (None,0,1)]
    count = 0
    for k in range(4,129):
        assert matches(tables[0],k)==0
        for h in range(k):
            near,far = [matches(t,k,h) for t in tables[1:]]
            expected = k%2==0 and h not in (0,k//2) and 2*h%k != k//2
            assert near>=0 and (near>0)==expected
            assert far>=0 and (far>0)==(k>=6)
            count += 2
    print(count, "port decisions from integer matrices")

    # Test the counted multiplicities as well as existence on a non-cycle base.
    graph = [(0,1),(1,2),(2,0),(1,3)]
    tests = 0
    for port in (None,0,1,2):
        table = signatures(graph,port)
        for k in range(4,10):
            direct = [0]*k
            for tail in permutations(range(1,k),3):
                x = (0,)+tail
                if port is None:
                    if sorted((x[u]+x[v])%k for u,v in graph)==sorted(x):
                        direct[0] += 1
                    continue
                u,v = graph[port]
                inside = [(x[a]+x[b])%k for i,(a,b) in enumerate(graph) if i!=port]
                for a in range(k):
                    for b in range(k):
                        old = (a+b)%k
                        if sorted(inside+[(a+x[u])%k,(b+x[v])%k]) == sorted((*x,old)):
                            direct[(a-b)%k] += 1+int(old in x)
            for h in range(k if port is not None else 1):
                assert matches(table,k,h) == direct[h]
                tests += 1
    print(tests, "exact multiplicities on a triangle with an attached leaf")

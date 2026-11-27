"""Independently count the shapes by Burnside's lemma and test the actual substitutions."""

import argparse
from itertools import permutations, product
from math import comb, gcd
from pathlib import Path
from random import Random

from .cycle_pendants import chain, read_witnesses


def dihedral_count(c, w):
    fixed = 0
    for a in range(c):
        # Cycles of a rotation all have the same length.
        g = gcd(c,a)
        if w%(c//g) == 0:
            fixed += comb(g,w//(c//g))
        # The reflection i -> a-i has f fixed sites and the rest in pairs.
        f = sum((2*i-a)%c == 0 for i in range(c))
        for j in range(min(f,w)+1):
            if (w-j)%2 == 0 and (w-j)//2 <= (c-f)//2:
                fixed += comb(f,j)*comb((c-f)//2,(w-j)//2)
    assert fixed%(2*c) == 0
    return fixed//(2*c)


def labels_work(labels, edges, n):
    return sorted(labels) == list(range(n)) and sorted(
        (labels[u]+labels[v])%n for u,v in edges) == list(range(n))


def records(n, path):
    count = bad = 0
    seen = set()
    with path.open() as inp:
        for line in inp:
            code,*f = map(int,line.split())
            bits = format(code,'b')[1:]
            c = len(bits)
            assert 4 <= c < n and c%2 == 0 and c+bits.count('1') == n
            key = min(row[i:]+row[:i] for row in (bits,bits[::-1]) for i in range(c))
            assert key not in seen
            seen.add(key)
            edges = [(v,(v+1)%c) for v in range(c)]
            edges.extend((v,c+j) for j,v in enumerate(i for i,b in enumerate(bits) if b=='1'))
            if f:
                assert labels_work(f,edges,n)
            else:
                assert n <= 8
                assert not any(labels_work((0,)+p,edges,n) for p in permutations(range(1,n)))
                bad += 1
            count += 1
    assert count == sum(dihedral_count(c,n-c) for c in range(4,n,2) if n-c <= c)
    return count,bad


def verify_chain(m,ports,left,right,witnesses):
    k = 2*m
    pairs = chain(m,left,right,ports,witnesses)
    counts = [0]*k
    vertices = [0]*k
    previous = left
    for (a,b),row in zip(ports,pairs):
        for x in row:
            assert 0 <= x < k
            vertices[x] += 1
        counts[(previous+row[a])%k] += 1
        counts[sum(row)%k] += 1
        previous = row[b]
    assert previous == left
    counts[(previous+right)%k] += 1
    counts[(left+right)%k] -= 1
    assert vertices == counts == [len(ports)//m]*k


def substitutions(m,witnesses,rng):
    n = 0
    for pattern in product(range(2),repeat=m):
        if all(pattern):
            continue
        first = [rng.randrange(2) for _ in pattern]
        ports = [(a,a^b) for a,b in zip(first,pattern)]
        verify_chain(m,ports,rng.randrange(2*m),rng.randrange(2*m),witnesses)
        n += 1
    for _ in range(100):
        ports = [(rng.randrange(2),rng.randrange(2)) for _ in range(rng.randint(2,9)*m)]
        if len(ports)%2 and all(a != b for a,b in ports):
            ports[-1] = (0,0)
        verify_chain(m,ports,rng.randrange(2*m),rng.randrange(2*m),witnesses)
        n += 1
    return n


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory',type=Path)
    args = parser.parse_args()
    rng = Random(261991)
    total = 0
    for n in range(6,31,2):
        path = args.directory/f'cycle-{n}.txt'
        count,bad = records(n,path)
        print(f'order={n} shapes={count} excluded={bad}')
        if n%4 == 2:
            total += substitutions(n//2,read_witnesses(path),rng)
    print(f'{total} chain substitutions verified')

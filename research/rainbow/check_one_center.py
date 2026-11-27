"""Recount arbitrary-offset grafts on actual trees and check the unit-gap bound."""
from itertools import product
from math import gcd
from random import Random

from .star_period import one_center


def replay(k,children,offsets,center,parents,surplus):
    n = len(offsets)
    shifts = [b if i in children else (b+p)%k for i,(b,p) in enumerate(zip(offsets,parents))]
    new = one_center(k,shifts,center,children)
    assert new is not None and len(new)==n and all(0<=x<k for x in new)
    # The old star has center surplus and leaf labels forming a permutation.
    labels = [surplus]+[(p+surplus)%k for p in range(k)]+[(x+surplus)%k for x in new]
    edges = [(0,1+i,0) for i in range(k)]
    for i,p in enumerate(parents):
        parent = k+1+center if i in children else 1+p
        edges.append((parent,k+1+i,offsets[i]))
    vertex_bins = [0]*k
    edge_bins = [0]*k
    for x in labels:
        vertex_bins[x] += 1
    for u,v,b in edges:
        edge_bins[(labels[u]+labels[v]+b)%k] += 1
    assert max(vertex_bins)-min(vertex_bins)<=1 and max(edge_bins)-min(edge_bins)<=1


def main():
    rng = Random(28112611)
    exhaustive = varied = repairs = 0
    for k in (2,3):
        n = k+1
        for c in range(n):
            for offsets in product(range(k),repeat=n):
                replay(k,set(range(1,c+1)),offsets,0,[0]*n,0)
                exhaustive += 1
    for k in range(2,501):
        units = [x for x in range(k) if gcd(x,k)==1]
        gap = max(b-a for a,b in zip(units,units[1:]+[units[0]+k]))
        assert gap<=k//3+2
    for k in range(2,46):
        for r in sorted({1,2,k//3+1,k-1,k,k+1,2*k+3}):
            n = k+r
            for c in range(n):
                center = rng.randrange(n)
                children = set(rng.sample([i for i in range(n) if i!=center],c))
                parents = [rng.randrange(k) for _ in range(n)]
                offsets = [rng.randrange(k) for _ in range(n)]
                replay(k,children,offsets,center,parents,rng.randrange(k))
                varied += 1
                feasible = range(max(0,c-r),min(c,k-1)+1)
                if not any(gcd(j,k)==1 or gcd(j+1,k)==1 for j in feasible):
                    repairs += 1
    # Several distinct primes give longer gaps; exercise every short-slack
    # exceptional population directly instead of relying on random sampling.
    for k in (60,90,105,210):
        for r in range(1,9):
            for c in range(r,k):
                if any(gcd(j,k)==1 or gcd(j+1,k)==1 for j in range(c-r,c+1)):
                    continue
                n = k+r
                replay(k,set(range(1,c+1)),[rng.randrange(k) for _ in range(n)],0,
                       [rng.randrange(k) for _ in range(n)],0)
                repairs += 1
                varied += 1
    print('exhaustive effective shifts',exhaustive,'other whole trees',varied,
          'virtual-source repairs',repairs,'unit-gap moduli',499)


if __name__=='__main__':
    main()

"""Independently check unrooted coverage, moments, kernels and explicit labelings."""

import argparse
from collections import Counter
import ctypes
import gzip
import json
from pathlib import Path


def shape_key(parents):
    p = len(parents)
    assert parents[0] == -1 and all(0 <= a < i for i,a in enumerate(parents[1:],1))
    adj = [[] for _ in parents]
    for i,a in enumerate(parents[1:],1):
        adj[a].append(i)
        adj[i].append(a)
    def rooted(v, prev):
        return tuple(sorted(rooted(w,v) for w in adj[v] if w != prev))
    return min(rooted(v,-1) for v in range(p))


def free_count(n):
    # Count rooted trees by adjoining unordered multisets of existing tree sizes.
    from math import comb
    ways = [1]+[0]*(n-1)
    rooted = [0]
    for d in range(1,n+1):
        r = ways[d-1]
        rooted.append(r)
        old = ways[:]
        for j in range(d,n):
            ways[j] += sum(comb(r+c-1,c)*old[j-c*d] for c in range(1,j//d+1))
    oriented = sum(rooted[i]*rooted[n-i] for i in range(1,n))
    symmetric = 0 if n%2 else rooted[n//2]
    return rooted[n]-(oriented-symmetric)//2


def rank(vectors, p):
    pivots = {}
    for v in vectors:
        v = list(v)
        for j,x in enumerate(v):
            if not x:
                continue
            if j not in pivots:
                pivots[j] = [a*pow(x,-1,p)%p for a in v]
                break
            for i in range(j,len(v)):
                v[i] = (v[i]-x*pivots[j][i])%p
    return len(pivots)


def verify(lib, p):
    n = p-1
    shapes, dims = set(), Counter()
    total = 0
    path = Path(__file__).with_name(f"p{p}.jsonl.gz")
    with gzip.open(path,"rt") as stream:
        for line in stream:
            par,scalar,columns,cases = json.loads(line)
            assert len(par) == p
            shape = shape_key(par)
            assert shape not in shapes
            shapes.add(shape)
            out = (ctypes.c_int*(1+n*n))()
            lib.orbit_check(p,(ctypes.c_int*p)(*par),int(scalar == 0),out)
            assert scalar == out[0]
            if scalar:
                assert not columns and not cases
                continue
            assert len(columns) == n and all(len(c) == n for c in columns)
            assert [a for c in columns for a in c] == list(out)[1:]
            dim = n-rank([*zip(*columns),[1]+[0]*(n-1)],p)
            dims[dim] += 1
            covered = set()
            for bias,labels in cases:
                assert len(bias) == n and bias[0] == 0 and all(0 <= x < p for x in bias)
                assert next((x for x in bias if x),1) == 1 and tuple(bias) not in covered
                for row in zip(*columns):
                    assert sum(a*b for a,b in zip(row,bias))%p == 0
                assert sorted(labels) == list(range(p))
                assert len({(labels[i]+labels[par[i]]+bias[i-1])%p for i in range(1,p)}) == n
                covered.add(tuple(bias))
            assert len(covered) == 1+(p**dim-1)//(p-1)
            total += len(covered)
    assert len(shapes) == free_count(p)
    print(f"{p}: {len(shapes)} trees, {sum(dims.values())} zero scalars, "
          f"kernel dimensions {dict(sorted(dims.items()))}, {total} explicit cases")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("library")
    parser.add_argument("primes",nargs="*",type=int)
    args = parser.parse_args()
    lib = ctypes.CDLL(str(Path(args.library).resolve()))
    for p in args.primes or [2,3,5,7,11,13]:
        assert p in (2,3,5,7,11,13)
        verify(lib,p)

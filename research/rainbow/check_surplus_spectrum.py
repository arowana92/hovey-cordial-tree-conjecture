"""Verify raw boundary-orbit coverage, all positive rows, and all negative rows."""
from itertools import permutations
from math import comb,gcd
from pathlib import Path
import json
import sys

from research.eight.verify import components


def catalog(k,n):
    def coefficient(types,total):
        p = [1]+[0]*total
        for size,multiplicity in enumerate(types,1):
            p = [sum(p[s-size*j]*comb(multiplicity+j-1,j) for j in range(s//size+1))
                 for s in range(total+1)]
        return p[total]
    rooted = []
    for size in range(1,n+1):
        rooted.append(coefficient(rooted,size-1))
    return coefficient([k*c for c in rooted],n)


def orbit(ps,k):
    items = components(ps)
    return {tuple(sorted(((u*x)%k,tree) for x,tree in items))
            for u in range(1,k) if gcd(u,k)==1}


def verify(path,k):
    seen = set()
    bad = []
    raw = neg = 0
    with path.open() as rows:
        for line in rows:
            ps,f = json.loads(line)
            assert len(ps)==k-1 and all(-k<=p<i for i,p in enumerate(ps))
            images = orbit(ps,k)
            canonical = repr(min(images))
            assert canonical not in seen
            seen.add(canonical)
            raw += len(images)
            def distinct(g):
                return len({(g[i]+(g[p] if p>=0 else -1-p))%k for i,p in enumerate(ps)})==k-1
            if f:
                assert sorted(f)==list(range(1,k)) and distinct(f)
            else:
                assert not any(distinct(g) for g in permutations(range(1,k)))
                bad.append(ps)
                neg += len(images)
    assert raw==catalog(k,k-1)
    print('modulus',k,'colored forests',raw,'orbits',len(seen),'failed orbits',len(bad),
          'failed colored forests',neg,flush=True)
    return bad


if __name__=='__main__':
    failures = verify(Path(sys.argv[2]),int(sys.argv[1]))
    if len(sys.argv)>3:
        Path(sys.argv[3]).write_text(json.dumps(failures)+'\n')

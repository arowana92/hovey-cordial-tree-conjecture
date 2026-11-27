"""Check each cyclic order and independently count all compatible weight-hole sets."""
from math import comb,gcd
from pathlib import Path
import sys


def verify(k,h,path):
    universe = set(range(k))
    total = k*(k-1)//2
    # The coefficient indexed by cardinality and residue counts distinct subsets.
    counts = [[0]*k for _ in range(h+1)]
    counts[0][0] = 1
    for x in range(k):
        for j in range(h,0,-1):
            for r,z in enumerate(counts[j-1]):
                counts[j][(r+x)%k] += z
    covered = set()
    rows = raw = representatives = 0
    old = None
    with path.open() as stream:
        for line in stream:
            x,y,*cycle = map(int,line.split())
            if x!=old:
                if old is not None:
                    assert len(weight_holes)==counts[h][target]
                    raw += orbit_size*len(weight_holes)
                omitted = [i for i in range(k) if x>>i&1]
                assert len(omitted)==h and x<1<<k and min(omitted)>=0
                images = {sum(1<<((u*i+t)%k) for i in omitted)
                          for u in range(1,k) if gcd(k,u)==1 for t in range(k)}
                assert covered.isdisjoint(images)
                covered.update(images)
                orbit_size = len(images)
                target = (2*sum(omitted)-total)%k
                vertices = universe-set(omitted)
                weight_holes = set()
                old = x
                representatives += 1
            assert y not in weight_holes and len(cycle)==k-h and set(cycle)==vertices
            weights = {(a+b)%k for a,b in zip(cycle,cycle[1:]+cycle[:1])}
            missing = universe-weights
            assert len(missing)==h and sum(1<<i for i in missing)==y and sum(missing)%k==target
            weight_holes.add(y)
            rows += 1
    assert old is not None and len(weight_holes)==counts[h][target]
    raw += orbit_size*len(weight_holes)
    assert len(covered)==comb(k,h)
    assert raw==sum(n*counts[h][(2*r-total)%k] for r,n in enumerate(counts[h]))
    print(k,h,'vertex orbits',representatives,'cycles',rows,'compatible pairs',raw,flush=True)


if __name__=='__main__':
    verify(int(sys.argv[1]),int(sys.argv[2]),Path(sys.argv[3]))

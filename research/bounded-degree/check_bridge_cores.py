"""Check path weights, auxiliary embedding hypotheses and long-bridge parities."""
from collections import Counter
from itertools import product
from math import gcd
from pathlib import Path
from random import Random
import sys

from bridge_cores import short,auxiliary
from partial_gap import build as complete_core
from port_parity import build as reconnect
from check_two_leaf_repair import inspect
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from research.census.cycle_subdivision import pendant


def short_cases():
    count = 0
    for k in range(5,32):
        for t in range(3,k):
            if k <= 4*t-10+2*gcd(2,k):
                continue
            for b in range(k):
                for d,e in ((0,0),(b,b),((b+2)%k,(b-1)%k),(k//2,(b+k//2)%k)):
                    row = short(k,0,b,d,e,t)
                    assert len(row)==len(set(row))==t
                    path = [0]+row+[b]
                    delta = Counter((x+y)%k for x,y in zip(path,path[1:]))
                    delta[d] -= 1
                    delta[e] -= 1
                    assert all(v in (0,1) for v in delta.values())
                    count += 1
    return count


def auxiliary_cases(rng):
    count = 0
    for k in (180,225,256,315,504,729):
        for t in (8,9,k//2,k-3,k-2,k-1):
            for i in range(15):
                a,b,d,e = (rng.randrange(k) for _ in range(4))
                if i%3==0:
                    a,d = b,e
                if i%3==1:
                    d,e = (a+b+sum(range(k)))%k,(a+b)%k
                edges,pins,gap = auxiliary(k,a,b,d,e,t)
                full = complete_core(edges,pins,gap,rng)
                assert full is not None and all(full[v]==x for v,x in pins.items())
                degree = Counter(v for edge in edges for v in edge)
                assert len(edges)==k-1 and [(v,v+1) for v in range(t-1)]==edges[:t-1]
                assert len(set(full.values()))==len(full)
                sums = [(full[u]+full[v])%k for u,v in edges if u in full and v in full]
                assert len(set(sums))==len(sums) and gap not in sums
                assert sum(full.values())%k==sum(range(k))%k
                assert sum(degree[v]*x for v,x in full.items())%k==(sum(range(k))-gap)%k
                for d0 in set(degree.values()):
                    positions = {v for v in degree if degree[v]==d0}
                    marked = len(positions & full.keys())
                    assert marked==len(positions) or min(marked,len(positions)-marked)>=6
                # E occurs on the retained path; the other entering sum occurs on a discarded edge.
                assert (a+full[0])%k==d and (full[2]+full[3])%k==e
                assert (b+full[t-1])%k==(full[5]+full[t])%k
                count += 1
    return count


def long_cases(rng):
    good = bad = 0
    for k in (180,225,256,315):
        tree = [(i-1,i) for i in range(1,k)]
        total = sum(range(k))
        for t in (k,k+1,k+2,2*k,2*k+1,3*k+1,4*k-1):
            for i in range(8):
                a,b,d,e = (rng.randrange(k) for _ in range(4))
                # For the first divisible tree use normalized counts 1 on vertices,
                # and 1 on edges except for its single missing weight.
                prefix = []
                if t>k:
                    first = (d-a)%k
                    prefix = [first]+pendant(k,first,first,t-k-1)
                z = prefix[-1] if prefix else a
                f = Counter((u+v)%k for u,v in zip([a]+prefix,prefix))
                f[d] -= 1
                g = Counter(prefix)
                def high(counts):
                    low = min(counts[x] for x in range(k))
                    assert all(counts[x]-low in (0,1) for x in range(k))
                    return {x for x in range(k) if counts[x]>low}
                eh,vh = high(f),high(g)
                target = (e-z-b-total)%k
                if not target:
                    # The uniform path case is covered by the uniform two-port theorem.
                    assert not (k%2==0 and t%k==1 and (a+b-d-e-(t//k)*total)%2)
                    continue
                result = reconnect(tree,[0,k-1],[z,b],[e],eh,vh,rng)
                obstruction = k%2==0 and t%k==1 and (a+b-d-e-(t//k)*total)%2==1
                assert (result is None) == obstruction
                if result is None:
                    bad += 1
                else:
                    aux,labels,absent,dup,gap,holes = result
                    inspect(k,tree,[0,k-1],[z,b],[e],eh,vh,(aux,labels,absent,dup[1],gap[1],holes))
                    good += 1
    return good,bad


if __name__ == '__main__':
    rng = Random(199192)
    print("Elementary bridges",short_cases())
    print("Prescribed embedding cores",auxiliary_cases(rng))
    print("Long bridges and parity obstructions",long_cases(rng))

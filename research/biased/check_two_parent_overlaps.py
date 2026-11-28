"""Check the three-vertex overlap argument, actual leaf joins, and the long-path cut."""
from collections import Counter
from itertools import combinations, combinations_with_replacement
from math import gcd
from random import Random

from .check_two_parent_pruning import match


def rotate(mask,step,k):
    step %= k
    return ((mask << step) | (mask >> (k-step))) & ((1 << k)-1)


def bad_pairs(k):
    cases = pairs = 0
    for delta in range(1,k):
        weights = 1 | (1 << delta)
        for sites in combinations(range(k),3):
            high = sum(1 << x for x in sites)
            vacant = ((1 << k)-1) ^ (high | weights)
            bad = []
            for t in range(1,k):
                moved = rotate(high,t,k)
                overlap = moved & weights
                if not overlap or (overlap & (overlap-1)):
                    continue
                if not (moved | rotate(weights,-t,k)) & vacant:
                    bad.append(t)
            assert len(bad)<=2
            for a,b in combinations(bad,2):
                assert k//gcd(k,a-b)==5 and {a,b}=={delta,k-delta}
                # A fourth addition can always raise a count after a blocked pair.
                for y in range(k):
                    if not vacant & (1 << y):
                        continue
                    after = high | (1 << y)
                    assert all(bin(rotate(after,z,k) & ~after).count('1')>=2 for z in range(1,k))
                pairs+=1
            cases+=1
    return cases,pairs


def build(k,h,parents,a,b,rng):
    vertices = [0]+list(range(k))
    edges = [(0,i+1) for i in range(k)]
    high,weights = {0},set()
    def shared(p):
        return len({(x+p)%k for x in high}&weights)
    for i,parent in enumerate(parents):
        p = vertices[parent]
        order = list(range(1,k))
        rng.shuffle(order)
        for x in order:
            w=(p+x)%k
            if x in high or w in weights:
                continue
            def grows(t):
                return (p==t or (w-t)%k in high or (x+t)%k in weights)
            if i<2 and not shared((a,b)[i]) and not grows((a,b)[i]):
                continue
            if i in (2,3) and a!=b and max(shared(a),shared(b))==1 and not (grows(a) or grows(b)):
                continue
            break
        else:
            assert i==2 and h>=5 and a!=b and k//gcd(k,a-b)==5
            x=next(x for x in order if x not in high and (p+x)%k not in weights)
            w=(p+x)%k
        edges.append((parent,len(vertices)))
        vertices.append(x)
        high.add(x)
        weights.add(w)
    assert min(shared(a),shared(b))>=1 and (a==b or max(shared(a),shared(b))>=2)
    return vertices,edges,high,weights


def tree_trials():
    rng=Random(271152)
    cases=0
    for k in range(7,31):
        for h in range(4,(k+2)//2+1):
            r=k-2*h+2
            if r<1:
                continue
            for step in sorted({gcd(k,i) for i in range(1,k)}):
                if k//step==5 and h<5:
                    continue
                a=rng.randrange(k)
                b=(a+step)%k
                parents=[rng.randrange(k+1+i) for i in range(h-1)]
                vertices,edges,high,weights=build(k,h,parents,a,b,rng)
                for j in sorted(set(range(r+1)) if k==27 else {0,r//2,r}):
                    labels=match(k,a,b,high,weights,r-j,j)
                    assert labels is not None
                    vs=vertices[:]
                    es=edges[:]
                    for x,choice in labels:
                        es.append((1+(a if choice==1 else b),len(vs)))
                        vs.append(x)
                    for bins in (Counter(vs),Counter((vs[v]+vs[w])%k for v,w in es)):
                        sizes=[bins[i] for i in range(k)]
                        assert max(sizes)-min(sizes)<=1
                    cases+=1
    return cases


def windows(k):
    count=0
    for e in range(5):
        for pos in combinations_with_replacement(range(k),e):
            mass=[1]*k
            for j in pos:
                mass[j]+=1
            assert any(sum(mass[i:j])==k for j in range(1,k+1) for i in range(j))
            count+=1
    return count


if __name__=='__main__':
    totals=[bad_pairs(k) for k in [*range(6,23),27,30]]
    assert any(b for _,b in totals)
    print('three-source and two-weight sets',sum(n for n,_ in totals),
          'simultaneously blocked shift pairs',sum(b for _,b in totals),flush=True)
    print('whole trees',tree_trials(),'corridor windows',windows(27))

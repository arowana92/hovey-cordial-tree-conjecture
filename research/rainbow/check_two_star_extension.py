"""Verify final histograms on actual trees and exhaust small star packets."""
from collections import Counter
from itertools import combinations
from math import gcd, isqrt
from random import Random

from .two_star_extension import extend


def deficits(k,s,q):
    """Positive inputs by literal center/leaf-subset enumeration, with old parent zero."""
    colors = set(range(k))
    good = set()
    for x in colors:
        for y in colors-{x}:
            rest = colors-{x,y}
            for leaves in combinations(rest,s-1):
                weights = [x,(q+y)%k]+[(v+x)%k for v in leaves]+[
                    (v+y)%k for v in rest-set(leaves)]
                counts = Counter(weights)
                if len(counts)==k:
                    return colors
                if len(counts)==k-1:
                    good.update(z for z,n in counts.items() if n==2)
    return good


def core(k,d):
    """A concrete cordial tree of divisible order containing every prescribed label."""
    labels = list(range(k))
    if k==2 and d==1:
        return [0,0,1,1],[(0,1),(1,2),(2,3)]
    for u in labels:
        edges = [(u,v) for v in labels if u!=v]
        if 2*u%k==d:
            return labels,edges
        c,r = (d-u)%k,(3*u-d)%k
        if len({c,r,u})==3:
            edges.remove((u,c))
            edges.append((c,r))
            return labels,edges
    raise AssertionError('missing core')


def replay(k,s,t,a,b,d,parts):
    assert list(map(len,parts))==[s,t]
    labels,edges = core(k,d)
    original = Counter((labels[i]+labels[j])%k for i,j in edges)
    assert all(original[i]==len(labels)//k-(i==d) for i in range(k))
    for part,old in zip(parts,(a,b)):
        center = len(labels)
        edges.extend([(labels.index(old),center)]+[(center,center+j) for j in range(1,len(part))])
        labels.extend(part)
    assert len(edges)==len(labels)-1
    for counts in (Counter(labels),Counter((labels[i]+labels[j])%k for i,j in edges)):
        bins = [counts[z] for z in range(k)]
        assert max(bins)-min(bins)<=1


def capacity_search(k,s,q,d):
    """Assign each actual leaf label to one of the two centers under weight caps."""
    calls = 0
    def place(remaining,need):
        nonlocal calls
        calls += 1
        if not remaining:
            return need==0
        best = None
        for v in remaining:
            options = []
            if need and capacity[(x+v)%k]:
                options.append((0,(x+v)%k))
            if need<len(remaining) and capacity[(y+v)%k]:
                options.append((1,(y+v)%k))
            if not options:
                return False
            if best is None or len(options)<len(best[1]):
                best = v,options
            if len(options)==1:
                break
        v,options = best
        for side,w in options:
            capacity[w] -= 1
            if place(remaining-{v},need-(side==0)):
                return True
            capacity[w] += 1
        return False

    for x in range(k):
        for y in range(k):
            if x!=y:
                capacity = [1+int(w==d) for w in range(k)]
                capacity[x] -= 1
                capacity[(q+y)%k] -= 1
                if min(capacity)>=0 and place(set(range(k))-{x,y},s-1):
                    return True,calls
    return False,calls


def prime(n):
    return n>=2 and all(n%d for d in range(2,isqrt(n)+1))


def check():
    literal = joins = negative = antipodal = semiprime = 0
    rng = Random(1991)
    for k in range(2,11):
        for s in range(1,k):
            for q in range(k):
                expected = deficits(k,s,q)
                for d in range(k):
                    parts = extend(k,s,k-s,0,q,d)
                    assert (parts is not None)==(d in expected)
                    if parts is not None:
                        replay(k,s,k-s,0,q,d,parts)
                        joins += 1
                    literal += 1
    for k in range(3,161):
        for _ in range(80):
            s,t = rng.randrange(1,3*k),rng.randrange(1,3*k)
            a,b,d = [rng.randrange(k) for _ in range(3)]
            parts = extend(k,s,t,a,b,d)
            if parts is None:
                assert s+t==k
                negative += 1
            else:
                replay(k,s,t,a,b,d,parts)
                joins += 1
        if k%2==0:
            for s in range(1,k//2+1):
                parts = extend(k,s,k-s,0,k//2,0)
                fail = s%(k&-k)==0 and gcd(k//2,s*s-1)==1
                assert (parts is None)==fail
                antipodal += 1
                if parts is None:
                    negative += 1
                else:
                    replay(k,s,k-s,0,k//2,0,parts)
                    joins += 1
        if k%2==0 and k//2>2 and prime(k//2):
            p = k//2
            # All q up to units, with every deficit and every split up to exchange.
            for q in (0,1,2,p):
                for s in range(1,p+1):
                    for d in range(k):
                        if (q-d)%gcd(s,k)==0:
                            continue
                        parts = extend(k,s,k-s,0,q,d)
                        fail = q==p and d==0 and s%2==0 and s!=p-1
                        assert (parts is None)==fail
                        semiprime += 1
                        if parts is None:
                            negative += 1
                        else:
                            replay(k,s,k-s,0,q,d,parts)
                            joins += 1
    # Concentrate large prime-power tests on the singular subgroup case.
    for k in (16,25,27,32,49,64,81,121,125,128,169,243,256,343,512,625,729,1024):
        for _ in range(100):
            delta = rng.randrange(1,k)
            q = rng.randrange(k)*delta%k
            m = k//gcd(delta,k)
            if m==k:
                continue
            s = rng.randrange(1,k//m)*m
            d = (q+delta)%k
            parts = extend(k,s,k-s,0,q,d)
            assert parts is not None
            replay(k,s,k-s,0,q,d,parts)
            joins += 1
    searches = 0
    for s in range(2,13,2):
        possible,calls = capacity_search(26,s,13,0)
        assert possible==(s==12)
        searches += calls
    semiprime_small = 0
    for p in range(2,16):
        if prime(p):
            for q in range(p+2,180//p+1):
                if prime(q):
                    k = p*q
                    for b in range(q,k,q):
                        for delta in range(q,k,q):
                            assert extend(k,p,k-p,0,b,(b+delta)%k) is None
                            semiprime_small += 1
    print('direct 26-label search nodes',searches,'small-star semiprime obstructions',semiprime_small)
    print('literal small inputs',literal,'whole-tree extensions',joins,
          'obstructions across tests',negative,'antipodal inputs',antipodal,
          'twice-prime inputs beyond the prefix criterion',semiprime)


if __name__=='__main__':
    check()

"""Rebuild cordial cores with unit surplus differences and attach two groups of leaves."""
from collections import Counter
from functools import lru_cache
from math import gcd
from random import Random


def match(k, a, b, inputs, weights, first, second):
    step = (b-a)%k
    g = gcd(k,step)
    d = k//g
    assert d >= 2
    sites = [(i+j*step)%k for i in range(g) for j in range(d)]

    @lru_cache(None)
    def walk(i, p, q, previous_shifted, first_flat):
        if p+q == 0:
            return ()
        if k-i < p+q:
            return None
        x = sites[i]
        start = i%d == 0
        end = i%d == d-1
        for choice in (1,2,0):
            if choice == 1 and (not p or (not start and previous_shifted) or (x+a)%k in weights):
                continue
            if choice == 2 and (not q or (end and first_flat) or (x+b)%k in weights):
                continue
            if choice and x in inputs:
                continue
            tail = walk(i+1,p-(choice==1),q-(choice==2),choice==2,choice==1 if start else first_flat)
            if tail is not None:
                return ((x,choice),)+tail if choice else tail
        return None

    answer = walk(0,first,second,False,False)
    walk.cache_clear()
    return answer


def trial(k,h,rng):
    # The star on k+1 vertices has surplus zero and every residue at an old vertex.
    vertices = [0]+list(range(k))
    edges = [(0,i+1) for i in range(k)]
    high, weights = {0}, set()
    for j in range(h-1):
        parent = len(vertices)-1 if j%2 else rng.randrange(len(vertices))
        y = next(u for u in range(1,k) if gcd(u,k)==1 and u not in high
                 and (vertices[parent]+u)%k not in weights)
        edges.append((parent,len(vertices)))
        weights.add((vertices[parent]+y)%k)
        high.add(y)
        vertices.append(y)
    assert {x for x in high if gcd(x,k)>1} == {0}
    r = k-2*h+1
    tests = 0
    for step in sorted({gcd(i,k) for i in range(1,k)}):
        a = rng.randrange(k)
        b = (a+step)%k
        for j in sorted({0,r//2,r} | (set(range(r+1)) if k==27 else set())):
            chosen = match(k,a,b,high,weights,r-j,j)
            assert chosen is not None
            colors = vertices[:]
            actual = list(edges)
            for x,choice in chosen:
                actual.append((1+(a if choice==1 else b),len(colors)))
                colors.append(x)
            assert len(colors)-1==len(actual)
            for hist in (Counter(colors),Counter((colors[u]+colors[v])%k for u,v in actual)):
                counts=[hist[x] for x in range(k)]
                assert max(counts)-min(counts)<=1
            tests += 1
    return tests


if __name__=='__main__':
    rng = Random(271128)
    cases = sum(trial(k,h,rng) for k in range(3,46) for h in range(1,(k+1)//2+1)
                if k-2*h+1>0 and sum(gcd(u,k)==1 for u in range(1,k))>2*(h-2))
    print('whole trees recounted',cases)

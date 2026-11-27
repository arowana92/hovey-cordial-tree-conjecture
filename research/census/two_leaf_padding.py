"""Add two leaves and a replacement path while increasing all bins by one."""
from functools import lru_cache
from itertools import permutations
from math import gcd
from pathlib import Path

from .cycle_subdivision import after, interval_cycle


@lru_cache(None)
def even_cycles():
    result = {}
    source = Path(__file__).with_name("two-leaf-cycles.txt")
    for line in source.read_text().splitlines():
        k,h,x,y,*row = map(int,line.split())
        result.setdefault((k,h),[]).append((x,y,row))
    return result


def odd_templates(k,h):
    r = (k-3)//2
    cycle = interval_cycle(k-2)
    if h==0:
        yield cycle,r-2,r-1
        return
    g = gcd(k,h)
    if g==1:
        yield cycle,r-1,r-2
        t = 1
    elif g<=r//2:
        t = g
    else:
        assert 3*g==k
        t = (g-1)//2
    i,j = 2*(t-1),2*(r-t)
    switched = cycle[:i+1]+cycle[i+1:j+1][::-1]+cycle[j+1:]
    first,second = r-1+2*t,(3*r+1-2*t)%k
    if g==1 or g<=r//2:
        yield switched,second,first
    else:
        yield switched,first,second


def direct(k,a,b,p,q):
    """Exact finite check for the smallest moduli."""
    for f in permutations(range(k)):
        x,y,*row = f
        chain = [a]+row+[b]
        bins = [0]*k
        bins[(a+b)%k] -= 1
        bins[(x+p)%k] += 1
        bins[(y+q)%k] += 1
        for left,right in zip(chain,chain[1:]):
            bins[(left+right)%k] += 1
        if bins==[1]*k:
            return x,y,row
    return None


def two_leaves(k,a,b,p,q):
    """Return the leaf labels at p,q and the ordered new vertices from a to b."""
    if k<5 or k in (6,8):
        raise ValueError("this constructor requires odd k>=5 or even 10<=k<=64")
    if k==5:
        return direct(k,a,b,p,q)
    h = (q-p)%k
    if k%2:
        # A template has leaf labels -2 and -1 and missing weights A and B.
        for cycle,A,B in odd_templates(k,h):
            P,Q = A+2,B+1
            for u in range(1,k):
                if gcd(u,k)!=1 or (Q-P)*u%k!=h:
                    continue
                shift = (p-u*P)%k
                x,y = (shift-2*u)%k,(shift-u)%k
                if a not in (x,y):
                    return x,y,after([(u*v+shift)%k for v in cycle],a)
    elif k<=64:
        g = gcd(k,h)%k
        u = next(v for v in range(1,k) if gcd(v,k)==1 and v*g%k==h)
        for x,y,cycle in even_cycles()[k,g]:
            if a not in ((p+u*x)%k,(p+u*y)%k):
                return (p+u*x)%k,(p+u*y)%k,after([(p+u*v)%k for v in cycle],a)
    else:
        raise ValueError("no explicit cycle table at this even modulus")
    raise AssertionError("the disjoint omitted pairs supply an anchor")


def padded_tree(k,edges,chosen,extra):
    """Label a tree after inserting extra vertices on the specified edge."""
    n = len(edges)+1
    a,b = edges[chosen]
    adjacent = [set() for _ in range(n)]
    for u,v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    batches = []
    tips = {v for v in range(n) if v not in (a,b) and len(adjacent[v])==1}
    while len(tips)>=2:
        pair = sorted(tips)[:2]
        batch = [(v,next(iter(adjacent[v]))) for v in pair]
        tips.difference_update(pair)
        for v,p in batch:
            adjacent[p].remove(v)
            adjacent[v].clear()
            if p not in (a,b) and len(adjacent[p])==1:
                tips.add(p)
        batches.append(batch)

    spare = extra-(k-2)*len(batches)
    if spare<0:
        raise ValueError("too few subdivisions for this peeling")
    start = next(i for i,neigh in enumerate(adjacent) if len(neigh)==1)
    path = [start]
    while True:
        v = path[-1]
        choices = adjacent[v] - set(path[-2:-1])
        if not choices:
            break
        path.append(next(iter(choices)))
    if path.index(a)>path.index(b):
        path.reverse()
    pos = path.index(b)
    assert path[pos-1]==a
    total = len(path)+spare
    base = [(i//2+(i%2)*((total+1)//2))%k for i in range(total)]
    labels = [None]*n
    inside = base[pos:pos+spare]
    for i,v in enumerate(path):
        labels[v] = base[i if i<pos else i+spare]
    for (u,p),(v,q) in reversed(batches):
        start = inside[-1] if inside else labels[a]
        labels[u],labels[v],row = two_leaves(k,start,labels[b],labels[p],labels[q])
        inside.extend(row)
    return labels,inside

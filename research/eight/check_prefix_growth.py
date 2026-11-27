"""Check whole growing trees and independently test the all-moduli obstruction."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from math import gcd
from random import Random

from .prefix_growth import construct
from .surplus_grafts import star


def replay(k,parents,core,additions):
    assert additions is not None and len(core)+len(additions)==len(parents)
    present = dict(enumerate(core))
    vertices = Counter(core)
    edges = Counter((core[i]+core[parents[i]])%k for i in range(1,len(core)))
    for v,x in additions:
        assert v not in present and parents[v] in present
        edges[(x+present[parents[v]])%k] += 1
        present[v] = x
        vertices[x] += 1
        for counts in (vertices,edges):
            bins = [counts[a] for a in range(k)]
            assert max(bins)-min(bins)<=1
    assert set(present)==set(range(len(parents)))
    return len(additions)


def core_paths(k):
    # Actual divisible-order cores realizing every possible edge deficit.
    by_deficit = {}
    for labels in permutations(range(k)):
        missing = set(range(k))-{(a+b)%k for a,b in zip(labels,labels[1:])}
        if len(missing)==1:
            d, = missing
            by_deficit.setdefault(d,list(labels))
        if len(by_deficit)==k:
            break
    assert len(by_deficit)==k
    return by_deficit


def add_stars(parents,a,b,s,t):
    for site,size in ((a,s),(b,t)):
        center = len(parents)
        parents.extend([site]+[center]*(size-1))


def verify_growth():
    rng = Random(1991)
    checked = failures = prefixes = 0
    for k in (8,9):
        sources = core_paths(k)
        for size in range(1,k//2+1):
            for a,b,d in product(range(k),repeat=3):
                core = sources[d]
                ps = [-1]+list(range(k-1))
                add_stars(ps,core.index(a),core.index(b),size,k-size)
                result = construct(k,ps,core)
                impossible = (a+b-d)%gcd(size,k)!=0
                assert (result is None)==impossible
                if impossible:
                    failures += 1
                else:
                    prefixes += replay(k,ps,core,result)
                    checked += 1
        for base in (k,k+1):
            for p in range(k):
                for s in ((2,4) if k==8 else (3,)):
                    if base==k:
                        core = sources[(3*p)%k]
                        ps = [-1]+list(range(k-1))
                    else:
                        core = [0]+list(range(k))
                        ps = [-1]+[0]*k
                    current = core.index(p)
                    for _ in range(k-base%k):
                        ps.append(current)
                        current = len(ps)-1
                    add_stars(ps,current,current,s,k-s)
                    prefixes += replay(k,ps,core,construct(k,ps,core))
                    checked += 1
        for n in range(1,80):
            for trial in range(3):
                ps = [-1]+[rng.randrange(i) if trial==0 else
                           (i-1 if trial==1 else rng.randrange(min(i,7))) for i in range(1,n)]
                core = [rng.randrange(k)]
                prefixes += replay(k,ps,core,construct(k,ps,core))
                checked += 1
    print('complete growth orders',checked,'cordial prefixes',prefixes,'two-star failures',failures)


def local_congruence():
    valid = cases = 0
    for k in range(3,14):
        nonzero = set(range(1,k))
        for s in range(1,k):
            # The first star has size k-s; translate its forced center to zero.
            g = gcd(s,k)
            for b in range(k):
                possible = False
                for y in nonzero:
                    for leaves in combinations(nonzero-{y},s-1):
                        singles = nonzero-{y}-set(leaves)
                        weights = singles | {(b+y)%k} | {(y+x)%k for x in leaves}
                        if len(weights)==k-1:
                            missing, = set(range(k))-weights
                            assert b%g==0 and (missing-y)%g==0
                            possible = True
                            valid += 1
                assert possible==(b%g==0)
                cases += 1
    print('two-star congruence cases',cases,'successful center and leaf-set assignments',valid)


def obstruction(k):
    p = next(d for d in range(2,k) if k%d==0)
    g = k//p
    parents = [-1]+[0]*(k-1)
    previous_center = 0
    for old_vertex in range(p+1):
        second_center = len(parents)+g
        add_stars(parents,previous_center,old_vertex,g,k-g)
        previous_center = second_center
    return parents


def literal_order(k):
    # Enumerate the actual permutations in each ordered k-block. Retain the
    # next deficit and second-center label, the only new data used afterwards.
    ps = obstruction(k)
    prime = len(ps[k:])//k-1
    block = k//prime
    words = list(permutations(range(k)))

    @lru_cache(None)
    def advance(start,a,b,d):
        results = set()
        for labels in words:
            incoming = []
            for j,x in enumerate(labels):
                old = ps[start+j]
                other = labels[old-start] if old>=start else (a if j==0 else b)
                incoming.append((x+other)%k)
            if incoming[0]==d and len(set(incoming[1:]))==k-1:
                missing, = set(range(k))-set(incoming[1:])
                results.add((labels[block],missing))
        return results

    checked = 0
    for initial in words:
        if initial[0]!=0:
            continue
        weights = {(initial[i]+initial[ps[i]])%k for i in range(1,k)}
        if len(weights)!=k-1:
            continue
        d, = set(range(k))-weights
        states = {(initial[0],d)}
        for i,start in enumerate(range(k,len(ps),k)):
            states = set().union(*(advance(start,a,initial[i],gap) for a,gap in states))
        assert not states
        checked += 1
    print('ordered obstruction',k,'vertices',len(ps),'normalized initial labelings exhausted',checked)


def reordered(k):
    ps = obstruction(k)
    prime = len(ps)//k-2
    g = k//prime
    same_class = list(range(1,k,g))
    initial = [0]+same_class+[x for x in range(1,k) if x not in same_class]
    labels = initial.copy()
    gap = 0
    order = list(range(k))
    for number,start in enumerate(range(k,len(ps),k)):
        if number==0:
            kids = [(-j)%k for j in range(1,g)]
            others = sorted(set(range(k))-{0,1}-set(kids))
            labels.extend([1]+kids+[0]+others)
            first = start+g
            order.extend([first]+[v for v in range(start,start+k) if v!=first])
        else:
            first = start
            x = (gap-labels[ps[first]])%k
            boundary = (labels[ps[start+g]]-x)%k
            y,kids,others = star(k,k-g-1,boundary)
            word = [0]+others+[y]+kids
            labels.extend((x+z)%k for z in word)
            order.extend(range(start,start+k))
        recent = {(labels[v]+labels[ps[v]])%k for v in range(start,start+k) if v!=first}
        gap, = set(range(k))-recent
    return replay(k,ps,initial[:1],[(v,labels[v]) for v in order[1:]])


if __name__=='__main__':
    verify_growth()
    local_congruence()
    for k in (4,6):
        literal_order(k)
    composites = [k for k in range(4,101) if any(k%d==0 for d in range(2,k))]
    restored = sum(reordered(k) for k in composites)
    print('reordered composite examples',len(composites),'cordial additions',restored)

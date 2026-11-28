"""Check lifted histogram counts, modular moments and actual embedding cores."""
from collections import Counter
from functools import reduce
from math import gcd
from random import Random

from check import adjacency
from check_shifted_ring import verify
from edge_histogram import construct
from spectrum_projection import lift


def feasible(edges, opening, root, a, bins, shifts):
    k = len(bins)
    n = len(edges) if opening else len(edges)+1
    copies = n//k
    graph = adjacency(n,edges)
    degree = list(map(len,graph))
    leaves = [v for v,d in enumerate(degree) if d==1]
    vertex_sum = copies*sum(range(k))
    weights = sum(j*b for j,b in enumerate(bins))
    moment = weights-vertex_sum-sum(shifts.values())
    h = reduce(gcd,(d-1 for v,d in enumerate(degree) if v!=root),k)
    if (moment-(degree[root]-1)*a)%h:
        return False
    correction = (vertex_sum-moment)%k
    if not leaves:
        return correction==0
    if copies>1:
        return True
    if len(leaves)==1:
        if not correction:
            return False
        y = leaves[0]
        j = degree.index(3)
        z = next(iter(graph[y]))
        if z in graph[j]:
            dy = shifts.get(tuple(sorted((y,z))),0)
            dj = shifts.get(tuple(sorted((j,z))),0)
            if (correction+dy-dj)%k==0:
                return max(bins)>1
    return opening is not None or root not in leaves or len(leaves)>2 or (2*a-correction)%k!=0


def fixtures(n):
    cycle = [(v,(v+1)%n) for v in range(n)]
    yield cycle, cycle[0], 1
    c = n-2
    tail = [(v,(v+1)%c) for v in range(c)] + [(0,c),(c,c+1)]
    yield tail, tail[0], 1
    yield tail, tail[c//2], c//2
    if n%2==0:
        c=n//2
        sun = [(v,(v+1)%c) for v in range(c)] + [(v,v+c) for v in range(c)]
        yield sun, sun[1], 1
    path = [(v-1,v) for v in range(1,n)]
    yield path, None, 0
    yield path, None, n//2
    if n%3==0:
        edges = [(0,1),(0,2)]
        for s in range(3,n,3):
            edges.extend((s//3,t) for t in range(s,s+3))
        yield edges, None, 0


def audit(n,k,edges,opening,anchor,a,hist,offsets,rng):
    lifted = lift(edges,opening,anchor,a,hist,offsets)
    expected = feasible(edges,opening,anchor,a,hist,offsets)
    if lifted is None:
        assert not expected
        return False
    missing, extra, shifts = lifted
    target = Counter(range(n))
    target.subtract(missing)
    target.update(extra)
    reduced = [0]*k
    for x,amount in target.items():
        reduced[x%k] += amount
    assert min(target.values())>=0 and reduced==hist
    assert len(missing)==sum(max(0,n//k-h) for h in hist)
    assert all((shifts.get(tuple(sorted(e)),0)-offsets.get(tuple(sorted(e)),0))%k==0 for e in edges)
    result = construct(edges,opening,anchor,a,missing,extra,rng,cap=4,offsets=shifts)
    assert (result is not None)==expected
    if result is None:
        return False
    aux, pairs, temp = result
    kept, _, gap, pins, core = aux
    assert pins[anchor]==a and all(core[v]==x for v,x in pins.items())
    if opening:
        verify(edges,{frozenset(pair):x for pair,x in temp.items() if x},aux)
    else:
        adj = adjacency(n,kept)
        assert len(core)==len(set(core.values())) and (sum(core.values())-sum(range(n)))%n==0
        assert (sum(len(adj[v])*x for v,x in core.items())+gap-sum(range(n)))%n==0
        colors = [(core[u]+core[v])%n for u,v in kept if u in core and v in core]
        assert len(colors)==len(set(colors)) and gap not in colors
    assert [(pins[u]+pins[v]+shifts.get((u,v),0))%n for u,v in pairs]==extra
    return True


def main():
    rng = Random(271116)
    counts = Counter()
    for n in (420,504,625):
        for k in {d for d in (1,2,3,4,5,7,n//2,n) if n%d==0}:
            r = n//k
            for es,opening,anchor in fixtures(n):
                for mode in range(4):
                    a = rng.randrange(k)
                    hist = [r]*k
                    if opening is None:
                        hist[rng.randrange(k)]-=1
                    if mode>=2 and k>1:
                        for _ in range(min(7,k-1)):
                            origin = rng.choice([x for x in range(k) if hist[x]>0])
                            hist[origin]-=1
                            hist[rng.randrange(k)]+=1
                    offsets = {}
                    if mode%2:
                        offsets = {tuple(sorted(e)):rng.randrange(k) for e in rng.sample(es,5)}
                    passed = audit(n,k,es,opening,anchor,a,hist,offsets,rng)
                    counts["accepted" if passed else "rejected"]+=1
                    if passed and 1<k<n:
                        counts["proper nontrivial quotient"]+=1

    for n in (419,420):
        c=n-2
        es=[(v,(v+1)%c) for v in range(c)]+[(0,c),(c,c+1)]
        shifts={(0,c):11}
        hist=[1]*n
        if n%2:
            hist[0]=hist[2]=0
            hist[1]=3
        else:
            hist[0]=0
            hist[n//2]=2
        for a in (0,7,n-1):
            assert audit(n,n,es,es[0],1,a,hist,shifts,rng)
            counts["forced repeated tail weight"]+=1
    print(dict(counts))


if __name__ == "__main__":
    main()

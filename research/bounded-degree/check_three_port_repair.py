"""Rebuild the targets and compare the actual signed sums of every changed edge."""
from collections import Counter
from math import gcd
from random import Random

from check import adjacency
from check_sparse_ports import star
from three_port_repair import build


def inspect(k,edges,ports,old,removed,high):
    aux,labels,absent,extra,holes = build(edges,ports,old,removed,high)
    active = set(range(k))-{absent}
    assert len(aux)==len(active)-1 and len(set(aux))==len(aux)
    neigh = adjacency(k,aux)
    start = next(iter(active))
    stack,seen = [start],{start}
    while stack:
        v = stack.pop()
        for u in neigh[v]:
            if u not in seen:
                seen.add(u)
                stack.append(u)
    assert seen==active
    S = k*(k-1)//2
    assert set(labels)<=active and len(labels)==len(set(labels.values())) and sum(labels.values())%k==S%k
    if absent is not None:
        assert 0 not in labels.values() and extra in labels.values()
    assert len(holes)==len(set(holes))==1+(absent is not None)
    assert sum(len(neigh[v])*x for v,x in labels.items())%k==(S-sum(holes))%k
    counts = Counter(len(neigh[v]) for v in active)
    marked = Counter(len(neigh[v]) for v in labels)
    for d,total in counts.items():
        assert marked[d]==total or min(marked[d],total-marked[d])>=6
    weights = [(labels[a]+labels[b])%k for a,b in aux if a in labels and b in labels]
    assert len(weights)==len(set(weights)) and set(weights).isdisjoint(holes)
    restored = labels.copy()
    if absent is not None:
        restored[absent] = extra
    original = {tuple(sorted(e)) for e in edges}
    plus = Counter((restored[a]+restored[b])%k for a,b in original-set(aux))
    plus.update((restored[r]+a)%k for r,a in zip(ports,old))
    minus = Counter((restored[a]+restored[b])%k for a,b in set(aux)-original)
    minus.update(w%k for w in removed)
    if absent is None:
        assert plus==minus+Counter([extra])
        assert extra not in high and holes[0] in high
    else:
        assert plus==minus+Counter(holes)


def literal_example():
    k = 11
    # Actual old star, with two copies of every leaf label, centered at zero.
    old = [0]+list(range(k))*2
    edges = [(0,v) for v in range(1,len(old)) if v not in (1,1+k)]
    free = [9,1,2,5,1,10,6,3,4,7,8]
    tree,ports = star(k,[1,1,8],False,-1)
    n = len(old)
    edges.extend((n+a,n+b) for a,b in tree)
    edges.extend((a,n+r) for a,r in zip((0,1,1+k),ports))
    labels = old+free
    assert len(edges)==len(labels)-1
    assert sorted(Counter(labels).values())==[3]*10+[4]
    assert Counter((labels[a]+labels[b])%k for a,b in edges)==Counter({i:3 for i in range(k)})


def main():
    rng = Random(2741991)
    samples = 0
    for k in (251,256,381,512,625,729,1024):
        for t in range(3,10):
            if gcd(k,t-2)!=1:
                continue
            for center_port in (False,True):
                m = t-int(center_port)
                lengths = [1]*(m-1)+[k-m]
                edges,ports = star(k,lengths,center_port,-1)
                for old,removed in [([0]*t,[0]*(t-1)),
                    ([rng.randrange(k) for _ in ports],[rng.randrange(k) for _ in ports[1:]])]:
                    for high in (None,{0},set(range(1,k)),set(rng.sample(range(k),k//2))):
                        inspect(k,edges,ports,old,removed,high)
                        samples += 1
    literal_example()
    print('checked tree targets and changed edge multisets',samples,'complete 11-label example',1)


if __name__=='__main__':
    main()

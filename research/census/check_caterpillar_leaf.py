"""Recount the original caterpillar and spur edges across all order regimes."""

from collections import Counter
from itertools import product
from random import Random

from research.census.caterpillar_leaf import attach, label, staircase


def check(counts,index,k):
    n = len(counts)+sum(counts)+2
    values,case = label(counts,index,k)
    assert set(values)==set(range(n)) and all(0<=x<k for x in values.values())
    edges = [(i,i+1) for i in range(len(counts)-1)]
    v = len(counts)
    for u,count in enumerate(counts):
        edges += [(u,w) for w in range(v,v+count)]
        v += count
    edges += [(index,n-2),(n-2,n-1)]
    for seq in (values.values(),((values[u]+values[w])%k for u,w in edges)):
        freq=Counter(seq)
        row = [freq[i] for i in range(k)]
        assert max(row)-min(row)<=1,(counts,index,k,row)
    return case


def main():
    stats=Counter()
    for s in range(1,6):
        for counts in product(range(3),repeat=s):
            for i in range(s):
                for k in range(1,s+sum(counts)+6):
                    stats[check(counts,i,k)]+=1
    rng=Random(1991)
    for _ in range(1600):
        s=rng.randint(3,100)
        c=[rng.choice([0,0,0,1,2,7,20,70]) for _ in range(s)]
        for k in (8,25,rng.randint(1,s+sum(c)+3)):
            stats[check(c,rng.randrange(s),k)]+=1
    for k in range(3,101):  # Equal arms force the endpoint case.
        stats[check([0]*(2*k-3),k-2,k)]+=1
    total=0
    for counts in [(2,), (0,1,3), (1,3,2,0), (1,0,1), (2,1,1,2,1)]:
        end=len(counts)-1;leaves={};v=len(counts)
        for u,c in enumerate(counts):
            leaves[u]=list(range(v,v+c));v+=c
        spine=list(range(len(counts)))
        _,edges=staircase(spine,leaves)
        t=len(edges)
        for k in range(t,t+8):
            for c in range(k):
                for d in range(k):
                    labels=attach(spine,leaves,end,{end:c},d,k)
                    free=[y for u,y in labels.items() if u!=end]
                    sums=[(labels[u]+labels[w])%k for u,w in edges]
                    assert len(set(free))==len(set(sums))==t and d in sums
                    total+=1
    print("whole trees",dict(sorted(stats.items())),"prescribed tail extensions",total)


if __name__=="__main__":
    main()

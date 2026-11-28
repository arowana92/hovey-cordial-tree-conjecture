"""Verify neutral forest attachments by comparing the exact palette differences."""
from collections import Counter
from functools import reduce
from math import gcd
from random import Random

from check import adjacency
from forest_period import build, lift_boundary


def verify(parents,boundary,result):
    k=len(parents)
    tree,vertices,colors,marks,shift=result
    active={v for edge in tree for v in edge}
    graph=adjacency(k,tree)
    seen,queue={next(iter(active))},[next(iter(active))]
    for v in queue:
        for u in graph[v]-seen:
            seen.add(u)
            queue.append(u)
    assert seen==active and len(tree)+1==len(active)==len(vertices)==len(colors)+1
    assert len(set(marks.values()))==len(marks) and set(marks.values())<=set(range(k))
    on={v:x for v,x in marks.items() if v in active}
    assert set(on.values())<=vertices and (sum(on.values())-sum(vertices))%k==0
    assert (sum(len(graph[v])*x for v,x in on.items())-sum(colors))%k==0
    for d,count in Counter(len(graph[v]) for v in active).items():
        m=sum(len(graph[v])==d for v in on)
        assert m==count or min(m,count-m)>=6
    present=Counter((marks[u]+marks[v])%k for u,v in tree if u in marks and v in marks)
    assert set(present)<=colors and max(present.values(),default=0)<=1
    assert {marks[v] for v in range(k) if v not in active}==set(range(k))-vertices
    # Work in the translated coordinates of the certificate. All original
    # weights created or destroyed at the boundary must be visible on marks.
    actual=Counter()
    for v,p in enumerate(parents):
        if p>=0 and p in marks and v in marks:
            actual[(marks[p]+marks[v])%k]+=1
        elif p<0:
            assert v in marks
            actual[(marks[v]+boundary[v]-shift)%k]+=1
    assert actual==present+Counter(set(range(k))-colors)
    inside={frozenset((p,v)) for v,p in enumerate(parents) if p>=0}
    aux=set(map(frozenset,tree))
    assert all(set(edge)<=set(marks) for edge in inside^aux)


def main():
    rng=Random(26081991)
    yes=no=projected=altered=0
    for k in (420,729,840,1008):
        samples=[]
        for m in (2,3,7):
            spine=k-30
            p=[-1]*m+[v-m for v in range(m,spine)]+[i%3 for i in range(30)]
            samples.append(p)
            p=p[:]
            for v in range(m,k):
                if p[v]==m-1:
                    p[v]=0
            samples.append(p)
        for t in (0,1,6):
            samples.append([-1]*(t+1)+[i-1 for i in range(t+1,k)])
        for split in (2,k//2,k-2):
            samples.append([-1]+list(range(split-1))+[-1]+list(range(split,k-1)))
        samples.append([-1]+list(range(k-2))+[2])
        if k%2==0:
            p=[-1,-1]
            for i in range((k-2)//2):
                p.extend((i,i))
            samples.append(p)
        for p in samples:
            roots=[v for v,u in enumerate(p) if u<0]
            counts=Counter(u for u in p if u>=0)
            g=reduce(gcd,(counts[v] for v in range(k)),k)
            for z in range(5):
                boundary={r:(0 if z==0 else rng.randrange(k)) for r in roots}
                result=build(p,boundary,3,rng)
                if sum(boundary.values())%g:
                    assert result is None
                    no+=1
                else:
                    verify(p,boundary,result)
                    yes+=1
            for low in range(1,k+1):
                if k%low: continue
                boundary={r:rng.randrange(low) for r in roots}
                lifted=lift_boundary(p,boundary,low)
                possible=any((sum(boundary.values())+low*t)%g==0 for t in range(k//low))
                assert (lifted is not None)==possible
                if lifted is None: continue
                assert all(0<=x<k and x%low==boundary[r] for r,x in lifted.items())
                assert sum(lifted.values())%g==0
                assert Counter(x%low for x in range(k))==dict.fromkeys(range(low),k//low)
                projected+=1
                if lifted!=boundary:
                    verify(p,lifted,build(p,lifted,3,rng))
                    altered+=1
    assert altered
    print(yes,"uniform-period targets and",no,"incompatible parent sums")
    print(projected,"projected targets including",altered,"with a changed lift")


if __name__=="__main__":
    main()

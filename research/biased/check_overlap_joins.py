"""Read the policy at sampled actual cores and reconstruct every leaf edge explicitly."""
from argparse import ArgumentParser
from collections import Counter
from mmap import ACCESS_READ, mmap
from pathlib import Path
from random import Random
from struct import Struct

from .check_two_parent_pruning import match

record = Struct('<II27B')


def choice(stream,high,weights,parent):
    u=sum(1 << y for y in high)
    w=sum(1 << z for z in weights)
    lo,hi=0,len(stream)//record.size
    while lo<hi:
        mid=(lo+hi)//2
        x,e,*row=record.unpack_from(stream,mid*record.size)
        if (e,x)<(w,u):
            lo=mid+1
        elif (e,x)>(w,u):
            hi=mid
        else:
            return row[parent]
    return None


def replay(stream,steps,delta,target,rng):
    k=27
    a=rng.randrange(k)
    unit=rng.choice([u for u in range(1,k) if u%3])
    inverse=pow(unit,-1,k)
    b=(a+unit*delta)%k
    edges=[(0,i+1) for i in range(k)]
    vertices=[0]+list(range(k))
    high,weights={0},set()
    for i in range(steps):
        v = len(vertices)-1 if i%3 else rng.randrange(len(vertices))
        p = (vertices[v]-a)*inverse%k
        y = choice(stream,high,weights,p)
        if y is None:
            c = [sum((x+d)%k in weights for x in high) for d in (0,delta)]
            assert min(c)>=target and (not delta or max(c)>target)
            y=next(t for t in range(k) if t not in high and (p+t)%k not in weights)
        assert y not in high and (y+p)%k not in weights
        high.add(y)
        weights.add((y+p)%k)
        edges.append((v,len(vertices)))
        vertices.append(unit*y%k)

    # Obtain the actual forbidden sets by recounting the complete core.
    u={v for v,n in Counter(vertices).items() if n>1}
    w={z for z,n in Counter((vertices[v]+vertices[q])%k for v,q in edges).items() if n>1}
    r=k-2*steps-1+target
    assert len(u)==steps+1 and len(w)==steps
    for number in range(r+1):
        if a==b:
            labels=[(x,1) for x in range(k) if x not in u and (x+a)%k not in w][:r]
        else:
            labels=match(k,a,b,u,w,r-number,number)
        assert labels is not None and len(labels)==r
        vs=vertices[:]
        es=edges[:]
        for x,side in labels:
            es.append((1+(a if side==1 else b),len(vs)))
            vs.append(x)
        assert len(es)==len(vs)-1
        for bins in (Counter(vs),Counter((vs[i]+vs[j])%k for i,j in es)):
            counts=[bins[x] for x in range(k)]
            assert max(counts)-min(counts)<=1
    return r+1


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    args=parser.parse_args()
    rng=Random(27112803)
    total=0
    for steps,target in ((2,1),(4,2),(6,3),(7,3)):
        for delta in (0,1,3,9):
            with (args.directory/f'overlap-{steps}-{target}-{delta}').open('rb') as data:
                with mmap(data.fileno(),0,access=ACCESS_READ) as stream:
                    total+=sum(replay(stream,steps,delta,target,rng) for _ in range(12))
    print('whole-tree leaf joins recounted',total)

"""Assemble actual small-forest grafts from dense-cycle witnesses at 26 and 27."""
from itertools import combinations_with_replacement
from random import Random
from pathlib import Path
from subprocess import check_output
import sys

from .check_near_period import find_path
from .cycle_subdivision import after
from .edge_padding import leaf_packet
from .near_period import prepare


def graft(k,ps,a,b,solver):
    h = len(ps)
    half = k*(k-1)//2%k
    kids = [ps.count(i) for i in range(h)]
    tips = [i for i,c in enumerate(kids) if c==0]
    if h==1:
        x,row = leaf_packet(k,a,b,-1-ps[0])
        return [x],row
    if len(tips)==1 and h==2 and k%2:
        result = prepare(k,[-1,0],[-1-ps[0],0],a,b,(a+b)%k)
        if result is None:
            return None
        f,(prefix,v,z,inside,colors) = result
        return f,prefix+find_path(k,v,z,inside,colors,Random(239+a*k+b))
    target = (half+sum(-1-p for p in ps if p<0))%k
    tip = target if len(tips)==1 else None
    anchor = b if a==tip else a
    enlarged = a==b==tip
    pinned = {}
    if tip is not None:
        pinned[h-1] = tip
    if enlarged:
        parent = -1-ps[0]
        if k%2:
            pinned.update({0:(parent+1)%k,1:(parent-1)%k})
        else:
            pinned[0] = parent
    first,second = tips[-2:] if len(tips)>=2 else (None,None)
    order = [i for i in range(h) if i not in (first,second)]
    if first is not None:
        order.extend([first,second])
    f = [None]*h

    def assign(pos,vs,es):
        if pos==h:
            return True
        i = order[pos]
        p = ps[i]
        parent = f[p] if p>=0 else -1-p
        if i==second:
            candidates = [(target-sum((1-c)*x for c,x in zip(kids,f) if x is not None))%k]
        else:
            candidates = [pinned[i]] if i in pinned else range(k)
        for x in candidates:
            w = (x+parent)%k
            if x in vs or w in es or (x==anchor and not enlarged):
                continue
            if tip is not None and i<h-1 and x==tip:
                continue
            f[i] = x
            if assign(pos+1,vs|{x},es|{w}):
                return True
            f[i] = None
        return False

    assert assign(0,set(),set())
    missing_v = set(f)
    missing_e = {(x+(f[p] if p>=0 else -1-p))%k for x,p in zip(f,ps)}
    if enlarged:
        missing_v.remove(tip)
        missing_e.remove(2*tip%k)
    code = lambda sites: str(sum(1<<i for i in sites))
    cycle = list(map(int,check_output([solver,str(k),str(len(missing_v)),
                                      code(missing_v),code(missing_e)],text=True).split()))
    row = after(cycle,anchor)
    if enlarged:
        return f,row[:-1]
    return f,row if anchor==a else row[::-1]


def recount(k,ps,a,b,f,row):
    assert sorted(f+row)==list(range(k))
    # Select explicit old vertices with the prescribed labels, one per root.
    old = [a,b]+[-p-1 for p in ps if p<0]
    old_edges = [(0,i) for i in range(1,len(old))]
    edges = old_edges[1:]
    port = 2
    for i,p in enumerate(ps):
        if p<0:
            edges.append((port,len(old)+i))
            port += 1
        else:
            edges.append((len(old)+p,len(old)+i))
    labels = old+f+row
    chain = [0]+list(range(len(old)+len(f),len(labels)))+[1]
    edges.extend(zip(chain,chain[1:]))
    def bins(labels,edges):
        v,e = [0]*k,[0]*k
        for x in labels: v[x] += 1
        for u,w in edges: e[(labels[u]+labels[w])%k] += 1
        return v,e
    before = bins(old,old_edges)
    final = bins(labels,edges)
    assert all(y==x+1 for s,t in zip(before,final) for x,y in zip(s,t))


def main():
    solver = str(Path(sys.argv[1]).resolve())
    rng = Random(28112615)
    cases = exceptions = 0
    for a,b in combinations_with_replacement(range(27),2):
        answer = graft(27,[-1,0],a,b,solver)
        if answer is None:
            assert (a+b)%27==0
            exceptions += 1
        else:
            assert (a+b)%27!=0
            recount(27,[-1,0],a,b,*answer)
            cases += 1
    for k in (26,27):
        for h in range(1,7):
            for i in range(30):
                if i%3==0:
                    ps = [-1-rng.randrange(k)]+list(range(h-1))
                elif i%3==1:
                    ps = [-1-rng.randrange(k) for _ in range(h)]
                else:
                    ps = [rng.randrange(-k,j) for j in range(h)]
                a,b = rng.randrange(k),rng.randrange(k)
                if i%6==0:
                    a = b = (-1-ps[0]+k*(k-1)//2)%k
                result = graft(k,ps,a,b,solver)
                if result is None:
                    assert k%2 and ps==[ps[0],0] and (a+b+2*(1+ps[0]))%k==0
                    exceptions += 1
                else:
                    recount(k,ps,a,b,*result)
                    cases += 1
    print('whole tree joins',cases,'normalized or sampled obstructions',exceptions)


if __name__=='__main__':
    main()

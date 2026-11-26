"""An asymmetric integer interval completion for two hubs and long segments."""

from bisect import bisect_right
from random import Random

from research.hub.polynomial_hub import trials
from research.hub.two_hub_contraction import complete, elongate_group, segment_core, remove_fillers
from research.hub.polynomial_two_hubs import complete as polynomial_complete, polynomial_bound
from research.large_order_subdivision import POSITIONS


def stretch_fixed(interval, left, right, target):
    p,q = max(left,right),min(left,right)
    assert p>0>q
    path = [p]
    moves = 0
    while min(-interval.lo,interval.hi)<target or moves%6:
        x,y = interval.stretch(p,q)
        path.extend((x,y))
        p = y
        moves += 1
    path.append(q)
    return (path if left>right else path[::-1]),moves


def insert_neutral(edge, blocks, width, used, minority, rng):
    left,right = edge
    assert left and right and left+right
    prefix,tails = [left],[]
    p,q = left,right
    for _ in range(blocks):
        for u in trials(width,rng):
            v = 4*u
            values = [a*p+b*q+c*u+d*v for a,b,c,d in POSITIONS]
            if len(set(values))==12 and used.isdisjoint(values) and not any(map(minority,values)):
                break
        else:
            raise ValueError("no injective neutral path")
        prefix.append(values[0])
        tails.append(values[1:])
        used.update(values)
        p,q = u,v
    return prefix+[x for tail in reversed(tails) for x in tail]+[right]


def buffered_complete(tree, a, b, *, use_polynomial=False, pins=()):
    """Return a compressed interval witness with few filler leaves at b."""
    compact,other,segments = segment_core(tree,a,b,lambda n:n if n<=20 else 9+(n-9)%12,pins)
    witness = complete(compact,0,other)
    if witness is None:
        assert all(len(full)==len(short) for full,short in segments)
        return None
    base,interval,_ = witness
    extra = [len(full)-len(short) for full,short in segments]
    longest = max(range(len(extra)),key=extra.__getitem__)
    use_polynomial = use_polynomial or interval.hi-interval.lo+1>polynomial_bound(len(compact))
    if use_polynomial:
        short = segments[longest][1]
        base,interval,_ = polynomial_complete(compact,0,other,(short[0],short[-1]))
    h,w = len(tree),interval.hi-interval.lo+1
    cap = 100+6*(2+h+w).bit_length()
    width = 100*(h+(cap+8)*(w+1)+1)
    target = 16*width+4*w
    labeled = [[base[v] for v in short] for _,short in segments]
    moves = neutral = 0
    if extra[longest]<2*cap:
        if use_polynomial:
            full,iv,_ = polynomial_complete(tree,a,b)
            return full,iv,(w,cap,0,0)
        jobs,sites = [],[]
        for i,(row,n) in enumerate(zip(labeled,extra)):
            if n:
                j = next(j for j,(p,q) in enumerate(zip(row,row[1:])) if min(p,q)<=0<max(p,q))
                jobs.append((row[j],row[j+1],n//2))
                sites.append((i,j))
        for (i,j),path in zip(sites,elongate_group(interval,jobs)):
            labeled[i][j:j+2] = path
    else:
        row = labeled[longest]
        j = next(j for j,(p,q) in enumerate(zip(row,row[1:])) if min(p,q)<0<max(p,q))
        path,moves = stretch_fixed(interval,row[j],row[j+1],target)
        assert moves<=cap and moves%6==0
        # Save a different original edge for all remaining subdivisions.
        sites = []
        for i,original in enumerate(labeled):
            if extra[i]:
                u = next(u for u,(p,q) in enumerate(zip(original,original[1:]))
                         if p and q and p+q and (i!=longest or u!=j))
                sites.append((i,u if i!=longest or u<j else u+2*moves))
        row[j:j+2] = path
        extra[longest] -= 2*moves
        used = set(base)|set(path)
        old = used.copy()
        ranges = sorted((a,b) for p,a,b in interval.blocks if p==1)
        starts = [x for x,_ in ranges]
        def minority(x):
            i = bisect_right(starts,x)-1
            return i>=0 and x<ranges[i][1]
        rng = Random(1952)
        for i,j in sites:
            blocks = extra[i]//12
            if blocks:
                row = labeled[i]
                row[j:j+2] = insert_neutral(row[j:j+2],blocks,width,used,minority,rng)
                neutral += blocks
        assert all(interval.lo<=x<=interval.hi for x in used)
        remove_fillers(interval,used-old)
    result = [None]*h
    for (full,_),row in zip(segments,labeled):
        assert len(full)==len(row)
        for v,x in zip(full,row):
            assert result[v] in (None,x)
            result[v] = x
    return result,interval,(w,cap,moves,neutral)

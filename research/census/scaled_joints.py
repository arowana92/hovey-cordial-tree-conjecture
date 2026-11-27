"""Pack independently repeated pairs or triples of branch populations into one interval."""

from itertools import chain
from math import gcd
from functools import reduce


def plan(counts, groups):
    """Center zero has counts[0] children. All other centers are partitioned by groups."""
    m = len(counts)
    if m<3 or min(counts)<1 or sorted(chain.from_iterable(groups))!=list(range(1,m)):
        raise ValueError("expected a partition of the other centers")
    groups = sorted(groups,key=len,reverse=True)
    if len(groups[0])>3 or any(len(g)!=2 for g in groups[1:]) or len(groups[0])<2:
        raise ValueError("use pairs and at most one triple")
    center = {0:0}
    used = {0}
    blocks = []
    waste = 0
    for group in groups:
        ids = sorted(group,key=counts.__getitem__)
        copies = reduce(gcd,(counts[i] for i in ids))
        sizes = [counts[i]//copies for i in ids]
        L = sum(sizes)
        triangle = sizes==[1,1,1]
        if len(ids)==2:
            a,b = sizes
            jumps = [b,-a]
        elif triangle:
            jumps = [1,2,-3]
        else:
            a,b,c = sizes
            jumps = [b+c,c-a,-a-b]
        scale = 1
        while any(scale*j in used for j in jumps):
            scale += 1
        for i,j in zip(ids,jumps):
            center[i] = scale*j
            used.add(scale*j)
        assert not triangle or scale==1
        waste += 1 if triangle else (scale-1)*L
        blocks.append((ids,sizes,jumps,scale,copies))
    reserve = max(used)-min(used)+1-m+waste
    return center,blocks,reserve


def construct(counts,groups,plain,size=None):
    """Return centers and labeled leaves for any requested prefix of size >= m."""
    center,blocks,reserve = plan(counts,groups)
    m = len(counts)
    full = m+sum(counts)+plain
    n = full if size is None else size
    if plain<0 or n<m:
        raise ValueError("expected nonnegative direct count and at least all centers")
    zero = counts[0]+plain+max(0,n-full)
    lengths = [sum(sizes) for ids,sizes,jumps,scale,copies in blocks]
    total = n-m
    if total<=zero:
        labels = list(range(m))
        spare = list(range(m,n))
        keep = min(counts[0],len(spare))
        return [(x,spare[:keep] if x==0 else []) for x in labels],spare[keep:]
    if zero<reserve+(max(lengths) if n<full else 0):
        raise ValueError("insufficient zero-shift capacity for this guarantee")
    moves = [[] for _ in counts]
    lo = min(center.values())
    start = max(center.values())+1
    need = total-zero
    for (ids,sizes,jumps,scale,copies),L in zip(blocks,lengths):
        take = min(copies,max(0,(need+L-1)//L))
        need -= take*L
        if not take:
            continue
        if sizes==[1,1,1]:
            # Three distinct jumps. One triangle uses a hole; pairs and triples of
            # triangles tile their whole interval with these same displacements.
            tables = []
            if take==1:
                tables.append([1,3,2,0])
            else:
                if take%2:
                    tables.append([2,3,4,0,1,6,7,8,5])
                tables.extend([[1,3,4,0,5,2]]*((take-3*(take%2))//2))
            for table in tables:
                for x,y in enumerate(table):
                    if x!=y:
                        moves[ids[jumps.index(y-x)]].append(start+x)
                start += len(table)
        else:
            pattern = list(chain.from_iterable([i]*a for i,a in zip(ids,sizes)))
            while take:
                lanes = min(scale,take)
                for lane in range(lanes):
                    for x,i in enumerate(pattern):
                        moves[i].append(start+scale*x+lane)
                start += scale*L
                take -= lanes
    assert need<=0 and start<=lo+n
    occupied = set(center.values()).union(*moves)
    spare = [z for z in range(lo,lo+n) if z not in occupied]
    keep = min(len(spare),counts[0])
    moves[0] = spare[:keep]
    return [(center[i],vs) for i,vs in enumerate(moves)],spare[keep:]

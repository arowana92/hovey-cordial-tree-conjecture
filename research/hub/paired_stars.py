"""Exact sparse repair using two pendant stars apiece at distinct vertices."""

from itertools import chain
from random import Random

from research.hub.modular_injection import candidates
from research.hub.pendant_repair import finish_leaves, prepare
from research.hub.star_repair import erasures


def root_values(a,q,c,h,d):
    roots = [d,d+a,d-c,-d-a-h-q,-d-a-q]
    tips = [-2*d-2*a-h-q,d+a+q,-d-a,2*d+a+q-c]
    return roots,tips


def select_anchors(pool,labels,s,t,gap,k):
    def take(excluded):
        forbidden = {x % k for x in excluded}
        for v in pool:
            if labels[v] not in forbidden:
                pool.remove(v)
                return v
        raise ValueError("insufficient distinct boundary labels")

    a = take((0,t,-s,-gap))
    x = labels[a]
    q = take((0,-x,t-x,-x-s,-x-gap))
    y = labels[q]
    c = take((0,-x,-x-y,-t))
    h = take((0,-y,-x-y-s,-x-y-gap))
    return a,q,c,h


def offsets(roots,jumps,k,rng):
    residual,cycles,end = erasures(roots,jumps,0,k)
    row = dict(residual)
    used = set(row.values())|{end}
    for cycle in cycles:
        for shift in candidates(k,rng):
            placed = [(v,(x+shift) % k) for v,x in cycle]
            if all(x not in used for _,x in placed):
                row.update(placed)
                used.update(x for _,x in placed)
                break
        else:
            raise ValueError("no translate for an auxiliary root cycle")
    return row,end,len(cycles)


def repair(parents,stars,arities,roles,extra,labels,blocked,s,t,gap,k,rng):
    groups = []
    auxiliary = [root for v in extra for root in stars[v]]
    for a,q,c,h in roles:
        roots = [stars[a][1],stars[q][1],stars[c][1],stars[h][0],stars[q][0]]
        auxiliary.extend([stars[a][0],stars[c][0],stars[h][1]])
        filled = [r+1 for r in roots[1:]]
        groups.append((tuple(labels[v] for v in (a,q,c,h)),roots,filled))
    extra_offsets,total,cycles = offsets(auxiliary,{r:labels[parents[r]] for r in auxiliary},k,rng)
    tips = []
    for _,roots,_ in groups:
        tips.append([v for i,r in enumerate(roots) for v in range(r+1+(i!=0),r+1+arities[r])])
    primary = [row[0] for row in tips[:4]]
    backward = ([tips[4][0],tips[5][0]]+tips[4][1:]+tips[5][1:]
                +[v for row in tips[:4] for v in row[1:]]
                +[v for r in auxiliary for v in range(r+1,r+1+arities[r])])
    radix = 12*(len(backward)+30)
    scales = [pow(radix,i,k) for i in range(5)]
    samples = ([rng.randrange(k) for _ in range(5)] for _ in range(min(k,2048)))
    line = ([w*z % k for w in scales] for z in candidates(k,rng))
    for a,b,c,u,v in chain(samples,line):
        shifts = (a,b,c,s-t-total-a-b-c,u,v)
        row = {r:(t+a+b+offset) % k for r,offset in extra_offsets.items()}
        for (boundary,roots,filled),shift in zip(groups,shifts):
            xs,ys = root_values(*boundary,shift)
            row.update((w,x % k) for w,x in zip(roots+filled,xs+ys))
        row.update(zip(primary,[t,(t+a) % k,(t+a+b+total) % k,(s-shifts[3]) % k]))
        used = set(row.values())
        if len(used) != len(row) or not blocked.isdisjoint(used-{t}):
            continue
        jumps = {w:row[parents[w]] for w in backward}
        new_gap = (gap-sum(jumps.values())) % k
        if new_gap in blocked or new_gap in used or new_gap == gap:
            continue
        residual,loops,end = erasures(backward[::-1],jumps,new_gap,k)
        assert end == gap
        if any(x in blocked or x in used for _,x in residual):
            continue
        row.update(residual)
        occupied = blocked | set(row.values())
        for loop in loops:
            for shift in candidates(k,rng):
                placed = [(w,(x+shift) % k) for w,x in loop]
                if all(x not in occupied for _,x in placed):
                    row.update(placed)
                    occupied.update(x for _,x in placed)
                    break
            else:
                break
        else:
            blocked.update(row.values())
            labels.update(row)
            return new_gap,cycles,len(loops)
    raise ValueError("no specialization for the distributed repair")


def construct(core,counts,anchors,m,n,k,palette,seed=381):
    """Append an m-leaf and an n-leaf star at each listed vertex and restore direct leaves."""
    if (len(anchors) < 32 or (len(anchors)-8) % 24 or len(set(anchors)) != len(anchors)
            or not 1 <= m <= n or counts[0] != max(counts.values())
            or len(core)+sum(counts.values())+len(anchors)*(2+m+n) != k):
        raise ValueError("incompatible tree size or pair count")
    rng = Random(seed)
    labels,bills,blocked,leaves,stats = prepare(core,counts,k,palette,rng)
    jobs = (len(anchors)-8)//24
    if jobs < len(bills):
        raise ValueError(f"the preparation produced {len(bills)} errors for {jobs} repairs")
    parents = list(core)
    stars = {}
    arities = {}
    for v in anchors:
        roots = []
        for size in (m,n):
            root = len(parents)
            roots.append(root)
            arities[root] = size
            parents.extend([v]+[root]*size)
        stars[v] = roots
    pool = list(anchors)
    gap = 0
    for i in range(jobs):
        if i < len(bills):
            s,t = bills[i]
            stats['repairs'] += 1
        else:
            s = t = next(x for x in candidates(k,rng) if x not in blocked)
            stats['neutral'] += 1
        roles = [select_anchors(pool,labels,s,t,gap,k) for _ in range(6)]
        extra = pool if i == jobs-1 else []
        gap,first,last = repair(parents,stars,arities,roles,extra,labels,blocked,s,t,gap,k,rng)
        stats['root cycles'] += first
        stats['leaf cycles'] += last
    parents,values = finish_leaves(parents,labels,leaves,counts,k)
    return parents,values,gap,dict(stats)

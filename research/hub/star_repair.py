"""Absorb a prescribed weight difference using repeated pendant stars."""

from itertools import chain
from random import Random

from research.hub.modular_injection import candidates
from research.hub.pendant_repair import finish_leaves, prepare


def five_roots(p,d):
    """Five root labels and the four filled child slots (root zero's slot stays open)."""
    return [d,d+p,d-p,-d-3*p,-d-2*p],[-2*d-4*p,d+2*p,-d-p,2*d+p]


def erasures(steps,jumps,start,k):
    positions = [start]
    where = {start:0}
    edges = []
    cycles = []
    for v in steps:
        tail = positions[-1]
        head = (tail+jumps[v]) % k
        edges.append((v,tail))
        if head in where:
            j = where[head]
            cycles.append(edges[j:])
            del edges[j:]
            for x in positions[j+1:]:
                del where[x]
            del positions[j+1:]
        else:
            where[head] = len(positions)
            positions.append(head)
    return edges,cycles,positions[-1]


def alternating(left,right):
    return [v for pair in zip(left,right) for v in pair]


def group_layout(p,m):
    """Local vertex IDs in root, then m children order on each pendant star."""
    groups = []
    parents = []
    for _ in range(5):
        roots,filled,open_leaves = [],[],[]
        for j in range(5 if p else 1):
            r = len(parents)
            roots.append(r)
            parents.extend([-1]+[r]*m)
            tips = list(range(r+1,r+m+1))
            if j:
                filled.append(tips.pop(0))
            open_leaves.extend(tips)
        groups.append((roots,filled,open_leaves))
    lists = [group[2] for group in groups]
    primary = [row[0] for row in lists[:3]]
    backward = alternating(lists[3],lists[4])+[v for row in lists[:3] for v in row[1:]]
    return parents,groups,primary,backward


def repair(p,m,s,t,gap,k,blocked,rng):
    parents,groups,primary,backward = group_layout(p,m)
    radix = 24*m+17
    scales = [pow(radix,i,k) for i in range(4)]
    samples = ([rng.randrange(k) for _ in range(4)] for _ in range(min(k,2048)))
    line = ([v*z % k for v in scales] for z in candidates(k,rng))
    for a,b,c,d in chain(samples,line):
        shifts = [a,b,(s-t-a-b) % k,c,d]
        row = {}
        jumps = {}
        for (roots,filled,open_leaves),shift in zip(groups,shifts):
            xs,ys = five_roots(p,shift) if p else ([shift],[])
            row.update((v,x % k) for v,x in zip(roots+filled,xs+ys))
            jumps.update((v,row[parents[v]]) for v in open_leaves)
        distinguished = [t,(t+a) % k,(t+a+b) % k]
        row.update(zip(primary,distinguished))
        used = set(row.values())
        if len(used) != len(row) or not blocked.isdisjoint(used-{t}):
            continue
        next_gap = (gap-sum(jumps[v] for v in backward)) % k
        if next_gap == gap or next_gap in blocked or next_gap in used:
            continue
        # Read the backward construction in forward order for cycle erasure.
        residual,cycles,end = erasures(backward[::-1],jumps,next_gap,k)
        assert end == gap
        if any(x in used or x in blocked for _,x in residual):
            continue
        row.update(residual)
        occupied = blocked | set(row.values())
        for cycle in cycles:
            for shift in candidates(k,rng):
                translated = [(v,(x+shift) % k) for v,x in cycle]
                if all(x not in occupied for _,x in translated):
                    row.update(translated)
                    occupied.update(x for _,x in translated)
                    break
            else:
                break
        else:
            blocked.update(row.values())
            return parents,[row[i] for i in range(len(parents))],next_gap,len(cycles)
    raise ValueError("no disjoint placement for the five groups")


def construct(core,counts,anchor,m,number,k,palette,seed=112):
    """Append number copies of an m-leaf star at the given marked vertex."""
    if (m < 1 or number <= 0 or number % 25 or anchor not in counts
            or counts[0] != max(counts.values()) or len(core)+sum(counts.values())+number*(m+1) != k):
        raise ValueError("incompatible star count, modulus, leaf populations or order")
    rng = Random(seed)
    labels,bills,blocked,leaves,stats = prepare(core,counts,k,palette,rng,guard_digits=True)
    parents = list(core)
    p = labels[anchor]
    step = 25 if p else 5
    gap = 0
    if step*len(bills) > number:
        raise ValueError(f"these errors need {step*len(bills)} pendant stars")
    for i in range(number//step):
        if i < len(bills):
            s,t = bills[i]
            stats['repairs'] += 1
        else:
            t = next(x for x in candidates(k,rng) if x not in blocked)
            s = t
            stats['neutral'] += 1
        local,values,gap,cycles = repair(p,m,s,t,gap,k,blocked,rng)
        offset = len(parents)
        parents.extend(anchor if u < 0 else offset+u for u in local)
        labels.update(enumerate(values,offset))
        stats['erased cycles'] += cycles
    parents,values = finish_leaves(parents,labels,leaves,counts,k)
    return parents,values,gap,dict(stats)

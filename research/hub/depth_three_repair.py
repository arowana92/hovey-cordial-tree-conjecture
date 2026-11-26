"""Repair with branches consisting of two successive supports and their leaves."""

from itertools import chain
from random import Random

from research.hub.modular_injection import candidates
from research.hub.pendant_repair import finish_leaves, prepare
from research.hub.star_repair import close_leaf_walk


def triple_rows(a,b,c,d):
    return ((d-a,d), (d-a-b,2*d-a,-4*d+2*a-c),
            (-2*d+a-c,-2*d+a,3*d-2*a-b))


def double_rows(multiplier,d):
    x = multiplier*d
    return ((x,d),(-2*x-d,x+d,-x))


def split_triple(pool,labels,t,k,first):
    if first:
        a = next(v for v in pool if labels[v] and (t+labels[v]) % k)
        pool.remove(a)
        b = next(v for v in pool if (labels[a]+labels[v]) % k
                 and (t+labels[a]+labels[v]) % k)
        pool.remove(b)
        return (a,b,pool.pop())
    group = [pool.pop() for _ in range(3)]
    for j in (1,2):
        if (labels[group[0]]+labels[group[j]]) % k:
            group[1],group[j] = group[j],group[1]
            return tuple(group)
    raise ValueError("no nonopposite pair in the triple")


def repair(parents,clusters,shape,s,t,gap,k,labels,blocked,rng):
    l,m = shape
    zero = len(clusters[0]) == 2
    multiplier = (2*m+10)*(1 if m-1 >= l else -1)
    slopes = double_rows(multiplier,1) if zero else triple_rows(0,0,0,1)
    data = []
    for cluster in clusters:
        fixed = [labels[parents[root]] for root in cluster]
        ids,positive,negative = [],[],[]
        for i,root in enumerate(cluster):
            second = root+1
            ids.extend([root,second])
            if i:
                ids.append(second+1)
            for j,children in ((0,range(second+1+m,second+1+m+l)),
                               (1,range(second+1+(i!=0),second+1+m))):
                target = positive if slopes[i][j]>0 else negative
                target.extend(children)
        distinguished = cluster[0]+2
        positive.remove(distinguished)
        data.append((fixed,ids,[distinguished]+positive+negative))
    primary = [entry[2][0] for entry in data[:3]]
    tips = [entry[2] for entry in data]
    backward = [tips[3][0],tips[4][0]]+tips[3][1:]+tips[4][1:]+[v for row in tips[:3] for v in row[1:]]
    radix = 12*(len(backward)+9)*(abs(multiplier)+5)
    scales = [pow(radix,i,k) for i in range(4)]
    samples = ([rng.randrange(k) for _ in range(4)] for _ in range(min(k,2048)))
    line = ([w*z % k for w in scales] for z in candidates(k,rng))
    for a,b,u,v in chain(samples,line):
        row = {}
        for (fixed,ids,_),d in zip(data,(a,b,s-t-a-b,u,v)):
            groups = double_rows(multiplier,d) if zero else triple_rows(*fixed,d)
            row.update(zip(ids,(x % k for group in groups for x in group)))
        row.update(zip(primary,(t,(t+a) % k,(t+a+b) % k)))
        occupied = set(row.values())
        if len(occupied) != len(row) or not blocked.isdisjoint(occupied-{t}):
            continue
        result = close_leaf_walk(row,backward,parents,gap,k,blocked,rng)
        if result is not None:
            labels.update(row)
            return result
    raise ValueError("no placement for the depth-three repair")


def construct(core,counts,suppliers,l,m,k,palette,seed=594):
    """Append one branch per supplier occurrence, using distinct sites or one common site."""
    common = len(set(suppliers)) == 1
    if (not suppliers or l < 0 or m < 1 or counts[0]!=max(counts.values())
            or (common and suppliers[0] not in counts)
            or (not common and (0 in suppliers or len(set(suppliers))!=len(suppliers)))
            or len(core)+sum(counts.values())+len(suppliers)*(2+m+l)!=k):
        raise ValueError("invalid branch profile, suppliers or tree order")
    rng = Random(seed)
    labels,bills,blocked,leaves,stats = prepare(core,counts,k,palette,rng,guard_digits=common)
    parents = list(core)
    zero = common and labels[suppliers[0]] == 0
    width = 2 if zero else 3
    if len(suppliers) % (5*width) or len(suppliers) < len(bills)*5*width:
        raise ValueError(f"need complete packets for {len(bills)} errors")
    roots = []
    for v in suppliers:
        r = len(parents)
        roots.append(r)
        parents.extend([v,r]+[r+1]*m+[r]*l)
    boundary = dict(zip(roots,(labels[v] for v in suppliers)))
    gap = 0
    for i in range(len(suppliers)//(5*width)):
        if i < len(bills):
            s,t = bills[i]
            stats['repairs'] += 1
        else:
            s = t = next(x for x in candidates(k,rng) if x not in blocked)
            stats['neutral'] += 1
        clusters = []
        for j in range(5):
            if common:
                group = [roots.pop() for _ in range(width)]
            else:
                group = split_triple(roots,boundary,t,k,j==0)
            clusters.append(group)
        gap,num = repair(parents,clusters,(l,m),s,t,gap,k,labels,blocked,rng)
        stats['cycles'] += num
    parents,values = finish_leaves(parents,labels,leaves,counts,k)
    return parents,values,gap,dict(stats)

"""Mixed-arity depth-three repairs for arbitrary sparse rooted trees."""

from itertools import chain, permutations, product
from math import gcd
from random import Random

from research.hub.depth_three_repair import double_rows, triple_rows
from research.hub.modular_injection import candidates
from research.hub.seven_errors import prepare
from research.hub.star_repair import close_leaf_walk


def signed_total(profiles,j=None):
    if j is None:
        (l,m),(u,n),(v,w) = profiles
        return l+u-2*v+m+2*(n-1)-2*(w-1)
    (l,m),(u,n) = profiles
    return m+j*l+(-2*j-1)*u+(j+1)*(n-1)


def guard(roots,shapes):
    if len(roots)==2:
        j = 4 if sum(shapes[r][1]-1-shapes[r][0] for r in roots)>=0 else -4
    else:
        j = None
    for order in permutations(roots):
        if signed_total([shapes[r] for r in order],j)>0:
            return order,j
    raise AssertionError("no positive guard permutation")


def guard_split(steps,k):
    """Latest prefix whose coordinate has gcd at most the largest step size."""
    bound = max(map(abs,steps))
    total = 0
    split = 0
    for i,s in enumerate(steps,1):
        total += s
        if total and gcd(total,k)<=bound:
            split = i
    if not split:
        raise ValueError("guard has no usable first jump")
    return split


def layout(roots,shapes,parents,labels,j):
    slopes = double_rows(j,1) if j is not None else triple_rows(0,0,0,1)
    ids,positive,negative = [],[],[]
    coefficients = {}
    for i,r in enumerate(roots):
        l,m = shapes[r]
        ids.extend((r,r+1))
        if i:
            ids.append(r+2)
        for s,leaves in ((slopes[i][0],range(r+2+m,r+2+m+l)),
                         (slopes[i][1],range(r+2+(i!=0),r+2+m))):
            (positive if s>0 else negative).extend(leaves)
            coefficients.update((leaf,s) for leaf in leaves)
    first = roots[0]+2
    positive.remove(first)
    sequence = [first]+positive+negative
    return [labels[parents[r]] for r in roots],ids,j,sequence,[coefficients[v] for v in sequence]


def packet(clusters,shapes,parents,labels,blocked,b,t,gap,k,rng):
    rows = []
    for i,cl in enumerate(clusters):
        roots,j = guard(cl,shapes) if i>=3 else (cl,4 if len(cl)==2 else None)
        rows.append(layout(roots,shapes,parents,labels,j))
    lists = [entry[3] for entry in rows]
    primary = [seq[0] for seq in lists[:3]]
    first,second = lists[3:]
    cut = guard_split(rows[3][4],k)
    backward = ([first[0],second[0]]+[v for seq in lists[:3] for v in seq[1:]]
                +first[1:cut]+second[1:]+first[cut:])
    samples = ([rng.randrange(k) for _ in range(4)] for _ in range(2048))
    for a,c,u,v in chain(samples,product(range(k),repeat=4)):
        row = {}
        for (fixed,ids,j,_,_),d in zip(rows,(a,c,b-t-a-c,u,v)):
            values = triple_rows(*fixed,d) if j is None else double_rows(j,d)
            row.update(zip(ids,(x%k for group in values for x in group)))
        row.update(zip(primary,(t,(t+a)%k,(t+a+c)%k)))
        used = set(row.values())
        if len(used)!=len(row) or not blocked.isdisjoint(used-{t}):
            continue
        result = close_leaf_walk(row,backward,parents,gap,k,blocked,rng)
        if result is not None:
            labels.update(row)
            return result
    raise ValueError("no independent parameter choice for the mixed repair")


def allocate(roots,labels,parents,targets,k,common):
    width = 2 if common and labels[parents[roots[0]]]==0 else 3
    jobs = [[None]*5 for _ in targets]
    pool = list(roots)
    if len(pool)!=5*width*len(jobs):
        raise ValueError("incorrect number of saved branches")
    if common:
        return [[tuple(pool.pop() for _ in range(width)) for _ in range(5)] for _ in jobs]

    def take(excluded):
        excluded = {x%k for x in excluded}
        v = next(v for v in pool if labels[parents[v]] not in excluded)
        pool.remove(v)
        return v
    for job in jobs:
        for i in (3,4):
            group = []
            for _ in range(3):
                group.append(take([-labels[parents[r]] for r in group]))
            job[i] = group
    for job,t in zip(jobs,targets):
        a = take([-t])
        x = labels[parents[a]]
        job[0] = (a,take([-x,-x-t]),pool.pop())
    for job in jobs:
        for i in (1,2):
            group = [pool.pop() for _ in range(3)]
            a,b,c = group
            if (labels[parents[a]]+labels[parents[b]])%k==0:
                group = [a,c,b]
            job[i] = group
    return jobs


def construct(core,branches,k,seed=902):
    """Each supplied branch is (parent, extra leaves at first, leaves at second)."""
    rng = Random(seed)
    labels,bills,blocked,_ = prepare(core,k,rng,guard_multiples=True)
    parents,shapes = list(core),{}
    sites = {p for p,_,_ in branches}
    common = len(sites)==1
    if not common and (len(sites)!=len(branches) or 0 in sites):
        raise ValueError("expected distinct nonroot boundary vertices or one common parent")
    width = 2 if sites=={0} else 3
    if len(branches)%(5*width) or len(branches)//(5*width)<len(bills):
        raise ValueError("insufficient complete groups for the error list")
    for p,l,m in branches:
        if l<0 or m<1:
            raise ValueError("invalid branch shape")
        r = len(parents)
        shapes[r] = l,m
        parents.extend([p,r]+[r+1]*m+[r]*l)
    errors = list(bills)
    for _ in range(len(branches)//(5*width)-len(errors)):
        t = next(x for x in candidates(k,rng)
                 if x not in blocked and all((x+j*labels[p])%k for p in sites for j in (1,2))
                 and all((x-2*labels[p])%k for p in sites))
        blocked.add(t)
        errors.append((t,t))
    groups = allocate(list(shapes),labels,parents,[t for _,t in errors],k,common)
    gap = cycles = 0
    for (b,t),cl in zip(errors,groups):
        gap,l = packet(cl,shapes,parents,labels,blocked,b,t,gap,k,rng)
        cycles += l
    return parents,[labels[v] for v in range(len(parents))],gap,len(bills),cycles

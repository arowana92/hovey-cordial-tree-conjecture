"""Prefix-cordial growth from a divisible core across two prescribed stars."""
from math import gcd

from research.eight.surplus_grafts import star
from research.large_order_hall_pools import hall_pair


def second_star(k,children,singles,boundary):
    """The first center has just filled the deficit and is translated to zero."""
    if children==0:
        y = (-boundary)%k or 1
        return y,[],sorted(set(range(1,k))-{y})[:singles]
    if children+singles==k-2 or boundary==0:
        y,kids,other = star(k,children,boundary)
        return y,kids,other[:singles]
    y = (-boundary)%k
    classes = gcd(k,y)
    period = k//classes
    kids = []
    for r in range(1,classes):
        take = min(period,children-len(kids))
        kids.extend((r+i*y)%k for i in range(take))
        if len(kids)==children:
            break
    take = children-len(kids)
    kids.extend(((i+2)*y)%k for i in range(take))
    available = set(range(1,k))-{y}-set(kids)-{(v+y)%k for v in kids}
    assert len(available)>=singles
    return y,kids,sorted(available)[:singles]


def grow(k,s,t,a,b,deficit):
    """Return ordered (star number, label) pairs, or None. First occurrence is its center."""
    if k<2 or min(s,t)<1:
        raise ValueError('use a modulus at least two and two nonempty stars')
    if s+t>=k:
        left = next((j for j in range(max(1,k-t),min(k-1,s)+1)
                     if (a+b-deficit)%gcd(j,k)==0),None)
        if left is None:
            return None
        right = k-left
    else:
        left,right = s,t
    x = (deficit-a)%k
    y,kids,singles = second_star(k,right-1,left-1,(b-x)%k)
    first = [(0,0),(1,y)]+[(1,z) for z in kids]+[(0,z) for z in singles]
    result = [(i,(z+x)%k) for i,z in first]
    centers = [x,(x+y)%k]
    pending = [0]*(s-left)+[1]*(t-right)
    if not pending:
        return result
    used = {(centers[1]+b)%k} | {(x+z+x)%k for z in singles} | {
        (centers[1]+z+x)%k for z in kids}
    gap, = set(range(k))-used
    for start in range(0,len(pending),k):
        group = pending[start:start+k]
        first_side = group[0]
        surplus = (gap-centers[first_side])%k
        result.append((first_side,surplus))
        shifts = [centers[side] for side in group[1:]]
        padding = shifts+[(-sum(shifts))%k]+[0]*(k-1-len(shifts))
        source = [(-u)%k for u,_ in hall_pair(padding)]
        offset = surplus-source[len(shifts)]
        fresh = [(v+offset)%k for v in source[:len(shifts)]]
        result.extend(zip(group[1:],fresh))
        if len(group)==k:
            gap, = set(range(k))-{(v+w)%k for v,w in zip(fresh,shifts)}
    return result

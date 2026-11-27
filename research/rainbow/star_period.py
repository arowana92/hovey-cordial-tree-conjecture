"""Compressed counts for a star and equal-parent singleton leaves over whole periods."""
from math import gcd

from research.large_order_hall_pools import hall_pair, zero_block


def cyclic(k,q,c,p,b,a):
    """Return child and singleton count vectors, or None, for a prescribed center."""
    if k<1 or q<1 or not 0<=c<q*k:
        raise ValueError("the center and children must fit")
    a,b,p = a%k,b%k,p%k
    d = (a-b)%k
    surplus = (b-p-c*d)%k
    rhs = [0]*k
    for i,z in ((0,1),(a,1),(surplus,-1),((p+d)%k,-1)):
        rhs[i] += z
    children = [0]*k
    cosets = []
    g = gcd(d,k)
    h = k//g
    for root in range(g):
        sites = [(root+j*d)%k for j in range(h)]
        base = 0
        for i in sites:
            base -= rhs[i]
            children[i] = base
        if base:
            return None
        lower = -min(children[i] for i in sites)
        upper = min(q-int(i==p)-children[i] for i in sites)
        if upper<lower:
            return None
        for i in sites:
            children[i] += lower
        cosets.append((sites,upper-lower))
    layers,remainder = divmod(c-sum(children),h)
    if remainder or layers<0 or layers>sum(cap for _,cap in cosets):
        return None
    for sites,cap in cosets:
        take = min(layers,cap)
        for i in sites:
            children[i] += take
        layers -= take
    singletons = [q-int(i==(p+d)%k)-children[(i-d)%k] for i in range(k)]
    return children,singletons,surplus


def arbitrary(k,shifts,center,children):
    """Use either congruence with arbitrary edge offsets and singleton-parent colors.

    The input shifts include the old parent plus offset for externally attached
    rows, and just the edge offset for center children. The old surplus is zero.
    """
    n = len(shifts)
    if n%k or not n or center in children:
        raise ValueError("need whole periods and an external center")
    c = len(children)
    total = sum(shifts)
    for move in (False,True):
        for a in range(k):
            if ((c+int(move))*a+total)%k:
                continue
            delta = [(b+(a if i in children else 0))%k for i,b in enumerate(shifts)]
            if move:
                delta[center] = (delta[center]+a)%k
            # Each zero-sum Hall layer can be translated, so the distinguished
            # row can receive its prescribed source even when it occurs once.
            pending = {}
            for i,x in enumerate(delta):
                pending.setdefault(x,[]).append(i)
            left = n
            f = [None]*n
            while left:
                block = zero_block([len(pending.get(x,[])) for x in range(k)])
                sites = [pending[x].pop() for x in block]
                pair = hall_pair(block)
                sources = [-x%k for x,_ in pair]
                shift = 0
                if center in sites:
                    shift = ((0 if move else a)-sources[sites.index(center)])%k
                for i,x in zip(sites,sources):
                    f[i] = (x+shift)%k
                left -= k
            f[center] = a
            return f
    return None

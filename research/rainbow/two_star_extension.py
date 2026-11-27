"""Ordinary fixed-core extensions by two stars at any cyclic modulus."""
from math import gcd

from .two_star_growth import grow, leaf_suffix


def groups(order):
    return [[x for side,x in order if side==i] for i in (0,1)]


def shift(block,offset,k):
    return [[(x+offset)%k for x in side] for side in block]


def from_leaves(k,x,y,first_leaves):
    occupied = {x,y}|set(first_leaves)
    return [[x]+sorted(first_leaves),[y]+sorted(set(range(k))-occupied)]


def unit_packet(k,s,q):
    """Parents 0,q, deficit q+1. The discrepancy generates the group."""
    t = k-s
    if min(s,t)==1:
        return groups(grow(k,s,t,0,q,(q+1)%k))
    if q==0:
        return from_leaves(k,k-1,0,range(2,s+1))
    if q==1:
        return from_leaves(k,k-1,0,{1}|set(range(3,s+1)))
    if q<=k-s+1:
        return from_leaves(k,1,0,{q}|set(range(k-s+2,k)))
    # In the opposite orientation the preceding cases cover this q.
    reversed_block = unit_packet(k,t,(-q)%k)
    return shift(reversed_block,q,k)[::-1]


def lifted_packet(k,s,q,delta,m,size):
    """Use m blocks in the cyclic subgroup of the given size."""
    width = size//m
    index = k//size
    mass = (s%size)//width
    q_coordinate = next(i for i in range(m) if i*delta%k==q)
    if q_coordinate>m-mass:
        opposite = lifted_packet(k,k-s,(-q)%k,delta,m,size)
        return shift(opposite,q,k)[::-1]
    if q_coordinate:
        target = delta
        marked = (1-mass)%m
        blocks = {q_coordinate}|set(range(m-mass+1,m))
    else:
        target = -delta
        marked = (-1-mass)%m
        blocks = set(range(m-mass-1,m-1))
    step = next(index*u for u in range(1,size) if gcd(u,size)==1
                and (width*index*u-target)%k==0)
    leaves = {width*i+j for i in blocks for j in range(width)}
    leaves.remove(width*marked)
    local = from_leaves(size,1,0,leaves)
    block = [[v*step%k for v in side] for side in local]
    for r in range(1,index):
        side = 0 if r<=s//size else 1
        block[side].extend(range(r,k,index))
    return block


def integral_packet(k,s,q,delta):
    """Set the second center to zero and integrate the required indicator."""
    for h in range(1,k):
        # B shifted by h, minus B, has this prescribed signed histogram.
        gap = (delta-(s-1)*h)%k
        rhs = [0]*k
        for x in (0,(q+delta)%k):
            rhs[x] += 1
        for x in (q,gap):
            rhs[x] -= 1
        orbit_count = gcd(k,h)
        period = k//orbit_count
        needed = s-1
        chosen = []
        flexible = []
        for r in range(orbit_count):
            orbit = [(r+j*h)%k for j in range(period)]
            values = []
            current = 0
            for i in orbit:
                current -= rhs[i]
                values.append(current)
            low,high = -min(values),1-max(values)
            if r==0:
                for i in (0,h):
                    fixed = -values[orbit.index(i)]
                    low,high = max(low,fixed),min(high,fixed)
            if current or low>high:
                break
            chosen.extend(i for i,v in zip(orbit,values) if v+low)
            if low<high:
                flexible.append(orbit)
        else:
            extra = needed-len(chosen)
            if 0<=extra<=period*len(flexible) and extra%period==0:
                chosen.extend(i for orbit in flexible[:extra//period] for i in orbit)
                return from_leaves(k,h,0,chosen)
    return None


def packet(k,s,a,b,d):
    """Construct the full k-vertex packet, or certify its impossibility."""
    t = k-s
    if (a+b-d)%gcd(s,k)==0:
        return groups(grow(k,s,t,a,b,d))
    if s>t:
        block = packet(k,t,b,a,d)
        return None if block is None else block[::-1]

    delta = (d-a-b)%k
    q = (b-a)%k
    index = gcd(k,delta)
    period = k//index
    if q%index:
        # One leaf goes in q's coset. The negative segment closes inside H.
        whole,remainder = divmod(s-2,period)
        available = [r for r in range(1,index) if r!=q%index]
        assert remainder<=period-2 and whole<=len(available)
        leaves = {q}|{(-i*delta)%k for i in range(1,remainder+1)}
        leaves.update((r+j*delta)%k for r in available[:whole] for j in range(period))
        return shift(from_leaves(k,delta,0,leaves),a,k)

    if s%period:
        # Solve inside the subgroup, then put complete outside cosets at the centers.
        coordinate = q//index*pow(delta//index,-1,period)%period
        short = unit_packet(period,s%period,coordinate)
        block = [[(v*delta)%k for v in side] for side in short]
        for r in range(1,index):
            side = 0 if r<=s//period else 1
            block[side].extend(range(r,k,index))
        return shift(block,a,k)

    for size in range(2*period,k+1,period):
        width = size//period
        if k%size==0 and s%width==0 and 2<=(s%size)//width<=period-2:
            return shift(lifted_packet(k,s,q,delta,period,size),a,k)

    block = integral_packet(k,s,q,delta)
    if block is not None:
        return shift(block,a,k)
    block = integral_packet(k,t,(-q)%k,delta)
    return None if block is None else shift(block,b,k)[::-1]


def extend(k,s,t,a,b,d):
    """The two returned lists give centers first, followed by their leaf labels."""
    if k<2 or min(s,t)<1:
        raise ValueError('use a modulus at least two and two nonempty stars')
    if s+t<k:
        return groups(grow(k,s,t,a,b,d))
    low,high = max(1,k-t),min(s,k-1)
    delta = (d-a-b)%k
    period = k//gcd(k,delta)
    left = next((j for j in range(low,high+1) if j%period),low)
    block = packet(k,left,a,b,d)
    if block is None or s+t==k:
        assert block is not None or s+t==k
        return block
    centers = [side[0] for side in block]
    counts = [1-int(i==d%k) for i in range(k)]
    for side,p in zip(block,(a,b)):
        counts[(p+side[0])%k] += 1
        for v in side[1:]:
            counts[(v+side[0])%k] += 1
    gap = counts.index(min(counts))
    pending = [0]*(s-left)+[1]*(t-k+left)
    for side,z in leaf_suffix(k,pending,centers,gap):
        block[side].append(z)
    return block

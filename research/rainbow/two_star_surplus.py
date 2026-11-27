"""Two rooted stars on k-1 new vertices with forbidden vertex label zero."""
from math import gcd

from ..census.surplus_caterpillar import plain
from .two_star_extension import indicator


def split(k,x,y,leaves):
    return [[x]+sorted(leaves), [y]+sorted(set(range(1,k))-{x,y}-set(leaves))]


def zero_site(k,s,t,direct=0):
    # The virtual old vertex is 0, and each star center occupies a spine end.
    left = list(range(3,s+2))
    right = list(range(s+2,s+t+1))
    singles = list(range(s+t+1,s+t+1+direct))
    labels,_ = plain([1,0,2],{0:singles,1:left,2:right})
    def values(nodes):
        return [(labels[v]-labels[0])%k for v in nodes]
    return values([1]+left),values([2]+right),values(singles)


def exact(k,s,a,b):
    t = k-1-s
    for h in range(1,k):
        for y in dict.fromkeys((a,(b-h)%k,(a+b+s*h)%k)):
            x = (y+h)%k
            if not x or not y:
                continue
            gap = (-a-b-(s-1)*x-(t-1)*y)%k
            rhs = [0]*k
            for v in (0,x,y):
                rhs[v] += 1
            for v in ((a+h)%k,b,(gap-y)%k):
                rhs[v] -= 1
            leaves = indicator(k,h,rhs,{0,x,y},s-1)
            if leaves is not None:
                return split(k,x,y,leaves)
    return None


def packet(k,s,a,b):
    """Construct a rainbow packet or return None. Star sizes are s and k-1-s."""
    if not 1<=s<=k-2:
        raise ValueError("the two stars must be nonempty")
    a,b = a%k,b%k
    t = k-1-s
    if a==b:
        if a==0:
            return list(zero_site(k,s,t)[:2])
        if s>t:
            return packet(k,t,b,a)[::-1]
        h = 1 if 2*a<=k else -1
        return split(k,(a+h)%k,a,[(-j*h)%k for j in range(1,s)])
    if a and b:
        if s==1:
            return split(k,(b-a)%k,b,[])
        if t==1:
            return packet(k,t,b,a)[::-1]
        h = (a-b)%k
        if gcd(h,k)==1:
            if a*pow(h,-1,k)%k>k-s:
                return packet(k,t,b,a)[::-1]
            return split(k,(a+h)%k,a,[b]+[(-j*h)%k for j in range(1,s-1)])
    else:
        if not a:
            block = packet(k,t,b,0)
            return None if block is None else block[::-1]
        if gcd(a,k)==gcd(s,k)==1:
            h = a*pow(s,-1,k)%k
            return split(k,(a+h)%k,a,[j*h%k for j in range(1,s)])
    return exact(k,s,a,b)


def common(k,s,t,direct,site):
    """Full rainbow packet at one normalized site, also allowing direct leaves."""
    if min(s,t)<1 or direct<0 or s+t+direct!=k-1:
        raise ValueError("expected a full common-site packet")
    if site%k==0:
        return zero_site(k,s,t,direct)
    if s>t:
        right,left,singles = common(k,t,s,direct,site)
        return left,right,singles
    left,combined = packet(k,s,site,site)
    return left,combined[:t],combined[t:]


def surplus_site(k,s,c):
    """Full packet with the order-s star at the surplus and the other site c."""
    if not 1<=s<=k-2:
        raise ValueError("expected two nonempty stars")
    d = k//gcd(k,c)
    if d==1:
        return True
    for m in range(2,k+1):
        if k%m:
            continue
        r = s%m
        if r==m-1:
            continue
        if m%d and s>=m:
            return True
        if m%d==0 and m>d and r>=m//d-1:
            return True
        if m==d and r >= (1 if m%2 else 2):
            return True
    return False


def antipodal(k,s):
    """The order-s star attaches at the surplus and the other at its antipode."""
    if k%2 or not 1<=s<=k-2:
        raise ValueError("expected an even modulus and two nonempty stars")
    for m in range(3,k+1):
        if k%m:
            continue
        r = s%m
        if r<=m-2 and (s>=m if m%2 else r>=m//2-1):
            return True
    return False


def one_center(k,s,parent,other):
    """Full batch with one star of order s and singleton leaves at the other site."""
    for z in range(1,k):
        h = (z-other)%k
        gap = (-parent-(s-1)*z-(k-1-s)*other)%k
        rhs = [0]*k
        for v in (0,z):
            rhs[v] += 1
        for v in ((parent+h)%k,(gap-other)%k):
            rhs[v] -= 1
        kids = indicator(k,h,rhs,{0,z},s-1)
        if kids is not None:
            return [z]+kids,sorted(set(range(1,k))-{z}-set(kids))
    raise ValueError("no one-center witness for this full batch")


def prime_growth(k,order,a,b,special,*,surplus):
    """Label a prescribed interleaving of two stars at a prime modulus.

    The first occurrence of each side (0 or 1) is its center. Special is the
    old vertex surplus or edge deficit, according to the starting phase.
    """
    from .two_star_growth import rainbow_leaves

    if k<2 or any(i not in (0,1) for i in order):
        raise ValueError("expected two star indices and modulus at least two")
    parents = [a%k,b%k]
    centers = [None,None]
    labels = []
    while len(labels)<len(order):
        if not surplus:
            side = order[len(labels)]
            parent = parents[side] if centers[side] is None else centers[side]
            special = (special-parent)%k
            labels.append(special)
            if centers[side] is None:
                centers[side] = special
            surplus = True
            continue
        batch = order[len(labels):len(labels)+k-1]
        fresh = [i for i in (0,1) if centers[i] is None and i in batch]
        if len(fresh)==2:
            digits = packet(k,batch.count(0),(a-special)%k,(b-special)%k)
            if digits is None:
                raise ValueError("no two-star witness for this full batch")
        elif fresh:
            i, = fresh
            other = centers[1-i] if centers[1-i] is not None else special
            star,singles = one_center(k,batch.count(i),(parents[i]-special)%k,(other-special)%k)
            digits = [star,singles] if i==0 else [singles,star]
        else:
            shifts = [centers[i] for i in batch]
            leaves = rainbow_leaves(k,shifts,special)
        indices = [0,0]
        weights = set()
        for j,i in enumerate(batch):
            z = (special+digits[i][indices[i]])%k if fresh else leaves[j]
            parent = centers[i] if centers[i] is not None else parents[i]
            labels.append(z)
            weights.add((z+parent)%k)
            indices[i] += 1
            if centers[i] is None:
                centers[i] = z
        if len(batch)==k-1:
            special, = set(range(k))-weights
            surplus = False
    return labels

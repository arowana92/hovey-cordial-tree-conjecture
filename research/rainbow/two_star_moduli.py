"""Divisor criterion for universally extendible two-star splits on a divisible core."""
from functools import lru_cache
from math import gcd, isqrt, lcm

from .two_star_extension import from_leaves, packet, shift


@lru_cache(None)
def divisors(k):
    small = [x for x in range(1,isqrt(k)+1) if k%x==0]
    return tuple(small+[k//x for x in reversed(small) if x*x!=k])


@lru_cache(None)
def prime_powers(k):
    result = []
    for p in divisors(k):
        if len(divisors(p))==2:
            power = p
            while k%(p*power)==0:
                power *= p
            result.append((p,power))
    return tuple(result)


def distance(s,size):
    r = s%size
    return min(r,size-r)


def prime_witness(k,s,p):
    """Subgroup size witnessing extension for a saturated prime p."""
    return next((size for size in divisors(k) if size%p==0 and s%size
                 and distance(s,size)>=size//p-1),None)


def obstructing_prime(k,s):
    """None exactly when every prescribed old labeling extends at this split."""
    if not 0<s<k:
        raise ValueError('a full packet has two nonempty stars')
    return next((p for p,power in prime_powers(k)
                 if s%power==0 and prime_witness(k,s,p) is None),None)


def first_obstruction(k):
    for s in range(1,k//2+1):
        p = obstructing_prime(k,s)
        if p is not None:
            return s,p
    return None


def generator(k,size,multiple,target):
    index = k//size
    return next(index*u for u in range(1,size) if gcd(u,size)==1
                and (multiple*index*u-target)%k==0)


def fill(k,s,size,h,leaves,excluded):
    index = k//size
    cosets = [r for r in range(1,index) if r not in excluded]
    assert s//size<=len(cosets)
    for r in cosets[:s//size]:
        leaves.update(range(r,k,index))
    assert len(leaves)==s-1 and not leaves.intersection({0,h})
    return from_leaves(k,h,0,leaves)


def middle(k,s,q,delta,size):
    m = k//gcd(delta,k)
    width = size//m
    r = s%size
    h = generator(k,size,width,delta)
    index = k//size
    c = (q//index)*pow(h//index,-1,size)%size
    if c>size-r+1:
        return shift(middle(k,k-s,(-q)%k,delta,size),q,k)[::-1]
    positions = list(range(c,c+width))+list(range(size-r+1+width,size))
    return fill(k,s,size,h,{i*h%k for i in positions},set())


def lift(k,s,q,delta,size):
    order = k//gcd(q,k)
    width = size//order
    r = s%size
    if distance(s,size)==width-1:
        if r!=size-width+1:
            return shift(lift(k,k-s,(-q)%k,delta,size),q,k)[::-1]
        h = generator(k,size,width,q)
        return fill(k,s,size,h,{i*h%k for i in range(width,size)},set())
    assert distance(s,size)>=width+1
    if delta%(k//size)==0:
        return middle(k,s,q,delta,size)
    if s>k-s:
        return shift(lift(k,k-s,(-q)%k,delta,size),q,k)[::-1]
    h = generator(k,size,width,-q)
    leaves = {i*h%k for i in range(-width,0)}
    start = delta-(s-1)*h
    leaves.update((start+i*h)%k for i in range(r-1-width))
    return fill(k,s,size,h,leaves,{delta%(k//size)})


def construct(k,s,a,b,deficit):
    """Construct full packets certified by the divisor proof. None is inconclusive
    for an individual input whose split fails the universal test.
    """
    q,delta = (b-a)%k,(deficit-a-b)%k
    index = gcd(delta,k)
    m = k//index
    if delta%gcd(s,k)==0 or q==0 or q%index or s%m:
        return packet(k,s,a,b,deficit)
    for ell,power in prime_powers(k):
        if ell<m and s%power:
            size = lcm(m,ell*gcd(s,power))
            return shift(middle(k,s,q,delta,size),a,k)
    order = k//gcd(q,k)
    for p,_ in prime_powers(order):
        size = prime_witness(k,s,p)
        if size is not None:
            return shift(lift(k,s,q,delta,lcm(size,order)),a,k)
    return None

"""Extend a prescribed surplus core across direct leaves and two-edge arms."""

from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import gcd

from .two_site_arms import avoid_vertex, block, even_period, from_surplus, short_at_hub


def interval(arms, start):
    """On tip positions start+j use the index-doubling displacement at j."""
    period = arms if arms%2 else arms+1
    first = 1-arms%2
    return [(2*j%period-j,start+j) for j in range(first,first+arms)]


def complement(k, pairs):
    used = {v%k for pair in pairs for v in pair}
    return [x for x in range(k) if x not in used]


def delete_tip(k, pairs, y):
    leaves = complement(k,pairs)
    for i,(a,z) in enumerate(pairs):
        if z%k == y:
            return pairs[:i]+pairs[i+1:], leaves+[a]
    raise AssertionError("the specified label must be a tip")


def positive_hole(k, y, b):
    """Here 0<y<=k/2, and e=k-1-2b is positive."""
    h = b//2
    if 1 <= y <= h and (b%2 or k > 2*b+2):
        start = h+1
        pairs = interval(b,start)
        vacancy = (-start)%k
        leaves = complement(k,pairs)
        leaves.remove(vacancy)
        # The arm at index y is (y,start+y). Its new internal sum is y.
        pairs[y-(1-b%2)] = (vacancy,start+y)
        return pairs,leaves
    if h < y < k-h-b:
        pairs = interval(b,k-h-b-(1-b%2))
        leaves = complement(k,pairs)
        leaves.remove(y)
        return pairs,leaves

    q = b+1
    t = q//2
    if t < y < k-t and k-2*t-1 >= q:
        first_tip = max(t+1, y-q+1)
        return delete_tip(k,interval(q,first_tip-(1-q%2)),y)
    if q%2 == 0 and 2*q == k:
        return delete_tip(k,even_period(q),y)

    # One leaf at modulus 2q, with q odd. Odd tips fill the odd coset.
    assert k == 2*q and q%2 == 1
    if y%2:
        pairs = [(2*(2*j%q-j),2*j+1) for j in range(q)]
        return delete_tip(k,pairs,y)
    # The even label has odd additive order. A unit multiple lies far from zero.
    g = gcd(k,y)
    m = k//g
    z = g*((m-1)//2)
    root = (y//g)*pow(z//g,-1,m)%m
    scale = next(a for a in range(root,k,m) if gcd(a,k)==1)
    pairs,leaves = positive_hole(k,z,b)
    return [(scale*a,scale*x) for a,x in pairs],[scale*x for x in leaves]


def mixed(k, y, e):
    """Use every vertex residue except y, with distinct weights and e singletons."""
    if k < 1 or not 0 <= e < k or (k-1-e)%2:
        raise ValueError("the remaining vertices must split into pairs")
    y %= k
    b = (k-1-e)//2
    if y == 0:
        return short_at_hub(b,e,k)
    if e == 0:
        return avoid_vertex(k,y),[]
    sign = 1 if 2*y <= k else -1
    pairs,leaves = positive_hole(k,min(y,k-y),b)
    return [((sign*a)%k,(sign*z)%k) for a,z in pairs],[(sign*x)%k for x in leaves]


@lru_cache(None)
def four_tail(y,b,e):
    """Residual case after removing uniform four-arm and four-leaf groups."""
    for pairs in combinations_with_replacement(product(range(4),repeat=2),b):
        for leaves in combinations_with_replacement(range(4),e):
            vertices = [y,*leaves]+[x for pair in pairs for x in pair]
            weights = list(leaves)+[x for a,z in pairs for x in (a,(a+z)%4)]
            if all(max(freq)-min(freq)<=1 for freq in
                   ([vals.count(i) for i in range(4)] for vals in (vertices,weights))):
                return list(pairs),list(leaves)
    raise AssertionError("no labeling for four-label remainder")


def extend(k, joint, surplus, b, leaves):
    """Actual labels for arbitrary arms and leaves at an order-one-residue core."""
    if k <= 0 or min(b,leaves) < 0:
        raise ValueError("need a positive modulus and nonnegative populations")
    if k == 1:
        return [(0,0)]*b,[0]*leaves
    y = (surplus-joint)%k
    if k == 4:
        pairs,singles = four_tail(y,b%4,leaves%4)
        pairs = [(0,1),(0,2),(1,2),(3,3)]*(b//4)+pairs
        singles = list(range(4))*(leaves//4)+singles
    else:
        prefix = []
        plain = []
        if k%2:
            if not leaves:
                return from_surplus(k,joint,surplus,b),[]
            periods,b = divmod(b,k)
            prefix = [(j,j) for j in range(k)]*periods
            if b > k//2:
                tip,arms = block(k,0)
                prefix.extend(arms)
                plain.append(tip)
                b -= k//2
                leaves -= 1
        else:
            periods,b = divmod(b,k//2)
            if periods:
                prefix = even_period(k//2)*periods
        e = k-1-2*b
        pairs,singles = mixed(k,y,e)
        if leaves > e:
            weights = {w%k for a,z in pairs for w in (a,a+z)} | {x%k for x in singles}
            missing, = set(range(k))-weights
            cycle = [missing]+[x for x in range(k) if x != missing]
            singles += [cycle[i%k] for i in range(leaves-e)]
        else:
            singles = singles[:leaves]
        pairs = prefix+pairs
        singles = plain+singles
    return [((a+joint)%k,(z+joint)%k) for a,z in pairs],[(x+joint)%k for x in singles]

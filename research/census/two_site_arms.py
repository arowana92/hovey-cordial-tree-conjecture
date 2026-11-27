"""A uniform block with one leaf and paired path vertices at two specified sites."""

from functools import lru_cache
import json
from math import gcd
from pathlib import Path

from .regular_joint import single_tips



@lru_cache(None)
def seeds():
    return json.loads(Path(__file__).with_name("two-site-arm-seeds.json").read_text())


def signed_jumps(d, s):
    """Displacements in order of position, from Jordon and Mitchell, Theorems 3.1–3.2."""
    if d < 1 or s < 2*d-1:
        raise ValueError("signed Langford order below the existence threshold")
    if s == 2*d-1:
        jumps = [0]*(2*s)
        for j in range(s):
            high = s+2*j % s
            jumps[j], jumps[high] = high-j, j-high
        return jumps
    h = s//2
    if s % 2:
        bands = [(h, d+s-2), (d, d+s-1), (h+1, -d),
                 (h+1-d, s-d-1), (d-1, d-s-2), (h-d+1, -d-1)]
    else:
        bands = [(h, d+s-1), (d-1, d+s-2), (h, -d),
                 (h-d+1, s-d), (d, d-s-1), (h-d, -d-1)]
    return [first-2*j for length,first in bands for j in range(length)]


def enlarge(radius, s):
    """Attach new two-edge arms around a signed interval already in use."""
    start = radius+s+1
    return [(diff, start+x) for x,diff in enumerate(signed_jumps(radius+1, s))]


def nonzero_arms(g):
    """Use all nonzero bins exactly once at a zero joint, for odd g other than 3."""
    if g % 4 == 1:
        s = g//4
        return [(2*j % (2*s+1)-j, s+j) for j in range(1, 2*s+1)]
    if g < 55:
        return seeds()["nonzero"][str(g)]
    # In this seed both histograms fill [-5,5] except for zero.
    frame = [(-5, 4), (1, 3), (2, -4), (5, -2), (-3, -1)]
    return frame+enlarge(5, (g-11)//4)


def difference_three(k):
    """Normalize the singleton parent to 3, with the common parent zero."""
    if str(k) in seeds()["difference_three"]:
        base = seeds()["difference_three"][str(k)]
        return base["singleton"], base["arms"]
    if k % 4 == 3:
        singleton, frame, radius = 0, [(-2, 1), (-3, 3), (2, -1)], 3
    else:
        singleton, frame, radius = -2, [(-3, 1), (0, 2), (-4, 3), (4, -1)], 4
    s = (k-2*radius-1)//4
    return singleton, frame+(enlarge(radius, s) if s else [])


def unit_block(k, difference):
    b = k//2
    h = (b+1)//2
    if b % 2:
        start = h+1
        rule = [1+(2*j % b) for j in range(b)]+[0]
        target = -b
    else:
        start = h+1
        rule = [2*j % (b+1) for j in range(b+1)]
        target = -h
    scale = difference*pow(target, -1, k) % k
    singleton = None
    arms = []
    for j, dest in enumerate(rule):
        jump = dest-j
        if jump == target:
            singleton = scale*(start+j)
        else:
            arms.append((scale*jump, scale*(start+j)))
    return singleton, arms


def fill_fibers(g, m, subgroup):
    result = [(g*a, g*z) for a,z in subgroup]
    for a,z in nonzero_arms(g):
        result.extend((a+g*j, z+g*j) for j in range(m))
    return result


def lift_unit_from_three(k, value):
    return next(u for u in range(value//3,k,k//3) if gcd(u,k) == 1)


def block(k, difference):
    """Return singleton label and (intermediate, tip) labels with common parent zero."""
    if k <= 0 or k % 2 == 0:
        raise ValueError("the modulus must be positive and odd")
    x = difference % k
    b = k//2
    if not x:
        if b % 2:
            start = (b+1)//2
            return start+b, [(2*j % b-j, start+j) for j in range(b)]
        return 0, nonzero_arms(k)
    g = gcd(x, k)
    if g == 3:
        old, pairs = difference_three(k)
        # Need a unit modulo k mapping 3 to x, including when 9 divides k.
        scale = lift_unit_from_three(k, x)
        return scale*old, [(scale*a, scale*z) for a,z in pairs]
    m = k//g
    old, pairs = unit_block(m, x//g)
    return g*old, fill_fibers(g,m,pairs)


def unit_hole(k, y):
    """The omitted vertex label is a unit. The omitted weight can vary."""
    b = k//2
    if b % 2:
        missing, pairs = block(k, 0)
    else:
        h = b//2
        missing = 2*h+1
        pairs = [((2*j+1) % (b+1)-j, h+1+j) for j in range(b+1) if j != h]
    scale = y*pow(missing, -1, k) % k
    return [(scale*a, scale*z) for a,z in pairs]


def avoid_vertex(k, y):
    """(k-1)/2 arms with distinct weights and distinct labels avoiding y."""
    if k < 1 or k % 2 == 0:
        raise ValueError("the modulus must be positive and odd")
    y %= k
    if y == 0:
        return [(1,2)] if k == 3 else nonzero_arms(k)
    g = gcd(k,y)
    if g == 3:
        small = seeds()["forbidden_three"]
        if str(k) in small:
            pairs = small[str(k)]
        else:
            if k % 4 == 3:
                r, pairs = 3, [(-2,-1), (0,1), (2,-3)]
            else:
                r, pairs = 4, [(-4,1), (0,-2), (2,-3), (4,-1)]
            s = (k-2*r-1)//4
            if s:
                pairs += enlarge(r,s)
        scale = lift_unit_from_three(k,y)
        return [(scale*a,scale*z) for a,z in pairs]
    m = k//g
    return fill_fibers(g,m,unit_hole(m,y//g))


def hit_weight(k, target, r):
    """A short batch with distinct labels and weights and a designated weight hit."""
    for x, scale in ((0,1),(0,-1),(1,1)):
        _, pairs = block(k,x)
        moved = [(a*scale,z*scale) for a,z in pairs]
        for i,(a,z) in enumerate(moved):
            if target % k in (a % k, (a+z) % k):
                return [moved[i]]+(moved[:i]+moved[i+1:])[:r-1]
    raise AssertionError("the full batches have different omitted weights")


def from_surplus(k, joint, surplus, count):
    """Attach any number of two-edge paths to a fixed order-one-residue core."""
    if k <= 0 or k % 2 == 0 or count < 0:
        raise ValueError("need a positive odd modulus and a nonnegative path count")
    periods, rest = divmod(count,k)
    pairs = [(j,j) for _ in range(periods) for j in range(k)]
    if rest:
        b = k//2
        first = avoid_vertex(k, surplus-joint)
        pairs.extend(first[:rest])
        if rest > b:
            used = {w % k for a,z in first for w in (a,a+z)}
            target, = set(range(k))-used
            pairs.extend(hit_weight(k,target,rest-b))
    return [((a+joint)%k,(z+joint)%k) for a,z in pairs]


def short_at_hub(b, leaves, k):
    """At 2b<k, use an interval excluding zero or complete one full period."""
    half = b//2
    pairs = [(2*j % (2*half+1)-j, half+j+(b%2))
             for j in range(1,2*half+1)]
    if leaves < k-2*b:
        if b%2:
            pairs.append((-half-1,half+1))
        occupied = {0}
        for a,z in pairs:
            occupied.update((a%k,z%k,(a+z)%k))
        return pairs,[x for x in range(k) if x not in occupied][:leaves]
    if b % 2:
        pairs = [(2*j%b-j, half+1+j) for j in range(b)]
    used = {v%k for pair in pairs for v in pair}
    singles = [x for x in range(k) if x not in used]
    singles.extend(i%k for i in range(1,leaves-len(singles)+1))
    return pairs,singles


def even_period(b):
    """A neutral full block of b arms at modulus 2b, for b different from two."""
    if b % 2:
        return [(2*j%b-j, b//2+1+j) for j in range(b)]
    if b <= 20:
        return list(single_tips(b).items())
    s = (b-8)//2
    def move(x):
        return x+s*((x>=4)-(x<=-4))
    frame = [(move(a),move(z)) for a,z in single_tips(8).items()]
    return frame+[(d,10+s+j) for j,d in enumerate(signed_jumps(4,s))]

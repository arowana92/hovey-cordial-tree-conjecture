"""A uniform block with one leaf and paired path vertices at two specified sites."""

from functools import lru_cache
import json
from math import gcd
from pathlib import Path



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
        scale = next(u for u in range(x//3, k, k//3) if gcd(u,k) == 1)
        return scale*old, [(scale*a, scale*z) for a,z in pairs]
    m = k//g
    old, pairs = unit_block(m, x//g)
    result = [(g*a, g*z) for a,z in pairs]
    for a,z in nonzero_arms(g):
        result.extend((a+g*j, z+g*j) for j in range(m))
    return g*old, result

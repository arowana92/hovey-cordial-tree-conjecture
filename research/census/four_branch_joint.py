"""Uniform increments at a hub with four independently prescribed child populations."""

from math import gcd

from research.census.regular_joint import prefix


def assemble(n, counts, jumps):
    """Convert child displacements to labels on the tree with hub zero."""
    branches = {p % n: [] for p in counts}
    fixed = []
    for x in range(n):
        step = jumps.get(x,0) % n
        if step:
            branches[step].append(x)
        elif x not in branches:
            fixed.append(x)
    branches[0] = fixed[:counts[0]]
    return list(branches.items()), fixed[counts[0]:]


def rotate_and_pair(R, B, C, D, plain):
    """Pair B children at opposite centers, then rotate the unmatched children."""
    g = gcd(R,C-B)
    s,t = R//g, (C-B)//g
    H = D+2*B+4+plain
    n = H+R+C-B
    assert s != t and D+plain >= s and s+max(s,t)+1 <= H
    counts = {t:R, s:B, -s:C, 0:D}
    available = set(range(-s,H-s)) - counts.keys()
    jumps = {}
    for x in range(-s,H-s):
        if B and x in available and x+s in available:
            jumps[x % n], jumps[(x+s) % n] = s,-s
            available.difference_update((x,x+s))
            B -= 1
    assert B == 0
    for i in range(g*(s+t)):
        jumps[(H-s+i) % n] = t if i % (s+t) < s else -s
    return assemble(n,counts,jumps)


def twin_sum(a, b, plain):
    """Populations a,b,b,a+b. Split each negative step into two edges."""
    T = a+b
    n = 2*a+3*b+4+plain
    start = b+3+plain
    jumps = {}
    for i in range(T):
        x = start+i
        if i < a:
            jumps[x] = b
        else:
            jumps[x] = b+1
            jumps[x+b+1] = -(T+1)
    return assemble(n,{0:T, b:a, b+1:b, -T-1:b},jumps)


def clockwise(start, steps, n):
    jumps = {}
    x = start % n
    for step in steps:
        jumps[x] = step
        x = (x+step) % n
    assert x == start % n
    return jumps


def double_sum(a, b, plain):
    """Populations a,b,c,c with c=a+b, including both resonances."""
    c = a+b
    n = 3*c+4+plain
    if 2*a == plain+4:
        jumps = clockwise(-1,[4,2]+[4]*(a-1)+[2]*(b-1)+[1]*c,n)
        return assemble(n,{0:c,4:a,2:b,1:c},jumps)
    if a == plain+4:
        macro = clockwise(-12,[3,3,4,4,4,4]+[4]*(a-4)+[3]*(b-2),n)
        jumps = {}
        for x,step in macro.items():
            jumps[x] = step+5
            jumps[(x+step+5)%n] = -5
        return assemble(n,{0:c,9:a,8:b,-5:c},jumps)

    # Compress mixed corners of a rotation. The step from each preceding
    # position then skips the chosen corner and takes the sum of its two jumps.
    lo, length = a+1,2*c+a
    positive, negative = c+a,-c
    def following(x):
        return lo + (x-lo+positive) % length
    pred = {following(x):x for x in range(lo,lo+length)}
    valleys = set(range(lo,lo+c))
    skipped = {positive}
    peak = n-c
    if lo <= peak < lo+length:
        skipped.add(peak)
        valleys.difference_update((pred[peak],following(peak)))
    valleys.difference_update(skipped)
    skipped.update(sorted(valleys)[:a-len(skipped)])
    assert len(skipped) == a and all(following(x) not in skipped for x in skipped)
    jumps = {}
    for x in range(lo,lo+length):
        if x not in skipped:
            y = following(x)
            if y in skipped:
                y = following(y)
            jumps[x] = y-x
    return assemble(n,{0:c,positive:b,negative:c,a:a},jumps)


def four_branch(counts, plain=0):
    if len(counts)!=4 or min(counts)<1 or plain<0:
        raise ValueError("expected four positive child counts and nonnegative direct leaves")
    a,b,c,d = sorted(counts)
    n = a+b+c+d+plain+4
    if a==c or b==d:
        q,e = (b,d) if a==c else (b,a)
        return prefix(4,q,e,plain,n)
    if c>b and c-b!=a:
        return rotate_and_pair(a,b,c,d,plain)
    if b==c:
        if d==a+b:
            return twin_sum(a,b,plain)
        if d>=2*b:
            return rotate_and_pair(b,a,b,d,plain)
        return rotate_and_pair(a,b,d,b,plain)
    assert c == a+b
    if d==c:
        return double_sum(a,b,plain)
    if d<=2*c:
        return rotate_and_pair(a,b,d,c,plain)
    if a<b:
        return rotate_and_pair(c,a,b,d,plain)

    # a,a,2a,d with d>4a. Repeat a four-position permutation.
    jumps = {}
    for i in range(a):
        for j,step in enumerate((3,1,-2,-2)):
            jumps[4+4*i+j] = step
    return assemble(n,{0:d,1:a,3:a,-2:2*a},jumps)

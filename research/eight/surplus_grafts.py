"""Construct extensions from a one-surplus core and the all-modulus star family."""
from collections import Counter
from math import gcd

from research.rainbow.generate import rainbow
from .lean_tables import normalize


def star(k,c,p,b=0,center=None):
    """One c-child star at p and k-2-c singletons at common parent color b.

    With the surplus translated to zero, return (center, children, singletons)
    or None. A supplied center fixes its label for the entire test.
    """
    if k<3 or not 1<=c<=k-2:
        raise ValueError("the star must fit in a packet of k-1 vertices")
    p,b = p%k,b%k
    if b==0 and p%gcd(c+1,k):
        return None
    for a in range(1,k) if center is None else [center%k]:
        if a==0:
            continue
        d = (a-b)%k
        g = gcd(k,d)
        h = k//g
        inverse = pow(d//g,-1,h) if h>1 else 0

        def steps(y):
            return None if y%g else (y//g*inverse)%h

        j = steps(a)
        caps = (h-1,h-1) if j is None else (h-j-1,j-1)
        used_cosets = {0,a%g}
        w = (p+d)%k
        for side,length in enumerate((steps(-w),steps(a-w))):
            if length is None or length>caps[side] or length>c:
                continue
            whole,other = divmod(c-length,h)
            if other>caps[1-side] or whole>g-len(used_cosets):
                continue
            l0,la = (length,other) if side==0 else (other,length)
            kids = {(-i*d)%k for i in range(1,l0+1)}
            kids.update((a-i*d)%k for i in range(1,la+1))
            full_cosets = [x for x in range(g) if x not in used_cosets][:whole]
            for x in full_cosets:
                kids.update((x+i*d)%k for i in range(h))
            return a,sorted(kids),sorted(set(range(1,k))-kids-{a})
    return None


def first_seven(parents):
    """Choose seven vertices of an eight-vertex ideal, independently of colors."""
    for skip in range(8):
        if skip in parents[:8]:
            continue
        take = [i for i in range(8) if i!=skip]
        child_counts = Counter(parents[i] for i in take if parents[i]>=0)
        if len(child_counts)!=1 or next(iter(child_counts.values()))%2==0:
            return take
    raise AssertionError("no admissible seven-vertex ideal")


def extend(core,parents,levels):
    """Label an attachment to any eight-cordial core of order one modulo eight.

    A negative parent -1-i denotes old core vertex i. Other parents index
    earlier free vertices. The result contains only the new vertex labels.
    A seven-vertex prescribed-core obstruction returns None.
    """
    hist = Counter(core)
    surplus = max(range(8),key=hist.__getitem__)
    old = [(x-surplus)%8 for x in core]
    n = len(parents)
    take = list(range(n)) if n<=7 else first_seven(parents)
    labels = [None]*n

    def packet(indices):
        local = {}
        ps = []
        for j,i in enumerate(indices):
            p = parents[i]
            if p in local:
                ps.append(local[p])
            else:
                color = old[-1-p] if p<0 else labels[p]
                ps.append(-1-color)
            local[i] = j
        return ps

    ps = packet(take)
    try:
        word = rainbow(ps,8)
    except ValueError:
        if n!=7:
            raise
        return None
    weights = [0]*8
    for i,x in zip(take,word):
        labels[i] = x
        p = parents[i]
        weights[(x+(old[-1-p] if p<0 else labels[p]))%8] += 1

    chosen = set(take)
    pending = [i for i in range(n) if i not in chosen]
    for pos in range(0,len(pending),8):
        indices = pending[pos:pos+8]
        ps = packet(indices)
        key,ren = normalize([-1-p if p<0 else 8+p for p in ps])
        size = len(indices)
        d = min(range(8),key=weights.__getitem__)
        word = levels[size][key][d*size:(d+1)*size]
        for j,i in enumerate(indices):
            x = word[ren[j]]
            labels[i] = x
            p = parents[i]
            weights[(x+(old[-1-p] if p<0 else labels[p]))%8] += 1
    return [(x+surplus)%8 for x in labels]

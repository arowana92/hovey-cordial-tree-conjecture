"""Independently search for obstructing quotient sets and replay actual affine joins."""
from functools import lru_cache
from itertools import product
from math import gcd
from random import Random

from .check_deficit_cut import realize

# Total deficit, threshold, remaining smooth divisor, sufficient quotients.
CASES = (
    (2, 7, 12, (8,9,12)),
    (3, 13, 360, (7,10,15,16,18,24,25,27)),
    (4, 25, 5040, (11,14,20,21,25,27,30,32,35,36,45,48,49)),
)


@lru_cache(None)
def units(m):
    return tuple(u for u in range(1,m) if gcd(u,m)==1)


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit
        mask -= bit


def prove(m, a, h, port, first):
    # Start with no forbidden bins. A successful move can only be destroyed by
    # putting one of its vertex holes or unfilled edge holes in the old low sets.
    def blockers(u, d):
        vertex = sum(1 << ((u*i+d) % m) for i in range(h))
        edge = sum(1 << ((u*i+2*d) % m) for i in range(first,first+h+1))
        return vertex, edge & ~(1 << ((u*port+d) % m))

    piece = tuple(dict.fromkeys(blockers(u,u*(port-j)) for u in units(m)
                                for j in range(first,first+h+1)))

    @lru_cache(None)
    def old(z):
        return tuple(dict.fromkeys(blockers(u,z-u*port) for u in units(m)))

    @lru_cache(None)
    def covers(v, w, nv, nw):
        action = next((p for p in piece if not (p[0]&v or p[1]&w)),None)
        if action is None:
            action = next((p for bit in bits(w) for p in old(bit.bit_length()-1)
                           if not (p[0]&v or p[1]&w)),None)
        if action is None:
            if not w:
                return all(covers(v,1 << z,nv,1) for z in range(m))
            return False
        vertex, edge = action
        return ((nv == a or all(covers(v|x,w,nv+1,nw) for x in bits(vertex))) and
                (nw == a+1 or all(covers(v,w|y,nv,nw+1) for y in bits(edge))))

    return covers(0,0,0,0)


def lifted(k, m, old_v, old_w, v, w, port):
    v0, w0 = {i % m for i in old_v}, {i % m for i in old_w}
    for u,d in product(units(m),range(m)):
        vertices = {(u*i+d) % m for i in v}
        edges = {(u*i+2*d) % m for i in w}
        bridge = (u*port+d) % m
        if vertices & v0 or bridge not in edges|w0 or (edges & w0)-{bridge}:
            continue
        U = next(i for i in units(k) if i % m == u)
        if bridge in edges:
            j, = [i for i in w if (u*i+2*d) % m == bridge]
            shift = U*(port-j)
        else:
            z = next(i for i in old_w if i % m == bridge)
            shift = z-U*port
        assert shift % m == d
        return U, shift % k
    raise AssertionError("no quotient move")


def tree(k, low_v, low_w, rng):
    return realize(k,[2-int(i in low_v) for i in range(k)],
                   [2-int(i in low_w) for i in range(k)],rng)


def cordial(k, core, part, labels, old_port, port, bias):
    x, xp, _ = core
    _, yp, _ = part
    vertex = [0]*k
    edge = [0]*k
    for vals,parents in ((x,xp),(labels,yp)):
        for i,val in enumerate(vals):
            vertex[val] += 1
            if i:
                edge[(val+vals[parents[i]]) % k] += 1
    edge[(x[old_port]+labels[port]+bias) % k] += 1
    return max(vertex)-min(vertex) <= 1 and max(edge)-min(edge) <= 1


def examples():
    rng = Random(271991)
    lifts = 0
    for H,_,_,moduli in CASES:
        for m,h,trial in product(moduli,range(1,H),range(12)):
            a = H-h
            k = m*rng.choice((6,9,10))
            # Even deliberately fold all the core edge holes into one residue.
            center = rng.randrange(m)
            old_w = ({center+m*i for i in rng.sample(range(k//m),a+1)} if trial % 2
                     else set(rng.sample(range(k),a+1)))
            old_v = set(rng.sample(range(k),a))
            first = rng.randrange(k)
            v, w = set(range(h)), {(first+j) % k for j in range(h+1)}
            b, bias = rng.randrange(k), rng.randrange(k)
            u,d = lifted(k,m,old_v,old_w,v,w,b)
            core,part = tree(k,old_v,old_w,rng),tree(k,v,w,rng)
            y = [(u*i+d) % k for i in part[0]]
            assert cordial(k,core,part,y,core[2][-bias % k][0],part[2][b][0],bias)
            lifts += 1

    failures = 0
    fixtures = ((6,{3},{2,4},1,0,3), (12,{4,8},{0,2,10},1,1,6),
                (24,{8,16},{0,4,20},2,2,12))
    for k,old_v,old_w,h,f,b in fixtures:
        core,part = tree(k,old_v,old_w,rng),tree(k,set(range(h)),set(range(f,f+h+1)),rng)
        for u,d in product(units(k),range(k)):
            y = [(u*i+d) % k for i in part[0]]
            assert not cordial(k,core,part,y,core[2][0][0],part[2][b][0],0)
            failures += 1
    return lifts,failures


if __name__ == "__main__":
    for H,threshold,smooth,moduli in CASES:
        for k in range(threshold,smooth+1):
            if smooth % k == 0:
                assert any(k % m == 0 for m in moduli)
        profiles = 0
        for m in moduli:
            for h,b,f in product(range(1,H),range(m),range(m)):
                assert prove(m,H-h,h,b,f), (m,H,h,b,f)
                profiles += 1
        print(f"deficit={H} quotient inputs before choosing old low bins={profiles}",flush=True)
    print("Successful lifted tree joins and rejected affine images:", *examples())

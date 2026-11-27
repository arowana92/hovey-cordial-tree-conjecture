"""Literal histogram checks for large prime powers, parity fibers, and affine obstructions."""

from math import gcd
from random import Random

from .check_deficit_cut import realize


def bridge_histograms(k, port, holes, low_vertices, low_edges, rng):
    core, cp, old_sites = realize(k, [3-int(v in low_vertices) for v in range(k)],
                                 [3-int(w in low_edges) for w in range(k)], rng)
    piece, pp, sites = realize(k, [3-int(v == 0) for v in range(k)],
                              [3-int(w in holes) for w in range(k)], rng)
    # Search by the bridge value. Moving to the next unit moves the vertex hole too.
    units = [u for u in range(1, k) if gcd(u,k) == 1]
    for z in range(k):
        for u in units:
            x = (z-u*port) % k
            if x in low_vertices:
                continue
            y, w = ((u*d+2*x) % k for d in holes)
            if not ((y == z and w not in low_edges) or (w == z and y not in low_edges)
                    or (z in low_edges and y not in low_edges and w not in low_edges)):
                continue
            changed = [(u*v+x) % k for v in piece]
            vertices = [0]*k
            edges = [0]*k
            for row, parents in ((core,cp),(changed,pp)):
                for i, v in enumerate(row):
                    vertices[v] += 1
                    if i:
                        edges[(v+row[parents[i]]) % k] += 1
            bridge = (core[old_sites[0][0]]+changed[sites[port][-1]]) % k
            assert bridge == z
            edges[bridge] += 1
            assert max(vertices)-min(vertices) <= 1 and max(edges)-min(edges) <= 1
            return True
    return False


def large_factors():
    rng = Random(2131326)
    count = 0
    for p, exponent, cofactor in [(7,2,2), (11,2,1), (11,2,4), (13,2,3),
                                  (13,1,6), (17,1,8), (19,1,15), (31,1,2)]:
        power = p**exponent
        k = power*cofactor
        for i in range(70):
            a = rng.randint(1,(p-5)//2)
            b = p**(i%exponent)*rng.randrange(1,p)
            if i%4 == 0 and cofactor > 1:
                residues = (b,b)
            elif i%4 <= 2:
                residues = (b,3*b*pow(2,-1,power) % power)
            else:
                residues = rng.sample(range(power),2)
            d, e = [v+power*rng.randrange(cofactor) for v in residues]
            if d == e:
                e = (e+power) % k
            assert d != e and (d%power,e%power) != ((2*b)%power,(2*b)%power)
            low_v = set(rng.sample(range(k),a))
            if i%2:
                low_e = set(rng.sample(range(k),a+1))
            else:
                origin = rng.randrange(k//p)
                low_e = set(rng.sample(range(origin,k,k//p),a+1))
            assert bridge_histograms(k,b,(d,e),low_v,low_e,rng)
            count += 1
    return count


def obstruction_examples():
    rng = Random(19311952)
    count = 0
    for m in (11,13,31,121,143,31*41):
        k = 2*m
        for loss in (1,2,3):
            # Forbidden directions wholly inside the subgroup of order two.
            b = rng.choice((0,m))
            low_e = {0,m} | set(range(1,loss))
            forced = {(z-b) % k for z in low_e-{0,m}}
            low_v = forced | set(rng.sample(sorted(set(range(k))-forced),loss-len(forced)))
            assert not bridge_histograms(k,b,(0,m),low_v,low_e,rng)
            count += 1
        # Both holes over twice a nonzero port, with a closed projection.
        assert not bridge_histograms(k,1,(2,m+2),{0},{0,m},rng)
        count += 1
        if m%31 == 0:
            scale = m//31
            low_e = {0,m} | {scale*j for j in (1,2,4,8,16)}
            assert not bridge_histograms(k,1,(2,m+2),set(range(6)),low_e,rng)
            count += 1
    return count


if __name__ == '__main__':
    print('Ordinary tree pairs with a large prime-power factor:', large_factors(), flush=True)
    print('Fixed tree pairs with certified affine obstructions:', obstruction_examples(), flush=True)

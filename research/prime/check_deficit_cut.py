"""Independent checks for affine gluing of a tree of order -1 modulo k."""

from itertools import combinations
from math import comb, gcd, isqrt
from random import Random


def primes(bound):
    return [p for p in range(5, bound + 1)
            if all(p % q for q in range(2, isqrt(p) + 1))]


def affine_hits(k, port, holes, low_edges, x, units):
    """After removing uniform increments, the net edge change must preserve balance."""
    for u in units:
        left, right = ((2*x + u*w) % k for w in holes)
        bridge = (x + u*port) % k
        if bridge == left:
            if right not in low_edges:
                return u
        elif bridge == right:
            if left not in low_edges:
                return u
        elif bridge in low_edges and left not in low_edges and right not in low_edges:
            return u
    return None


def exhaustive():
    # Normalize the low vertex to zero and dilate a nonzero port to one.
    # For each high-edge set, count the viable x directly. Any r-set of
    # high vertices must contain one if its complement is too small.
    tested = 0
    for p in (7, 11, 13):
        units = range(1, p)
        for port in (0, 1):
            for holes in combinations(range(p), 2):
                for r in range((p+7)//2, p):
                    for low in combinations(range(p), p-r+1):
                        viable = 0
                        for x in range(p):
                            if affine_hits(p, port, holes, low, x, units) is not None:
                                viable += 1
                                if viable > p-r:
                                    break
                        assert viable > p-r, (p, port, holes, r, low)
                        tested += comb(p, r)
    return tested


def coefficients():
    # Expand the leading polynomial literally; scan all coefficients that
    # fit the two independent lists. Include smaller cosets and uneven lists.
    tested = 0
    for p in primes(127):
        for m in range(1, (p-5)//2+1):
            f = [1]
            for c in [-1] + [1]*m + [3]*m:
                f = [(a+c*b) % p for a, b in zip(f+[0], [0]+f)]
            assert len(f) == 2*m+2 and f[0] and f[-1]
            assert all(any(f[j:j+3]) for j in range(len(f)-2))
            for xsize in range(p - (p-7)//2, p+1):
                if xsize-m-2 < 3:
                    continue
                assert any(f[j] for j in range(m) if len(f)-1-j < xsize)
                tested += 1
    return tested


def realize(k, vertex_counts, edge_counts, rng):
    """Realize the histograms on an ordinary tree using one copy of every label in a star."""
    labels = list(range(k))
    rng.shuffle(labels)
    root = labels[0]
    parents = [-1]+[0]*(k-1)
    sites = [[] for _ in range(k)]
    for i, x in enumerate(labels):
        sites[x].append(i)
    rest = [n-1 for n in vertex_counts]
    weights = list(edge_counts)
    for x in labels[1:]:
        weights[(root+x) % k] -= 1
    assert min(rest) >= 0 and min(weights) >= 0
    extra = [x for x, n in enumerate(rest) for _ in range(n)]
    sums = [w for w, n in enumerate(weights) for _ in range(n)]
    assert len(extra) == len(sums)
    rng.shuffle(extra)
    rng.shuffle(sums)
    for x, w in zip(extra, sums):
        parents.append(rng.choice(sites[(w-x) % k]))
        sites[x].append(len(labels))
        labels.append(x)
    return labels, parents, sites


def check_histograms(k, labels, parents):
    vertices, edges = [0]*k, [0]*k
    for i, x in enumerate(labels):
        vertices[x] += 1
        if i:
            edges[(x+labels[parents[i]]) % k] += 1
    assert max(vertices)-min(vertices) <= 1
    assert max(edges)-min(edges) <= 1
    return vertices, edges


def actual_trees():
    rng = Random(19912629)
    moduli = primes(79) + [49, 77, 121, 143, 169]
    count = crossed = 0
    for _ in range(2400):
        k = rng.choice(moduli)
        least = next((j for j in range(2, isqrt(k)+1) if k % j == 0), k)
        loss = rng.randint(1, max(1, (least-7)//2))
        r = k-loss
        a, c, b = (rng.randrange(k) for _ in range(3))
        if count % 3:
            # Crossed configurations can defeat both choices of bridge hole.
            order = rng.choice([d for d in range(5, k+1) if k % d == 0])
            step = k//order
            b = (a + step) % k
            d = (a+b) % k
            e = ((a+3*b)*pow(2, -1, k)) % k
            crossed += 1
        else:
            d, e = rng.sample(range(k), 2)
        low_v = set(rng.sample(range(k), loss))
        low_e = set(rng.sample(range(k), loss+1))
        if count % 2:
            low_v = {c} | set(rng.sample([x for x in range(k) if x != c], loss-1))
            low_e = {2*c % k} | set(rng.sample([x for x in range(k) if x != 2*c % k], loss))
        core, cp, old_sites = realize(k, [2+int(x not in low_v) for x in range(k)],
                                     [2+int(x not in low_e) for x in range(k)], rng)
        piece, pp, new_sites = realize(k, [3-int(x == a) for x in range(k)],
                                      [3-int(x in (d,e)) for x in range(k)], rng)
        old_port, new_port = rng.choice(old_sites[c]), rng.choice(new_sites[b])
        # Inspect actual edge and vertex counts, including the specified ports.
        check_histograms(k, core, cp)
        check_histograms(k, piece, pp)
        units = [u for u in range(1, k) if gcd(u,k) == 1]
        holes = ((d-2*a) % k, (e-2*a) % k)
        C = {(w-2*c) % k for w in low_e}
        for x in range(k):
            if (x+c) % k in low_v:
                continue
            u = affine_hits(k, (b-a) % k, holes, C, x, units)
            if u is not None:
                break
        else:
            raise AssertionError((k,r,a,b,c,d,e))
        joined = core+[(c+x+u*(v-a)) % k for v in piece]
        verts = [0]*k
        edges = [0]*k
        for v in joined:
            verts[v] += 1
        for labels, parents in ((core, cp), (joined[len(core):], pp)):
            for i in range(1, len(labels)):
                edges[(labels[i]+labels[parents[i]]) % k] += 1
        edges[(core[old_port]+joined[len(core)+new_port]) % k] += 1
        assert max(verts)-min(verts) <= 1 and max(edges)-min(edges) <= 1
        count += 1
    return count, crossed


if __name__ == '__main__':
    print('Abstract prime profiles covered:', exhaustive(), flush=True)
    print('Nonzero grid coefficients:', coefficients(), flush=True)
    print('Whole trees joined, including crossed profiles:', actual_trees(), flush=True)

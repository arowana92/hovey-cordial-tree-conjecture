"""Count the actual edges before and after attaching the two rooted pieces."""

from collections import Counter
from math import gcd
from random import Random

from .two_site_arms import block, nonzero_arms, signed_jumps


def increments(parent, labels, cut, k):
    vertices = [0]*k
    edges = [0]*k
    for v in range(cut, len(parent)):
        vertices[labels[v] % k] += 1
        edges[(labels[parent[v]]+labels[v]) % k] += 1
    assert vertices == edges == [1]*k


def one(k, x, rng):
    tip, arms = block(k, x)
    assert len(arms) == (k-1)//2
    sites = [0, 0 if not x and rng.randrange(2) else 4]
    core = [-1, 0, 0, 1, 2, 0, 4]
    base = [rng.randrange(2*k) for _ in core]
    base[sites[1]] = (base[0]+x) % k + k*rng.randrange(2) if sites[1] else base[0]
    forest = [(sites[1], tip)]
    for a,z in arms:
        v = len(core)+len(forest)
        forest.extend([(0,a), (v,z)])

    parent = core+[p for p, _ in forest]
    labels = base+[base[0]+z for _, z in forest]
    increments(parent, labels, len(core), k)

    # Replace each added vertex by an edge. The two attachment ports of a
    # neighboring pair are independent, even along the same chain.
    parent = core.copy()
    labels = base.copy()
    for p,z in forest:
        old = p if p < len(core) else len(core)+2*(p-len(core))+rng.randrange(2)
        low = (base[0]+z) % k
        entry = low if (low-labels[old]) % 2 == 0 else low+k
        parent.extend((old, len(parent)))
        labels.extend((entry, (entry+k) % (2*k)))
    increments(parent, labels, len(core), 2*k)


def main():
    rng = Random(199112)
    bands = 0
    for d in range(1, 19):
        for s in range(2*d-1, 151):
            jumps = signed_jumps(d, s)
            assert sorted(i+x for i,x in enumerate(jumps)) == list(range(2*s))
            assert sorted(jumps) == list(range(1-d-s,1-d))+list(range(d,d+s))
            bands += 1
    for g in range(7, 54, 4):
        pairs = nonzero_arms(g)
        expected = Counter(range(1,g))
        assert Counter(d % g for pair in pairs for d in pair) == expected
        assert Counter(d % g for a,z in pairs for d in (a,a+z)) == expected
    inputs = {(k,x) for k in range(1, 76, 2) for x in range(k)}
    for g in (7,11,15,19,23,27,31,35,39,43,47,51,55,59,63):
        for q in (3,5,9,15):
            inputs.update((g*q,g*u) for u in range(q) if gcd(u,q) == 1)
    for k in (79,101,255,513,1001):
        inputs.update((k,x) for x in range(k) if gcd(k,x) == 1)
    inputs.update((k,x) for k in (999,15015,65535) for x in (0,3,5,7,15,21,33,55))
    for k,x in sorted(inputs):
        one(k,x,rng)
    print("parent differences",len(inputs),"complete attachments",2*len(inputs),"signed Langford permutations",bands)


if __name__ == "__main__":
    main()

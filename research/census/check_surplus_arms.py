"""Verify the forbidden vertex bin and count full fixed-core histograms."""

from collections import Counter
from random import Random

from .two_site_arms import avoid_vertex, from_surplus


def verify_hole(k, y):
    pairs = avoid_vertex(k,y)
    vertices = [v%k for pair in pairs for v in pair]
    weights = [(v+a)%k for a,z in pairs for v in (0,z)]
    assert sorted(vertices) == [i for i in range(k) if i != y%k]
    assert len(set(weights)) == len(weights) == k-1


def check_tree(k, count, trial, rng):
    size = k*(1+trial%3)+1
    if trial % 2:
        parent = [-1]+list(range(size-1))
        base = [(v//2+(v%2)*((size+1)//2))%k for v in range(size)]
    else:
        parent = [-1]+[0]*(size-1)
        base = [v%k for v in range(size)]
    shift = rng.randrange(k)
    fixed = [(x+shift)%k for x in base]
    joint = rng.randrange(size)
    f = fixed.copy()
    for a,z in from_surplus(k,f[joint],shift,count):
        parent.extend([joint,len(f)])
        f.extend([a,z])
    assert f[:size] == fixed and len(f) == size+2*count
    for values in (f, [(f[i]+f[p])%k for i,p in enumerate(parent) if i]):
        counts = Counter(values)
        bins = [counts[i] for i in range(k)]
        assert max(bins)-min(bins) <= 1


def main():
    rng = Random(199154)
    holes = trees = 0
    for k in range(1, 102, 2):
        for y in range(k):
            verify_hole(k,y)
            holes += 1
        for i in range(3*k+1):
            check_tree(k,i,i,rng)
            trees += 1
    for k in (165,189,1001,15015,65535):
        for y in (0,1,3,5,7,15,21,33,55,59,63):
            verify_hole(k,y)
            holes += 1
    print("forbidden bins",holes,"whole trees",trees)


if __name__ == "__main__":
    main()

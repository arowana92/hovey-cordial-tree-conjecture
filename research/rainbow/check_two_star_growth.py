"""Audit the two-star criterion using direct endpoint sums and small exhaustive searches."""
from functools import lru_cache
from itertools import permutations
from math import gcd
from random import Random

from .two_star_growth import grow


@lru_cache(None)
def exact_first_block(k,first,shift):
    second = k-first
    for word in permutations(range(1,k)):
        y = word[0]
        weights = [(y+shift)%k]+[(y+t)%k for t in word[1:second]]+list(word[second:])
        if len(set(weights))==k-1:
            return True
    return False


def replay(k,s,t,a,b,d,word):
    vertices = [1]*k
    weights = [1]*k
    weights[d] = 0
    centers = {}
    mass = [0,0]
    assert len(word)==s+t
    for side,z in word:
        p = centers.get(side,(a,b)[side])
        centers.setdefault(side,z)
        mass[side] += 1
        vertices[z] += 1
        weights[(p+z)%k] += 1
        for bins in vertices,weights:
            assert max(bins)-min(bins)<=1
    assert mass==[s,t]


def longest_nonunit_run(k):
    longest = run = 0
    for i in range(1,k):
        run = run+1 if gcd(i,k)>1 else 0
        longest = max(longest,run)
    return longest


def main():
    positives = negatives = literal = 0
    rng = Random(1991)
    for k in range(2,65):
        if k<=8:
            pairs = [(s,t) for s in range(1,2*k+1) for t in range(1,2*k+1)]
        else:
            pairs = [(rng.randrange(1,4*k+1),rng.randrange(1,4*k+1)) for _ in range(80)]
        for s,t in pairs:
            for shift in (range(k) if k<=8 else (0,1,rng.randrange(k))):
                a,b = rng.randrange(k),rng.randrange(k)
                d = (a+b-shift)%k
                word = grow(k,s,t,a,b,d)
                if k<=8 and s+t>=k:
                    assert (word is not None)==any(exact_first_block(k,j,shift)
                        for j in range(max(1,k-t),min(k-1,s)+1))
                    literal += 1
                if word is None:
                    assert s+t>=k
                    negatives += 1
                else:
                    replay(k,s,t,a,b,d,word)
                    positives += 1
        # Construct the extremal example at each attainable run length.
        longest = longest_nonunit_run(k)
        for length in range(1,longest+1):
            lower = next(i for i in range(1,k-length+1)
                         if all(gcd(j,k)>1 for j in range(i,i+length)))
            assert grow(k,lower+length-1,k-lower,0,1,0) is None
        if k==26:
            assert longest==3 and grow(k,14,14,0,1,0) is None
        # Check the bound in the opposite direction on every pair of sizes
        # capable of failing. A full star of size k always allows a unit cut.
        for s in range(1,k):
            for t in range(max(1,k+longest-s),k):
                assert any(gcd(j,k)==1 for j in range(k-t,s+1))
    print('successful growth orders',positives,'obstructed inputs',negatives,
          'small exhaustive existence comparisons',literal,'moduli',63)


if __name__=='__main__':
    main()

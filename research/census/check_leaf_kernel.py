"""Compare integer matrix counts to direct injections and weight multiplicities."""

from collections import Counter
from itertools import permutations

from research.census.leaf_kernel import all_deficits, evaluate, spectrum
from research.rainbow.verify import rooted_shapes


def brute(parent, site, n):
    s = len(parent)-1
    neutral = 0
    marked = [0]*n
    for free in permutations(range(n), s):
        label = (0,*free)
        remaining = set(range(n)) - set(free)
        weights = [(label[i]+label[p]) % n for i,p in enumerate(parent[1:],1)]
        outside = [(label[site]+x) % n for x in remaining]
        bins = Counter(weights+outside)
        neutral += len(bins) == n
        for v,d in enumerate(weights):
            # Remove this specific edge; the n-1 other edges must be distinct.
            if len(set(weights[:v]+weights[v+1:]+outside)) == n-1:
                marked[d] += 1
    return neutral, marked


def main():
    checks = 0
    for s in range(1,5):
        for parent in rooted_shapes(s+1).values():
            for site in range(s+1):
                N = spectrum(parent, site)
                M = spectrum(parent, site, marked=True)
                combined = Counter(N)
                combined.update(M)
                assert all_deficits(combined, s) is not None
                for n in range(s,s+4):
                    neutral, marked = brute(parent, site, n)
                    assert neutral == evaluate(N,n)
                    assert marked == [evaluate(M,n,d) for d in range(n)]
                    checks += n+1
    N = spectrum((-1,0,0,2,3), 1)
    # Check the entire symbolic expression before testing individual values.
    assert N == {(0, (), 0): -1, (0, ((2,2),), 0): -1,
                 (0, ((4,4),), 0): 1, (0, ((5,5),), 0): 1}
    for n in range(4,5000):
        assert evaluate(N,n) == 2*(n%4==0) + 4*(n%5==0)
    print(f"{checks} exact modular counts independently enumerated, "
          "and the four-variable expression checked symbolically.")


if __name__ == "__main__":
    main()

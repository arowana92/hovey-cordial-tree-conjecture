"""Compare the degree classification to exact permutation sums on every small rooted tree."""

from functools import lru_cache
from math import gcd

from research.rainbow.verify import rooted_shapes


@lru_cache(None)
def attainable(coefficients):
    k = len(coefficients)
    full = (1 << k) - 1
    # A state records all sums after assigning the indicated set of distinct labels.
    sums = [0] * (1 << k)
    sums[0] = 1
    for used in range(full):
        a = coefficients[bin(used).count("1")]
        remaining = full ^ used
        while remaining:
            bit = remaining & -remaining
            remaining -= bit
            offset = a*(bit.bit_length()-1) % k
            moved = sums[used] << offset
            sums[used | bit] |= (moved & full) | (moved >> k)
    return sums[-1]


def check():
    roots = pairs = excluded = ruled_out = 0
    for k in range(5,13):
        for par in rooted_shapes(k+1).values():
            roots += 1
            deg = [0]*(k+1)
            for v in range(1,k+1):
                deg[v] += 1
                deg[par[v]] += 1
            possible = False
            for mate in range(1,k+1):
                pairs += 1
                def vertex(v):
                    return 0 if v == mate else v
                edges = [tuple(sorted((vertex(v),vertex(par[v])))) for v in range(1,k+1)]
                simple = len(set(edges)) == k
                degrees = {vertex(v): 0 for v in range(k+1)}
                for v,w in edges:
                    degrees[v] += 1
                    degrees[w] += 1
                coeff = sorted(a-1 for a in degrees.values())
                positive = [a for a in coeff if a]
                bad = ((coeff == [1]*k and k % 2 == 0)
                       or (coeff == [0]+[1]*(k-2)+[2] and k % 2 == 1)
                       or (len(positive)==2 and gcd(positive[0],k)==1))
                exact = (attainable(tuple(coeff)) & 1) != 0
                assert exact != bad
                excluded += bad
                possible |= simple and exact
            children = [v for v in range(1,k+1) if par[v]==0]
            structural = (len(children)==2 and all(deg[v]>=2 for v in children)
                          and sum(d>=2 for d in deg)==3
                          and all(gcd(deg[v]-1,k)==1 for v in children))
            assert possible != structural
            ruled_out += structural
    print(f"{roots} rooted shapes, {pairs} specified pairs, {excluded} moment exclusions, "
          f"{ruled_out} roots excluded by moment or parallel edges.")


if __name__ == '__main__':
    check()

"""Verify the determinant formula by directly trying disjoint sets of leaf labels."""

from itertools import combinations, permutations

from research.biased.two_sites import short_arm_quadratic, short_arm_sum, two_site_counts
from research.prime.verify_templates import primes_through
from research.rainbow.verify import rooted_shapes


def direct(parents, second, p):
    h = len(parents)
    counts = [0]*(p-h+1)
    for row in permutations(range(2,p),h-2):
        x = list(row)
        x.insert(0,0)
        x.insert(second,1)
        free = sorted(set(range(p))-set(x))
        core = {x[v]:(x[v]+x[u])%p for v,u in enumerate(parents) if v}
        for b in range(len(free)+1):
            for chosen in combinations(free,b):
                image = {**core, **{z:z for z in free}}
                for z in chosen:
                    image[z] = (z+1)%p
                weights = set(image.values())
                if len(weights) != p-1:
                    continue
                image[0], = set(range(p))-weights
                inversions = sum(image[u]>image[v] for v in range(p) for u in range(v))
                counts[b] += (-1)**inversions
    return counts


if __name__ == "__main__":
    comparisons = 0
    for h in range(2,6):
        for parent in rooted_shapes(h).values():
            for second in range(1,h):
                for n in range(h,10):
                    result = two_site_counts(parent,second,n)
                    assert result == direct(parent,second,n)
                    comparisons += len(result)
    print(f"{comparisons} determinant coefficients checked against direct subsets and endpoint sums")

    proofs = 0
    for p in primes_through(73):
        if p < 5:
            continue
        for kind, parent, second in [
            ("distance two", [-1,0,1], 2),
            ("one middle leaf", [-1,0,1,1], 2),
            ("distance three", [-1,0,1,2], 3),
            ("adjacent with arm", [-1,0,0,2], 1),
        ]:
            values = two_site_counts(parent,second,p)
            for b, z in enumerate(values):
                a = p-len(parent)-b
                if kind != "adjacent with arm" and b > a:
                    continue
                if kind == "distance two":
                    expected = -1
                elif kind == "one middle leaf":
                    expected = b+3-p if b%2 else b+2
                elif kind == "distance three":
                    expected = b+1
                else:
                    expected = short_arm_sum(p,b)
                    assert 2*expected%p == short_arm_quadratic(p,b)
                assert z == (-1)**b*expected, (kind,p,a,b,z,expected)
                proofs += 1
    print(f"{proofs} exact signed counts checked for the four families")

    for p in primes_through(5000):
        if p < 5:
            continue
        exceptional = [b for b in range(p-3) if not short_arm_quadratic(p,b)]
        assert len(exceptional) <= 2 and all(y>x+1 for x,y in zip(exceptional,exceptional[1:]))
        assert not exceptional or (min(exceptional)>0 and max(exceptional)<p-4)
        if p%24 in (5,19):
            assert not exceptional
    print("Exceptional population bounds checked at every prime through 5000")

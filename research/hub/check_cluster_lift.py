"""Recount lifted labelings on the original uncontracted trees."""

from collections import Counter
from math import gcd
from random import Random

from research.hub.cluster_lift import lift
from research.hub.linear_hub_batches import construct as batches
from research.hub.universal_hub import construct as integer
from research.rainbow.verify import rooted_shapes


def site_digits(cluster,d):
    values,_,_ = integer(cluster)
    if len({x % d for x in values}) != len(values):
        return None
    unit = next((x for x in values if gcd(x,d) == 1),None)
    if unit is None:
        return None
    return [x*pow(unit,-1,d) % d for x in values]


def audit(tree,digits,quotient,q,d,counts):
    parents,labels = lift(tree,digits,quotient,q,d,counts)
    k,s = q*d,len(digits)
    assert parents[:len(tree)] == tree and len(parents) == k
    assert labels[:s] == [q*x for x in digits]
    assert set(labels) == set(range(k))
    assert Counter(parents[len(tree):]) == Counter({v:n for v,n in enumerate(counts) if n})
    weights = [(labels[v]+labels[parents[v]]) % k for v in range(1,k)]
    assert len(weights) == len(set(weights)) == k-1
    missing, = set(range(k))-set(weights)
    return missing//q


def main():
    rng = Random(872351)
    cases = vertices = repeated = sharp = 0
    gaps = set()
    clusters = [([-1,0],2),([-1,0],4),([-1,0,0],3),([-1,0,0,0],6),
                ([-1,0,1,2],7),([-1,0,0,1,1],11)]
    for cluster,d in clusters:
        digits = site_digits(cluster,d)
        assert digits is not None
        s = len(cluster)
        for n in range(3,8):
            for raw in rooted_shapes(n).values():
                if not any(p > 0 for p in raw):
                    continue
                x,g,_ = integer(raw)
                assert g != 0
                for modulus in (17,24):
                    q = max(modulus,3*n+2)
                    while len({v % q for v in x}) < n:
                        q += 1
                    quotient = [v % q for v in x]
                    tree = list(cluster)+[rng.randrange(s) if p == 0 else p+s-1 for p in raw[1:]]
                    occupied = d*n-len(tree)
                    spare = q*d-len(tree)-2*occupied
                    assert spare >= 0
                    for mode in range(3):
                        counts = [0]*s
                        counts[digits.index(0)] = counts[digits.index(1)] = occupied
                        if mode < 2:
                            counts[digits.index(mode)] += spare
                        else:
                            for _ in range(spare):
                                counts[rng.randrange(s)] += 1
                        gaps.add((d,audit(tree,digits,quotient,q,d,counts)))
                        vertices += d*q
                        cases += 1
                    if s == 2 and gcd(q,d) == 1:
                        branches = sum(p == 1 for p in tree[2:])
                        forced = (d-1)*branches
                        assert forced < occupied
                        for extra in range(d):
                            second = forced+extra
                            counts = [q*d-len(tree)-second,second]
                            audit(tree,digits,quotient,q,d,counts)
                            sharp += 1

    # Without withholding a pair, all these contracted trees have only the root left.
    for n in range(2,9):
        for raw in rooted_shapes(n).values():
            tree = [-1,0]+[p+1 for p in raw[1:]]+[0]+[p+n+1 for p in raw[1:]]
            for q in (65536,99991):
                labels,g,_ = batches(tree,q,nonzero_gap=True)
                weights = {(labels[v]+labels[p]) % q for v,p in enumerate(tree) if v}
                assert labels[0] == 0 and g != 0 and len(set(labels)) == len(tree)
                assert len(weights) == len(tree)-1 and weights == set(labels)-{g}
                repeated += 1
    assert {d for d,_ in gaps} == {d for _,d in clusters}
    print(f"{cases:,} whole-tree lifts, {vertices:,} vertex assignments, "
          f"{len(gaps)} distinct divisor/gap-digit pairs; {repeated:,} nonzero-gap certificates on paired trees.")
    print(f"{sharp:,} coprime two-site lifts starting at the exact forced population.")


if __name__ == '__main__':
    main()

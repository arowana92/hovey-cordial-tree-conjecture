"""Recompute boundary edges and complete histograms on trees with distinct paired sites."""

from collections import Counter
from itertools import product
from random import Random

from research.hub.paired_stars import construct, root_values, select_anchors


def main():
    identities = 0
    for k in range(2,9):
        for a,q,c,h,d in product(range(k),repeat=5):
            xs,ys = root_values(a,q,c,h,d)
            actual = [(p+x) % k for p,x in zip((a,q,c,h,q),xs)]
            actual.extend((x+y) % k for x,y in zip(xs[1:],ys))
            assert Counter(actual) == Counter(x % k for x in xs+ys)
            identities += 1
    rng = Random(512)
    selections = 0
    for k in (32,33,64,75,91,101):
        labels = list(range(k))
        for _ in range(400):
            pool = rng.sample(range(k),32)
            s,t,g = rng.randrange(k),rng.randrange(1,k),rng.randrange(k)
            for j in range(6):
                a,q,c,h = select_anchors(pool,labels,s,t,g,k)
                plus = {x % k for x in (0,a,-c,a+q)}
                minus = {x % k for x in (-a-h-q,-a,-a-q)}
                assert len(plus)==4 and len(minus)==3
                assert t not in plus and s not in minus and g not in minus
                selections += 1
            assert len(pool)==8
    cases = edges = repairs = root_cycles = leaf_cycles = 0
    for near,far in ((65520,262140),(65521,262139),(65536,262144)):
        for distant in (False,True):
            k = far if distant else near
            for m,n in ((1,1),(1,3),(2,4)):
                number = 24*(20 if distant else 12)+8
                core = [-1]
                if distant:
                    core.extend(range(number))
                else:
                    core.extend([0]*number)
                anchors = list(range(1,number+1)) if distant else list(range(number))
                second = number if distant else 1
                counts = {second:23}
                counts[0] = k-len(core)-len(anchors)*(m+n+2)-23
                parents,labels,gap,stats = construct(core,counts,anchors,m,n,k,range(k))
                expected = list(core)
                for v in anchors:
                    for size in (m,n):
                        r = len(expected)
                        expected.extend([v]+[r]*size)
                assert parents[:len(expected)] == expected
                assert Counter(parents[len(expected):]) == Counter(counts)
                assert len(labels) == len(parents) == k and set(labels) == set(range(k))
                sums = Counter((labels[v]+labels[p]) % k for v,p in enumerate(parents) if v)
                assert set(sums) == set(range(k))-{gap} and max(sums.values()) == 1
                root_cycles += stats['root cycles']
                leaf_cycles += stats['leaf cycles']
                repairs += stats['repairs']
                cases += 1
                edges += k-1
    assert min(repairs,root_cycles,leaf_cycles)>0
    print(f"{identities:,} actual nine-edge histograms and {selections:,} group selections.")
    print(f"{cases} expanded trees with {edges:,} actual sums, {repairs} surplus repairs, "
          f"{root_cycles} auxiliary-root cycles and {leaf_cycles} leaf cycles.")


if __name__ == '__main__':
    main()

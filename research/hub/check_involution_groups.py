"""Verify complete involution packets and original edge sums of the even-order construction."""

from collections import Counter
from itertools import product
from random import Random

from research.hub.check_odd_branch_groups import append_branch
from research.hub.involution_groups import construct, packet
from research.hub.signed_tree import BLOCKS
from research.rainbow.verify import rooted_shapes


def counts(tree,labels,k,gap):
    vertices = Counter(labels)
    edges = Counter((labels[v]+labels[p]) % k for v,p in enumerate(tree) if v)
    assert len(vertices) == len(labels) == len(tree)
    assert vertices == edges+Counter([gap])


def main():
    rng = Random(16381)
    for _,entries,_ in BLOCKS.values():
        slopes = [(sgn*a,sgn*b) for a,b in entries for sgn in (-1,1)]
        for i,(a,b) in enumerate(slopes):
            assert a and all(a != c or abs(b-e) == 1 for c,e in slopes[:i])
    checked = edges = 0
    for n in range(1,10):
        for branch in rooted_shapes(n).values():
            for k in (65536,98310):
                p = k//2
                forbidden = {0,p,1,13,512,k-9}
                copies = packet(branch,k,set(forbidden),rng)
                flat = [v for row in copies for v in row]
                actual = [(row[v]+(p if u < 0 else row[u])) % k
                          for row in copies for v,u in enumerate(branch)]
                assert len(set(flat)) == 12*n and set(flat).isdisjoint(forbidden)
                assert Counter(actual) == Counter(flat)
                checked += 1
                edges += len(actual)

    modes = Counter()
    virtual = parities = 0
    for height in (2,3,4):
        for sides in product(range(5),repeat=height-1):
            branch = [-1]+list(range(height-1))
            for v,n in enumerate(sides):
                branch.extend([v]*n)
            for m in (0,1):
                tree = [-1,0]
                for _ in range(17):
                    append_branch(tree,1,branch)
                append_branch(tree,0,[-1,0,0,1])
                q = 2**24 if m == 0 else 10000019
                labels,gap,mode = construct(tree,q,m)
                counts(tree+[1]*m,labels,2*q,gap)
                assert labels[:2] == [0,q] and mode == f'height-{height}'
                modes[mode] += 1
                if height == 4:
                    v = min(sides[0],max(0,sides[2]-sides[1]))
                    virtual += v
                    parities += v % 2
    for tag,branch,copies,m in (('fork',[-1,0,0,1,2],18,0),
                                ('deep',[-1]+list(range(39)),4,1),
                                ('bounded',[-1,0,1],1,16)):
        tree = [-1,0]
        for _ in range(copies):
            append_branch(tree,1,branch)
        for _ in range(28):
            append_branch(tree,0,[-1,0,1])
        q = 200003
        labels,gap,mode = construct(tree,q,m)
        counts(tree+[1]*m,labels,2*q,gap)
        assert labels[:2] == [0,q] and mode == tag
        modes[tag] += 1
    assert virtual > parities > 0
    print(f"{checked:,} neutral twelve-copy packets, {edges:,} actual edges, "
          "including every rooted branch through order nine.")
    print(f"{sum(modes.values())} full two-site certificates across {len(modes)} cases, "
          f"{virtual} virtual jumps and {parities} odd virtual counts.")


if __name__ == '__main__':
    main()

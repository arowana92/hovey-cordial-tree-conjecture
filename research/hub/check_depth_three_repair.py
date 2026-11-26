"""Rebuild the saved branches and verify both complete histograms and the pruning argument."""

from collections import Counter
from itertools import product

from research.hub.depth_three_repair import construct, double_rows, triple_rows
from research.rainbow.verify import rooted_shapes


def tables():
    checked = 0
    for k in range(2,15):
        for a,b,c,d in product(range(k),repeat=4):
            rows = triple_rows(a,b,c,d)
            sums = [v+w for p,row in zip((a,b,c),rows) for v,w in zip((p,)+row,row)]
            assert Counter(x % k for x in sums) == Counter(x % k for row in rows for x in row)
            checked += 1
        for d,f in product(range(k),repeat=2):
            rows = double_rows(f,d)
            sums = [v+w for row in rows for v,w in zip((0,)+row,row)]
            assert Counter(x % k for x in sums) == Counter(x % k for row in rows for x in row)
            checked += 1
    return checked


def prune_check(tree):
    kids = [[] for _ in tree]
    for v,p in enumerate(tree[1:],1):
        kids[p].append(v)
    height = [0]*len(tree)
    for v in reversed(range(len(tree))):
        height[v] = max((height[w]+1 for w in kids[v]),default=0)
    live = set(range(len(tree)))
    for _ in range(2):
        live -= {v for v in live if not live.intersection(kids[v])}
    tips = {v for v in live if not live.intersection(kids[v])}
    assert tips == {v for v,h in enumerate(height) if h == 2}
    seen = set()
    cases = set()
    for v in tips:
        stars = [w for w in kids[v] if kids[w]]
        assert stars and all(not kids[u] for w in stars for u in kids[w])
        packet = {v,*kids[v],*(u for w in stars for u in kids[w])}
        assert seen.isdisjoint(packet)
        seen.update(packet)
        cases.add('pair' if len(stars)>=2 else 'single')
    assert all(tree[v] not in seen for v in tips)
    return cases


def main():
    identities = tables()
    shapes = 0
    types = set()
    for n in range(1,12):
        for tree in rooted_shapes(n).values():
            types.update(prune_check(tree))
            shapes += 1
    assert types == {'pair','single'}
    cases = edges = repairs = cycles = 0
    for k in (65520,65521,65536):
        for kind in ('zero','common','distinct','distant'):
            for l,m in ((0,1),(2,3),(5,1),(2,2)):
                number = 30*(9 if kind == 'distant' else 5)
                core = [-1]+(list(range(number)) if kind == 'distant' else [0]*number)
                suppliers = ([0]*number if kind=='zero' else
                             [1]*number if kind=='common' else list(range(1,number+1)))
                site = number if kind == 'distant' else 1
                counts = {0:k-len(core)-number*(2+l+m)-23,site:23}
                parents,labels,gap,stats = construct(core,counts,suppliers,l,m,k,range(k))
                expected = list(core)
                for v in suppliers:
                    r = len(expected)
                    expected.extend([v,r]+[r+1]*m+[r]*l)
                assert expected == parents[:len(expected)]
                assert Counter(parents[len(expected):]) == Counter(counts)
                assert len(parents) == len(labels) == k and set(labels) == set(range(k))
                weights = Counter((labels[v]+labels[p]) % k for v,p in enumerate(parents) if v)
                assert set(weights) == set(range(k))-{gap} and max(weights.values()) == 1
                cases += 1
                edges += k-1
                repairs += stats['repairs']
                cycles += stats['cycles']
    assert repairs and cycles
    print(f"{identities:,} actual branch identities, two pruning rounds on {shapes:,} rooted trees.")
    print(f"{cases} complete trees and {edges:,} actual endpoint sums, {repairs} repairs and {cycles} erased cycles.")


if __name__ == '__main__':
    main()

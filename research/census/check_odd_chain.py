"""Audit joined copies by direct graph reconstruction and ordinary endpoint sums."""

from collections import Counter
from itertools import permutations

from research.census.odd_chain import odd_join
from research.rainbow.verify import rooted_shapes


def piece_labels(par):
    for f in permutations(range(len(par))):
        w = {f[v]+f[p] for v,p in enumerate(par[1:],1)}
        if len(w) == len(par)-1 and max(w)-min(w)+1 == len(w):
            return f,min(w),max(w)
    raise AssertionError("no base labeling")


def quotients():
    for q in [3,5,7]:
        t = q//2
        for par in rooted_shapes(q).values():
            for f in permutations(range(q)):
                if any((f[i] <= t) == (f[u] <= t) for i,u in enumerate(par[1:],1)):
                    continue
                if len({f[i]+f[u] for i,u in enumerate(par[1:],1)}) == q-1:
                    yield par,f
                    break


if __name__ == "__main__":
    qs = list(quotients())
    stats = Counter()
    for n in range(2,9):
        for par in rooted_shapes(n).values():
            f,lo,hi = piece_labels(par)
            parity = [0]*n
            for v,u in enumerate(par[1:],1):
                parity[v] = 1-parity[u]
            for a in range(n):
                for b in range(a,n):
                    if f[a]+f[b] not in (lo-1,hi+1):
                        continue
                    for Q,g in qs:
                        q = len(Q)
                        labels,actual = odd_join(par,f,Q,g,(a,b))
                        port = [a if 2*x < q else b for x in g]
                        expected = {(s*n+u,s*n+i) for s in range(q) for i,u in enumerate(par[1:],1)}
                        expected.update((u*n+port[u],i*n+port[i]) for i,u in enumerate(Q[1:],1))
                        assert expected == {tuple(sorted(pair)) for pair in actual}
                        assert len(expected) == q*n-1 and sorted(labels) == list(range(q*n))
                        weights = sorted(labels[i]+labels[j] for i,j in expected)
                        assert weights == list(range(weights[0],weights[0]+q*n-1))
                        stats[parity[a]==parity[b],f[a]+f[b]==lo-1] += 1
    print(f"{len(qs)} balanced quotient labelings, {sum(stats.values())} joined trees")
    print(f"Cases by same-side ports and lower-end sum: {dict(sorted(stats.items()))}")

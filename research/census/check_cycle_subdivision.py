"""Recompute vertex and edge histograms across actual edge replacements."""
from collections import Counter
from itertools import permutations
from random import Random

from .cycle_subdivision import half_weights, insert, interval_cycle, long_divisible, pendant


def balanced(values,k):
    counts = Counter(values)
    bins = [counts[i] for i in range(k)]
    return max(bins)-min(bins) <= 1


def edge_rows():
    tests = 0
    for k in range(5,23):
        for a in range(k):
            for b in range(a,k):
                for t in range(3*k+3):
                    forbidden = (t == 1 and a == b == 0) or (k%4 == 2 and t%(2*k) == k)
                    try:
                        row = insert(k,a,b,0,t)
                    except ValueError:
                        assert forbidden
                        continue
                    assert not forbidden and len(row) == t
                    weights = Counter((x+y)%k for x,y in zip([a]+row,row+[b]))
                    weights[(a+b)%k] -= 1
                    freq = [weights[i] for i in range(k)]
                    assert balanced([0]+row,k) and max(freq)-min(freq)<=1
                    tests += 1
    return tests


def tree(k, t, trial, rng):
    divisible = trial%3 == 1
    endpath = trial%3 == 2
    n = k*(1+trial%2)+(not divisible)
    # Both path and star bases have known cordial labelings at every order.
    if trial%4 < 2:
        edges = [(i-1,i) for i in range(1,n)]
        f = [(i//2+(i%2)*((n+1)//2))%k for i in range(n)]
    else:
        edges = [(0,i) for i in range(1,n)]
        f = [i%k for i in range(n)]
    shift = rng.randrange(k)
    f = [(x+shift)%k for x in f]
    bins = Counter((f[u]+f[v])%k for u,v in edges)
    fixed = f.copy()
    if endpath:
        u = rng.randrange(n)
        row = pendant(k,f[u],shift,t)
        chain = [u,*range(n,n+t)]
    else:
        index = rng.randrange(len(edges))
        u,v = edges.pop(index)
        if divisible:
            d = min(range(k),key=lambda i:bins[i])
            t += k
            inadmissible = k%2 == 0 and t%k == 1 and (d+(t//k)*(k//2))%2
            try:
                row = long_divisible(k,f[u],f[v],d,t)
            except ValueError:
                assert inadmissible
                return 0
            assert not inadmissible
        else:
            if t == 1 and f[u] == f[v] == shift or k%4 == 2 and t%(2*k) == k:
                return 0
            row = insert(k,f[u],f[v],shift,t)
        chain = [u,*range(n,n+t),v]
    f.extend(row)
    edges.extend(zip(chain,chain[1:]))
    assert len(f) == n+t and len(edges) == len(f)-1 and f[:n] == fixed
    assert all(0 <= x < k for x in f)
    assert balanced(f,k) and balanced([(f[u]+f[v])%k for u,v in edges],k)
    return 1


def six_obstructions():
    # All possible six-label vertex multisets for a fixed old surplus zero,
    # including every way to shift it. Test each actual endpoint sum.
    k = 6
    count = 0
    for surplus in range(k):
        labels = list(range(1,k))+[surplus]
        for row in set(permutations(labels)):
            internal = [(a+b)%k for a,b in zip(row,row[1:])]
            for a in range(k):
                for b in range(a,k):
                    need = [1+(i==(a+b)%k) for i in range(k)]
                    w = internal+[(a+row[0])%k,(b+row[-1])%k]
                    assert [w.count(i) for i in range(k)] != need
                    count += 1
    return count


def main():
    arrays = 0
    for n in range(3,1025):
        p = interval_cycle(n)
        w = [a+b for a,b in zip(p,p[1:]+p[:1])]
        assert sorted(p) == list(range(n)) and len(set(w)) == n
        assert max(w)-min(w) == n-(n%2)
        arrays += 1
        if n%2 == 0 and n >= 6:
            for r in (0,1,n//2,n-1):
                p = half_weights(n,r)
                assert sorted(p) == list(range(n))
                c = Counter((a+b)%n for a,b in zip(p,p[1:]+p[:1]))
                assert all(c[j] == 1+(j==r)-(j==(r+n//2)%n) for j in range(n))
                arrays += 1
    rows = edge_rows()
    rng = Random(199101)
    trees = 0
    for k in list(range(5,91))+[125,126,255,256,1001,4096]:
        for trial in range(72):
            t = rng.choice([1,2,3,k-2,k-1,k,k+1,k+2,2*k-1,2*k,2*k+1,3*k+3,rng.randrange(5*k)])
            trees += tree(k,t,trial,rng)
    print("cycle arrays",arrays,"fixed endpoint rows",rows,"whole trees",trees,
          "six-label negative checks",six_obstructions())


if __name__ == "__main__":
    main()

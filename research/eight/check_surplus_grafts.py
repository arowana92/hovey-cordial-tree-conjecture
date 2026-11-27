"""Independent graph sums for constrained stars and complete eight-label grafts."""
from collections import Counter
from itertools import combinations
from math import gcd
from pathlib import Path
from random import Random

from .generate import forests,parent_vector
from .lean_tables import collect
from .surplus_grafts import extend,first_seven,star


def check_star(k,c,p,brute):
    row = star(k,c,p)
    if brute:
        # Labels of sibling tips and of the singletons can be permuted.
        xs = set(range(1,k))
        possible = False
        for a in xs:
            for kids in combinations(sorted(xs-{a}),c):
                singles = xs-{a}-set(kids)
                ws = singles | {(a+p)%k} | {(a+x)%k for x in kids}
                if len(ws)==k-1:
                    possible = True
                    break
            if possible:
                break
        assert possible==(row is not None)
    assert (p%gcd(c+1,k)==0)==(row is not None)
    if row is not None:
        a,kids,singles = row
        assert len(kids)==c and sorted(kids+singles+[a])==list(range(1,k))
        weights = [(p+a)%k]+[(a+x)%k for x in kids]+singles
        assert len(set(weights))==k-1


def fixed_stars():
    total = 0
    for k in range(3,10):
        xs = set(range(1,k))
        for a in xs:
            for c in range(1,k-1):
                for b in range(k):
                    allowed = set()
                    for children in combinations(sorted(xs-{a}),c):
                        singles = xs-{a}-set(children)
                        edges = {(x+b)%k for x in singles}|{(a+x)%k for x in children}
                        if len(edges)==k-2:
                            allowed.update((w-a)%k for w in set(range(k))-edges)
                    for p in range(k):
                        row = star(k,c,p,b,a)
                        assert (row is not None)==(p in allowed)
                        if row is not None:
                            center,kids,singles = row
                            assert center==a and len(kids)==c
                            assert sorted([a,*kids,*singles])==list(range(1,k))
                            w = [(p+a)%k]+[(x+a)%k for x in kids]+[(x+b)%k for x in singles]
                            assert len(set(w))==k-1
                        total += 1
    return total


def main():
    rng = Random(812607)
    stars = brute = trees = shapes = 0
    for k in range(3,34):
        for c in range(1,k-1):
            for p in range(k):
                check_star(k,c,p,k<=12)
                stars += 1
                brute += k<=12
    for k in (36,64,81,91,127,252,1001,4096):
        for _ in range(20):
            check_star(k,rng.randrange(1,k-1),rng.randrange(k),False)
            stars += 1
    for f in forests(8):
        p = parent_vector(f,[0]*len(f))
        selected = first_seven(p)
        assert len(set(selected))==7
        assert all(p[i]<0 or p[i] in selected for i in selected)
        counts = sorted(Counter(p[i] for i in selected if p[i]>=0).values())
        assert counts not in ([1],[3],[5])
        shapes += 1
    levels = collect(Path(__file__).with_name('certificate.jsonl.gz'))
    for n in list(range(7))+list(range(8,88)):
        for j in range(6):
            q = 1+j%3
            order = 8*q+1
            old = ([i%8 for i in range(order)] if j%2 else
                   [(i//2+(i%2)*((order+1)//2))%8 for i in range(order)])
            old_edges = [(0,i) if j%2 else (i-1,i) for i in range(1,order)]
            shift = rng.randrange(8)
            old = [(x+shift)%8 for x in old]
            p = [rng.randrange(-order,i) for i in range(n)]
            new = extend(old,p,levels)
            assert len(new)==n
            f = old+new
            edges = old_edges+[(order+i,order+x if x>=0 else -1-x) for i,x in enumerate(p)]
            for h in (Counter(f),Counter((f[a]+f[b])%8 for a,b in edges)):
                bins = [h[x] for x in range(8)]
                assert max(bins)-min(bins)<=1
            trees += 1
    print('star inputs',stars,'brute-force comparisons',brute,
          'eight-vertex forests',shapes,'complete grafts',trees,'fixed stars',fixed_stars())


if __name__=='__main__':
    main()

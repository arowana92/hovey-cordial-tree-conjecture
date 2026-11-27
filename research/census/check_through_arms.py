"""Build every oriented 26-vertex replacement and count its actual endpoint sums."""
from itertools import product
from math import gcd
from pathlib import Path
import sys


def verify(path):
    k = 26
    rows = {}
    for line in Path(path).read_text().splitlines():
        l, r, m, h, *labels = map(int, line.split())
        assert 0 <= l <= r and m >= 1 and 1+l+r+m == k
        assert h in (0, 1, 2, 13) and (l,r,m,h) not in rows
        assert len(labels) == k and set(labels) == set(range(k))
        rows[l,r,m,h] = labels
    assert len(rows) == 676
    units = [u for u in range(k) if gcd(u,k)==1]
    normalize = {}
    for h in (0, 1, 2, 13):
        for u in units:
            normalize[u*h % k] = h,u
    checks = 0
    for m in range(1,k):
        for left in range(k-m):
            right = k-1-m-left
            l,r = sorted((left,right))
            for a,b in product(range(k),repeat=2):
                x,y = (a,b) if left<=right else (b,a)
                h,u = normalize[(y-x)%k]
                free = [(x+u*v)%k for v in rows[l,r,m,h]]
                assert len(set(free)) == k
                center = free[0]
                paths = [[center]+free[1:1+l]+[x], [center]+free[1+l:1+l+r]+[y],
                         [center]+free[1+l+r:]]
                counts = [0]*k
                for arm in paths:
                    for v,w in zip(arm,arm[1:]):
                        counts[(v+w)%k] += 1
                counts[(a+b)%k] -= 1
                assert counts == [1]*k
                checks += 1
    print('representatives',len(rows),'oriented replacements',checks)


if __name__ == '__main__':
    verify(sys.argv[1])

"""Check marked-leaf frequencies and doubled trees on the original edges."""

from random import Random

from .check_matching_expansion import check
from .marked_leaf import cut, label
from .near_matching import label as double
from .rainbow.verify import rooted_shapes


def verify(p,m,mark):
    f = label(p,m,mark)
    a,_ = check(f,[(v,p[v]) for v in range(1,len(p))],m)
    assert a[f[mark]] == max(a)


def path_staircases():
    # Paths test the centroid suffix when neither end can supply enough leaves.
    # A reversed identifier order alternates the marked leaf inside/outside the core.
    stats = [0,0]
    for m in range(4,31):
        for extra in (3,4,5,6):
            n = m+extra
            p = [-1]+list(range(n-1))
            g = {i:[j for j in (i-1,i+1) if 0 <= j < n] for i in range(n)}
            t = (n-1)%m
            if t:
                outside = cut(g,t)
                for mark in (0,n-1):
                    verify(p,m,mark)
                    stats[int(mark in outside)] += 1
    return stats


def main():
    ncases = 0
    for n in range(2,9):
        for p in rooted_shapes(n).values():
            for v in range(n):
                if p.count(v)+int(v>0) == 1:
                    for m in range(2,11):
                        verify(p,m,v)
                        ncases += 1
    rng = Random(501991)
    random_marks = 0
    for m in (6,8,9,12,15,17,19,21,23,25):
        for _ in range(20):
            n = m+rng.randrange(2,13)
            p = [-1]+[rng.randrange(v) for v in range(1,n)]
            leaves = [v for v in range(n) if p.count(v)+int(v>0) == 1]
            verify(p,m,rng.choice(leaves))
            random_marks += 1
    matched = 0
    for m in (9,15,17,19,21,23,25,27,29):
        # Use expanded paths for the larger bounded-leaf cases.
        for s in [m,m+1,m+2,m+4,m+6]:
            for _ in range(2):
                p = [-1]
                site = 0
                for _ in range(s):
                    p.extend([site,len(p)])
                    site = len(p)-1
                # Reverse selected match edges' attachment choices on smaller quotients.
                if s <= 18:
                    site = 0
                    p = [-1]
                    for _ in range(s):
                        p.extend([site,len(p)])
                        site = len(p)-1-rng.randrange(2)
                f = double(p,m)
                check(f,[(i,p[i]) for i in range(1,len(p))],2*m)
                matched += 1
    print(f"{ncases} marked small trees, retained/exterior path marks {path_staircases()}, "
          f"{random_marks} random marked trees, {matched} full matching lifts")


if __name__ == "__main__":
    main()

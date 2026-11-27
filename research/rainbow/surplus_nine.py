"""Exact small surplus packets and the residual two-star case at modulus nine."""
from collections import Counter
from itertools import combinations

from research.eight.surplus import mask_solver,shape
from .generate import boundary_orbits,forests,parent_vector,rainbow


def two_stars(a,b,d):
    """Return labels in center, two tips, center, five tips order."""
    for x in range(9):
        for y in range(9):
            if x==y:
                continue
            rest = set(range(9))-{x,y}
            for two in combinations(sorted(rest),2):
                five = sorted(rest-set(two))
                w = [(a+x)%9,(b+y)%9]+[(v+x)%9 for v in two]+[(v+y)%9 for v in five]
                counts = Counter(w)
                if counts[d]>=1 and all(counts[i]<=1+(i==d) for i in range(9)):
                    return [x,*two,y,*five]
    raise ValueError("no divisible-core two-star witness")


def main():
    levels = {():()}
    for r in range(1,9):
        following = {}
        for ps in levels.values():
            for p in range(-9,r-1):
                grown = ps+(p,)
                following.setdefault(shape(grown,9),grown)
        levels = following
    solve = mask_solver(8,9)
    failures = set()
    for key,ps in levels.items():
        f = solve(ps)
        if f is None:
            failures.add(key)
        else:
            assert len(set(f))==8 and 0 not in f
            assert len({(f[i]+(f[p] if p>=0 else -1-p))%9 for i,p in enumerate(ps)})==8
    expected = set()
    for c in (2,5):
        for p in (1,2,4,5,7,8):
            singles = 7-c
            expected.add(shape([-1]*singles+[-1-p]+[singles]*c,9))
    assert failures==expected
    all_shapes = set()
    independent = set()
    rows = 0
    for forest in forests(8):
        for colors in boundary_orbits(forest,9):
            ps = parent_vector(forest,colors)
            orbit = {shape(parent_vector(forest,[u*c%9 for c in colors]),9)
                     for u in (1,2,4,5,7,8)}
            assert orbit.isdisjoint(all_shapes)
            all_shapes.update(orbit)
            try:
                rainbow(ps,9)
            except ValueError:
                independent.update(orbit)
            rows += 1
    assert all_shapes==levels.keys() and independent==failures
    twins = 0
    ps = (-1,0,0,-2,3,3,3,3,3)
    for a in range(9):
        for b in range(9):
            for d in range(9):
                f = two_stars(a,b,d)
                assert sorted(f)==list(range(9))
                e = Counter((f[j]+(f[p] if p>=0 else (a,b)[-1-p]))%9 for j,p in enumerate(ps))
                bins = [e[i]+(i!=d) for i in range(9)]
                assert sorted(bins)==[1]+[2]*8
                twins += 1
    print('colored forests',len(levels),'unit orbits',rows,'raw failures',len(failures),
          'two-star boundary and deficit assignments',twins)


if __name__=='__main__':
    main()

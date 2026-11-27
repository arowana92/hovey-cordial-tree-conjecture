"""Classify all one-surplus attachments through seven free vertices at modulus eight."""
from functools import lru_cache
from itertools import permutations

from .verify import components, key
from research.rainbow.generate import boundary_orbits, forests, parent_vector, rainbow


def shape(parents):
    return key(components(parents),0,8)


def mask_solver(r):
    assignments = list(permutations(range(1,8),r))
    all_bits = (1<<len(assignments))-1

    @lru_cache(None)
    def weights(i,p):
        groups = [bytearray((len(assignments)+7)//8) for _ in range(8)]
        for j,f in enumerate(assignments):
            w = (f[i]+(f[p] if p>=0 else -1-p))%8
            groups[w][j//8] |= 1<<(j%8)
        return [int.from_bytes(a,'little') for a in groups]

    @lru_cache(None)
    def collision(i,p,j,q):
        return sum(x&y for x,y in zip(weights(i,p),weights(j,q)))

    def solve(ps):
        allow = all_bits
        for j,p in enumerate(ps):
            for i in range(j):
                allow &= ~collision(i,ps[i],j,p)
        if not allow:
            return None
        return assignments[(allow & -allow).bit_length()-1]
    return solve


def profile(ps):
    cs = components(ps)
    stars = [(p,code) for p,code in cs if code!='()']
    parent,code = stars[0]
    arms = (len(code)-2)//2
    assert len(stars)==1 and code=='('+'()'*arms+')'
    singles = [p for p,code in cs if code=='()']
    return min((arms,tuple(sorted(u*p%8 for p in singles)),u*parent%8)
               for u in (1,3,5,7))


def main():
    levels = {():()}
    failures = set()
    profiles = set()
    for r in range(1,8):
        expanded = {}
        for ps in levels.values():
            for p in range(-8,r-1):
                grown = ps+(p,)
                expanded.setdefault(shape(grown),grown)
        levels = expanded
        solve = mask_solver(r)
        bad = set()
        for canonical,ps in levels.items():
            f = solve(ps)
            if f is None:
                bad.add(canonical)
                profiles.add(profile(ps))
            else:
                assert len(set(f))==r and 0 not in f
                sums = {(f[i]+(f[p] if p>=0 else -p-1))%8 for i,p in enumerate(ps)}
                assert len(sums)==r
        print(r,len(levels),len(bad))
        assert not bad or r==7
        failures.update(bad)
    # Independently construct unordered shape multisets, assign the boundary
    # colors up to units, and search vertex-by-vertex with early weight pruning.
    all_shapes = set()
    other_failures = set()
    unit_rows = 0
    for forest in forests(7):
        for colors in boundary_orbits(forest,8):
            ps = parent_vector(forest,colors)
            orbit = {shape(parent_vector(forest,[u*c%8 for c in colors])) for u in (1,3,5,7)}
            assert orbit.isdisjoint(all_shapes)
            all_shapes.update(orbit)
            try:
                rainbow(ps,8)
            except ValueError:
                other_failures.update(orbit)
            unit_rows += 1
    assert all_shapes==levels.keys() and other_failures==failures
    assert len(failures)==42 and len(profiles)==11
    for n,singles,p in sorted(profiles):
        print(n,' '.join(str(x) for x in singles),p,sep=' | ')
    print('independent unit orbits',unit_rows,'raw failures',len(failures))


if __name__=='__main__':
    main()

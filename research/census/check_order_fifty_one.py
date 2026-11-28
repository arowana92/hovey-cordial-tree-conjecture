"""Certify centroid cuts at order 51 with the independent one- and two-vertex extensions."""
from collections import Counter
from functools import lru_cache
from pathlib import Path

from .check_leaf_profile_manifests import read_rows
from .check_sixteen_leaf_corridor import ProfileCatalog
from .leaf_profile_geometry import numerical_branches, suffix_shapes
from research.rainbow.spine_counts import partitions


@lru_cache(None)
def admissible_sizes(sizes):
    reached = 1
    for s in sizes:
        reached |= reached << s
    return sizes[-1] <= 20 and not reached & ((1 << 21) | (1 << 22))


def short_arms(parts):
    lengths = []
    for size, tips in parts:
        lengths.extend([size] if tips == 1 else [1]*tips)
    return sum(sorted(lengths)[-6:]) < 23


def centroid_profiles(leaves):
    def assign(sizes, i, left, parts, maximum):
        if i == len(sizes):
            if left == 0 and short_arms(parts):
                yield parts
            return
        s = sizes[i]
        lo = parts[-1][1] if i and sizes[i-1] == s else 1
        hi = min(leaves-8, max(1, s-1), left-(len(sizes)-1-i))
        for h in range(lo, hi+1):
            if h <= 7 and s+maximum[7-h] >= 23:
                continue
            next_max = maximum[:h] + tuple(max(maximum[j], s+maximum[j-h]) for j in range(h,8))
            yield from assign(sizes, i+1, left-h, parts+((s,h),), next_max)

    for sizes in partitions(50):
        if len(sizes) <= leaves and admissible_sizes(sizes):
            yield from assign(sizes, 0, leaves, (), (0,)*8)


def two_sites(parts):
    # Every allowed change of old parent color occurs after a prefix of mass one or two.
    prefix = parts[0][0]
    if prefix > 2:
        return False
    for size, _ in parts[1:]:
        if prefix > 2 and size > prefix:
            return False
        prefix += size
    return True


def cut_checker(catalog):
    @lru_cache(None)
    def covers(whole, z, h):
        if sum(j for _,j in whole)+min(z,h) <= 7:
            return True
        for suffix in suffix_shapes(z, min(z,h)) if z else ((),):
            exterior = tuple(sorted(whole+suffix))
            if sum(j for _,j in exterior) > 7 and not two_sites(exterior) and exterior not in catalog:
                return False
        return True

    def accepts(parts):
        if sum(s for s,h in parts if h == 1) >= 23:
            return True
        total_tips = sum(h for _,h in parts)
        # Visit submultisets directly; many centroid branches can have identical type.
        kinds = sorted(Counter(parts).items(),reverse=True)
        remaining = [quantity for part,quantity in kinds]

        def choose(start,whole,z,tips):
            if z == 0:
                return total_tips-tips <= 7 or covers(whole,0,0)
            if whole:
                smallest = whole[0][0]
                for j,((s,h),_) in enumerate(kinds):
                    if remaining[j] and z < s and smallest >= min(s,z+min(z,h)):
                        if covers(whole,z,h):
                            return True
            for j in range(start,len(kinds)):
                (s,h),_ = kinds[j]
                if remaining[j] and s <= z:
                    remaining[j] -= 1
                    ok = choose(j,((s,h),)+whole,z-s,tips+h)
                    remaining[j] += 1
                    if ok:
                        return True
            return False

        return choose(0,(),23,0)
    return accepts


def certificates():
    base = Path(__file__).parent
    catalog = ProfileCatalog()
    # Keep the base catalogue fixed so later leaf-count runs can reuse these streams.
    for mass, maximum_leaves in ((23,16), (24,15), (25,14), (26,13)):
        for h in range(12, maximum_leaves+1):
            path = base/'leaf-profile-audits'/f'{h}-{mass+28}.txt'
            catalog.known[mass].update(read_rows(path,mass))
    totals = Counter()
    for path in sorted((base/'order-51-audits').glob('*.txt')):
        mass = int(path.stem.split('-')[0])
        rows = read_rows(path,mass)
        assert not rows.keys() & catalog.known[mass]
        catalog.known[mass].update(rows)
        totals['profiles'] += len(rows)
        for forests, witnesses, inputs in rows.values():
            totals.update(forests=forests, witnesses=witnesses, assignments=inputs)
    return catalog, totals


def check(leaves,accepts):
    cases = set(centroid_profiles(leaves))
    independent = {p for p in numerical_branches(50,leaves,leaves-8,23,7)
                   if admissible_sizes(tuple(s for s,_ in p)) and short_arms(p)}
    assert cases == independent
    for profile in cases:
        assert accepts(profile), profile
    print('leaves', leaves, 'centroid profiles covered', len(cases))


def fits_parent_capacities(groups, first, second, other):
    # Each group has 'sites' slots of capacity 'other'. Two slots can take more.
    excess = [(leaves-other*sites,sites) for leaves,sites in groups if leaves>other*sites]
    if not excess:
        return True
    if len(excess) == 1:
        extra, sites = excess[0]
        return extra <= first-other + (second-other if sites >= 2 else 0)
    if len(excess) == 2:
        low, high = sorted(value for value,_ in excess)
        return low <= second-other and high <= first-other
    return False


def check_parent_bound():
    cases = excluded = further = 0
    pairs = [(b,min(b,19-2*b),min(b,19-2*b)) for b in range(1,10)]
    triples = [(b,c,min(c,20-2*b-c)) for b in range(1,10) for c in range(1,b+1)
               if 2*b+c <= 20]
    for parts in centroid_profiles(22):
        # Each branch has h leaves distributed among at most s-h potential parents.
        groups = [(sum(s == 1 for s,h in parts), 1)]
        groups.extend((h,s-h) for s,h in parts if s > 1)
        counts = []
        for leaves, sites in groups:
            q, r = divmod(leaves,sites)
            counts.extend([q+1]*r + [q]*(sites-r))
        first, second, third = sorted(counts,reverse=True)[:3]
        fits = 2*first+second <= 19
        assert fits == any(fits_parent_capacities(groups,*caps) for caps in pairs)
        cases += 1
        excluded += not fits
        # Four branches of order greater than one give four distinct leaves of the stripped tree.
        if fits and len(groups) >= 5:
            fits_three = 2*first+second+third <= 20
            assert fits_three == any(fits_parent_capacities(groups,*caps) for caps in triples)
            further += not fits_three
    print('22-leaf centroid profiles',cases,'excluded by individual parent counts',excluded,
          'further exclusions at three parents',further)


if __name__ == '__main__':
    catalog, totals = certificates()
    accepts = cut_checker(catalog)
    for h in range(17,23):
        check(h,accepts)
    print(dict(totals))
    check_parent_bound()

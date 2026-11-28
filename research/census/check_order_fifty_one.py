"""Certify centroid cuts at order 51 with the independent one- and two-vertex extensions."""
from collections import Counter
from functools import lru_cache
from itertools import combinations
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
        for length in range(1,len(parts)+1):
            if sum(s for s,_ in parts[:length]) > 23:
                break
            for whole in set(combinations(parts,length)):
                z = 23-sum(s for s,_ in whole)
                if z < 0:
                    continue
                if z == 0:
                    if total_tips-sum(j for _,j in whole) <= 7 or covers(whole,0,0):
                        return True
                    continue
                # Multiplicities matter when a whole branch and the partial one have equal type.
                for s,h in (Counter(parts)-Counter(whole)):
                    if z < s and whole[0][0] >= min(s,z+min(z,h)) and covers(whole,z,h):
                        return True
        return False
    return accepts


def certificates():
    base = Path(__file__).parent
    catalog = ProfileCatalog()
    for mass in range(23,27):
        for path in (base/'leaf-profile-audits').glob(f'*-{mass+28}.txt'):
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


def check(leaves,catalog):
    cases = set(centroid_profiles(leaves))
    independent = {p for p in numerical_branches(50,leaves,leaves-8,23,7)
                   if admissible_sizes(tuple(s for s,_ in p)) and short_arms(p)}
    assert cases == independent
    accepts = cut_checker(catalog)
    for profile in cases:
        assert accepts(profile), profile
    print('leaves', leaves, 'centroid profiles covered', len(cases))


if __name__ == '__main__':
    catalog, totals = certificates()
    for h in (17,18):
        check(h,catalog)
    print(dict(totals))

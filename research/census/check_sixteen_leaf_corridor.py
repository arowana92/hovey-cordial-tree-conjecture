"""Test all four-branch centroids and eight/eight corridors above order 54."""
from collections import defaultdict
from functools import lru_cache
from itertools import combinations_with_replacement
from pathlib import Path

from .check_leaf_corridor import endpoint_cases
from .check_leaf_profile_manifests import read_rows
from .leaf_profile_geometry import cut_test, numerical_branches


class ProfileCatalog:
    def __init__(self):
        directory = Path(__file__).with_name("leaf-profile-audits")
        self.known = {}
        for m in range(22,27):
            leaves = (12,13,14,15) if m <= 23 else (12,13)
            self.known[m] = set().union(*(read_rows(directory/f"{j}-{28+m}.txt",m)
                                         for j in leaves))

    @lru_cache(None)
    def __contains__(self, parts):
        mass = sum(s for s,_ in parts)
        if parts in self.known[mass]:
            return True
        if mass == 26:
            return False
        for i,(s,h) in enumerate(parts):
            if s == parts[-1][0]:
                larger = tuple(sorted(parts[:i] + ((s+1,h),) + parts[i+1:]))
                if larger in self:
                    return True
        return False


def cross_cut(t, whole, other):
    size, tips = whole
    s, j = other
    z = t-size
    if not 0 < z <= s or tips+j > 7:
        return False
    padding = 26-t
    if s == z:
        return max(size,s)+padding > min(size,s)
    return size+padding >= z+min(j,z)


def check(t, catalog):
    cuts = cut_test(t,catalog,7)
    hubs = [tuple((s,4) for s in sizes) for sizes in
            combinations_with_replacement(range(5,t),4) if sum(sizes) == 54+t]
    assert all(cuts(p) for p in hubs)
    cases = set(endpoint_cases(t,8))
    by_size = {p for a in range(8,2*t-1) for p in numerical_branches(a,8,7,t,7)}
    assert cases == by_size

    groups = defaultdict(list)
    for p in cases:
        a = sum(s for s,_ in p)
        if a >= t and cuts(p):
            continue
        ring = min((26-a+s for s,j in p if 1 <= 8-j <= 6 and 26-a+s >= 2), default=27)
        # Beyond the 27-vertex block we must leave a path with a-26 vertices.
        terminal = max(1, max((s for s,j in p if j == 1), default=0))
        groups[a].append((ring,terminal,p))

    for n in (55+t,82+t):
        blocks = crossing = 0
        for a,left in groups.items():
            for b,right in groups.items():
                h = n-a-b-2
                if a > b or h not in range(27):
                    continue
                if any(m % 27 in (0,n % 27) for m in range(a+1,a+h+2)):
                    continue
                assert min(a,b) >= 27
                for ring,tip,p in left:
                    if ring <= h:
                        continue
                    for other_ring,other_tip,q in right:
                        if other_ring <= h:
                            continue
                        if a-26 <= tip and b-26 <= other_tip:
                            blocks += 1
                            continue
                        assert any(cross_cut(t,v,w) or cross_cut(t,w,v) for v in p for w in q), (n,p,q)
                        crossing += 1
        print(f"n={n} hub_profiles={len(hubs) if n==55+t else 0} endpoints={len(cases)} "
              f"two_blocks={blocks} cross_cuts={crossing}")


if __name__ == "__main__":
    catalog = ProfileCatalog()
    for t in range(22,27):
        check(t,catalog)

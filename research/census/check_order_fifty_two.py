"""Check the order-52 centroid inventories against verified forest joins."""
from collections import Counter
from pathlib import Path

from .check_leaf_profile_manifests import read_rows
from .check_order_fifty_one import certificates, centroid_profiles, cut_checker, short_arms
from .leaf_profile_geometry import numerical_branches


def allowed_sizes(sizes):
    # A single 24-vertex side is already excluded; larger centered sides
    # give the earlier 25/27 or 26/26 splits.
    return max(sizes) <= 23


def star_and_leaves(parts):
    # Singletons have the same boundary color because equal sizes cannot
    # change boundary runs. The rooted star may have a different parent.
    nonsingletons = [(s, h) for s, h in parts if s > 1]
    return len(nonsingletons) == 1 and nonsingletons[0][0] == nonsingletons[0][1]+1


def singleton_cut(parts):
    sizes = [s for s, _ in parts]
    if 1 not in sizes:
        return False
    sizes.remove(1)
    reachable = 1
    for size in sizes:
        reachable |= reachable << size
    return bool(reachable & (1 << 24))


def catalog_and_totals():
    base = Path(__file__).parent
    catalog, _ = certificates()
    catalog.known[24].update(read_rows(base/'leaf-profile-audits'/'16-52.txt',24))
    totals = Counter()
    for path in sorted((base/'order-52-audits').glob('*.txt')):
        mass = int(path.stem.split('-')[0])
        rows = read_rows(path,mass)
        assert not rows.keys() & catalog.known[mass]
        catalog.known[mass].update(rows)
        totals['profiles'] += len(rows)
        for forests, witnesses, assignments in rows.values():
            totals.update(forests=forests, witnesses=witnesses, assignments=assignments)
    return catalog, totals


def check(leaves, catalog):
    cases = set(centroid_profiles(leaves,52,24,allowed_sizes))
    independent = {p for p in numerical_branches(51,leaves,leaves-8,24,7)
                   if allowed_sizes(tuple(s for s,_ in p)) and short_arms(p,24)}
    assert cases == independent
    accepts = cut_checker(catalog,24,star_and_leaves)
    for parts in cases:
        assert singleton_cut(parts) or accepts(parts), parts
    print('leaves', leaves, 'centroid profiles covered', len(cases))


if __name__ == '__main__':
    catalog, totals = catalog_and_totals()
    check(17,catalog)
    print(dict(totals))

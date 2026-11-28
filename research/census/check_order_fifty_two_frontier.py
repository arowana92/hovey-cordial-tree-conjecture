"""Check the sufficient finite profile list for all remaining 52-vertex trees."""
import argparse
from collections import Counter
from copy import deepcopy
import gzip
from pathlib import Path

from research.census.check_leaf_profile_manifests import read_rows
from research.census.check_order_fifty_one import centroid_profiles, cut_checker, short_arms
from research.census.check_order_fifty_two import catalog_and_totals, singleton_cut
from research.census.check_order_fifty_two_eighteen import allowed_sizes, common_or_pair, possible_spectra
from research.census.leaf_profile_geometry import numerical_branches
from research.rainbow.seven_tip_profiles import count
from research.rainbow.spine_counts import boundaries


def frontier(path):
    groups = {h:set() for h in range(19,24)}
    seen = set()
    for line in gzip.decompress(path.read_bytes()).decode().splitlines():
        level,*parts = line.split()
        q = tuple(tuple(map(int,p.split(','))) for p in parts)
        assert q==tuple(sorted(q)) and q not in seen
        assert sum(s for s,h in q)==24 and 7<sum(h for s,h in q)<=16
        assert all(s>=1 and 1<=h<=max(1,s-1) for s,h in q)
        seen.add(q)
        groups[int(level)].add(q)
    return groups


def published():
    directory = Path(__file__).parent
    cat,_ = catalog_and_totals()
    for m,last in ((23,16),(24,16),(25,15),(26,14)):
        for leaves in range(12,last+1):
            f = directory/'leaf-profile-audits'/f'{leaves}-{m+28}.txt'
            cat.known[m].update(read_rows(f,m))
    cat.known[24].update(read_rows(directory/'order-52-audits/eighteen/24-restarts.txt',24))
    return cat


def inventory(leaves):
    initial = set(centroid_profiles(leaves,52,24,allowed_sizes))
    # The forbidden subset sums and complementary pairs persist when adding
    # branches, so the descending recursion can reject a partial size list.
    other = {p for p in numerical_branches(51,leaves,leaves-8,24,7,allow_sizes=allowed_sizes)
             if short_arms(p,24)}
    assert initial==other
    possible = {p for p in initial if possible_spectra(p)}
    return len(initial),possible


def check(path,through,receipt_paths,pending_path=None,reduced=False):
    original = frontier(path)
    directory = path.parent/'order-52-audits'
    nineteen = read_rows(directory/'nineteen/24-restarts.txt',24)
    further = read_rows(directory/'frontier/24-restarts.txt',24)
    assert set(nineteen)==original[19]
    assert set(further)<=set.union(*(original[h] for h in range(20,24)))
    published_profiles = set(nineteen)|set(further)
    cat = published()
    groups = original
    if reduced:
        groups = frontier(path.with_name('order-52-reduced.profiles.gz'))
        candidates = set.union(*groups.values())
        assert not groups[19] and candidates<=set.union(*original.values())-published_profiles
        cat.known[24].update(published_profiles)
        print('starting forest profiles with published receipts',len(published_profiles))
    old_cut = cut_checker(cat,24,common_or_pair)
    totals = Counter()
    needed = set()
    for level in range(19,through+1):
        current = groups[level]
        for q in current:
            sizes = tuple(s for s,h in q)
            shapes = count(q)
            totals.update(profiles=1,forests=shapes,assignments=shapes*boundaries(sizes,27))
        needed.update(current)
        # Each fresh instance has its own cached answers to padded membership.
        stage = deepcopy(cat)
        stage.known[24].update(needed)
        new_cut = cut_checker(stage,24,common_or_pair)
        numeric,possible = inventory(level)
        gaps = [p for p in possible if not singleton_cut(p) and not old_cut(p)]
        assert all(new_cut(p) for p in gaps)
        print(level,'leaves; numerical, surviving, outside earlier catalog, added tests',
              numeric,len(possible),len(gaps),len(current),flush=True)
    print('sufficient tests',dict(totals))
    remaining = needed-published_profiles
    print('published receipts used',len(needed & published_profiles),
          'remaining by leaf count',{h:len(groups[h] & remaining) for h in range(19,through+1)})
    if receipt_paths:
        accepted = set()
        for receipt in receipt_paths:
            rows = read_rows(receipt,24)
            assert not accepted.intersection(rows)
            accepted.update(rows)
        remaining -= accepted
        assert not remaining, f'missing {len(remaining)} requested test receipts'
    if remaining:
        shapes = {p:count(p) for p in remaining}
        inputs = sum(n*boundaries(tuple(s for s,h in p),27) for p,n in shapes.items())
        print('conditional tests',len(remaining),'forests',sum(shapes.values()),'assignments',inputs)
    else:
        print('all required profiles have receipts with matching shape and boundary counts')
    if pending_path:
        lines = [' '.join(f'{s},{h}' for s,h in p) for level in range(19,through+1)
                 for p in sorted(groups[level] & remaining)]
        pending_path.write_text(''.join(line+'\n' for line in lines))


if __name__=='__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--through',type=int,choices=range(19,24),default=23)
    cli.add_argument('--receipts',nargs='+',type=Path)
    cli.add_argument('--reduced',action='store_true',help='use alternative cuts with the published receipts as a base')
    cli.add_argument('--write-pending',type=Path,help='write remaining profiles in generator format')
    args = cli.parse_args()
    check(Path(__file__).with_name('order-52-frontier.profiles.gz'),args.through,args.receipts,args.write_pending,args.reduced)

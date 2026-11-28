"""Certify all 18-leaf trees of order 52 using cuts with complementary side orders."""
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

from .check_leaf_profile_manifests import read_rows
from .check_order_fifty_one import centroid_profiles,cut_checker,short_arms
from .check_order_fifty_two import catalog_and_totals,star_and_leaves
from .leaf_profile_geometry import numerical_branches


@lru_cache(None)
def allowed_sizes(sizes):
    if sizes[-1]>21 or any(25-s in sizes for s in sizes):
        return False
    mask=1
    for s in sizes:
        mask|=mask<<s
    return not mask & ((1<<22)|(1<<24))


@lru_cache(None)
def tip_counts(forbidden):
    # Multisets of allowed rooted trees. A new root contributes order one.
    child_forests=[{0}]+[set() for _ in range(21)]
    trees=[set() for _ in range(22)]
    for s in range(1,22):
        if s in forbidden:
            continue
        trees[s]={1} if s==1 else child_forests[s-1].copy()
        for mass in range(s,22):
            child_forests[mass].update(a+b for a in child_forests[mass-s] for b in trees[s])
    return trees


def possible_tips(parts):
    forced=[set(range(1,s+1)) if h==1 else {1,s} for s,h in parts]
    for i,(s,h) in enumerate(parts):
        forbidden=frozenset(25-a for j,orders in enumerate(forced) if i!=j for a in orders)
        if h not in tip_counts(forbidden)[s]:
            return False
    return True


def minimal(masks):
    found=[]
    for m in sorted(masks,key=lambda x:bin(x).count('1')):
        if all((a&m)!=a for a in found):
            found.append(m)
    return tuple(found)


@lru_cache(None)
def spectra(s,h):
    if (s,h)==(1,1):
        return (2,)
    if not 1<=h<s:
        return ()
    return tuple(m|(1<<s) for m in forest_spectra(s-1,h))


@lru_cache(None)
def forest_spectra(mass,h):
    if mass==h==0:
        return (0,)
    if not 1<=h<=mass:
        return ()
    masks=set()
    for s in range(1,mass+1):
        for a in range(1,min(h,max(1,s-1))+1):
            for x in spectra(s,a):
                masks.update(x|y for y in forest_spectra(mass-s,h-a))
    return minimal(masks)


@lru_cache(None)
def complements(mask):
    return sum(1<<(25-i) for i in range(1,25) if mask&(1<<i))


def possible_spectra(parts):
    # Each mask comes from some actual rooted tree of the given order and tip count.
    orders=Counter(s for s,h in parts)
    roots=sum(1<<s for s in orders)
    choices=[]
    for s,h in parts:
        others=roots if orders[s]>1 else roots^(1<<s)
        forbidden=complements(others)
        choices.append([m for m in spectra(s,h) if not m&forbidden])
    choices.sort(key=len)
    def place(i,blocked):
        return i==len(choices) or any(place(i+1,blocked|complements(m))
                                      for m in choices[i] if not m&blocked)
    return place(0,0)


def common_or_pair(parts):
    if star_and_leaves(parts):
        return True
    mass=0
    for size,_ in parts:
        if mass and size>mass and mass!=2:
            return False
        mass+=size
    return True


def check():
    local=Path(__file__).parent
    catalog,_=catalog_and_totals()
    for mass,tag in ((25,'15-53'),(26,'14-54')):
        catalog.known[mass].update(read_rows(local/'leaf-profile-audits'/(tag+'.txt'),mass))
    cases=set(centroid_profiles(18,52,24,allowed_sizes))
    second={p for p in numerical_branches(51,18,10,24,7)
            if allowed_sizes(tuple(s for s,h in p)) and short_arms(p,24)}
    assert cases==second
    possible={p for p in cases if possible_tips(p)}
    assert possible=={p for p in second if possible_spectra(p)}
    first=cut_checker(catalog,24,common_or_pair)
    remaining=[p for p in possible if not first(p)]
    rows=read_rows(local/'order-52-audits'/'eighteen'/'24-restarts.txt',24)
    # Fresh catalog avoids cached negative membership from previous lookups.
    full=deepcopy(catalog)
    assert not full.known[24].intersection(rows)
    full.known[24].update(rows)
    final=cut_checker(full,24,common_or_pair)
    for p in remaining:
        assert final(p),p
    print('numerical centroids',len(cases),'without forced complementary sides',len(possible),
          'needing the new catalog',len(remaining))
    print('new profiles',len(rows),'forests, rows, boundary assignments',tuple(map(sum,zip(*rows.values()))))


if __name__=='__main__':
    check()

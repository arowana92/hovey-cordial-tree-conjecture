"""Enumerate disjoint 27-label profiles for the seventh rooted tip."""
from argparse import ArgumentParser
from collections import Counter
from math import comb, prod

from research.census.leaf_profile_geometry import suffix_shapes
from research.rainbow.spine_counts import rooted


def count(parts):
    return prod(comb(rooted(s)[h]+c-1,c) for (s,h),c in Counter(parts).items())


def single_trees(mass, tips):
    # All ancestors strictly above the first branching vertex have one child.
    for stem in range(1,mass-tips+1):
        for parts in suffix_shapes(mass-stem,tips):
            if len(parts)>=2 and sum(h for s,h in parts)==tips:
                yield stem,parts


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("mass", type=int)
    parser.add_argument("tips", type=int)
    args = parser.parse_args()
    if not 2<=args.tips<args.mass<27:
        parser.error("expected 2 <= tips < mass <= 26")
    profiles = sorted(single_trees(args.mass,args.tips),key=lambda x:(-count(x[1]),x))
    assert sum(count(p) for _,p in profiles)==rooted(args.mass)[args.tips]
    for stem,parts in profiles:
        print(f"stem={stem}",*(f"{s},{h}" for s,h in parts))


if __name__=="__main__":
    main()

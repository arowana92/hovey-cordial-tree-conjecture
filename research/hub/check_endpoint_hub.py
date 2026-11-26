"""Rebuild all ordinary endpoint sums and check interval completion at the hub."""

from collections import Counter
from itertools import product
from random import Random

from research.hub.endpoint_hub import endpoint
from research.rainbow.verify import rooted_shapes


def check(parents, fill=False):
    x, gap, case = endpoint(parents)
    h = len(parents)
    e = sum(p > 0 for p in parents)
    lo, hi = min(x), max(x)
    edges = [x[v]+x[p] for v, p in enumerate(parents) if v]
    if (x[0] != 0 or len(set(x)) != h or gap not in (lo, hi)
            or sorted(edges+[gap]) != sorted(x) or hi-lo > 32*h*(h+2)*2**e):
        raise ValueError(f"invalid endpoint certificate on {parents}: {x}, {gap}")
    if fill:
        missing = sorted(set(range(lo, hi+1))-set(x))
        for extra in (0, 1, 7):
            additional = (list(range(hi+1, hi+1+extra)) if gap == lo
                          else list(range(lo-extra, lo)))
            labels = x+missing+additional
            full_tree = list(parents)+[0]*(len(missing)+extra)
            sums = sorted(labels[i]+labels[p] for i, p in enumerate(full_tree) if i)
            if sorted(labels) != list(range(min(labels), max(labels)+1)) or (
                    sums and sums != list(range(sums[0], sums[0]+len(sums)))):
                raise ValueError("failed whole-tree interval completion")
    return case


def stress(depth, t, fork_leaves, arms, tail):
    # The hub's single child forks. Its first child supports a second branch.
    tree = [-1, 0, 1, 2]
    parent = 1
    for _ in range(depth):
        tree.append(parent)
        parent = len(tree)-1
    for _ in range(arms):
        tree.extend([parent, len(tree)])
        end = len(tree)-1
        for _ in range(tail):
            tree.append(end)
            end = len(tree)-1
        tree += [end]*t
    tree += [parent]*fork_leaves
    return tree


if __name__ == '__main__':
    counts = Counter()
    for h in range(1, 15):
        for tree in rooted_shapes(h).values():
            counts[check(tree, fill=h<=9)] += 1
    print(f"{sum(counts.values())} rooted shapes through order fourteen: {dict(counts)}")
    rng = Random(3912128)
    for n in range(25, 175):
        for _ in range(20):
            check([-1]+[rng.randrange(i) for i in range(1,n)])
    profiles = 0
    for depth, t, direct, arms, tail in product(range(1, 6), range(6), range(4),
                                                range(2, 5), range(3)):
        check(stress(depth, t, direct, arms, tail))
        profiles += 1
    print(f"3000 larger trees and {profiles} fork profiles checked; "
          "whole-tree interval completion through order nine.")

"""Count the sharp-cut hypotheses from size partitions without enumerating trees."""

from collections import Counter
from functools import lru_cache
from itertools import groupby
from math import comb
import sys


def partitions(total, least=1):
    if not total:
        yield ()
    for head in range(least, total+1):
        for tail in partitions(total-head, head):
            yield (head,) + tail


@lru_cache(None)
def rooted(n):
    if n == 1:
        return {1: 1}
    counts = Counter()
    for sizes in partitions(n-1):
        counts.update(forest_leaves(sizes))
    return counts


@lru_cache(None)
def same_size(size, count):
    # Pick an unordered multiset of exactly count trees of the given order.
    ways = Counter({(0, 0): 1})
    for leaves, types in rooted(size).items():
        new = Counter()
        for (chosen, mass), ways_so_far in ways.items():
            for take in range(count-chosen+1):
                new[chosen+take, mass+take*leaves] += ways_so_far*comb(types+take-1, take)
        ways = new
    return {leaves: n for (chosen, leaves), n in ways.items() if chosen == count}


def forest_leaves(sizes):
    ways = Counter({0: 1})
    for size, part in groupby(sizes):
        more = same_size(size, sum(1 for _ in part))
        combined = Counter()
        for a, x in ways.items():
            for b, y in more.items():
                combined[a+b] += x*y
        ways = combined
    return ways


def boundaries(sizes, k):
    ways = {1: k}
    prefix = sizes[0]
    for size in sizes[1:]:
        new = Counter(ways)
        for runs, amount in ways.items():
            if size >= prefix+runs:
                new[runs+1] += (k-1)*amount
        ways = new
        prefix += size
    return sum(ways.values())


def totals(k):
    all_shapes = eligible = assignments = 0
    for sizes in partitions(k-1):
        distribution = forest_leaves(sizes)
        all_shapes += sum(distribution.values())
        small = sum(n for leaves, n in distribution.items() if 3*leaves <= 2*(k-2))
        eligible += small
        assignments += small*boundaries(sizes, k)
    return all_shapes, eligible, assignments


if __name__ == '__main__':
    for k in map(int, sys.argv[1:] or (18, 19, 20)):
        if k < 5:
            raise SystemExit("the sharp-cut theorem here assumes k >= 5")
        base, forests, colors = totals(k)
        print(f"k={k} rooted bases={base} eligible forests={forests} boundary assignments={colors}")

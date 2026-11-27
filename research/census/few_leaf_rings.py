"""Enumerate bracelets of rooted trees with a prescribed number of off-cycle leaves."""

import argparse
from functools import lru_cache
from itertools import combinations


@lru_cache(None)
def forests(order, leaves, minimum=""):
    if order == 0:
        return ("",) if leaves == 0 else ()
    if not 1 <= leaves <= order:
        return ()
    words = []
    for size in range(1, order + 1):
        for tips in range(1, min(size, leaves) + 1):
            for tree in trees(size, tips):
                if tree >= minimum:
                    words.extend(tree + rest for rest in forests(order-size, leaves-tips, tree))
    return tuple(words)


@lru_cache(None)
def trees(order, leaves):
    if order == 1:
        return ("()",) if leaves == 1 else ()
    return tuple("(" + word + ")" for word in forests(order-1, leaves))


@lru_cache(None)
def decorations(max_order, max_leaves):
    return tuple((size, tips, "(" + word + ")")
                 for size in range(1, max_order + 1)
                 for tips in range(1, min(size, max_leaves) + 1)
                 for word in forests(size, tips))


def occupied_sites(order, leaves, slots):
    if slots == 1:
        for word in forests(order, leaves):
            yield ("(" + word + ")",)
        return
    for size, tips, word in decorations(order-slots+1, leaves-slots+1):
        for tail in occupied_sites(order-size, leaves-tips, slots-1):
            yield (word,) + tail


def keys(order, leaves):
    for cycle in range(3, order-leaves+1):
        for slots in range(1, min(cycle, leaves) + 1):
            for row in occupied_sites(order-cycle, leaves, slots):
                if row[0] != min(row):
                    continue
                for other in combinations(range(1, cycle), slots-1):
                    positions = (0,) + other
                    sites = ["()"] * cycle
                    for pos, word in zip(positions, row):
                        sites[pos] = word
                    bracelet = tuple(sites)
                    # Occupied sites sort before the empty decoration.
                    if all(bracelet <= tuple(sites[(pos+sign*j) % cycle] for j in range(cycle))
                           for pos, word in zip(positions, row) if word == row[0]
                           for sign in (1, -1)):
                        yield ".".join(bracelet)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("order", type=int)
    parser.add_argument("leaves", type=int)
    args = parser.parse_args()
    for key in keys(args.order, args.leaves):
        print(key)

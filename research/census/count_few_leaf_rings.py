"""Count unlabelled unicyclic graphs by cycle length and leaves without listing them."""

import argparse
from collections import Counter
from functools import lru_cache
from math import comb, gcd


def rooted_forests(mass, leaves):
    counts = {(0, 0): 1}
    for size in range(1, mass+1):
        for tips in range(1, min(leaves, size)+1):
            types = int(tips == 1) if size == 1 else counts.get((size-1, tips), 0)
            if types == 0:
                continue
            for (n, t), old in list(counts.items()):
                for copies in range(1, min((mass-n)//size, (leaves-t)//tips)+1):
                    key = n+copies*size, t+copies*tips
                    counts[key] = counts.get(key, 0) + old*comb(types+copies-1, copies)
    return counts


def count_by_cycle(order, leaves):
    forest = rooted_forests(order-3, leaves)

    @lru_cache(None)
    def fixed(orbits, n, t):
        if not orbits:
            return int(n == t == 0)
        d = orbits[-1]
        return sum(types * fixed(orbits[:-1], n-d*mass, t-d*tips)
                   for (mass, tips), types in forest.items() if d*mass <= n and d*tips <= t)

    for c in range(3, order+1):
        symmetries = Counter()
        for shift in range(c):
            g = gcd(c, shift)
            symmetries[(c//g,)*g] += 1
            singles = sum((2*i-shift) % c == 0 for i in range(c))
            symmetries[(1,)*singles + (2,)*((c-singles)//2)] += 1
        total = sum(mult * fixed(orbits, order-c, leaves) for orbits, mult in symmetries.items())
        assert total % (2*c) == 0
        yield c, total//(2*c)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("order", type=int)
    parser.add_argument("leaves", type=int)
    args = parser.parse_args()
    for length, count in count_by_cycle(args.order, args.leaves):
        print(length, count)

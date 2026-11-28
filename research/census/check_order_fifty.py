"""Certify possible centroid branch profiles for an ordinary 50-vertex tree."""
import argparse
from collections import Counter
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import subprocess

from research.rainbow.spine_counts import boundaries, partitions
from .check_leaf_profile_manifests import read_rows
from .check_sixteen_leaf_corridor import ProfileCatalog
from .leaf_profile_geometry import suffix_shapes


@lru_cache(None)
def minimum_tips(order, forbidden):
    """Unbounded knapsack over the orders of the root's children."""
    infinity = 50
    forest = [0] + [infinity] * order
    tree = [infinity] * (order + 1)
    for size in range(1, order + 1):
        if size in forbidden:
            continue
        tree[size] = max(1, forest[size - 1])
        for total in range(size, order + 1):
            forest[total] = min(forest[total], forest[total - size] + tree[size])
    return tree[order]


def possible_centroids(leaf_limit):
    def assign(sizes, lower, i, parts, total, best):
        if i == len(sizes):
            if total >= 17:
                yield tuple(sorted(parts))
            return
        s = sizes[i]
        low = lower[i]
        if i and sizes[i - 1] == s:
            low = max(low, parts[-1][1])
        high = min(max(1, s - 1), leaf_limit - total - sum(lower[i+1:]))
        for h in range(low, high + 1):
            if h <= 7 and s + best[7-h] >= 22:
                continue
            capacity = best[:h] + tuple(max(best[j], s + best[j-h]) for j in range(h, 8))
            yield from assign(sizes, lower, i+1, parts+((s,h),), total+h, capacity)

    for sizes in partitions(49):
        if len(sizes) > leaf_limit or sizes[-1] > 21:
            continue
        sums = 1
        for s in sizes:
            sums |= sums << s
        if sums & (1 << 22) or any(a+b == 23 for a,b in combinations(sizes, 2)):
            continue
        lower = []
        for i, s in enumerate(sizes):
            forbidden = frozenset(23-x for j,x in enumerate(sizes) if i != j and 23-x <= s)
            lower.append(minimum_tips(s, forbidden))
        if sum(lower) <= leaf_limit:
            yield from assign(sizes[::-1], lower[::-1], 0, (), 0, (0,)*8)


def cut_checker(catalog):
    @lru_cache(None)
    def covers(whole, z, cap):
        if sum(h for _,h in whole) + cap <= 7:
            return True
        for suffix in suffix_shapes(z, cap):
            parts = tuple(sorted(whole + suffix))
            if sum(h for _,h in parts) <= 7:
                continue
            sizes = tuple(s for s,_ in parts)
            if boundaries(sizes, 27) != 27 and parts not in catalog:
                return False
        return True

    def accepts(parts):
        if sum(s for s,h in parts if h == 1) >= 22:
            return True
        for i, (s,h) in enumerate(parts):
            if i and parts[i-1] == (s,h):
                continue
            others = parts[:i] + parts[i+1:]
            for length in range(1, len(others)+1):
                if sum(a for a,_ in others[:length]) >= 22:
                    break
                for whole in set(combinations(others, length)):
                    z = 22 - sum(a for a,_ in whole)
                    if 0 < z < s and whole[0][0] >= min(s, z+min(z,h)):
                        if covers(whole, z, min(z,h)):
                            return True
        return False
    return accepts


def certificates():
    base = Path(__file__).parent
    catalog = ProfileCatalog()
    for mass, limit in [(22,16), (23,16), (24,15), (25,14), (26,13)]:
        for leaves in range(12, limit+1):
            path = base/'leaf-profile-audits'/f'{leaves}-{mass+28}.txt'
            catalog.known[mass].update(read_rows(path, mass))
    totals = Counter()
    for path in sorted((base/'order-50-audits').glob('*.txt')):
        mass = int(path.stem.split('-')[0])
        rows = read_rows(path, mass)
        assert not rows.keys() & catalog.known[mass]
        catalog.known[mass].update(rows)
        totals['profiles'] += len(rows)
        for forests, witnesses, assignments in rows.values():
            totals.update(forests=forests, witnesses=witnesses, assignments=assignments)
    return catalog, totals


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('native', type=Path)
    cli.add_argument('leaf_limit', type=int, choices=range(17,22))
    args = cli.parse_args()
    candidates = set(possible_centroids(args.leaf_limit))
    catalog, totals = certificates()
    accepts = cut_checker(catalog)
    for h in range(17, args.leaf_limit+1):
        lines = subprocess.check_output([args.native.resolve(), str(h)], text=True).splitlines()
        independent = {tuple(tuple(map(int, x.split(','))) for x in line.split()) for line in lines}
        group = {p for p in candidates if sum(j for _,j in p) == h}
        assert len(lines) == len(independent) and group == independent
        for parts in group:
            assert accepts(parts), (h, parts)
        print('leaves', h, 'centroid profiles covered', len(group), flush=True)
    print(dict(totals))


if __name__ == '__main__':
    main()

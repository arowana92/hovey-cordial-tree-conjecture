"""Reconstruct both branch profiles and the two integer intervals on every tree."""

from collections import Counter
from itertools import combinations_with_replacement, product
from random import Random

from research.hub.two_center_layers import two_center_tree


def check(left, right, direct):
    edges, labels = two_center_tree(left, right, direct)
    n = len(labels)
    assert n == 2 + sum(1+x for x in (*left, *right)) + sum(direct)
    assert len(edges) == n-1
    adjacency = [[] for _ in labels]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    seen = {0, 1}
    assert 1 in adjacency[0]
    for side, profile in enumerate((left, right)):
        children = Counter()
        for parent in adjacency[side]:
            if parent == 1-side:
                continue
            assert parent not in seen
            seen.add(parent)
            tips = [v for v in adjacency[parent] if v != side]
            children[len(tips)] += 1
            for v in tips:
                assert v not in seen and adjacency[v] == [parent]
                seen.add(v)
        expected = Counter(profile)
        if direct[side]:
            expected[0] = direct[side]
        assert children == expected
    assert len(seen) == n
    assert sorted(labels) == list(range(min(labels), min(labels)+n))
    sums = sorted(labels[u]+labels[v] for u, v in edges)
    assert sums == list(range(sums[0], sums[0]+n-1))


def main():
    equal = unequal = 0
    for h in range(5):
        profiles = list(combinations_with_replacement(range(1, 5), h))
        for left, right in product(profiles, repeat=2):
            for direct in product(range(min(left, default=4)), range(min(right, default=4))):
                check(left, right, direct)
                equal += 1
    rng = Random(1991)
    for h in range(1, 51):
        for a in range(h//2, 2*h-h//2+1):
            d = abs(a-h)
            r = h if not d else h-2*d+1
            for _ in range(3):
                profiles = [[rng.randint(1, 15) for _ in range(r)] + [1]*(s-r)
                            for s in (a, 2*h-a)]
                direct = tuple(rng.randrange(min(x)) for x in profiles) if a == h else (0, 0)
                check(*profiles, direct)
                if d:
                    unequal += 1
                else:
                    equal += 1
    print(f"Verified {equal} equal-count and {unequal} unequal-count two-center trees.")


if __name__ == "__main__":
    main()

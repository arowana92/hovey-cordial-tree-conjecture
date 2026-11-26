"""Verify ball inequalities against independent exact scheduling and actual labels."""

from functools import lru_cache
from itertools import combinations, product
from random import Random
from research.large_order_degree import attach_batch, balanced, counts


def plan(parents, k, seed):
    live = set(range(seed, len(parents)))
    depth = [0] * seed
    for p in parents[seed:]:
        depth.append(1 + depth[p])
    if any(sum(0 < x <= d for x in depth) < k*d for d in range(1, max(depth))):
        return None
    reverse = []
    while live:
        nonterminal = {parents[v] for v in live}
        leaves = sorted(live - nonterminal, key=depth.__getitem__, reverse=True)
        size = (len(live)-1) % k+1
        batch = leaves[:size]
        assert len(batch) == size
        live.difference_update(batch)
        reverse.append(batch)
    return list(reversed(reverse))


def feasible(parents, k):
    @lru_cache(None)
    def extend(seen):
        ready = [v for v in range(1, len(parents)) if not seen >> v & 1 and seen >> parents[v] & 1]
        left = len(parents)-bin(seen).count('1')
        return not left or any(extend(seen+sum(1 << v for v in group))
                               for group in combinations(ready, min(left, k)))
    return extend(1)


def check_plan(parents, k, seed, batches):
    used = set(range(seed))
    for i, batch in enumerate(batches):
        assert 1 <= len(batch) <= k and (i == len(batches)-1 or len(batch) == k)
        assert len(set(batch)) == len(batch) and used.isdisjoint(batch)
        assert all(parents[v] in used for v in batch)
        used.update(batch)
    assert len(used) == len(parents)


if __name__ == '__main__':
    comparisons = labeled = 0
    for n in range(1, 9):
        for pp in product(*(range(v) for v in range(1, n))):
            parents = [-1, *pp]
            for k in (2, 3, 4):
                steps = plan(parents, k, 1)
                assert (steps is not None) == feasible(parents, k)
                if steps is not None:
                    check_plan(parents, k, 1, steps)
                comparisons += 1
    rng = Random(61)
    for k in range(2, 9):
        for seed in (1, k+1):
            for _ in range(8):
                parents = [-1] + [0]*(seed-1) + [rng.randrange(seed) for _ in range(3*k)]
                parents.extend(rng.randrange(v) for v in range(len(parents), 20*k))
                batches = plan(parents, k, seed)
                if batches is None:
                    continue
                check_plan(parents, k, seed, batches)
                labels = [0] + list(range(k))*(seed != 1) + [None]*(len(parents)-seed)
                for batch in batches:
                    attach_batch(parents, labels, batch, k)
                assert all(balanced(x) for x in counts(parents, labels, k))
                labeled += 1
    print(f"{comparisons} independent scheduling comparisons; {labeled} full tree labelings")

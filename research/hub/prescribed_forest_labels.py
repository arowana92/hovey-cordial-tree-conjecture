"""Assign prescribed input residues to a forest, bounding its edge multiplicities."""
from collections import Counter
from heapq import heappop, heappush
from itertools import combinations, product
from random import Random

from research.hub.breadth_first_leaves import finish_batches
from research.hub.sparse_leaf_sites import complete
from research.hub.two_private_leaves import distinct_shifts, helper_weights


def assign(k, parents, inputs):
    """Negative parent -1-b denotes a boundary vertex of fixed residue b."""
    n = len(parents)
    assert len(inputs) == n
    assert all(0 <= x < k for x in inputs)
    children = [[] for _ in parents]
    mass = [1]*n
    balance = [0]*k
    roots = []
    for v in reversed(range(n)):
        p = parents[v]
        if p < 0:
            assert -1-p < k
            roots.append(v)
            balance[-1-p] += mass[v]
        else:
            assert p < v
            children[p].append(v)
            mass[p] += mass[v]
    for x in inputs:
        balance[x] -= 1
    # Start immediately after a minimum of the prefix sums around the circle.
    origin = total = minimum = 0
    for b, delta in enumerate(balance):
        total += delta
        if total < minimum:
            minimum, origin = total, (b+1) % k
    assert total == 0
    queue = []
    for v in roots:
        heappush(queue, ((-1-parents[v]-origin) % k, v))
    labels = [-1]*n
    previous = -1
    for x in sorted((a-origin) % k for a in inputs):
        p, v = heappop(queue)
        assert previous <= p <= x
        previous = p
        labels[v] = (x+origin) % k
        for child in children[v]:
            heappush(queue, (x, child))
    return labels


def verify_forest(k, parents, inputs):
    f = assign(k, parents, inputs)
    assert sorted(f) == sorted(inputs)
    weights = [(f[v]+(f[p] if p >= 0 else -1-p)) % k for v, p in enumerate(parents)]
    assert max(Counter(weights).values(), default=0) <= 2*max(Counter(inputs).values(), default=0)
    return weights


def extend(k, base, base_parents, forest, sites, strategy):
    """Replay on a divisible base, keeping its labels. Sites are real vertex indices."""
    n = len(base)
    r = len(forest)
    a = n//k
    base_weights = [(base[v]+base[p]) % k for v,p in enumerate(base_parents,1)]
    hole, = [w for w in range(k) if base_weights.count(w) == a-1]
    parents = list(base_parents) + list(forest)
    if 2*r <= k:
        f = list(base)
        used = set()
        added = set()
        for v, p in enumerate(forest):
            x = (hole-f[p]) % k if v == 0 else next(
                x for x in range(k) if x not in used and (x+f[p]) % k not in added)
            f.append(x)
            used.add(x)
            added.add((x+f[p]) % k)
        labels = complete(k, f, parents, [0]*len(parents), [(p,0) for p in sites])
        assert labels is not None
    else:
        relative = [-1-base[p] if p < n else p-n for p in forest]
        f = list(base) + assign(k, relative, list(range(r)))
        old = [(f[v]+f[p]) % k for v,p in enumerate(parents,1)]
        effective = Counter(old)
        normalized = [w for w in range(k) for _ in range(effective[w]-a+1)]
        outputs = helper_weights(k, normalized, k-r)
        xs = list(range(r,k))
        if strategy == "distinct":
            rows = distinct_shifts(k, xs, outputs)
        else:
            rows = [((y-x) % k,x) for x,y in zip(xs, sorted(outputs,reverse=True))]
        populations = Counter(sites)
        labels = finish_batches(k, f, [populations[v] for v in range(n+r)], old, 1, rows)
        assert sites == sorted(sites)
    assert labels[:n] == base
    assert len(labels) == n+r+len(sites) and all(0 <= x < k for x in labels)
    all_parents = parents+sites
    weights = [(labels[v]+labels[p]) % k for v,p in enumerate(all_parents,1)]
    for counts in (Counter(labels), Counter(weights)):
        bins = [counts[x] for x in range(k)]
        assert max(bins)-min(bins) <= 1


def checks():
    forests = 0
    for k in range(1,8):
        for n in range(1,min(k,4)+1):
            for parents in product(*(range(-k,v) for v in range(n))):
                for inputs in combinations(range(k), n):
                    verify_forest(k, parents, inputs)
                    forests += 1
    rng = Random(20261129)
    repeated = 0
    for k in (1,2,5,8,9,12,17,27):
        for n in (k,2*k,3*k+1):
            for _ in range(12):
                parents = [rng.randrange(-k,v) for v in range(n)]
                inputs = [rng.randrange(k) for _ in range(n)]
                verify_forest(k, parents, inputs)
                repeated += 1
    joins = 0
    for k in (5,8,9,12,15,18,21,27):
        for a in (1,2,3):
            # A star on ak vertices, center zero, has one deficient edge bin.
            base = [v % k for v in range(a*k)]
            n = len(base)
            for r in sorted({1,k//2,k//2+1,k-2,k-1}):
                forest = [rng.randrange(n+v) for v in range(r)]
                for strategy in (["sorted","distinct"] if k%2 else ["sorted"]):
                    extra = 1 if strategy=="sorted" and 2*r>k else 0
                    sites = sorted(v for v in range(k) for _ in range(2+extra*int(0<v<k-r)))
                    extend(k, base, [0]*(n-1), forest, sites, strategy)
                    joins += 1
    print(f'{forests} prescribed sets, {repeated} prescribed multisets, {joins} fixed-core tree extensions')


if __name__ == '__main__':
    checks()

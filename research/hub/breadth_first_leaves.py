"""Construct cordial labels on a tree with at least two or three leaves per site."""
from collections import Counter, defaultdict, deque
from itertools import accumulate
from random import Random

from research.large_order_hall_pools import hall_pair, pairs_for


def breadth_first(parents):
    children = [[] for _ in range(len(parents)+1)]
    for v, p in enumerate(parents, 1):
        children[p].append(v)
    queue = deque([0])
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        queue.extend(children[v])
    return order


def helpers(k, h, leaves, weights):
    """Return the batch count and the (site color, leaf color) helper pairs."""
    q, r = divmod(h, k)
    if not r:
        return 2*q, []
    t = k-r
    if 2*r <= k and t <= leaves*r:
        return q+2, [(i//leaves, r+i) for i in range(t)]

    def gap(batches, rows):
        return ((q+1+batches)*sum(range(k))-sum(weights)-sum(s+x for s, x in rows)) % k

    if 2*r <= k:
        # Translate the near-transversal's input by one at even modulus.
        def shift(x):
            if k % 2:
                return x
            a = (x-1) % k
            return a + int(a >= k//2)
        base = [(shift(x), x) for x in range(r, k)]
        for c in range(k):
            rows = [((s+c) % k, x) for s, x in base]
            if not 1 <= gap(q+1, rows) <= 2*r-3:
                return q+1, rows
    else:
        fixed = [(i, r+i) for i in range(t-1)]
        used = {(s+x) % k for s, x in fixed}
        for s in range(r):
            rows = fixed + [(s, k-1)]
            if (s+k-1) % k not in used and not 1 <= gap(q+2, rows) <= 2*r-k-3:
                return q+2, rows
    raise AssertionError("no admissible helper assignment")


def label_tree(k, parents, populations):
    h = len(parents)+1
    assert len(populations) == h and h >= k >= 1
    if k == 1:
        return [0]*(h+sum(populations))
    q, r = divmod(h, k)
    leaves = 2 if q >= 2 or r == 0 else 3
    assert min(populations) >= leaves
    labels = [-1]*(h+sum(populations))
    for i, v in enumerate(breadth_first(parents)):
        labels[v] = i % k
    weights = [(labels[p]+labels[i]) % k for i, p in enumerate(parents, 1)]
    batches, rows = helpers(k, h, leaves, weights)
    # Leaf numbers are consecutive per original site in the caller's numbering.
    starts = list(accumulate([h]+list(populations)))
    slots = defaultdict(list)
    for p in range(h):
        slots[labels[p]].extend(range(starts[p], starts[p+1]))
    for s, x in rows:
        labels[slots[s].pop()] = x
        weights.append((s+x) % k)
    per_bin = (h+len(rows))//k + batches
    d = (per_bin*sum(range(k))-sum(weights)) % k
    hist = Counter(weights)
    residual = [per_bin - int(w == d) - hist[w] for w in range(k)]
    assert min(residual) >= 0 and sum(residual) == batches*k
    for s, x in pairs_for(residual):
        labels[slots[s].pop()] = x

    spare = [(s, vertex) for s in range(k) for vertex in slots[s]]
    finish_from_divisible(k, labels, spare, d)
    return labels


def finish_from_divisible(k, labels, spare, d):
    """Fill leaf slots (parent color, vertex index) starting at deficient edge d."""
    for pos in range(0, len(spare), k):
        s, vertex = spare[pos]
        surplus = (d-s) % k
        labels[vertex] = surplus
        rest = spare[pos+1:pos+k]
        shifts = [s for s, _ in rest]
        padding = [0]*(k-len(shifts)-1) + [(-sum(shifts)) % k]
        pairs = hall_pair(shifts+padding)
        xs = [(-a) % k for a, _ in pairs[:len(rest)]]
        missing = next(v for v in range(k) if v not in xs)
        for (s, vertex), x in zip(rest, xs):
            labels[vertex] = (x+surplus-missing) % k
        if len(rest) == k-1:
            used = {(s+labels[v]) % k for s, v in rest}
            d, = set(range(k))-used


def verify(k, parents, populations):
    labels = label_tree(k, parents, populations)
    all_parents = list(parents) + [v for v, n in enumerate(populations) for _ in range(n)]
    assert len(labels) == len(all_parents)+1 and all(0 <= x < k for x in labels)
    edges = [(labels[p]+labels[v]) % k for v, p in enumerate(all_parents, 1)]
    for hist in (Counter(labels), Counter(edges)):
        counts = [hist[x] for x in range(k)]
        assert max(counts)-min(counts) <= 1


def ordered_trees(h, parents=()):
    if len(parents) == h-1:
        yield parents
        return
    for p in range(parents[-1] if parents else 0, len(parents)+1):
        yield from ordered_trees(h, parents+(p,))


def checks():
    rng = Random(19521961)
    small = broad = 0
    for h in range(1, 9):
        for parents in ordered_trees(h):
            for k in range(1, h+1):
                n = 2 if h >= 2*k or h % k == 0 else 3
                verify(k, parents, [n]*h)
                small += 1
    for k in list(range(2, 19))+[21, 24, 27, 32, 36, 45]:
        for q in (1, 2, 3):
            for r in sorted({0, 1, k//4, k//2, (k+1)//2, k-1}):
                h = q*k+r
                parents = [rng.randrange(v) for v in range(1, h)]
                n = 2 if q >= 2 or r == 0 else 3
                verify(k, parents, [n+rng.randrange(4) for _ in range(h)])
                broad += 1
    # A single batch can fail the exact test for this fixed BFS core.
    k = 5
    w = [(x+p) % k for x, p in enumerate([0, 0, 0, 3], 1)]
    d = -sum(w) % k
    assert w.count(d) == 2 and d == 2
    print(f'{small} small whole-tree labelings, {broad} variable-population labelings, '
          'one forced failure with a fixed core')


if __name__ == '__main__':
    checks()

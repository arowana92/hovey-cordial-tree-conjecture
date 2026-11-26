"""Construct a common vertex/edge histogram using seven-edge paths and leaf layers."""

from bisect import bisect_left
from collections import Counter, deque
from random import Random

from research.check_large_order_subdivision import children, compress
from research.large_order_hall_pools import hall_pair
from research.large_order_subdivision import expand


def gap_path(p, s, t):
    """Arrival labels below p, supplying old gap s and removing new gap t."""
    return [t, -p - 2*t, p + t, s + t, -t, -p - t, p + s + 2*t]


def paired_path(p, s, t, z, k):
    first = gap_path(p, s, z)
    second = gap_path(first[-1], z, t)
    return [v % k for v in first + second]


def prune(tree, pins, depth, batch_size=None):
    """Delete full batches first if requested, then synchronous terminal layers."""
    kids = children(tree)
    live = set(range(len(tree)))
    sizes = list(map(len, kids))
    leaves = deque(i for i in live if not sizes[i] and i not in pins)

    def remove(batch):
        live.difference_update(batch)
        for v in batch:
            u = tree[v]
            sizes[u] -= 1
            if sizes[u] == 0 and u not in pins:
                leaves.append(u)

    full, layers = [], []
    while batch_size is not None and len(leaves) >= batch_size:
        batch = [leaves.popleft() for _ in range(batch_size)]
        remove(batch)
        full.append(batch)
    for _ in range(depth):
        if not leaves:
            break
        level = list(leaves)
        leaves.clear()
        remove(level)
        layers.append(level)

    # Each surviving unprotected terminal has one child in every successive layer.
    layer_of = {v: i for i, level in enumerate(layers) for v in level}
    paths = []
    for v in sorted(live):
        if sizes[v] or v in pins:
            continue
        assert len(layers) == depth
        chain = []
        for j in reversed(range(depth)):
            v = next(u for u in kids[v] if layer_of.get(u) == j)
            chain.append(v)
        paths.append(chain)
    return live, full, layers, paths


def core_data(tree, live, pins):
    ids, small, holes = compress(tree, children(tree), live, pins)
    return ids, small, holes


def expand_core(labels, holes, k):
    if not holes:
        return
    specs = [(labels[a[0]], labels[a[-1]], (len(a)-2)//12) for a in holes]
    for path, vals in zip(holes, expand(specs, k)):
        for v, x in zip(path, vals):
            labels[v] = x


def repair_paths(tree, labels, ids, small, chains, k, seed=1):
    slots = [(path[i:i+14]) for path in chains for i in range(0, len(path)-13, 14)]
    if len(slots) < len(small)-1:
        raise ValueError("insufficient consecutive path blocks")
    free = Counter()
    threshold = 36 * ((12 * (len(small)-1) + k-1) // k) + 1
    rng = Random(seed)
    for j, path in enumerate(slots[:len(small)-1], 1):
        s = labels[ids[j]]
        t = (s + labels[ids[small[j]]]) % k
        p = labels[tree[path[0]]]
        start = rng.randrange(k)
        for shift in range(k):
            values = paired_path(p, s, t, (start+shift) % k, k)
            # Positions 7 and 11 (zero-based) are t and -t.
            movable = values[:7] + values[8:11] + values[12:]
            if all(free[x] < threshold for x in movable):
                free.update(movable)
                for v, x in zip(path, values):
                    labels[v] = x
                break
        else:
            raise AssertionError("path choice bound")
    return len(small)-1


def pack_cycles(values, order, base, k):
    """Split a closed walk into simple cycles and try to translate them disjointly."""
    walk = [0]
    edges = []
    position = {0: 0}
    cycles = []
    for i in order:
        head = (walk[-1] + values[i] - base) % k
        edges.append(i)
        if head in position:
            start = position[head]
            cycles.append(list(zip(edges[start:], walk[start:])))
            for x in walk[start+1:]:
                del position[x]
            del edges[start:]
            del walk[start+1:]
        else:
            position[head] = len(walk)
            walk.append(head)
    assert walk == [0] and not edges
    used = set()
    result = [None] * k
    loops = []
    for cycle in sorted(cycles, key=len, reverse=True):
        if len(cycle) == 1:
            loops.append(cycle[0])
            continue
        for offset in range(k):
            if all((x+offset) % k not in used for _,x in cycle):
                for i,x in cycle:
                    result[i] = (x+offset) % k
                    used.add(result[i])
                break
        else:
            return None
    # The first available offset for a loop gives the first unused tail at or after start.
    available = [x for x in range(k) if x not in used]
    for i,start in loops:
        index = bisect_left(available, start)
        result[i] = available.pop(index if index < len(available) else 0)
    return result


def permutation_tails(values, k):
    """Translating all heads by a common base preserves their distinctness."""
    order = list(range(k))
    bases = list(dict.fromkeys([0] + [v for v,_ in Counter(values).most_common()]))
    rng = Random(1)
    for attempt in range(1 if k < 7 else 64):
        result = pack_cycles(values, order, bases[attempt % len(bases)], k)
        if result is not None:
            return result
        rng.shuffle(order)
    return [(-p) % k for p,_ in hall_pair(values)]


def leaf_batch(displacements, gap, k):
    """Extend a single gap. A complete batch changes V by 1 + new_gap - old_gap."""
    if not displacements:
        return [], gap
    if len(displacements) > k:
        raise ValueError("batch too large")
    initial = list(displacements[:k-1])
    special = (-sum(initial)) % k
    values = initial + [special] + [0] * (k-1-len(initial))
    tails = permutation_tails(values, k)
    offset = (gap - tails[len(initial)]) % k
    labels = [(offset + x) % k for x in tails[:len(initial)]]
    missing = (gap + special) % k
    if len(displacements) == k:
        missing = (missing-displacements[-1]) % k
        labels.append(missing)
    return labels, missing


def restore_layers(tree, labels, layers, gap, k):
    for level in reversed(layers):
        pending = [v for v in level if labels[v] is None]
        for i in range(0, len(pending), k):
            group = pending[i:i+k]
            new, gap = leaf_batch([labels[tree[v]] for v in group], gap, k)
            for v, x in zip(group, new):
                labels[v] = x
    return gap


def common(tree, k, depth=336):
    """The unrestricted single-root construction. Smaller depths need enough paths."""
    live, batches, levels, chains = prune(tree, {0}, depth, batch_size=k)
    ids, small, holes = core_data(tree, live, {0})
    labels = [None] * len(tree)
    queue = deque([0])
    kids = children(small)
    rank = 0
    while queue:
        i = queue.popleft()
        labels[ids[i]] = rank % k
        rank += 1
        queue.extend(kids[i])
    expand_core(labels, holes, k)
    blocks = repair_paths(tree, labels, ids, small, chains, k)
    gap = restore_layers(tree, labels, levels, 0, k)
    gap = restore_layers(tree, labels, batches, gap, k)
    return labels, gap, (blocks, sum((len(p)-2)//12 for p in holes), len(batches))

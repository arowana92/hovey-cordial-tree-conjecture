"""Uniform label increments at a hub with equal positive child populations."""

import json
from functools import lru_cache
from pathlib import Path

from research.hub.subdivided_stars import folded_block
from research.large_order_hall_pools import hall_pair


@lru_cache(None)
def seeds():
    path = Path(__file__).with_name("regular-joint-seeds.jsonl")
    entries = [json.loads(line) for line in path.read_text().splitlines()]
    return {entry["centers"]: entry for entry in entries}


def parents(m):
    return sorted([0, 1, 2, -3, *[a for j in range(4, m//2 + 2) for a in (-j, j)]])


@lru_cache(None)
def signed_interval(d, s):
    """Find a signed Langford permutation of defect d by finite exact cover."""
    n = 2 * s
    jumps = [a for a in range(1-d-s, d+s) if abs(a) >= d]
    rows = [(x, x+a, a) for x in range(n) for a in jumps if 0 <= x+a < n]
    groups = {(kind, value): set() for kind, values in enumerate((range(n), range(n), jumps))
              for value in values}
    columns = [tuple(enumerate(row)) for row in rows]
    for i, keys in enumerate(columns):
        for key in keys:
            groups[key].add(i)

    def cover():
        if not groups:
            return []
        key = min(groups, key=lambda col: len(groups[col]))
        for i in sorted(groups[key]):
            removed = []
            for col in columns[i]:
                options = groups.pop(col)
                removed.append((col, options))
                for option in options:
                    for other in columns[option]:
                        if other in groups:
                            groups[other].remove(option)
            tail = cover()
            if tail is not None:
                return [rows[i], *tail]
            for col, options in reversed(removed):
                for option in options:
                    for other in columns[option]:
                        if other in groups:
                            groups[other].add(option)
                groups[col] = options

    result = cover()
    if result is None:
        raise ValueError("no signed Langford permutation at this order")
    return result


@lru_cache(None)
def single_tips(m):
    if m < 22:
        return dict(zip(parents(m), seeds()[m]["tips"]))
    s = (m - 8) // 2

    def move(x):
        return x + s * (int(x >= 4) - int(x <= -4))

    frame = {move(p): move(x) for p, x in single_tips(8).items()}
    start = max(*frame, *frame.values()) + 1
    frame.update((a, start + x) for x, _, a in signed_interval(4, s))
    return frame


@lru_cache(None)
def nonzero_layer(m):
    if m < 30:
        return seeds()[m]["one"]
    part = sorted(signed_interval(6, (m - 8) // 2))
    return [*nonzero_layer(8), *(7 + y for _, y, _ in part)]


def even_branches(m, q, exceptional):
    """Use one zero center with the exceptional number of children."""
    data = seeds()
    if m in (4, 6) and q == 2:
        branch = {p: [] for p in parents(m)}
        slots = [p for p in branch for _ in range(1 if p == 0 else 2)]
        for p, x in zip(slots, data[m]["short"]):
            branch[p].append(x)
        layers = []
    else:
        branch = {p: [x] for p, x in single_tips(m).items()}
        count = q - 1
        if m in (4, 6):
            layers = [data[m]["three"]] if count % 2 else []
            layers.extend([data[m]["two"]] * ((count - 3*len(layers)) // 2))
        else:
            layers = [nonzero_layer(m)] * count if count else []
    start = max(max(p, *xs) for p, xs in branch.items()) + 1
    for layer in layers:
        for x, y in enumerate(layer):
            branch[y-x].append(start+x)
        start += len(layer)
    branch[0].extend(range(start, start + exceptional - 1))
    return [(p, branch[p]) for p in [0, *sorted(branch.keys() - {0})]]


def paired_branches(pairs, single):
    """Keep the input order of pairs, also when truncation makes counts zero."""
    branches = [(0, [])]
    for i in range(1, len(pairs) + 1):
        branches.extend(((i, []), (-i, [])))
    by_parent = dict(branches)
    start = len(pairs) + 1
    for level in range(1, max(pairs, default=0) + 1):
        active = sum(size >= level for size in pairs)
        for p, x in folded_block(active, start).items():
            by_parent[p].append(x)
        start += 2 * active
    by_parent[0].extend(range(start, start + single))
    return branches


def truncated_pairs(pairs, capacity, total):
    half = min(sum(pairs), total // 2)
    single = total - 2*half
    assert 0 <= single <= capacity
    sizes = []
    for cap in pairs:
        take = min(half, cap)
        sizes.append(take)
        half -= take
    return paired_branches(sizes, single)


def prefix(m, q, e, plain, size):
    """Integer interval on a connected prefix containing all m branch centers."""
    if m < 3 or min(q, e) < 1 or plain < 0:
        raise ValueError("expected at least three nonempty branches")
    demand = (m-1)*q + e
    if not m <= size <= m + demand + plain:
        raise ValueError("prefix must contain every center and fit the tree")
    tips = min(size-m, demand)
    if m % 2:
        branches = truncated_pairs([q] * (m//2), e, tips)
    elif tips > (m-1)*q:
        branches = even_branches(m, q, tips - (m-1)*q)
    else:
        branches = truncated_pairs([q] * (m//2 - 1), q, tips)
        high = max(max([p, *xs]) for p, xs in branches)
        branches.insert(0, (high + 1, []))  # The exceptional center is a leaf in this prefix.
    high = max(max([p, *xs]) for p, xs in branches)
    direct = list(range(high + 1, high + 1 + size-m-tips))
    return branches, direct


def append_batch(labels, parent, vertices, deficit, k):
    """From uniform vertex counts, add up to k vertices with labeled parents."""
    if not vertices:
        return deficit
    root = vertices[0]
    first = (deficit - labels[parent[root]]) % k
    labels[root] = first
    other = vertices[1:]
    shifts = [labels[parent[v]] for v in other]
    requests = [*shifts, -sum(shifts), *([0] * (k-1-len(shifts)))]
    pairs = hall_pair(requests)
    offset = first + pairs[len(other)][0]
    weights = set()
    for v, p, (left, _) in zip(other, shifts, pairs):
        labels[v] = (offset-left) % k
        weights.add((labels[v]+p) % k)
    if len(vertices) == k:
        return next(x for x in range(k) if x not in weights)
    return None


def extend(m, q, e, plain, k, root_label, deficit):
    """Label the given attachment at a core of order divisible by k."""
    if k < 1 or m < 3 or min(q, e) < 1 or plain < 0:
        raise ValueError("invalid modulus or branch populations")
    counts = [e] + [q] * (m-1)
    parent = [-1] + [0]*m
    children = []
    for i, count in enumerate(counts, 1):
        children.append(list(range(len(parent), len(parent) + count)))
        parent.extend([i]*count)
    direct = list(range(len(parent), len(parent) + plain))
    parent.extend([0]*plain)
    labels = [None] * len(parent)
    labels[0] = root_label % k
    centers = list(range(1, m+1))
    n = len(parent)-1
    if m <= k:
        block, ordinary = prefix(m, q, e, plain, min(n, k))
        for v, (p, xs) in zip(centers, block):
            labels[v] = (p + root_label) % k
            for w, x in zip(children[v-1], xs):
                labels[w] = (x + root_label) % k
        for v, x in zip(direct, ordinary):
            labels[v] = (x + root_label) % k
        if n < k:
            hit = {(labels[v] + labels[parent[v]]) % k for v in range(1,n+1)}
            if deficit not in hit:
                v = next(v for v in range(m+1,n+1) if labels[parent[v]] == labels[0])
                labels[v] = (deficit - labels[0]) % k
            return labels
    else:
        used = m - m % k
        for i, v in enumerate(centers[:used]):
            labels[v] = (root_label+i) % k
        if used < m:
            ready = [w for tips in children[:used] for w in tips]
            batch = centers[used:] + ready[:k-(m-used)]
            deficit = append_batch(labels, parent, batch, deficit, k)
    remaining = [v for v in range(1, n+1) if labels[v] is None]
    for j in range(0,len(remaining),k):
        deficit = append_batch(labels, parent, remaining[j:j+k], deficit, k)
    return labels

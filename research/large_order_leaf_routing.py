"""Realize a histogram correction by actual leaves with prescribed parent labels."""

from collections import Counter, deque
from itertools import product
from random import Random
from bisect import bisect_right
from itertools import accumulate

from research.large_order_subdivision import round_groups


class LeafRoutes:
    def __init__(self, k, radix):
        if not 2 <= radix < k:
            raise ValueError("need 2 <= radix < modulus")
        self.k = k
        self.radix = radix
        self.strides = []
        top = 1
        while top * radix < k:
            self.strides.append(top)
            top *= radix
        self.top = top
        self.height = (k + top - 1) // top
        self.width = (radix + self.height - 1) // self.height
        self.grid_size = top * self.height
        self.mask_count = self.width * self.height
        # Each entry denotes a separate parent, including at coinciding residues.
        self.shifts = {}
        for i, stride in enumerate(self.strides):
            for t in range(1 - radix, radix):
                self.shifts[i, t] = stride * t
        for m in range(self.height):
            for v in range(self.width):
                self.shifts['plus', m, v] = m * top + v
        for t in range(2 - 2 * self.height, self.height):
            for v in range(self.width):
                self.shifts['minus', t, v] = t * top - v

    @property
    def digits(self):
        return len(self.strides) + 1

    def leg(self, start, end, mask):
        """List (parent entry, new leaf label) in travel order."""
        current = start
        for i, stride in enumerate(self.strides):
            change = (end // stride) % self.radix - (start // stride) % self.radix
            yield (i, change), current % self.k
            current += stride * change
        m, v = divmod(mask, self.width)
        yield ('plus', m, v), current % self.k
        yield ('minus', end // self.top - start // self.top - m, v), (
            current + m * self.top + v) % self.k

    def route(self, source, target, middle, first_mask, last_mask):
        return [*self.leg(source, middle, first_mask),
                *self.leg(middle, target, last_mask)]


def label_core(parents, sites, routes):
    children = [[] for _ in parents]
    for child, parent in enumerate(parents[1:], 1):
        children[parent].append(child)
    marked = set(sites)
    if len(marked) != len(routes.shifts) or not marked <= set(range(len(parents))):
        raise ValueError("need one distinct core vertex per shift entry")
    pending = deque([0])
    entries = iter(sorted(routes.shifts, key=lambda e: routes.shifts[e] % routes.k))
    labels = [None] * len(parents)
    holders = {}
    rank = 0
    while pending:
        v = pending.popleft()
        if v in marked:
            entry = next(entries)
            labels[v] = routes.shifts[entry] % routes.k
            holders[entry] = v
        else:
            labels[v] = rank % routes.k
            rank += 1
        pending.extend(children[v])
    return labels, holders


def loads(paths):
    at_bin, at_site = Counter(), Counter()
    for path in paths:
        for entry, label in path:
            at_bin[label] += 1
            at_site[entry] += 1
    return at_bin, at_site


def select_routes(routes, demands, bound, seed=1, exact=False):
    if not demands:
        return []
    k, d = routes.k, routes.digits
    rng = Random(seed)
    if not exact:
        paths = [routes.route(x, y, rng.randrange(routes.grid_size),
                              rng.randrange(routes.mask_count), rng.randrange(routes.mask_count))
                 for x, y in demands]
        tails, sites = loads(paths)
        error = 8 * (d + 1)
        if (max(tails.values()) <= 4 * bound * (d + 1) + error and
                max(sites.values()) <= (2 * bound * k + routes.radix - 1) // routes.radix + error):
            return paths
    # Exact finite fallback. Each column records its tail counts and its parent uses.
    site_rows = {entry: k + i for i, entry in enumerate(routes.shifts)}
    options = list(product(range(routes.grid_size), range(routes.mask_count),
                           range(routes.mask_count)))
    columns = []
    for source, target in demands:
        group = []
        for option in options:
            column = [0] * (k + len(site_rows))
            for entry, label in routes.route(source, target, *option):
                column[label] += 1
                column[site_rows[entry]] += 1
            group.append(column)
        columns.append(group)
    chosen = round_groups(columns, k + len(site_rows))
    return [routes.route(x, y, *options[i]) for (x, y), i in zip(demands, chosen)]


def diagonal_leaves(deficits, radix):
    for lo in range(0, len(deficits), radix):
        tokens = [x for x in range(lo, min(lo + radix, len(deficits)))
                  for _ in range(deficits[x])]
        for x, y in zip(tokens, reversed(tokens)):
            yield (0, y - x), x


def build_seed(parents, sites, routes, seed=1):
    """Return a labeled tree of order 1 mod k, its site map and its routing leaf count."""
    k = routes.k
    labels, holders = label_core(parents, sites, routes)
    vertices, edges = Counter(labels), Counter(
        (labels[v] + labels[p]) % k for v, p in enumerate(parents) if v)
    defect = [vertices[x] - edges[x] - int(x == 0) for x in range(k)]
    sources = [x for x, f in enumerate(defect) for _ in range(-f)]
    targets = [x for x, f in enumerate(defect) for _ in range(f)]
    assert len(sources) == len(targets)
    paths = select_routes(routes, list(zip(sources, targets)),
                          max(map(abs, defect)), seed)
    result = parents.copy()
    tails, _ = loads(paths)
    level = max(vertices[x] + tails[x] for x in range(k))
    deficits = [level + int(x == 0) - vertices[x] - tails[x] for x in range(k)]
    for path in paths:
        for entry, label in path:
            result.append(holders[entry])
            labels.append(label)
    routing_count = len(result) - len(parents)
    for entry, label in diagonal_leaves(deficits, routes.radix):
        result.append(holders[entry])
        labels.append(label)
    return result, labels, holders, routing_count


def rank_bands(populations, min_rank, max_rank, min_population):
    """Keep the largest dyadic rank in each occupied dyadic population band."""
    kept = {}
    rank = 1
    while rank <= min(max_rank, len(populations)):
        size = populations[rank - 1]
        if rank >= min_rank and size >= min_population:
            kept[size.bit_length()] = (rank, size)
        rank *= 2
    return sorted(kept.values())


def shared_sites(parents_by_rank, networks):
    """Install each residue once, at its earliest network's population guarantee."""
    holders = {}
    next_parent = iter(parents_by_rank)
    for net in networks:
        for value in sorted({s % net.k for s in net.shifts.values()} - holders.keys()):
            holders[value] = next(next_parent)
    return holders


def sparse_labels(parents, k, holders, critical_limit, seed):
    """Pin one bipartition, then complete the Steiner paths and hanging branches."""
    from itertools import chain

    nbr = [[] for _ in parents]
    for v, p in enumerate(parents[1:], 1):
        nbr[p].append(v)
        nbr[v].append(p)
    pins = set(holders.values())
    hull = set(range(len(parents)))
    degrees = list(map(len, nbr))
    queue = deque(v for v in hull - pins if degrees[v] <= 1)
    while queue:
        v = queue.popleft()
        hull.remove(v)
        for u in nbr[v]:
            if u in hull:
                degrees[u] -= 1
                if degrees[u] == 1 and u not in pins:
                    queue.append(u)
    junctions = sorted(v for v in hull - pins if degrees[v] >= 3)
    fixed = pins.union(junctions)
    fixed_edges = [(p, v) for v, p in enumerate(parents) if v and v in fixed and p in fixed]
    assert not any(p in pins and v in pins for p, v in fixed_edges)
    rng = Random(seed)
    trials = ([rng.randrange(k) for _ in junctions] for _ in range(32))
    labels = [None] * len(parents)
    for x, v in holders.items():
        labels[v] = x
    # The finite fallback is lazy, including when the number of junctions is large.
    def all_choices():
        yield from product(range(k), repeat=len(junctions))
    for row in chain(trials, all_choices()):
        for v, x in zip(junctions, row):
            labels[v] = x
        vert = Counter(labels[v] for v in fixed)
        edge = Counter((labels[p] + labels[v]) % k for p, v in fixed_edges)
        if max(chain(vert.values(), edge.values(), (0,))) <= 2 * critical_limit + 1:
            break
    else:
        raise ValueError("no critical-site assignment within the supplied limit")
    cap = max(2 * critical_limit + 2, 8 * ((len(parents) + k - 1) // k))
    def assign(v):
        old = [labels[u] for u in nbr[v] if labels[u] is not None]
        assert len(old) <= 2
        for x in range(k):
            if vert[x] < cap and all(edge[(x + y) % k] < cap for y in old):
                labels[v] = x
                vert[x] += 1
                edge.update((x + y) % k for y in old)
                return
        raise AssertionError("greedy bin bound")
    for v in sorted(hull - fixed):
        assign(v)
    queue = deque(hull)
    while queue:
        v = queue.popleft()
        for u in nbr[v]:
            if labels[u] is None:
                assign(u)
                queue.append(u)
    return labels


def mixed_seed(parents, labels, networks, shares, holders, seed=1, exact=False):
    """Assign routes using pooled residue quotas, then fill consecutive intervals."""
    from fractions import Fraction
    from math import ceil

    k = networks[0].k
    assert len(shares) == len(networks) and all(s > 0 for s in shares)
    assert all(labels[v] == x for x, v in holders.items())
    total = sum(shares)
    vertices = Counter(labels)
    edges = Counter((labels[p] + labels[v]) % k for v, p in enumerate(parents) if v)
    f = [vertices[x] - edges[x] - int(x == 0) for x in range(k)]
    sources = [x for x in range(k) for _ in range(-f[x])]
    targets = [x for x in range(k) for _ in range(f[x])]
    assert len(sources) == len(targets)
    demands = list(zip(sources, targets))
    bound = max(map(abs, f))
    d = max(net.digits for net in networks)
    error = 8 * (d + 1)
    site_mean_bound = Counter()
    for net, share in zip(networks, shares):
        for jump in net.shifts.values():
            site_mean_bound[jump % k] += Fraction(2 * len(demands) * share, total * net.radix)

    def observations(net, option, x, y):
        return [(net.shifts[e] % k, z) for e, z in net.route(x, y, *option)]

    rng = Random(seed)
    paths = []
    cumulative = list(accumulate(shares))
    for x, y in demands:
        net = networks[bisect_right(cumulative, rng.randrange(total))]
        opt = (rng.randrange(net.grid_size), rng.randrange(net.mask_count), rng.randrange(net.mask_count))
        paths.append(observations(net, opt, x, y))
    tails, uses = loads(paths)
    if demands and (exact or max(tails.values()) > 4 * bound * (d + 1) + error or
                    any(n > ceil(site_mean_bound[p]) + error for p, n in uses.items())):
        outcomes, probabilities = [], []
        for j, (net, share) in enumerate(zip(networks, shares)):
            size = net.grid_size * net.mask_count ** 2
            for opt in product(range(net.grid_size), range(net.mask_count), range(net.mask_count)):
                outcomes.append((j, opt))
                probabilities.append(Fraction(share, total * size))
        groups = []
        for x, y in demands:
            group = []
            for j, opt in outcomes:
                column = [0] * (2 * k)
                for p, z in observations(networks[j], opt, x, y):
                    column[k + p] += 1
                    column[z] += 1
                group.append(column)
            groups.append(group)
        selected = round_groups(groups, 2 * k, probabilities=[probabilities] * len(groups))
        paths = []
        for (x, y), index in zip(demands, selected):
            j, opt = outcomes[index]
            paths.append(observations(networks[j], opt, x, y))
        tails, uses = loads(paths)
    assert all(n <= ceil(site_mean_bound[p]) + error for p, n in uses.items())
    assert max(tails.values(), default=0) <= 4 * bound * (d + 1) + error
    level = max(vertices[x] + tails[x] for x in range(k))
    missing = [level + int(x == 0) - vertices[x] - tails[x] for x in range(k)]
    result, values = parents.copy(), labels.copy()
    for path in paths:
        for p, z in path:
            result.append(holders[p])
            values.append(z)
    routed = len(result) - len(parents)
    start = used_shares = 0
    for net, share in zip(networks, shares):
        used_shares += share
        stop = k * used_shares // total
        for (_, jump), x in diagonal_leaves(missing[start:stop], net.radix):
            result.append(holders[jump % k])
            values.append(x + start)
        start = stop
    return result, values, routed

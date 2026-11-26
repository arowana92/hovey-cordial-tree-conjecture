"""Independently count mixed-radix routes, capacities and the original tree edges."""

from collections import Counter
from fractions import Fraction
from itertools import product
from random import Random

from research.large_order_degree import attach_batch
from research.large_order_leaf_routing import (
    LeafRoutes, build_seed, diagonal_leaves, mixed_seed, rank_bands,
    select_routes, shared_sites, sparse_labels,
)


def histograms(tree, lab, k):
    assert len(tree) == len(lab) and tree[0] == -1
    assert all(0 <= x < k for x in lab)
    v, e = [0] * k, [0] * k
    for i, x in enumerate(lab):
        v[x] += 1
        if i:
            assert 0 <= tree[i] < i
            e[(x + lab[tree[i]]) % k] += 1
    return v, e


def check_seed(tree, lab, k):
    v, e = histograms(tree, lab, k)
    assert len(set(e)) == 1 and v == [e[0] + 1] + e[1:]


def check_means(k, radix):
    net = LeafRoutes(k, radix)
    d = net.digits
    assert len(net.shifts) <= (2 * d + 6) * radix
    assert max(Counter(x % k for x in net.shifts.values()).values()) <= 2 * d + 12
    trials = net.grid_size * net.mask_count
    for inbound in (False, True):
        rows = [Counter() for _ in range(d + 1)]
        for endpoint in range(k):
            loc = Counter()
            for middle, mask in product(range(net.grid_size), range(net.mask_count)):
                start, end = (middle, endpoint) if inbound else (endpoint, middle)
                ptr = start % k
                for j, (entry, x) in enumerate(net.leg(start, end, mask)):
                    assert x == ptr
                    rows[j][x] += 1
                    loc[entry] += 1
                    ptr = (ptr + net.shifts[entry]) % k
                assert ptr == end % k and j == d
            # For every individual demand the probability of any entry is <= 1/R.
            assert all(n * radix <= trials for n in loc.values())
        assert all(max(row.values()) <= 2 * trials for row in rows)
    return 2 * trials * k


def finish_small(tree, lab, k, rng):
    start = len(tree)
    count = 2 * k + rng.randrange(1, k)
    tree.extend(rng.randrange(start) for _ in range(count))
    lab.extend([None] * count)
    for i in range(start, len(tree), k):
        attach_batch(tree, lab, list(range(i, min(i + k, len(tree)))), k)
    assert all(max(v) - min(v) <= 1 for v in histograms(tree, lab, k))
    return count


def core_tree(n, shape, rng):
    if shape == 0:
        ps = [max(0, i - 1) for i in range(1, n)]
    elif shape == 1:
        ps = [(i - 1) // 2 for i in range(1, n)]
    elif shape == 2:
        ps = [0 if i % 4 else i - 1 for i in range(1, n)]
    else:
        ps = [rng.randrange(i) for i in range(1, n)]
    return [-1] + ps


def check_single(k, r, shape, rng):
    net = LeafRoutes(k, r)
    count = len(net.shifts)
    p = core_tree(2 * count + 19, shape, rng)
    sites = rng.sample(range(len(p)), count)
    tree, lab, holders, nroute = build_seed(p, sites, net, seed=shape)
    check_seed(tree, lab, k)
    v, e = histograms(p, lab[:len(p)], k)
    A = (len(p) + k - 1) // k
    b = 4 * (2 * A + 2) * (2 * net.digits + 12) + 2
    assert max(v + e) < b
    assert max(abs(v[i] - e[i] - (i == 0)) for i in range(k)) <= b
    assert set(tree[len(p):]) <= set(sites)
    assert all(lab[who] == net.shifts[entry] % k for entry, who in holders.items())
    scale = (k + r - 1) // r
    N = b + 4 * b * (net.digits + 1) + 8 * (net.digits + 1)
    assert max(Counter(tree[len(p):]).values(), default=0) <= (
        2 * b * scale + 8 * (net.digits + 1) + (N + 1) * scale)
    extra = finish_small(tree, lab, k, rng) if k <= 8 else 0
    return len(tree), nroute, extra


def check_mixed(k, radices, shape, rng):
    nets = [LeafRoutes(k, r) for r in radices]
    wanted = set(x % k for net in nets for x in net.shifts.values())
    p = core_tree(4 * len(wanted) + 11, shape, rng)
    parity = [0]
    for parent in p[1:]:
        parity.append(1 - parity[parent])
    side = max((parity.count(t), t) for t in (0, 1))[1]
    eligible = [v for v in range(len(p)) if parity[v] == side]
    rng.shuffle(eligible)
    holders = shared_sites(eligible, nets)
    assert set(holders) == wanted and len(set(holders.values())) == len(wanted)
    labels = sparse_labels(p, k, holders, 12, shape)
    assert all(labels[v] == x for x, v in holders.items())
    tree, lab, routed = mixed_seed(p, labels, nets, list(range(1, len(nets) + 1)),
                                   holders, shape)
    assert tree[:len(p)] == p and lab[:len(p)] == labels
    assert set(tree[len(p):]) <= set(holders.values())
    check_seed(tree, lab, k)
    extra = finish_small(tree, lab, k, rng) if k <= 8 else 0
    return len(tree), routed, extra


def check_bands(rng):
    cases = 0
    for n in (17, 64, 357, 1024, 5000):
        for _ in range(12):
            values = sorted((2 ** rng.randrange(16) + rng.randrange(17)
                             for _ in range(n)), reverse=True)
            lo = rng.randrange(1, 12)
            hi = rng.randrange(max(lo, n // 3), n + 1)
            cut = rng.randrange(1, 16)
            chosen = rank_bands(values, lo, hi, cut)
            ranks = [1 << j for j in range(n.bit_length())
                     if lo <= 1 << j <= hi and values[(1 << j) - 1] >= cut]
            total = sum(r * values[r - 1] for r in ranks)
            assert total <= 4 * sum(r * a for r, a in chosen)
            for i, (_, a) in enumerate(chosen):
                assert sum(b for _, b in chosen[i:]) <= 4 * a
            cases += 1
    return cases


def check_pooled_capacity():
    """Charge every occurrence to its actual first holder, counting tail blocks."""
    from math import ceil

    cases = sites = 0
    for k in (4099, 65003, 262144):
        D = 16
        K = 8 * (2 * D + 6)
        ranks = [1 << j for j in range(10, k.bit_length() - 1)]
        b, error = 100, 8 * (D + 1)
        level = b + 4 * b * (D + 1) + error + 1
        threshold = 64 * K * ((2 * D + 12) * b + level) * k
        for tilt in (1, 2, 3):
            pops = [(tilt * threshold + r - 1) // r for r in ranks]
            total = sum(r * p for r, p in zip(ranks, pops))
            assert total >= threshold and min(pops) >= 64 * level + 4 * error
            capacity, load = {}, Counter()
            prefix = 0
            for rank, pop in zip(ranks, pops):
                net = LeafRoutes(k, rank // K)
                assert net.digits <= D
                share = Fraction(rank * pop, total)
                start = prefix
                prefix += rank * pop
                length = k * prefix // total - k * start // total
                for jump in net.shifts.values():
                    p = jump % k
                    capacity.setdefault(p, pop)
                    load[p] += 2 * b * k * share / net.radix
                for jump in range(1 - net.radix, net.radix):
                    load[jump % k] += level * ((length + net.radix - 1) // net.radix)
                assert len(capacity) <= rank
            assert all(ceil(load[p]) + error <= pop for p, pop in capacity.items())
            cases += 1
            sites += len(capacity)
    return cases, sites


def check_degree_pins():
    checked = 0
    for k in (7, 17, 36, 61, 127):
        nets = [LeafRoutes(k, 2), LeafRoutes(k, max(3, k // 4))]
        values = {v % k for net in nets for v in net.shifts.values()}
        for shape in (0, 1, 2):
            rng = Random(k * 19 + shape)
            tree = core_tree(4 * len(values) + 10, shape, rng)
            nbr = [[] for _ in tree]
            parity = [0]
            for v, p in enumerate(tree[1:], 1):
                nbr[v].append(p)
                nbr[p].append(v)
                parity.append(1 - parity[p])
            side = max((parity.count(i), i) for i in (0, 1))[1]
            pool = [i for i, t in enumerate(parity) if t == side]
            rng.shuffle(pool)
            holders = shared_sites(pool, nets)
            pinned = set(holders.values())
            free = [i for i in range(len(tree)) if i not in pinned]
            big = [i for i in free if len(nbr[i]) > 3]
            labels = [None] * len(tree)
            for x, i in holders.items():
                labels[i] = x
            for i in big:
                labels[i] = 0
            V = Counter(x for x in labels if x is not None)
            E = Counter((labels[i] + labels[p]) % k for i, p in enumerate(tree)
                        if i and labels[i] is not None and labels[p] is not None)
            assert max(E.values(), default=0) <= 2 * len(big) + 1
            cap = 16 * ((len(tree) + k - 1) // k) + 2 * len(big) + 2
            for i in reversed(free):
                if labels[i] is not None:
                    continue
                neighbors = [labels[j] for j in nbr[i] if labels[j] is not None]
                x = next(x for x in range(k) if V[x] < cap and
                         all(E[(x + y) % k] < cap for y in neighbors))
                labels[i] = x
                V[x] += 1
                E.update((x + y) % k for y in neighbors)
            v, e = histograms(tree, labels, k)
            assert max(v + e) <= cap + 4
            tr, lab, _ = mixed_seed(tree, labels, nets, [2, 5], holders, shape)
            check_seed(tr, lab, k)
            checked += 1
    return checked


def main():
    rng = Random(461037)
    legs = sum(check_means(k, r) for k in range(3, 22) for r in range(2, k))
    dtests = 0
    for weights in product(range(3), repeat=7):
        for r in (2, 4, 6):
            out, inc, jumps = Counter(), Counter(), Counter()
            for (_, t), x in diagonal_leaves(weights, r):
                out[x] += 1
                inc[x + t] += 1
                jumps[t] += 1
            assert [out[i] for i in range(7)] == [inc[i] for i in range(7)] == list(weights)
            assert max(jumps.values(), default=0) <= max(weights) * ((7 + r - 1) // r)
            dtests += 1
    # Exercise rational rounding itself, including unequal shares in a pooled row.
    net = LeafRoutes(3, 2)
    path = select_routes(net, [(1, 2)], 1, exact=True)[0]
    assert path[0][1] == 1 and (path[-1][1] + net.shifts[path[-1][0]]) % 3 == 2
    p = [-1, 0, 0, 0, 1, 2]
    holders = {0: 1, 1: 2, 2: 3}
    tr, lab, _ = mixed_seed(p, [2, 0, 1, 2, 0, 0], [net, net], [1, 3], holders, exact=True)
    check_seed(tr, lab, 3)
    singles = [check_single(k, r, shape, rng) for k, r in
               ((3, 2), (7, 4), (8, 2), (17, 3), (36, 6), (61, 17), (127, 4),
                (200, 80), (257, 2), (1009, 24)) for shape in range(4)]
    pooled = [check_mixed(k, rs, s, rng) for k, rs in
              ((5, (2, 3)), (8, (2, 5)), (37, (3, 7, 14)), (61, (4, 11, 20)),
               (127, (3, 12, 39)), (256, (5, 16, 69)), (1009, (5, 15, 37)))
              for s in range(4)]
    print(f"{check_degree_pins()} additional trees checked with the degree-based pinning bound.")
    cases, sites = check_pooled_capacity()
    print(f"{cases} weighted population profiles, {sites:,} actual pooled capacities checked.")
    all_trees = singles + pooled
    print(f"{legs:,} directed legs, {dtests:,} reversal histograms, {check_bands(rng)} rank profiles.")
    print(f"{len(singles)} single and {len(pooled)} pooled trees, largest order "
          f"{max(n for n, _, _ in all_trees):,}; {sum(n for _, n, _ in all_trees):,} routing "
          f"leaves and {sum(n for _, _, n in all_trees)} further Hall leaves recounted.")


if __name__ == '__main__':
    main()

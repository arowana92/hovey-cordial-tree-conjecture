"""Repair a compressed core at nested intervals of leaf-parent residues."""

from collections import Counter
from random import Random

from research.large_order_check import histograms
from research.large_order_gap_paths import core_data, expand_core, prune, repair_paths, restore_layers
from research.large_order_leaf_routing import diagonal_leaves, sparse_labels
from research.large_order_subdivision import round_groups


def interval_walks(demands, radius, seed=1, exact=False):
    """Route integer pairs with |jump| < radius and bounded load at each internal site."""
    if radius < 2:
        raise ValueError("radius must be at least two")
    width = radius // 2
    blocks, walks = [], []
    for x,y in demands:
        a,b = x // width, y // width
        step = 1 if a <= b else -1
        itinerary = list(range(a, b+step, step))
        blocks.append(itinerary)
        walks.append([x] + [None] * len(itinerary) + [y])
    hops = sum(len(walk)-1 for walk in walks)
    max_tails = len(demands)//width + 6
    max_jumps = hops//width + 6
    rng = Random(seed)
    for parity in (0,1):
        groups = [(i,j) for i, itinerary in enumerate(blocks)
                  for j in range(parity,len(itinerary),2)]
        if not groups:
            continue

        def observations(i, j, offset):
            x = blocks[i][j]*width + offset
            before, after = walks[i][j], walks[i][j+2]
            result = [('tail', x)]
            if before is not None:
                result.append(('jump', x-before))
            if after is not None:
                result.append(('jump', after-x))
            return result

        for attempt in range(0 if exact else 20):
            chosen = [rng.randrange(width) for _ in groups]
            load = Counter(entry for (i,j),z in zip(groups,chosen) for entry in observations(i,j,z))
            if all(n <= (max_tails if t == 'tail' else max_jumps) for (t,_),n in load.items()):
                break
        else:
            options = [[observations(i,j,z) for z in range(width)] for i,j in groups]
            rows = sorted({row for group in options for col in group for row in col})
            cols = [[[col.count(row) for row in rows] for col in group] for group in options]
            chosen = round_groups(cols,len(rows))
        for (i,j),z in zip(groups,chosen):
            walks[i][j+1] = blocks[i][j]*width + z
    return walks


def assign_holders(ranks, ranked_sites):
    holders = {}
    for rank, radius, population in ranks:
        for jump in range(1-radius, radius):
            if jump not in holders:
                holders[jump] = ranked_sites[len(holders)]
        assert len(holders) <= rank and population > 0
    return holders


def seed(tree, k, ranks, ranked_sites, aux_modulus, depth=840, seed_value=1):
    """Build a uniform-edge seed. Ranks give (rank, radius, lower population)."""
    holders = assign_holders(ranks, ranked_sites)
    pins = set(holders.values()) | {0}
    live, _, layers, chains = prune(tree, pins, depth)
    ids, small, holes = core_data(tree, live, pins)
    index = {v:i for i,v in enumerate(ids)}
    use_paths = sum(len(path)//14 for path in chains) >= len(small)-1
    modulus = k if use_paths else aux_modulus
    fixed = {jump % modulus:index[v] for jump,v in holders.items()}
    if len(fixed) != len(holders):
        raise ValueError("prescribed residues coincide")
    # A union bound over three lists per bin proves an assignment exists whenever
    # 3M (2v/M)^m < 1. The deterministic limit v also works at all densities.
    v = len(holders)
    critical_limit = v
    if 2*v < modulus:
        numerator, denominator = 3*modulus, 1
        for m in range(1,v):
            numerator *= 2*v
            denominator *= modulus
            if numerator < denominator:
                critical_limit = m
                break
    small_lab = sparse_labels(small,modulus,fixed,critical_limit,seed_value)
    # Use the signed representatives for the actual pins in both constructions.
    for jump,v in holders.items():
        small_lab[index[v]] = jump
    labels = [None] * len(tree)
    for v,x in zip(ids,small_lab):
        labels[v] = x % k
    expand_core(labels,holes,k)
    result = tree.copy()
    routed = 0
    if use_paths:
        repairs = repair_paths(tree,labels,ids,small,chains,k,seed_value)
    else:
        pairs = [(small_lab[j]+small_lab[p],small_lab[j]) for j,p in enumerate(small) if j]
        for walk in interval_walks(pairs,ranks[-1][1],seed_value):
            for x,y in zip(walk,walk[1:]):
                result.append(holders[y-x])
                labels.append(x % k)
                routed += 1
        repairs = 0
    gap = restore_layers(tree,labels,layers,labels[0],k)
    v,e = histograms(result,labels,k)
    assert all(v[x]-e[x] == (x==gap) for x in range(k))
    level = max(v)
    missing = [level+(x==gap)-v[x] for x in range(k)]
    total = sum(rank*pop for rank,_,pop in ranks)
    cumulative = start = 0
    for rank,radius,pop in ranks:
        cumulative += rank*pop
        end = k*cumulative//total
        for (_,jump),x in diagonal_leaves(missing[start:end],radius):
            result.append(holders[jump])
            labels.append(start+x)
        start = end
    return result,labels,holders,(repairs,routed)

"""Complete a prescribed tree by large sets of leaves at fixed sites."""
from collections import deque
from functools import reduce
from math import gcd


def moment(counts):
    return sum(z * n for z, n in enumerate(counts))


def subgroup_index(k, shifts):
    return reduce(gcd, shifts, k)


def route_leaves(k, shifts, sizes, sources, targets):
    """Destinations are normalized by subtracting the final site's label."""
    assert shifts[-1] == 0 and sum(sizes) == sum(sources) == sum(targets)
    index = subgroup_index(k, shifts)
    discrepancy = [b-a for a, b in zip(sources, targets)]
    if any(sum(discrepancy[j::index]) for j in range(index)):
        return None
    if (moment(discrepancy) - sum(h*n for h, n in zip(shifts, sizes))) % k:
        return None

    predecessor = {0: None}
    todo = deque([0])
    while todo:
        z = todo.popleft()
        for i, h in enumerate(shifts[:-1]):
            w = (z+h) % k
            if w not in predecessor:
                predecessor[w] = (z, i)
                todo.append(w)
    tables = [[0]*k for _ in sizes]
    for j in range(index):
        tails = [z for z in range(j, k, index) for _ in range(-discrepancy[z])]
        heads = [z for z in range(j, k, index) for _ in range(discrepancy[z])]
        for start, end in zip(tails, heads):
            relative = (end-start) % k
            while relative:
                previous, i = predecessor[relative]
                tables[i][(start+previous) % k] += 1
                relative = previous

    cursor = 0
    for i, h in enumerate(shifts[:-1]):
        remaining = sizes[i] - sum(tables[i])
        if remaining < 0:
            raise ValueError("too few leaves for the selected paths")
        full, remainder = divmod(remaining, k)
        step_index = gcd(k, h)
        order = k//step_index
        orbits, partial = divmod(remainder, order)
        # Put full orbits outside the cursor's orbit, then advance along it.
        for z in range(k):
            residue = (z-cursor) % step_index
            tables[i][z] += full + (0 < residue <= orbits)
        for _ in range(partial):
            tables[i][cursor] += 1
            cursor = (cursor+h) % k
    assert cursor == 0
    for z, count in enumerate(sources):
        tables[-1][z] = count - sum(row[z] for row in tables[:-1])
    if min(tables[-1]) < 0:
        raise ValueError("too few leaves at the final site for these routes")
    assert sum(tables[-1]) == sizes[-1]
    return tables


def subset_with_sum(length, count, total):
    """A subset of the given cardinality and residue sum on a cyclic interval."""
    positions = list(range(count))
    extra = (total - sum(positions)) % length
    for i in reversed(range(count)):
        move = min(extra, length-count)
        positions[i] += move
        extra -= move
    assert not extra
    return positions


def fixed_core(k, parents, labels, populations):
    """Parents in topological order with one root. Return the leaf tables or None."""
    r = len(parents)
    sites = [v for v, size in enumerate(populations) if size]
    sizes = [populations[v] for v in sites]
    if not sites or min(sizes) < 4*k*r:
        raise ValueError("the core theorem assumes at least 4kr leaves per site")
    baseline = labels[sites[-1]]
    shifts = [(labels[v]-baseline) % k for v in sites]
    index = subgroup_index(k, shifts)
    length = k//index
    vertices, edges = [0]*k, [0]*k
    for v, p in enumerate(parents):
        vertices[labels[v] % k] += 1
        if p >= 0:
            edges[(labels[v]+labels[p]-baseline) % k] += 1

    difference = [a-b for a, b in zip(vertices, edges)]
    gaps = [sum(difference[j::index]) for j in range(index)]
    floor, edge_extras = divmod(r+sum(sizes)-1, k)
    counts = [max(0, -g) for g in gaps]
    upper = [min(length, length-g) for g in gaps]
    spare = edge_extras - sum(counts)
    if spare < 0 or any(a > b for a, b in zip(counts, upper)):
        return None
    for j, cap in enumerate(upper):
        inc = min(spare, cap-counts[j])
        counts[j] += inc
        spare -= inc
    if spare:
        return None

    changed = [list(range(abs(g))) for g in gaps]
    required = moment(difference) - sum(n*h for n, h in zip(sizes, shifts))
    current = sum((1 if g > 0 else -1) * sum(j+t*index for t in changed[j])
                  for j, g in enumerate(gaps))
    assert (required-current) % index == 0
    if length > 1:
        j = next(j for j, g in enumerate(gaps) if 0 < abs(g) < length)
        sign = 1 if gaps[j] > 0 else -1
        target = sum(changed[j]) + sign*((required-current)//index)
        changed[j] = subset_with_sum(length, abs(gaps[j]), target)

    sources = [floor - n for n in vertices]
    targets = [floor - n for n in edges]
    for j, g in enumerate(gaps):
        special = set(changed[j])
        common = min(counts[j], counts[j]+g)
        for t in range(length):
            z = j+t*index
            if t in special:
                sources[z] += g > 0
                targets[z] += g < 0
            elif common:
                sources[z] += 1
                targets[z] += 1
                common -= 1
        assert not common
    tables = route_leaves(k, shifts, sizes, sources, targets)
    assert tables is not None
    return dict(zip(sites, tables))


def prime_powers(k):
    p = 2
    while p*p <= k:
        power = 1
        while k % p == 0:
            k //= p
            power *= p
        if power > 1:
            yield p, power
        p += 1
    if k > 1:
        yield k, k


def choose_labels(k, children, boundary_sum, sites, pins):
    """Solve the moment while making site-label differences generate Z/k."""
    free = [v for v in range(len(children)) if v not in pins]
    if len(sites) < 3 or len(set(sites) - pins.keys()) < 2:
        raise ValueError("three sites, with at least two free, are required")
    target = -boundary_sum - sum(children[v]*z for v, z in pins.items())
    labels = [0]*len(children)
    modulus = 1
    for p, power in prime_powers(k):
        divisor = reduce(gcd, (children[v] for v in free), power)
        if target % divisor:
            return None
        reduced = power//divisor
        origin = [pins.get(v, 0) % power for v in range(len(children))]
        pivot = None
        if reduced > 1:
            pivot = next(v for v in free if children[v]//divisor % p)
            inv = pow(children[pivot]//divisor, -1, reduced)
            origin[pivot] = (target//divisor)*inv % reduced

        local = origin.copy()
        for v in free:
            if len({local[u] % p for u in sites}) > 1:
                break
            if v == pivot:
                continue
            local = origin.copy()
            local[v] = 1
            if pivot is not None:
                local[pivot] = (local[pivot] - (children[v]//divisor)*inv) % reduced
        assert len({local[u] % p for u in sites}) > 1
        inverse = pow(modulus, -1, power)
        for v, residue in enumerate(local):
            labels[v] += modulus * (((residue-labels[v])*inverse) % power)
        modulus *= power
    return labels


def uniform_forest(k, parents, boundaries, populations, pins):
    """Exact uniform increment from a forest with large terminal leaf sets."""
    r = len(parents)
    sites = [v for v, n in enumerate(populations) if n]
    sizes = [populations[v] for v in sites]
    n = r + sum(sizes)
    if not sites or min(sizes) < 3*k*r or n % k:
        raise ValueError("the forest theorem assumes k divides n and at least 3kr leaves per site")
    children = populations.copy()
    for p in parents:
        if p >= 0:
            children[p] += 1
    labels = choose_labels(k, children, sum(boundaries.values()), sites, pins)
    if labels is None:
        return None
    baseline = labels[sites[-1]]
    shifts = [(labels[v]-baseline) % k for v in sites]
    sources, targets = [n//k]*k, [n//k]*k
    for v, p in enumerate(parents):
        parent_label = labels[p] if p >= 0 else boundaries[v]
        sources[labels[v]] -= 1
        targets[(labels[v]+parent_label-baseline) % k] -= 1
    tables = route_leaves(k, shifts, sizes, sources, targets)
    assert tables is not None
    return labels, dict(zip(sites, tables))

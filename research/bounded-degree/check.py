"""Build and check concrete instances of the bounded-degree embedding hypotheses."""

from collections import Counter
from random import Random


def require(condition, message):
    if not condition:
        raise ValueError(message)


def adjacency(n, edges):
    result = [set() for _ in range(n)]
    for a, b in edges:
        require(a != b and b not in result[a], "loop or duplicate edge")
        result[a].add(b)
        result[b].add(a)
    return result


def sample_forest(k, count, shape, even_sizes):
    if even_sizes:
        sizes = [(k - 1 + i) // count for i in reversed(range(count))]
    else:
        sizes = [1 + i % 3 for i in range(count - 1)]
        sizes.insert(0, k - 1 - sum(sizes))
    roots, edges = [], []
    start = 0
    for size in sizes:
        roots.append(start)
        for i in range(1, size):
            if shape == "path":
                parent = i - 1
            elif shape == "binary":
                parent = (i - 1) // 2
            else:
                parent = 0 if i in (1, 2) else i - 2
            edges.append((start + parent, start + i))
        start += size
    return roots, edges, sizes[0]


def make_auxiliary(k, roots, internal, primary_size, boundary, rng):
    old = adjacency(k - 1, internal)
    o, r = k - 1, roots[0]
    terminals = [i for i in range(primary_size) if i != r and len(old[i]) == 1]
    leaves = terminals[:2]
    protected = next(iter(old[leaves[0]])) if len(leaves) == 1 else None
    occupied = {r, *leaves}
    if protected is not None:
        occupied.add(protected)
    forbidden = occupied.union(*(old[i] for i in occupied))
    needed = int(boundary[0] != 0)
    if len(roots) == 2:
        needed += int(boundary[1] != 0)
    elif len(roots) > 2:
        needed += len(roots) - 1
    sites = []
    for i in range(primary_size):
        if i not in forbidden and len(sites) < needed:
            sites.append(i)
            forbidden.update({i, *old[i]})
    require(len(sites) == needed, "insufficient separated sites in fixture")
    for _ in range(5000):
        slots = iter(sites)
        pins = {u: rng.randrange(k) for u in roots}
        pins[o] = 0
        target = r
        if boundary[0]:
            target = next(slots)
            pins[target] = (pins[r] + boundary[0]) % k
        added = [(o, target)]
        if len(roots) == 2:
            target = o
            if boundary[1]:
                target = next(slots)
                pins[target] = boundary[1]
            added.append((target, roots[1]))
        elif len(roots) >= 3:
            for j in range(1, len(roots)):
                successor = 1 + j % (len(roots) - 1)
                target = next(slots)
                pins[target] = (pins[roots[successor]] + boundary[successor] - pins[roots[j]]) % k
                added.append((target, roots[j]))
        if len(set(pins.values())) != len(pins):
            continue
        if len({(pins[a] + pins[b]) % k for a, b in added}) == len(added):
            return internal + added, pins, leaves, protected
    raise ValueError("failed to choose root labels for fixture")


def assign_core(k, aux, pins, leaves, protected, rng):
    graph = adjacency(k, aux)
    degree = [len(neighbors) for neighbors in graph]
    q = set(pins).union(leaves)
    for d in set(degree):
        outside = [i for i, v in enumerate(degree) if v == d and i not in q]
        rng.shuffle(outside)
        if protected in outside:
            outside.remove(protected)
            outside.append(protected)
        inside = degree.count(d) - len(outside)
        number = max(0, 6 - inside)
        q.update(outside if len(outside) - number < 6 else outside[:number])
    if protected is not None:
        require(protected not in q, "reserved leaf has a core neighbor")
    d = max((d for d in set(degree) if d >= 2), key=degree.count)
    remote = set(range(k)) - q - set().union(*(graph[i] for i in q)) - {protected}
    choices = [i for i in sorted(remote) if degree[i] == d]
    z = choices[0]
    other = next(i for i in choices if i != z and i not in graph[z])
    q.update([z, other])
    fixed = dict(pins)
    edges = [(a, b) for a, b in aux if a in q and b in q]
    for i in sorted(q - set(fixed) - set(leaves) - {z, other}):
        used = {(fixed[a] + fixed[b]) % k for a, b in edges if a in fixed and b in fixed}
        banned = set(fixed.values())
        for j in graph[i].intersection(fixed):
            banned.update((w - fixed[j]) % k for w in used)
        fixed[i] = rng.choice([x for x in range(k) if x not in banned])
    group_sum = k * (k - 1) // 2 % k
    for _ in range(5000):
        labels = dict(fixed)
        for i in [*leaves, z]:
            labels[i] = rng.randrange(k)
        labels[other] = (group_sum - sum(labels.values())) % k
        if len(set(labels.values())) != len(labels):
            continue
        missing = (group_sum - sum(degree[i] * x for i, x in labels.items())) % k
        sums = {(labels[a] + labels[b]) % k for a, b in edges}
        if len(sums) == len(edges) and missing not in sums:
            return labels, missing
    raise ValueError("failed to solve the two core conditions for fixture")


def verify(k, roots, internal, aux, labels, missing, original_boundary, omitted):
    # Verify the constructed witness directly, independently of its parametrization.
    graph = adjacency(k, aux)
    reached, todo = {0}, [0]
    while todo:
        for neighbor in graph[todo.pop()]:
            if neighbor not in reached:
                reached.add(neighbor)
                todo.append(neighbor)
    require(len(aux) == k - 1 and len(reached) == k, "auxiliary graph is not a tree")
    forest = adjacency(k - 1, internal)
    delta = max(len(row) + int(i in roots) for i, row in enumerate(forest))
    require(max(map(len, graph)) <= delta + 1, "too large an auxiliary degree")
    original = {tuple(sorted(e)) for e in internal}
    auxiliary = {tuple(sorted(e)) for e in aux}
    require(original <= auxiliary, "lost an internal edge")
    require(labels[k - 1] == 0, "dummy label is not zero")
    new = Counter((labels[a] + labels[b] + 2 * omitted) % k for a, b in auxiliary - original)
    old = Counter((labels[r] + omitted + b) % k for r, b in zip(roots, original_boundary))
    require(old == new, "boundary weight multiset changed")
    require(len(set(labels.values())) == len(labels), "repeated core label")
    edges = [(a, b) for a, b in aux if a in labels and b in labels]
    weights = Counter((labels[a] + labels[b]) % k for a, b in edges)
    require(all(n == 1 for n in weights.values()) and missing not in weights, "bad core weights")
    for d in set(map(len, graph)):
        total = sum(len(neighbors) == d for neighbors in graph)
        inside = sum(len(graph[i]) == d for i in labels)
        require(inside == total or min(inside, total - inside) >= 6, "invalid degree core")
    require(sum(labels.values()) % k == sum(range(k)) % k, "vertex-target sum")
    target_sum = sum(i for i in range(k) if i != missing)
    require(sum(len(graph[i]) * x for i, x in labels.items()) % k == target_sum % k,
            "weight-target sum")


def main():
    rng = Random(1991)
    cases = 0
    for k in (251, 256, 315, 512):
        for c in (1, 2, 3, 5):
            for shape in ("path", "binary", "fork"):
                for even_sizes in (False, True):
                    roots, internal, primary_size = sample_forest(k, c, shape, even_sizes)
                    boundaries = [[0] * c, [9] * c, [i % 3 for i in range(c)],
                                  [rng.randrange(k) for _ in range(c)]]
                    for b in boundaries:
                        aux, pins, leaves, protected = make_auxiliary(k, roots, internal, primary_size, b, rng)
                        labels, missing = assign_core(k, aux, pins, leaves, protected, rng)
                        omitted = rng.randrange(k)
                        original = [(x + omitted) % k for x in b]
                        verify(k, roots, internal, aux, labels, missing, original, omitted)
                        cases += 1
    print(f"Verified the boundary multisets and both embedding sums in {cases} instances.")


if __name__ == "__main__":
    main()

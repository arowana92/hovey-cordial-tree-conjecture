"""Audit edge cuts, matching, affine labels and the embedding core on concrete forests."""

from collections import Counter, defaultdict
from itertools import combinations
from math import gcd
from random import Random

from check import adjacency, assign_core, require, sample_forest, verify


def expression(*terms, constant=0):
    # Nonnegative indices denote original free vertices, -1 is the constant.
    row = Counter({-1: constant})
    for variable, coefficient in terms:
        row[variable] += coefficient
    return {i: a for i, a in row.items() if a}


def difference(lhs, rhs):
    return expression(*lhs.items(), *((i, -a) for i, a in rhs.items()))


def choose_variables(label_forms, weight_forms, k, rng, avoid=()):
    tests = defaultdict(list)
    for forms in (label_forms, weight_forms):
        for a, b in combinations(forms, 2):
            row = difference(a, b)
            last = max(row, default=-1)
            if last < 0:
                require(row.get(-1, 0) % k != 0, "identically equal expressions")
            else:
                tests[last].append(row)
    for form in label_forms + weight_forms:
        for value in avoid:
            row = difference(form, {-1: value})
            last = max(row, default=-1)
            if last >= 0:
                tests[last].append(row)
            else:
                require(row.get(-1, 0) % k != 0, "fixed value in reserved set")
    point = {-1: 1}
    for i in sorted({j for f in label_forms + weight_forms for j in f if j >= 0}):
        banned = set()
        for row in tests[i]:
            a = row[i]
            g = gcd(a, k)
            rhs = -sum(c * point[j] for j, c in row.items() if j != i)
            if rhs % g == 0:
                x = (rhs // g) * pow(a // g, -1, k // g) % (k // g)
                banned.update(x + t * (k // g) for t in range(g))
        available = [x for x in range(k) if x not in banned]
        require(available, "greedy affine constraints exhausted the group")
        point[i] = rng.choice(available)
    return lambda row: sum(a * point[j] for j, a in row.items()) % k


def match(others, parents):
    owner = {}

    def augment(j, seen):
        for i in others:
            if i in seen or i == j or parents[i] == j:
                continue
            seen.add(i)
            if i not in owner or augment(owner[i], seen):
                owner[i] = j
                return True
        return False

    for j in others:
        require(augment(j, set()), "Hall matching failed")
    return {j: i for i, j in owner.items()}


def construct(parents, k, cap, rng, avoid=()):
    n = len(parents)
    children = [[] for _ in parents]
    roots = {i for i, p in enumerate(parents) if p < 0}
    for i, p in enumerate(parents):
        if p >= 0:
            children[p].append(i)
    leaves = [i for i in range(n) if i not in roots and not children[i]][:2]
    protected = parents[leaves[0]] if len(leaves) == 1 else None
    for group in children:
        preferred = sorted(group, key=lambda i: i not in leaves)
        roots.update(preferred[cap - 1:])
    fixed = roots.union(parents[r] for r in roots if parents[r] >= 0)
    excluded = fixed.union(leaves, {protected})
    buffers = []
    for v, p in enumerate(parents):
        if p >= 0 and v not in excluded and p not in excluded:
            buffers.append(v)
            excluded.update((v, p))
            if len(buffers) == 5:
                break
    require(len(buffers) == 5, "too few buffer edges in fixture")
    roots.update(buffers)
    fixed.update(buffers)
    fixed.update(parents[v] for v in buffers)
    kept = [(v, p) for v, p in enumerate(parents) if v not in roots]
    graph = adjacency(n, kept)
    marked = fixed.union(leaves)
    if protected is not None:
        marked.add(protected)
    unavailable = marked.union(*(graph[i] for i in marked))
    component = {}
    pools = {r: [] for r in roots}
    for v, p in enumerate(parents):
        r = v if v in roots else component[p]
        component[v] = r
        if v not in unavailable:
            pools[r].append(v)
            unavailable.update(graph[v])
    order = sorted(roots, key=lambda r: (-len(pools[r]), r))
    first, *others = order
    matching = match(others, parents)
    connectors = []
    forms = {v: expression((v, 1)) for v in fixed}
    forms[n] = {}
    weights = {}
    for r in order:
        p = parents[r]
        weights[r] = (expression((r, 1), (p, 1)) if p >= 0
                      else expression((r, 1), constant=-1 - p))
    sites = pools[first][:]
    if parents[first] == -1:
        connectors.append((n, first))
    else:
        site = sites.pop()
        forms[site] = weights[first]
        connectors.append((n, site))
    for r in others:
        site = sites.pop()
        forms[site] = difference(weights[matching[r]], forms[r])
        connectors.append((r, site))
        sites.extend(pools[r])
    edge_forms = list(weights.values()) + [
        expression((v, 1), (p, 1)) for v, p in kept if v in fixed and p in fixed
    ]
    evaluate = choose_variables(list(forms.values()), edge_forms, k, rng, avoid)
    pins = {v: evaluate(f) for v, f in forms.items()}
    return order, kept, kept + connectors, pins, leaves, protected


def run():
    rng = Random(4179)
    cases = adjacent = 0
    max_degree = max_cut = 0
    for k in (251, 256, 511, 729, 1024):
        for c in (1, 3, 6):
            for shape in ("path", "binary", "fork"):
                roots, internal, _ = sample_forest(k, c, shape, False)
                for heavy in (False, True):
                    par = [-1] * (k - 1)
                    for p, v in internal:
                        par[v] = p
                    for r in roots:
                        par[r] = -1 - rng.randrange(3)
                    if heavy:
                        # Make adjacent exceptional vertices, one itself a cut root.
                        for v in range(3, 17):
                            par[v] = 0
                        for v in range(17, 30):
                            par[v] = 15
                    order, kept, aux, pins, leaves, protected = construct(par, k, 3, rng)
                    labels, missing = assign_core(k, aux, pins, leaves, protected, rng)
                    omitted = rng.randrange(k)
                    boundary = [((labels[par[r]] if par[r] >= 0 else -1 - par[r]) + omitted) % k
                                for r in order]
                    # Actual internal cuts use the same free labels as the original graph.
                    require(all(par[r] < 0 or par[r] in pins for r in order), "unfixed cut parent")
                    original = {(i, p) for i, p in enumerate(par) if p >= 0}
                    restored = set(kept).union((i, par[i]) for i in order if par[i] >= 0)
                    require(original == restored, "the specified cuts do not reconstruct the forest")
                    require(set(roots) == {i for i in order if par[i] < 0}, "wrong external boundary")
                    verify(k, order, kept, aux, labels, missing, boundary, omitted)
                    require(max(map(len, adjacency(k, aux))) <= 4, "auxiliary degree exceeds D+1")
                    deg = Counter(par)
                    max_degree = max(max_degree, max(1 + deg[i] for i in range(k - 1)))
                    max_cut = max(max_cut, len(order) - c)
                    adjacent += any(p >= 0 and 1 + deg[p] > 3 and 1 + deg[i] > 3
                                    for i, p in enumerate(par))
                    cases += 1
    print(f"Verified {cases} forests, including {adjacent} with adjacent exceptional vertices. "
          f"Maximum original free degree {max_degree}, maximum cut count {max_cut}.")


if __name__ == "__main__":
    run()

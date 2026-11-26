"""Finite checks for the common-boundary forest proof. Run from the repository root."""

from collections import Counter
from fractions import Fraction
from itertools import product
from random import Random

from research.hub.branching_pools import finish_vertex, palette_law
from research.rainbow.verify import rooted_shapes


def orbit_laws():
    count = 0
    for k in (30, 41, 64, 105):
        for roots in (k // 3, 2 * k // 3):
            r = max(2, (k - roots) // 6)
            p = Fraction(r, k)
            for marked_primary in range(r + 1):
                rows = [r - marked_primary, r, k - roots - 2 * r + marked_primary]
                columns = [r, k - roots - r]
                cells = palette_law(k, rows, columns, {(1, 0)})
                # Record indicators for the marks, the deferred children and their colors.
                law = Counter()
                law[True, False, False] += Fraction(marked_primary, k)
                law[False, False, False] += Fraction(roots - marked_primary, k)
                for i, row in enumerate(cells[1:]):
                    for j, mass in enumerate(row[1:]):
                        law[i == 0, i == 1, j == 0] += Fraction(mass, k * k)
                assert sum(law.values()) == 1
                assert all(sum(mass for bits, mass in law.items() if bits[i]) == p
                           for i in range(3))
                assert sum(mass for bits, mass in law.items() if bits[1] and bits[2]) == p*p
                for size in (1, 2):
                    probabilities = Counter()
                    for states in product(law, repeat=size):
                        mass = Fraction(1, 3)
                        for state in states:
                            mass *= law[state]
                        for chosen in range(3):
                            # For the reflected color role, membership uses the inverse site.
                            received = all(states[(-1-i) % size if chosen == 2 else i][chosen]
                                           for i in range(size))
                            accept = (p if size == 1 else 1) if received else 0
                            probabilities[chosen] += mass * accept
                            probabilities[None] += mass * (1 - accept)
                    assert all(probabilities[i] == p*p/3 for i in range(3))
                    assert probabilities[None] == 1 - p*p
                    count += 1
    return count


def ordinary_suffix(tree, leaves, modulus):
    # tree is the ordinary core, its children at zero all have order at least two.
    h = len(tree)
    t = (h + leaves - 1) % modulus
    assert leaves < t and h > modulus
    a = modulus // 8
    removed = min(leaves, max(0, t-a))
    s = t - removed
    children = [[] for _ in tree]
    sizes = [1] * h
    for v in range(h - 1, 0, -1):
        p = tree[v]
        children[p].append(v)
        sizes[p] += sizes[v]
    assert all(sizes[v] >= 2 for v in children[0])
    order, stack = [], [0]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(sorted(children[v], key=lambda x: (sizes[x], x), reverse=True))
    return set(order[-s:]), removed, modulus - 1 - t


def check_suffix(tree, leaves, k):
    kept_out, removed, padding = ordinary_suffix(tree, leaves, k)
    edges = [(p, v) for v, p in enumerate(tree) if v and v in kept_out]
    crossing = [(p, v) for p, v in edges if p not in kept_out]
    exceptions = len([p for p, _ in crossing if p != 0])
    inside = sum(p in kept_out for p, _ in edges)
    assert 0 not in kept_out
    assert all(p not in kept_out for v,p in enumerate(tree) if v not in kept_out)
    degrees = Counter(tree[1:])
    d = max([3] + [degrees[v] + 1 for v in range(1, len(tree))])
    assert exceptions <= d * (2 + k.bit_length())
    assert 2 * (inside + exceptions) >= len(kept_out)
    assert len(kept_out) + removed + padding == k - 1
    assert inside + padding >= k//8 / 2 - exceptions - 1
    if k//8 / 2 - exceptions - 1 >= k/20:
        assert inside + padding >= k/20
    return len(crossing) - exceptions, exceptions, inside + padding


def strip_root_leaves(tree):
    parents = set(tree[1:])
    kept = [v for v,p in enumerate(tree) if v == 0 or p != 0 or v in parents]
    index = {v: i for i, v in enumerate(kept)}
    return [-1] + [index[tree[v]] for v in kept[1:]]


def separators(tree, m):
    # Bottom-up construction, checked by rebuilding the components and positional matchings.
    pending = [1] * len(tree)
    removed = set()
    for v in reversed(range(len(tree))):
        if pending[v] >= m:
            removed.add(v)
        elif tree[v] >= 0:
            pending[tree[v]] += pending[v]
    assert len(removed) * m <= len(tree)
    parts, owner = [], {}
    for v, p in enumerate(tree):
        if v in removed:
            continue
        if p not in owner:
            owner[v] = len(parts)
            parts.append([])
        else:
            owner[v] = owner[p]
        parts[owner[v]].append(v)
    assert all(len(part) < m for part in parts)
    for j in range(1, max(map(len, parts), default=0)):
        layer = [part[j] for part in parts if j < len(part)]
        assert len(set(tree[v] for v in layer)) == len(layer)
        assert not (set(layer) & {tree[v] for v in layer})
    return len(removed)


def cut_checks(rng):
    count = seps = most_primary = most_other = 0
    for n in range(5, 12):
        for tree in rooted_shapes(n).values():
            core = strip_root_leaves(tree)
            for k in range(4, len(core)):
                for leaves in (0, 1, k//2):
                    if leaves < (len(core) + leaves - 1) % k:
                        primary, other, _ = check_suffix(core, leaves, k)
                        most_primary = max(most_primary, primary)
                        most_other = max(most_other, other)
                        count += 1
            seps += separators(tree, 3)
    # A hub with branches of sizes from two to 70 at bounded nonroot degree.
    for n in (250, 2048, 12000):
        for mode in range(3):
            tree = [-1]
            while len(tree) < n:
                top = len(tree)
                length = rng.randrange(2, 71)
                tree.append(0)
                for j in range(1, length):
                    parent = top + (j-1 if mode == 0 else (j-1)//(2+mode))
                    tree.append(parent)
            for k in (97, n//3, n-3):
                for leaves in (0, k//10, k//2, k-3):
                    if leaves < (len(tree) + leaves - 1) % k:
                        primary, other, _ = check_suffix(tree, leaves, k)
                        most_primary = max(most_primary, primary)
                        most_other = max(most_other, other)
                        count += 1
            for m in (3, 7, 15):
                seps += separators(tree, m)
    assert most_primary > 10 and most_other >= 2
    return count, seps, most_primary, most_other


def witness(tree, boundary, k, u, fixed):
    """Direct depth-first search using only vertex distinctness and actual incoming sums."""
    labels, used, colors = [None] * len(tree), {u}, set()
    if len(set(fixed.values())) != len(fixed) or u in fixed.values():
        return None
    reserved = set(fixed.values())
    internal_parents = set(tree)
    singletons = [v for v,p in enumerate(tree)
                  if p < 0 and v not in internal_parents and boundary[v] == 0 and v not in fixed]
    singles = set(singletons)
    order = [v for v in range(len(tree)) if v not in singles]

    def descend(position):
        if position == len(order):
            remaining = set(range(k)) - used
            if remaining & colors:
                return None
            assert len(remaining) == len(singletons)
            for v,x in zip(singletons, sorted(remaining)):
                labels[v] = x
            return tuple(labels)
        v = order[position]
        a = labels[tree[v]] if tree[v] >= 0 else boundary[v]
        choices = (fixed[v],) if v in fixed else range(k)
        for x in choices:
            c = (x + a) % k
            if x in used or c in colors or (v not in fixed and x in reserved):
                continue
            used.add(x)
            colors.add(c)
            labels[v] = x
            found = descend(position + 1)
            if found is not None:
                return found
            labels[v] = None
            colors.remove(c)
            used.remove(x)
        return None

    return descend(0)


def exact_checks():
    cases = Counter()
    common_parents = matching_primary = mixed = composites = 0
    for k in range(11, 17):
        for mode in ('matching', 'path-common', 'path-distinct'):
            core = ([-1,0,-1,2,-1,4,4,-1] if mode == 'matching' else
                    [-1,0,1,2,-1,-1,-1,-1] if mode == 'path-common' else
                    [-1,0,1,2,-1,-1,5,-1])
            tree = core + [7] + [-1] * (k - 2 - len(core))
            for extra in (0, 1):
                boundary = [0] * len(tree)
                if extra:
                    boundary[-1] = 3
                for u in (0, 1, k//2):
                    choices = ([{7: 0}] if u else
                               [{7: a, 8: (-a) % k} for a in range(1, k) if 2*a % k])
                    labels = next((row for fix in choices
                                   if (row := witness(tree, boundary, k, u, fix)) is not None), None)
                    assert labels is not None, (k, mode, extra, u)
                    parents = [boundary[v] if p == -1 else labels[p] for v,p in enumerate(tree)]
                    weights = [(p+x) % k for p,x in zip(parents,labels)]
                    assert set(labels) == set(range(k)) - {u}
                    assert len(set(weights)) == k - 1 and 0 in weights
                    gap, = set(range(k)) - set(weights)
                    if mode == 'matching':
                        z = 4
                        neighbors = [parents[z], labels[5], labels[6]]
                        X = [labels[0], labels[2]]
                        assert 0 not in X + [labels[1], labels[3], weights[1], weights[3]]
                        V = {labels[z], labels[1], labels[3]}
                        C = {gap, *(weights[i] for i in (4,5,6,1,3))}
                        assert len(C) == 6
                        A = sum(C) - sum(V) - sum(X) - sum(neighbors)
                        assert (A - 2*labels[z]) % k == gap
                        assert finish_vertex(k, neighbors, V, C, sum(X)) is not None
                        matching_primary += len(X)
                    else:
                        zi, wi = (4,5) if mode == 'path-common' else (4,6)
                        z,w = labels[zi], labels[wi]
                        p,q = parents[zi], parents[wi]
                        V = {z,w,labels[2]}
                        C = {gap, weights[zi], weights[wi], weights[2], weights[3]}
                        assert len(C) == 5
                        A = sum(C) - labels[1] - labels[3] - 2*sum(V) - p - q
                        assert (A+w) % k != p
                        assert (A+z+w) % k == gap
                        assert (labels[1] + 2*labels[2] + labels[3]) % k == (weights[2]+weights[3]) % k
                        common_parents += p == q
                    # Translate to genuinely nonzero common boundary, keeping the correct gap shift.
                    shift = 3
                    shifted = [(x+shift) % k for x in labels]
                    after = [((boundary[v]+shift if p < 0 else shifted[p]) + shifted[v]) % k
                             for v,p in enumerate(tree)]
                    assert set(shifted) == set(range(k)) - {(u+shift) % k}
                    assert set(after) == set(range(k)) - {(gap+2*shift) % k}
                    cases[mode, u == 0, extra] += 1
                    mixed += extra
                    composites += any(k % j == 0 for j in range(2, int(k**0.5)+1))
    assert len(cases) == 12 and sum(cases.values()) == 108
    assert common_parents and matching_primary and mixed and composites
    return sum(cases.values()), common_parents, matching_primary, mixed, composites


if __name__ == '__main__':
    print(f"{orbit_laws()} exact symmetric orbit laws, including singleton inverse orbits.")
    n, s, a, b = cut_checks(Random(913701))
    print(f"{n:,} rooted suffixes and {s:,} separator selections checked; "
          f"up to {a} common and {b} exceptional boundary edges in a cut.")
    n, p, x, e, c = exact_checks()
    print(f"{n} direct forest completions, {p} two-leaf repairs with equal parents, "
          f"{x} marked primary parents, {e} mixed-boundary and {c} composite instances.")

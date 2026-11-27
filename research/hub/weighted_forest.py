"""Integer forest preparation with simultaneous control of terminal-parent sums."""

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from random import Random

from research.hub.integer_layers import candidate, offsets_for_level
from research.hub.polynomial_hub import DEPTH
from research.hub.polynomial_two_hubs import forest_seed


def echelon(vectors):
    """Yield a pivot for each independent column and a rational relation for every other column."""
    pivots = {}
    for i, vec in enumerate(vectors):
        v = list(map(Fraction, vec))
        combination = {i: Fraction(1)}
        for j, (old, old_combination) in sorted(pivots.items()):
            a = v[j]
            if a:
                v = [x-a*y for x, y in zip(v, old)]
                for k, c in old_combination.items():
                    combination[k] = combination.get(k, 0)-a*c
        pivot = next((j for j, a in enumerate(v) if a), None)
        if pivot is None:
            yield i, None, {k:c for k,c in combination.items() if c}
        else:
            a = v[pivot]
            pivots[pivot] = [x/a for x in v], {k:c/a for k,c in combination.items() if c}
            yield i, pivot, None


def inverse(cols):
    n = len(cols)
    rows = [[Fraction(col[i]) for col in cols]+[Fraction(i==j) for j in range(n)]
            for i in range(n)]
    for i in range(n):
        j = next(j for j in range(i, n) if rows[j][i])
        rows[j], rows[i] = rows[i], rows[j]
        a = rows[i][i]
        rows[i] = [x/a for x in rows[i]]
        for j in range(n):
            if j != i and rows[j][i]:
                a = rows[j][i]
                rows[j] = [x-a*y for x, y in zip(rows[j], rows[i])]
    return [row[n:] for row in rows]


def signed_sum(cols, signs):
    return tuple(sum(s*x for s, x in zip(signs, row)) for row in zip(*cols))


def sign_basis(cols):
    n, rank = len(cols), len(cols[0])
    if not rank:
        return [], []
    def initial(i):
        return tuple(-1 if j == i-1 else 1 for j in range(n))
    initial_cols = (signed_sum(cols, initial(i)) for i in range(n+1))
    signs = []
    for i, pivot, _ in echelon(initial_cols):
        if pivot is not None:
            signs.append(initial(i))
            if len(signs) == rank:
                break
    basis = [signed_sum(cols, s) for s in signs]
    while True:
        dual = inverse(basis)
        for j, row in enumerate(dual):
            products = [sum(a*x for a, x in zip(row, w)) for w in cols]
            if sum(map(abs, products)) > 1:
                signs[j] = tuple(1 if x>=0 else -1 for x in products)
                basis[j] = signed_sum(cols, signs[j])
                break
        else:
            return dual, signs


def split_direction(cols, ids):
    active = list(ids)
    slopes = {v: Fraction(0) for v in ids}
    while active:
        relation = next((r for _, _, r in echelon(cols[v] for v in active) if r), None)
        if relation is None:
            break
        step = min(((1 if c>0 else -1)-slopes[active[i]])/c for i,c in relation.items())
        for i, c in relation.items():
            slopes[active[i]] += step*c
        active = [v for v in active if abs(slopes[v]) < 1]
    return slopes


@dataclass
class Plan:
    nodes: list
    cols: list
    dual: list
    signatures: list
    parts: list


def partition(nodes, weights):
    coordinates = [i for i, p, _ in echelon(zip(*weights)) if p is not None]
    cols = [tuple(w[i] for i in coordinates) for w in weights]
    dual, signs = sign_basis(cols)
    baskets = defaultdict(list)
    for i in range(len(nodes)):
        baskets[tuple(s[i] for s in signs)].append(i)
    parts = []
    for g, ids in enumerate(baskets.values()):
        slopes = split_direction(cols, ids)
        for s in (-1, 1):
            side = [nodes[i] for i in ids if slopes[i] == s]
            if side:
                parts.append((g, Fraction(s), side))
        for i in ids:
            if abs(slopes[i]) < 1:
                parts.append((g, slopes[i], [nodes[i]]))
    return Plan(nodes, cols, dual, list(baskets), parts)


def trials(width, small, baskets, parts, rng):
    lengths = [width]*baskets+[small]*parts
    yield [0]*len(lengths)
    for _ in range(150):
        yield [rng.randrange(k) for k in lengths]
    count = width**baskets*small**parts
    for value in range(count):
        coords = []
        for k in lengths:
            value, r = divmod(value, k)
            coords.append(r)
        yield coords


def place(plan, jumps, used, blocked, rng):
    layouts = [offsets_for_level({v:jumps[v] for v in part}) for _, _, part in plan.parts]
    offsets = {v:a for row, _ in layouts for v,a in row.items()}
    target = signed_sum(plan.cols, [-offsets[v] for v in plan.nodes])
    c = [sum(a*x for a,x in zip(row, target)) for row in plan.dual]
    base = [sum(x*y for x,y in zip(c, sig)) for sig in plan.signatures]
    groups, parts = len(base), len(layouts)
    support = len(blocked)+len(plan.nodes)+1
    width = 100*(parts+1)**2*(support+1)**2
    small = 100*(parts+1)**2*(support+1)
    for coords in trials(width, small, groups, parts, rng):
        current, forbidden = used.copy(), blocked.copy()
        result = []
        for j, ((g, slope, _), (row, end)) in enumerate(zip(plan.parts, layouts)):
            exact = base[g]+slope*coords[g]
            x = exact.numerator//exact.denominator+coords[groups+j]
            placement = candidate(row, end, x, current, forbidden)
            if placement is None:
                break
            _, values, reserve, _ = placement
            current.update(values)
            forbidden.update(values | reserve)
            result.append(placement)
        else:
            return result
    raise AssertionError("weighted forest box exhausted")


def prepare(tree, boundary, fixed, terminal_counts, rng=None):
    """Label only the given free vertices. terminal_counts are masses on them."""
    rng = rng or Random(709)
    n = len(tree)-1
    if (not tree or tree[0] != -1 or any(not 0 <= p < v for v,p in enumerate(tree[1:], 1))
            or set(boundary) != {v for v in range(1, n+1) if not tree[v]}
            or not set(boundary.values()) <= set(fixed)
            or any(v not in range(1, n+1) or not isinstance(d, int) or d < 0
                   for v,d in terminal_counts.items())):
        raise ValueError("invalid forest, external boundary, or terminal counts")
    labels, _ = forest_seed(tree, boundary, n, max(map(abs, fixed), default=0), rng)
    used = set(labels.values()) | set(fixed)
    blocked = used.copy()
    depth = {}
    levels = defaultdict(list)
    kids = defaultdict(list)
    for v in range(1, n+1):
        if v not in labels:
            p = tree[v]
            depth[v] = depth.get(p, 0)+1
            levels[depth[v]].append(v)
            kids[p].append(v)
    assert max(levels, default=0) <= DEPTH
    plans = []
    child_class = {}
    group_count = 0
    for depth_index in range(max(levels, default=0), 0, -1):
        nodes = levels[depth_index]
        weights = []
        for v in nodes:
            row = [terminal_counts.get(v, 0)]+[0]*group_count
            for w in kids[v]:
                row[1+child_class[w]] += 1
            weights.append(row)
        plan = partition(nodes, weights)
        plans.append(plan)
        child_class = {v:j for j, (_, _, part) in enumerate(plan.parts) for v in part}
        group_count = len(plan.parts)
    pairs = []
    for plan in reversed(plans):
        jumps = {v:labels[tree[v]] if tree[v] else boundary[v] for v in plan.nodes}
        for row, values, reserve, jobs in place(plan, jumps, used, blocked, rng):
            labels.update(row)
            used.update(values)
            blocked.update(values | reserve)
            pairs.extend(jobs)
    return labels, pairs, plans

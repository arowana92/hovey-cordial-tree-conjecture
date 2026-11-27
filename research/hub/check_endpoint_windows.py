"""Recount the first extreme omission and the exact integer interval it produces."""

from collections import Counter
from random import Random

from research.hub.check_two_hub_contraction import audit_ranges
from research.hub.decorated_spine import expand_edge, path_values
from research.hub.endpoint_windows import LEFT_MARK, RIGHT_MARK, extremal_mass
from research.hub.integer_layers import balanced_order, prepare
from research.hub.integer_windows import finish_walk, restore
from research.hub.star_repair import five_roots


def audit(parents, row, gap):
    xs = sorted(row.values())
    assert set(row) == set(range(len(parents))) and row[0] == 0
    assert len(set(xs)) == len(xs) and gap == xs[0] and -gap > xs[-1]
    edges = [row[v]+row[p] for v, p in enumerate(parents) if v]
    assert Counter([gap]+edges) == Counter(xs)
    holes = [(a+1, b) for a, b in zip(xs, xs[1:]) if b > a+1]
    for extension in (0, 1, 31):
        bands = holes+([(xs[-1]+1, xs[-1]+1+extension)] if extension else [])
        audit_ranges(xs, bands, gap, xs[-1]+1+extension)
        audit_ranges(edges, bands, gap+1, xs[-1]+1+extension)
    return len(edges)


def windows(kind, m, rng):
    core = [-1, 0, 1, 1, 2, 2, 3, 4, 5, 6]
    row, pairs, _ = prepare(core, {1: 0}, {0}, rng)
    row[0] = 0
    blocked = set(row.values()) | {v for _, t in pairs for v in (t, -t)}
    count = len(pairs)*(4 if kind == 'active' else 1)
    if kind == 'active':
        count += 8
    first = len(core)
    free = 1
    for _ in range(count):
        while free in blocked:
            free += 1
        row[len(core)] = free
        blocked.add(free)
        core.append(0)
    spare = iter(range(first, len(core)))
    parents = list(core)
    jobs = []
    for j, (b, t) in enumerate(pairs):
        blocks = []
        for k, length in enumerate([87] if kind == 'uniform' else [21, 21, 43, 43]):
            if kind == 'uniform':
                counts = [m if j == len(pairs)-1 or not m else 1+j%3]*length
            elif k < 2:
                counts = [0]*21
                counts[0] = 1+j
            else:
                counts = [rng.randrange(5) for _ in range(length)]
            blocks.append(expand_edge(parents, next(spare), [(d, ()) for d in counts]))
        jobs.append((kind, blocks, b, t))
    extras = []
    if kind == 'active':
        for i in range(8):
            counts = [rng.randrange(2) for _ in range(21)]
            # Both signs occur and the eight signed totals dominate any single slope.
            counts[9 if i%2 else 10] += 6
            extras.append(expand_edge(parents, next(spare), [(d, ()) for d in counts]))
    assert next(spare, None) is None
    gap = restore(parents, row, blocked, jobs, 0, rng, endpoint_windows=extras)
    return audit(parents, row, gap)


def common_stars(p, rng):
    parents = [-1, 0] if p else [-1]
    fixed = dict(enumerate([0, p] if p else [0]))
    groups = []
    slopes = {}
    for _ in range(10):
        roots, filled, pending = [], [], []
        arities = sorted((rng.randrange(1, 7) for _ in range(5)), reverse=True) if p else [4]
        for j, m in enumerate(arities):
            r = len(parents)
            roots.append(r)
            parents.extend([int(bool(p))]+[r]*m)
            tips = list(range(r+1, r+1+m))
            if j:
                filled.append(tips.pop(0))
            slopes.update((v, 1 if j<3 else -1) for v in tips)
            pending.extend(tips)
        groups.append((roots, filled, pending))
    width = 20*(len(parents)+1)**2
    jumps = {v: slopes[v] for _, _, leaves in groups[2:] for v in leaves}
    scale = extremal_mass(sum(jumps.values()), 2, len(parents), 20*width)
    for _ in range(100):
        row = {}
        for i, (roots, filled, pending) in enumerate(groups):
            d = (scale if i>=2 else 0)+rng.randrange(1, width+1)
            xs, ys = five_roots(p, d) if p else ([d], [])
            row.update(zip(roots+filled, xs+ys))
        if len(set(row.values())) != len(row) or set(fixed.values()).intersection(row.values()):
            continue
        a, b = [sorted(group[2], key=lambda v: -slopes[v]) for group in groups[:2]]
        order = [a[0], b[0]]+a[1:]+b[1:]+balanced_order(jumps)
        gap = finish_walk(row, set(fixed.values()), order, {v: row[parents[v]] for v in order}, 0)
        if gap is not None:
            row.update(fixed)
            return audit(parents, row, gap)
    raise AssertionError("no common-star specialization in test")


def main():
    for side, expected, z in ((0, RIGHT_MARK, 1080), (1, LEFT_MARK, 700)):
        for fixed in (0, -57, 22):
            for weight in (0, 147):
                old = [fixed, -630]
                new = [fixed, -1260]
                if side:
                    old.reverse()
                    new.reverse()
                a = path_values(*old, weight, z, None)
                b = path_values(*new, weight, 2*z, None)
                assert tuple(v-u for u, v in zip(a, b)) == expected
    rng = Random(814)
    data = [windows('uniform', m, rng) for m in (0, 1, 2, 9, 55)]
    data.extend(windows('active', 0, rng) for _ in range(4))
    data.extend(common_stars(p, rng) for _ in range(4) for p in (-5, 0, 7))
    print(f"24 exact bridge slope checks; {len(data)} extreme-gap trees with {sum(data):,} actual edges.")
    print(f"{3*len(data)} complete vertex and edge interval checks after adding root leaves.")


if __name__ == "__main__":
    main()

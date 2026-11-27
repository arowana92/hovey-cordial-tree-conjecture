"""Check pooled window and broom claims directly on integer-labeled trees."""

from collections import Counter
from random import Random

from research.hub.decorated_spine import expand_edge
from research.hub.integer_broom import finish
from research.hub.integer_layers import prepare
from research.hub.integer_windows import restore


def verify(kind, mode, rng):
    # Supply multiple actual discrepancies and sometimes unused neutral windows.
    core = [-1, 0, 1, 1, 2, 2, 3, 3, 4, 5, 8, 8, 9, 9, 10, 10, 11, 12]
    roots = {1: 0}
    row, pairs, _ = prepare(core, roots, {0}, rng)
    row[0] = 0
    pairs = list(pairs)
    assert 2 <= len(pairs) <= 14
    bounds = set(row.values()) | {v for _, t in pairs for v in (t, -t)}
    for x in range(1, 500):
        if len(pairs) >= 14:
            break
        if x not in bounds and -x not in bounds:
            pairs.append((x, x))
            bounds.update((x, -x))
    if kind == 'active':
        # Each window needs its own edge. Grow neutral branches at zero.
        for j in range(4*len(pairs)):
            idx = len(core)
            core.append(0)
            row[idx] = max(bounds)+2
            bounds.add(row[idx])
        first = idx-4*len(pairs)+1
    else:
        first = 1
    parents = list(core)
    jobs = []
    selected = []
    for i, (b, t) in enumerate(pairs):
        windows = []
        if kind == 'active':
            for k, length in enumerate((21, 21, 43, 43)):
                counts = [rng.randrange(5) for _ in range(length)]
                if k < 2:
                    counts = [0]*length
                    counts[rng.randrange(length)] = 1+i
                elif k == 3:
                    counts[0] += 20
                child = first+4*i+k
                windows.append(expand_edge(parents, child, [(m, ()) for m in counts]))
                selected.append(child)
        else:
            m = (i%3+1) if mode else 0
            child = first+i
            windows.append(expand_edge(parents, child, [(m, ())]*87))
            selected.append(child)
        jobs.append((kind, windows, b, t))
    gap = restore(parents, row, bounds, jobs, 0, rng)
    assert len(set(row.values())) == len(row) == len(parents)
    vertices = Counter(row.values())
    weights = Counter(row[v]+row[p] for v,p in enumerate(parents) if v)
    weights[gap] += 1
    assert vertices == weights
    for child in selected:
        v = parents[child]
        while v >= len(core):
            v = parents[v]
        assert v == core[child]
    return len(parents)-1


def brooms():
    cases = 0
    for anchors in ((0, 1), (-1, 0, 2), (-3, 0, 1, 4)):
        for p in range(-17, 18 if len(anchors) > 2 else 1):
            fixed = {-23, 0, 4, 11, p, *anchors}
            for gap in (min(fixed), 0, max(fixed)):
                for n in (1, 2, 9):
                    x, tips, fillers = finish(fixed, gap, p, n, anchors)
                    labels = [x, *tips]+[v for _, v in fillers]
                    weights = Counter([p+x]+[x+v for v in tips]+[a+v for a, v in fillers])
                    weights[tips[-1]] += 1
                    expected = Counter(labels)
                    expected[gap] += 1
                    assert weights == expected and set(labels).isdisjoint(fixed)
                    assert len(set(labels)) == len(labels) and tips[-1] == min(set(labels)|fixed)
                    assert all(a in anchors for a, v in fillers)
                    cases += 1
    return cases


def main():
    rng = Random(1477)
    edges = sum(verify(kind, mode, rng) for kind, mode in
                [('active', 1), ('uniform', 1), ('uniform', 0)]*3)
    print(f"9 multi-window restorations, 126 repair jobs, {edges:,} actual edge sums.")
    print(f"{brooms():,} integer broom placements at signed boundary labels.")


if __name__ == "__main__":
    main()

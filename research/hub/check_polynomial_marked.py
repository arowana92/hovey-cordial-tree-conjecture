"""Compose the integer forest, pooled windows, broom and exact leaf counts."""

from collections import Counter
from random import Random

from research.hub.check_two_hub_contraction import audit_ranges
from research.hub.decorated_spine import expand_edge
from research.hub.integer_broom import finish
from research.hub.integer_layers import prepare
from research.hub.integer_windows import restore
from research.hub.marked_leaf_blocks import complete


def audit(anchors, kind, rng):
    # Seed edges (1,-1), (-1,2), (2,0) give weights 0,1,2.
    seeds = [1, -1, 2, 0]
    parents = [-1, 0, 1, 2]
    labels = dict(enumerate(seeds))
    virtual = [-1]
    boundary = {}
    index = {0: None}
    for i in range(38):
        parent = 0 if i < 16 else rng.randrange(1, i+1)
        v = len(virtual)
        virtual.append(parent)
        index[v] = len(parents)
        if parent == 0:
            real = rng.randrange(len(seeds))
            boundary[v] = seeds[real]
        else:
            real = index[parent]
        parents.append(real)
    free, pairs, _ = prepare(virtual, boundary, set(seeds), rng)
    labels.update((index[v], x) for v, x in free.items())
    blocked = set(labels.values()) | {u for _, t in pairs for u in (t, -t)}
    assert 1 <= len(pairs) <= 8
    core = list(parents)
    jobs = []
    expected_paths = {}
    for j, (b, t) in enumerate(pairs):
        windows = []
        for i, length in enumerate([87] if kind == 'uniform' else [21, 21, 43, 43]):
            if kind == 'uniform':
                counts = [j%3+1]*length
            elif i < 2:
                counts = [0]*length
                counts[1+i] = 2+j
            else:
                counts = [rng.randrange(4) for _ in range(length)]
            child = len(seeds)+(j if kind == 'uniform' else 4*j+i)
            w = expand_edge(parents, child, [(m, ()) for m in counts])
            expected_paths[child] = length
            windows.append(w)
        jobs.append((kind, windows, b, t))
    gap = restore(parents, labels, blocked, jobs, -1, rng)
    for child, length in expected_paths.items():
        v = child
        for _ in range(length):
            v = parents[v]
            assert v >= len(core)
        assert parents[v] == core[child]

    parent_digit = -1 if len(anchors) == 2 else 2
    x, tips, fillers = finish(set(labels.values()), gap, parent_digit, 17, anchors)
    z = len(parents)
    parents.extend([seeds.index(parent_digit)]+[z]*len(tips))
    labels.update(enumerate([x]+tips, z))
    assert len(parents) == len(labels)
    all_values = sorted([*labels.values(), *(v for p, v in fillers)])
    assert len(set(all_values)) == len(all_values)
    holes = [(a+1, b) for a, b in zip(all_values, all_values[1:]) if a+1 < b]
    lo, hi = all_values[0], all_values[-1]
    edges = [labels[v]+labels[p] for v, p in enumerate(parents) if v]
    audit_ranges(all_values, holes, lo, hi+1)
    audit_ranges(edges+[p+v for p, v in fillers], holes, lo+1, hi+1)

    # These requested counts are set from the size of the constructed core interval,
    # before choosing the final extension blocks. Recount every population below.
    promised = {p: 3*(hi-lo+1)+100000 for p in anchors}
    promised[0] *= 2
    charged = Counter(p for p, v in fillers)
    charged[0] += sum(b-a for a, b in holes)
    remaining = {p: c-charged[p] for p, c in promised.items()}
    for block in complete(remaining, anchors):
        d = len(block.parents)
        assert sorted(i+p-block.offset for i, p in enumerate(block.parents)) == list(range(d))
        for p, c in Counter(block.parents).items():
            charged[p] += c*block.copies
    assert charged == Counter(promised)
    return len(edges), len(jobs), hi-lo+1


def main():
    rng = Random(5119)
    data = [audit(anchors, kind, rng) for _ in range(3)
            for anchors in ((0, 1), (-1, 0, 2), (-1, 0, 1, 2))
            for kind in ('uniform', 'active')]
    print(f"{len(data)} full marked constructions, {sum(d[1] for d in data)} repair jobs, "
          f"{sum(d[0] for d in data):,} ordinary edges.")
    print(f"Independent interval and population checks through width {max(d[2] for d in data):,}.")


if __name__ == "__main__":
    main()

"""Compose the integer forest, pooled windows, broom and exact leaf counts."""

from collections import Counter
from random import Random
from types import SimpleNamespace

from research.hub.check_two_hub_contraction import audit_ranges
from research.hub.decorated_spine import expand_edge
from research.hub.dominant_marked import buffer_interval
from research.hub.integer_broom import finish
from research.hub.integer_layers import prepare
from research.hub.integer_windows import restore
from research.hub.marked_leaf_blocks import complete, insertion
from research.hub.two_hub_buffer import insert_neutral
from research.hub.two_hub_contraction import Interval, remove_fillers


def test_buffer(parents, labels, anchors, gap, rng):
    occupied = sorted(labels.values())
    assert gap == occupied[0] and -gap > occupied[-1]+20
    iv = Interval(SimpleNamespace(lo=gap, hi=occupied[-1], added=[]))
    iv.blocks = [(0, a+1, b) for a, b in zip(occupied, occupied[1:]) if a+1 < b]
    band, slot = ((1, -1), 1) if len(anchors)==2 else insertion(anchors, -1, 0)
    h = len(parents)+300
    iv, path, limit, moves, minor = buffer_interval(iv, band, slot, 2, -1, h, 96)
    assert minor <= (len(band)-1)*moves and moves%6 == 0
    def replace(child, inside):
        p = parents[child]
        for x in inside:
            labels[len(parents)] = x
            parents.append(p)
            p = len(parents)-1
        parents[child] = p
    assert labels[2] == 2 and labels[parents[2]] == -1
    replace(2, path[-2:0:-1])
    v = next(v for v in range(4, len(occupied)) if
             labels[v] and labels[parents[v]] and labels[v]+labels[parents[v]])
    used = set(labels.values())
    forbidden = [(a, b) for p, a, b in iv.blocks if p]
    row = insert_neutral((labels[parents[v]], labels[v]), 8, limit, used,
                         lambda z: any(a <= z < b for a, b in forbidden), rng)
    replace(v, row[1:-1])
    remove_fillers(iv, set(row[1:-1]))
    audit_ranges(list(labels.values()), [(a,b) for _,a,b in iv.blocks], iv.lo, iv.hi+1)
    edges = [labels[v]+labels[p] for v, p in enumerate(parents) if v]
    audit_ranges(edges, [(a+p,b+p) for p,a,b in iv.blocks], iv.lo+1, iv.hi+1)
    return moves, minor


def audit(anchors, kind, rng, *, endpoint=False):
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
    assert pairs
    needed = len(seeds)+(4 if kind == 'active' else 1)*len(pairs)
    while len(parents) < needed:
        x = max(blocked)+1
        labels[len(parents)] = x
        blocked.add(x)
        parents.append(seeds.index(0))
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
    gap = restore(parents, labels, blocked, jobs, -1, rng, endpoint_windows=[] if endpoint else None)
    for child, length in expected_paths.items():
        v = child
        for _ in range(length):
            v = parents[v]
            assert v >= len(core)
        assert parents[v] == core[child]

    if endpoint:
        return test_buffer(parents, labels, anchors, gap, rng)

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


    buffers = [audit(anchors, 'uniform', rng, endpoint=True) for _ in range(2)
               for anchors in ((0, 1), (-1, 0, 2), (-1, 0, 1, 2))]
    print(f"{len(buffers)} asymmetric marked endpoint replays, {sum(m for m, _ in buffers)} moves, "
          f"at most {max(c for _, c in buffers)} nonzero-parent buffer leaves.")


if __name__ == "__main__":
    main()

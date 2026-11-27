"""Verify interval witnesses and exhaustive coverage of all fork populations."""

from collections import Counter, defaultdict
from gzip import open as gzopen
from itertools import combinations, product
import json
from math import lcm, prod
from pathlib import Path

CERTIFICATE = Path(__file__).with_name("five-nonleaf.jsonl.gz")


def required_forks():
    result = set()
    for edges in combinations(combinations(range(5), 2), 4):
        degrees = sorted(sum(v in e for e in edges) for v in range(5))
        if degrees != [1, 1, 1, 2, 3]:
            continue
        reached = {0}
        for _ in range(4):
            for u, v in edges:
                if u in reached or v in reached:
                    reached.update([u, v])
        if len(reached) == 5:
            result.add(edges)
    return result


def seed_edges(edges, base, result):
    lo, f, parents, _ = result
    h = len(f)
    counts = [sum(base[i:])+int(sum(i in e for e in edges) == 1) for i in range(h)]
    hi = lo+h+sum(counts)-1
    assert len(set(f)) == h and set(f) <= set(range(lo, hi+1))
    slots = sorted(set(range(lo, hi+1))-set(f))
    assert len(parents) == len(slots)
    assert Counter(parents) == Counter({i: n for i, n in enumerate(counts) if n})
    actual = [(f[a], f[b]) for a, b in edges]
    actual.extend((f[p], x) for p, x in zip(parents, slots))
    assert sorted(u+v for u, v in actual) == list(range(lo+1, hi+1))
    return lo, hi, actual


def check_record(edges, base, steps, result):
    assert len(base) == len(steps) == len(result[1]) == len(edges)+1
    assert all(isinstance(n, int) and n >= 0 for n in (*base, *steps))
    lo, hi, actual = seed_edges(edges, base, result)
    _, f, _, bands = result
    assert len(bands) == sum(step > 0 for step in steps)
    chosen = list(base)
    blocks = iter(bands)
    for i, step in enumerate(steps):
        if not step:
            continue
        lower, upper = next(blocks)
        assert Counter(lower+upper) == Counter({p: step for p in f[:i+1]})
        assert sorted(j+p-1 for j, p in enumerate(lower)) == list(range(len(lower)))
        assert sorted(j+p for j, p in enumerate(upper)) == list(range(len(upper)))
        # Materialize a nontrivial representative, then recount actual endpoint sums.
        times = i%3+1
        chosen[i] += step*times
        for _ in range(times):
            actual.extend((p, lo-len(lower)+j) for j, p in enumerate(lower))
            actual.extend((p, hi+1+j) for j, p in enumerate(upper))
            lo -= len(lower)
            hi += len(upper)
    assert {x for e in actual for x in e} == set(range(lo, hi+1))
    assert sorted(u+v for u, v in actual) == list(range(lo+1, hi+1))
    leaf_parents = Counter(p for p, _ in actual[len(edges):])
    for i, p in enumerate(f):
        assert leaf_parents[p] == sum(chosen[i:])+int(sum(i in e for e in edges) == 1)


def check_coverage(cells):
    h = len(cells[0][0])
    limits = []
    for j in range(h):
        cutoff = 1+max(base[j] for base, _ in cells)
        period = lcm(1, *(steps[j] for _, steps in cells if steps[j]))
        limits.append(cutoff+period)
    covered = set()
    for base, steps in cells:
        axes = [range(b, end, d) if d else [b] for b, d, end in zip(base, steps, limits)]
        for profile in product(*axes):
            assert profile not in covered
            covered.add(profile)
    assert len(covered) == prod(limits)
    return len(covered)


def read(path):
    opener = gzopen if path.suffix == ".gz" else open
    with opener(path, "rt") as records:
        for line in records:
            yield json.loads(line)


def check(path):
    groups = defaultdict(list)
    rows, periodic, largest = 0, 0, 0
    for edges, base, steps, witness in read(path):
        edges = tuple(map(tuple, edges))
        check_record(edges, base, steps, witness)
        rows += 1
        periodic += max(steps) == 2
        largest = max(largest, len(witness[1])+len(witness[2]))
        groups[edges].append((base, steps))
    assert set(groups) == required_forks()
    grid = sum(check_coverage(cells) for cells in groups.values())
    print(f"{len(groups)} ranked forks, {rows} witnessed cells ({periodic} using a double layer), "
          f"largest seed order {largest}, {grid} finite coverage representatives.")


if __name__ == "__main__":
    import sys
    check(Path(sys.argv[1]) if len(sys.argv) == 2 else CERTIFICATE)

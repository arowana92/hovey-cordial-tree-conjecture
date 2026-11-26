"""Regenerate a four-branch seed table or a table of pairs of odd layers."""

import argparse
import json
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import permutations, product


def odd_pair(a, b):
    from ortools.sat.python import cp_model

    counts = Counter()
    for h in (a, b):
        counts.update(range(-h, 0))
        counts.update(range(1, h + 2))
    ranges = [(a + b + 2, 0), (a + b, 1)]
    model = cp_model.CpModel()
    columns = defaultdict(list)
    shifts = defaultdict(list)
    bands = []
    for size, first_target in ranges:
        band = []
        for x in range(1, size + 1):
            row = {}
            for p in counts:
                y = x - p
                if first_target <= y < first_target + size:
                    var = model.new_bool_var("")
                    row[p] = var
                    columns[first_target, y].append(var)
                    shifts[p].append(var)
            model.add_exactly_one(row.values())
            band.append(row)
        bands.append(band)
    for variables in columns.values():
        model.add_exactly_one(variables)
    for p, count in counts.items():
        model.add(sum(shifts[p]) == count)
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 4
    status = solver.solve(model)
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        raise ValueError(f"No witness for ranks {a}, {b}: {solver.status_name(status)}")
    return [[next(p for p, v in row.items() if solver.value(v)) for row in band] for band in bands]


def leaf_assignment(counts, parents, lo):
    span = set(range(lo, lo + 5 + sum(counts)))
    fixed = {0, *parents}
    missing = -sum(p * m for p, m in zip(parents, counts))
    if not fixed <= span or missing not in span or missing in parents:
        return None
    labels = sorted(span - fixed)
    targets = span - set(parents) - {missing}

    @lru_cache(maxsize=None)
    def choose(i, remaining, used):
        if i == len(labels):
            return ()
        for j, p in enumerate(parents):
            y = labels[i] + p
            if remaining[j] and y in targets and not used & (1 << (y - lo)):
                reduced = list(remaining)
                reduced[j] -= 1
                tail = choose(i + 1, tuple(reduced), used | (1 << (y - lo)))
                if tail is not None:
                    return (p,) + tail
        return None

    return choose(0, counts, 0)


def four_seed(e):
    counts = tuple(sum(e[i:]) for i in range(4))
    n = 5 + sum(counts)
    if max(e[2:]) >= 4:
        choices = [(1, -1, 3, -2)]
    else:
        choices = [(1, -1, a, b) for a, b in permutations((2, -2, 3, -3, 4, -4, 5, -5), 2)]
    for parents in choices:
        missing = -sum(p * m for p, m in zip(parents, counts))
        positions = (*parents, 0, missing)
        lower = [missing] if max(e) >= 4 else range(max(positions) - n + 1, min(positions) + 1)
        for lo in lower:
            result = leaf_assignment(counts, parents, lo)
            if result is not None:
                return [lo, parents, result]
    raise ValueError(f"No seed for {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("family", choices=("four", "pairs"))
    parser.add_argument("--rank", type=int, default=16)
    args = parser.parse_args()
    if args.family == "four":
        rows = ([e, four_seed(e)] for e in product(range(5), (0,), range(6), range(1, 6)))
    else:
        rows = ([a, b, odd_pair(a, b)] for b in range(2, args.rank + 1) for a in range(1, b))
    for row in rows:
        print(json.dumps(row, separators=(",", ":")), flush=True)

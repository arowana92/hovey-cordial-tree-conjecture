"""Optional CP-SAT discovery of the two integer seeds at a given even degree."""

import argparse
import json
from collections import Counter, defaultdict

from ortools.sat.python import cp_model

from .even_layers import parents


def search(c, extra, seconds):
    p = parents(c)
    required = Counter(p + extra*p[:5])
    lo = -sum(label * count for label, count in required.items())
    interval = set(range(lo, lo + 2*c + 5*extra + 1))
    vertices = sorted(interval - {0, *p})
    targets = interval - {lo, *p}
    model = cp_model.CpModel()
    rows = []
    weight_uses = defaultdict(list)
    parent_uses = defaultdict(list)
    for x in vertices:
        options = {}
        for label in required:
            if x + label in targets:
                chosen = model.new_bool_var("")
                options[label] = chosen
                weight_uses[x + label].append(chosen)
                parent_uses[label].append(chosen)
        model.add_exactly_one(options.values())
        rows.append(options)
    for y in targets:
        model.add_exactly_one(weight_uses[y])
    for label, count in required.items():
        model.add(sum(parent_uses[label]) == count)
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 3
    solver.parameters.max_time_in_seconds = seconds
    status = solver.solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return solver.status_name(status)
    return [next(label for label, v in row.items() if solver.value(v)) for row in rows]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("degree", type=int)
    parser.add_argument("--seconds", type=float, default=30)
    args = parser.parse_args()
    if args.degree < 6 or args.degree % 2:
        parser.error("the degree must be even and at least six")
    for extra in (0, 1):
        print(json.dumps([args.degree, extra, search(args.degree, extra, args.seconds)]))

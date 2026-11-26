"""Exact Presburger projections for a fixed core with leaves at vertex zero (islpy)."""

from collections import Counter
from itertools import combinations
import islpy as isl


def equalities(length):
    """Names for the classes of an equality pattern, in first-appearance order."""
    def grow(prefix, number):
        if len(prefix) == length:
            yield prefix
            return
        for c in range(number+1):
            yield from grow(prefix+(c,), max(number, c+1))
    yield from grow((0,), 1)


def inequalities(terms):
    return [f"{a} != {b}" for a, b in combinations(terms, 2)]


def projection(dimensions, variables, clauses):
    predicate = " and ".join(clauses) if clauses else "1 = 1"
    if variables:
        predicate = f"exists ({', '.join(variables)} : {predicate})"
    return isl.Set(f"{{ [{', '.join(dimensions)}] : {predicate} }}")


def capacity(v, e, qv, qe):
    return max(0, qv-v, qe-e), min(qv+1-v, qe+1-e)


def count_clauses(h, vertices, weights, classes):
    choices = []
    for qv in range(h):
        for qe in sorted({qv, max(0, qv-1)}):
            ordinary_lo, ordinary_hi = capacity(0, 0, qv, qe)
            limits = [capacity(vertices[c], weights[c], qv, qe) for c in range(classes)]
            if any(lo > hi for lo, hi in limits):
                continue
            minimum = sum(lo for lo, hi in limits)-classes*ordinary_lo
            maximum = sum(hi for lo, hi in limits)-classes*ordinary_hi
            clauses = [f"{qv}k <= m+{h} < {qv+1}k",
                       f"{qe}k <= m+{h-1} < {qe+1}k",
                       f"{ordinary_lo}k + ({minimum}) <= m <= {ordinary_hi}k + ({maximum})"]
            choices.append("("+" and ".join(clauses)+")")
    return "("+ " or ".join(choices)+")" if choices else None


def modular_holes(parents, pins=(), domain=None):
    """Failures in h+m <= (h-1)k. For ordinary labelings every point above works."""
    h = len(parents)
    wedge = isl.Set(f"{{ [k,m] : k >= 1 and m >= 0 and m+{h} <= {h-1}k }}")
    holes = wedge if domain is None else wedge.intersect(domain)
    internal = [i for i in range(1, h) if parents[i] != 0]
    for parts in equalities(h+len(internal)):
        classes = max(parts)+1
        names = ["0"]+[f"x{i}" for i in range(1, classes)]
        f = [names[c] for c in parts[:h]]
        weights = list(parts[1:h])
        clauses = [f"k >= {classes}"] + [f"0 < {x} < k" for x in names[1:]]
        clauses += inequalities(names[1:])
        clauses += [f"{f[i]} = {value}" for i, value in pins]
        for i, cls in zip(internal, parts[h:]):
            weights[i-1] = cls
            raw = f"({f[i]} + {f[parents[i]]})"
            clauses.append(f"({names[cls]} = {raw} or {names[cls]} + k = {raw})")
        bounds = count_clauses(h, Counter(parts[:h]), Counter(weights), classes)
        if bounds is None:
            continue
        success = projection(["k", "m"], names[1:], clauses+[bounds])
        holes = holes.subtract(success).coalesce()
        if holes.is_empty():
            break
    return holes


def interval_holes(parents, pins=()):
    """Leaf counts with no normalized consecutive-sums labeling. Pins use normalized integers."""
    h = len(parents)
    f = [f"x{i}" for i in range(h)]
    weights = [f"({f[i]}+{f[parents[i]]})" for i in range(1, h)]
    lo, hi = "L", f"(L+m+{h-1})"
    clauses = ["m >= 0"] + [f"{lo} <= {x} <= {hi}" for x in f]
    clauses += [f"{lo} < {y} <= {hi}" for y in weights]
    clauses += inequalities(f) + inequalities(weights)
    clauses += [f"{f[i]} = {v}" for i, v in pins]
    params = ["m", "L"]+f
    candidates = projection(params, [], clauses)
    target = " and ".join([f"{lo} < z <= {hi}"]+[f"z != {w}" for w in weights])
    source = " and ".join([f"{lo} <= z-x0 <= {hi}"]+[f"z-x0 != {x}" for x in f])
    differs = f"((({target}) and not ({source})) or (({source}) and not ({target})))"
    mismatch = projection(params, ["z"], [differs])
    success = candidates.subtract(mismatch).project_out(isl.dim_type.set, 1, h+1)
    return isl.Set("{ [m] : m >= 0 }").subtract(success).coalesce()

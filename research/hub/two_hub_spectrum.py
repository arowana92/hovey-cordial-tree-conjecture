"""Exact unit-difference leaf distributions on an order-k tree. Requires islpy."""

import argparse
from itertools import permutations

import islpy as isl


def domain(h):
    return isl.Set(f"{{ [k,t] : k >= {h} and 0 <= t <= k-{h} }}")


def pieces(parents, a, b):
    """Project each ordering of occupied labels and blocked edge slots onto (k,t)."""
    h = len(parents)
    edges = [(v, p) for v, p in enumerate(parents) if v]
    names = ["0", "1"] + [f"x{i}" for i in range(2, h)]
    upper = names[1:] + ["k"]
    others = sorted(set(range(h)) - {a, b})
    limits = [f"k >= {h}", f"0 <= t <= k-{h}"]
    limits.extend(f"{x} < {u}" for x, u in zip(names, upper))
    for tail in permutations(others):
        rank = {v: i for i, v in enumerate((a, b) + tail)}
        fixed = {}
        free_edges = []
        for v, p in edges:
            i, j = sorted((rank[v], rank[p]))
            if i == 0:
                gap, val = j-1, names[j]
            elif i == 1:
                gap, val = j, f"({names[j]} + 1)"
            else:
                free_edges.append((i, j))
                continue
            if gap in fixed:
                break
            fixed[gap] = val
        else:
            slots = sorted(set(range(h)) - fixed.keys())
            ys = [f"y{i}" for i in range(len(free_edges))]
            for gaps in permutations(slots):
                clauses = list(limits)
                for (i, j), g, y in zip(free_edges, gaps, ys):
                    raw = f"{names[i]} + {names[j]}"
                    clauses += [f"{names[g]} < {y} <= {upper[g]}",
                                f"({y} = {raw} or {y} + k = {raw})"]
                occupied = list(fixed.values()) + ys
                missing = "(k + " + " + ".join(names) + " - " + " - ".join(occupied) + " - t)"
                g = gaps[-1]
                clauses.append(f"{names[g]} < {missing} <= {upper[g]}")
                statement = " and ".join(clauses)
                variables = names[2:] + ys
                if variables:
                    statement = f"exists ({', '.join(variables)} : {statement})"
                yield isl.Set("{ [k,t] : " + statement + " }")


def excluded(parents, a, b):
    if (len(parents) < 2 or parents[0] != -1 or a == b
            or not 0 <= a < len(parents) or not 0 <= b < len(parents)
            or any(not 0 <= p < i for i, p in enumerate(parents) if i)):
        raise ValueError("expected distinct hubs and a parent-before-child tree")
    holes = domain(len(parents))
    for piece in pieces(parents, a, b):
        holes = holes.subtract(piece).coalesce()
        if holes.is_empty():
            break
    return holes


def exhaustive(parents, a, b, k):
    h = len(parents)
    available = list(range(2, k))
    vertices = [v for v in range(h) if v not in (a, b)]
    achieved = set()
    for t in range(k-h+1):
        # The new vertices come last, first the leaves at a, then those at b.
        full = tuple(parents) + (a,)*(k-h-t) + (b,)*t
        for values in permutations(available):
            labels = [0]*k
            labels[b] = 1
            for v, x in zip(vertices + list(range(h, k)), values):
                labels[v] = x
            weights = {(labels[v] + labels[p]) % k for v, p in enumerate(full) if v}
            if len(weights) == k-1:
                achieved.add(t)
                break
    return achieved


def check():
    from research.rainbow.verify import rooted_shapes

    instances = 0
    for h in range(2, 6):
        for parents in rooted_shapes(h).values():
            for b in range(1, h):
                holes = excluded(parents, 0, b)
                for k in range(h, 9):
                    valid = exhaustive(parents, 0, b, k)
                    for t in range(k-h+1):
                        point = isl.Set(f"{{ [k,t] : k={k} and t={t} }}")
                        assert holes.intersect(point).is_empty() == (t in valid)
                        instances += 1
    print(f"{instances} projected membership tests agree with direct full permutations.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--hubs", type=int, nargs=2, default=(0, 1))
    parser.add_argument("parents", type=int, nargs="*")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        print(excluded(args.parents, *args.hubs))

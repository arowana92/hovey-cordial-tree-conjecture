"""Search interval seeds and periodic leaf layers on a prescribed core."""

import argparse
import ctypes
import json
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path


def array(values):
    return (ctypes.c_int*len(values))(*values)


@lru_cache(None)
def single(rank):
    blocks = {}
    for width in range(rank+1):
        for pi in permutations(range(width)):
            lower = tuple(1+x-i for i, x in enumerate(pi))
            if len(set(lower)) != width:
                continue
            for rho in permutations(range(rank-width)):
                upper = tuple(x-i for i, x in enumerate(rho))
                if len(set(lower+upper)) == rank:
                    blocks.setdefault(tuple(sorted(lower+upper)), (lower, upper))
    return blocks


def repeated(parents, copies):
    size = len(parents)*copies
    below = copies*sum(parents)
    if not 0 <= below <= size:
        return None
    options = []
    for start, length, offset in ((0, below, 1), (below, size-below, 0)):
        for i in range(length):
            options.append([(p, start+i+p-offset) for p in parents if 0 <= i+p-offset < length])
    left = dict.fromkeys(parents, copies)
    ans = [0]*size

    def assign(rows, used):
        if not rows:
            return True
        choices = {i: [(p, y) for p, y in options[i] if y not in used and left[p]] for i in rows}
        i = min(sorted(rows), key=lambda j: len(choices[j]))
        for p, y in choices[i]:
            left[p] -= 1
            ans[i] = p
            if assign(rows-{i}, used | {y}):
                return True
            left[p] += 1
        return False

    if assign(set(range(size)), set()):
        return tuple(ans[:below]), tuple(ans[below:])
    return None


@lru_cache(None)
def catalog(rank, step):
    if step == 1:
        return single(rank)
    return {p: bands for p in combinations(range(-5, 7), rank)
            if (bands := repeated(p, step)) is not None}


@lru_cache(None)
def prefixes(steps):
    active = [(i+1, d) for i, d in enumerate(steps) if d]
    if not active:
        return 0, array([]), 1
    rank, step = active[-1]
    # Prune a failed prefix as soon as it is complete. Keeping the original
    # sorted-set and lexicographic permutation order preserves witness selection.
    constraints = {r: catalog(r, d) for r, d in active[:-1]}
    allowed = []

    def extend(prefix, remaining):
        r = len(prefix)
        if r in constraints and tuple(sorted(prefix)) not in constraints[r]:
            return
        if not remaining:
            allowed.extend(prefix)
            return
        for i, x in enumerate(remaining):
            extend(prefix+(x,), remaining[:i]+remaining[i+1:])

    for p in sorted(catalog(rank, step)):
        extend((), p)
    return rank, array(allowed), len(allowed)//rank


def seed(library, edges, base, steps):
    h = len(base)
    counts = [sum(base[i:])+int(sum(i in e for e in edges) == 1) for i in range(h)]
    n = h+sum(counts)
    rank, allowed, number = prefixes(tuple(steps))
    out = (ctypes.c_int*(1+h+n))()
    ok = library.solve(h, array([v for e in edges for v in e]), array(counts),
                       rank, allowed, number, out)
    if ok < 0:
        raise ValueError("seed outside the native search limits")
    if not ok:
        return None
    lo = out[0]
    f = tuple(out[1:1+h])
    parents = [out[1+h+i] for i in range(n) if lo+i not in f]
    bands = [catalog(r, d)[tuple(sorted(f[:r]))] for r, d in enumerate(steps, 1) if d]
    return [lo, f, parents, bands]


def extensions(base, steps, stage):
    if stage == 0:
        # Split each unbounded coordinate at its first value.
        for new in product(*([(0, 0), (d, d)] if d else [(0, 0)] for d in steps)):
            yield tuple(v+a for v, (a, _) in zip(base, new)), tuple(b for _, b in new)
    else:
        rank = {1: 3, 2: 5}[stage]-1
        if not steps[rank]:
            raise ValueError("no free coordinate for parity split")
        updated = list(steps)
        updated[rank] *= 2
        for extra in (0, steps[rank]):
            lower = list(base)
            lower[rank] += extra
            yield tuple(lower), tuple(updated)


def records(library, edges, base, steps, stage=0):
    result = seed(library, edges, base, steps)
    if result is not None:
        yield [edges, base, steps, result]
        return
    if stage >= 3:
        raise ValueError(f"search exhausted for {edges}, {base}, {steps}")
    for lower, updated in extensions(base, steps, stage):
        yield from records(library, edges, lower, updated, stage+1)


def fork_orders():
    edges = ((0, 1), (0, 2), (0, 3), (1, 4))
    return sorted({tuple(sorted(tuple(sorted((p[a], p[b]))) for a, b in edges))
                   for p in permutations(range(5))})


def load_native(path):
    library = ctypes.CDLL(str(Path(path).resolve()))
    pointer = ctypes.POINTER(ctypes.c_int)
    library.solve.argtypes = [ctypes.c_int, pointer, pointer, ctypes.c_int, pointer,
                              ctypes.c_int, pointer]
    return library


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("library")
    args = parser.parse_args()
    lib = load_native(args.library)
    for edges in fork_orders():
        for free in product((0, 1), repeat=5):
            for record in records(lib, edges, free, free):
                print(json.dumps(record, separators=(",", ":")))


if __name__ == "__main__":
    main()

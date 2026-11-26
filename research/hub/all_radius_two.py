"""Verify the finite and expanding interval labelings of all radius-two trees."""

import gzip
import json
from collections import Counter
from itertools import product
from pathlib import Path

from . import branch_levels, even_layers


HERE = Path(__file__).parent


def records(name):
    path = HERE / name
    raw = gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes()
    return [json.loads(line) for line in raw.splitlines()]


def check_band(parents, band):
    lower, upper = band
    copies, rem = divmod(len(lower) + len(upper), len(parents))
    assert copies >= 1 and rem == 0
    assert Counter(lower + upper) == Counter(list(parents) * copies)
    assert sorted(i-p for i, p in enumerate(lower, 1)) == list(range(len(lower)))
    assert sorted(i-p for i, p in enumerate(upper, 1)) == list(range(1, len(upper)+1))
    return copies


def layer_options(p, bands):
    assert len(set(p)) == len(p) == len(bands) and 0 not in p
    options = []
    for r, band in enumerate(bands, 1):
        copies = check_band(p[:r], band)
        if copies > 1:
            options.append((r, copies))
    return options


def required(p, options, residues):
    return list(p) + [v for (r, _), e in zip(options, residues) for _ in range(e) for v in p[:r]]


def residue_tuples(options):
    return product(*(range(copies) for _, copies in options))


def check_seed(p, requirements, shifts):
    assert Counter(shifts) == Counter(requirements)
    lo = -sum(requirements)
    hi = lo + len(p) + len(shifts)
    vertices = set(range(lo, hi+1))
    assert {0, *p} <= vertices
    rows = sorted(vertices - {0, *p})
    assert len(rows) == len(shifts)
    edges = list(zip(rows, shifts))
    weights = p + [x+v for x, v in edges]
    assert sorted(weights) == list(range(lo+1, hi+1))
    return lo, hi, edges


def check_finite(p, bands, seeds):
    options = layer_options(p, bands)
    residues = list(residue_tuples(options))
    assert len(residues) == len(seeds)
    for e, seed in zip(residues, seeds):
        check_seed(p, required(p, options, e), seed)


def check_four():
    repairs = {}
    for e, data in records("four-consecutive.jsonl"):
        assert tuple(e) not in repairs
        repairs[tuple(e)] = data
    needed = {e for e, (lo, _, shifts) in branch_levels.FOUR.items() if lo != -sum(shifts)}
    assert set(repairs) == needed
    count = 0
    for e, (lo, p, seed) in branch_levels.FOUR.items():
        if e not in needed:
            shifts = [v for i, n in enumerate(e, 1) for _ in range(n) for v in p[:i]]
            assert check_seed(p, shifts, seed)[0] == lo
            continue
        assert e[1] == 0 and max(e) < 4
        band, variants = repairs[e]
        for rem, (p, seed) in enumerate(variants):
            assert len(p) == len(set(p)) == 4 and 0 not in p
            assert check_band(p[:2], band) == len(variants)
            profile = [e[0], rem, *e[2:]]
            shifts = [v for i, n in enumerate(profile, 1) for _ in range(n) for v in p[:i]]
            check_seed(p, shifts, seed)
            count += 1
    return count


def slope(x, cutoff, center):
    relative = x - (center if x % 2 else 0)
    return int(relative >= cutoff) - int(relative <= -cutoff)


def extend_parents(p, size):
    skip = len(p) % 2
    out = p[:]
    for r in range(len(p), size):
        length = r-skip
        out.append(-length if length % 2 == 0 else length+1)
    return out


def check_suffix(p, sigma):
    active = p[len(p) % 2:]
    assert p[0] == 1 and sorted(sigma) == list(range(len(active)))
    assert sorted(1 + y-i for i, y in enumerate(sigma)) == sorted(active)
    # The lower permutation can be extended at any rank by the two formulas.
    out = active[:]
    for _ in range(12):
        n = len(sigma)
        if n % 2 == 0:
            sigma = [y+1 for y in sigma] + [0]
            out.append(-n)
            offset = 0
        else:
            sigma = [n] + sigma
            out.append(n+1)
            offset = 1
        assert sorted(sigma) == list(range(n+1))
        assert sorted(offset + y-i for i, y in enumerate(sigma)) == sorted(out)


def minimal_shell(d):
    # At the endpoint m=2d-1 the signed Langford permutation is elementary.
    m = 2*d-1
    start = d+m
    pi = {}
    for i in range(m):
        x, y = start+i, start+m+(2*i) % m
        pi[x], pi[y] = y, x
    tau = {}
    for x, y in pi.items():
        u, v, w = x, -y, y-x
        assert len({u, v, w}) == 3
        tau[u], tau[v], tau[w] = -v, -w, -u
    shell = {sign*x for x in range(d, d+3*m) for sign in (-1, 1)}
    assert set(tau) == set(tau.values()) == {y-x for x, y in tau.items()} == shell
    return tau


def check_frame(p, bands, sigma, witnesses):
    options = layer_options(p, bands)
    residues = list(residue_tuples(options))
    assert [tuple(e) for e, _, _, _ in witnesses] == residues
    check_suffix(p, sigma)
    c = len(p)
    extent = c - c % 2
    for e, cutoff, center, seed in witnesses:
        assert cutoff >= 2 and cutoff % 2 == 0 and center % 2 == 1
        speed = lambda x: slope(x, cutoff, center)
        assert all(speed(x) == 0 for x in p if x % 2)
        assert all(speed(x) == 0 for r, _ in options for x in p[:r])
        assert {x for x in p if x >= cutoff and x % 2 == 0} == set(range(cutoff, extent+1, 2))
        assert {-x for x in p if x <= -cutoff and x % 2 == 0} == set(range(cutoff, extent-1, 2))
        assert cutoff <= extent
        lo, hi, edges = check_seed(p, required(p, options, e), seed)
        for offset in (0, center):
            assert lo+1 <= offset-cutoff+2 <= offset+cutoff-2 <= hi
        assert all(speed(x)+speed(v) == speed(x+v) for x, v in edges)

        # Reconstruct a complete larger seed at the first Langford order.
        tau = minimal_shell(cutoff//2)
        delta = len(tau)
        moved = lambda x: x + delta*speed(x)
        larger = extend_parents(p, c+delta)
        additions = [(center+2*x, 2*(y-x)) for x, y in tau.items()]
        enlarged = [(moved(x), moved(v)) for x, v in edges] + additions
        assert {moved(v) for v in p} | {v for _, v in additions} == set(larger)
        assert sorted([0, *larger, *(x for x, _ in enlarged)]) == list(range(lo-delta, hi+delta+1))
        assert sorted(larger + [x+v for x, v in enlarged]) == list(range(lo-delta+1, hi+delta+1))
        assert Counter(v for _, v in enlarged) == Counter(required(larger, options, e))
    return c + 6*(max(cutoff for _, cutoff, _, _ in witnesses)-1)


def verify():
    branch_levels.verify_data()
    four = check_four()
    even_layers.check_bands()
    even_seeds = even_layers.load_seeds()
    for (c, extra), shifts in even_seeds.items():
        p = even_layers.parents(c)
        check_seed(p, p + extra*p[:5], shifts)

    thresholds = {}
    frames = records("radius-two-frames.jsonl")
    for p, bands, sigma, witnesses in frames:
        residue = len(p) % 6
        assert residue not in thresholds
        thresholds[residue] = check_frame(p, bands, sigma, witnesses)
    assert set(thresholds) == set(range(6))
    direct = set()
    finite = records("radius-two-finite.jsonl.gz")
    for p, bands, seeds in finite:
        assert len(p) not in direct
        direct.add(len(p))
        check_finite(p, bands, seeds)
    needed = {c for c in range(3, max(thresholds.values())) if c < thresholds[c % 6]}
    assert direct.isdisjoint({4, *even_layers.DEGREES})
    assert direct | {4, *even_layers.DEGREES} == needed
    print("First degrees covered by expansion in residues 0 through 5:", [thresholds[i] for i in range(6)])
    print(f"Verified {len(finite)} direct branch counts, {len(even_layers.DEGREES)} earlier even counts, "
          f"{four} replacement four-branch seeds, and {sum(len(w[-1]) for w in frames)} expanding seeds.")


if __name__ == "__main__":
    verify()

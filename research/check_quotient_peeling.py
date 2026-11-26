"""Construct leaf-by-leaf lifts and verify the complete tree histograms."""

from collections import Counter
from functools import lru_cache
from itertools import combinations
from math import gcd
from random import Random

from research.check_odd_quotient import low_slots, make_system, piece, whole_tree
from research.rainbow.generate import rainbow
from research.rainbow.verify import rooted_shapes


@lru_cache(None)
def cutoff(g):
    sizes = Counter(gcd(i, g) for i in range(g))
    totals = {0}
    for size in sizes.values():
        totals |= {n+size for n in totals}
    return max(min(v, g-v) for v in totals)


def restore_order(mid, q):
    neighbors = [set() for _ in range(q)]
    for i, j in mid.values():
        neighbors[i].add(j)
        neighbors[j].add(i)
    active, rows, removed = set(range(q)), set(mid), []
    while active:
        v = min(i for i in active if len(neighbors[i] & active) <= 1)
        rows_here = sorted(c for c in rows if c == v or v in mid[c])
        assert len(rows_here) <= 2
        assert sum(c != v for c in rows_here) <= 1
        removed.append((v, rows_here))
        rows.difference_update(rows_here)
        active.remove(v)
    return removed[::-1]


def restore(mid, order, ports, slots, m, g):
    q = len(order)
    units, trans = [None]*q, [None]*q
    chosen = {}
    for v, rows in order:
        h, k, endpoint_row = None, None, None
        for c in rows:
            i, j = mid[c]
            a, b = ports[c]
            eta = (i+j-2*c)//q
            if v == c:
                h = eta + trans[i]+units[i]*a + trans[j]+units[j]*b
            else:
                endpoint_row = c
                port, other, value = (a, j, b) if v == i else (b, i, a)
                k = 2*trans[c]-eta-trans[other]-units[other]*value
        scale = 1
        if h is not None and k is not None:
            left = {gcd(w-2*port, g): w for w in slots[v]}
            for w in slots[endpoint_row]:
                target = h-2*(k+units[endpoint_row]*w)
                if gcd(target, g) in left:
                    break
            else:
                return None
            chosen[endpoint_row] = w
            chosen[v] = left[gcd(target, g)]
            scale = next(u for u in range(1, g+1) if gcd(u, g) == 1 and
                         (u*(chosen[v]-2*port)-target) % g == 0)
        elif rows:
            chosen[rows[0]] = slots[rows[0]][0]
        if k is not None:
            shift = k+units[endpoint_row]*chosen[endpoint_row]-scale*port
        elif h is not None:
            shift = (h-scale*chosen[v])*pow(2, -1, g) if g > 1 else 0
        else:
            shift = 0
        units[v] = next(u for u in range(1, m+1)
                        if gcd(u, m) == 1 and (u-scale) % g == 0)
        trans[v] = shift % g
    return units, trans, chosen


def lift(system, order, pieces, m, rng):
    mid, root, keys, d, adj = system
    q = len(pieces)
    factor = gcd(d, *(a for row in adj for a in row))
    exponent = d//factor
    g = gcd(exponent, m)
    links, ports = [], {}
    for c in keys:
        i, j = mid[c]
        u, v = rng.randrange(len(pieces[i][0])), rng.randrange(len(pieces[j][0]))
        links.append((i, u, j, v))
        ports[c] = (pieces[i][0][u], pieces[j][0][v])
    slots = {c: low_slots(pieces[c], m) for c in keys}
    answer = restore(mid, order, ports, slots, m, g)
    if answer is None:
        assert any(len(ws)*g <= m*cutoff(g) for ws in slots.values())
        return False
    units, trans, selected = answer
    trans = [t-trans[root] for t in trans]
    error = []
    for c in keys:
        i, j = mid[c]
        a, b = ports[c]
        target = (i+j-2*c)//q + trans[i]+units[i]*a + trans[j]+units[j]*b
        v = (target-2*trans[c]-units[c]*selected[c]) % m
        assert v % g == 0
        error.append(v)
    n = m//g
    z = [v//g*pow(exponent//g, -1, n) % n for v in error] if n > 1 else [0]*len(keys)
    for c, row in zip(keys, adj):
        trans[c] += sum((a//factor)*b for a, b in zip(row, z))
    assert whole_tree(pieces, links, range(q), units, trans, m)
    return True


def check_local():
    count = 0
    for g in [3, 5, 7, 9, 15]:
        # For each first set, grow its full unit orbit by actual multiplication.
        # Its complement is the largest possible incompatible second set.
        best = 0
        units = [u for u in range(g) if gcd(u, g) == 1]
        orbit = [{u*w % g for u in units} for w in range(g)]
        for n in range(g+1):
            for subset in combinations(range(g), n):
                covered = set().union(*(orbit[w] for w in subset))
                best = max(best, min(n, g-len(covered)))
                count += 1
        assert cutoff(g) == best
    return count


def main():
    rng = Random(1991)
    checked, moduli, exponents = Counter(), set(), set()
    for q in [3, 5, 7]:
        for parents in rooted_shapes(q).values():
            labels = [0]+rainbow(tuple(p-1 for p in parents[1:]), q)
            edges = [(labels[i], labels[p]) for i, p in enumerate(parents) if i]
            system = make_system(edges, q)
            mid, _, _, d, adj = system
            order = restore_order(mid, q)
            e = d//gcd(d, *(v for row in adj for v in row))
            exponents.add((d, e))
            for m in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 21, 25, 35, 49]:
                g = gcd(m, e)
                moduli.add(g)
                for s in sorted({1, m, m+1, max(1, m-1), 2*m-max(1, m*cutoff(g)//g),
                                 max(1, 2*m-m*cutoff(g)//g-1)}):
                    parts = [piece(s, m, rng.getrandbits(1), rng) for _ in range(q)]
                    checked[lift(system, order, parts, m, rng)] += 1
    print("Complete reconstructed trees:", checked[True])
    print("Greedy failures outside the bound:", checked[False])
    print("Shared moduli:", sorted(moduli), "determinant/exponent pairs:", sorted(exponents))
    print("Arbitrary subset orbit checks:", check_local())


if __name__ == "__main__":
    main()

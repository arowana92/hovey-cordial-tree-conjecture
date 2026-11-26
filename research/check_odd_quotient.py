"""Exact arithmetic and independent histogram checks for the odd quotient lift."""

from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd
from random import Random

from research.rainbow.generate import rainbow
from research.rainbow.verify import rooted_shapes


def det(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    value = 1
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            value = -value
        value *= a[j][j]
        for i in range(j + 1, len(a)):
            ratio = a[i][j] / a[j][j]
            for k in range(j + 1, len(a)):
                a[i][k] -= ratio * a[j][k]
    assert int(value) == value
    return int(value)


def adjugate(a):
    return [[(-1)**(i+j) * det([row[:i] + row[i+1:]
                                 for k, row in enumerate(a) if k != j])
             for j in range(len(a))] for i in range(len(a))]


def make_system(edges, q):
    mid = {(i+j)*pow(2, -1, q) % q: (i, j) for i, j in edges}
    assert len(mid) == q - 1
    root, = set(range(q)) - mid.keys()
    keys = sorted(mid)
    a = [[2 * (c == j) - (j in mid[c]) for j in keys] for c in keys]
    d = det(a)
    count = 0
    for choices in product(range(2), repeat=q-1):
        succ = {c: mid[c][bit] for c, bit in zip(keys, choices)}
        for c in keys:
            for _ in range(q-1):
                if c == root:
                    break
                c = succ[c]
            if c != root:
                break
        else:
            count += 1
    assert count == d and d > 0 and d % q == 0
    return mid, root, keys, d, adjugate(a)


def piece(n, m, star, rng):
    if star:
        edges = [(0, i) for i in range(1, n)]
        labels = list(range(n))
    else:
        edges = [(i-1, i) for i in range(1, n)]
        labels = [i//2 + (n+1)//2 * (i % 2) for i in range(n)]
    sign, shift = rng.choice([-1, 1]), rng.randrange(m)
    return [(sign*x + shift) % m for x in labels], edges


def histogram(values, modulus):
    counts = [0] * modulus
    for x in values:
        counts[x % modulus] += 1
    return counts


def balanced(counts):
    return max(counts) - min(counts) <= 1


def low_slots(p, m):
    labels, edges = p
    counts = histogram((labels[i]+labels[j] for i, j in edges), m)
    assert balanced(counts) and balanced(histogram(labels, m))
    return [u for u in range(m) if counts[u] == min(counts)]


def whole_tree(pieces, links, cosets, signs, shifts, m):
    q = len(pieces)
    lifted = [[cosets[c] + q*((signs[c]*x + shifts[c]) % m) for x in lab]
              for c, (lab, _) in enumerate(pieces)]
    weights = [lifted[c][u]+lifted[c][v] for c, (_, edges) in enumerate(pieces)
               for u, v in edges]
    weights.extend(lifted[i][u]+lifted[j][v] for i, u, j, v in links)
    labels = [x for part in lifted for x in part]
    assert len(weights) == len(labels)-1
    return balanced(histogram(labels, q*m)) and balanced(histogram(weights, q*m))


def construct(system, pieces, m, rng):
    mid, root, keys, d, adj = system
    g = gcd(d, m)
    links, rhs = [], []
    for c in keys:
        i, j = mid[c]
        u, v = rng.randrange(len(pieces[i][0])), rng.randrange(len(pieces[j][0]))
        links.append((i, u, j, v))
        carry = (i+j-2*c)//len(pieces)
        target = carry + pieces[i][0][u] + pieces[j][0][v]
        lows = [w for w in low_slots(pieces[c], m) if (target-w) % g == 0]
        if not lows:
            return False
        rhs.append((target-rng.choice(lows)) % m)
    n = m//g
    z = [b//g * pow(d//g, -1, n) % n for b in rhs] if n > 1 else [0]*len(keys)
    shifts = [0] * len(pieces)
    for c, row in zip(keys, adj):
        shifts[c] = sum(x*y for x, y in zip(row, z)) % m
    assert shifts[root] == 0
    assert whole_tree(pieces, links, range(len(pieces)), [1]*len(pieces), shifts, m)
    return True


def check_three(pieces, ports, m):
    a, b, c = (p[0] for p in pieces)
    u, v, i, j = ports
    links = [(0, u, 1, i), (0, v, 2, j)]
    lows_b, lows_c = (low_slots(p, m) for p in pieces[1:])
    predicted = (a[u]-a[v]) % 3 != 0 or any((b[i]+w) % 3 for w in lows_b) or any(
        (c[j]+w) % 3 for w in lows_c)
    actual = any(whole_tree(pieces, links, cosets, signs, (0, x, y), m)
                 for cosets in [(0, 1, 2), (0, 2, 1)]
                 for signs in product([-1, 1], repeat=3)
                 for x, y in product(range(m), repeat=2))
    assert bool(predicted) == actual
    return actual


def main():
    rng = Random(1991)
    determinants, lifts = Counter(), Counter()
    for q in [3, 5, 7]:
        for parents in rooted_shapes(q).values():
            labels = [0] + rainbow(tuple(p-1 for p in parents[1:]), q)
            edges = [(labels[i], labels[p]) for i, p in enumerate(parents) if i]
            system = make_system(edges, q)
            _, root, keys, d, _ = system
            determinants[q, d] += 1
            for m in range(1, 13):
                for s in sorted({1, m, m+1, 2*m-1, 2*m+2}):
                    for unequal in [False, True]:
                        # Keep vertex totals and completed edge totals inside one block.
                        sizes = [s] * q
                        if unequal:
                            if s % m == 0:
                                sizes[root] += 1
                            else:
                                sizes[rng.choice(keys)] += 1
                        pieces = [piece(n, m, rng.getrandbits(1), rng) for n in sizes]
                        good = construct(system, pieces, m, rng)
                        guaranteed = all((sizes[c]-1) % m < m//gcd(d, m) for c in keys)
                        assert not guaranteed or good
                        if good:
                            lifts[unequal] += 1
    triples = Counter()
    for m in [3, 6, 9]:
        for s in [m, m+1, 2*m-1]:
            for stars in product([False, True], repeat=3):
                pieces = [piece(s, m, star, rng) for star in stars]
                for ports in [(0, 0, 0, 0), tuple(rng.randrange(s) for _ in range(4))]:
                    result = check_three(pieces, ports, m)
                    if s == m and all(stars) and ports == (0, 0, 0, 0):
                        assert not result
                    triples[result] += 1
    print("Quotients and determinant multiplicities:", sorted(determinants.items()))
    print("Full histogram checks (equal, variable sizes):", lifts[False], lifts[True])
    print("Three-piece exhaustive checks (feasible, obstructed):", triples[True], triples[False])


if __name__ == "__main__":
    main()

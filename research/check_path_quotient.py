"""Verify the path difference construction against whole-tree histograms."""

from collections import Counter
from itertools import product
from math import gcd
from random import Random

from research.check_odd_quotient import low_slots, piece, whole_tree


def prime_factors(n):
    primes = []
    p = 2
    while p*p <= n:
        if n % p == 0:
            primes.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        primes.append(n)
    return primes


def solve(pieces, links, m):
    q = len(pieces)
    r, g = (q-1)//2, gcd(q, m)
    ports = [0]*q
    for i, u, j, v in links:
        ports[i] += j * pieces[i][0][u]
        ports[j] += j * pieces[j][0][v]
    # Retain one slot selection per achievable gcd.
    states = {g: ()}
    for i, part in enumerate(pieces):
        options = [0] if i == r else low_slots(part, m)
        next_states = {}
        for old, prefix in states.items():
            for w in options:
                nxt = gcd(old, ports[i]-(i-r)*w)
                next_states.setdefault(nxt, prefix + (w,))
        states = next_states
    if 1 not in states:
        return False
    slots = states[1]
    b = [ports[i]-(i-r)*slots[i] for i in range(q)]
    primes = prime_factors(g)
    units = [u for u in range(m) if gcd(u, m) == 1]
    negated = {}
    for p in primes:
        if sum(b) % p == 0:
            negated[p] = next(i for i in range(q) if b[i] % p)
    multipliers = [next(u for u in units if all(
        (u - (-1 if negated.get(p) == i else 1)) % p == 0 for p in primes))
        for i in range(q)]
    total = sum(u*x for u, x in zip(multipliers, b))
    scale = next(u for u in units if (u*total + r*r) % g == 0)
    multipliers = [u*scale % m for u in multipliers]

    rhs = [0]*q
    d = (q+1)//2
    for i, u, j, v in links:
        c = (i+d) % q
        rhs[c] = ((i+j-2*c)//q + multipliers[i]*pieces[i][0][u]
                  + multipliers[j]*pieces[j][0][v] - multipliers[c]*slots[c]) % m
    cyclic = [(r+j*d) % q for j in range(q)]
    target = sum((q-j)*rhs[cyclic[j]] for j in range(1, q))
    diff = next(x for x in range(m) if (q*x-target) % m == 0)
    shifts = [0]*q
    for j in range(1, q):
        c = cyclic[j]
        shifts[c] = (shifts[cyclic[j-1]] + diff) % m
        diff -= rhs[c]
    assert (shifts[cyclic[-1]]+diff) % m == 0
    assert whole_tree(pieces, links, range(q), multipliers, shifts, m)
    return True


def exhaustive(pieces, links, m):
    q = len(pieces)
    options = []
    for i, (lab, edges) in enumerate(pieces):
        # Two transformations with the same vertex/weight multisets and
        # attachment labels are interchangeable for the direct histogram test.
        choices = {}
        ports = ([links[i-1][3]] if i else []) + ([links[i][1]] if i < q-1 else [])
        for u in range(m):
            if gcd(u, m) != 1:
                continue
            # A common high shift translates every full labeling.
            for t in ([0] if i == (q-1)//2 else range(m)):
                values = [(u*x+t) % m for x in lab]
                key = (tuple(sorted(values)), tuple(sorted((values[a]+values[b]) % m
                                                           for a, b in edges)),
                       tuple(values[v] for v in ports))
                choices[key] = (u, t)
        options.append(list(choices.values()))
    for choices in product(*options):
        units, shifts = zip(*choices)
        if whole_tree(pieces, links, range(q), units, shifts, m):
            return True
    return False


def main():
    rng = Random(1991)
    results, small = Counter(), Counter()
    for q in [3, 5, 7, 9, 15, 21, 25, 45]:
        for m in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 16, 21, 25, 27, 30, 45]:
            g = gcd(q, m)
            for s in sorted({1, max(1, m//2), m-1, m, m+1, 2*m-1, 2*m+2} - {0}):
                for case in ['mixed', 'centers', 'end leaf']:
                    parts = [piece(s, m, case != 'mixed' or rng.getrandbits(1), rng)
                             for _ in range(q)]
                    links = [(i, rng.randrange(s), i+1, rng.randrange(s))
                             if case == 'mixed' else (i, int(case == 'end leaf' and
                                                            i == 0 and s > 1), i+1, 0)
                             for i in range(q-1)]
                    actual = solve(parts, links, m)
                    if g == 1 or m-(s-1) % m > m//min(prime_factors(g)):
                        assert actual
                    if s == m and case == 'centers':
                        assert actual == (g == 1)
                    if s == m and case == 'end leaf':
                        assert actual
                    results[actual] += 1
                    if (q == 3 and m in [3, 6]) or (q == m == 5 and s in [m, m+1]):
                        assert exhaustive(parts, links, m) == actual
                        small[actual] += 1
    print("Path instances (lifted, obstructed):", results[True], results[False])
    print("Independent exhaustive checks (lifted, obstructed):", small[True], small[False])


if __name__ == "__main__":
    main()

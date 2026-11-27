"""Check the parity specialization and direct leaf assignments at twice prime powers."""

from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from math import comb, factorial, gcd, prod
from random import Random

from .check_leaf_lists import choose
from .check_spare_lists import balanced, verify_choice


def exponents(r, pair):
    for row in permutations(range(r)):
        if pair is None or row[pair[0]] == row[pair[1]] + 1:
            yield row


def mobius(n):
    value = 1
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            n //= factor
            if n % factor == 0:
                return 0
            value = -value
        factor += 1
    return value if n == 1 else -value


@lru_cache(None)
def ramanujan(k, divisor):
    # Sum of exp(2 pi i a j/k) over all units a, with gcd(j,k) = divisor.
    return sum(d * mobius(k // d) for d in range(1, divisor + 1) if divisor % d == 0)


def verify_coefficient(k, p, shifts, pair):
    r = len(shifts)
    counts = Counter(sum(a * b for a, b in zip(shifts, row)) % k for row in exponents(r, pair))
    projected = sum((-1) ** e * value for e, value in counts.items())
    v = sum(x % 2 for x in shifts)
    if pair is None:
        formula = factorial(v) * factorial(r - v) * comb(r // 2, v // 2)
    else:
        formula = factorial(v - 1) * factorial(r - v - 1) * comb(r // 2 - 1, (v - 1) // 2)
    assert abs(projected) == formula and formula % p != 0
    # This is the trace of the squared absolute value at the actual modulus.
    trace = sum(a * b * ramanujan(k, gcd(i - j, k))
                for i, a in counts.items() for j, b in counts.items())
    assert trace > 0


def check_grid():
    """Recover the actual two-Vandermonde coefficient by finite differences."""
    p = 13
    cases = 0
    for r in range(1, 6):
        for v in range(r + 1):
            mixed = r % 2 == 0 and v % 2 == 1
            powers = [r-1] * r
            if mixed:
                powers[0] += 1
                powers[v] -= 1
            total = 0
            for xs in product(*(range(h+1) for h in powers)):
                ys = tuple(-x if i < v else x for i,x in enumerate(xs))
                if len(set(xs)) < r or len(set(ys)) < r:
                    continue
                vertex = prod(y-x for x,y in combinations(xs,2))
                edge = prod(y-x for x,y in combinations(ys,2))
                weight = prod((-1)**(h-x)*comb(h,x) for h,x in zip(powers,xs))
                total += vertex * edge * weight
            coeff = total * pow(prod(factorial(h) for h in powers), -1, p) % p
            pair = (0,v) if mixed else None
            projected = sum((-1)**sum(e[:v]) for e in exponents(r,pair))
            assert coeff == ((-1)**(r*(r-1)//2 + mixed) * projected) % p != 0
            cases += 1
    return cases


def check_lists():
    rng = Random(2691)
    cases = counterexamples = 0
    for k, p, limit in ((6,3,2), (18,3,2), (10,5,4), (50,5,4), (14,7,6),
                        (98,7,6), (22,11,7), (26,13,7), (338,13,6), (1778,7,5)):
        for r in range(1, limit + 1):
            for v in range(r + 1):
                shifts = [2*rng.randrange(k // 2) + (i < v) for i in range(r)]
                if r % 2 == 0 and v % 2 == 1:
                    pairs = [(0, v), (v, 0)]
                else:
                    pairs = [None]
                for pair in pairs:
                    verify_coefficient(k, p, shifts, pair)
                    sizes = [r] * r
                    if pair:
                        sizes[pair[0]] += 1
                        sizes[pair[1]] -= 1
                    lists = [rng.sample(range(k), size) for size in sizes]
                    verify_choice(k, shifts, lists)
                    cases += 1
                if r % 2 == 0 and v % 2 == 1:
                    half = k // 2
                    common = tuple(i+j for i in range(r // 2) for j in (0, half))
                    assert choose(k, [half] * v + [0] * (r-v), [common] * r) is None
                    counterexamples += 1
    return cases, counterexamples


def check_trees():
    rng = Random(52026)
    cases = 0
    for k, p in ((14,7), (22,11), (26,13), (38,19), (98,7), (338,13)):
        for r in range(3, min(12, p), 2):
            s = (k + r + 1) // 2
            for periods in range(3):
                h = k * periods + s - r
                labels = [(i//2 + (i%2)*((h+1)//2)) % k for i in range(h)]
                edges = [(i-1, i, 0) for i in range(1, h)]
                high_vertices = {x for x, n in Counter(labels).items() if n > periods}
                weights = [(labels[i]+labels[j]+b) % k for i, j, b in edges]
                high_weights = {x for x, n in Counter(weights).items() if n > periods}
                assert len(high_vertices) == s-r and len(high_weights) == s-r-1
                parents = [0,h-1] + [rng.randrange(h) for _ in range(r-2)]
                offsets = [rng.randrange(k) if periods == 2 else 0 for _ in parents]
                shifts = [(labels[parent]+b) % k for parent, b in zip(parents, offsets)]
                lists = [[x for x in range(k) if x not in high_vertices and (x+b)%k not in high_weights]
                         for b in shifts]
                assert min(map(len, lists)) >= r
                labels.extend(verify_choice(k, shifts, [rng.sample(row,r) for row in lists]))
                edges.extend((parent,h+i,offsets[i]) for i,parent in enumerate(parents))
                assert balanced(labels,k)
                assert balanced([labels[i]+labels[j]+b for i,j,b in edges],k)
                cases += 1
    return cases


if __name__ == "__main__":
    cases, bad = check_lists()
    print(f"{cases} exact coefficients and separate-list witnesses, {bad} sharp parity obstructions")
    print(f"{check_grid()} independent two-Vandermonde grid evaluations")
    print(f"{check_trees()} whole-tree extensions at the excluded boundary")

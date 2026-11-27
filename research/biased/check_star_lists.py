"""Verify the exact coefficient by polynomial multiplication and check actual lists."""

from fractions import Fraction
from itertools import combinations
from random import Random

from research.biased.forest_grid import forest_coefficient
from research.biased.star_lists import grid_coefficient, reduced_coefficients, terminal_exceptions


def multiply(poly, linear, cap):
    result = {}
    for exponent, coeff in poly.items():
        for i, a in enumerate(linear):
            if a and exponent[i] < cap:
                key = exponent[:i] + (exponent[i]+1,) + exponent[i+1:]
                result[key] = result.get(key, 0) + a*coeff
    return {key: value for key, value in result.items() if value}


def polynomial_coefficient(parents, e):
    r = len(parents)
    x = [[int(i == v) for i in range(r)] for v in range(r)]
    y = [row.copy() for row in x]
    for v, p in enumerate(parents):
        if p >= 0:
            y[v][p] += 1
    poly = {(0,)*r: 1}
    cap = r+e-1
    for row in y:
        for _ in range(e):
            poly = multiply(poly, row, cap)
    for matrix in (x, y):
        for a, b in combinations(matrix, 2):
            poly = multiply(poly, [v-u for u, v in zip(a, b)], cap)
    return poly.get((cap,)*r, 0)


def direct(r, j, e):
    return polynomial_coefficient([-1] + [0]*j + [-1]*(r-j-1), e)


def find_witness(p, j, shifts, lists, forbidden):
    r = len(lists)
    labels = []
    used = set()

    def search(i):
        if i == r:
            return True
        for x in lists[i]:
            y = (x+shifts[i]+(labels[0] if 0 < i <= j else 0)) % p
            if x in labels or y in forbidden or y in used:
                continue
            labels.append(x)
            used.add(y)
            if search(i+1):
                return True
            used.remove(y)
            labels.pop()
        return False

    if not search(0):
        return None
    weights = [(x+shifts[i]+(labels[0] if 0 < i <= j else 0)) % p for i, x in enumerate(labels)]
    assert len(set(labels)) == len(set(weights)) == r and not forbidden.intersection(weights)
    assert all(x in allowed for x, allowed in zip(labels, lists))
    return labels


if __name__ == "__main__":
    comparisons = 0
    for r, highest_e in [(1, 6), (2, 6), (3, 6), (4, 5), (5, 3), (6, 1)]:
        for e in range(highest_e+1):
            for j in range(r):
                assert direct(r, j, e) == grid_coefficient(r, j, e), (r, j, e)
                comparisons += 1
    print(f"{comparisons} exact coefficients checked by direct polynomial multiplication", flush=True)

    rng = Random(20261127)
    cases = 0
    for p in (2, 3, 5, 7, 11, 13, 17):
        for r in range(1, min(8, p)+1):
            for e in range(p-r+1):
                for j, a in enumerate(reduced_coefficients(r, e)):
                    if a % p:
                        for _ in range(2):
                            lists = [rng.sample(range(p), r+e) for _ in range(r)]
                            shifts = [rng.randrange(p) for _ in range(r)]
                            forbidden = set(rng.sample(range(p), e))
                            assert find_witness(p, j, shifts, lists, forbidden) is not None
                            cases += 1
    print(f"{cases} independent-list and forbidden-weight examples checked by direct search")

    primes = [p for p in range(3, 128) if all(p % d for d in range(2, int(p**0.5)+1))]
    for p in primes:
        for j, a in enumerate(reduced_coefficients(p-1)):
            assert a % p == (-1)**(j+1) % p
        h = 0
        for j, a in enumerate(reduced_coefficients(p-2)):
            h += pow(j+1, -1, p)
            assert a % p == (-1)**(j+1)*(j+2)*h % p
        for j, a in enumerate(reduced_coefficients(p)):
            assert a % p == (0 if j == 0 else (-1)**j % p)
    for r in range(2, 100):
        vals = reduced_coefficients(r)
        assert vals[-1] == 1 and vals[-2] == r-r%2
    assert {s: terminal_exceptions(29, s) for s in range(17, 30)
            if terminal_exceptions(29, s)} == {20: [1], 26: [10, 16], 28: [9, 25]}

    # At r=4, the one-child formula is 4*4 - H(1). Interpolate from
    # directly multiplied polynomials at e=0,1,2,3 (degree at most 3).
    sign_factor = 2
    for j, expected in [(1, Fraction(211, 16)), (2, Fraction(61, 4))]:
        nodes = range(4)
        value = Fraction()
        for a in nodes:
            term = Fraction(direct(4, j, a), sign_factor)
            for b in nodes:
                if a != b:
                    term *= (Fraction(-5, 2)-b)/(a-b)
            value += term
        assert value == expected
    print("Closed forms, extremal leaf tests at 29, and the four-row rational constants checked")

    # For two disjoint edges each child transfers at most four exponents,
    # so degree at most eight in e. Interpolate direct polynomials at 0..8.
    parents = [-1, 0, -1, 2, -1]
    scalar = Fraction()
    for a in range(9):
        term = Fraction(polynomial_coefficient(parents, a))
        for b in range(9):
            if b != a:
                term *= Fraction(102-b, a-b)
        scalar += term
    assert scalar == forest_coefficient(parents, 102) and scalar % 211 == 66
    print("Two independent exact evaluations certify the exceptional modulus 211")

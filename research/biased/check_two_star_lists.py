"""Check two-center scalars and the resulting bounds for ordinary trees."""

from argparse import ArgumentParser
from itertools import combinations_with_replacement, permutations, product
from math import comb
import subprocess

from research.biased.forest_grid import forest_coefficient
from research.biased.star_lists import terminal_exceptions
from research.biased.two_star_lists import two_star_coefficient


def determinant(matrix, p):
    a = [row.copy() for row in matrix]
    result = 1
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i] % p), None)
        if pivot is None:
            return 0
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            result = -result
        result = result*a[i][i] % p
        inv = pow(a[i][i], -1, p)
        for j in range(i+1, len(a)):
            factor = a[j][i]*inv % p
            for t in range(i+1, len(a)):
                a[j][t] = (a[j][t]-factor*a[i][t]) % p
    return result


def parent_matrix_check(parents, e, p):
    # Expand the selector coefficients by assigning the required exponents
    # to actual vertices. Keep the second exponent permutation as a determinant.
    r = len(parents)
    centers = sorted(set(parents)-{-1})
    assert centers and r+e < p
    cols = range(e, e+r)
    total = 0
    for point in product(range(1, p), repeat=len(centers)-1):
        params = dict(zip(centers, (1, *point)))
        for order in permutations(cols):
            matrix = []
            for v, m in enumerate(order):
                a = params.get(parents[v], 0)
                if v in params:
                    t = params[v]
                    row = [pow(t, -m, p)*pow(t+a, n, p) % p for n in cols]
                else:
                    row = [comb(n, m)*pow(a, n-m, p) % p if m <= n else 0 for n in cols]
                matrix.append(row)
            sign = (-1)**sum(order[i] > order[j] for j in range(r) for i in range(j))
            total += sign*determinant(matrix, p)
    value = (-1)**(r*(r-1)//2+len(centers)-1)*total % p
    assert value == forest_coefficient(parents, e) % p


def run(native=None):
    comparisons = 0
    for p in (5, 7, 11):
        for j, h, singles in [(0,0,0), (0,1,2), (1,1,0), (1,1,1), (2,1,1), (2,2,0)]:
            parents = [-1]+[0]*j+[-1]+[j+1]*h+[-1]*singles
            if len(parents) >= p:
                continue
            for e in range(min(p-len(parents), 2)+1):
                args = p, j, h, singles, e
                ans = two_star_coefficient(*args)
                assert ans == forest_coefficient(parents, e) % p
                if native:
                    assert ans == int(subprocess.check_output([native, *map(str, args)]))
                comparisons += 1
    print(f"{comparisons} two-center scalars compared with determinant-permutation expansion", flush=True)

    nested = [([-1,0,1,2], 0, 5), ([-1,0,1,0,-1], 1, 7),
              ([-1,0,1,2,0], 0, 7), ([-1,0,-1,2,3], 1, 7)]
    for parents, e, p in nested:
        parent_matrix_check(parents, e, p)
    print("Nested parent matrices checked on four forests with up to three centers", flush=True)

    for p in (29, 31, 37, 41, 43, 47, 53, 59, 61):
        pairs = 0
        undecided = []
        for s in range((p+5)//2, p+1):
            r = 2*s-p
            leaves = r-2
            bad = terminal_exceptions(p, s)
            for j, h in combinations_with_replacement(bad, 2):
                if j+h > leaves:
                    continue
                values = []
                for e in range(p-s-1, p-s+1):
                    args = p, j, h, leaves-j-h, e
                    value = two_star_coefficient(*args)
                    if native and p == 29:
                        assert value == int(subprocess.check_output([native, *map(str, args)]))
                    values.append(value)
                    if value:
                        break
                pairs += 1
                if not any(values):
                    undecided.append((s, j, h))
        assert not undecided, (p, undecided)
        print(f"p={p}: {pairs} admissible terminal pairs, unresolved {undecided}", flush=True)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--native", help="independent finite-field determinant executable")
    run(parser.parse_args().native)

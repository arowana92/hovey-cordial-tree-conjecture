"""Find an integer witness for arbitrary leaf additions, or exhaust permutations."""

import argparse
from fractions import Fraction
from itertools import permutations
from math import gcd


def coordinate_forms(rows, n):
    """Coefficient vectors of the coordinates on the rational kernel."""
    rows = [[Fraction(a) for a in row] for row in rows]
    pivots, free = [], []
    for col in range(n):
        k = len(pivots)
        pivot = next((i for i in range(k, len(rows)) if rows[i][col]), None)
        if pivot is None:
            free.append(col)
            continue
        rows[k], rows[pivot] = rows[pivot], rows[k]
        scale = rows[k][col]
        rows[k] = [x / scale for x in rows[k]]
        for i in range(len(rows)):
            if i != k and rows[i][col]:
                factor = rows[i][col]
                rows[i] = [a - factor * b for a, b in zip(rows[i], rows[k])]
        pivots.append(col)
    forms = [None] * n
    for i, col in enumerate(free):
        forms[col] = tuple(Fraction(i == j) for j in range(len(free)))
    for i, col in enumerate(pivots):
        forms[col] = tuple(-rows[i][j] for j in free)
    return [(Fraction(0),) * len(free), *forms]


def integer_point(forms):
    # Distinct linear forms give distinct univariate polynomials on this curve.
    for t in range(1, 2 + (len(forms) * (len(forms) - 1) // 2) * len(forms[0])):
        point = [sum(a * t**j for j, a in enumerate(form)) for form in forms]
        if len(set(point)) == len(point):
            denominator = 1
            for x in point:
                denominator *= x.denominator // gcd(denominator, x.denominator)
            return [int(x * denominator) for x in point]
    raise ArithmeticError("distinct polynomials agreed on too many points")


def rational_witness(parents):
    if not parents or parents[0] != -1 or any(
            not 0 <= parents[i] < i for i in range(1, len(parents))):
        raise ValueError("expected a parent-first rooted tree")
    n = len(parents)
    moving = [0] + [i for i in range(1, n) if parents[i] != 0]
    systems = 0
    for image in permutations(moving):
        # A fixed point at an internal edge would force its parent label to zero.
        if any(i == j for i, j in zip(moving[1:], image[1:])):
            continue
        rows = []
        for i, j in zip(moving[1:], image[1:]):
            row = [0] * (n - 1)
            if j:
                row[j - 1] += 1
            row[i - 1] -= 1
            row[parents[i] - 1] -= 1
            rows.append(row)
        systems += 1
        forms = coordinate_forms(rows, n - 1)
        if len(set(forms)) != n:
            continue
        point = integer_point(forms)
        edges = {point[i] + point[b] for i, b in enumerate(parents) if i}
        if len(edges) != n - 1 or not edges <= set(point) or len(set(point)) != n:
            raise ArithmeticError("invalid integer witness")
        return point, systems
    return None, systems


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parents", type=int, nargs="+")
    args = parser.parse_args()
    witness, systems = rational_witness(args.parents)
    if witness is None:
        print(f"Every permutation forces a collision ({systems} linear systems checked).")
    else:
        print(f"Integer labels: {witness}. Valid for all k > {max(witness) - min(witness)}.")

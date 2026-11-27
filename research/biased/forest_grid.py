"""Exact grid coefficient for small rooted forests by exponent transfer."""

from itertools import permutations
from math import comb


def forest_coefficient(parents, e):
    """Use two determinant expansions and recover the unique binomial splits."""
    r = len(parents)
    if e < 0 or any(not -1 <= p < v for v, p in enumerate(parents)):
        raise ValueError("expected a forest in parent order and nonnegative forbidden size")
    orders = []
    for row in permutations(range(r)):
        inversions = sum(row[a] > row[b] for b in range(r) for a in range(b))
        orders.append((row, (-1)**inversions))
    result = 0
    for target, sign in orders:
        for out, other_sign in orders:
            sent = [0]*r
            factor = sign * other_sign
            for v in reversed(range(r)):
                a = out[v] - target[v] + sent[v]
                p = parents[v]
                if a < 0 or a > e+out[v] or (p < 0 and a):
                    factor = 0
                    break
                if p >= 0:
                    factor *= comb(e+out[v], a)
                    sent[p] += a
            result += factor
    return (-1)**(r*(r-1)//2) * result

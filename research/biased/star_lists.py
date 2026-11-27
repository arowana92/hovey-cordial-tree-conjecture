"""Top grid coefficients for a rooted star and singleton components."""

from math import comb, factorial


def reduced_coefficients(r, e=0):
    """Coefficient for each child count j, divided by its common signed factorials."""
    if r < 1 or e < 0:
        raise ValueError("expected a positive number of rows and nonnegative forbidden size")
    # Sum of all entries in the translated truncated Pascal matrix.
    powers = [comb(e+r, d+1) - comb(e+d, d+1) for d in range(r)]
    values = []
    for q in range(r):
        total = 0
        for a in reversed(powers):
            total = q*total + a
        values.append((-1)**q * total)
    return [sum(comb(r, j-q)*values[q] for q in range(j+1)) for j in range(r)]


def grid_coefficient(r, j, e=0):
    if not 0 <= j < r:
        raise ValueError("expected between zero and r-1 children")
    return ((-1)**(r*(r-1)//2) * factorial(j) * factorial(r-j-1)
            * reduced_coefficients(r, e)[j])


def terminal_exceptions(p, s):
    """Child counts left by the coefficient test at the extremal leaf bound."""
    r = 2*s-p-1
    if not 1 <= r < p or not 1 <= s <= p:
        raise ValueError("expected a positive critical forest size below the modulus")
    return [j for j, a in enumerate(reduced_coefficients(r, p-s)) if j and a % p == 0]

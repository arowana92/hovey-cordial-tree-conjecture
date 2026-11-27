"""Verify the extra excluded prime residue after the four-leaf theorem."""

from fractions import Fraction
from math import comb, prod

from .forest_grid import forest_coefficient
from .star_lists import reduced_coefficients, terminal_exceptions
from .two_star_lists import two_star_coefficient


def pascal_sum(j, e):
    """Sum the individual truncated Pascal diagonals at an integer e."""
    def h(q):
        return sum(comb(n, m) * q**(n-m) for n in range(e, e+6) for m in range(e, n+1))
    return sum((-1)**q * comb(6, j-q) * h(q) for q in range(j+1))


def main():
    expected = [Fraction(7767,256), Fraction(8181,128), Fraction(9459,128),
                Fraction(5661,128), Fraction(2895,256)]
    for j, target in enumerate(expected, 1):
        values = [pascal_sum(j, e) for e in range(6)]
        assert values == [reduced_coefficients(6, e)[j] for e in range(6)]
        evaluated = sum(value * prod((Fraction(-7,2)-i)/(k-i) for i in range(6) if i != k)
                        for k, value in enumerate(values))
        assert evaluated == target
    assert expected[0].numerator == 9*863 and expected[1].numerator == 81*101
    for p, j, expected_scalar in ((101,2,9),(863,1,858)):
        s = (p+7)//2
        assert terminal_exceptions(p, s) == [j]
        parents = [-1]+[0]*j+[-1]+[1+j]*j+[-1]*(5-2*j)
        e = (p-9)//2
        assert forest_coefficient(parents, e) % p == expected_scalar
        assert two_star_coefficient(p, j, j, 5-2*j, e) == expected_scalar
        print(f"p={p}, s={s}, both terminals have {j} children, coefficient={expected_scalar}")
    print("Five rational coefficients checked")


if __name__ == "__main__":
    main()

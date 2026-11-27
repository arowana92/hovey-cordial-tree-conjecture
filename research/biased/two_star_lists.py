"""Grid coefficient for disjoint rooted stars over a prime field."""

from math import comb, factorial


def two_star_coefficient(p, j, h, singletons, e):
    """Coefficient of the uniform top list monomial, modulo the prime p."""
    r = 2+j+h+singletons
    if min(j, h, singletons, e) < 0 or r+e > p or r >= p:
        raise ValueError("expected nonnegative counts and r<p, r+e<=p")

    def kernel(left, right, points):
        # v(left)^T B(x) u(right), with both exponents in e..e+r-1.
        inv = pow(right, -1, p)
        ratio = left*inv % p
        powers = [sum(comb(i+d, d)*pow(ratio, i, p) for i in range(e, e+r-d))
                  * pow(inv, d, p) % p for d in range(r)]
        result = {}
        for x in points:
            value = 0
            for a in reversed(powers):
                value = (value*x+a) % p
            result[x] = value
        return result

    indices = [(a, b) for a in range(j+1) for b in range(h+1)]
    inverse = {(a, b): (-1)**(a+b)*comb(a+b, a) % p for a, b in indices}
    det = {(a, b): comb(r, a+b)*comb(a+b, a) % p for a, b in indices}
    total = 0
    for t in range(1, p):
        points = {i: (i[0]+t*i[1]) % p for i in indices}
        values = set(points.values())
        aa, ab, ba, bb = [kernel(left, right, values)
                          for left, right in ((1, 1), (1, t), (t, 1), (t, t))]
        # Extract z^j w^h in det(D) times the two-by-two determinant.
        for a, b in indices:
            x = points[a, b]
            for c in range(j-a+1):
                for d in range(h-b+1):
                    y = points[c, d]
                    total += (inverse[a, b]*inverse[c, d]*det[j-a-c, h-b-d]
                              * (aa[x]*bb[y]-ab[x]*ba[y]))
        total %= p
    # Mean over the nonzero field elements is minus their sum.
    scale = (-1)**(r*(r-1)//2)*factorial(j)*factorial(h)*factorial(singletons)
    return -total*scale % p

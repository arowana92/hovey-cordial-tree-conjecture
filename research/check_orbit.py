"""Check the three-vertex polynomial examples exactly in Z[omega], omega^2=-1-omega."""

from itertools import permutations
from math import prod


class Eisenstein(tuple):
    def __new__(cls, a=0, b=0):
        return super().__new__(cls, (a, b))

    def __mul__(self, other):
        a, b = self
        c, d = other
        return Eisenstein(a * c - b * d, a * d + b * c - b * d)

    def __sub__(self, other):
        return Eisenstein(self[0] - other[0], self[1] - other[1])


def ordered_product(values):
    return prod((b - a for i, a in enumerate(values) for j, b in enumerate(values) if i != j),
                start=Eisenstein(1))


def verify():
    parents = (0, 0, 1)
    ordinary = [(i + parents[i]) % 3 for i in (1, 2)]
    translated = [(i + parents[(i + 1) % 3]) % 3 for i in (1, 2)]
    if ordinary != [1, 0] or translated != [2, 2]:
        raise ValueError("partial translation")
    # The second product for the endpoint-rooted path only uses these two edges.
    reverse = (2, 1, 0)
    edges = {tuple(sorted((i, parents[i]))) for i in (1, 2)}
    if {tuple(sorted((reverse[a], reverse[b]))) for a, b in edges} != edges or reverse[0] == 0:
        raise ValueError("root stabilizer")

    roots = (Eisenstein(1), Eisenstein(0, 1), Eisenstein(-1, -1))
    one = Eisenstein(1)
    full = ordered_product(roots)
    eta = prod(roots, start=one)
    constant = full * full * eta * eta
    values = []
    for center in range(3):
        star = [roots[center] * roots[j] for j in range(3) if j != center]
        values.append(full * ordered_product(star))
    if any(v == Eisenstein() for v in values) or tuple(map(sum, zip(*values))) != (0, 0):
        raise ValueError("leading orbit sum")
    for assignment in permutations(roots):
        weights = [assignment[a] * assignment[b] for a, b in edges]
        m = prod(weights, start=one)
        normalized = Eisenstein(9) * m * m * full * ordered_product(weights)
        if normalized != constant:
            raise ValueError("normalized rainbow count")
    print("Verified the translation, rooted stabilizer, zero leading sum and normalized values.")


if __name__ == "__main__":
    verify()

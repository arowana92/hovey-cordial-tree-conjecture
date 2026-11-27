"""Top list-grid coefficients by signed subset convolution on a rooted forest."""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import comb



def coefficient_table(order, forbidden, modulus=None):
    """Produce a reusable evaluator at an integer or half-integer forbidden size.

    The forest is the sorted tuple of component trees used by research.eight.
    In modular mode the forbidden size is a nonnegative integer.
    """
    if order < 1 or Fraction(forbidden).denominator not in (1, 2):
        raise ValueError("Expected a positive order and a dyadic half-integer")
    if modulus is not None and (not isinstance(forbidden, int) or forbidden < 0 or modulus < 2):
        raise ValueError("Modular evaluation requires a nonnegative integer forbidden size")

    full = (1 << order) - 1
    indices = [tuple(i for i in range(order) if mask & (1 << i)) for mask in range(full + 1)]
    sums = list(map(sum, indices))
    max_transfer = order**2 // 4 + 1
    # At a half-integer, 4**k clears the denominator of binom(x,k).
    scale = 1 if modulus or Fraction(forbidden).denominator == 1 else 4**max_transfer
    weights = []
    for j in range(order):
        if modulus is not None:
            weights.append([comb(forbidden+j, k) % modulus for k in range(max_transfer+1)])
        else:
            row = [scale]
            value = Fraction(scale)
            for k in range(1, max_transfer+1):
                value *= Fraction(forbidden+j-k+1, k)
                assert value.denominator == 1
                row.append(value.numerator)
            weights.append(row)

    @lru_cache(None)
    def splits(mask, count):
        result = []
        for chosen in combinations(enumerate(indices[mask]), count):
            part = sum(1 << i for _, i in chosen)
            inversions = sum(pos for pos, _ in chosen) - count*(count-1)//2
            result.append((part, mask ^ part, (-1)**inversions))
        return result

    @lru_cache(None)
    def dimensions(tree):
        shift, children = tree
        parts = [dimensions(child) for child in children]
        return 1 + sum(n for n, _ in parts), shift + sum(d for _, d in parts)

    @lru_cache(None)
    def component(tree, target, offered, anchored):
        _, children = tree
        send = sums[offered] - sums[target] - dimensions(tree)[1]
        if send < 0 or (anchored and send != 0):
            return 0
        total = 0
        for _, other_in, sign_in in splits(target, 1):
            for head, other_out, sign_out in splits(offered, 1):
                weight = weights[head.bit_length()-1][send]
                if weight:
                    below = forest(children, other_in, other_out, False)
                    total += sign_in * sign_out * weight * below
        return total % modulus if modulus else total

    @lru_cache(None)
    def forest(trees, target, offered, anchored):
        if not trees:
            return 1
        if len(trees) == 1:
            return component(trees[0], target, offered, anchored)
        # Peel a smallest component, so the subset splits stay short.
        i = min(range(len(trees)), key=lambda k: dimensions(trees[k])[0])
        first = trees[i]
        rest = trees[:i] + trees[i+1:]
        width = dimensions(first)[0]
        total = 0
        for a, b, sign_in in splits(target, width):
            for c, d, sign_out in splits(offered, width):
                left = component(first, a, c, anchored)
                if left:
                    total += sign_in * sign_out * left * forest(rest, b, d, anchored)
        return total % modulus if modulus else total

    def coefficient(trees, shifts=None):
        if shifts is None:
            shifts = (0,) * order
        if len(shifts) != order or sum(shifts) or sum(map(abs, shifts)) > 2:
            raise ValueError("Expected zero shifts or one +1,-1 pair")
        positions = iter(shifts)

        def tag(children):
            return next(positions), tuple(tag(child) for child in children)

        decorated = tuple(tag(children) for children in trees)
        if sum(dimensions(tree)[0] for tree in decorated) != order:
            raise ValueError("Forest size differs from the exponent interval")
        value = (-1)**(order*(order-1)//2) * forest(decorated, full, full, True)
        return value % modulus if modulus else Fraction(value, scale**order)

    return coefficient

"""Independent forward expansion in two alternating sets of exponent indices."""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import comb


def exterior_evaluator(r, e, prime=None):
    """Return a coefficient evaluator on parent lists with specified degree shifts."""
    universe = (1 << r) - 1
    entries = [tuple(i for i in range(r) if mask & (1 << i)) for mask in range(1 << r)]
    mass = list(map(sum, entries))
    # Multiply each row by the same denominator. One extra unit of transfer
    # covers the shifted target monomials used in the exceptional cases.
    distance = r*r//4 + 1
    scale = 4**distance if Fraction(e).denominator == 2 else 1
    factors = []
    for j in range(r):
        if prime:
            factors.append([comb(e+j, k) % prime for k in range(distance+1)])
        else:
            row = [scale]
            for k in range(1, distance+1):
                numerator = row[-1] * (2*e + 2*j - 2*k + 2)
                quotient = Fraction(numerator, 2*k)
                assert quotient.denominator == 1
                row.append(quotient.numerator)
            factors.append(row)

    @lru_cache(None)
    def additions(mask, n):
        """All disjoint wedges of length n appended after mask, with signs."""
        result = []
        for subset in combinations(entries[universe ^ mask], n):
            bits = sum(1 << j for j in subset)
            inversions = sum(len(entries[mask >> (j+1)]) for j in subset)
            result.append((bits, (-1)**inversions))
        return result

    @lru_cache(None)
    def summary(tree):
        shift, children = tree
        desc = [summary(child) for child in children]
        return 1+sum(n for n,_ in desc), shift+sum(d for _,d in desc)

    def finish(output):
        if prime:
            return {ij: v % prime for ij, v in output.items() if v % prime}
        return {ij: v for ij, v in output.items() if v}

    @lru_cache(None)
    def rooted(tree, external):
        _, children = tree
        _, shifts = summary(tree)
        output = {}
        for (a,b), value in multiply(children, False).items():
            for i, sign_in in additions(a, 1):
                target = a | i
                for j, sign_out in additions(b, 1):
                    offered = b | j
                    sent = mass[offered] - mass[target] - shifts
                    if sent < 0 or (external and sent != 0):
                        continue
                    factor = factors[j.bit_length()-1][sent]
                    if factor:
                        ij = target, offered
                        output[ij] = output.get(ij, 0) + sign_in*sign_out*value*factor
        return finish(output)

    @lru_cache(None)
    def multiply(forest, external):
        if not forest:
            return {(0,0): 1}
        if len(forest) == 1:
            return rooted(forest[0], external)
        # Multiply the smallest component into the already expanded others.
        smallest = min(forest, key=lambda tree: summary(tree)[0])
        index = forest.index(smallest)
        rest = forest[:index] + forest[index+1:]
        width, _ = summary(smallest)
        multiplier = rooted(smallest, external)
        output = {}
        for (a,b), value in multiply(rest, external).items():
            for i, sign_in in additions(a, width):
                for j, sign_out in additions(b, width):
                    v = multiplier.get((i,j))
                    if v:
                        ij = a | i, b | j
                        output[ij] = output.get(ij, 0) + sign_in*sign_out*value*v
        return finish(output)

    def evaluate(parents, shifts=None):
        if shifts is None:
            shifts = [0] * r
        if len(parents) != r or len(shifts) != r or sum(shifts) or sum(map(abs,shifts)) > 2:
            raise ValueError("Expected zero shifts or a single +1,-1 pair")
        children = [[] for _ in range(r+1)]
        for v in reversed(range(r)):
            parent = parents[v]
            if not -1 <= parent < v:
                raise ValueError("Expected parents in topological order")
            children[parent].append((shifts[v], tuple(sorted(children[v]))))
        forest = tuple(sorted(children[-1]))
        value = (-1)**(r*(r-1)//2) * multiply(forest, True).get((universe, universe), 0)
        return value % prime if prime else Fraction(value, scale**r)

    return evaluate

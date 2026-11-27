"""Build whole trees and verify their modular vertex and edge counts from scratch."""

from itertools import product
from random import Random

from research.check_odd_quotient import piece
from research.matching_expansion import matching_labels, star_labels
from research.rainbow.verify import rooted_shapes


def check(labels, edges, modulus):
    assert len(edges) == len(labels) - 1
    vertices = [0] * modulus
    weights = [0] * modulus
    for label in labels:
        assert 0 <= label < modulus
        vertices[label] += 1
    for left, right in edges:
        weights[(labels[left] + labels[right]) % modulus] += 1
    assert max(vertices) - min(vertices) <= 1
    assert max(weights) - min(weights) <= 1
    return vertices, weights


def verify(parents, labels, joins, modulus, size, constructor):
    quotient_edges = [(p, i) for i, p in enumerate(parents) if i]
    before, before_edges = check(labels, quotient_edges, modulus)
    tree = [(i * size, i * size + j)
            for i in range(len(labels)) for j in range(1, size)]
    tree.extend((p * size + left, i * size + right)
                for (p, i), (left, right) in zip(quotient_edges, joins))
    if constructor is matching_labels:
        full = constructor(parents, labels, joins, modulus)
    else:
        full = constructor(parents, labels, joins, modulus, size)
    _, weights = check(full, tree, size * modulus)
    # The entire zero digit row reproduces the original edge histogram.
    assert weights[::size] == before_edges
    for digit in range(1, size):
        assert sorted(weights[digit::size]) == sorted(before)


def small_labeling(parents, modulus):
    # Complete finite search only for the small quotient fixtures.
    edges = [(p, i) for i, p in enumerate(parents) if i]
    for tail in product(range(modulus), repeat=len(parents)-1):
        labels = (0,) + tail
        try:
            check(labels, edges, modulus)
        except AssertionError:
            continue
        return labels
    raise AssertionError("no cordial quotient fixture")


def main():
    rng = Random(1991)
    matchings = stars = 0
    # All rooted shapes through order five, all four ways to join each pair.
    for order in range(1, 6):
        for parents in rooted_shapes(order).values():
            for m in (1, 3, 5, 7):
                labels = small_labeling(parents, m)
                for joins in product(tuple(product(range(2), repeat=2)), repeat=order-1):
                    verify(parents, labels, joins, m, 2, matching_labels)
                    matchings += 1
    for m in (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 35):
        for order in sorted({1, m, 2*m, *(m+i for i in range(1, m+1))}):
            for shape in (False, True):
                labels, edges = piece(order, m, shape, rng)
                parents = [-1] + [p for p, _ in edges]
                joins = [(rng.randrange(2), rng.randrange(2)) for _ in edges]
                verify(parents, labels, joins, m, 2, matching_labels)
                matchings += 1
                for size in (2, 3, 4, 5, 6, 9, 12, 15):
                    joins = [(rng.randrange(1, size), rng.randrange(1, size))
                             if rng.randrange(2) else (0, 0) for _ in edges]
                    verify(parents, labels, joins, m, size, star_labels)
                    stars += 1
    print(f"Verified {matchings} matching expansions and {stars} star expansions.")


if __name__ == "__main__":
    main()

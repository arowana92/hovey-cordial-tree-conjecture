"""Verify all rooted boundary forests on p-1 free vertices by signed moments."""

import argparse
import subprocess
from collections import Counter
from itertools import product
from pathlib import Path

from research.eight.verify import require
from research.rainbow.generate import rainbow
from research.rainbow.verify import rooted_shapes


def kernel_basis(columns, p):
    """Eliminate columns while recording the combinations giving zero."""
    height, width = len(columns[0]), len(columns)
    basis, kernel = {}, []
    for j, col in enumerate(columns):
        row = list(col) + [int(j == i) for i in range(width)]
        for pivot in sorted(basis):
            factor = row[pivot]
            if factor:
                row = [(a - factor * b) % p for a, b in zip(row, basis[pivot])]
        pivot = next((i for i in range(height) if row[i]), None)
        if pivot is None:
            kernel.append(row[height:])
        else:
            inverse = pow(row[pivot], -1, p)
            basis[pivot] = [a * inverse % p for a in row]
    return kernel


def projective_vectors(basis, p):
    for i, leading in enumerate(basis):
        tail = basis[i + 1:]
        for coeffs in product(range(p), repeat=len(tail)):
            yield [(v + sum(c * row[j] for c, row in zip(coeffs, tail))) % p
                   for j, v in enumerate(leading)]


def check_coloring(parents, roots, boundary, p):
    colored = list(parents)
    for j, color in zip(roots, boundary):
        colored[j] = -1 - color
    labels = rainbow(colored, p)
    require(sorted(labels) == list(range(1, p)), "invalid witness labels")
    weights = {(x + (labels[b] if b >= 0 else -1 - b)) % p
               for x, b in zip(labels, colored)}
    require(len(weights) == p - 1, "invalid witness weights")


def verify(engine, p):
    def moments(parents):
        engine.stdin.write(" ".join(map(str, parents)) + "\n")
        engine.stdin.flush()
        values = list(map(int, engine.stdout.readline().split()))
        require(len(values) == p and all(0 <= x < p for x in values), "invalid moments")
        return values

    shapes = rooted_shapes(p)
    scalar = witnesses = 0
    nullities = Counter()
    for tree in shapes.values():
        parents = [v - 1 for v in tree[1:]]
        if moments(parents)[0]:
            scalar += 1
            continue
        roots = [i for i, v in enumerate(parents) if v < 0]
        columns = []
        for j in roots:
            marked = parents.copy()
            marked[j] = -2
            count, *col = moments(marked)
            require(count == 0, "boundary invariance failed")
            columns.append(col)
        kernel = kernel_basis(columns, p)
        nullities[len(kernel)] += 1
        check_coloring(parents, roots, [0] * len(roots), p)
        witnesses += 1
        for vector in projective_vectors(kernel, p):
            check_coloring(parents, roots, vector, p)
            witnesses += 1
    print(f"p={p}: {len(shapes)} shapes, {scalar} nonzero scalar counts, "
          f"nullities {dict(sorted(nullities.items()))}, {witnesses} direct witnesses.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prime", type=int)
    parser.add_argument("counter", type=Path)
    args = parser.parse_args()
    with subprocess.Popen([str(args.counter.resolve()), str(args.prime)], text=True,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE) as process:
        try:
            verify(process, args.prime)
        finally:
            process.stdin.close()
        require(process.wait() == 0, "moment counter failed")

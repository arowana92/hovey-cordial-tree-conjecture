"""Check the prime-uniform extension for forests with at most four internal edges."""

import argparse
import subprocess
from functools import lru_cache
from math import factorial, isqrt
from pathlib import Path

from research.eight.verify import require
from research.rainbow.verify import rooted_shapes


def primes_through(n):
    return [p for p in range(2, n + 1)
            if all(p % d for d in range(2, isqrt(p) + 1))]


def rank(columns, p):
    basis = {}
    for column in columns:
        row = [x % p for x in column]
        for i in sorted(basis):
            factor = row[i]
            row = [(v - factor * w) % p for v, w in zip(row, basis[i])]
        pivot = next((i for i, x in enumerate(row) if x), None)
        if pivot is not None:
            inverse = pow(row[pivot], -1, p)
            basis[pivot] = [x * inverse % p for x in row]
    return len(basis)


def check_witness(parents, p, marked, labels):
    require(len(labels) == len(parents) and len(set(labels)) == len(labels)
            and all(0 < x < p for x in labels), "invalid template labels")
    weights = [(labels[i] + (labels[parent] if parent >= 0 else int(i == marked))) % p
               for i, parent in enumerate(parents)]
    require(len(set(weights)) == len(weights) and set(weights) <= {0, *labels},
            "template weights collide with each other or a padding label")


def verify(engine):
    @lru_cache(maxsize=None)
    def count(parents, p, marked=-1):
        args = [p, len(parents), marked, *parents]
        engine.stdin.write(" ".join(map(str, args)) + "\n")
        engine.stdin.flush()
        output = engine.stdout.readline()
        require("|" in output, "template counter stopped")
        sums, witness = output.split("|")
        values = tuple(map(int, sums.split()))
        labels = tuple(map(int, witness.split()))
        require(len(values) == len(parents) + 1, "missing moments")
        if labels:
            check_witness(parents, p, marked, labels)
        return values, labels

    def padded_column(parents, p, marked):
        (_, *active), _ = count(parents, p, marked)
        s = p - 1 - len(parents)
        result = [factorial(s) * v % p for v in active]
        if s:
            result.extend([-factorial(s - 1) * sum(active) % p] * s)
        return result

    def check_exception(parents, p):
        _, witness = count(parents, p)
        require(witness, "zero-boundary witness missing")
        n = len(parents)
        columns = [padded_column(parents, p, i) for i, parent in enumerate(parents)
                   if parent < 0]
        if n < p - 1:
            first = padded_column(parents + (-1,), p, n)
            for i in range(n, p - 1):
                col = first[:]
                col[i], col[n] = col[n], col[i]
                columns.append(col)
        actual = rank(columns, p)
        require(actual == len(columns),
                f"moment rank {actual} of {len(columns)} for {parents} at {p}")
        return actual

    primes = primes_through(63)
    shape_counts = [0] * 5
    exceptions = 0
    # Removing a dummy root yields all unordered forests. A non-singleton
    # component with d edges has d+1 <= 2d vertices, hence n <= 8.
    for n in range(2, 9):
        for tree in rooted_shapes(n + 1).values():
            parents = tuple(parent - 1 for parent in tree[1:])
            m = sum(parent >= 0 for parent in parents)
            if not 1 <= m <= 4:
                continue
            if any(i not in parents for i, parent in enumerate(parents) if parent < 0):
                continue
            bound = factorial(m + 1) * factorial(n + 1)
            cutoff = isqrt(5 ** m)
            value, modulus = 0, 1
            for q in primes:
                if q <= max(cutoff, n):
                    continue
                sums, _ = count(parents, q)
                digit = (sums[0] - value) * pow(modulus, -1, q) % q
                value += modulus * digit
                modulus *= q
                if modulus > 2 * bound:
                    break
            require(modulus > 2 * bound, "CRT modulus too small")
            if 2 * value > modulus:
                value -= modulus
            require(0 < abs(value) <= bound, f"stable invariant failed for {parents}")
            candidates = [p for p in primes_through(max(abs(value), cutoff))
                          if p > n and (p <= cutoff or value % p == 0)]
            for p in candidates:
                sums, _ = count(parents, p)
                if sums[0] == 0:
                    actual = check_exception(parents, p)
                    print(f"{parents} at p={p}: full first-moment rank {actual}")
                    exceptions += 1
            shape_counts[m] += 1
    print(f"Template counts by internal-edge count: {shape_counts[1:]}. "
          f"Verified {exceptions} exceptional template/prime pairs.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("counter", type=Path)
    args = parser.parse_args()
    with subprocess.Popen([str(args.counter.resolve())], text=True,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE) as process:
        try:
            verify(process)
        finally:
            process.stdin.close()
        require(process.wait() == 0, "template counter failed")

"""Verify each path-forest permutation and all independently prescribed parent colors."""
from itertools import combinations, permutations
from math import gcd
from pathlib import Path
import sys


def verify(k, count, path):
    units = [u for u in range(1, k) if gcd(k, u) == 1]
    powers = [k**i for i in range(count)]
    # Quotient the raw input space independently. Multiplication fixes the
    # excluded vertex label zero and multiplies every sum by the same unit.
    orbit = [-1] * k**count
    classes = 0
    for code in range(len(orbit)):
        if orbit[code] < 0:
            digits = [code // place % k for place in powers]
            for u in units:
                orbit[sum(place * (u*x % k) for x, place in zip(digits, powers))] = classes
            classes += 1

    expected = set()
    for cuts in combinations(range(1, k-1), count-1):
        points = (0,) + cuts + (k-1,)
        lengths = tuple(b-a for a,b in zip(points, points[1:]))
        expected.add(tuple(sorted(lengths)))
    shapes = len(expected)
    rows = 0
    residues = set(range(k))
    with Path(path).open() as stream:
        for line in stream:
            fields = line.split()
            assert list(map(int, fields[:2])) == [k, count]
            lengths = tuple(map(int, fields[2:2+count]))
            expected.remove(lengths)
            starts = [sum(lengths[:i]) for i in range(count)]
            internal = sorted(set(range(k-1)) - set(starts))
            hit = bytearray(classes)
            for word in fields[2+count:]:
                labels = [ord(c)-ord('!') for c in word]
                assert len(labels) == k-1 and set(labels) == residues-{0}
                weights = {(labels[i-1]+labels[i]) % k for i in internal}
                assert len(weights) == len(internal)
                remaining = residues-weights
                # Assign distinct available weights to the entering edges.
                # Subtracting each actual first label gives its required parent.
                codes = [{w: ((w-labels[i]) % k)*place for w in remaining}
                         for i, place in zip(starts, powers)]
                for incoming in permutations(remaining, count):
                    code = sum(row[w] for row,w in zip(codes, incoming))
                    hit[orbit[code]] = 1
                rows += 1
            assert all(hit), (lengths, hit.count(0))
    assert not expected
    print(k, count, 'shapes', shapes, 'permutations', rows,
          'parent tuples', shapes*k**count, flush=True)


if __name__ == '__main__':
    verify(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])

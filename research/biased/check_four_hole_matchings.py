"""Verify every positive witness and count the required orbits independently."""
import argparse
import hashlib
import math
import struct
import sys
from itertools import combinations

K = 27
FULL = (1 << K) - 1
RECORD = struct.Struct('<HHH23B')
UNITS = [u for u in range(K) if math.gcd(u, K) == 1]


def catalog():
    holes = sorted(sum(1 << x for x in group) for group in combinations(range(K), 4)
                   if sum(group) % K == 0)
    index = {mask: i for i, mask in enumerate(holes)}
    assert len(index) == math.comb(K, 4) // K == 650
    images = []
    for mask in holes:
        points = [x for x in range(K) if mask >> x & 1]
        images.append(tuple(index[sum(1 << (u*x % K) for x in points)] for u in UNITS))
    return holes, images


def orbit_count(images, lower):
    # A triple's least possible first index is at least lower precisely when
    # each of the three points belongs to this invariant subset.
    points = {i for i, orbit in enumerate(images) if min(orbit) >= lower}
    total = 0
    for column in range(len(UNITS)):
        seen = set()
        cycles = [0] * 4
        for i in points:
            if i in seen:
                continue
            j, length = i, 0
            while j not in seen:
                seen.add(j)
                length += 1
                j = images[j][column]
            assert j == i
            if length <= 3:
                cycles[length] += 1
        single, double, triple = cycles[1:]
        total += math.comb(single + 2, 3) + single*double + triple
    result, rem = divmod(total, len(UNITS))
    assert not rem
    return result


def check(stream, low, high):
    holes, images = catalog()
    shifts = [[x for x in range(K) if not mask >> x & 1] for mask in holes]
    bits = [1 << x for x in range(K)]
    zbit = [[bits[(-s-x) % K] for x in range(K)] for s in range(K)]
    last = (-1, -1, -1)
    digest = hashlib.sha256()
    count = 0
    while True:
        block = stream.read(RECORD.size * 4096)
        if not block:
            break
        digest.update(block)
        for i, j, k, *labels in RECORD.iter_unpack(block):
            key = (i, j, k)
            assert last < key and low <= i < high and i <= j <= k < len(holes)
            # Distinct sorted records cannot represent the same orbit after this test.
            assert all(key <= tuple(sorted(g)) for g in zip(images[i], images[j], images[k]))
            source, third = holes[i], holes[k]
            for s, x in zip(shifts[j], labels):
                assert x < K
                source |= bits[x]
                third |= zbit[s][x]
            assert source == third == FULL
            last, count = key, count + 1
    required = orbit_count(images, low) - orbit_count(images, high)
    assert count == required, (count, required)
    print(f'indices {low}..{high} exclusive, {count} matchings, SHA-256 {digest.hexdigest()}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--low', type=int, default=0)
    parser.add_argument('--high', type=int, default=650)
    args = parser.parse_args()
    assert 0 <= args.low <= args.high <= 650
    check(sys.stdin.buffer, args.low, args.high)

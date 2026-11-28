"""Verify every positive witness and count the required orbits independently."""
import argparse
import hashlib
import math
import re
import struct
import sys
from itertools import combinations
from pathlib import Path

K = 27
FULL = (1 << K) - 1
UNITS = [u for u in range(K) if math.gcd(u, K) == 1]


def catalog(omitted=4):
    assert omitted in (4, 5)
    holes = sorted(sum(1 << x for x in group) for group in combinations(range(K), omitted)
                   if sum(group) % K == 0)
    index = {mask: i for i, mask in enumerate(holes)}
    assert len(index) == math.comb(K, omitted) // K
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


def check(stream, low, high, omitted=4):
    holes, images = catalog(omitted)
    record = struct.Struct(f'<HHH{K-omitted}B')
    assert 0 <= low <= high <= len(holes)
    shifts = [[x for x in range(K) if not mask >> x & 1] for mask in holes]
    bits = [1 << x for x in range(K)]
    zbit = [[bits[(-s-x) % K] for x in range(K)] for s in range(K)]
    last = (-1, -1, -1)
    digest = hashlib.sha256()
    count = 0
    while True:
        block = stream.read(record.size * 4096)
        if not block:
            break
        digest.update(block)
        for i, j, k, *labels in record.iter_unpack(block):
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


def check_manifest(path, omitted):
    _, images = catalog(omitted)
    starts = sorted({min(orbit) for orbit in images})
    expected = orbit_count(images, 0)
    lines = path.read_text().splitlines()
    assert len(lines) == len(starts)
    total = 0
    for start, line in zip(starts, lines):
        match = re.fullmatch(r'indices (\d+)\.\.(\d+) exclusive, (\d+) matchings, SHA-256 ([0-9a-f]{64})', line)
        assert match, line
        low, high, count = map(int, match.groups()[:3])
        assert (low, high) == (start, start+1)
        assert count == orbit_count(images, low) - orbit_count(images, high)
        total += count
    assert total == expected
    print(f'{len(starts)} complete first-index ranges, {total} required matching orbits')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--low', type=int, default=0)
    parser.add_argument('--high', type=int)
    parser.add_argument('--holes', type=int, choices=(4, 5), default=4)
    parser.add_argument('--manifest', type=Path, help='audit the published shard inventory and counts')
    args = parser.parse_args()
    high = math.comb(K, args.holes) // K if args.high is None else args.high
    if args.manifest:
        check_manifest(args.manifest, args.holes)
    else:
        check(sys.stdin.buffer, args.low, high, args.holes)

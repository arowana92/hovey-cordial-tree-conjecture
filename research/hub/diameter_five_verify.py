"""Independently check a binary stream of diameter-five tree labelings."""

import argparse
import hashlib
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def expected(k):
    # Coefficients of the integer-partition generating product.
    p = [1] + [0]*k
    for size in range(1, k+1):
        for total in range(size, k+1):
            p[total] += p[total-size]
    result = 0
    for left in range(2, (k-2)//2+1):
        right = k-2-left
        a, b = p[left]-1, p[right]-1
        result += a*b if left < right else a*(a+1)//2
    return result


def verify(k, stream):
    digest = hashlib.sha256()
    rows = 0
    previous = None
    residues = set(range(k))

    def read(count):
        data = stream.read(count)
        if len(data) != count:
            raise ValueError("incomplete record")
        digest.update(data)
        return data

    while first := stream.read(1):
        digest.update(first)
        a = tuple(read(first[0]))
        b = tuple(read(read(1)[0]))
        labels = read(k)
        for half in (a, b):
            require(half and max(half) >= 2 and min(half) >= 1, "invalid branch sizes")
            require(tuple(sorted(half)) == half, "parts out of order")
        require(sum(a) + sum(b) == k-2, "tree has the wrong order")
        require((sum(a), a) <= (sum(b), b), "sides out of order")
        key = (sum(a), a, b)
        require(previous is None or previous < key, "duplicate or out-of-order shape")
        previous = key
        require(set(labels) == residues, "vertex labels do not form a permutation")
        weights = [(labels[0]+labels[1]) % k]
        start = 2
        for hub, half in zip(labels[:2], (a, b)):
            for size in half:
                parent = labels[start]
                weights.append((hub+parent) % k)
                weights.extend((parent+child) % k for child in labels[start+1:start+size])
                start += size
        require(start == k and len(weights) == len(set(weights)) == k-1, "invalid edge sums")
        rows += 1
    require(rows == expected(k), "incomplete shape coverage")
    return rows, digest.hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modulus", type=int, choices=range(6, 256), metavar="K")
    args = parser.parse_args()
    print(args.modulus, *verify(args.modulus, sys.stdin.buffer))

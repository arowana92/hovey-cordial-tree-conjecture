"""Check literal path witnesses, unit coverage, and all small failures by permutation."""
from itertools import combinations, permutations
from math import gcd
from pathlib import Path
import sys


def check(directory, k):
    group = set(range(k))
    units = [u for u in group if gcd(u, k) == 1]
    total = sum(group) % k
    required = {(x, b, c) for x in range(1, k) for b, c in combinations(range(k), 2)
                if (x + total + b + c) % k not in (0, x)}
    positive, negative = set(), set()
    for line in (directory / f"{k}.txt").read_text().splitlines():
        x, b, c, *row = map(int, line.split())
        triple = (x, b, c)
        orbit = {(u*x % k, *sorted((u*b % k, u*c % k))) for u in units}
        if triple != min(orbit) or orbit & (positive | negative) or not orbit <= required:
            raise ValueError("invalid or repeated input")
        if row:
            if len(row) != k-1 or row[0] != x or set(row) != group - {0}:
                raise ValueError("invalid path permutation")
            for parent in (b, c):
                sequence = [parent] + row
                weights = {(a+d) % k for a, d in zip(sequence, sequence[1:])}
                if len(weights) != k-1:
                    raise ValueError("repeated weight")
            positive.update(orbit)
        else:
            negative.update(orbit)
    if positive | negative != required:
        raise ValueError("missing inputs")
    if k <= 8:
        direct = set()
        for row in permutations(range(1, k)):
            internal = {(a+b) % k for a,b in zip(row,row[1:])}
            if len(internal) == k-2:
                b,c = sorted((w-row[0]) % k for w in group-internal)
                direct.add((row[0], b, c))
        if direct != positive:
            raise ValueError("exhaustive permutation search disagrees")
    elif negative:
        raise ValueError("moment-compatible inputs still lack witnesses")
    possible_pairs = {(b,c) for _,b,c in positive}
    predicted = {(b,c) for b,c in combinations(range(k), 2) if (total+b+c) % k}
    if possible_pairs != predicted:
        raise ValueError("incorrect free-first-label criterion")
    if k == 8:
        exceptional = {(2*u % 8, *sorted((u, 7*u % 8))) for u in units}
        if negative != exceptional:
            raise ValueError("incorrect eight-label exception list")
    if k >= 9:
        for x,z in permutations(range(1,k),2):
            allowed = {d for y,b,c in positive if y == x and (x+total+b+c) % k == z
                       for d in (b,c)}
            if allowed != {b for b in group if (2*b-z+x+total) % k}:
                raise ValueError("incorrect endpoint-prescribed parents")
    print(k, len(positive), len(negative), len(possible_pairs))
    return len(positive), len(negative)


if __name__ == "__main__":
    directory = Path(sys.argv[1])
    results = [check(directory,k) for k in range(3,int(sys.argv[2])+1)]
    print("checked triples", sum(p for p,_ in results), "additional small failures", sum(n for _,n in results))

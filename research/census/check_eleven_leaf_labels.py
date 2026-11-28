"""Check every boundary triple by masking collisions on the actual edges."""
from functools import lru_cache
from itertools import combinations, product
from math import gcd
from pathlib import Path
from struct import unpack_from
import sys

from research.rainbow.check_spine_samples import parse, profiles


def masks(k):
    colors = list(product(range(k), repeat=3))
    bins = [[bytearray((len(colors)+7)//8) for _ in range(k)] for _ in range(3)]
    pairs = list(combinations(range(3),2))
    differences = {pair:[bytearray((len(colors)+7)//8) for _ in range(k)] for pair in pairs}
    for i, c in enumerate(colors):
        for group, value in enumerate(c):
            bins[group][value][i//8] |= 1 << (i%8)
        for a, b in pairs:
            differences[a,b][(c[a]-c[b]) % k][i//8] |= 1 << (i%8)
    def pack(rows):
        return [int.from_bytes(v,"little") for v in rows]
    orbits = {}
    units = [a for a in range(1,k) if gcd(a,k) == 1]
    for i, c in enumerate(colors):
        key = min(((a*c[0])%k*k + (a*c[1])%k)*k + (a*c[2])%k for a in units)
        orbits.setdefault(key,[]).append(i)
    return [pack(v) for v in bins], {p:pack(v) for p,v in differences.items()}, list(orbits.values())


def check(words, stream):
    k = 27
    raw = stream.read_bytes()
    assert raw[:5] == b"SPN2\x1b"
    required = list(map(int,words.read_text().split()))
    bins, differences, orbits = masks(k)
    full = (1 << (k**3))-1
    @lru_cache(maxsize=20000)
    def permitted(group, residues):
        result = 0
        while residues:
            bit = residues & -residues
            result |= bins[group][bit.bit_length()-1]
            residues -= bit
        return result

    pos = 5
    actual = []
    total_rows = 0
    for word in required:
        code, count = unpack_from("<QI",raw,pos)
        pos += 12
        assert code == word and count > 0
        parents, roots, sizes, active = parse(k,code)
        assert len(profiles(k,sizes,active)) == k**3
        groups = []
        mass = 0
        for root, size in zip(roots,sizes):
            if size > mass:
                groups.append([])
            groups[-1].append(root)
            mass += size
        assert len(groups) == 3
        internal = [(v,p) for v,p in enumerate(parents) if p >= 0]
        cross = [(a,b,v,w) for a,b in combinations(range(3),2)
                 for v in groups[a] for w in groups[b]]
        covered = 0
        for _ in range(count):
            labels = raw[pos:pos+k-1]
            pos += k-1
            assert len(set(labels)) == k-1 and min(labels) == 1 and max(labels) == k-1
            used = 0
            for v,p in internal:
                bit = 1 << ((labels[v]+labels[p]) % k)
                assert not (bit & used)
                used |= bit
            free = ((1 << k)-1) ^ used
            good = full
            for a, verts in enumerate(groups):
                allowed = (1 << k)-1
                for v in verts:
                    shift = labels[v]
                    allowed &= (free >> shift) | (free << (k-shift))
                good &= permitted(a,allowed)
            for a,b,v,w in cross:
                good &= ~differences[a,b][(labels[w]-labels[v]) % k]
            covered |= good
        bits = covered.to_bytes((k**3+7)//8,"little")
        assert all(any(bits[i//8] & (1 << (i%8)) for i in orbit) for orbit in orbits)
        actual.append(code)
        total_rows += count
    assert len(set(actual)) == len(required) and pos == len(raw)
    print(f"Literal coverage: {len(actual)} forests, {total_rows} permutations, {len(actual)*k**3} parent triples")


if __name__ == "__main__":
    check(*(Path(arg) for arg in sys.argv[1:]))

"""Exhaust the actual high vertex choices on a sample of half-turn certificate rows."""

import argparse
from itertools import combinations
from pathlib import Path
from random import Random
import struct


def check(k, filename, limit):
    m, n = k//2, k-1
    # Enumerate *all* offset bits, including the two opposite common shifts.
    size = 1 << n
    full = (1 << size)-1
    edge_bit = [full//((1 << (1 << i))+1) << (1 << i) for i in range(n)]
    collision = {(i,j): edge_bit[i]^edge_bit[j] for i,j in combinations(range(n),2)}
    rng = Random(1991)
    samples = []
    count = 0
    with filename.open("rb") as f:
        assert f.read(5) == b'FBL1'+bytes([k])
        while chunk := f.read(12):
            word, profiles = struct.unpack("<QI",chunk)
            stack, parents, roots = [], [], []
            for a in f"{word:0{2*n}b}":
                if a == "1":
                    if not stack:
                        roots.append(len(parents))
                    parents.append(stack[-1] if stack else -1)
                    stack.append(len(parents)-1)
                else:
                    stack.pop()
            for _ in range(profiles):
                raw, rows = struct.unpack("<HI",f.read(6))
                where = f.tell()
                f.seek(8*rows,1)
                pos = count if count < limit else rng.randrange(count+1)
                if pos < limit:
                    p = parents[:]
                    for i,j in zip(roots,roots[1:]+[n]):
                        if j-i > i:
                            color,raw = raw%m,raw//m
                        p[i] = -1-color
                    item = (where, rows, p)
                    if pos == count:
                        samples.append(item)
                    else:
                        samples[pos] = item
                count += 1
        lifts = 0
        for where,rows,parents in samples:
            f.seek(where)
            cover = 0
            for packed, in struct.iter_unpack("<Q",f.read(8*rows)):
                lows = [packed>>(3*i)&7 for i in range(n)]
                assert sorted(lows) == [0]+[t for t in range(1,m) for _ in range(2)]
                order = [lows[:i].count(a) if a else 1 for i,a in enumerate(lows)]
                pairs = None
                for flips in range(1 << (m-1)):
                    x = [a+m*(b ^ ((flips<<1)>>a&1)) for a,b in zip(lows,order)]
                    assert sorted(x) == list(range(1,k))
                    weights = [(x[i]+(x[p] if p>=0 else -1-p))%k for i,p in enumerate(parents)]
                    if pairs is None:
                        pairs = [(i,j) for i,j in combinations(range(n),2)
                                 if (weights[i]-weights[j])%m == 0]
                        assert len(pairs)==m-1
                    hit = full
                    for i,j in pairs:
                        opposite = collision[i,j]
                        hit &= opposite if weights[i]==weights[j] else full^opposite
                    cover |= hit
                    lifts += 1
            assert cover == full
    print(f"k={k} direct profiles={len(samples)} vertex lifts={lifts} "
          f"offset vectors={len(samples)*size}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("k",type=int,choices=(4,8,16))
    parser.add_argument("file",type=Path)
    parser.add_argument("--limit",type=int,default=16)
    args = parser.parse_args()
    check(args.k,args.file,args.limit)

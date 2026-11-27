"""Verify prime-power offset covers by testing every pair of endpoint sums."""

import argparse
from collections import Counter, defaultdict
import gzip
from itertools import combinations
import json
from pathlib import Path

from research.rainbow.spine_counts import boundaries, rooted


def masks(n, p):
    total = p**n
    universe = (1<<total)-1
    digits = [[0]*p for _ in range(n)]
    for code in range(total):
        value = code
        for i in range(n):
            digits[i][value%p] |= 1<<code
            value //= p
    # Table entry (i,j,d) removes assignments with digit_i-digit_j = d.
    allowed = {}
    for i,j in combinations(range(n),2):
        for d in range(p):
            collision = 0
            for a in range(p):
                collision |= digits[i][a] & digits[j][(a-d)%p]
            allowed[i,j,d] = universe^collision
    return universe,allowed


def verify(k, directory):
    p = 3 if k == 9 else 2
    stride, n = k//p, k-1
    universe, allowed = masks(n,p)
    shapes = defaultdict(set)
    totals = Counter()
    with gzip.open(directory/f"power{k}.jsonl.gz","rt") as file:
        for line in file:
            parents,words = json.loads(line)
            assert len(parents) == n
            children = [[] for _ in parents]
            roots = []
            for i,j in enumerate(parents):
                assert -stride <= j < i
                if j < 0:
                    roots.append(i)
                else:
                    children[j].append(i)

            def branch(v):
                return "("+ "".join(sorted(branch(j) for j in children[v])) +")"

            pieces = sorted((len(s),s,-1-parents[v]) for v in roots for s in [branch(v)])
            shape = tuple(s for _,s,_ in pieces)
            colors = tuple(c for _,_,c in pieces)
            assert colors not in shapes[shape]
            shapes[shape].add(colors)
            sizes = [length//2 for length,_,_ in pieces]
            eligible = 3*sum(not c for c in children) <= 2*(k-2)
            if eligible:
                starts = [i for i in range(1,len(colors)) if colors[i] != colors[i-1]]
                for run,start in enumerate(starts,1):
                    assert sizes[start] >= sum(sizes[:start])+run
            else:
                assert not any(colors)

            covered = 0
            for word in words:
                assert 0 <= word < 16**n
                x = [word>>(4*i)&15 for i in range(n)]
                assert sorted(x) == list(range(1,k))
                weights = [(x[i]+(x[j] if j >= 0 else -1-j))%k for i,j in enumerate(parents)]
                hits = universe
                for i,j in combinations(range(n),2):
                    diff = weights[j]-weights[i]
                    if diff%stride == 0:
                        hits &= allowed[i,j,(diff//stride)%p]
                covered |= hits
            assert covered == universe
            totals.update(low_inputs=1,offset_vectors=p**n,witnesses=len(words))
    # Canonical unordered shapes, counted independently by multiset coefficients.
    assert len(shapes) == sum(rooted(k).values())
    for shape,colors in shapes.items():
        sizes = [len(s)//2 for s in shape]
        leaves = sum(s.count("()") for s in shape)
        expected = boundaries(sizes,stride) if 3*leaves <= 2*(k-2) else 1
        assert len(colors) == expected
    print(f"k={k} rooted shapes={len(shapes)}, low inputs={totals['low_inputs']}, "
          f"offset vectors={totals['offset_vectors']}, witness rows={totals['witnesses']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory",type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument("moduli",nargs="*",type=int)
    args = parser.parse_args()
    for k in args.moduli or [4,8,9]:
        assert k in (4,8,9)
        verify(k,args.directory)

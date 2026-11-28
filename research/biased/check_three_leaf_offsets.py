"""Audit two exceptional offsets on every three-leaf tree of the given order."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from itertools import combinations_with_replacement
from math import comb, gcd
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory


def shapes(k):
    return [(a,b,k-1-a-b) for a in range(1,k) for b in range(a,k)
            if b <= k-1-a-b]


def edges(arms):
    result = []
    next_vertex = 1
    for length in arms:
        last = 0
        for v in range(next_vertex,next_vertex+length):
            result.append((last,v))
            last = v
        next_vertex += length
    return result


def audit(path, arms):
    graph = edges(arms)
    k = len(graph)+1
    units = [u for u in range(1,k) if gcd(u,k)==1]
    expanded = {}
    rows = 0
    with path.open() as stream:
        for line in stream:
            i,j,a,b,*labels = map(int,line.split())
            assert sorted(labels) == list(range(k))
            assert 0 <= i <= j < k and (not i or i < j)
            assert 0 <= a < k and 0 <= b < k
            assert (i == 0) == (a == 0) and (j == 0) == (b == 0)
            weights = [(labels[x]+labels[y]) % k for x,y in graph]
            if i:
                weights[i-1] = (weights[i-1]+a) % k
            if j:
                weights[j-1] = (weights[j-1]+b) % k
            assert len(set(weights)) == k-1
            seen = expanded.setdefault((i,j),set())
            orbit = {(a*u % k,b*u % k) for u in units}
            assert seen.isdisjoint(orbit)
            seen.update(orbit)
            rows += 1
    total = sum(map(len,expanded.values()))
    assert total == 1+(k-1)**2+comb(k-1,2)*(k-1)**2
    return rows,total


def census(k, generator, directory, workers):
    cases = shapes(k)
    independent = [p for p in combinations_with_replacement(range(1,k),3)
                   if sum(p)==k-1]
    assert cases == independent
    def one(arms):
        a,b,c = arms
        path = directory/f'{a}-{b}-{c}.txt'
        with path.open('wb') as stream:
            subprocess.run([generator,str(k),str(a),str(b)],stdout=stream,check=True)
        rows,total = audit(path,arms)
        digest = sha256(path.read_bytes()).hexdigest()
        return f'{a} {b} {c} {digest} {rows} {total}\n'
    with ThreadPoolExecutor(max_workers=workers) as pool:
        lines = list(pool.map(one,cases))
    return ''.join(lines)


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('generator',type=Path)
    cli.add_argument('--modulus',type=int,default=27)
    cli.add_argument('--workers',type=int,default=2)
    cli.add_argument('--keep',type=Path,help='keep row streams for whole-tree replay')
    cli.add_argument('--manifest',type=Path)
    args = cli.parse_args()
    with TemporaryDirectory() as scratch:
        directory = args.keep or Path(scratch)
        directory.mkdir(exist_ok=True)
        result = census(args.modulus,args.generator.resolve(),directory,args.workers)
    if args.manifest:
        assert args.manifest.read_text() == result
    print(result,end='')

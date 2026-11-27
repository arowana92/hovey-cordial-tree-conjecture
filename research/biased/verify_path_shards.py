"""Count affine dihedral offset orbits by Burnside; audit and hash all witness shards."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from math import gcd
from pathlib import Path
import subprocess


def orbit_count(k):
    total = 0
    for direction in (-1,1):
        for shift in range(k):
            unused = set(range(k))
            periods = []
            while unused:
                i = next(iter(unused))
                size = 0
                while i in unused:
                    unused.remove(i)
                    i = (direction*i+shift)%k
                    size += 1
                periods.append(size)
            for unit in range(1,k):
                if gcd(k,unit)>1:
                    continue
                for translation in range(k):
                    ways = [1]+[0]*(k-1)
                    for L in periods:
                        sums = []
                        for v in range(k):
                            y = v
                            weight = 0
                            for _ in range(L):
                                weight += y
                                y = (unit*y+translation)%k
                            if y==v:
                                sums.append(weight%k)
                        ways = [sum(ways[(w-s)%k] for s in sums) for w in range(k)]
                    total += ways[(k*(k-1)//2)%k]
    group = 2*k*k*sum(gcd(k,u)==1 for u in range(k))
    if total%group:
        raise ArithmeticError("nonintegral orbit count")
    return total//group


def audit(k,parts,directory,verifier,workers):
    def one(i):
        path = directory/f"{i}.bin"
        result = subprocess.run([verifier,str(k),path,str(i),str(parts)],check=True,
                                capture_output=True,text=True)
        count = int(result.stdout.strip().split("=")[-1])
        digest = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda:f.read(1<<20),b""):
                digest.update(chunk)
        if path.stat().st_size!=16*count:
            raise ValueError("inconsistent stream length")
        return count,digest.hexdigest()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(one,range(parts)))
    total = sum(n for n,_ in rows)
    if total!=orbit_count(k):
        raise ValueError("the affine orbit catalog is incomplete")
    print(f"k={k} verified affine orbits={total}")
    return "".join(f"{digest}  {i}.bin\n" for i,(_,digest) in enumerate(rows))


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("k",type=int)
    parser.add_argument("parts",type=int)
    parser.add_argument("directory",type=Path)
    parser.add_argument("verifier",type=Path)
    parser.add_argument("manifest",type=Path)
    parser.add_argument("--workers",type=int,default=1)
    args = parser.parse_args()
    manifest = audit(args.k,args.parts,args.directory,args.verifier.resolve(),args.workers)
    args.manifest.write_text(manifest)

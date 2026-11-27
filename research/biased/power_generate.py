"""Generate high-offset covers for the ordered-cut test at k=4,8,9."""

import argparse
from functools import lru_cache
import json
from pathlib import Path
import subprocess


@lru_cache(None)
def rooted(n):
    types = [t for size in range(1,n) for t in rooted(size)]

    def forests(left, start):
        if not left:
            yield ()
            return
        for j in range(start,len(types)):
            t = types[j]
            size = len(t)//2
            if size > left:
                break
            for rest in forests(left-size,j):
                yield (t,*rest)

    return sorted("("+"".join(f)+")" for f in forests(n-1,0))


def cases(k, stride):
    for tree in rooted(k):
        parents, roots, stack, sizes = [], [], [], []
        for c in tree[1:-1]:
            if c == "(":
                if not stack:
                    roots.append(len(parents))
                parents.append(stack[-1] if stack else -1)
                stack.append(len(parents)-1)
            else:
                stack.pop()
                if not stack:
                    sizes.append(len(parents)-roots[-1])

        def walk(i, runs, previous):
            if i == len(roots):
                yield parents[:]
                return
            for a in range(stride):
                if i and a != previous and sizes[i] < sum(sizes[:i])+runs:
                    continue
                parents[roots[i]] = -1-a
                yield from walk(i+1,runs+int(a != previous),a)

        if 3*tree.count("()") <= 2*(k-2):
            yield from walk(0,0,-1)
        else:
            yield parents


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("search",type=Path)
    parser.add_argument("modulus",type=int,choices=(4,8,9))
    args = parser.parse_args()
    k = args.modulus
    p = 3 if k == 9 else 2
    with subprocess.Popen([str(args.search.resolve())],text=True,
                          stdin=subprocess.PIPE,stdout=subprocess.PIPE) as proc:
        try:
            for parents in cases(k,k//p):
                proc.stdin.write(" ".join(map(str,[k,p,*parents]))+"\n")
                proc.stdin.flush()
                words = list(map(int,proc.stdout.readline().split()))
                if not words:
                    raise ValueError(f"missing cover at {parents}")
                print(json.dumps([parents,words],separators=(",",":")))
        finally:
            proc.stdin.close()
        if proc.wait():
            raise RuntimeError("search failed")

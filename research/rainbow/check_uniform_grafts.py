"""Reconstruct uniform path grafts on arbitrarily labeled cores from the certificate rows."""

from argparse import ArgumentParser
from collections import Counter
from functools import lru_cache
from math import gcd
from pathlib import Path
from random import Random


@lru_cache(None)
def four_row(lengths, x):
    parent = []
    for i,n in enumerate(lengths):
        parent.append(-1 - (x if i == 0 else 0))
        for _ in range(n-1):
            parent.append(len(parent)-1)
    q = len(parent)//4
    vertices, edges, labels = [q]*4, [q]*4, []

    def visit(i):
        if i == len(parent):
            return True
        prev = parent[i]
        old = labels[prev] if prev >= 0 else -1-prev
        for z in range(4):
            w = (old+z)%4
            if vertices[z] and edges[w]:
                labels.append(z)
                vertices[z] -= 1
                edges[w] -= 1
                if visit(i+1):
                    return True
                vertices[z] += 1
                edges[w] += 1
                labels.pop()
        return False

    return tuple(labels) if visit(0) else None


def partitions(n, least=1):
    if not n:
        yield ()
    for a in range(least,n+1):
        for rest in partitions(n-a,a):
            yield (a,)+rest


def batches(k, sizes, core, joint):
    parents = [-1]+[v//2 for v in range(1,core)]
    arms = []
    for n in sizes:
        path = list(range(len(parents),len(parents)+n))
        parents.extend([joint]+path[:-1])
        arms.append(path)
    total = sum(sizes)
    steps = []
    while total:
        arms.sort(key=len)
        take = k
        if k == 4:
            if total == 8 or (total == 12 and all(len(p)==2 for p in arms)):
                take = total
            elif len(arms) >= 2 and len(arms[-1]) == len(arms[-2]) == 2:
                if len(arms[0]) == 2:
                    take = 8
                else:
                    # At least two singleton arms by parity.
                    arms = arms[2:-1]+[arms[0], arms[1], arms[-1]]
        removed = []
        total -= take
        while take:
            n = min(take,len(arms[-1]))
            removed.append(arms[-1][-n:])
            del arms[-1][-n:]
            if not arms[-1]:
                arms.pop()
            take -= n
        steps.append(sorted(removed,key=len))
    return parents, steps[::-1]


def check(directory, k):
    rng = Random(199104000+k)
    tests = []
    shapes = set()
    for i in range(72):
        q = 1+i%5
        left = q*k
        lengths = []
        while left:
            n = min(left,rng.randint(1, max(1,(i%3+1)*k//3)))
            lengths.append(n)
            left -= n
        if i%6 == 0:
            lengths = [1]*(q*k)
        if k == 4 and lengths == [2,2]:
            lengths = [1,3]
        if k == 4 and i%6 == 1 and q > 1:
            lengths = [2]*(2*q)
        core = 1+i%9
        parents, steps = batches(k, lengths, core, rng.randrange(core))
        tests.append((q, [rng.randrange(k) for _ in range(core)], parents, steps))
        shapes.update(tuple(map(len,p)) for p in steps)
    rows = {}
    if k != 4:
        with (directory/f"neutral{k}").open() as src:
            for line in src:
                fields = line.split()
                lengths = tuple(map(int, fields[2:-1]))
                if lengths in shapes:
                    rows[lengths,int(fields[1])] = tuple(ord(z)-33 for z in fields[-1])
    cases = 0
    for q, fixed, parents, steps in tests:
        f = fixed.copy()+[None]*(len(parents)-len(fixed))
        for paths in steps:
            roots = [f[parents[path[0]]] for path in paths]
            common = roots[-1]
            delta = (roots[0]-common)%k
            lengths = tuple(map(len,paths))
            assert all(y == common for y in roots[1:])
            assert not delta or lengths[0] < lengths[1]
            if k == 4:
                digits = four_row(lengths,delta)
                assert digits is not None
                scale = 1
            else:
                rep = gcd(delta,k) if delta else 0
                digits = rows[lengths,rep]
                scale = next(u for u in range(1,k) if gcd(u,k)==1 and u*rep%k==delta)
            for v,z in zip((v for path in paths for v in path),digits):
                f[v] = (common+scale*z)%k
            cases += 1
        assert f[:len(fixed)] == fixed and None not in f
        new = range(len(fixed),len(f))
        assert Counter(f[i] for i in new) == Counter({i:q for i in range(k)})
        assert Counter((f[parents[i]]+f[i])%k for i in new) == Counter({i:q for i in range(k)})
        if k % 2:
            actual = [x+k*rng.randrange(2) for x in fixed]
            added_edges = []
            for v in new:
                p = parents[v]
                port = p if p < len(fixed) else len(fixed)+2*(p-len(fixed))+rng.randrange(2)
                bit = len(actual)
                entry = f[v] if f[v]%2 == actual[port]%2 else f[v]+k
                actual.extend((entry,(entry+k)%(2*k)))
                added_edges.extend(((port,bit),(bit,bit+1)))
            expected = Counter({x:q for x in range(2*k)})
            assert Counter(actual[len(fixed):]) == expected
            assert Counter((actual[u]+actual[v])%(2*k) for u,v in added_edges) == expected
    return cases


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("directory",type=Path)
    parser.add_argument("moduli",type=int,nargs="+")
    args = parser.parse_args()
    assert four_row((2,2),0) is None
    for p in partitions(4):
        for x in (range(4) if len(p)>1 and p[0]<p[1] else [0]):
            assert (four_row(p,x) is None) == (p == (2,2))
    assert all(four_row(p,0) for p in partitions(8)) and four_row((2,)*6,0)
    print("whole trees",72*len(args.moduli),"uniform batches",sum(check(args.directory,k) for k in args.moduli))

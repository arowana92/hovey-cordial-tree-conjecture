"""Build matched-chain grafts batch by batch, preserving a divisible core."""
from argparse import ArgumentParser
from collections import Counter
from random import Random

from research.paired_forest import lift
from .generate import native_search


def peel(arms, m):
    remaining = sum(map(len,arms))
    steps = []
    while remaining:
        arms.sort(key=len)
        take = (remaining-1)%m+1
        remaining -= take
        cut = []
        while take:
            arm = arms[-1]
            n = min(take,len(arm))
            cut.append(arm[-n:])
            del arm[-n:]
            if not arm:
                arms.pop()
            take -= n
        steps.append(sorted(cut,key=len))
    return steps[::-1]


def extend(m, fixed, core_parent, parents, steps, witness):
    k = 2*m
    counts = Counter((fixed[i]+fixed[p])%k for i,p in enumerate(core_parent) if i)
    deficit = min(range(k),key=counts.__getitem__)
    f = fixed.copy()+[None]*(2*len(parents))
    for paths in steps:
        first = paths[0][0]
        old = f[parents[first]]
        z = (deficit-old)%k
        f[first:first+2] = [z,(z+m)%k]
        paths = [p for p in [paths[0][1:]]+paths[1:] if p]
        if not paths:
            continue
        shift = z%m
        links = []
        for path in paths:
            n = len(links)
            links.append(-1-(f[parents[path[0]]]-shift)%m)
            links.extend(range(n,n+len(path)-1))
        actual = len(links)
        links.extend(range(actual-1,m-2))
        digits = witness(links,m)
        even = set()
        for pair,x in zip((v for p in paths for v in p),digits):
            old = f[parents[pair]]
            entry = lift((shift+x)%m,old%2,m)
            f[pair:pair+2] = [entry,(entry+m)%k]
            even.add((entry+old)%k)
        if actual == m-1:
            deficit, = set(range(0,k,2))-even
    return f


def check(library,m):
    witness = native_search(library,m)
    rng = Random(1991120+m)
    k = 2*m
    total = 0
    for i in range(85):
        n = k*(1+i%3)
        if i%2:
            core_parent = [-1]+list(range(n-1))
            fixed = [(v//2+(v%2)*(n//2))%k for v in range(n)]
        else:
            core_parent = [-1]+[0]*(n-1)
            fixed = [v%k for v in range(n)]
        shift = rng.randrange(k)
        fixed = [(x+shift)%k for x in fixed]
        edges = [(p,v) for v,p in enumerate(core_parent) if v]
        joint = rng.randrange(n)
        parents,arms = {},[]
        lengths = [rng.randint(1,m+2) for _ in range(rng.randint(1,8))]
        if i%5 == 0:
            lengths = [1]*(i+1)
        for length in lengths:
            arm = []
            old = joint
            for _ in range(length):
                first = n+2*len(parents)
                parents[first] = old
                arm.append(first)
                edges.extend([(old,first),(first,first+1)])
                old = first+rng.randrange(2)
            arms.append(arm)
        steps = peel(arms,m)
        f = extend(m,fixed,core_parent,parents,steps,witness)
        assert f[:n] == fixed and all(0<=x<k for x in f)
        assert len(edges)+1 == len(f)
        for values in (f,[(f[v]+f[w])%k for v,w in edges]):
            bins = Counter(values)
            counts = [bins[x] for x in range(k)]
            assert max(counts)-min(counts) <= 1
        total += len(steps)
    return total


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("library")
    parser.add_argument("moduli",type=int,nargs="+")
    args = parser.parse_args()
    print("matched grafts",85*len(args.moduli),"batches",sum(check(args.library,m) for m in args.moduli))

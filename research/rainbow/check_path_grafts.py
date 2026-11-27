"""Build fixed-core extensions from the published path rows and count every edge."""

from argparse import ArgumentParser
from collections import Counter, defaultdict
from itertools import permutations, product
from math import gcd
from pathlib import Path
from random import Random


def counts(values, k):
    bins = Counter(x % k for x in values)
    return [bins[i] for i in range(k)]


def balanced(bins):
    return max(bins) - min(bins) <= 1


def four_weights(digits, lengths, roots):
    i = 0
    edges = []
    for length,old in zip(lengths,roots):
        for x in digits[i:i+length]:
            edges.append((old+x)%4)
            old = x
        i += length
    return edges


def four_certificates():
    rows = {}
    assert all(len(set(four_weights(p,(1,2),(0,1))))<3 for p in permutations((1,2,3)))
    # For a mixed pair (1,2), use this test only when both paths start at the joint.
    for lengths in [(1,), (2,), (1,1), (3,), (1,1,1), (1,2)]:
        for roots in product(range(4),repeat=len(lengths)):
            if lengths==(1,2) and roots[0]!=roots[1]:
                continue
            size = sum(lengths)
            rows[lengths,roots] = next(p for p in permutations(range(1,4),size)
                                       if len(set(four_weights(p,lengths,roots)))==size)
    whole = {}
    for root,deficit in product(range(4),repeat=2):
        for p in permutations(range(4)):
            edges = four_weights(p,(2,2),(root,root))
            if balanced([edges.count(w)-(w==deficit) for w in range(4)]):
                whole[root,deficit]=p
                break
    assert len(whole)==16
    return rows,whole


def four_batch(arms,t):
    if t==3 and len(arms)>=3:
        removed = [p[-1:] for p in arms[-3:]]
        for p in arms[-3:]:
            p.pop()
        return removed
    if len(arms)==2 and t==3 and [len(p) for p in arms]==[2,2]:
        removed = arms.copy()
        arms.clear()
        return removed
    removed = []
    while t:
        take = min(t,len(arms[-1]))
        removed.append(arms[-1][-take:])
        del arms[-1][-take:]
        t -= take
        if not arms[-1]:
            arms.pop()
    return sorted(removed,key=len)


def prepare(k, rng, trial):
    core = rng.choice([1, k, k+1, 2*k, 2*k+1, 3*k])
    joint = rng.randrange(core)
    affine = rng.choice([u for u in range(1,k) if gcd(u,k)==1])
    shift = rng.randrange(k)
    if trial%2:
        parents = [-1] + list(range(core-1))
        base = [v//2 + (v%2)*((core+1)//2) for v in range(core)]
    else:
        parents = [-1] + [0]*(core-1)
        base = list(range(core))
    fixed = [(affine*x+shift)%k for x in base]
    sizes = [rng.randrange(1,k+4) for _ in range(rng.randint(1,8))]
    if trial%4==0:
        sizes = [1]*(k+trial%7) + [2,2,3]
    arms = []
    for size in sizes:
        path = list(range(len(parents),len(parents)+size))
        parents.extend([joint]+path[:-1])
        arms.append(path)
    n = len(parents)
    steps = []
    while n>core:
        arms = sorted((p for p in arms if p),key=len)
        t = (n-1)%k
        if t==0:
            steps.append((None,[arms[-1][-1:]]))
            arms[-1].pop()
            n -= 1
            continue
        assert t<=n-core
        if k==4:
            removed = four_batch(arms,t)
            steps.append((tuple(map(len,removed)),removed))
            n -= sum(map(len,removed))
            continue
        n -= t
        removed = []
        while t:
            take = min(t,len(arms[-1]))
            removed.append(arms[-1][-take:])
            del arms[-1][-take:]
            t -= take
            if not arms[-1]:
                arms.pop()
        removed.sort(key=len)
        assert all(parents[p[0]]==joint for p in removed[1:])
        if len(removed)>1 and parents[removed[0][0]]!=joint:
            assert len(removed[0])<len(removed[1])
        padded = [len(p) for p in removed]
        padded[-1] += k-1-sum(padded)
        steps.append((tuple(padded),removed))
    return parents,fixed,list(reversed(steps))


def replay(k, parents, fixed, steps, records, units):
    f = fixed.copy()+[None]*(len(parents)-len(fixed))
    vertices = counts(fixed,k)
    weights = counts((f[v]+f[p] for v,p in enumerate(parents[:len(fixed)]) if v),k)
    for key,removed in steps:
        assert balanced(vertices) and balanced(weights)
        if key is None:
            v, = removed[0]
            assert len(set(vertices))==1 and weights.count(min(weights))==1
            f[v] = (weights.index(min(weights))-f[parents[v]])%k
        elif k==4:
            rows,whole = records
            roots = tuple(f[parents[p[0]]] for p in removed)
            if key==(2,2):
                assert len(set(vertices))==1 and roots[0]==roots[1]
                digits = whole[roots[0],weights.index(min(weights))]
            else:
                assert len(set(weights))==1 and vertices.count(max(vertices))==1
                surplus = vertices.index(max(vertices))
                norm = tuple((x-surplus)%4 for x in roots)
                digits = [(surplus+x)%4 for x in rows[key,norm]]
            for v,x in zip((v for path in removed for v in path),digits):
                f[v] = x
        else:
            assert len(set(weights))==1 and vertices.count(max(vertices))==1
            surplus = vertices.index(max(vertices))
            roots = [f[parents[path[0]]] for path in removed]
            for row in records[key]:
                for unit in units:
                    i = 0
                    edges = []
                    for length,root in zip(key,roots):
                        old = (root-surplus)%k
                        for x in row[i:i+length]:
                            digit = (unit*x)%k
                            edges.append((digit+old)%k)
                            old = digit
                        i += length
                    if len(set(edges))==k-1:
                        break
                else:
                    continue
                break
            else:
                raise AssertionError((k,key,roots,surplus))
            i = 0
            for length,path in zip(key,removed):
                for v,x in zip(path,row[i:]):
                    f[v] = (unit*x+surplus)%k
                i += length
        for path in removed:
            for v in path:
                vertices[f[v]] += 1
                weights[(f[v]+f[parents[v]])%k] += 1
    assert f[:len(fixed)]==fixed and None not in f
    assert vertices==counts(f,k) and balanced(vertices)
    assert weights==counts((f[v]+f[p] for v,p in enumerate(parents) if v),k)
    assert balanced(weights)


def check(directory,k):
    rng = Random(199100+k)
    tests = [prepare(k,rng,i) for i in range(80)]
    if k==4:
        rows = four_certificates()
        for parents,fixed,steps in tests:
            replay(k,parents,fixed,steps,rows,[])
        return sum(len(steps) for _,_,steps in tests)
    requested = {key for _,_,steps in tests for key,_ in steps if key}
    records = defaultdict(list)
    with (directory/f'leg{k}').open() as rows:
        for line in rows:
            fields=line.split()
            size=int(fields[1])
            key=tuple(map(int,fields[2:2+size]))
            if key in requested:
                for word in fields[2+size:]:
                    records[key].append([ord(c)-ord('!') for c in word])
    units = [u for u in range(1,k) if gcd(k,u)==1]
    for parents,fixed,steps in tests:
        replay(k,parents,fixed,steps,records,units)
    return sum(len(steps) for _,_,steps in tests)


if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument('directory',type=Path)
    parser.add_argument('moduli',type=int,nargs='+')
    args = parser.parse_args()
    total = sum(check(args.directory,k) for k in args.moduli)
    print('fixed-core trees',80*len(args.moduli),'restored batches',total)

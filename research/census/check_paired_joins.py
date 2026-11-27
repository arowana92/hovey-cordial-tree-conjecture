"""Reconstruct both attached components and count the resulting label frequencies."""

from argparse import ArgumentParser
from itertools import product
from math import gcd
from pathlib import Path
from random import Random

N = 26
UNITS = [u for u in range(N) if gcd(u,N) == 1]
RESIDUES = set(range(N))
ORBITS = [{u*d%N for u in UNITS} for d in range(N)]


def decode(word):
    f = [ord(c)-ord('A') for c in word]
    assert len(f) == N and set(f) == RESIDUES
    return f


def arms(split, pattern):
    sides = []
    edges = []
    base = 0
    for start, stop in [(0,split),(split,12)]:
        sides.append(base)
        prev = None
        for i in range(start,stop):
            a,b = base,base+1
            edges.append((a,b))
            if prev is not None:
                edges.append((prev,a))
            prev = b if pattern & (1<<i) else a
            base += 2
        if prev is not None:
            edges.append((prev,base))
        base += 1
    assert base == N and len(edges) == N-2
    return edges,sides


def holes(f,edges):
    left = RESIDUES-{(f[i]+f[j])%N for i,j in edges}
    assert len(left) == 2
    return sorted(left)


def actual_join(records, edges, sides, parent, deficit):
    # Try the physical boundary weights after an affine change of the free labels.
    # Fixing the first bridge to a free-edge hole or to the core deficit fixes the shift.
    p,q = parent
    for f in records:
        a,b = (f[v] for v in sides)
        u,v = holes(f,edges)
        for scale in UNITS:
            for shift in (p+scale*(a-u),p+scale*(a-v),deficit-p-scale*a):
                joined = [(p+scale*a+shift)%N,(q+scale*b+shift)%N]
                free = [(scale*h+2*shift)%N for h in (u,v)]
                if sorted(joined)==sorted(free) or any(
                    sorted(joined)==sorted([deficit,h]) for h in free):
                    labels = [(scale*x+shift)%N for x in f]
                    counts = [1]*N
                    counts[deficit] -= 1
                    for i,j in edges:
                        counts[(labels[i]+labels[j])%N] += 1
                    for i,j in zip(parent,sides):
                        counts[(i+labels[j])%N] += 1
                    assert sorted(counts)==[1]+[2]*(N-1) and set(labels)==RESIDUES
                    return labels
    raise AssertionError((sides,parent,deficit))


def check_arms(path,rng):
    rows = 0
    with path.open() as source:
        for split,pat in product(range(7),range(4096)):
            s,mask,*words = next(source).split()
            assert (int(s),int(mask)) == (split,pat)
            edges,sides = arms(split,pat)
            records = [decode(w) for w in words]
            differences,sums = set(),set()
            for f in records:
                a,b = (f[v] for v in sides)
                u,v = holes(f,edges)
                for h,k in [(u,v),(v,u)]:
                    differences.update(ORBITS[(h-k-a+b)%N])
                    sums.update(ORBITS[(h-a-b)%N])
            assert differences==RESIDUES or sums==RESIDUES
            actual_join(records,edges,sides,[rng.randrange(N),rng.randrange(N)],rng.randrange(N))
            rows += len(records)
        assert not source.read()
    return rows


def ring(key):
    sites = key.split('.')
    c = len(sites)
    edges = [(i,(i+1)%c) for i in range(c)]
    next_id = c
    for i,site in enumerate(sites):
        stack = []
        for ch in site:
            if ch == '(':
                if stack:
                    edges.append((stack[-1],next_id))
                    stack.append(next_id)
                    next_id += 1
                else:
                    stack.append(i)
            else:
                stack.pop()
    assert next_id==len(edges)==N
    return c,edges


def possible_fake(edges,edge):
    remaining = RESIDUES-set(edge)
    adj = {v:set() for v in remaining}
    for i,j in edges:
        if i in adj and j in adj:
            adj[i].add(j)
            adj[j].add(i)
    while adj:
        a = next(v for v,hood in adj.items() if len(hood)<=1)
        if not adj[a]:
            return False
        b, = adj[a]
        for v in adj.pop(b):
            adj[v].discard(b)
        del adj[a]
    return True


def sample_whole_trees(path,rng):
    tested = 0
    with path.open() as source:
        for j,line in enumerate(source):
            if j>=12 and j%65537:
                continue
            key,*words = line.split()
            c,edges = ring(key)
            records = [decode(w) for w in words]
            mates = [i for i in range(c) if possible_fake(edges,edges[i])]
            for _ in range(12):
                fake = rng.choice(mates)
                close = rng.choice([i for i in range(c) if i!=fake])
                pieces = [edge for i,edge in enumerate(edges) if i not in (fake,close)]
                # A second copy cut at any edge is a bijectively labeled 26-vertex tree.
                base = rng.choice(records)
                cut = rng.randrange(N)
                core = edges[:cut]+edges[cut+1:]
                deficit = sum(base[v] for v in edges[cut])%N
                a,b = rng.sample(range(N),2)
                if base[a]%13==base[b]%13:
                    b = next(v for v in range(N) if base[a]%13!=base[v]%13)
                left,right = edges[close]
                f = actual_join(records,pieces,[left,right],[base[a],base[b]],deficit)
                tree = core+[(N+x,N+y) for x,y in pieces]+[(a,N+left),(b,N+right)]
                labels = base+f
                sums = [(labels[x]+labels[y])%N for x,y in tree]
                assert len(tree)==51 and all(labels.count(v)==2 for v in range(N))
                assert sorted(sums.count(v) for v in range(N))==[1]+[2]*25
                tested += 1
    return tested


if __name__ == '__main__':
    opt = ArgumentParser()
    opt.add_argument('directory',type=Path)
    out = opt.parse_args().directory
    rng = Random(521991)
    print('unbranched arm records',28672,'bijections',check_arms(out/'arms.out',rng))
    print('literal 52-vertex joins',sum(sample_whole_trees(out/f'socket{b}.txt',rng)
                                        for b in range(1,6)))

"""Construct complete three-arm trees and count their adjusted endpoint sums."""
import argparse
from collections import Counter
from functools import lru_cache
from math import gcd
from pathlib import Path
from random import Random

from .check_sparse_path_offsets import random_block

def lookup(directory, k):
    units = tuple(u for u in range(1,k) if gcd(u,k)==1)
    @lru_cache(None)
    def stream(name):
        return b'\n'+(directory/f'{name}.txt').read_bytes()

    def row(name, offsets):
        marks = [(i,b%k) for i,b in enumerate(offsets,1) if b%k]
        assert len(marks) <= 2
        (i,a),(j,b) = [(0,0)]*(2-len(marks))+marks
        x,y,u = min((a*u%k,b*u%k,u) for u in units)
        head = f'\n{i} {j} {x} {y} '.encode()
        data = stream(name)
        start = data.index(head)+len(head)
        end = data.index(b'\n',start)
        inv = pow(u,-1,k)
        return [int(v)*inv%k for v in data[start:end].split()]
    return row


def construct(lengths, offsets, row, visits, k):
    """Use original vertex IDs throughout, with 0 at the center."""
    arms = []
    next_id = 1
    for s in lengths:
        arms.append(list(range(next_id,next_id+s)))
        next_id += s

    def weight(u,v):
        return offsets.get(max(u,v),0)

    def short_path(path, adjustments):
        return dict(zip(path,row('path',adjustments)))

    def base(sides):
        sides = sorted((side for side in sides if side),key=len)
        if len(sides) < 3:
            if len(sides)<2:
                path = [0]+(sides[0] if sides else [])
            else:
                path = sides[0][::-1]+[0]+sides[1]
            return short_path(path,[weight(u,v) for u,v in zip(path,path[1:])])
        ids = [0]+[v for side in sides for v in side]
        lengths = [len(side) for side in sides]
        lengths[-1] += k-len(ids)
        name = '-'.join(map(str,lengths))
        shifts = [weight(u,v) for side in sides for u,v in zip([0]+side,side)]
        return dict(zip(ids,row(name,shifts)))

    def hole(labels, links):
        weights = {(labels[u]+labels[v]+c)%k for u,v,c in links}
        assert len(labels)==k and len(weights)==k-1
        missing, = set(range(k))-weights
        return missing

    def add_block(labels, block, u, v, boundary, missing):
        shift = labels[u]+block[v]+boundary-missing
        assert labels.keys().isdisjoint(block)
        labels.update((x,(y+shift)%k) for x,y in block.items())

    def path_blocks(path, shifts):
        sizes = [(len(path)-1)%k+1]+[k]*((len(path)-1)//k)
        used = sizes[0]
        labels = short_path(path[:used],shifts[:used-1])
        for size in sizes[1:]:
            vertices = path[used:used+size]
            internal = shifts[used:used+size-1]
            block = short_path(vertices,internal)
            missing = hole(block,zip(vertices,vertices[1:],internal))
            add_block(labels,block,path[used-1],vertices[0],shifts[used-1],missing)
            used += size
        return labels

    removed = []
    for side in arms:
        while len(side)>=k:
            segment = side[-k:]
            del side[-k:]
            removed.append((side[-1] if side else 0,segment))
    n = 1+sum(map(len,arms))
    if sum(bool(side) for side in arms)<3:
        visits['path'] += 1
        directions = [s for s in arms if s]+[[],[]]
        path = directions[0][::-1]+[0]+directions[1]
        labels = path_blocks(path,[weight(u,v) for u,v in zip(path,path[1:])])
    elif n<=k:
        visits['short claw'] += 1
        labels = base(arms)
    elif n==k+1:
        visits['one extra vertex'] += 1
        side = max(arms,key=len)
        leaf = side.pop()
        labels = base(arms)
        links = [(u,v,weight(u,v)) for s in arms for u,v in zip([0]+s,s)]
        missing = hole(labels,links)
        parent = side[-1] if side else 0
        labels[leaf] = (missing-labels[parent]-weight(parent,leaf))%k
    else:
        visits['two ports'] += 1
        keep = next((i for i,side in enumerate(arms) if any(offsets.get(v,0)%k for v in side)),0)
        a = arms[keep]
        b,c = [side for i,side in enumerate(arms) if i!=keep]
        x = min(len(b)-1,k-1-len(a))
        y = k-1-len(a)-x
        assert 0<=y<len(c)
        piece = [a,b[:x],c[:y]]
        block = base(piece)
        links = [(u,v,weight(u,v)) for s in piece for u,v in zip([0]+s,s)]
        missing = hole(block,links)
        p,r = (b[x-1] if x else 0),(c[y-1] if y else 0)
        left,right = b[x],c[y]
        offset = (block[p]+block[r]-missing+weight(p,left)+weight(r,right))%k
        path = b[x:][::-1]+c[y:]
        shifts = [offset if (u,v)==(left,right) else weight(u,v)
                  for u,v in zip(path,path[1:])]
        labels = path_blocks(path,shifts)
        add_block(labels,block,left,p,weight(p,left),missing)
        if p==r:
            visits['coincident ports'] += 1
    for u,segment in reversed(removed):
        visits['pendant period'] += 1
        shifts = [weight(x,y) for x,y in zip(segment,segment[1:])]
        block = short_path(segment,shifts)
        missing = hole(block,zip(segment,segment[1:],shifts))
        add_block(labels,block,u,segment[0],weight(u,segment[0]),missing)
    return labels


def check_expansions(row, rng, k):
    totals = Counter()
    for trial in range(120):
        sides = tuple(rng.randint(1,45) for _ in range(3))
        graph = []
        start = 1
        for s in sides:
            graph.extend(zip([0]+list(range(start,start+s-1)),range(start,start+s)))
            start += s
        first,second = rng.sample(graph,2)
        chains = {first:[random_block(k,rng) for _ in range(1+trial%3)],
                  second:[random_block(k,rng)]}
        effective = {v:sum(p+r-h for _,h,p,r in blocks)%k
                     for (u,v),blocks in chains.items()}
        labels = construct(sides,effective,row,Counter(),k)
        expanded = []
        for u,v in graph:
            for internal,hole,p,r in chains.get((u,v),()):
                base = len(labels)
                shift = labels[u]+p-hole
                labels.update((base+j,(j+shift)%k) for j in range(k))
                expanded.extend((base+x,base+y) for x,y in internal)
                expanded.append((u,base+p))
                u = base+r
                totals['pieces'] += 1
            expanded.append((u,v))
        assert len(expanded)==len(labels)-1
        hist = Counter((labels[u]+labels[v])%k for u,v in expanded)
        for counts in (Counter(labels.values()),hist):
            bins = [counts[j] for j in range(k)]
            assert max(bins)-min(bins)<=1
        totals['ordinary trees'] += 1
    print('expansions',dict(totals))


def replay(directory,k=27):
    row = lookup(directory,k)
    rng = Random(199127)
    visits = Counter()
    trials = 0
    lengths = [(1,1,1),(1,1,25),(2,10,15),(1,26,26),(26,26,26),
               (27,54,81),(28,54,3),(1,27,26),(25,26,79),(52,1,1)]
    lengths += [tuple(rng.randint(1,100) for _ in range(3)) for _ in range(120)]
    for sides in lengths:
        n = 1+sum(sides)
        edges = []
        start = 1
        for s in sides:
            edges.append((0,start))
            edges.extend((v,v+1) for v in range(start,start+s-1))
            start += s
        for j in range(12):
            exceptional = rng.sample(range(1,n),j%3)
            offsets = {v:rng.randrange(1,k) for v in exceptional}
            labels = construct(sides,offsets,row,visits,k)
            assert set(labels)==set(range(n))
            vertices = Counter(labels.values())
            sums = Counter((labels[u]+labels[v]+offsets.get(v,0))%k for u,v in edges)
            for hist in (vertices,sums):
                bins = [hist[c] for c in range(k)]
                assert max(bins)-min(bins)<=1
            trials += 1
    if k==27:
        assert all(visits[key] for key in ('path','short claw','one extra vertex','two ports',
                                          'coincident ports','pendant period'))
    print('whole trees',trials,'construction cases',dict(visits))
    check_expansions(row,rng,k)


if __name__=='__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('directory',type=Path)
    cli.add_argument('--modulus',type=int,default=27)
    args = cli.parse_args()
    replay(args.directory,args.modulus)

"""Rebuild entire trees from a short-forest stream and a fixed cordial core."""

from argparse import ArgumentParser
from collections import Counter
from math import gcd
from pathlib import Path
from random import Random
from struct import unpack


def decode_tree(word,mass):
    stack=[]
    parents=[]
    roots=[]
    for token in format(word,'b'):
        if token=='1':
            if not stack:
                roots.append(len(parents))
            parents.append(stack[-1] if stack else -1)
            stack.append(len(parents)-1)
        else:
            stack.pop()
    assert not stack and len(parents)==mass and word.bit_length()==2*mass
    return parents,roots


def whole_tree(k,parents,roots,colors,word_rows,rng,periods):
    mass=len(parents)
    count=periods*k+1
    if periods%2:
        base=[(i//2+(i%2)*((count+1)//2))%k for i in range(count)]
        edges=[(i-1,i) for i in range(1,count)]
    else:
        base=[i%k for i in range(count)]
        edges=[(0,i) for i in range(1,count)]
    boundary=dict(zip(roots,colors))
    for word in word_rows:
        for u in range(1,k):
            if gcd(u,k)>1:
                continue
            f=[u*x%k for x in word]
            weights=[(x+(f[p] if p>=0 else boundary[i]))%k for i,(x,p) in enumerate(zip(f,parents))]
            if len(set(weights))==mass:
                break
        else:
            continue
        break
    else:
        raise AssertionError((parents,colors))
    assert len(set(f))==mass and 0 not in f
    for i,p in enumerate(parents):
        if p<0:
            old=rng.choice([v for v in range(count) if base[v]==boundary[i]])
        else:
            old=count+p
        assert old<count+i
        edges.append((old,count+i))
    shift=rng.randrange(k)
    labels=[(x+shift)%k for x in base+f]
    vertex=Counter(labels)
    edge=Counter((labels[x]+labels[y])%k for x,y in edges)
    assert len(edges)==len(labels)-1
    for histogram in (vertex,edge):
        bins=[histogram[x] for x in range(k)]
        assert max(bins)-min(bins)<=1


def replay(path):
    rng=Random(261991)
    run_counts=set()
    trials=0
    with path.open('rb') as source:
        assert source.read(4)==b'SPN3'
        k,mass=source.read(2)
        for record in range(160000):
            header=source.read(12)
            if not header:
                break
            word,rows=unpack('<QI',header)
            force=record<5 or record%8191==0
            if not force and len(run_counts)==4:
                source.seek(mass*rows,1)
                continue
            parents,roots=decode_tree(word,mass)
            colors=[]
            last=None
            runs=0
            total=0
            for a,b in zip(roots,roots[1:]+[mass]):
                if b-a>=total+runs:
                    last=rng.randrange(k) if last is None else (last+rng.randrange(1,k))%k
                    runs+=1
                colors.append(last)
                total+=b-a
            if not force and runs in run_counts:
                source.seek(mass*rows,1)
                continue
            raw=source.read(mass*rows)
            assert raw and len(raw)==mass*rows
            words=[raw[i:i+mass] for i in range(0,len(raw),mass)]
            run_counts.add(runs)
            for periods,pattern in enumerate(([0]*len(roots),colors,[rng.randrange(k)]*len(roots)),1):
                whole_tree(k,parents,roots,pattern,words,rng,periods)
                trials+=1
    return trials,sorted(run_counts)


if __name__=='__main__':
    parser=ArgumentParser()
    parser.add_argument('streams',type=Path,nargs='+')
    for stream in parser.parse_args().streams:
        tests,runs=replay(stream)
        print(stream.name,'whole trees',tests,'sampled boundary run counts',runs)

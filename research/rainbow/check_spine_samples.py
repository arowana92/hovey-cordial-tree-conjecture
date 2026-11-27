"""Independently cover sampled SPN2 records by excluding pairwise collisions."""

import argparse
from functools import lru_cache
from itertools import combinations, product
from math import gcd
import mmap
from pathlib import Path
import struct


def parse(k,word,n=None):
    if n is None:
        n=k-1
    assert word.bit_length()==2*n
    stack,parents,roots=[],[],[]
    for bit in f"{word:b}":
        if bit=="1":
            if not stack:
                roots.append(len(parents))
            parents.append(stack[-1] if stack else -1)
            stack.append(len(parents)-1)
        else:
            stack.pop()
    assert not stack and len(parents)==n
    sizes=tuple(b-a for a,b in zip(roots,roots[1:]+[n]))
    active=3*(n-len(set(parents)-{-1}))<=2*(k-2)
    return parents,roots,sizes,active


@lru_cache(None)
def profiles(k,sizes,active):
    # Enumerate actual color changes, then independent colors for the runs.
    allowed=set()
    for subset in range(1<<(len(sizes)-1)) if active else [0]:
        cuts=[j+1 for j in range(len(sizes)-1) if subset>>j&1]
        if any(sizes[j]<sum(sizes[:j])+t for t,j in enumerate(cuts,1)):
            continue
        levels=[sum(i>=j for j in cuts) for i in range(len(sizes))]
        for seq in product(range(k) if active else [0],repeat=len(cuts)+1):
            if any(a==b for a,b in zip(seq,seq[1:])):
                continue
            # Groups separated by size gaps. Change subsets above used every
            # position and never assumed that this compression was sufficient.
            allowed.add(tuple(seq[level] for i,level in enumerate(levels)
                              if sizes[i]>sum(sizes[:i])))
    return sorted(allowed)


def direct(k,parents,roots,sizes,active,payload):
    colors=profiles(k,sizes,active)
    groups=len(colors[0])
    pos={c:i for i,c in enumerate(colors)}
    units=[u for u in range(1,k) if gcd(u,k)==1]
    N=len(colors)
    full=(1<<N)-1
    bins=[[bytearray((N+7)//8) for _ in range(k)] for _ in range(groups)]
    for i,colors_at_root in enumerate(colors):
        for j,value in enumerate(colors_at_root):
            bins[j][value][i//8] |= 1<<(i%8)
    bins=[[int.from_bytes(b,"little") for b in row] for row in bins]
    group_at=[]
    mass=0
    group=-1
    for size in sizes:
        if size>mass:
            group+=1
        group_at.append(group)
        mass+=size
    by_group=[[v for v,g in zip(roots,group_at) if g==j] for j in range(groups)]
    diff={}
    for j,h in combinations(range(groups),2):
        for d in range(k):
            mask=0
            for b in range(k):
                mask |= bins[j][(b+d)%k]&bins[h][b]
            diff[j,h,d]=mask
    hit=0
    options=set(range(1,k))
    for row in struct.iter_unpack(f"{len(parents)}B",payload):
        assert len(set(row))==len(parents) and set(row)<=options
        inside=[(row[u]+row[v])%k for u,v in enumerate(parents) if v>=0]
        internal=set(inside)
        assert len(internal)==len(inside)
        good=full
        for j,verts in enumerate(by_group):
            blocked={ (w-row[v])%k for w in internal for v in verts }
            mask=0
            for b in range(k):
                if b not in blocked:
                    mask |= bins[j][b]
            good &=mask
        for j,h in combinations(range(groups),2):
            for a in by_group[j]:
                for b in by_group[h]:
                    good &= ~diff[j,h,(row[b]-row[a])%k]
        hit |= good
    bits=hit.to_bytes((N+7)//8,"little")
    seen=set()
    for i,c in enumerate(colors):
        if bits[i//8]>>(i%8)&1:
            seen.update(pos[tuple((u*b)%k for b in c)] for u in units)
    assert len(seen)==N,"sampled forest is missing a required input"
    return N


def scan(path,stride):
    with path.open("rb") as f, mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as data:
        assert data[:4] in (b"SPN2",b"SPN3")
        k=data[4]
        partial=data[:4]==b"SPN3"
        mass=data[5] if partial else k-1
        offset=6 if partial else 5
        index=checked=rows=N=0
        types=set()
        # A first run needs one vertex. A new run needs at least
        # the previous mass plus the previous number of runs.
        min_mass=max_runs=1
        while 2*min_mass+max_runs<=mass:
            min_mass=2*min_mass+max_runs
            max_runs+=1
        while offset<len(data):
            word,length=struct.unpack_from("<QI",data,offset)
            start=offset+12;offset=start+mass*length
            assert offset<=len(data)
            # Sample the file throughout and deliberately include each possible
            # run count, so the deepest boundary test is represented.
            if index%stride==0 or any(r not in types for r in range(1,max_runs+1)) or (not partial and 0 not in types):
                parents,roots,sizes,active=parse(k,word,mass)
                runs=int(active)
                for i,s in enumerate(sizes[1:],1):
                    if active and s>=sum(sizes[:i])+runs:
                        runs+=1
                if index%stride==0 or runs not in types:
                    types.add(runs)
                    N+=direct(k,parents,roots,sizes,active,data[start:offset])
                    checked+=1;rows+=length
            index+=1
    print(f"k={k} file records={index} sampled={checked} witnesses={rows} "
          f"sampled boundary inputs={N} run counts={sorted(types)}")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("shard",type=Path)
    parser.add_argument("--stride",type=int,default=50000)
    args=parser.parse_args()
    if args.stride < 1:
        parser.error("--stride must be positive")
    scan(args.shard,args.stride)

"""Verify the finite five-arm bounds and the connector bounds on integer masses."""

from argparse import ArgumentParser
from itertools import combinations_with_replacement
from pathlib import Path
from random import Random
from math import comb


def allocations(slots, total):
    if slots == 0:
        yield ()
        return
    for first in range(total+1):
        for tail in allocations(slots-1,total-first):
            yield (first,)+tail


def five_arms(side):
    # Sort lengths, but allow every placement of the budget on the named arms.
    feasible = list(allocations(5,side))
    pairs = [(i,j) for i in range(5) for j in range(i)]
    permitted = set()
    for costs in feasible:
        permitted.add(sum(1<<z for z,(i,j) in enumerate(pairs) if costs[i]+costs[j]>2))
    best = 0
    for a in combinations_with_replacement(range(12-side),5):
        need = sum(1<<z for z,(i,j) in enumerate(pairs) if a[i]+a[j]>=12)
        if any(need & ~mask == 0 for mask in permitted):
            best=max(best,sum(a))
    return best


def connectors():
    # Bit j remembers a cut boundary j units behind the current one.
    # The two endpoints of a mass-13 window with at least six intermediate
    # boundaries use at most six side pairs. Such a window is reducible.
    maxima = [0]+[-1]*11
    population = [bin(i).count("1") for i in range(4096)]
    for forbidden in range(1,13):
        states = {(1,0)}
        for mass in range(1,37):
            following = set()
            for recent,side in states:
                shifted=(recent<<1)&8191
                if side<11:
                    following.add((shifted,side+1))
                if mass%13==forbidden:
                    continue
                if recent & 4096 and population[recent & 4095]>=6:
                    continue
                following.add((shifted+1,side))
                maxima[side]=max(maxima[side],mass-side)
            states=following
    return maxima


def check_windows():
    # A group of thirteen positions has masses between 13 and 25. Enumerate
    # its twelve interior boundaries via the standard next-combination operation.
    cases=0
    for mass in range(13,26):
        interior=(1<<12)-1
        limit=1<<(mass-1)
        subtotal=0
        while interior<limit:
            cuts=1|(interior<<1)|(1<<mass)
            assert cuts & (cuts>>13)
            subtotal+=1
            bit=interior & -interior
            following=interior+bit
            interior=following+((following^interior)//bit>>2)
        assert subtotal==comb(mass-1,12)
        cases+=subtotal
    return cases


def neutral_joins(directory,sides):
    from .check_paired_joins import UNITS, decode, possible_fake, ring

    rng=Random(26505)
    tested=0
    for side in range(1,sides+1):
        stride=2027 if side<=2 else 131071
        with (directory/f'allneutral{side}').open() as source:
            for index,line in enumerate(source):
                if index>7 and index%stride:
                    continue
                key,*words=line.split()
                if not words:
                    continue
                c,edges=ring(key)
                fake=rng.choice([j for j in range(c) if possible_fake(edges,edges[j])])
                close=rng.choice([j for j in range(c) if j!=fake])
                pieces=[e for j,e in enumerate(edges) if j not in (fake,close)]
                left,right=edges[close]
                for n,diff in ((26,0),(27,13),(51,2),(53,1)):
                    base=[(v//2+(v%2)*((n+1)//2))%26 for v in range(n)]
                    first=rng.randrange(n)
                    target=(base[first]+diff)%26
                    second=base.index(target)
                    for word in words:
                        f=decode(word)
                        for unit in UNITS:
                            for t in range(26):
                                z=[(unit*x+t)%26 for x in f]
                                added=[(z[x]+z[y])%26 for x,y in pieces]
                                added.extend(((base[first]+z[left])%26,(base[second]+z[right])%26))
                                if len(set(added))==26:
                                    break
                            else:
                                continue
                            break
                        else:
                            continue
                        break
                    else:
                        raise AssertionError((side,key,first,second))
                    tree=[(i-1,i) for i in range(1,n)]+[(x+n,y+n) for x,y in pieces]
                    tree.extend(((first,n+left),(second,n+right)))
                    labels=base+z
                    weights=[(labels[x]+labels[y])%26 for x,y in tree]
                    old=[(base[i]+base[i-1])%26 for i in range(1,n)]
                    for i in range(26):
                        assert labels.count(i)==base.count(i)+1
                        assert weights.count(i)==old.count(i)+1
                    tested+=1
    return tested


if __name__=='__main__':
    parser=ArgumentParser()
    parser.add_argument('--directory',type=Path)
    parser.add_argument('--sides',type=int,choices=range(1,7),default=2)
    args=parser.parse_args()
    arms=[five_arms(h) for h in range(12)]
    maxima=connectors()
    bounds=[]
    for h in range(12):
        lengths=max(maxima[a]+maxima[b] for a in range(h+1) for b in range(h-a+1))
        bounds.append(arms[h]+3+h+lengths)
    assert maxima==[11,11,10,11,11,11,11,17,23,23,23,23]
    assert max(bounds)<62
    print('thirteen-position windows',check_windows())
    print('five-arm totals',arms)
    print('connector maxima',maxima)
    print('matching-size upper bounds at deficiency five',bounds)
    if args.directory:
        print('literal uniform joins',neutral_joins(args.directory,args.sides))

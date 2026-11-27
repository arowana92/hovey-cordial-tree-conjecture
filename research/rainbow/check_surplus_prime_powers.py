"""Check prime-power two-star witnesses against actual tree edges at each step."""
from math import gcd
from random import Random
from subprocess import check_output
import sys

from .check_two_star_surplus import literal
from .surplus_prime_powers import full, grow, obstruction


def replay(k,s,t,a,b,surplus,steps):
    labels = [surplus]+list(range(k))
    edges = [(0,j) for j in range(1,k+1)]
    vertex,weight = [0]*k,[0]*k
    for v in labels:
        vertex[v] += 1
    for v,w in edges:
        weight[(labels[v]+labels[w])%k] += 1
    centers = [None,None]
    sizes = [0,0]
    for side,z in steps:
        parent = centers[side]
        if parent is None:
            parent = 1+(a,b)[side]
            centers[side] = len(labels)
        edges.append((parent,len(labels)))
        labels.append(z)
        vertex[z] += 1
        weight[(labels[parent]+z)%k] += 1
        assert max(weight)-min(weight)<=1 and max(vertex)-min(vertex)<=1
        sizes[side] += 1
    assert sizes==[s,t]


def whole(k,s,a,b,parts):
    assert [len(side) for side in parts]==[s,k-1-s]
    assert set(parts[0]+parts[1])==set(range(1,k))
    sums = [(old+side[0])%k for old,side in zip((a,b),parts)]
    sums.extend((side[0]+v)%k for side in parts for v in side[1:])
    assert len(set(sums))==k-1


def main(checker):
    endpoint = absent = small = samples = prefixes = orders = 0
    for k in (3,4,5,7,8,9,16,25,27,32,49):
        rows = check_output([checker,str(k)],text=True).splitlines()
        assert len(rows)==k*k
        for row in rows:
            a,b,mask = map(int,row.split())
            for s in range(1,k-1):
                result = full(k,s,a,b)
                success = bool(mask & (1<<s))
                assert success==(result is not None)==(not obstruction(k,s,a,b))
                if success:
                    whole(k,s,a,b,result)
                else:
                    absent += 1
                if k<=9:
                    assert literal(k,s,a,b)==success
                    small += 1
                endpoint += 1
    rng = Random(281991)
    for k in (2,3,4,5,8,9,16,25,27,32,49,64,81,125,128,243,256,343,512,625,729,1024):
        for _ in range(100):
            if k>=4:
                # Concentrate on parent differences of small order and star orders
                # divisible by that order or one short of a multiple.
                factors = [j for j in range(2,k+1) if k%j==0]
                m = rng.choice(factors)
                h = (k//m)*rng.choice([j for j in range(1,m) if gcd(j,m)==1])
                idx = k//m
                a = (idx*rng.randrange(m) if rng.randrange(2) else rng.randrange(k))
                b = (a-h)%k
                s = rng.randrange(1,k//m+1)*m-rng.randrange(2)
                if 1<=s<=k-2:
                    result = full(k,s,a,b)
                    assert (result is None)==obstruction(k,s,a,b)
                    if result is not None:
                        whole(k,s,a,b,result)
                    samples += 1
        for _ in range(18):
            sizes = [(1,max(1,k-2)),(1,k),(2,max(1,k-3)),
                     (rng.randrange(1,2*k),rng.randrange(1,2*k))]
            u = rng.randrange(k)
            for s,t in sizes:
                a,b = (u,(u+1)%k) if rng.randrange(2) else (rng.randrange(k),rng.randrange(k))
                if rng.randrange(2):
                    s,t,a,b = t,s,b,a
                steps = grow(k,s,t,a,b,u)
                if steps is None:
                    assert s+t==k-1 and obstruction(k,s,(a-u)%k,(b-u)%k)
                else:
                    replay(k,s,t,a,b,u,steps)
                    prefixes += len(steps)
                orders += 1
    print('independent endpoint decisions',endpoint,'exceptions',absent,'literal inputs',small)
    print('larger packet cases',samples,'attachment orders',orders,'recounted prefixes',prefixes)


if __name__=='__main__':
    main(sys.argv[1])

"""Check prescribed surplus/mark pairs, joined histograms and the unit graph bound."""

from itertools import combinations
from math import gcd
from random import Random

from .prescribed_path_surplus import least_prime,prescribe


def bins(vals,k):
    row = [0]*k
    for v in vals:
        row[v%k] += 1
    return row


def validate(k,a,b,x,y):
    row = prescribe(k,a,b,x,y)
    q = (a+b)//k
    assert len(row)==a+b+1 and row[a]==y
    assert bins(row,k) == [q+int(i==x) for i in range(k)]
    assert bins((u+v for u,v in zip(row,row[1:])),k) == [q]*k
    return row


def paths():
    rng = Random(19911952)
    count = 0
    for k in range(3,74,2):
        for a in range(k+1):
            for d in range(k):
                validate(k,a,k-a,0,d)
                count += 1
    for _ in range(6000):
        k = rng.randint(2,90)
        p = least_prime(k)
        q = (12*(k//p)+12+k-1)//k+rng.randrange(5)
        if k%2:
            q = rng.randrange(1,7)
        total = q*k
        a = rng.randrange(total+1)
        validate(k,a,total-a,rng.randrange(k),rng.randrange(k))
        count += 1
    return count


def graph():
    checked = 0
    for k in range(3,26,2):
        p = least_prime(k)
        size = k//p
        adj = [sum(1<<j for j in range(k) if gcd(j-i,k)==1) for i in range(k)]
        for A in combinations(range(k),size):
            neighbors = 0
            for i in A:
                neighbors |= adj[i]
            assert k-bin(neighbors).count('1') <= size
            checked += 1
    return checked


def join():
    rng = Random(199113)
    for _ in range(2000):
        k = rng.choice(range(3,50,2))
        n = rng.randrange(1,4*k+1)
        labels = [i%k for i in range(n)]
        weights = [i%k for i in range(n-1)]
        rng.shuffle(labels)
        rng.shuffle(weights)
        old = []
        for v,w in enumerate(weights,1):
            u=rng.randrange(v)
            old.append((u,v,w-labels[u]-labels[v]))
        vh,eh = bins(labels,k),bins(weights,k)
        csite = rng.randrange(n)
        offset = rng.randrange(k)
        x = min(range(k),key=vh.__getitem__)
        y = min(range(k),key=eh.__getitem__)
        total = rng.randrange(1,5)*k
        a = rng.randrange(total+1)
        block = validate(k,a,total-a,x,(y-offset-labels[csite])%k)
        full = labels+block
        edges = old+[(csite,n+a,offset)]+[(n+i-1,n+i,0) for i in range(1,len(block))]
        for h in (bins(full,k),bins((full[u]+full[v]+b for u,v,b in edges),k)):
            assert max(h)-min(h)<=1
    return 2000


def quotient_trees():
    rng = Random(5826777)
    for _ in range(400):
        k = rng.choice(range(3,42,2))
        pieces = rng.randrange(2,3*k+1)
        labels,edges,locations = [],[],[]
        for v in range(pieces):
            total = rng.randrange(1,4)*k
            mark = rng.randrange(total+1)
            target = v%k
            if v:
                u = rng.choice(locations)
                site = rng.randrange(*u)
                bias = rng.randrange(k)
                weight = (v-1)%k
                port = (weight-labels[site]-bias)%k
                edges.append((site,len(labels)+mark,bias))
            else:
                port = rng.randrange(k)
            start = len(labels)
            labels.extend(prescribe(k,mark,total-mark,target,port))
            locations.append((start,len(labels)))
            edges.extend((i-1,i,0) for i in range(start+1,len(labels)))
        for h in (bins(labels,k),bins((labels[i]+labels[j]+b for i,j,b in edges),k)):
            assert max(h)-min(h)<=1
    return 400


if __name__=='__main__':
    print(f'{paths()} prescribed path pairs verified directly')
    print(f'{graph()} unit-graph neighbor sets verified directly')
    print(f'{join()} joins verified on complete trees')
    print(f'{quotient_trees()} trees of path pieces checked')

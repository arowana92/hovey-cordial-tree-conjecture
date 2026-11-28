"""Verify every interval input and reconstruct concrete 52-vertex trees."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import product
from math import gcd
from pathlib import Path

K = 27
BIN = [1 << (8*i) for i in range(K)]


def maps(row):
    swap, u, d, e = row[:4]
    assert swap in (0,1) and 0 < u < K and gcd(u,K)==1 and max(row[2:]) < K
    return ((u,e),(1,d)) if swap else ((1,d),(u,e))


def check_stream(shape, data):
    assert len(data) == 7*K**4
    vertices, edges = {}, {}
    for u in range(1,K):
        if gcd(u,K) != 1:
            continue
        for d in range(K):
            vertices[u,d] = sum(BIN[(u*x+d)%K] for x in range(24))
            for f in range(K):
                edges[u,d,f] = sum(BIN[(u*w+2*d)%K] for w in range(f,f+23))

    for i,(a,f,b,g) in enumerate(product(range(K),repeat=4)):
        row = data[7*i:7*i+7]
        (u,d),(v,e) = maps(row)
        x,y,z = row[4:]
        vertex = vertices[u,d]+vertices[v,e]+BIN[0]+BIN[x]+BIN[y]+BIN[z]
        weights = edges[u,d,f]+edges[v,e,g]+BIN[(u*a+d)%K]+BIN[(v*b+e)%K]
        last_parent = x if shape=='fork' else y
        weights += BIN[x]+BIN[(x+y)%K]+BIN[(last_parent+z)%K]
        # Each base-256 digit is a literal frequency. All 27 bins are present.
        for histogram in (vertex,weights):
            counts = histogram.to_bytes(K,'little')
            assert min(counts)==1 and max(counts)==2, (shape,a,f,b,g,row)
    return K**4


def piece(start):
    # Use integer vertex labels as vertex IDs. Monotone steps give consecutive sums.
    i,j = 0,start
    tree = [(i,j)]
    while i+1<start or j<23:
        if i+1<start:
            i += 1
            tree.append((i,j))
        if j<23:
            j += 1
            tree.append((i,j))
    assert len(tree)==23 and {a+b for a,b in tree}==set(range(start,start+23))
    return tree


def join_samples(shape,data):
    trees = {f:piece(f) for f in (1,5,12)}
    checked = 0
    for f,left in trees.items():
        for g,right in trees.items():
            for a,b in product(range(24),repeat=2):
                i = ((a*K+f)*K+b)*K+g
                row = data[7*i:7*i+7]
                labels = [0,*row[4:]]
                joined = [(0,1),(1,2),(1 if shape=='fork' else 2,3)]
                for root,tree,(u,d) in zip((a,b),(left,right),maps(row)):
                    offset = len(labels)
                    labels.extend((u*j+d)%K for j in range(24))
                    joined.extend((offset+i,offset+j) for i,j in tree)
                    joined.append((0,offset+root))
                assert len(labels)==52 and len(joined)==51
                for hist in (Counter(labels), Counter((labels[i]+labels[j])%K for i,j in joined)):
                    assert all(1 <= hist[k] <= 2 for k in range(K))
                checked += 1
    return checked


if __name__ == '__main__':
    cli = ArgumentParser(description=__doc__)
    cli.add_argument('shape',choices=('path','fork'))
    cli.add_argument('stream',type=Path)
    args = cli.parse_args()
    raw = args.stream.read_bytes()
    rows = check_stream(args.shape,raw)
    actual = join_samples(args.shape,raw)
    print(args.shape,'interval cases',rows,'whole trees',actual,'sha256',sha256(raw).hexdigest())

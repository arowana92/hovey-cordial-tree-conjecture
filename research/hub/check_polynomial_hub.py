"""Audit integer certificates and the modular consequences using the original edges."""

from collections import Counter
from itertools import product
from random import Random

from research.hub.polynomial_hub import DEPTH, construct, first_layer, seed
from research.rainbow.verify import rooted_shapes


def certificate(tree, labels, gap):
    assert labels[0] == 0 and len(set(labels)) == len(tree) == len(labels)
    edges = Counter(labels[v]+labels[p] for v,p in enumerate(tree) if v)
    edges[gap] += 1
    assert edges == Counter(labels)


def audit_seed(tree):
    labels,(blocks,subs) = seed(tree,DEPTH,Random(31))
    assert len(set(labels.values()))==len(labels)
    weights=Counter()
    for v in labels:
        if v:
            assert tree[v] in labels
            weights[labels[v]+labels[tree[v]]] += 1
    weights[0] += 1
    assert weights==Counter(labels.values())
    assert max(map(abs,labels.values())) <= 4096*(len(tree)+1)
    return blocks,subs


def sequence_checks():
    total=0
    for n in range(6):
        for jumps in product((-2,-1,0,1,2),repeat=n):
            tree=[-1,0,0,0,0]
            labels={0:0,1:1,2:-1,3:2,4:-2}
            idx={x:v for v,x in labels.items()}
            tree.extend(idx[x] for x in jumps)
            layer=list(range(5,len(tree)))
            a,b,_=first_layer(layer,tree,labels)
            tails=Counter(labels[v] for v in layer)
            heads=Counter(labels[v]+labels[tree[v]] for v in layer)
            heads[a]+=1
            tails[b]+=1
            assert heads==tails and len(set(labels.values()))==len(labels) and b>max(labels.values())
            total+=1
    return total


def fixture(kind,stem, rng):
    tree=[-1]+list(range(stem))
    boundary=len(tree)-1
    def child(p):
        tree.append(p)
        return len(tree)-1
    # Sides at intermediate heights make the layer parents include negative and positive labels.
    for pos in range(6,stem-10,31):
        for _ in range(1+rng.randrange(3)):
            p=pos
            for _ in range(1+rng.randrange(12)):
                p=child(p)
    if kind=='arms':
        for i in range(3):
            a=child(boundary)
            b=child(a)
            for _ in range(i+1):
                child(b)
            for _ in range(i):
                child(a)
    else:
        a=child(boundary)
        b=child(a)
        c=child(b)
        child(c)
        for _ in range(4 if kind=='path-c' else 1):
            child(b)
        for _ in range(2):
            child(c)
    return tree


def main():
    rng=Random(20261127)
    kinds=Counter()
    tall=0
    for n in range(1,12):
        for tree in rooted_shapes(n).values():
            x,g,stats=construct(tree)
            certificate(tree,x,g)
            kinds[stats[0]]+=1
    totals=[0,0,0]
    for kind in ('arms','path-b','path-c'):
        for stem in (17,65,431,467,807,1493):
            tree=fixture(kind,stem,rng)
            x,g,stats=construct(tree)
            certificate(tree,x,g)
            assert stats[0]==kind
            assert max(x)-min(x) <= 2**20*(len(tree)+1)**435
            kinds[kind]+=1
            for i in range(3):
                totals[i]+=stats[i+1]
            tall=max(tall,len(tree))
    multi=[-1]
    for j in range(9):
        p=0
        for i in range(600+7*j):
            multi.append(p)
            p=len(multi)-1
            if i in (20,164,290):multi.append(p)
    b,s=audit_seed(multi)
    assert b>0 and s>0
    x,g,stats=construct(multi)
    certificate(multi,x,g)
    random_trees = 0
    for _ in range(75):
        n = rng.randrange(30,400)
        stem = rng.randrange(15,n)
        tree = [-1]+list(range(stem-1))
        while len(tree)<n:
            tree.append(rng.randrange(len(tree)))
        x,g,_ = construct(tree)
        certificate(tree,x,g)
        random_trees += 1
    # Inspect both full histograms, including empty bins, at every leaf count.
    tree = [-1]+list(range(14))
    x,g,_ = construct(tree)
    span = max(x)-min(x)
    for k in range(span+1,span+9):
        core = {z%k for z in x}
        period = [z for z in range(k) if z not in core]+[g%k]+sorted(core-{g%k})
        assert len(set(period))==k
        vertices = [0]*k
        edges = [0]*k
        for i,p in enumerate(tree):
            vertices[x[i]%k] += 1
            if i:
                edges[(x[i]+x[p])%k] += 1
        for z in period*2:
            vertices[z] += 1
            edges[(z+x[0])%k] += 1
            assert max(vertices)-min(vertices)<=1 and max(edges)-min(edges)<=1
    print(f"{sum(kinds.values()):,} integer certificates by rooted shape or fringe: {dict(kinds)}.")
    print(f"Tall fringe replays through order {tall:,}: {totals}. "
          f"Separate {len(multi):,}-vertex host: {b} transfers, {s} neutral subdivisions.")
    print(f"{sequence_checks():,} signed first layers; {random_trees} random rooted trees; two full periods at moduli {span+1}–{span+8}.")


if __name__=='__main__':
    main()

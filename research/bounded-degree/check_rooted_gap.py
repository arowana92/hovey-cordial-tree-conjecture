"""Recount the two target moments and verify the original rooted tree and moved edges."""
from collections import Counter
from functools import reduce
from math import gcd
from itertools import permutations
from pathlib import Path
import sys
from random import Random

from check import adjacency
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"census"))
from few_leaf_rings import trees as rooted_words
from rooted_gap import build


def verify(k,original,root,gap,result):
    tree,labels = result
    adj = adjacency(k,tree)
    seen,stack = {root},[root]
    while stack:
        v = stack.pop()
        for u in adj[v]-seen:
            stack.append(u)
            seen.add(u)
    assert len(seen)==k and len(tree)==k-1
    assert labels[root]==0 and set(labels.values())<=set(range(k)) and len(labels)==len(set(labels.values()))
    assert (sum(labels.values())-sum(range(k)))%k==0
    assert (sum(len(adj[v])*x for v,x in labels.items())+gap-sum(range(k)))%k==0
    weights = [(labels[a]+labels[b])%k for a,b in tree if a in labels and b in labels]
    assert len(set(weights))==len(weights) and gap not in weights
    for d,total in Counter(map(len,adj)).items():
        count = sum(len(adj[v])==d for v in labels)
        assert total==count or min(count,total-count)>=6
    old,new = {frozenset(e) for e in original},{frozenset(e) for e in tree}
    assert Counter((labels[a]+labels[b])%k for a,b in old-new)==Counter(
        (labels[a]+labels[b])%k for a,b in new-old)


def eight():
    words = {w for m in range(1,8) for w in rooted_words(8,m)}
    assert len(words)==115
    solutions = extra = zero = 0
    for w in words:
        parent,stack = [],[]
        for token in w:
            if token=='(':
                parent.append(stack[-1] if stack else -1)
                stack.append(len(parent)-1)
            else: stack.pop()
        gaps = set()
        for seq in permutations(range(1,8)):
            x = (0,)+seq
            weights = {(x[v]+x[parent[v]])%8 for v in range(1,8)}
            if len(weights)==7:
                gap, = set(range(8))-weights
                gaps.add(gap)
        degrees = [parent.count(i)+(i!=0) for i in range(8)]
        h = reduce(gcd,(d-1 for d in degrees[1:]),8)
        possible = set(range(0,8,h))
        if max(degrees)==2 and degrees[0]==1: possible.discard(4)
        assert gaps<=possible
        solutions += len(gaps)
        extra += len(possible-gaps)
        zero += 0 in gaps
    return solutions,extra,zero


def main():
    rng = Random(994261)
    yes = no = max_degree = 0
    for k in (504,729,1024,1350,1601):
        binary = [((v-1)//2,v) for v in range(1,k)]
        path = [(v-1,v) for v in range(1,k)]
        decorated = [(v-1,v) for v in range(1,k-56)]+[(2+(v%2),v) for v in range(k-56,k)]
        trees = [(binary,3),(path,3),(decorated,4)]
        # A full unrooted binary tree, with no degree-two vertex.
        if k%2==0:
            n = k//2-1
            full = [(v-1,v) for v in range(1,n)]
            v = n
            for j in range(n):
                for _ in range(1+(j in (0,n-1))):
                    full.append((j,v))
                    v += 1
            trees.append((full,3))
        # Subdivide one edge of a full degree-four tree. At the subdivision
        # root the gcd is three, while at other roots it can be one.
        if k%3==0:
            n = (k-3)//3
            base = [(v-1,v) for v in range(1,n)]
            tip = n
            for j in range(n):
                for _ in range(2+(j in (0,n-1))):
                    base.append((j,tip))
                    tip += 1
            assert tip==k-1
            a,b = base.pop(0)
            trees.append((base+[(a,tip),(tip,b)],4))
        for edges,cap in trees:
            adj = adjacency(k,edges)
            leaf = next(v for v in range(k) if len(adj[v])==1)
            max_degree = max(max_degree,max(map(len,adj)))
            for root in {0,2,k//2,leaf,k-1}:
                h = reduce(gcd,(len(adj[v])-1 for v in range(k) if v!=root),k)
                for w in {0,1,k//2,(3*k//7)%k,rng.randrange(k)}:
                    result = build(edges,root,w,cap,rng)
                    if result is None:
                        endpoint = max(map(len,adj))==2 and len(adj[root])==1
                        assert w%h or (endpoint and (w+sum(range(k)))%k==0)
                        no += 1
                    else:
                        verify(k,edges,root,w,result)
                        yes += 1
    print('rooted gap targets',yes,'gcd or endpoint obstructions',no,'original maximum degree',max_degree,
          'eight-label realized, additional missing, and zero-root successes',eight())


if __name__=='__main__':
    main()

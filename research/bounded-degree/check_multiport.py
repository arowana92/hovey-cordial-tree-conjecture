"""Verify local data in the multiport proof on paths, branching trees and mixed moduli."""
from collections import Counter
from functools import reduce
from math import gcd
from random import Random

from check import adjacency
from check_unicyclic_core import inspect
from multiport import construct


def branch_tree(k,t):
    # Insert t ports into different edges of an unrooted binary tree.
    n = k-t
    assert n%2==0
    internal = n//2-1
    edges = [(i-1,i) for i in range(1,internal)]
    next_leaf = internal
    for i in range(internal):
        for _ in range(1+(i in (0,internal-1))):
            edges.append((i,next_leaf))
            next_leaf += 1
    assert next_leaf==n
    ports = list(range(n,k))
    selected = list(range(1,2*t,2))
    for p,i in zip(ports,selected):
        u,v = edges[i]
        edges[i] = (u,p)
        edges.append((p,v))
    return edges,ports


def run():
    rng = Random(3101991)
    accepted = rejected = proper = 0
    for k in (503,720,729,1024,1458,1601):
        for t in (2,3,4,5,8,12):
            families = [([(i-1,i) for i in range(1,k)],rng.sample(range(1,k-1),t))]
            # Use both degree-one and degree-two ports away from two reserved tips.
            binary = [((i-1)//2,i) for i in range(1,k)]
            families.append((binary,rng.sample(range(2,k-2),t)))
            if (k-t)%2==0:
                families.append(branch_tree(k,t))
            for edges,ports in families:
                for parity in (0,1):
                    a = [rng.randrange(k) for _ in ports]
                    removed = [rng.randrange(k) for _ in range(t-1)]
                    removed[-1] += (parity-sum(removed)+sum(a))%2
                    degree = Counter(v for edge in edges for v in edge)
                    g = reduce(gcd,(degree[v]-1+(v in ports) for v in range(k)),k)
                    assert (t-2)%g==0
                    result = construct(edges,ports,a,removed,rng)
                    if result is None:
                        assert (sum(removed)-sum(a))%g
                        rejected += 1
                        continue
                    auxiliary,cut,labels,pairs,wires,quotient = result
                    assert len(auxiliary)==k and len({frozenset(edge) for edge in auxiliary})==k
                    opened = adjacency(k,auxiliary[:cut]+auxiliary[cut+1:])
                    seen,stack = {0},[0]
                    while stack:
                        v = stack.pop()
                        for u in opened[v]:
                            if u not in seen:
                                seen.add(u)
                                stack.append(u)
                    assert len(seen)==k
                    assert set(edges)==set(auxiliary[:cut])|set(pairs)
                    assert all((labels[u]+labels[v]-w)%k==0 for (u,v),w in zip(pairs,removed))
                    assert Counter((labels[u]+labels[v])%k for u,v in wires)==Counter(
                        (labels[v]+b)%k for v,b in zip(ports,a))
                    inspect(k,auxiliary,cut,labels)
                    assert (sum(removed)-sum(a))%g==0
                    accepted += 1
                    proper += quotient>1
    # Check the actual old four-vertex path in the obstructed parity example.
    old = [0,1,2,3]
    assert [old[i]+old[i+1] for i in range(3)]==[1,3,5]
    assert (sum([1,3,5])-sum(old))%2==1
    print('certified multiport cores',accepted,'moment obstructions',rejected,
          'successful nontrivial quotient checks',proper)


if __name__=='__main__':
    run()

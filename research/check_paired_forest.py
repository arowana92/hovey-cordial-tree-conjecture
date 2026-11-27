"""Rebuild expanded trees and edge weights independently of the labeling decisions."""

from itertools import product
from random import Random

from .paired_forest import extend, replace_edge


def hist(values,k):
    out = [0]*k
    for x in values:
        out[x%k] += 1
    return out


def verify_forest(m, core, edges, sites, links):
    k = 2*m
    old_weights = [(core[a]+core[b]+h)%k for a,b,h in edges]
    bins = hist(old_weights,k)
    deficit = bins.index(min(bins))
    pairs = extend(m,[core[v] for v in sites],links,deficit)
    values = core+[v for row in pairs for v in row]
    new_edges = list(edges)
    for i,(p,a,b,h) in enumerate(links):
        v = len(core)+2*i
        u = sites[-1-p] if p < 0 else len(core)+2*p+a
        new_edges.extend([(v,v+1,0),(u,v+b,h)])
    weights = [(values[a]+values[b]+h)%k for a,b,h in new_edges]
    for counts in (hist(values,k),hist(weights,k)):
        assert max(counts)-min(counts) <= 1
    if len(links) and len(links)%m == 0:
        counts = hist(weights,k)
        assert counts.index(min(counts))%2 == 0
    return deficit%2


def forests():
    rng = Random(13261991)
    counts = [0,0]
    for m in (3,5,7,11,13):
        k = 2*m
        for t in range(1,3*m+1):
            for repeat in range(10):
                n = k*(1+rng.randrange(3))
                # On this path, the two classes use consecutive integer ranks. A
                # constant edge offset shifts the unique deficit to any desired parity.
                c,h = rng.randrange(k),rng.randrange(k)
                core = [(c+v//2+(v%2)*(n//2))%k for v in range(n)]
                edges = [(v-1,v,h) for v in range(1,n)]
                sites = [rng.randrange(n) for _ in range(rng.randint(1,8))]
                links = [(rng.randrange(-len(sites),i),rng.randrange(2),rng.randrange(2),
                          rng.randrange(k)) for i in range(t)]
                counts[verify_forest(m,core,edges,sites,links)] += 1
    return counts


def verify_chain(m,left,right,sides):
    pairs = replace_edge(m,left,right,sides)
    weights = []
    previous = left
    for pair,(a,b) in zip(pairs,sides):
        weights.extend([sum(pair),previous+pair[a]])
        previous = pair[b]
    weights.append(previous+right)
    k = 2*m
    copies = len(sides)//m
    assert hist((v for row in pairs for v in row),k) == [copies]*k
    counts = hist(weights,k)
    counts[(left+right)%k] -= 1
    assert counts == [copies]*k


def chains():
    rng = Random(199126)
    total = 0
    for m in (1,3,5):
        for traversed in product(range(2),repeat=m):
            if sum(traversed)%2:
                continue
            for left,right in product(range(2*m),repeat=2):
                verify_chain(m,left,right,[(0,b) for b in traversed])
                total += 1
    for _ in range(1800):
        m = 2*rng.randrange(30)+1
        n = m*rng.randint(1,4)
        sides = [(rng.randrange(2),rng.randrange(2)) for _ in range(n)]
        if sum(a != b for a,b in sides)%2:
            a,b = sides[-1]
            sides[-1] = a,1-b
        verify_chain(m,rng.randrange(2*m),rng.randrange(2*m),sides)
        total += 1
    return total


if __name__ == "__main__":
    print("whole-tree extensions by initial deficit parity",forests())
    print("chain replacements with exact vertex and edge increments",chains())

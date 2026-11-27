"""Replay growth certificates on the original tree, recounting both histograms."""
from itertools import permutations
from random import Random
import sys

from ..marked_leaf import growth
from .generate import native_search
from .site_growth import grow
from .verify import rooted_shapes


def solver(library,k):
    if k==1:
        return lambda parents,m: []
    search = native_search(library,k)
    def padded(parents,m):
        links = list(parents)
        if all(p < 0 for p in links):
            links.extend([-1]*(k-1-len(links)))
        else:
            roots = []
            for v,p in enumerate(links):
                roots.append(v if p<0 else roots[p])
            largest = max(set(roots),key=roots.count)
            end = max(i for i,r in enumerate(roots) if r==largest)
            while len(links)<k-1:
                links.append(end)
                end = len(links)-1
        return search(links,m)[:len(parents)]
    return padded


def replay(parent,labels,k,order,old=()):
    """Induce the tree on each prefix using the input edges only."""
    prefix = set(old)
    assert len(labels)==len(parent) and all(0<=x<k for x in labels)
    assert len(order)+len(old)==len(parent) and sorted([*old,*order])==list(range(len(parent)))
    for v in order:
        prefix.add(v)
        vertices, edges = [0]*k,[0]*k
        for w in prefix:
            vertices[labels[w]] += 1
            if w and parent[w] in prefix:
                edges[(labels[w]+labels[parent[w]])%k] += 1
        assert sum(edges)==len(prefix)-1
        assert max(vertices)-min(vertices)<=1 and max(edges)-min(edges)<=1
    return len(order)


def forest(rng,core,site,tips,count):
    # Start with several components, make binary forks, then subdivide edges.
    roots = rng.randint(1,tips)
    local = [-1]*roots
    ends = list(range(roots))
    for _ in range(tips-roots):
        at = rng.choice(ends)
        ends.remove(at)
        ends.extend([len(local),len(local)+1])
        local.extend([at,at])
    while len(local)<count:
        at = rng.randrange(len(local))
        local.append(local[at])
        local[at] = len(local)-1
    queue = [v for v,p in enumerate(local) if p<0]
    for v in queue:
        queue.extend(i for i,p in enumerate(local) if p==v)
    index = {v:core+i for i,v in enumerate(queue)}
    return [site if local[v]<0 else index[local[v]] for v in queue]


def main(library):
    rng = Random(261127)
    trees = prefixes = sites = fixed_prefixes = 0
    for k in range(1,31):
        witness = solver(library,k)
        size_list = [1,k, k+1, 2*k-1,2*k,2*k+1,3*k+2,4*k+3]
        cases = []
        for n in size_list:
            if k<=25:
                cases.append([-1]+[rng.randrange(v) for v in range(1,n)])
            cases.append([-1]+list(range(n-1)))
        if 26<=k<=30:
            tips = 10 if k<=27 else 8
            cases.append([-1]+forest(rng,1,0,tips-1,3*k+1))
        if k<=10:
            for n in range(2,9):
                cases.extend(rooted_shapes(n).values())
        for p in cases:
            mark = next(v for v in range(len(p)) if p.count(v)+int(v!=0)<=1)
            order,labels = growth(p,k,mark,witness=witness)
            prefixes += replay(p,labels,k,order)
            assert mark in order[-((len(p)-1)%k+1):]
            trees += 1
        if 26<=k<=30:
            tips = 6 if k<=27 else 5
            for size in (1,k,k+1,2*k,2*k+1):
                base = [-1]+list(range(size-1))
                _,labels = growth(base,k,witness=witness)
                for n in (0,1,k-1,k,k+1,2*k-1,2*k,3*k+4):
                    for tip_count in sorted({1,min(tips,(n+1)//2)}) if n else [0]:
                        extra = forest(rng,size,rng.randrange(size),tip_count,n) if n else []
                        order,extended = grow(base+extra,labels,k,witness=witness)
                        assert extended[:size]==labels
                        fixed_prefixes += replay(base+extra,extended,k,order,range(size))
                        sites += 1
    for p in range(4):
        assert any(len({(a+b)%4 for a,b in zip((p,)+x,x)})==3
                   for x in permutations((1,2,3)))
    print(trees,'marked trees,',prefixes,'connected prefixes;',sites,
          'fixed-core extensions,',fixed_prefixes,'new prefixes')


if __name__=='__main__':
    main(sys.argv[1])

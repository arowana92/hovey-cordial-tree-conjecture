"""Rebuild full trees from two-port witnesses and check every adjusted prefix in growth samples."""
import argparse
from collections import Counter
import ctypes
from itertools import combinations_with_replacement
from pathlib import Path
from random import Random

from research.marked_leaf import restore_batches
from research.rainbow.check_common_site import samples
from research.rainbow.check_cut_growth import solver

K = 27


def balanced(values):
    counts = Counter(values)
    bins = [counts[x] for x in range(K)]
    return max(bins)-min(bins)<=1


def replay_ports(stream,limit):
    expansions = offsets = 0
    for adj,rows in samples(stream,K,limit):
        edges = [(u,v) for u in range(K) for v in adj[u] if u<v]
        choices = {}
        for f in rows:
            occupied = {(f[u]+f[v])%K for u,v in edges}
            hole, = set(range(K))-occupied
            for u,v in combinations_with_replacement(range(K),2):
                menu = choices.setdefault((u,v),{})
                for unit in range(1,K):
                    if unit%3:
                        c = unit*(f[u]+f[v]-hole)%K
                        menu.setdefault(c,(f,unit,hole))
        for (u,v),menu in choices.items():
            assert 0 in menu or len(menu)==K-1
            if (u,v) in edges:
                assert 0 not in menu
                for bias in range(K):
                    f,unit,_ = next(iter(menu.values())) if bias==0 else menu[-bias%K]
                    weights = [(unit*(f[a]+f[b])+bias*((a,b)==(u,v)))%K for a,b in edges]
                    assert len(set(weights))==K-1
                    offsets += 1
            for n in (26,27):
                inner = [(n+a,n+b) for a,b in edges]
                for j in range(1,n):
                    f,unit,hole = menu[0] if 0 in menu else menu[-j%K]
                    labels = list(range(n))+[unit*(x+f[u]-hole)%K for x in f]
                    joined = [(0,i) for i in range(1,n) if i!=j]+inner+[(0,n+u),(j,n+v)]
                    assert len(joined)==len(labels)-1 and balanced(labels)
                    assert balanced((labels[a]+labels[b])%K for a,b in joined)
                    expansions += 1
    print('ordinary expansions',expansions,'adjusted bases',offsets)


def rooted(graph,root):
    parent,order = {root:None},[root]
    size = dict.fromkeys(graph,1)
    for v in order:
        for w in graph[v]:
            if w!=parent[v]:
                parent[w]=v
                order.append(w)
    for v in reversed(order[1:]):
        size[parent[v]] += size[v]
    return parent,order,size


def protected_growth(graph,mark,bias,base_search,forest_search):
    work = {v:list(nbrs) for v,nbrs in graph.items()}
    steps = []
    while len(work)>K:
        t = (len(work)-1)%K
        if not t:
            v = next(v for v in work if len(work[v])==1 and v not in mark)
            queue,roots = [(v,work[v][0])],1
        else:
            a,b = mark
            parent,_,size = rooted(work,a)
            if 2*size[b]<len(work):
                a,b = b,a
                parent,_,size = rooted(work,a)
            assert size[b]>t
            stack,walk = [a],[]
            while stack:
                v = stack.pop()
                walk.append(v)
                stack.extend(sorted((w for w in work[v] if w!=parent[v]),key=size.get,reverse=True))
            suffix = walk[-t:]
            outside = set(suffix)
            assert not outside.intersection(mark)
            incoming = [(v,parent[v]) for v in suffix if parent[v] not in outside]
            internal = [(v,parent[v]) for v in suffix if parent[v] in outside]
            queue,roots = incoming+internal,len(incoming)
        for v,w in queue[:roots]:
            work[w].remove(v)
        for v,w in queue:
            del work[v]
        steps.append((queue,roots,t==0))
    parent,order,_ = rooted(work,mark[0])
    assert len(order)==K and mark[1] in work[mark[0]]
    positions = {v:i for i,v in enumerate(order)}
    links = [positions[parent[v]]-1 for v in order[1:]]
    vector = ctypes.c_int*(K-1)
    digits = vector()
    flags = vector(*(bias if v==mark[1] else 0 for v in order[1:]))
    assert base_search(K,vector(*links),flags,digits)==1
    labels = dict(zip(order,[0,*digits]))
    weights = Counter((labels[v]+labels[parent[v]]+(bias if v==mark[1] else 0))%K
                      for v in order[1:])
    restore_batches(K,labels,weights,reversed(steps),forest_search)
    return labels


def replay_growth(stream,limit,library):
    rng = Random(271991)
    native = ctypes.CDLL(str(library.resolve())).fast_offset_witness
    search = solver(library,K)
    trees = prefixes = 0
    for adj,_ in samples(stream,K,limit):
        for n in (28,39,53,54,55,80,81,82,109):
            graph = {v:list(nbrs) for v,nbrs in enumerate(adj)}
            # Subdivide different original or previously subdivided edges.
            edges = [(a,b) for a in graph for b in graph[a] if a<b]
            for v in range(K,n):
                j = rng.randrange(len(edges))
                a,b = edges[j]
                graph[a].remove(b)
                graph[b].remove(a)
                graph[a].append(v)
                graph[b].append(v)
                graph[v]=[a,b]
                edges[j]=(a,v)
                edges.append((b,v))
            for mark,bias in zip(rng.sample(edges,4),(0,1,3,9)):
                labels = protected_growth(graph,mark,bias,native,search)
                vertices,weights = [],[]
                known = set()
                for v,f in labels.items():
                    vertices.append(f)
                    for w in graph[v]:
                        if w in known:
                            offset = bias if {v,w}==set(mark) else 0
                            weights.append((f+labels[w]+offset)%K)
                    known.add(v)
                    assert len(weights)==len(vertices)-1 and balanced(vertices) and balanced(weights)
                    prefixes += 1
                assert len(known)==n
                trees += 1
    print('adjusted growth trees',trees,'connected prefixes',prefixes)


if __name__=='__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('stream',type=Path)
    cli.add_argument('--limit',type=int,default=100)
    cli.add_argument('--growth-library',type=Path)
    args = cli.parse_args()
    replay_ports(args.stream,args.limit)
    if args.growth_library:
        replay_growth(args.stream,args.limit,args.growth_library)

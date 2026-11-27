"""Independently rebuild the joined stars, their edges and their integer sums."""

from collections import Counter
from itertools import product, permutations
from random import Random

from research.census.star_joins import join_stars
from research.rainbow.verify import rooted_shapes


def check(par, x, a, ends):
    result, reported = join_stars(par,x,a,ends)
    q = len(par)
    edges = [(v*(a+1),v*(a+1)+j+1) for v in range(q) for j in range(a)]
    edges.extend((p*(a+1)+ends[v-1][0]+1,v*(a+1)+ends[v-1][1]+1)
                 for v,p in enumerate(par[1:],1))
    assert edges == reported and len(edges)+1 == len(result) == q*(a+1)
    assert sorted(result) == list(range(len(result)))
    sums = sorted(result[u]+result[v] for u,v in edges)
    assert sums == list(range(q*a-q//2,q*a-q//2+len(edges)))
    for k in [2,3,8,23,47,q,a+1,len(result)]:
        for values in (result,sums):
            freq = Counter(v%k for v in values)
            assert max(freq.values())-min(freq.get(i,0) for i in range(k)) <= 1


def rainbow(par):
    n = len(par)
    for xs in permutations(range(1,n)):
        x = (0,*xs)
        if len({(x[i]+x[p])%n for i,p in enumerate(par[1:],1)}) == n-1:
            return x
    raise AssertionError("no quotient labeling")


def distances(par):
    adj = [[] for _ in par]
    for i,j in enumerate(par[1:],1):
        adj[i].append(j)
        adj[j].append(i)
    def visit(v,parent):
        depth = sorted((visit(w,v) for w in adj[v] if w != parent),reverse=True)
        children = [d for d,_ in depth]+[0,0]
        return children[0]+1,max([children[0]+children[1],*(span for _,span in depth)])
    return max(map(len,adj)),visit(0,-1)[1]


if __name__ == "__main__":
    rng = Random(23)
    count = 0
    for q in [3,5,7,9]:
        for par in rooted_shapes(q).values():
            x = rainbow(par)
            deg,diam = distances(par)
            for a in [deg+(diam+1)//2,deg+1]:
                used = [0]*q
                ends = []
                for v,u in enumerate(par[1:],1):
                    if a == deg+1:
                        ends.append((used[u],used[v]))
                        used[u] += 1
                        used[v] += 1
                    else:
                        ends.append((rng.randrange(a),rng.randrange(a)))
                check(par,x,a,ends)
                count += 1
    print(f"{count} joined trees on small rooted quotients")
    count = 0
    for q in range(3,18,2):
        par = (-1,*range(q-1))
        x = tuple(i//2+(q//2+1 if i%2 else 0) for i in range(q))
        for split in product(range(2),repeat=q-2):
            ends = [(split[i-1] if i else 0,0) for i in range(q-1)]
            check(par,x,2,ends)
            count += 1
        check(par,x,1,[(0,0)]*(q-1))
    print(f"{count} two-leaf star paths, all incidence partitions through 17 copies")
    for q in [51,101,255]:
        par = (-1,*range(q-1))
        check(par,range(q),5,[(rng.randrange(5),rng.randrange(5)) for _ in range(q-1)])
    print("Long paths through 255 copies verified")

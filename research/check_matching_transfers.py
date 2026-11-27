"""Whole-tree tests for mixed quotient pieces and matching completions."""

from itertools import combinations
from random import Random

from research.check_matching_expansion import check
from research.check_odd_quotient import piece
from research.matching_expansion import matching_labels
from research.rainbow.generate import rainbow
from research.rainbow.verify import rooted_shapes


def complementary_reps(t, missing, m):
    reps = [None]*t
    for a in range(t):
        if reps[a] is not None:
            continue
        b = (missing-a)%t
        if a == b:
            reps[a] = a+t*(((missing-2*a)//t)*pow(2,-1,m)%m)
        else:
            reps[a],reps[b] = a,missing-a
    return reps


def products(rng):
    total = mixed = 0
    for t in range(2,8):
        for parents in rooted_shapes(t).values():
            f = [0]+rainbow(tuple(p-1 for p in parents[1:]),t)
            internal = [(f[p],f[i]) for i,p in enumerate(parents) if i]
            missing, = set(range(t))-{(a+b)%t for a,b in internal}
            for m in (1,3,5,9):
                reps = complementary_reps(t,missing,m)
                for s in sorted({1, m, m+1, 2*m-1, 2*m+2}):
                    q, joins = piece(s,m,rng.randrange(2),rng)
                    labels = [(r+t*x)%(t*m) for x in q for r in reps]
                    edges = [(i*t+a,i*t+b) for i in range(s) for a,b in internal]
                    for i,j in joins:
                        a = rng.randrange(t)
                        edges.append((i*t+a,j*t+(missing-a)%t))
                    check(labels,edges,t*m)
                    total += 1
    # Enumerate common-sum trees of different shapes independently.
    choices = list(combinations(range(5),2))
    groups = {}
    for edges in combinations(choices,4):
        sums = tuple(sorted(x+y for x,y in edges))
        if len({x%5 for x in sums}) != 4:
            continue
        seen = {0}
        for _ in range(4):
            seen.update(y for x,y in edges if x in seen)
            seen.update(x for x,y in edges if y in seen)
        if len(seen) == 5:
            degrees = tuple(sorted(sum(i in e for e in edges) for i in range(5)))
            groups.setdefault(sums,{})[degrees] = edges
    for sums, variants in groups.items():
        if len(variants) < 2:
            continue
        missing, = set(range(5))-{x%5 for x in sums}
        pieces = list(variants.values())
        for m in (3,5,9,11):
            for s in (m-1,m,m+1,2*m+3):
                q,joins = piece(s,m,True,rng)
                full = [(a+5*x)%(5*m) for x in q for a in range(5)]
                edges = [(5*i+a,5*i+b) for i in range(s) for a,b in pieces[i%len(pieces)]]
                edges.extend((5*i,5*j+missing) for i,j in joins)
                check(full,edges,5*m)
                mixed += 1
    assert mixed
    return total,mixed


def match_cases(rng):
    sparse = leaf = deleted = 0
    for m in (1,3,5,7,11,13,19,21):
        for s in range(1,3*m+1):
            q,edges = piece(s,m,rng.randrange(2),rng)
            parents = [-1]+[p for p,_ in edges]
            links = [(rng.randrange(2),rng.randrange(2)) for _ in edges]
            f = matching_labels(parents,q,links,m)
            joined = [(2*i+a,2*j+b) for (i,j),(a,b) in zip(edges,links)]
            base = joined+[(2*i,2*i+1) for i in range(s)]
            check(f,base,2*m)
            if s <= m:
                used = {x for edge in joined for x in edge}
                absent = {next(x for x in (2*i,2*i+1) if x not in used) for i in range(s)
                          if any(x not in used for x in (2*i,2*i+1)) and rng.randrange(2)}
                remap = {x:i for i,x in enumerate(x for x in range(2*s) if x not in absent)}
                check([f[x] for x in remap],[(remap[x],remap[y]) for x,y in base
                      if x not in absent and y not in absent],2*m)
                sparse += 1
            if 2*(s%m) < m:
                v,w = check(f,base,2*m)
                for p in range(2*s):
                    x = next(x for x in range(2*m) if v[x] == min(v) and w[(f[p]+x)%(2*m)] == min(w))
                    check(f+[x],base+[(p,len(f))],2*m)
                    leaf += 1
            if s%m == 0:
                used = {x for e in joined for x in e}
                for x in set(range(2*s))-used:
                    remap = {v:i for i,v in enumerate(v for v in range(2*s) if v != x)}
                    check([f[v] for v in remap],[(remap[a],remap[b]) for a,b in base if x not in (a,b)],2*m)
                    deleted += 1
    return sparse,leaf,deleted


if __name__ == "__main__":
    rng = Random(1991)
    print("Verified homogeneous and mixed products:", *products(rng))
    print("Verified short restrictions, added leaves and deleted leaves:", *match_cases(rng))

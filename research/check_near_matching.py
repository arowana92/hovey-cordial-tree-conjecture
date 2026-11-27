"""Verify every prefix, compare maximum matchings by tree DP, and recount the original tree."""

from collections import Counter
from random import Random

from .check_matching_expansion import check
from .near_matching import label, matching_at_leaves, prefix_labels
from .rainbow.verify import rooted_shapes


def maximum(parent):
    # Leaving a vertex available for its own parent forbids matching a child there.
    available = [0]*len(parent)
    best_gain = [0]*len(parent)
    for v in reversed(range(1,len(parent))):
        p = parent[v]
        available[p] += available[v]+best_gain[v]
        best_gain[p] = max(best_gain[p],1-best_gain[v])
    return available[0]+best_gain[0]


def check_tree(parent, m):
    n = len(parent)
    d = n-2*maximum(parent)
    if n > 1:
        mate = matching_at_leaves(parent)
        degree = Counter(parent[1:])
        for v,u in enumerate(mate):
            if u == -1:
                assert degree[v]+int(v != 0) == 1
            else:
                assert mate[u] == v and (parent[v] == u or parent[u] == v)
        assert mate.count(-1) == d
    s = (n+d)//2
    if d > (s-1)%m+1:
        return 0
    f = label(parent,m)
    check(f,[(v,p) for v,p in enumerate(parent) if v],2*m)
    return 1


def check_prefix(parent, offsets, m):
    f = prefix_labels(parent,m,offsets)
    vertices, weights = [0]*m,[0]*m
    for i,p in enumerate(parent):
        vertices[f[i]] += 1
        if i:
            weights[(f[i]+f[p]+offsets[i]) % m] += 1
        assert max(vertices)-min(vertices) <= 1
        assert max(weights)-min(weights) <= 1


def main():
    rng = Random(26131991)
    primes = [3,5,7,11,13]
    small = 0
    for n in range(1,10):
        for p in rooted_shapes(n).values():
            for m in primes:
                small += check_tree(p,m)
    eligible = prefixes = 0
    for m in [2]+primes:
        for _ in range(140):
            n = rng.randint(1,5*m+1)
            parents = [-1]+[rng.randrange(i) for i in range(1,n)]
            offsets = [rng.randrange(m) for _ in parents]
            check_prefix(parents,offsets,m)
            prefixes += len(parents)
            if m != 2:
                eligible += check_tree(parents,m)
    near = 0
    for m in primes:
        for s in range(1,4*m+2):
            for _ in range(3):
                # Grow an exposed singleton by matched pairs, varying both attachment sites.
                tree = [-1]
                for _ in range(s):
                    p = rng.randrange(len(tree))
                    tree.extend([p,len(tree)])
                assert check_tree(tree,m)
                near += 1
    print(f"{prefixes} offset prefixes, {small} small trees, {eligible} random eligible trees, "
          f"{near} near-perfect matching trees")


if __name__ == "__main__":
    main()

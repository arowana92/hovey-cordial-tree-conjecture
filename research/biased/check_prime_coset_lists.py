"""Exhaust small separate lists and check actual tree labels at composite moduli."""
from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations
from random import Random

from .prime_coset_lists import assign


def verify(k, lists, shifts, labels):
    assert len(labels) == len(lists) == len(set(labels))
    assert all(x in a for x, a in zip(labels, lists))
    assert len({(x+s) % k for x, s in zip(labels, shifts)}) == len(labels)


def small(trace):
    checked = 0
    # Supersets preserve a witness. Shrink tight rows to r and other rows to r+1.
    for k, p, limit in ((4,2,4), (6,3,6)):
        for r in range(1, limit+1):
            rows = [(a,s) for size in (r,r+1) for a in combinations(range(k),size)
                    for s in range(0,k,k//p)]
            for sample in combinations_with_replacement(rows,r):
                if sum(len(a)==r for a,s in sample) >= p:
                    continue
                lists, shifts = zip(*sample)
                labels = assign(k,p,lists,shifts,trace)
                verify(k,lists,shifts,labels)
                checked += 1
    return checked


def sharp():
    checked = 0
    for p in (2,3,5,7):
        k = 2*p
        cell = list(range(0,k,2))
        shifts = [0]*(p-1)+[2]
        assert not any(len({(x+s)%k for x,s in zip(row,shifts)})==p
                       for row in permutations(cell))
        for row in range(p):
            lists = [cell if i!=row else cell+[1] for i in range(p)]
            verify(k,lists,shifts,assign(k,p,lists,shifts))
            checked += 1
    return checked


def tree_examples(trace):
    rng = Random(27)
    count = special = 0
    for p, k in ((2,10), (3,12), (3,27), (5,20), (7,28)):
        for h in range(2, min(k//3,6)+1):
            order = k+h
            low,high = iter(range((order+1)//2)),iter(range((order+1)//2,order))
            path = [next(low if i%2==0 else high)%k for i in range(order)]
            parent = {x: path.index(x) for x in path}
            old_edges = [(i,i+1) for i in range(order-1)]
            high_v = {x for x in path if path.count(x)==2}
            weights = [(path[i]+path[j])%k for i,j in old_edges]
            high_w = {w for w in weights if weights.count(w)==2}
            assert len(high_v)==h and len(high_w)==h-1
            for r in {k-2*h,k-2*h+1}:
                for _ in range(28):
                    start = rng.randrange(k)
                    shifts = [(start+rng.randrange(p)*(k//p))%k for i in range(r)]
                    lists = [{x for x in range(k) if x not in high_v and (x+s)%k not in high_w}
                             for s in shifts]
                    if sum(len(a)==r for a in lists)>=p:
                        continue
                    leaves = assign(k,p,lists,shifts,trace)
                    verify(k,lists,shifts,leaves)
                    actual = path+leaves
                    edges = old_edges+[(parent[s],order+i) for i,s in enumerate(shifts)]
                    vh, eh = Counter(actual), Counter((actual[i]+actual[j])%k for i,j in edges)
                    assert max(vh[x] for x in range(k))-min(vh[x] for x in range(k))<=1
                    assert max(eh[x] for x in range(k))-min(eh[x] for x in range(k))<=1
                    count += 1
                    special += (len(actual)==52 and k==27 and len(set(shifts))==3)
    return count, special


if __name__ == '__main__':
    trace = []
    print('sharpness repairs',sharp())
    print('small separate-list families',small(trace))
    print('whole trees and order-52 three-shift examples',*tree_examples(trace))
    print('allocation steps',dict(Counter(trace)))

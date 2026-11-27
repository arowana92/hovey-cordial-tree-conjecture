"""Verify quotient witnesses, all expansions of exceptional quotients, and actual lifts."""

import argparse
from collections import Counter
from functools import cache
from itertools import permutations, product
from math import comb, prod
from pathlib import Path


def parse(word, n):
    bits = format(word, "b")
    assert len(bits) == 2*n
    parent = [-1]
    stack = [0]
    for bit in bits:
        assert stack
        if bit == "1":
            parent.append(stack[-1])
            stack.append(len(parent)-1)
        else:
            assert len(stack) > 1
            stack.pop()
    assert stack == [0] and len(parent) == n+1
    return parent


def tree_shape(parent):
    rows = [[] for _ in parent]
    for v in reversed(range(1,len(parent))):
        rows[parent[v]].append(tuple(sorted(rows[v])))
    return tuple(sorted(rows[0]))


def rooted_count(n):
    # The multiset of children of a root has total order n-1.
    counts = [0]*(n+1)
    forests = [1]+[0]*(n-1)
    for s in range(1,n+1):
        counts[s] = forests[s-1]
        if s == n:
            break
        forests = [sum(forests[t-r*s]*comb(counts[s]+r-1,r) for r in range(t//s+1))
                   for t in range(n)]
    return counts[n]


@cache
def expansion_count(shape, paired):
    # Equal contracted children are indistinguishable. Each can choose one of
    # two endpoints when the current vertex is a pair.
    return prod(comb((1+int(paired))*expansion_count(child,True)+n-1,n)
                for child,n in Counter(shape).items())


def matched_count(m):
    forests = [1]+[0]*m
    for s in range(1,m+1):
        types = sum(forests[j]*forests[s-1-j] for j in range(s))
        forests = [sum(forests[n-r*s]*comb(types+r-1,r) for r in range(n//s+1))
                   for n in range(m+1)]
    return forests[m]


def check_labels(parent, free, k):
    assert sorted(free) == list(range(k))
    full = [0]+free
    assert sorted((full[p]+full[v]) % k for v,p in enumerate(parent[1:],1)) == list(range(k))


def check_lift(parent, free, m, mask):
    tree, labels = [-1], [0]
    for i, (p,x) in enumerate(zip(parent[1:],free),1):
        site = 2*p-1+(mask & 1) if p else 0
        if p:
            mask >>= 1
        tree.extend([site,2*i-1])
        bit = labels[site] % 2
        labels.extend([(2*x+m*bit) % (2*m),(2*x+m*(1-bit)) % (2*m)])
    check_labels(tree,labels[1:],2*m)


@cache
def paired_shapes(shape):
    # Start with the incoming endpoint and its mate. Each child edge may meet either.
    result = set()
    for children in product(*(paired_shapes(child) for child in shape)):
        for mask in range(1 << len(children)):
            mate = tuple(sorted(s for i,s in enumerate(children) if (mask >> i) & 1))
            top = [s for i,s in enumerate(children) if not ((mask >> i) & 1)]
            result.add(tuple(sorted([mate]+top)))
    return result


def expansions(shape):
    return {tuple(sorted(rows)) for rows in product(*(paired_shapes(child) for child in shape))}


def check_exception(parent, k):
    """Exhaust internal assignments and then match remaining leaf labels to parent shifts."""
    children = [[w for w in range(1,k+1) if parent[w] == v] for v in range(k+1)]
    inside = [v for v in range(1,k+1) if children[v]]
    for digits in permutations(range(k),len(inside)):
        values = {0:0, **dict(zip(inside,digits))}
        if sum(len(children[v])*values[v] for v in inside) % k:
            continue
        sums = {(values[v]+values[parent[v]]) % k for v in inside}
        if len(sums) != len(inside):
            continue
        demands = [0]*k
        for v in range(1,k+1):
            if not children[v]:
                demands[values[parent[v]]] += 1
        shifts = [i for i,c in enumerate(demands) if c]
        free = sorted(set(range(k))-set(digits))
        def assign(i, used):
            if i == len(free):
                return True
            for a in shifts:
                w = (free[i]+a) % k
                if demands[a] and w not in used:
                    demands[a] -= 1
                    if assign(i+1,used|{w}):
                        return True
                    demands[a] += 1
            return False
        assert not assign(0,sums)


def verify(m, stream):
    quotients, needed, direct = set(), set(), set()
    missing = lifts = 0
    with stream.open() as reader:
        for line in reader:
            tag, word, *digits = line.split()
            assert tag in ("Q","E")
            word = int(word)
            free = list(map(int,digits))
            k = m if tag == "Q" else 2*m
            p = parse(word,k)
            shape = tree_shape(p)
            seen = quotients if tag == "Q" else direct
            assert shape not in seen
            seen.add(shape)
            if tag == "Q" and not free:
                missing += 1
                check_exception(p,k)
                needed.update(expansions(shape))
                continue
            check_labels(p,free,k)
            if tag == "Q":
                masks = range(1 << sum(v > 0 for v in p)) if m <= 5 else [word ^ (word >> m)]
                for mask in masks:
                    check_lift(p,free,m,mask)
                    lifts += 1
    assert len(quotients) == rooted_count(m+1)
    assert direct == needed
    total = sum(expansion_count(q,False) for q in quotients)
    assert total == matched_count(m)
    print(f"m={m} quotients={len(quotients)} exceptions={missing} "
          f"direct expansions={len(direct)} lifted trees checked={lifts} rooted trees covered={total}")


if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument("modulus", type=int, choices=range(3,16,2))
    arg.add_argument("stream", type=Path)
    args = arg.parse_args()
    verify(args.modulus,args.stream)

"""Direct finite checks of the leaf list theorem, its threshold and two-shift converse."""

from itertools import combinations, product
from math import gcd
from random import Random


def choose(k, shifts, lists):
    def walk(i, labels, weights):
        if i==len(shifts):
            return ()
        for x in lists[i]:
            w = (x+shifts[i])%k
            if x in labels or w in weights:
                continue
            rest = walk(i+1,labels|{x},weights|{w})
            if rest is not None:
                return (x,*rest)
        return None
    return walk(0,set(),set())


def validate_two():
    separate = common = 0
    for k in range(2,11):
        for r in range(1,k+1):
            sets = list(combinations(range(k),r))
            for t in range(1,k):
                d = k//gcd(k,t)
                for b in range(r+1):
                    good = b%d<=r%d
                    # For a common list it suffices to choose which b entries move.
                    def feasible(xs):
                        X = set(xs)
                        return any(not ({(x+t)%k for x in S}&(X-set(S)))
                                   for S in combinations(xs,b))
                    observed = all(feasible(xs) for xs in sets)
                    assert observed==good
                    common += 1
                    if k<=5 and r<=3:
                        shifts = (0,)*(r-b)+(t,)*b
                        observed = all(choose(k,shifts,ls) is not None for ls in product(sets,repeat=r))
                        assert observed==good
                        separate += 1
    return common,separate


def validate_trees():
    rng = Random(38187)
    cases = sharp = 0
    for p in (3,5,7,11,13,17,19):
        for h in range(1,(p+1)//2+1):
            r = p-2*h+1
            if not 1<=r<=8:
                continue
            for _ in range(8):
                parents = [-1]+[rng.randrange(i) for i in range(1,h)]
                parents.extend(rng.randrange(h) for _ in range(r))
                offsets = [0]+[rng.randrange(p) for _ in parents[1:]]
                X,W = [0],set()
                for i in range(1,h):
                    s = (X[parents[i]]+offsets[i])%p
                    x = next(a for a in range(p) if a not in X and (a+s)%p not in W)
                    X.append(x)
                    W.add((x+s)%p)
                shifts = [(X[parents[i]]+offsets[i])%p for i in range(h,h+r)]
                lists = [tuple(x for x in range(p) if x not in X and (x+s)%p not in W) for s in shifts]
                assert min(map(len,lists))>=r
                tail = choose(p,shifts,lists)
                assert tail is not None
                X.extend(tail)
                actual = [(X[i]+X[parents[i]]+offsets[i])%p for i in range(1,h+r)]
                assert len(set(X))==h+r and len(set(actual))==h+r-1
                cases += 1

            # One more leaf with this same fixed core size makes extension fail.
            a = set(range(h))
            w = set(range(h,2*h-1))
            assert len(set(range(p))-a-w)==r
            sharp += 1
    return cases,sharp


if __name__=="__main__":
    print("Common-list classifications and independent-list classifications:",*validate_two(),flush=True)
    print("Edge-checked trees and sharp size obstructions:",*validate_trees())

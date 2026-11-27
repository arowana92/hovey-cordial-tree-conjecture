"""Check leaf extensions by direct assignment, exact root-of-unity arithmetic and tree histograms."""

from functools import lru_cache
from itertools import combinations, combinations_with_replacement, product
from math import gcd
from random import Random

from research.biased.check_leaf_lists import choose


def verify_choice(k, shifts, lists):
    labels = choose(k, shifts, lists)
    assert labels is not None
    assert all(v in allowed for v,allowed in zip(labels,lists))
    assert len(set(labels))==len(shifts)
    assert len({(v+s)%k for v,s in zip(labels,shifts)})==len(shifts)
    return labels


def all_small_lists():
    count = 0
    for k in range(2,7):
        for r in range(1,k):
            sets = list(combinations(range(k),r+1))
            for delta in range(1,k):
                for b in range(1,r):
                    for left in combinations_with_replacement(sets,r-b):
                        for right in combinations_with_replacement(sets,b):
                            verify_choice(k,[0]*(r-b)+[delta]*b,left+right)
                            count += 1
    return count


def remainder(poly, divisor):
    p = list(poly)
    while p and p[-1]==0:
        p.pop()
    while len(p)>=len(divisor):
        top = p[-1]
        at = len(p)-len(divisor)
        for i,v in enumerate(divisor):
            p[at+i] -= top*v
        while p and p[-1]==0:
            p.pop()
    return p


@lru_cache(None)
def cyclotomic(d):
    poly = [-1]+[0]*(d-1)+[1]
    for f in range(1,d):
        if d%f:
            continue
        factor = cyclotomic(f)
        quotient = [0]*(len(poly)-len(factor)+1)
        for i in reversed(range(len(quotient))):
            quotient[i] = poly[i+len(factor)-1]
            for j,c in enumerate(factor):
                poly[i+j] -= quotient[i]*c
        assert not any(poly)
        poly = quotient
    return poly


def check_minors():
    count = 0
    for d in range(2,21):
        for r in range(d,3*d+1):
            hole = r%d+1
            if hole==d:
                continue
            # Count actual subsets by their exponent sum modulo d.
            ways = [[0]*d for _ in range(r+1)]
            ways[0][0] = 1
            added = 0
            for j in range(r+1):
                if j==hole:
                    continue
                added += 1
                for b in range(added,0,-1):
                    for u,v in enumerate(ways[b-1]):
                        ways[b][(u+j)%d] += v
            for b in range(1,r):
                if b%d>r%d:
                    assert remainder(ways[b],cyclotomic(d))
                    count += 1
    return count


def balanced(values,k):
    bins = [0]*k
    for v in values:
        bins[v%k] += 1
    return max(bins)-min(bins)<=1


def check_trees():
    rng = Random(38185)
    count = 0
    for k in range(4,27):
        for h in range(1,k//2+1):
            r = min(8,k-2*h)
            if r<1:
                continue
            for periods in range(4):
                # An injective core on h vertices, with its actual sums distinct.
                par = [-1]+[rng.randrange(i) for i in range(1,h)]
                while True:
                    labels = rng.sample(range(k),h)
                    w = [(labels[i]+labels[par[i]])%k for i in range(1,h)]
                    if len(set(w))==len(w):
                        break
                for _ in range(periods):
                    at = rng.randrange(len(labels))
                    par.extend([at]*k)
                    labels.extend(rng.sample(range(k),k))
                w = [(labels[i]+labels[par[i]])%k for i in range(1,len(par))]
                assert balanced(labels,k) and balanced(w,k)
                heavy_v = {a for a in range(k) if labels.count(a)>periods}
                heavy_e = {a for a in range(k) if w.count(a)>periods}
                sites = rng.choices(range(len(par)),k=2)
                parents = rng.choices(sites,k=r)
                shifts = [labels[i] for i in parents]
                lists = [tuple(a for a in range(k) if a not in heavy_v and (a+s)%k not in heavy_e)
                         for s in shifts]
                assert all(len(ls)>=r+1 for ls in lists)
                labels.extend(verify_choice(k,shifts,lists))
                par.extend(parents)
                w = [(labels[i]+labels[par[i]])%k for i in range(1,len(par))]
                assert balanced(labels,k) and balanced(w,k)
                count += 1
    return count


def check_progressions():
    rng = Random(7807)
    count = 0
    for k in range(5,35):
        for delta in range(1,k):
            order = k//gcd(delta,k)
            for t in range(3,min(7,order)+1):
                r = min(8,order-t+1)
                if r<t:
                    continue
                shifts = [delta*i%k for i in range(t)]+[delta*rng.randrange(t)%k for _ in range(r-t)]
                lists = [rng.sample(range(k),r+t-1) for _ in range(r)]
                verify_choice(k,shifts,lists)
                count += 1
    return count


if __name__=="__main__":
    print(f"{all_small_lists()} independent-list families")
    print(f"{check_minors()} exact nonzero deleted-column coefficients")
    print(f"{check_trees()} actual trees, {check_progressions()} progression-list instances")

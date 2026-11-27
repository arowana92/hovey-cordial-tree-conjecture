"""Independent subset and multiplicity tests for single-center and two-star criteria."""
from collections import Counter
from itertools import combinations_with_replacement,permutations
from math import gcd
from random import Random

from .star_period import arbitrary,cyclic


def check_counts(k,q,c,p,b,a,row):
    kids,singles,x = row
    assert len(kids)==len(singles)==k and min(kids)>=0 and min(singles)>=0
    assert sum(kids)==c and sum(singles)==q*k-1-c
    v = [int(i==0)+int(i==a)+kids[i]+singles[i] for i in range(k)]
    e = [int(i==(a+p)%k)+kids[(i-a)%k]+singles[(i-b)%k] for i in range(k)]
    assert e==[q]*k and v==[q+int(i==x) for i in range(k)]


def enumerate_centers(k,q,c,p,b,a):
    for kids in combinations_with_replacement(range(k),c):
        e = Counter([(a+p)%k]+[(a+x)%k for x in kids])
        if any(t>q for t in e.values()):
            continue
        singles = [q-e[(x+b)%k] for x in range(k)]
        v = [int(x==0)+int(x==a)+kids.count(x)+singles[x] for x in range(k)]
        if max(v)-min(v)<=1:
            return True
    return False


def main():
    rng = Random(28112610)
    brute = criteria = arbitrary_cases = fans = 0
    for k in range(2,9):
        for q in (1,2):
            for c in range(min(q*k,5)):
                for a in range(k):
                    for p in range(k):
                        for b in range(k):
                            row = cyclic(k,q,c,p,b,a)
                            assert (row is not None)==enumerate_centers(k,q,c,p,b,a)
                            if row is not None:
                                check_counts(k,q,c,p,b,a,row)
                            brute += 1
    for k in range(2,43):
        for c in range(k):
            for p in range(k):
                hit = any(cyclic(k,1,c,p,0,a) is not None for a in range(k))
                assert hit==(p%gcd(c,k)==0 or p%gcd(c+1,k)==0)
                criteria += 1
        for _ in range(20):
            q = rng.randrange(2,11)
            c = rng.randrange(q*k)
            p,b = rng.randrange(k),rng.randrange(k)
            # Remove complete periods of children or singletons until two remain.
            reduced = c
            while q>2:
                if reduced>=k:
                    reduced -= k
                q -= 1
            a = (b-p)%k if reduced<k else p
            row = cyclic(k,2,reduced,p,b,a)
            assert row is not None
            check_counts(k,2,reduced,p,b,a,row)
        if k<=23:
            for j in range(16):
                q = 1+j%2
                center = rng.randrange(q*k)
                children = set(rng.sample([i for i in range(q*k) if i!=center],rng.randrange(q*k)))
                shifts = [rng.randrange(k) for _ in range(q*k)]
                f = arbitrary(k,shifts,center,children)
                c = len(children)
                assert (f is not None)==(sum(shifts)%gcd(c,k)==0 or sum(shifts)%gcd(c+1,k)==0)
                if f is not None:
                    v = Counter([0]+f)
                    e = Counter((x+shifts[i]+(f[center] if i in children else 0))%k
                                for i,x in enumerate(f))
                    assert all(e[r]==q and q<=v[r]<=q+1 for r in range(k))
                    arbitrary_cases += 1
    for k in range(4,43,2):
        m = k//2
        ok = False
        for a,b,z in permutations(range(k),3):
            labels = [a]+[x for x in range(k) if x not in (a,b,z)]+[b,z]
            weights = [a]+[(a+x)%k for x in labels[1:-2]]+[(m+b)%k,(b+z)%k]
            hist = Counter(weights)
            bins = [hist[i]+(i!=0) for i in range(k)]
            if max(bins)-min(bins)<=1:
                ok = True
                break
        assert ok==(k%4==0 or k%3==0)
        fans += 1
    print('prescribed-center subset comparisons',brute,'one-period divisibility tests',criteria,
          'arbitrary-offset packets',arbitrary_cases,'two-star moduli',fans)


if __name__=='__main__':
    main()

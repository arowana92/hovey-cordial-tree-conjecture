"""Construct harmonious odd cycles containing a full prescribed arithmetic progression."""
from collections import Counter
from math import gcd
from random import Random


def cycle(k, start, difference):
    if k < 3 or k % 2 == 0 or difference % k == 0:
        raise ValueError('expected an odd order at least three and a nonzero difference')
    m = gcd(k, difference)
    if m == 1:
        return [(start+j*difference) % k for j in range(k)]
    h = k//m
    unit = next(u for u in range(1,k) if gcd(u,k) == 1 and (u*m-difference) % k == 0)
    return [(start+unit*(i+j*m*(1 if i < m//2 else 2))) % k
            for i in range(m) for j in range(h)]


def check_cycles():
    cases = 0
    for k in range(3,252,2):
        for d in range(1,k):
            a = (k//2+d*d) % k
            f = cycle(k,a,d)
            h = k//gcd(d,k)
            assert f[:h] == [(a+j*d) % k for j in range(h)]
            assert set(f) == {(f[i-1]+v) % k for i,v in enumerate(f)} == set(range(k))
            cases += 1
    return cases


def check_fibres():
    # Independently prescribe an entire row of high coordinates over one base cycle.
    cases = 0
    for k in (3,9,15,25,27,45):
        for d in (3,5,9):
            for step in range(1,k):
                low = cycle(k,0,step)
                high = [(i*i+step*i+1) % d for i in range(k)]
                # Carry in the cyclic extension; componentwise addition in the product.
                for split in (False, True):
                    if split:
                        f = [(v,(sheet+b) % d) for sheet in range(d) for v,b in zip(low,high)]
                        sums = {((x[0]+y[0]) % k, (x[1]+y[1]) % d) for x,y in zip(f,f[1:]+f[:1])}
                        assert f[:k] == list(zip(low,high))
                    else:
                        f = [v+k*((sheet+b) % d) for sheet in range(d) for v,b in zip(low,high)]
                        sums = {(x+y) % (k*d) for x,y in zip(f,f[1:]+f[:1])}
                        assert f[:k] == [v+k*b for v,b in zip(low,high)]
                    assert len(set(f)) == len(sums) == k*d
                    cases += 1
    return cases


def check_trees():
    rng = Random(1991)
    cases = moved = 0
    for k in range(3,64,2):
        for d in range(1,k):
            a = rng.randrange(k)
            g = cycle(k,a,d)
            h = k//gcd(d,k)
            # Start with an injective rainbow path and add full leaf periods at its sites.
            labels = g[:h]
            edges = [(i-1,i) for i in range(1,h)]
            mark = rng.randrange(h-1)
            base_order = h + k*h
            actual = [(i,j) for i,j in edges if i != mark]
            actual += [(mark,base_order+mark+1),(mark+1,base_order+mark)]
            for v in range(h):
                for x in range(k):
                    j = len(labels)
                    labels.append(x)
                    edges.append((v,j))
                    transfer = rng.randrange(2) == 0
                    actual.append((base_order+v if transfer else v,j))
                    moved += int(transfer)
            original = Counter((labels[i]+labels[j]) % k for i,j in edges)
            assert len(labels) == base_order
            full = labels+g
            actual.extend((base_order+i,base_order+(i+1) % k) for i in range(k) if i != mark)
            assert len(actual) == len(full)-1
            assert Counter(full) == Counter(labels)+Counter(range(k))
            assert Counter((full[i]+full[j]) % k for i,j in actual) == original+Counter(range(k))
            for freq in (Counter(full), Counter((full[i]+full[j]) % k for i,j in actual)):
                bins = [freq[v] for v in range(k)]
                assert max(bins)-min(bins) <= 1
            cases += 1
    return cases,moved


if __name__ == '__main__':
    print('prescribed progressions', check_cycles(), 'cyclic and product lifts', check_fibres())
    print('whole trees and transferred branches', *check_trees())

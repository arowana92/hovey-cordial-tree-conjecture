"""Test the unit-scaled period-chain criterion and its ordinary tree expansion."""
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import gcd
from random import Random

from .check_sparse_path_offsets import random_block


@lru_cache(None)
def factors(k):
    out = []
    p = 2
    while k>1:
        if k%p==0:
            exponent = 0
            while k%p==0:
                exponent += 1
                k //= p
            out.append((p,exponent))
        p += 1
    return tuple(out)


def valuation(x,p,a):
    for j in range(a):
        if x%p:
            return j
        x //= p
    return a


def local_test(k,word,target):
    for p,a in factors(k):
        vals = [valuation(x,p,a) for x in word]
        j = min(vals,default=a)
        t = valuation(target,p,a)
        if t<j:
            return False
        if j==a:
            continue
        m = vals.count(j)
        if p==2 and (target//(p**j)-m)%2:
            return False
        if p>2 and m==1 and t!=j:
            return False
    return True


@lru_cache(None)
def orbit(k,x):
    return tuple(sorted({u*x%k for u in range(1,k) if gcd(u,k)==1}))


def exact_sums(k,word):
    current = {0}
    for x in word:
        current = {(a+b)%k for a in current for b in orbit(k,x)}
    return current


def prefix_interval(k,word):
    bits = [(p,j,a) for p,a in factors(k) for j in range(a)]
    mask = 0
    seen = {0:0}
    for end,x in enumerate(word,1):
        for i,(p,j,a) in enumerate(bits):
            if valuation(x,p,a)==j:
                mask ^= 1<<i
        if mask in seen:
            return seen[mask],end
        seen[mask] = end
    return None


def extremal(k):
    if k==1:
        return ()
    p = factors(k)[0][0]
    half = tuple(p*x for x in extremal(k//p))
    return half+(1,)+half


def check_words():
    tested = exhaustive = 0
    for k in range(2,65):
        types = [x%k for x in range(1,k+1) if k%x==0]
        for size in range(1,5):
            for word in combinations_with_replacement(types,size):
                assert exact_sums(k,word)=={y for y in range(k) if local_test(k,word,y)}
                tested += 1
        threshold = 2**sum(a for _,a in factors(k))
        bad = extremal(k)
        assert len(bad)==threshold-1
        for start in range(len(bad)):
            for end in range(start+1,len(bad)+1):
                assert not local_test(k,bad[start:end],0)
        if len(types)**threshold <= 150000:
            for word in product(types,repeat=threshold):
                start,end = prefix_interval(k,word)
                assert 0 in exact_sums(k,word[start:end])
                exhaustive += 1
    print('orbit multisets',tested,'complete threshold words',exhaustive)


def multipliers(k,word,target):
    layers = [{0:None}]
    for x in word:
        next_layer = {}
        for s in layers[-1]:
            for u in range(1,k):
                if gcd(u,k)==1:
                    next_layer.setdefault((s+u*x)%k,(s,u))
        layers.append(next_layer)
    result = []
    for layer in reversed(layers[1:]):
        target,u = layer[target]
        result.append(u)
    assert target==0
    return result[::-1]


def make_piece(k,rng,target,periods):
    labels = []
    edges = []
    for _ in range(periods):
        internal,h,_,_ = random_block(k,rng)
        base = len(labels)
        shift = 0
        if base:
            old = rng.randrange(base)
            port = rng.randrange(k)
            edges.append((old,base+port))
            shift = labels[old]+port-h
        labels.extend((j+shift)%k for j in range(k))
        edges.extend((base+u,base+v) for u,v in internal)
    hist = Counter((labels[u]+labels[v])%k for u,v in edges)
    hole, = (x for x in range(k) if hist[x]==periods-1)
    assert all(hist[x]==periods for x in range(k) if x!=hole)
    left = rng.randrange(len(labels))
    right = labels.index((target+hole-labels[left])%k)
    return labels,edges,hole,left,right


def whole_trees():
    rng = Random(271991)
    totals = Counter()
    for k in range(2,49):
        threshold = 2**sum(a for _,a in factors(k))
        for trial in range(25):
            # Alternating between random coefficients and a longest bad prefix exercises
            # cancellations at the end as well as short interior subchains.
            word = ([rng.randrange(k) for _ in range(threshold)] if trial%2 else
                    list(extremal(k))+[rng.randrange(k)])
            start,end = prefix_interval(k,word)
            part = word[start:end]
            units = multipliers(k,part,0)
            order = rng.randrange(2,2*k+4)
            labels = [v%k for v in range(order)]
            edges = [(0,v) for v in range(2,order)]
            # Replace (0,1) in a cordially labeled ordinary star.
            old_vertex = Counter(labels)
            old_edge = Counter((labels[u]+labels[v])%k for u,v in edges+[(0,1)])
            previous = 0
            increment = 0
            for x,u in zip(part,units):
                q = rng.randrange(1,4)
                f,internal,h,p,r = make_piece(k,rng,x,q)
                base = len(labels)
                shift = labels[previous]+u*(f[p]-h)
                labels.extend((u*y+shift)%k for y in f)
                edges.extend((base+i,base+j) for i,j in internal)
                edges.append((previous,base+p))
                previous = base+r
                increment += q
                totals['pieces'] += 1
                totals['coincident ports'] += p==r
            edges.append((previous,1))
            assert len(edges)==len(labels)-1
            vcounts = Counter(labels)
            weights = Counter((labels[u]+labels[v])%k for u,v in edges)
            for v in range(k):
                assert vcounts[v]-old_vertex[v]==weights[v]-old_edge[v]==increment
            totals['trees'] += 1
    print('whole trees',dict(totals))


if __name__=='__main__':
    check_words()
    whole_trees()

"""Independent vector identities, binomial order checks, and whole-tree sums."""
from collections import Counter
from itertools import product
from random import Random

from .large_order_short_pools import cyclic_split, label


def split_ok(f):
    k = len(f)
    flag,h,g = cyclic_split(f)
    assert flag in (0,1) and (k%2==0 or flag==0)
    for row in (h,g):
        assert sum(row)==0 and sum(x*i for i,x in enumerate(row))%k==0
    assert min(g)>=-2 and max(g[i]+g[i-1] for i in range(k))<=3
    assert 2*min(h)>=min(f)-4
    out = [2*h[i]+g[i]+g[i-1] for i in range(k)]
    for i,x in enumerate((1,-2,1)):
        out[i] += flag*x
    assert out==list(f)
    return flag


def subdivided(k,leaves,n,style,rng):
    # Generate an unrooted ternary skeleton by splitting edges at random.
    edges = [(0,1)]
    h = 2
    for j in range(2,leaves):
        a,b = edges.pop(rng.randrange(len(edges)) if style%2 else -1)
        edges.extend(((a,h),(h,b),(h,h+1)))
        h += 2
    gaps = [0]*len(edges)
    if style==0:
        gaps[-1] = n-h
    elif style==1:
        for j in range(n-h):
            gaps[j%len(gaps)] += 1
    else:
        for j in range(n-h):
            gaps[rng.randrange(len(gaps))] += 1
    adj = [[] for _ in range(n)]
    next_id = h
    for (a,b),g in zip(edges,gaps):
        chain = [a]+list(range(next_id,next_id+g))+[b]
        next_id += g
        for x,y in zip(chain,chain[1:]):
            adj[x].append(y)
            adj[y].append(x)
    root = rng.randrange(n)
    todo = [root]
    index = {root:0}
    parents = [-1]
    for v in todo:
        for x in adj[v]:
            if x not in index:
                index[x] = len(todo)
                parents.append(index[v])
                todo.append(x)
    assert len(parents)==n
    return parents


def main():
    rng = Random(261128)
    vectors = flags = trees = vertices = 0
    for k in range(3,10):
        for f in product((-1,0,1),repeat=k):
            if sum(f)==0 and sum(i*x for i,x in enumerate(f))%k==0:
                flags += split_ok(f)
                vectors += 1
    for k in list(range(3,157))+[254,255,256,1024,4095]:
        for r in range(3):
            f = [0]*k
            for _ in range(k):
                a,b,c = (rng.randrange(k) for _ in range(3))
                for i,z in ((a,1),(a+b,-1),(a+c,-1),(a+b+c,1)):
                    f[i%k] += z
            flags += split_ok(f)
            vectors += 1
    for k in (5,6,7,8,9,13):
        for style in range(3):
            n = 66*k+(k if style==2 else 1+style)
            parents = subdivided(k,k+1 if style else 2,n,style,rng)
            degrees = Counter(parents[1:])
            root = next(i for i in range(n) if (degrees[i]+(i>0)==2) == (style==0))
            f = label(k,parents,root)
            assert f[root]==0
            assert len(f)==n and all(0<=x<k for x in f)
            actual = Counter((f[v]+f[p])%k for v,p in enumerate(parents) if v)
            for hist in (Counter(f),actual):
                rows = [hist[r] for r in range(k)]
                assert max(rows)-min(rows)<=1
            v = Counter(f)
            diff = [v[r]-actual[r] for r in range(k)]
            assert sorted(diff)==[0]*(k-1)+[1]
            gap = diff.index(1)
            for j in range(3*k+1):
                assert max(v[r] for r in range(k))-min(v[r] for r in range(k))<=1
                assert max(actual[r] for r in range(k))-min(actual[r] for r in range(k))<=1
                low = min(v[r] for r in range(k))
                x = gap if v[gap]==low else next(r for r in range(k) if v[r]==low)
                v[x] += 1
                actual[(x+f[root])%k] += 1
            trees += 1
            vertices += n
    print('cyclic vectors',vectors,'unit squares',flags,'trees',trees,'vertices',vertices)


if __name__=='__main__':
    main()

"""Recount actual replacement paths, old trees, and target obstructions."""
from collections import Counter
from itertools import combinations
from random import Random

from .euler_subdivision import approximate_tree, bfs_padding, circuit, extend, one_neighbor, subset_sum


def counts(values,k):
    hist = Counter(values)
    return [hist[i] for i in range(k)]


def balanced(row):
    return max(row)-min(row) <= 1


def weights(k,parents,f):
    return [(f[i]+f[p])%k for i,p in enumerate(parents) if i]


def substituted(k,parents,child,f,row):
    a,b = f[parents[child]],f[child]
    keep = [(f[i]+f[p])%k for i,p in enumerate(parents) if i and i != child]
    keep.extend((x+y)%k for x,y in zip([a]+row,row+[b]))
    assert balanced(counts(f+row,k)) and balanced(counts(keep,k))


def high(row,k,rng):
    q,r = divmod(row,k)
    h = set(rng.sample(range(k),r))
    return [q+int(i in h) for i in range(k)]


def algebraic_targets(k,n):
    moments = set()
    for a in combinations(range(k),n%k):
        for b in combinations(range(k),(n-1)%k):
            sv = (n//k)*sum(range(k))+sum(a)
            se = ((n-1)//k)*sum(range(k))+sum(b)
            moments.add((2*sv-se)%k)
    return moments


def main():
    rng = Random(281126)
    subsets = margins = forbidden = trees = skeletons = singles = 0
    for k in range(2,66):
        for r in range(1,k):
            for target in range(k):
                values = subset_sum(k,r,target)
                assert len(values)==len(set(values))==r and all(0<=x<k for x in values)
                assert sum(values)%k==target
                subsets += 1
    for k in range(1,25):
        for j in range(75):
            n = rng.randrange(2,4*k+3)
            t = 3*k+j%(2*k+1)
            v,w = high(n,k,rng),high(n-1,k,rng)
            a,b = rng.randrange(k),rng.randrange(k)
            inv = sum(i*(2*x-y) for i,(x,y) in enumerate(zip(v,w)))%k
            possible = (k%2 or (n+t)%k!=1 or
                        (inv-(n+t)//k*sum(range(k)))%2==0)
            if k<=7:
                assert bool(possible)==(inv in algebraic_targets(k,n+t))
            try:
                row = extend(v,w,t,a)
            except ValueError:
                assert not possible
                forbidden += 1
                continue
            assert possible and len(row)==t
            gains = counts([(x+y)%k for x,y in zip([a]+row,row+[b])],k)
            gains[(a+b)%k] -= 1
            assert balanced([x+y for x,y in zip(v,counts(row,k))])
            assert balanced([x+y for x,y in zip(w,gains)])
            margins += 1
        for j in range(20):
            n = rng.randrange(2,100)
            parents = [-1]+sorted(rng.randrange(i) for i in range(1,n))
            child = rng.randrange(1,n)
            t = n+3*k-3+j
            f,row = bfs_padding(k,parents,child,t)
            assert len(row)==t and len(f)==n
            substituted(k,parents,child,f,row)
            trees += 1
    # Independently prescribe a strongly connected arc multiset with unequal
    # row sums. Only the two histograms, not the original arcs, reach the code.
    walks = 0
    for k in range(2,19):
        for j in range(15):
            path = list(range(k))*3
            rng.shuffle(path)
            path += [rng.randrange(k) for _ in range(j+1)]
            v = counts(path,k)
            e = counts([(x+y)%k for x,y in zip(path,path[1:]+path[:1])],k)
            # Add two copies of every weight per layer with the directed
            # loops and successor arcs. This also increases each vertex by two.
            gap = max(v)-min(v)
            v = [x+2*(gap+1) for x in v]
            e = [x+2*(gap+1) for x in e]
            a = rng.randrange(k)
            heads = circuit(v,e,a)
            assert heads[-1]==a and counts(heads,k)==v
            assert counts([(x+y)%k for x,y in zip([a]+heads,heads)],k)==e
            walks += 1
    for k in range(1,13):
        for j in range(24):
            ps = [rng.randrange(k) for _ in range(j)]
            labels = one_neighbor(k,ps)
            v = counts(labels,k)
            w = counts([(a+b)%k for a,b in zip(ps,labels)],k)
            assert max(v)-min(v)<=2 and max(w)-min(w)<=2 and k*max(w)<=j+k
            singles += 1
    for k in range(2,8):
        for j in range(9):
            n = 5+3*j
            p = [-1]+[rng.randrange(i) if i%3==0 else i-1 for i in range(1,n)]
            f = approximate_tree(k,p)
            vs,es = counts(f,k),counts(weights(k,p,f),k)
            h = sum((p.count(i)+(i>0))!=2 for i in range(n))
            cap = (2*h-3+k-1)//k
            assert max(vs)-min(vs)<=11 and k*max(es)<=n-1+k*(cap+9)
            t = (k*(31+cap) if k%2==0 else k*(21+cap))
            if (n+t)%k==1:
                t += 1
            child = rng.randrange(1,n)
            row = extend(vs,es,t,f[p[child]])
            substituted(k,p,child,f,row)
            skeletons += 1
    print('subset sums',subsets,'balanced inputs',margins,'parity obstructions',forbidden,
          'padded trees',trees,'prescribed circuits',walks,'one-neighbor lists',singles,
          'rounded whole trees',skeletons)


if __name__ == '__main__':
    main()

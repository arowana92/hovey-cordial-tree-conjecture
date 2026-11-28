"""Check collisions from a specified equal-label pair, including distance two."""
from collections import Counter
from itertools import combinations, permutations, product
from random import Random

from check import adjacency
from shifted_ring import construct
from sparse_offsets import edge


def quotient(edges, r, y):
    n=len(edges)
    v=[(r if i==y else i) for i in range(n+1)]
    ids={x:j for j,x in enumerate(sorted(set(v)))}
    return [edge(ids[v[a]],ids[v[b]]) for a,b in edges],ids[r]


def exception(edges, r, y, k):
    n=len(edges)
    t=n//k
    deg=Counter(v for e in edges for v in e)
    leaves=sum(d==1 for d in deg.values())
    q=leaves-int(deg[r]==1)-int(deg[y]==1)
    es,s=quotient(edges,r,y)
    if (s,s) in es:
        return t==1 and k%2==1 and max(deg.values())==2 and min(deg[r],deg[y])==1
    if len(set(es))<n:
        return t==1
    if q==0:
        return (t*k*(k-1)//2)%k!=0
    return q==1 and t==1 and k%2==1


def small():
    counts=Counter()
    for n,k in ((4,2),(4,4),(5,5),(6,3),(6,6),(7,7),(8,2),(8,4)):
        path=[(i-1,i) for i in range(1,n+1)]
        fork=path[:-1]+[(1,n)]
        for es in (path,fork):
            for r,y in combinations(range(n+1),2):
                merged,s=quotient(es,r,y)
                attained=False
                if k==n:
                    rows=permutations(range(n))
                else:
                    rows=product(range(k),repeat=n)
                for x in rows:
                    if x[s] or any(x.count(c)!=n//k for c in range(k)):
                        continue
                    bins=Counter((x[a]+x[b])%k for a,b in merged)
                    if all(bins[c]==n//k for c in range(k)):
                        attained=True
                        break
                failed=exception(es,r,y,k)
                assert not (failed and attained)
                counts['literal solutions' if attained else 'necessary exclusions' if failed
                       else 'additional small failures']+=1
    return counts


def digons():
    rng=Random(271119)
    cases=Counter()
    for n in (414,625,810):
        path=[(i-1,i) for i in range(1,n+1)]
        fork=path[:-2]+[(1,n-1),(1,n)]
        binary=[((v-1)//2,v) for v in range(1,n+1)]
        for tree,r,y in ((path,0,2),(path,3,5),(fork,n-1,n),(binary,3,4)):
            es,s=quotient(tree,r,y)
            repeated,=[e for e,c in Counter(es).items() if c==2]
            degree=Counter(v for e in es for v in e)
            leaf_count=sum(d==1 for d in degree.values())
            for k in sorted({k for k in (1,2,3,5,9,n//2,n//3,n//5) if k<n and n%k==0}):
                # Give the second copy offset k. Choose the offset of one
                # remote edge so that the total is 0, or k for an odd one-leaf order.
                total=k if leaf_count==1 and n%2 else 0
                remote=next(e for e in es if e!=repeated and not set(e)&set(repeated))
                offsets={remote:(total-k)%n}
                aux=construct(es,offsets,rng,cap=4,parallel=(repeated,k))
                assert aux is not None
                kept,closing,w,pins,core=aux
                assert closing==repeated and s in pins and all(core[v]==v0 for v,v0 in pins.items())
                assert (sum(pins[v] for v in closing)+k)%n==w
                assert max(map(len,adjacency(n,kept)))<=6
                assert sum(core.values())%n==sum(range(n))%n
                d=Counter(v for e in kept for v in e)
                assert (sum(d[v]*x for v,x in core.items())+w-sum(range(n)))%n==0
                for point in (pins,core):
                    original=Counter((point[a]+point[b]+offsets.get((a,b),0))%n
                                     for a,b in set(es) if a in point and b in point)
                    original[(sum(point[v] for v in closing)+k)%n]+=1
                    actual=Counter((point[a]+point[b])%n for a,b in kept if a in point and b in point)
                    assert w not in actual
                    actual[w]+=1
                    assert actual==original and max(actual.values())==1
                assert all(x%k==0 for x in offsets.values()) and k%n
                cases['digon cores']+=1
                cases['one-leaf cores']+=int(leaf_count==1)
            assert construct(es,{},rng,parallel=(repeated,0)) is None
    return cases


if __name__=='__main__':
    print(dict(digons()),dict(small()))

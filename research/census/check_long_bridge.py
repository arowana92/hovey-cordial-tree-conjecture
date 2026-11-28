"""Count every actual edge after joining arbitrarily precolored components."""
from random import Random

from .long_bridge import blocks_needed,bridge,pinned_path,realize,subset_sum


def counts(k,values):
    hist = [0]*k
    for x in values:
        hist[x%k] += 1
    return hist


def inputs(k,rng):
    n = rng.randrange(2,25)
    parent = [rng.randrange(v) for v in range(1,n)]
    x = [rng.randrange(k) for _ in range(n)]
    if rng.randrange(4) == 0:
        x = [x[0]]*n
    return x, [(u,v) for v,u in enumerate(parent,1)], rng.randrange(n)


def main():
    rng = Random(2761991)
    success = rejected = arbitrary = subsets = 0
    for k in range(2,65):
        for size in range(1,k):
            for target in range(k):
                values = subset_sum(k,size,target)
                assert len(values) == len(set(values)) == size and min(values)>=0 and max(values)<k
                assert sum(values)%k==target
                subsets += 1
    for k in range(2,27):
        for i in range(40):
            left,first,u = inputs(k,rng)
            right,second,v = inputs(k,rng)
            end = len(left)+v
            both = left+right
            edges = first+[(j+len(left),l+len(left)) for j,l in second]
            a,b = both[u],both[end]
            n = len(both)
            vertex = counts(k,both)
            edge = counts(k,(both[j]+both[l] for j,l in edges))
            q0 = 2 if k%4==0 else 1
            r = (1-n)%k if i%3==0 else rng.randrange(k)
            s = blocks_needed(vertex,edge,r)
            t = s*(q0*k+1) + k*rng.randrange(3)
            row = bridge(a,b,t,vertex,edge)
            chain = [u]+list(range(n,n+t))+[end]
            full_edges = edges+list(zip(chain,chain[1:]))
            degree = [0]*(n+t)
            for j,l in full_edges:
                degree[j]+=1
                degree[l]+=1
            odd_sum = sum(both[j] for j in range(n) if degree[j]%2)
            obstruction = k%2==0 and (n+t)%k==1 and (odd_sum-((n+t-1)//k)*sum(range(k)))%2
            assert (row is None) == bool(obstruction)
            if row is None:
                rejected += 1
            else:
                labels = both+row
                assert len(row)==t
                for hist in (counts(k,labels),counts(k,(labels[j]+labels[l] for j,l in full_edges))):
                    assert max(hist)-min(hist)<=1
                success += 1
            # Choose concentrated extras and arbitrary joining weights; force only
            # the last weight by the two endpoints, then recover the requested histograms.
            periods = (t-s)//k
            extras = [rng.randrange(k//2+1) for _ in range(s)]
            joins = [rng.randrange(k//2+1) for _ in range(s)]
            joins.append((a+b+periods*sum(range(k))+2*sum(extras)-sum(joins))%k)
            fv = [old+periods+c for old,c in zip(vertex,counts(k,extras))]
            fe = [old+periods+c for old,c in zip(edge,counts(k,joins))]
            row = realize(a,b,t,vertex,edge,fv,fe,s)
            labels = both+row
            assert counts(k,labels)==fv and counts(k,(labels[j]+labels[l] for j,l in full_edges))==fe
            arbitrary += 1
    paths = impossible = 0
    for k in range(2,27):
        d = k*((2 if k%4==0 else 1)*k+1)+2*k-1
        for step in range(12):
            sites = [0]
            for _ in range(1+step%5):
                sites.append(sites[-1]+d+rng.randrange(k))
            sites[-1] += (-sites[-1])%k
            n = sites[-1]+1
            pins = {i:rng.randrange(k) for i in sites}
            if step%3==1:
                n += k
                pins[n-1] = pins.pop(sites[-1])
            if step%3==2:
                n += 2
                pins = {i+1:x for i,x in pins.items()}
            if step%4==1:
                n += k
            obstruction = (k%2==0 and n%k==1 and 0 in pins and n-1 in pins
                           and (pins[0]+pins[n-1]-(n//k)*sum(range(k)))%2)
            row = pinned_path(k,n,pins)
            assert (row is None) == bool(obstruction)
            if row is None:
                impossible += 1
                continue
            assert len(row)==n and all(row[i]==x for i,x in pins.items())
            for hist in (counts(k,row),counts(k,(x+y for x,y in zip(row,row[1:])))):
                assert max(hist)-min(hist)<=1
            paths += 1
    print(paths,"multiply prescribed paths,",impossible,"impossible endpoint pairs")
    print(subsets,"subset sums,",success,"cordial completions,",rejected,"parity obstructions,",
          arbitrary,"prescribed histogram pairs")


if __name__ == '__main__':
    main()

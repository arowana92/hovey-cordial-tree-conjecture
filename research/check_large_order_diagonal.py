"""Recount second differences, sparse graph labels, supply rows and actual switches."""

from itertools import product
from random import Random
from research.large_order_diagonal import squared_terms
from research.large_order_subdivision import round_groups
from research.large_order_switches import run


def rebuild(f):
    k = len(f)
    result = [0]*k
    tables = squared_terms(f)
    for stride, table in tables.items():
        assert stride & (stride-1) == 0
        for i,v in enumerate(table):
            result[i] += v
            result[(i+stride)%k] -= 2*v
            result[(i+2*stride)%k] += v
    assert list(f)==result
    return max((abs(x) for row in tables.values() for x in row),default=0)


def check_phases(k, rng):
    # Each variable represents up to two nonadjacent raw tree vertices.
    n=53
    raw=[-1]+[rng.randrange(i) for i in range(1,n)]
    depth=[0]*n
    for v,p in enumerate(raw[1:],1):
        depth[v]=depth[p]+1
    groups=[]
    for parity in (0,1):
        indices=[v for v in range(n) if depth[v]%2==parity]
        rng.shuffle(indices)
        groups += [indices[i:i+2] for i in range(0,len(indices),2)]
    owner={v:i for i,g in enumerate(groups) for v in g}
    adj=[[] for _ in groups]
    for v,p in enumerate(raw[1:],1):
        i,j=owner[v],owner[p]
        assert i!=j
        adj[i].append(j);adj[j].append(i)
    live=set(range(len(groups)))
    layers=[]
    while live:
        forbidden=set()
        layer=[]
        for i in sorted(live):
            if i not in forbidden and sum(j in live for j in adj[i])<=8:
                layer.append(i)
                forbidden.update(adj[i])
        assert layer and len(layer)*18>=len(live)
        live.difference_update(layer)
        layers.append(layer)
    offsets=[rng.randrange(k) for _ in raw]
    values=[None]*n
    hist=[0]*(2*k)
    for layer in reversed(layers):
        possible=[]
        for i in layer:
            cols=[]
            for base in range(k):
                col=[0]*(2*k)
                for v in groups[i]:
                    x=(base+offsets[v])%k
                    col[x]+=1
                    for j,p in enumerate(raw):
                        other=p if j==v else j if p==v else -1
                        if other>=0 and values[other] is not None:
                            col[k+(x+values[other])%k]+=1
                cols.append(col)
            possible.append(cols)
        for i,base,cols in zip(layer,round_groups(possible,2*k),possible):
            for v in groups[i]:values[v]=(base+offsets[v])%k
            hist=[x+y for x,y in zip(hist,cols[base])]
    expected=[values.count(a) for a in range(k)]
    sums=[(values[i]+values[p])%k for i,p in enumerate(raw) if i]
    assert hist==expected+[sums.count(a) for a in range(k)]
    for start,total in ((0,n),(k,n-1)):
        assert all(abs(k*x-total)<=20*k*len(layers) for x in hist[start:start+k])


def check_supply(k):
    # Include the type and x quotas in the same rounding as both histograms.
    groups=[]
    for i in range(30):
        p=(i*i+1)%k
        s=1+(i%2);q=(p-s)%k
        cols=[]
        for x in range(k):
            col=[0]*(4*k)
            for parent,value in ((p,x),(q,(x+2*s)%k)):
                col[value]+=1
                col[k+(parent+value)%k]+=1
            col[(2+i%2)*k+x]+=1
            cols.append(col)
        groups.append(cols)
    picks=round_groups(groups,4*k)
    hist=[sum(g[j][a] for g,j in zip(groups,picks)) for a in range(4*k)]
    assert all(abs(k*x-60)<=10*k for x in hist[:2*k])
    assert all(abs(k*x-15)<=10*k for x in hist[2*k:])


if __name__=='__main__':
    rng=Random(153942)
    exhaustive=0
    largest=0
    for k in range(2,11):
        for f in product((-1,0,1),repeat=k):
            if not sum(f) and not sum(i*x for i,x in enumerate(f))%k:
                largest=max(largest,rebuild(f))
                exhaustive+=1
    for k in range(2,202):
        f=[0]*k
        for _ in range(5*k):
            x,a,b=(rng.randrange(k) for _ in range(3))
            f[x]+=1;f[(x+a+b)%k]+=1;f[(x+a)%k]-=1;f[(x+b)%k]-=1
        largest=max(largest,rebuild(f))
    trials=[run(k,leaf,64,True) for k in (5,6,8,9,10,13) for leaf in (False,True)]
    for k in (3,4,5,6):
        check_phases(k,rng)
        check_supply(k)
    print(f"{exhaustive} exhaustive vectors, 200 larger reconstructions, largest "
          f"observed coefficient {largest}; four contracted-tree and quota checks.")
    print(f"{len(trials)} whole trees, up to {max(n for n,_ in trials)} vertices; "
          f"{sum(w for _,w in trials)} diagonal switches applied.")

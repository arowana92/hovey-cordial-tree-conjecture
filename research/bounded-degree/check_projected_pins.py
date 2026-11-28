"""Validate the large-group embedding conditions and recompute all projected counts."""
from collections import Counter
from itertools import product
from math import gcd
from random import Random

from projected_pins import cordial_targets,prepare


def inspect(k,edges,pins,vcounts,ecounts,result,cap):
    N,aux,copies,marks,V,E = result
    n = len(edges)+1
    assert len(V)==n and len(E)==n-1 and max(V|E)<N and min(V|E)>=0
    vc,ec = Counter(x%k for x in V),Counter(x%k for x in E)
    assert [vc[i] for i in range(k)]==vcounts and [ec[i] for i in range(k)]==ecounts
    assert len(set(marks.values()))==len(marks) and set(marks.values())<=V
    assert all(marks[v]%k==x for v,x in pins.items())
    assert all(marks[z]%k==marks[v]%k for z,v in copies.items())
    assert len(aux)==n-1
    adj = [set() for _ in range(n)]
    for u,v in aux:
        assert u!=v and v not in adj[u]
        adj[u].add(v)
        adj[v].add(u)
    todo,seen = [0],{0}
    for v in todo:
        for u in adj[v]-seen:
            seen.add(u)
            todo.append(u)
    assert len(seen)==n and max(map(len,adj))<=cap+1
    sums = [(marks[u]+marks[v])%N for u,v in aux if u in marks and v in marks]
    assert len(sums)==len(set(sums)) and set(sums)<=E
    for d in set(map(len,adj)):
        sites = {i for i,nb in enumerate(adj) if len(nb)==d}
        h = len(sites & marks.keys())
        assert h==len(sites) or min(h,len(sites)-h)>=6
    assert (sum(marks.values())-sum(V))%N==0
    assert (sum(len(adj[v])*x for v,x in marks.items())-sum(E))%N==0
    # Restore cut edges on a full trial labeling, holding all protected values.
    low = [marks.get(v,19*v+3)%k for v in range(n)]
    assert Counter((low[u]+low[v])%k for u,v in edges)==Counter((low[u]+low[v])%k for u,v in aux)



def linear_fibers():
    total = 0
    for k in range(2,11):
        for ds in product((1,2,4,7),repeat=3):
            actual = {(sum(xs)%k,sum(d*x for d,x in zip(ds,xs))%k)
                      for xs in product(range(k),repeat=len(ds))}
            g = gcd(k,ds[1]-ds[0],ds[2]-ds[0])
            predicted = {(a,b) for a,b in product(range(k),repeat=2) if (b-ds[0]*a)%g==0}
            assert actual==predicted
            total += k*k
    return total


def noncordial_targets():
    # A tree with degree classes 1 and 4 forces a mod-three relation.
    k,h = 9,1060
    edges = [(i-1,i) for i in range(1,h)]
    v = h
    for i in range(h):
        for _ in range(2+int(i in (0,h-1))):
            edges.append((i,v))
            v += 1
    cases = 0
    for tt,cap in ((edges,4), ([(i-1,i) for i in range(1,v)],3)):
        pins = {0:3,v-1:3}
        vs,es = cordial_targets(k,tt,pins)
        assert prepare(k,tt,pins,vs,es,cap) is not None
        for shift in (1,2,4,5):
            bad = es.copy()
            bad[0] -= 1
            bad[shift] += 1
            assert prepare(k,tt,pins,vs,bad,cap) is None
            cases += 1
    return cases

def run():
    rng = Random(48192)
    good = impossible = arbitrary = copies = 0
    for k in (5,8,9,14,17,25):
        for r in (0,1,2,k-1):
            n = 350*k+r
            path = [(i-1,i) for i in range(1,n)]
            binary = [((i-1)//2,i) for i in range(1,n)]
            hubs = [(i-1,i) for i in range(1,n-20)]+[(2+(i%2),i) for i in range(n-20,n)]
            for shape,edges in enumerate((path,binary,hubs)):
                for index in range(3):
                    pins = {i:2%k for i in range(8)}
                    pins.update({0:index,n-1:(index+1)%k,20:rng.randrange(k)})
                    if index==2:
                        pins.pop(n-1)
                    targets = cordial_targets(k,edges,pins)
                    degree = Counter(v for e in edges for v in e)
                    odd = {v for v,d in degree.items() if d%2}
                    blocked = (k%2==0 and r==1 and odd<=pins.keys() and
                               (sum(pins[v] for v in odd)-(n//k)*sum(range(k)))%2)
                    assert (targets is None)==bool(blocked)
                    if targets is None:
                        impossible += 1
                        continue
                    ans = prepare(k,edges,pins,*targets,3)
                    assert ans is not None
                    inspect(k,edges,pins,*targets,ans,3)
                    good += 1
                    copies += len(ans[2])
                    # Obtain necessary moments from a full arbitrary coloring with repeats.
                    # Adding zero-moment bin changes can give profiles with spread above one.
                    low = list(range(n))
                    for v in range(n): low[v] %= k
                    for v,x in pins.items(): low[v]=x
                    masses = Counter(low)
                    sums = Counter((low[u]+low[v])%k for u,v in edges)
                    for hist,total in ((masses,n),(sums,n-1)):
                        target = sum(x*t for x,t in hist.items())%k
                        for x in range(k): hist[x]=total//k
                        for j in range(total%k): hist[j]+=1
                        delta = (target-sum(x*t for x,t in hist.items()))%k
                        hist[0]-=1
                        hist[delta]+=1
                    vc,ec = [masses[x] for x in range(k)],[sums[x] for x in range(k)]
                    custom = prepare(k,edges,pins,vc,ec,3)
                    assert custom is not None
                    inspect(k,edges,pins,vc,ec,custom,3)
                    arbitrary += 1
    print(good,"cordial target pairs,",impossible,"parity obstructions,",
          arbitrary,"prescribed profile pairs,",copies,"replicated attachment labels")


if __name__ == '__main__':
    print(linear_fibers(),"literal moment tests,",noncordial_targets(),"incompatible frequency pairs")
    run()

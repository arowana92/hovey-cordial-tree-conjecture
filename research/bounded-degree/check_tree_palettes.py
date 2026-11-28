"""Recount the palettes, induced edges and embedding moments on the actual trees."""
from collections import Counter
from functools import reduce
from itertools import product
from math import gcd
from random import Random

from check import adjacency
from edge_histogram import construct_histograms
from tree_palettes import lift_tree


def allowed(edges, root, a, vertices, weights, bias):
    n, k = len(edges)+1,len(vertices)
    degree = Counter(v for pair in edges for v in pair)
    if not vertices[a]:
        return False
    vtotal = sum(x*c for x,c in enumerate(vertices))
    etotal = sum(x*c for x,c in enumerate(weights))-sum(bias.values())
    target = etotal-vtotal-(degree[root]-1)*a
    if target%reduce(gcd,(degree[v]-1 for v in range(n) if v!=root),k):
        return False
    if max(degree.values())<=2 and degree[root]==1:
        other = (2*vtotal-etotal-a)%k
        return vertices[other]>int(other==a)
    return True


def audit(edges, root, a, vertices, weights, bias, rng):
    k,n = len(vertices),len(edges)+1
    N = ((n+k-1)//k)*k
    data = lift_tree(edges,root,a,vertices,weights,bias)
    assert (data is not None)==allowed(edges,root,a,vertices,weights,bias)
    if data is None:
        return False
    vh,vextra,eh,extra,shift,base = data
    va = set(range(N))-set(vh)
    true_vertices = Counter(va)
    true_vertices.update(vextra)
    temp_va = va | set(vh[:len(vextra)])
    true_edges = Counter(set(range(N))-set(eh))
    true_edges.update(extra)
    colors = set(range(N))-set(eh[len(extra):])
    for x in range(k):
        assert sum(true_vertices[y] for y in range(x,N,k))==vertices[x]
        assert sum(true_edges[y] for y in range((x-base)%k,N,k))==weights[x]
    for u,v in edges:
        e = tuple(sorted((u,v)))
        assert (shift.get(e,0)+base-bias.get(e,0))%k==0
    result = construct_histograms(edges,None,root,a,eh,extra,rng,cap=4,offsets=shift,
                                  vertex_holes=vh,vertex_extra=vextra)
    assert result is not None
    (tree,_,_,pins,labels),donors,temporary,switches = result
    assert pins[root]==a and all(labels[v]==x for v,x in pins.items())
    assert len(set(labels.values()))==len(labels) and set(labels.values())<=temp_va
    adj = adjacency(n,tree)
    reach,stack={0},[0]
    for v in stack:
        for w in adj[v]-reach:
            reach.add(w)
            stack.append(w)
    assert len(tree)==n-1 and len(reach)==n and max(map(len,adj))<=6
    assert (sum(labels.values())-sum(temp_va))%N==0
    assert (sum(len(adj[v])*x for v,x in labels.items())-sum(colors))%N==0
    for d,t in Counter(map(len,adj)).items():
        inside = sum(len(adj[v])==d for v in labels)
        assert inside==t or min(inside,t-inside)>=6
    original_pairs,aux_pairs = (set(tuple(sorted(e)) for e in es) for es in (edges,tree))
    assert all(u in pins and v in pins for u,v in (original_pairs^aux_pairs)|set(temporary))
    assert sorted(p for _,p in switches.values())==sorted(vextra)
    for point in (pins,labels):
        actual = point.copy()
        for v,(q,p) in switches.items():
            assert point[v]==q
            actual[v] = p
        assert Counter(actual.values())-Counter(point.values())==Counter(vextra)
        old = Counter((actual[u]+actual[v]+shift.get((u,v),0))%N for u,v in original_pairs
                      if u in point and v in point)
        aux = Counter((point[u]+point[v])%N for u,v in aux_pairs if u in point and v in point)
        assert set(aux)<=colors and all(c==1 for c in aux.values())
        old.update(eh[:len(donors)])
        aux.update(extra)
        assert old==aux
    return True


def suite():
    rng = Random(272711)
    counts = Counter()
    for n,k in ((1258,1260),(1258,420),(1258,7),(1258,3),(1257,3),(1513,1515),(1513,303),(1513,1)):
        h = (n+k-1)//k
        path = [(i-1,i) for i in range(1,n)]
        binary = [((i-1)//2,i) for i in range(1,n)]
        bush = path[:-15]+[(0,v) for v in range(n-15,n)]
        trees = [(path,0),(path,n//2),(binary,3),(bush,0)]
        if n%3==0:
            ternary = [(0,1),(0,2)]+[(s//3,v) for s in range(3,n,3) for v in range(s,s+3)]
            trees.append((ternary,0))
        for es,r in trees:
            for trial in range(8):
                vs = [h]*k
                for _ in range(k*h-n):
                    x = rng.choice([x for x,c in enumerate(vs) if c])
                    vs[x]-=1
                if trial>=4 and k>1:
                    p = rng.randrange(k)
                    for _ in range(min(3,n-vs[p])):
                        q = rng.choice([x for x in range(k) if x!=p and vs[x]])
                        vs[q]-=1
                        vs[p]+=1
                ws = vs.copy()
                ws[rng.choice([x for x,c in enumerate(ws) if c])]-=1
                if trial%2 and k>1:
                    p = rng.randrange(k)
                    for _ in range(min(4,n-vs[p])):
                        q = rng.choice([v for v in range(k) if v!=p and ws[v]>0])
                        ws[q]-=1
                        ws[p]+=1
                shifts = {tuple(sorted(e)):rng.randrange(k) for e in rng.sample(es,4)}
                a = vs.index(max(vs)) if trial==6 else rng.randrange(k)
                if es is path and r==0:
                    # Force the other endpoint onto the root color, or an absent one.
                    far = a if trial%3==0 else next((x for x,c in enumerate(vs) if not c),a)
                    vtotal,etotal=(sum(x*c for x,c in enumerate(bins)) for bins in (vs,ws))
                    e = tuple(sorted(es[0]))
                    shifts[e]=(shifts.get(e,0)+a+far-2*vtotal+etotal-sum(shifts.values()))%k
                if trial%3==2:
                    shifts = {tuple(sorted(e)):(1+shifts.get(tuple(sorted(e)),0))%k for e in es}
                    ws = [ws[(x-1)%k] for x in range(k)]
                passed = audit(es,r,a,vs,ws,shifts,rng)
                counts['accepted' if passed else 'rejected']+=1
                if passed and es is path and r==0: counts['path ends with equal projected color']+=int(
                    (sum(x*(2*v-w) for x,(v,w) in enumerate(zip(vs,ws)))+sum(shifts.values())-2*a)%k==0)
                if passed and max(vs)>h: counts['vertex overflows']+=1
                if passed and max(vs)>1 and h==1 and es is path and r==0 and trial==6:
                    counts['equal endpoints requiring a vertex switch upstairs']+=1
                if passed and max(ws)>h: counts['edge overflows']+=1
                if passed and max(map(len,adjacency(n,es)))>4: counts['degree reductions']+=1
    return counts


def literal():
    # Compare the necessary tests and the lift with histograms from complete labelings.
    cases = 0
    for n,k in ((4,5),(5,4),(6,3),(7,2)):
        path = [(v-1,v) for v in range(1,n)]
        fork = path[:-1]+[(1,n-1)]
        for edges,r in ((path,0),(path,2),(fork,0)):
            shifts = {edges[0]:1, edges[-1]:k-1}
            for x in product(range(k),repeat=n):
                vcount = [x.count(a) for a in range(k)]
                sums = [(x[u]+x[v]+shifts.get((u,v),0))%k for u,v in edges]
                ecount = [sums.count(a) for a in range(k)]
                assert allowed(edges,r,x[r],vcount,ecount,shifts)
                assert lift_tree(edges,r,x[r],vcount,ecount,shifts) is not None
                cases += 1
    return cases


if __name__=='__main__':
    print(dict(suite()), 'literal labelings',literal())

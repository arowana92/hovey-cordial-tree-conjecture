"""Independently recount repaired palettes, embedding targets and literal trees."""
from collections import Counter
from math import gcd
from random import Random

from check import adjacency
from two_leaf_repair import build, transfer


def coefficients_tree(k,t,g,mixed):
    n = (k+t-2)//g
    assert n*g==k+t-2
    ports = [2*i+1 for i in range(t)]
    degrees = [g+1-(v in ports) for v in range(n)]
    if mixed:
        # The frequent coefficient is six, but the gcd of all coefficients is two.
        degrees[-3] -= 2
        degrees[-5] += 2
    edges = [(i-1,i) for i in range(1,n)]
    tip = n
    for v,d in enumerate(degrees):
        for _ in range(d-2+(v in (0,n-1))):
            edges.append((v,tip))
            tip += 1
    assert tip==k
    return edges,ports


def inspect(k,edges,ports,old,removed,edge_high,vertex_high,data):
    aux,labels,absent,dup,gap,holes = data
    active = set(range(k))-{absent}
    assert set(labels)<=active
    pairs = {frozenset(e) for e in aux}
    assert len(aux)==len(pairs)==len(active)-1
    adj = adjacency(k,aux)
    start = next(iter(active))
    seen,stack = {start},[start]
    while stack:
        v = stack.pop()
        for u in adj[v]-seen:
            stack.append(u)
            seen.add(u)
    assert active==seen
    vertex_palette = set(range(k))-({gap} if absent is not None else set())
    edge_palette = set(range(k))-set(holes)
    assert len(vertex_palette)==len(active) and len(edge_palette)==len(aux)
    assert len(labels)==len(set(labels.values())) and set(labels.values())<=vertex_palette
    assert (sum(labels.values())-sum(vertex_palette))%k==0
    weights = [(labels[u]+labels[v])%k for u,v in aux if u in labels and v in labels]
    assert len(weights)==len(set(weights)) and set(weights)<=edge_palette
    assert (sum(len(adj[v])*x for v,x in labels.items())-sum(edge_palette))%k==0
    for degree in {len(adj[v]) for v in active}:
        vertices = {v for v in active if len(adj[v])==degree}
        assert vertices<=labels.keys() or min(len(vertices&labels.keys()),len(vertices-labels.keys()))>=6
    full = labels.copy()
    if absent is not None:
        full[absent] = dup
    original = {frozenset(e) for e in edges}
    delta = Counter(edge_palette)
    delta.update((full[u]+full[v])%k for u,v in original-pairs)
    delta.update((full[v]+a)%k for v,a in zip(ports,old))
    delta.subtract((full[u]+full[v])%k for u,v in pairs-original)
    delta.subtract(removed)
    vcounts = Counter(vertex_palette)
    if absent is not None:
        vcounts.update([dup])
    for old_high,addition in ((edge_high,delta),(vertex_high,vcounts)):
        bins = [addition[i]+(i in old_high) for i in range(k)]
        assert max(bins)-min(bins)<=1 and sum(addition.values())==k


def profiles():
    # Independently vary all high sets. If both sizes fail they cannot
    # be consecutive residues, even when the vertex count wraps to zero.
    checks = 0
    for k in range(2,13):
        for g in range(2,k+1):
            if k%g: continue
            for m in range(1,g):
                failing_edge,failing_vertex = set(),set()
                for mask in range(1<<k):
                    high = {i for i in range(k) if mask>>i&1}
                    if len(high)==k: continue
                    for target,sgn in ((failing_edge,-1),(failing_vertex,1)):
                        if not any((y-x-sgn*m)%g==0 for x in high for y in set(range(k))-high):
                            target.add(len(high))
                assert all((e+1)%k not in failing_vertex for e in failing_edge)
                checks += 1
    return checks


def literal_examples():
    k = 8
    piece = [(0,1),(1,2),(2,3),(0,4),(4,5),(0,6),(6,7)]
    ports = [1,2,4,6]
    examples = [
        ([0,1,2,3],[(0,1),(1,2),(2,3)],[(0,1),(1,2),(2,3)],[0,1,2,3],
         [0,1,2,3,6,4,7,5]),
        ([0]+list(range(k)),[(0,i) for i in range(1,k+1)],[(0,1),(0,3),(0,4)],[2,1,3,4],
         [1,1,3,5,4,7,6,2])]
    for old,edges,removed,sites,free in examples:
        old_weights = [(old[a]+old[b])%k for a,b in edges]
        assert (sum(old[a]+old[b] for a,b in removed)-sum(old[v] for v in sites))%2
        n = len(old)
        final = [edge for edge in edges if edge not in removed]
        final.extend((n+u,n+v) for u,v in piece)
        final.extend((s,n+v) for s,v in zip(sites,ports))
        labels = old+free
        for seq in (old,old_weights,labels,[(labels[u]+labels[v])%k for u,v in final]):
            counts = [seq.count(i) for i in range(k)]
            assert max(counts)-min(counts)<=1


def run():
    rng = Random(8041991)
    kinds = Counter()
    for k,g in ((512,2),(891,3),(1024,4),(1250,5),(1296,6),(1568,7)):
        for t in (2,g+2,2*g+2):
            for mixed in ((False,True) if g==6 else (False,)):
                edges,ports = coefficients_tree(k,t,g,mixed)
                h = gcd(g,2) if mixed else g
                for m in range(1,h):
                    old = [rng.randrange(k) for _ in ports]
                    removed = [rng.randrange(k) for _ in ports[1:]]
                    removed[-1] = (removed[-1]+m-sum(removed)+sum(old))%k
                    for edge_high in (set(),{0},set(range(k-1)),set(range(0,k,h)),set(rng.sample(range(k),k//2))):
                        vh = set(rng.sample(range(k),(len(edge_high)+1)%k))
                        op,_,_ = transfer(k,h,m,edge_high,vh)
                        data = build(edges,ports,old,removed,edge_high,vh,rng)
                        inspect(k,edges,ports,old,removed,edge_high,vh,data)
                        kinds[op] += 1
    literal_examples()
    print('reconstructed edge and vertex repairs',kinds['edge'],kinds['vertex'],
          'exhaustive profile parameters',profiles(),'complete 8-label examples',2)


if __name__=='__main__':
    run()

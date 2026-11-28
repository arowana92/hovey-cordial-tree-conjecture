"""Verify repeated-port targets and build actual cordial cores for prescribed data."""
from collections import Counter
from functools import reduce
from math import gcd
from random import Random

from check_port_parity import piece
from check_two_leaf_repair import inspect
from check_unicyclic_core import inspect as inspect_closed
from multiport import construct
from port_parity import build
from two_leaf_repair import build as two_leaves


def realize(k,labels,edges,weights,sites):
    """Create a chain of neutral double stars and return the cut and attachment vertices."""
    labels,edges = labels[:],edges[:]
    hub = 0
    cuts,anchors = [],[]
    for j,a in enumerate(sites):
        base = len(labels)
        labels.extend(list(range(k))*2)
        edges.extend((hub,v) for v in range(base,len(labels)))
        anchors.append(base+k+a)
        if j<len(weights):
            child = base+(weights[j]-labels[hub])%k
            cuts.append((hub,child))
            hub = child
    return labels,edges,cuts,anchors


def verify_realization(k,initial,old_edges,removed,site_values):
    labels,edges,cuts,sites = realize(k,initial,old_edges,removed,site_values)
    assert [labels[v] for v in sites]==site_values
    assert [(labels[a]+labels[b])%k for a,b in cuts]==removed
    original_hist = Counter((initial[a]+initial[b])%k for a,b in old_edges)
    histogram = Counter((labels[a]+labels[b])%k for a,b in edges)
    v_hist = Counter(labels)
    v0 = Counter(initial)
    assert all(histogram[i]-original_hist[i]==v_hist[i]-v0[i]==2*len(sites) for i in range(k))
    graph = [set() for _ in labels]
    for a,b in set(edges)-set(cuts):
        graph[a].add(b)
        graph[b].add(a)
    seen = set()
    for s in sites:
        assert s not in seen
        stack = [s]
        seen.add(s)
        while stack:
            v = stack.pop()
            for u in graph[v]-seen:
                stack.append(u)
                seen.add(u)
    assert len(seen)==len(labels)


def difference_cover(m):
    k = m*m
    A,B = list(range(2*m)),list(range(0,k,m))
    assert len(set(A))==len(A) and len(set(B))==len(B)
    verify_realization(k,[0],[],[0]*(3*m-1),A+B)
    # Normalize the first port's translate to zero. Every intersection
    # still has two colors, so after any translation one is nonzero.
    assert all(len(set(A)&{(b+d)%k for b in B})==2 for d in range(k))


def run():
    rng = Random(1181991)
    uniform = repaired = sparse = 0
    for k in (1080,1280,1575,1920,2025):
        binary = [((v-1)//2,v) for v in range(1,k)]
        for ps in ([4,4,4,5,5],[7]*4+[5]*3,[2,2,2,2]):
            old = list(range(len(ps)))
            removed = [rng.randrange(k) for _ in ps[1:]]
            data = construct(binary,ps,old,removed,rng)
            assert data is not None
            aux,cut,labels,pairs,wires,_ = data
            inspect_closed(k,aux,cut,labels)
            assert Counter((labels[v]+a)%k for v,a in zip(ps,old))==Counter((labels[a]+labels[b])%k for a,b in wires)
            assert [(labels[a]+labels[b])%k for a,b in pairs]==removed
            uniform += 1
        if k%2==0:
            n = k//2-1
            tree = [(v-1,v) for v in range(1,n)]
            tips = n
            for v in range(n):
                for _ in range(1+(v in (0,n-1))):
                    tree.append((v,tips))
                    tips += 1
            ps = [0]*4+[3]*2
            old = [0,1,2,3,1,3]
            removed = [0,0,0,0,1]
            assert (sum(removed)-sum(old))%2
            for eh in (set(),{0}):
                vh = set(range(len(eh)+1))
                data = two_leaves(tree,ps,old,removed,eh,vh,rng)
                inspect(k,tree,ps,old,removed,eh,vh,data)
                repaired += 1
        for count in (1,2,3,5):
            for charges in ([count],[count,count]):
                tree,ps = piece(k,charges,True,())
                # Put multiple additional entries at the first joint.
                ps += [1]*(2 if len(charges)==1 else count)
                delta = Counter(v for edge in tree for v in edge)
                delta.update(ps)
                h = reduce(gcd,(n-2 for n in delta.values()),k)
                if len(charges)>1 and h==1: continue
                old = list(range(len(ps)))
                for target in (0,1):
                    removed = [0]*(len(ps)-2)+[(sum(old)+k*(k-1)//2+target)%k]
                    for eh in (set(),{0},set(range(1,k))):
                        vh = set(range((len(eh)+1)%k))
                        data = build(tree,ps,old,removed,eh,vh,rng)
                        if data is None:
                            assert h%2==0 and target%2 and not eh
                            continue
                        aux,labels,absent,dup,gap,holes = data
                        inspect(k,tree,ps,old,removed,eh,vh,(aux,labels,absent,dup[1],gap[1],holes))
                        sparse += 1
    for k in range(5,26):
        verify_realization(k,[0,1,2],[(0,1),(1,2)],
                           [rng.randrange(k) for _ in range(11)],
                           [rng.randrange(k) for _ in range(12)])
    for m in range(3,14):
        difference_cover(m)
    print('repeated-port targets: uniform',uniform,'two-leaf repairs',repaired,
          'all leaves at ports',sparse,'arbitrary boundary cores',21,'difference covers',11)


if __name__=='__main__':
    run()

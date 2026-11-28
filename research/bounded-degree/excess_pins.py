"""Prescribed colors on a near-bounded-degree tree with two free leaves."""
from collections import Counter
from functools import reduce
from math import gcd, isqrt

from check import adjacency
from check_excess import expression
from multiport import lift_marks, residue_sums
from partial_gap import groups, valid
from port_degree_reduction import reduce_degree
from unicyclic_core import core


def build(edges, pins, gap, bound, rng):
    k = len(edges)+1
    if not valid(pins, edges, k, gap):
        return None
    graph = adjacency(k, edges)
    degrees = list(map(len, graph))
    leaves = [v for v,d in enumerate(degrees) if d == 1 and v not in pins]
    if len(leaves) < 2:
        raise ValueError("expected two unpinned leaves")
    target = -gap - sum((degrees[v]-1)*x for v,x in pins.items())
    h = reduce(gcd,(d-1 for v,d in enumerate(degrees) if v not in pins),k)
    if target % h:
        return None
    d = Counter(a for a in degrees if 2 <= a <= bound).most_common(1)[0][0]
    g = gcd(k,d-1)
    reps = {(a-1)%g:v for v,a in enumerate(degrees) if v not in pins and (a-1)%g}
    root = next(v for v,a in enumerate(degrees) if a == d and v not in pins)
    cap = bound+1
    tree, base, sites = reduce_degree(edges,set(pins)|set(reps.values()),
                                      root=root,degree_bound=cap,reserved=leaves[:2],
                                      site_degree=d,paired_buffers=True)
    # The private extra edges have low-degree endpoints. Place their variables
    # after the original cut endpoints, whose degrees can be large.
    buffers = {v for a,b,_ in sites.values() if max(degrees[a],degrees[b]) < cap
               for v in (a,b)}
    order = [root]
    visited = {root}
    for v in order:
        for w in sorted(graph[v]-visited):
            visited.add(w)
            order.append(w)
    ordered = [v for v in order if v in base and v not in pins and v not in buffers and v != root]
    ordered.extend([root] + sorted(buffers))
    index = {v:i for i,v in enumerate(ordered)}
    residues = dict(zip(reps.values(),residue_sums(g,reps,target)))
    forms = {v:expression(constant=x) for v,x in pins.items()}
    forms.update({v:expression((i,1),constant=residues.get(v,0)) for v,i in index.items()})
    for site,(a,b,r) in sites.items():
        forms[site] = expression(*forms[a].items(),*forms[b].items(),
                                 *((i,-c) for i,c in forms[r].items()))
    labels = lift_marks(k,g,index.values(),forms,groups(forms,tree,gap),rng)
    return tree,core(k,tree,None,labels,leaves[:2],d,holes=[gap])


def obstruction(k):
    """A caterpillar whose locally valid pins leave no color for its hub."""
    q = isqrt(k-1)+1
    targets = [(j*q)%k for j in range(1,(k+q-1)//q+1)]
    edges = [(0,i) for i in range(1,q+2)]
    pins = {j+1:j for j in range(q)}
    used = set(pins.values())
    n,previous = q+2,0
    for w in targets:
        a = next(x for x in range(k) if x not in used and (w-x)%k not in used
                 and x != (w-x)%k)
        b = (w-a)%k
        edges.extend([(previous,n),(n,n+1),(n+1,n+2)])
        pins.update({n+1:a,n+2:b})
        used.update((a,b))
        previous,n = n+2,n+3
    if n >= k:
        raise ValueError("insufficient room on the spine")
    edges.append((previous,n))
    edges.extend((v-1,v) for v in range(n+1,k))
    gap = next(w for w in range(k) if w not in targets)
    return edges,pins,gap

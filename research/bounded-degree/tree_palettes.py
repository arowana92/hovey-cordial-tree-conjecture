"""Lift prescribed vertex and edge histograms to a near-spanning cyclic order."""
from collections import Counter
from functools import reduce
from math import gcd

from check import adjacency
from sparse_offsets import closed, edge


def place_copies(graph, fixed, reserved, cuts, remaining, offsets, pairs, far, degree):
    """Pin temporary distinct residues, then restore the requested extra copies."""
    pairs = list(pairs)
    switches = {}
    if far is not None:
        v,p = far
        i = next(i for i,(_,x) in enumerate(pairs) if x==p)
        switches[v] = pairs.pop(i)
    blocked = closed(graph,closed(graph,fixed | set(reserved)))
    for v,neighbors in enumerate(graph):
        if not pairs:
            break
        if len(neighbors)==degree and v not in blocked:
            switches[v] = pairs.pop()
            blocked.update(closed(graph,closed(graph,[v])))
    if pairs:
        raise ValueError("insufficient separated sites for vertex copies")
    for v,(q,p) in switches.items():
        for u in graph[v]:
            pair = edge(u,v)
            offsets[pair] = offsets.get(pair,0)+p-q
            if pair not in cuts:
                cuts.add(pair)
                remaining[u].remove(v)
                remaining[v].remove(u)
            fixed.update(pair)
    return switches


def lift_tree(edges, anchor, label, vertices, weights, offsets):
    """Return the two lifted histograms, normalized offsets, and common shift."""
    k = len(vertices)
    n = len(edges)+1
    if (not k or len(weights)!=k or sum(vertices)!=n or sum(weights)!=n-1
            or min(vertices)<0 or min(weights)<0 or not 0<=label<k or not 0<=anchor<n):
        raise ValueError("inconsistent tree histograms or anchor")
    if not vertices[label]:
        return None
    original = {edge(*e):d%k for e,d in offsets.items()}
    edge_offsets = {edge(u,v):original.get(edge(u,v),0) for u,v in edges}
    common_offset = Counter(edge_offsets.values()).most_common(1)[0][0]
    weights = [weights[(x+common_offset)%k] for x in range(k)]
    height = (n+k-1)//k
    order = k*height
    vh = [x+k*i for x,amount in enumerate(vertices) for i in range(amount,height)]
    vertex_extra = [x for x,amount in enumerate(vertices) for _ in range(height,amount)]
    eh = [x+k*i for x,amount in enumerate(weights) for i in range(amount,height)]
    extra = [x for x,amount in enumerate(weights) for _ in range(height,amount)]
    bias = {e:(d-common_offset)%k for e,d in edge_offsets.items() if d!=common_offset}
    graph = adjacency(n,edges)
    degree = list(map(len,graph))
    vertex_sum = order*(order-1)//2-sum(vh)+sum(vertex_extra)
    difference = sum(vh)-sum(vertex_extra)-sum(eh)+sum(extra)-sum(bias.values())
    if max(degree)==2 and degree[anchor]==1:
        endpoint_sum = vertex_sum-difference
        far = (endpoint_sum-label)%k
        if vertices[far] <= int(far==label):
            return None
        far_lift = far+k*int(far==label and height>1)
        change = (label+far_lift-endpoint_sum)%order
    else:
        h = reduce(gcd,(d-1 for v,d in enumerate(degree) if v!=anchor),order)
        residual = difference-(degree[anchor]-1)*label
        common = gcd(h,k)
        if residual%common:
            return None
        modulus = h//common
        multiplier = (residual//common)*pow(k//common,-1,modulus)%modulus
        change = k*multiplier
    if change:
        assert change%k==0
        e = edge(*edges[0])
        bias[e] = (bias.get(e,0)+change)%order
    return vh,vertex_extra,eh,extra,bias,common_offset

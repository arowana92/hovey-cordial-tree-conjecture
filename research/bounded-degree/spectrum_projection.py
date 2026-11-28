"""Lift prescribed edge frequencies through a cyclic quotient of the vertex order."""
from functools import reduce
from math import gcd

from check import adjacency
from sparse_offsets import edge


def lift(edges, opening, anchor, label, histogram, offsets):
    """Return omitted residues, extra copies and offset lifts; None denotes a failed moment."""
    k = len(histogram)
    n = len(edges) if opening is not None else len(edges)+1
    if not k or n%k or not 0<=label<k or min(histogram)<0 or sum(histogram)!=len(edges):
        raise ValueError("invalid modulus, vertex order, anchor label or histogram")
    copies = n//k
    omitted = [x+k*i for x,amount in enumerate(histogram) for i in range(amount,copies)]
    extra = [x for x,amount in enumerate(histogram) for _ in range(copies,amount)]
    lifted = {edge(*pair):d%k for pair,d in offsets.items() if d%k}
    if copies == 1:
        return omitted, extra, lifted

    graph = adjacency(n,edges)
    degree = [len(ns) for ns in graph]
    h = reduce(gcd,(d-1 for v,d in enumerate(degree) if v!=anchor),n)
    s = n*(n-1)//2
    raw = sum(extra)-sum(omitted)-sum(lifted.values())
    leaves = [v for v,d in enumerate(degree) if d==1]
    remote = edge(*edges[0])
    if not leaves:
        shift = (raw-s)%n
        if shift%k:
            return None
    elif (opening is not None and len(leaves)==1) or (opening is None and len(leaves)==2 and anchor in leaves):
        # Pick a different lift if the two forced vertex labels would coincide.
        forbidden = 0 if opening is not None else 2*label
        correction = (s-raw)%k
        if correction == forbidden%n:
            correction += k
        if opening is not None:
            y = leaves[0]
            middle = next(iter(graph[y]))
            junction = next(v for v,d in enumerate(degree) if d==3)
            if middle in graph[junction]:
                tail = edge(y,middle)
                joint = edge(junction,middle)
                # Ensure the two tail weights differ upstairs, even if equal downstairs.
                if (correction+lifted.get(tail,0)-lifted.get(joint,0))%n == 0:
                    lifted[tail] = lifted.get(tail,0)+k
                    raw -= k
                remote = next(edge(*pair) for pair in edges if edge(*pair) not in (tail,joint))
        shift = (correction-s+raw)%n
    else:
        target = raw-(degree[anchor]-1)*label
        common = gcd(k,h)
        if target%common:
            return None
        reduced = h//common
        multiple = (target//common)*pow(k//common,-1,reduced)%reduced
        shift = k*multiple
    assert shift%k == 0
    lifted[remote] = (lifted.get(remote,0)+shift)%n
    return omitted, extra, lifted

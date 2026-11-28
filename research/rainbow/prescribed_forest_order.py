"""Extend a fixed cordial core in a prescribed parent-first order, block by block."""
from collections import Counter


def extend(parent, old, order, k, witness, offsets=None):
    """Offsets may be prescribed on edges entering a block from earlier vertices."""
    if k < 2 or not 0 < len(old) <= len(parent) or len(old)%k not in (0,1):
        raise ValueError("expected a nonempty core of order zero or one modulo k")
    if parent[0]!=-1 or any(not 0<=p<v for v,p in enumerate(parent[1:],1)):
        raise ValueError("expected a tree with parent-first indices")
    if any(not 0<=x<k for x in old) or sorted(order)!=list(range(len(old),len(parent))):
        raise ValueError("invalid core labels or growth order")
    offsets = {} if offsets is None else offsets
    if set(offsets)-set(order):
        raise ValueError("an offset must be on a new edge")
    vertices = Counter(old)
    weights = Counter((old[i]+old[parent[i]])%k for i in range(1,len(old)))
    for counts in (vertices,weights):
        bins = [counts[x] for x in range(k)]
        if max(bins)-min(bins)>1:
            raise ValueError("the core must be cordial")
    labels = list(old)+[-1]*len(order)
    pos = 0
    while pos<len(order):
        forced = (len(old)+pos)%k==0
        group = order[pos:pos+(1 if forced else k-1)]
        local = {}
        links = []
        surplus = max(range(k),key=vertices.__getitem__)
        for v in group:
            p = parent[v]
            if p in local:
                if offsets.get(v,0)%k:
                    raise ValueError("an internal edge of a batch has a nonzero offset")
                links.append(local[p])
            else:
                if labels[p]<0:
                    raise ValueError("the growth order must keep each prefix connected")
                links.append(-1-(labels[p]+offsets.get(v,0)-surplus)%k)
            local[v] = len(links)-1
        if forced:
            v, = group
            hole = min(range(k),key=weights.__getitem__)
            digits = [(hole-labels[parent[v]]-offsets.get(v,0))%k]
        else:
            digits = [(x+surplus)%k for x in witness(links,k)]
        if len(digits)!=len(group):
            raise ValueError("wrong witness length")
        for v,x in zip(group,digits):
            labels[v] = x
            vertices[x] += 1
            weights[(x+labels[parent[v]]+offsets.get(v,0))%k] += 1
        pos += len(group)
    return labels

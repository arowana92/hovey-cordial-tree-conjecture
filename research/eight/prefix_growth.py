"""Grow a tree cordially at eight or nine labels, preserving a supplied core."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations

from research.rainbow.generate import rainbow


@lru_cache(maxsize=4096)
def rainbow_word(local,k):
    return tuple(rainbow(local,k))


def ordinary_shape(k, parents, vertices):
    group = set(vertices)
    children = Counter(parents[i] for i in group if parents[i] in group)
    exceptional_counts = (1,3,5) if k==8 else (2,5)
    if len(group)==k-1 and len(children)==1:
        return next(iter(children.values())) not in exceptional_counts
    roots = {i for i in group if parents[i] not in group}
    if len(group)==k and len(roots)==2 and roots==children.keys():
        return min(children.values()) not in exceptional_counts
    return True


def split(k, parents, pool, size, test_remainder):
    # The pool is an ancestor-closed prefix of the as-yet-unlabelled vertices.
    universe = set(pool)
    for first in combinations(pool,size):
        group = set(first)
        if any(parents[i] in universe and parents[i] not in group for i in first):
            continue
        if ordinary_shape(k,parents,group) and (
                not test_remainder or ordinary_shape(k,parents,universe-group)):
            return list(first)
    return None


def construct(k, parents, core):
    """Return (vertex,label) additions in order, or None for an obstructed input.

    Vertex zero is the tree root. The first len(core) vertices form the supplied
    cordial core, whose order must be zero or one mod k. Every parent precedes
    its child in the input. The returned growth order can differ from that order.
    """
    assert k in (8,9) and parents[0]==-1 and 0<len(core)<=len(parents)
    assert all(0<=p<i for i,p in enumerate(parents) if i)
    assert len(core)%k in (0,1)
    labels = dict(enumerate(core))
    vertices = [core.count(x) for x in range(k)]
    edges = [0]*k
    for i in range(1,len(core)):
        edges[(core[i]+core[parents[i]])%k] += 1
    assert max(vertices)-min(vertices)<=1 and max(edges)-min(edges)<=1
    result = []

    def from_surplus(nodes, surplus, stem=False):
        index = {v:i for i,v in enumerate(nodes)}
        local = [index[parents[v]] if parents[v] in index else
                 -1-(labels[parents[v]]-surplus)%k for v in nodes]
        if stem:
            assert len(nodes)==k-1 and local[0]<0 and local[1:]==list(range(k-2))
            p = -1-local[0]
            divisor = 4 if k==8 else 3
            for word in permutations(range(1,k)):
                weights = {(a+b)%k for a,b in zip((p,)+word,word)}
                if len(weights)==k-1:
                    missing, = set(range(k))-weights
                    if (2*word[-1]-missing)%divisor==0:
                        break
            else:
                raise AssertionError('uncovered stem')
        else:
            word = rainbow_word(tuple(local),k)
        return [(v,(x+surplus)%k) for v,x in zip(nodes,word)]

    def batch(nodes, residue, stem):
        if residue==1:
            return from_surplus(nodes,vertices.index(max(vertices)),stem)
        deficit = edges.index(min(edges))
        for root in nodes:
            if parents[root] not in labels:
                continue
            x = (deficit-labels[parents[root]])%k
            labels[root] = x
            try:
                rest = from_surplus([v for v in nodes if v!=root],x,stem)
                return [(root,x)]+rest
            except ValueError:
                pass
            finally:
                del labels[root]
        raise ValueError('no first root can fill the deficit')

    remaining = list(range(len(core),len(parents)))
    while remaining:
        residue = (len(core)+len(result))%k
        size = k-residue
        stem = False
        if len(remaining)<=size:
            group = remaining
        elif len(remaining)==size+k:
            group = split(k,parents,remaining,size,True)
            if group is None:
                group = remaining[:size]
                stem = True
        else:
            group = split(k,parents,remaining[:size+1],size,False)
            assert group is not None
        try:
            additions = batch(group,residue,stem)
        except ValueError:
            if len(remaining)!=size:
                raise
            return None
        for v,x in additions:
            vertices[x] += 1
            edges[(labels[parents[v]]+x)%k] += 1
            labels[v] = x
        result.extend(additions)
        used = set(group)
        remaining = [v for v in remaining if v not in used]
    return result

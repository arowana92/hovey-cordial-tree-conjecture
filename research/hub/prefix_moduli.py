"""Integer collision certificates for the compressed prefixes of a rooted tree."""

from math import prod
from research.hub.branches import children_of
from research.hub.universal_hub import construct


def reduced_length(length):
    return length if length<=14 else 3+(length-3)%12


def segments(tree):
    """Return maximal directed chains in fixed depth-first order."""
    kids = children_of(tree)
    result = []
    stack = [(0,v) for v in reversed(kids[0])]
    while stack:
        start,v = stack.pop()
        path = [v]
        while len(kids[v]) == 1:
            v, = kids[v]
            path.append(v)
        result.append((start,path))
        stack.extend((v,u) for u in reversed(kids[v]))
    return result


def breadth_first(tree):
    kids = children_of(tree)
    order = [0]
    for v in order:
        order.extend(kids[v])
    index = {v:i for i,v in enumerate(order)}
    return [-1]+[index[tree[v]] for v in order[1:]]


def prefix_catalog(tree):
    yield [-1]
    old = [-1]
    ends = {0:0}
    for start,path in segments(tree):
        at = ends[start]
        first = len(old)
        for size in range(1,min(14,len(path))+1):
            yield breadth_first(old+[at]+list(range(first,first+size-1)))
        additional = reduced_length(len(path))
        old.extend([at]+list(range(first,first+additional-1)))
        ends[path[-1]] = len(old)-1


def collision_product(tree):
    """Explicit product for modest cores. A modulus not dividing it passes every prefix."""
    value = 1
    for core in prefix_catalog(tree):
        x,_,_ = construct(core)
        value *= prod(abs(u-v) for i,u in enumerate(x) for v in x[:i])
    return value

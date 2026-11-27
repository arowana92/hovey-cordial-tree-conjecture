"""Prime high-digit permutations on connected cyclic covers of a unicyclic base."""

from itertools import permutations
from math import comb


def criterion(p, length):
    h = (p-1)//2
    return sum(pow(comb(h,i),length,p) for i in range(h+1))%p


def lift(p, low, edges, offsets, deleted, low_offsets=None):
    """Return high-digit lift modulo m*p, with one edge of the covering graph deleted.

    Edge (u,v,t) joins (u,i) to (v,i+t); offsets[e][i] is a high digit.
    The base low edge offset is constant on its fiber.
    """
    m = len(low)
    low_offsets = [0]*m if low_offsets is None else low_offsets
    if len(edges)!=m or sorted(low)!=list(range(m)) or len(offsets)!=m or len(low_offsets)!=m:
        raise ValueError("expected uniform base labels and a square covering instance")
    if sorted((low[u]+low[v]+s)%m for (u,v,_),s in zip(edges,low_offsets))!=list(range(m)):
        raise ValueError("base edge residues must be a permutation")
    drop,j = deleted
    lists = [list(row) for row in offsets]
    if any(len(row)!=p for row in lists):
        raise ValueError("expected one high-digit offset per lifted edge")
    lists[drop][j] = -sum(x for i,x in enumerate(lists[drop]) if i!=j)%p
    if any(sum(row)%p for row in lists):
        return None
    # Each high fiber can be translated independently. The zero entry is normalized.
    assigned = [None]*m
    incident = [[] for _ in low]
    for e,(u,v,_) in enumerate(edges):
        incident[u].append(e)
        if v!=u:
            incident[v].append(e)

    def visit(left):
        if not left:
            return True
        def available(u):
            return sum(a==b or assigned[a] is not None or assigned[b] is not None
                       for a,b,t in (edges[e] for e in incident[u]))
        v = max(left,key=available)
        check = [e for e in incident[v] if all(z==v or assigned[z] is not None for z in edges[e][:2])]
        for perm in permutations(range(1,p)):
            assigned[v] = (0,*perm)
            valid = True
            for e in check:
                a,b,t = edges[e]
                if len({(assigned[a][i]+assigned[b][(i+t)%p]+lists[e][i])%p for i in range(p)})!=p:
                    valid = False
                    break
            if valid and visit(left-{v}):
                return True
        assigned[v] = None
        return False

    if not visit(set(range(m))):
        return None
    return [[low[v]+m*z for z in row] for v,row in enumerate(assigned)]

"""Cordial labelings of caterpillars with one additional leaf at an arbitrary vertex."""

from collections import Counter


def staircase(spine, leaves):
    """Return the bipartition ranks along a monotone edge list."""
    ranks = [{},{}]
    edges = []
    for i,u in enumerate(spine):
        rank = ranks[i%2]
        rank.setdefault(u,len(rank))
        opposite = ranks[1-i%2]
        for v in leaves[u]:
            opposite[v] = len(opposite)
            edges.append((u,v))
        if i+1<len(spine):
            v = spine[i+1]
            opposite.setdefault(v,len(opposite))
            edges.append((u,v))
    return ranks,edges


def integer_base(spine, leaves, parent, tip):
    ranks,edges = staircase(spine,leaves)
    A,B = ranks if parent in ranks[1] else ranks[::-1]
    a,b = len(A),len(B)
    y = B[parent]
    r = b-y if 2*y<b else b-1-y
    labels = {**A,**{v:a+j+(j>=r) for v,j in B.items()},tip:a+r}
    return labels,edges+[(parent,tip)]


def attach(spine, leaves, shared, base, deficit, k):
    ranks,_ = staircase(spine,leaves)
    A,B = ranks if shared in ranks[0] else ranks[::-1]
    a,b = len(A),len(B)
    c = base[shared]
    if A[shared]==a-1:  # Reverse both orderings to put the joint at zero.
        A = {v:a-1-j for v,j in A.items()}
        B = {v:b-1-j for v,j in B.items()}
    assert A[shared]==0
    t = a+b-1
    # The allowed starts [a,k-b+1] produce weight intervals whose union
    # is [a,k+a-1] after subtracting twice the label at the shared vertex.
    assert 1<=t<=k
    target=a+(deficit-2*c-a)%k
    start=min(target,k-b+1)
    labels = {**base,**{v:(c+j)%k for v,j in A.items()}}
    labels.update({v:(c+start+j)%k for v,j in B.items()})
    return labels


def label(populations, marked, k):
    """Spine 0,...,s-1 has the given direct leaves and a two-edge arm at marked."""
    s = len(populations)
    spine = list(range(s))
    leaves = {}
    first = s
    for u,count in enumerate(populations):
        leaves[u] = list(range(first,first+count))
        first += count
    w,tip = first,first+1
    leaves[marked].append(w)
    n = tip+1
    if marked in (0,s-1):
        # The new arm continues the spine in this case.
        ends = spine if marked==s-1 else spine[::-1]
        leaves[marked].remove(w)
        leaves[w]=[tip]
        (A,B),_ = staircase(ends+[w],leaves)
        return {**{v:x%k for v,x in A.items()},
                **{v:(len(A)+x)%k for v,x in B.items()}},"caterpillar"
    if k>=n or n%k==0:
        values,_ = integer_base(spine,leaves,w,tip)
        return {v:y%k for v,y in values.items()},"interval"

    t = n%k
    def capacity(side):
        return sum(1+len(leaves[u]) for u in side)+populations[marked]
    left,right = spine[:marked],spine[marked+1:][::-1]
    arm = max((left,right),key=capacity)
    if capacity(arm)<t:
        # Here n=2k-1. Duplicate a genuine caterpillar leaf distinct from w.
        # A spine end with no leaves can itself serve as that leaf.
        if any(populations):
            u = next(u for u,count in enumerate(populations) if count)
            twin = leaves[u][0]
            leaves[u].insert(0,n)
        else:
            free_end = next(u for u in (spine[0],spine[-1]) if u!=marked)
            twin = free_end
            if free_end==spine[0]:
                u=spine[1]; spine=spine[1:]
            else:
                u=spine[-2];spine=spine[:-1]
            leaves[u][0:0]=[n,twin]
        values,edges = integer_base(spine,leaves,w,tip)
        weights=Counter((values[x]+values[y])%k for x,y in edges)
        deficient=next(i for i in range(k) if weights[i]==1)
        if (values[n]+values[u])%k==deficient:
            values[n],values[twin]=values[twin],values[n]
        del values[n]
        return {v:y%k for v,y in values.items()},"twin"

    # Traverse an end arm towards the marked vertex. At the stopping vertex
    # remove only the desired number of its direct leaves, retaining the joint.
    order = arm+[marked]
    tail = []
    tail_leaves = {}
    rest = {u:list(row) for u,row in leaves.items()}
    remaining = t
    for u in order:
        tail.append(u)
        ordinary = [v for v in leaves[u] if v!=w]
        take = min(len(ordinary),remaining)
        tail_leaves[u] = ordinary[:take]
        removed = set(tail_leaves[u])
        rest[u] = [v for v in leaves[u] if v not in removed]
        remaining -= take
        if not remaining:
            break
        remaining -= 1  # edge to the next spine position
    assert not remaining
    shared = tail[-1]
    cut = set(tail[:-1])
    core = [v for v in spine if v not in cut]
    base,edges = integer_base(core,rest,w,tip)
    weights = Counter((base[x]+base[y])%k for x,y in edges)
    deficit = next(i for i in range(k) if weights[i]==len(base)//k-1)
    base = {v:y%k for v,y in base.items()}
    return attach(tail,tail_leaves,shared,base,deficit,k),"tail"

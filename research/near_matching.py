"""Cordial prefix labelings at the certified primes and matching lifts to twice a prime."""

from .marked_leaf import label as marked_leaf_labels
from .matching_expansion import matching_labels
from .rainbow.generate import rainbow


def prefix_labels(parent, m, offsets=None):
    """Parents precede children. The edge offset of vertex i is offsets[i]."""
    if offsets is None:
        offsets = [0]*len(parent)
    labels = []
    counts = [0]*m
    for start in range(0,len(parent),m):
        p = parent[start]
        surplus = (counts.index(min(counts))-labels[p]-offsets[start]) % m if start else 0
        labels.append(surplus)
        if start:
            counts[(surplus+labels[p]+offsets[start]) % m] += 1
        local, shifts = [], []
        end = min(start+m,len(parent))
        for v in range(start+1,end):
            p = parent[v]
            if p <= start:
                local.append(-1)
                shifts.append(offsets[v]+labels[p]-surplus)
            else:
                local.append(p-start-1)
                shifts.append(offsets[v])
        block = rainbow(local,m,shifts)
        labels.extend((surplus+x) % m for x in block)
        for v in range(start+1,end):
            counts[(labels[v]+labels[parent[v]]+offsets[v]) % m] += 1
    return labels


def matching_at_leaves(parent):
    """A maximum matching with every exposed vertex a leaf, for a nonsingleton."""
    n = len(parent)
    neighbors = [[] for _ in parent]
    mate = [-1]*n
    for v in reversed(range(1,n)):
        p = parent[v]
        neighbors[v].append(p)
        neighbors[p].append(v)
        if mate[p] == mate[v] == -1:
            mate[p], mate[v] = v,p
    for v in range(n):
        if mate[v] >= 0:
            continue
        back = -1
        while len(neighbors[v]) > 1:
            u = next(w for w in neighbors[v] if w != back)
            dest = mate[u]
            assert dest >= 0
            mate[v], mate[u], mate[dest] = u,v,-1
            back, v = u,dest
    return mate


def label(parent, m):
    """Label a tree when its number of unmatched vertices fits in the last quotient block."""
    n = len(parent)
    if n == 1:
        return [0]
    mate = matching_at_leaves(parent)
    exposed = {v for v,u in enumerate(mate) if u == -1}
    pairs = [(v,u) for v,u in enumerate(mate) if u > v]
    ordinary = len(pairs)
    pairs.extend((v,n+i) for i,v in enumerate(sorted(exposed)))
    s = len(pairs)
    if len(exposed) > (s-1)%m+1:
        raise ValueError("exposed vertices exceed the last quotient block")

    index = {v:(i,j) for i,pair in enumerate(pairs) for j,v in enumerate(pair)}
    adj = [[] for _ in pairs]
    for v in range(1,n):
        p = parent[v]
        a,l = index[p]
        b,r = index[v]
        if a != b:
            adj[a].append((b,l,r))
            adj[b].append((a,r,l))
    # Pair zero is ordinary. Postpone the exposed leaves and their dummy partners.
    order, previous = [0], {0:None}
    last = []
    for u in order:
        for v,l,r in adj[u]:
            if v in previous:
                continue
            previous[v] = (u,l,r)
            (order if v < ordinary else last).append(v)
    order.extend(last)
    pos = {u:i for i,u in enumerate(order)}
    qp, joins = [-1], []
    for v in order[1:]:
        u,l,r = previous[v]
        qp.append(pos[u])
        joins.append((l,r))
    if len(exposed) <= 1 and m not in (3,5,7,11,13):
        qlabels = marked_leaf_labels(qp,m,s-1 if exposed else None)
    else:
        qlabels = prefix_labels(qp,m)
    full = matching_labels(qp,qlabels,joins,m)
    return [full[2*pos[index[v][0]]+index[v][1]] for v in range(n)]

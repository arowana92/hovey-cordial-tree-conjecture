"""Place leaves at both ends of an integer labeling with distinct core sums."""

from collections import deque


def extend(core_labels, core_weights, parents, offsets=None):
    """Return leaf labels in the given parent order and a common interval-length bound.

    Core labels start at zero. Each old and each new edge uses its specified
    integer weight. Old vertex labels and old weights must each be distinct.
    """
    if offsets is None:
        offsets = [0]*len(parents)
    if len(offsets)!=len(parents) or not core_labels or min(core_labels)!=0:
        raise ValueError("expected normalized core labels and one offset per leaf")
    if len(set(core_labels))!=len(core_labels) or len(set(core_weights))!=len(core_weights):
        raise ValueError("repeated core label or weight")
    if any(p<0 or p>=len(core_labels) for p in parents):
        raise ValueError("parent outside the core")
    if not parents:
        weight_span = max(core_weights)-min(core_weights)+1 if core_weights else 0
        return [],max(max(core_labels)+1,weight_span)
    shifts = [core_labels[p]+b for p,b in zip(parents,offsets)]
    low,high = min(shifts),max(shifts)
    width = max(max(core_labels)+1,high-low)
    forbidden = set(core_weights)
    left_cost = sum(w<high for w in forbidden)
    right_cost = sum(w>=width+low for w in forbidden)
    left_anchor = min(forbidden|{width+low})
    right_anchor = max(forbidden|{high-1})
    slack = max(left_cost+right_cost,right_anchor-left_anchor+1-width)
    # Use any spare allowance on the right, keeping the left endpoint fixed.
    threshold = left_anchor+left_cost
    result = [0]*len(shifts)
    left = sorted((s,i) for i,s in enumerate(shifts) if s>=threshold)
    right = sorted((s,i) for i,s in enumerate(shifts) if s<threshold)
    for group, start, step in ((reversed(left),-1,-1),(right,width,1)):
        x = start
        for s,i in group:
            while x+s in forbidden:
                x += step
            result[i] = x
            x += step
    return result,width+len(shifts)+slack


def tree_labels(n, edges):
    """Construct the integer labels for a finite tree on vertices 0,...,n-1."""
    if n<0 or len(edges)!=max(0,n-1):
        raise ValueError("expected a tree")
    if n<2:
        return list(range(n))
    adj = [[] for _ in range(n)]
    for u,v in edges:
        if not 0<=u<n or not 0<=v<n or u==v:
            raise ValueError("invalid tree edge")
        adj[u].append(v)
        adj[v].append(u)
    if n==2:
        return [0,1]
    inside = {v for v in range(n) if len(adj[v])>1}
    if not inside:
        raise ValueError("expected a nonleaf core")
    root = min(inside)
    rank = {root:0}
    queue = deque([root])
    weights = []
    while queue:
        v = queue.popleft()
        for w in adj[v]:
            if w in inside and w not in rank:
                rank[w] = len(rank)
                weights.append(rank[v]+rank[w])
                queue.append(w)
    leaves = [v for v in range(n) if v not in inside]
    if len(rank)!=len(inside) or any(len(adj[v])!=1 or adj[v][0] not in rank for v in leaves):
        raise ValueError("disconnected tree")
    parents = [rank[adj[v][0]] for v in leaves]
    tail,_ = extend(range(len(rank)),weights,parents)
    result = [0]*n
    for v,x in rank.items():
        result[v] = x
    for v,x in zip(leaves,tail):
        result[v] = x
    return result

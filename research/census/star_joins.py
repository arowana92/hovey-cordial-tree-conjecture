"""Integer interval labelings for odd trees of equal stars joined at their leaves."""

from collections import defaultdict, deque


def join_stars(parents, quotient_labels, leaves, attachments):
    """On edge (parent[v],v), attachments[v-1] gives the two actual leaf indices.

    Vertex v*(leaves+1) is a star center. The following vertices are its leaves
    in their original index order. Return the labels and the actual tree edges.
    """
    q = len(parents)
    if q < 3 or q%2 == 0 or parents[0] != -1 or len(attachments) != q-1:
        raise ValueError("expected a nontrivial odd tree and one attachment pair per edge")
    if sorted(quotient_labels) != list(range(q)):
        raise ValueError("the quotient labels must be bijective")
    t = q//2
    edges = []
    parity = [0]*q
    for v,p in enumerate(parents[1:],1):
        if not 0 <= p < v:
            raise ValueError("invalid quotient parent")
        parity[v] = 1-parity[p]
        edges.append((p,v))
    sums = {(quotient_labels[u]+quotient_labels[v])%q for u,v in edges}
    if len(sums) != q-1:
        raise ValueError("repeated quotient edge residue")
    missing, = set(range(q))-sums
    shift = (t-missing)*pow(2,-1,q)%q
    x = [(a+shift)%q for a in quotient_labels]

    adjacent = defaultdict(list)
    bridge_ends = []
    for (u,v),(i,j) in zip(edges,attachments):
        if not (0 <= i < leaves and 0 <= j < leaves):
            raise ValueError("invalid attachment leaf")
        a,b = (u,i),(v,j)
        epsilon = 1-(x[u]+x[v]+t)//q
        step = epsilon if parity[u] else -epsilon
        adjacent[a].append((b,step))
        adjacent[b].append((a,-step))
        bridge_ends.append((a,b))

    components = []
    owner = {}
    for port in adjacent:
        if port in owner:
            continue
        delta = {port:0}
        stack = [port]
        while stack:
            a = stack.pop()
            owner[a] = len(components)
            for b,step in adjacent[a]:
                if b not in delta:
                    delta[b] = delta[a]+step
                    stack.append(b)
        components.append(delta)

    touching = [[] for _ in parents]
    for (v,_),component in owner.items():
        touching[v].append(component)
    used = [set() for _ in parents]
    index = {}
    queue = deque([0])
    scheduled = {0}
    while queue:
        delta = components[queue.popleft()]
        low, high = -min(delta.values()), leaves-1-max(delta.values())
        forbidden = {previous-d for (v,_),d in delta.items() for previous in used[v]}
        shift = next((s for s in range(low,high+1) if s not in forbidden),None)
        if shift is None:
            raise ValueError("insufficient leaf labels for this quotient and these attachments")
        for port,d in delta.items():
            v,_ = port
            ordinate = shift+d
            used[v].add(ordinate)
            index[port] = leaves-1-ordinate if parity[v] else ordinate
            for c in touching[v]:
                if c not in scheduled:
                    scheduled.add(c)
                    queue.append(c)

    labels, tree_edges = [], []
    for v in range(q):
        center = len(labels)
        labels.append(q*leaves+(x[v]+t)%q)
        chosen = {index[v,j] for j in range(leaves) if (v,j) in index}
        unused = iter(sorted(set(range(leaves))-chosen))
        for j in range(leaves):
            digit = index[v,j] if (v,j) in index else next(unused)
            labels.append(q*digit+x[v])
            tree_edges.append((center,len(labels)-1))

    def vertex(port):
        v,j = port
        return v*(leaves+1)+j+1
    tree_edges.extend((vertex(a),vertex(b)) for a,b in bridge_ends)
    return labels,tree_edges

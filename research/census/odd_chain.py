"""Join super edge-magic copies along an odd quotient with a balanced alpha-labeling."""


def odd_join(base, f, quotient, g, ports):
    """Inputs are parent arrays, vertex-label arrays, and the two base port vertices.

    The first port is used on quotient labels 0,...,q//2. The other is used
    on the remaining vertices. Return the new vertex labels and edge list.
    """
    n,q = len(base),len(quotient)
    if n < 2 or q < 3 or not q%2:
        raise ValueError("invalid piece or quotient order")
    if sorted(f) != list(range(n)) or sorted(g) != list(range(q)):
        raise ValueError("expected bijective labels")
    if any(par[0] != -1 or any(not 0 <= u < v for v,u in enumerate(par[1:],1))
           for par in (base,quotient)):
        raise ValueError("invalid tree")
    t = q//2
    piece_edges = [(v,u) for v,u in enumerate(base[1:],1)]
    sums = sorted(f[u]+f[v] for u,v in piece_edges)
    if sums != list(range(sums[0],sums[0]+n-1)):
        raise ValueError("piece sums are not consecutive")
    qedges = [(v,u) for v,u in enumerate(quotient[1:],1)]
    if (any((g[u] <= t) == (g[v] <= t) for u,v in qedges)
            or sorted(g[u]+g[v] for u,v in qedges) != list(range(t+1,3*t+1))):
        raise ValueError("expected a balanced alpha-labeling in sum form")
    a,b = ports
    if not (0 <= a < n and 0 <= b < n):
        raise ValueError("invalid ports")
    if f[a]+f[b] == sums[-1]+1:
        f = [n-1-v for v in f]
    elif f[a]+f[b] != sums[0]-1:
        raise ValueError("port labels must sum just outside the piece sum interval")

    side = [0]*n
    for v,u in piece_edges:
        side[v] = 1-side[u]
    same = side[a] == side[b]
    start,extra = divmod(t+1,2)
    label,edges = [],[]
    for i,rank in enumerate(g):
        index = rank if same else (start+rank)%q
        other = (index+t+(0 if same else extra))%q
        label.extend(q*f[v]+(index if side[v] == side[a] else other) for v in range(n))
        edges.extend((i*n+v,i*n+u) for v,u in piece_edges)
    for u,v in qedges:
        edges.append((u*n+(a if g[u] <= t else b),v*n+(a if g[v] <= t else b)))
    return label,edges

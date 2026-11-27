"""Insert paths with fixed endpoints and one specified additional edge weight."""

from itertools import combinations, cycle, islice
from math import gcd


# The last row of each table is the freely chosen terminal label.
EIGHT = ((1,-2), (-1,1), (2,-2), (-2,3), (0,-1), (1,-1), (-2,2), (0,1))
NINE = ((1,2), (2,2), (-4,-5), (3,4), (-1,-1), (2,3), (-2,-2), (-2,-3), (0,1))
EXTREME = ((0,-2), (-1,1), (0,2), (-1,-1), (1,-1), (-1,3), (1,-2), (0,1))
EXTREME_NINE = ((-1,2), (0,2), (1,-5), (-1,3), (0,-1), (-1,4), (1,-3), (0,-2), (0,1))
SINGLE = ((0,1),)


def linear(a, row, b, other):
    return tuple(a*x + b*y for x,y in zip(row,other))


def constant(x):
    return (x,0,0,0)


U, V, T = (0,1,0,0), (0,0,1,0), (0,0,0,1)


def paths(table, start, end):
    return [linear(a,start,b,end) for a,b in table]


def separate(rows, forbidden, signs, modulus, starts=None):
    """Choose each parameter after substituting all earlier ones in its constraints."""
    constraints = [[] for _ in signs]

    def exclude(form):
        pos = next((i for i in reversed(range(len(signs))) if form[i+1]), None)
        if pos is None:
            if not (form[0] if modulus is None else form[0] % modulus):
                raise ValueError("the prescribed data force a collision")
        else:
            constraints[pos].append(form)

    for row in rows:
        for x in forbidden:
            exclude((row[0]-x, *row[1:]))
    for a,b in combinations(rows,2):
        exclude(linear(1,a,-1,b))
    chosen = []
    for i, sign in enumerate(signs):
        bad = set()
        for form in constraints[i]:
            target = -form[0]-sum(a*x for a,x in zip(form[1:],chosen))
            coeff = form[i+1]
            if modulus is None:
                if target % coeff == 0:
                    bad.add(target//coeff)
            else:
                g = gcd(coeff,modulus)
                if target % g == 0:
                    stride = modulus//g
                    first = (target//g * pow(coeff//g, -1, stride)) % stride
                    bad.update(range(first,modulus,stride))
        if modulus is not None and len(bad) == modulus:
            raise ValueError("there is no available residue for this parameter")
        x = sign if starts is None else starts[i]
        while (x if modulus is None else x % modulus) in bad:
            x += sign
        chosen.append(x)
    result = [row[0] + sum(a*x for a,x in zip(row[1:],chosen)) for row in rows]
    return result if modulus is None else [x % modulus for x in result]


def join(left, p, right, q, weight, blocked, signs, modulus=None, starts=None):
    left_pre = paths(left,constant(p),U)
    right_pre = paths(right,constant(q),V)
    complement = linear(1,constant(weight),-1,T)
    final = [*left_pre, *paths(NINE,U,T), *reversed(paths(NINE,V,complement)), *reversed(right_pre)]
    return separate(final, blocked, signs, modulus, starts)


def bridge(p, q, weight, length, forbidden, modulus=None, extreme=None):
    """Return labels on length internal vertices. Keep 0 and all forbidden values free of reuse."""
    if length < 76:
        raise ValueError("the construction uses at least 76 internal vertices")
    if modulus is not None:
        if extreme is not None:
            raise ValueError("an extreme label is an integer option")
        p,q,weight = (x % modulus for x in (p,q,weight))
        forbidden = {x % modulus for x in forbidden}
    blocked = set(forbidden) | {0,p,q}
    remaining = length-18-int(p==0)-int(q==0)
    nines = remaining % 8
    eights = (remaining-9*nines)//8
    pieces = [EIGHT]*eights + [NINE]*nines
    assert eights >= 0 and len(pieces) >= 2

    def first(endpoint):
        if endpoint == 0:
            return SINGLE
        table = pieces.pop()
        if endpoint == extreme:
            return EXTREME if table == EIGHT else EXTREME_NINE
        return table

    left, right = first(p), first(q)
    prefix = [left, *pieces]
    result = []
    for table in prefix[:-1]:
        block = separate(paths(table,constant(p),U), blocked, [-1 if p==extreme else 1], modulus)
        blocked.update(block)
        result.extend(block)
        p = block[-1]

    # The last two neutral paths end at T and weight-T.
    last_sign = -1 if modulus is None and weight < 0 else 1
    signs = [-1 if p==extreme else 1, -1 if q==extreme else 1, last_sign]
    result.extend(join(prefix[-1],p,right,q,weight,blocked,signs,modulus))
    return result


def integer_subdivision(order, edges, internal, site):
    """Label a long subdivision of a tree or a connected unicyclic multigraph."""
    if len(edges) not in (order-1,order) or len(edges)!=len(internal) or not 0<=site<order:
        raise ValueError("expected a tree or unicyclic graph, lengths and one old site")
    N = order + sum(internal)
    M = 36*N
    labels = [None]*order
    labels[site] = 0
    unused = [v for v in range(order) if v!=site]
    extreme = None
    if len(edges) == order-1 and unused:
        extreme = -10*M
        labels[unused.pop()] = extreme
    for i,v in enumerate(unused,1):
        labels[v] = i
    weights = [x for x in labels if x!=extreme]
    actual = []
    occupied = set(labels)
    for (u,v),w,length in zip(edges,weights,internal):
        block = bridge(labels[u],labels[v],w,length,occupied,extreme=extreme)
        start = len(labels)
        labels.extend(block)
        occupied.update(block)
        path = [u,*range(start,start+length),v]
        actual.extend(zip(path,path[1:]))
    return labels,actual


def modular_attachment(initial, edges, internal, joint, site, leaves, k, deficit=None):
    """Preserve old vertex labels. Use uniform increments or a specified core deficit."""
    n = len(initial)-1 + sum(internal)
    if len(edges) != len(initial)-1 or len(internal) != len(edges):
        raise ValueError("expected a coarse tree and a length for each edge")
    if k <= 360*(n+3) or leaves < 0:
        raise ValueError("the sparse construction needs a larger modulus or a valid leaf count")
    origin = initial[site] % k
    labels = [(a-origin) % k for a in initial]
    free = [x for i,x in enumerate(labels) if i != joint]
    if not free or len(set(free)) != len(free):
        raise ValueError("expected distinct prescribed labels on the free coarse vertices")
    if deficit is None and (n+leaves) % k:
        raise ValueError("uniform increments need a multiple of the modulus")
    gap = free[0]
    weights = free.copy()
    if deficit is not None:
        weights[0] = (deficit-2*origin) % k
    occupied = set(labels) | set(weights)
    actual = []
    for (u,v), w, length in zip(edges, weights, internal):
        block = bridge(labels[u],labels[v],w,length,occupied,modulus=k)
        occupied.update(block)
        start = len(labels)
        labels.extend(block)
        path = [u,*range(start,start+length),v]
        actual.extend(zip(path,path[1:]))
    used = {x for i,x in enumerate(labels) if i!=joint}
    missing = (x for x in range(k) if x not in used)
    first = list(islice(missing, leaves))
    if len(first) < leaves:
        order = [gap, *(x for x in range(k) if x!=gap)]
        first.extend(islice(cycle(order), leaves-len(first)))
    start = len(labels)
    actual.extend((site,i) for i in range(start,start+leaves))
    labels.extend(first)
    return [(x+origin) % k for x in labels],actual

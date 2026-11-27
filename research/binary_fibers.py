"""Solve exactly for binary lifts of fixed low digits, including edge offsets."""


def eliminate(rows):
    """Return one assignment and the rank, or None for inconsistent equations."""
    basis = {}
    for mask, rhs in rows:
        while mask:
            pivot = mask.bit_length()-1
            if pivot not in basis:
                basis[pivot] = (mask,rhs)
                break
            old, value = basis[pivot]
            mask ^= old
            rhs ^= value
        else:
            if rhs:
                return None
    answer = 0
    for pivot,(mask,rhs) in sorted(basis.items()):
        if (bin(mask & answer).count("1")%2) != rhs:
            answer |= 1 << pivot
    return answer,len(basis)


def paired_rows(low, edges, offsets, m):
    if len(low) != 2*m or len(edges) != 2*m-1 or len(edges) != len(offsets):
        raise ValueError("expected 2m vertices and 2m-1 edges and offsets")
    counts = [0]*m
    tag = []
    for a in low:
        if not 0 <= a < m:
            raise ValueError("invalid low vertex label")
        tag.append(counts[a])
        counts[a] += 1
    if counts != [2]*m:
        raise ValueError("expected two vertices with each low label")
    groups = [[] for _ in range(m)]
    for (u,v),bias in zip(edges,offsets):
        carry, digit = divmod(low[u]+low[v]+bias,m)
        groups[digit].append(((1 << low[u]) ^ (1 << low[v]), tag[u]^tag[v]^(carry&1)))
    if sorted(map(len,groups)) != [1]+[2]*(m-1):
        return tag,None
    return tag,[(a^b,1^x^y) for pair in groups if len(pair)==2 for (a,x),(b,y) in [pair]]


def lift(low, edges, offsets, m):
    tag, rows = paired_rows(low,edges,offsets,m)
    if rows is None:
        return None
    solved = eliminate(rows)
    if solved is None:
        return None
    mask, rank = solved
    labels = [a+m*((mask>>a&1)^b) for a,b in zip(low,tag)]
    return labels,rank


def cyclic_edges(m, r=1, s=3, omit=0):
    """The two chords at every midpoint, omitting the second at one midpoint."""
    return [((a-step)%m,(a+step)%m) for a in range(m)
            for step in ((r,) if a == omit else (r,s))]


def matchings(indices):
    """All unordered maximum matchings of one fiber."""
    if not indices:
        yield ()
    elif len(indices)%2:
        for j in range(len(indices)):
            yield from matchings(indices[:j]+indices[j+1:])
    else:
        u = indices[0]
        for j in range(1,len(indices)):
            for tail in matchings(indices[1:j]+indices[j+1:]):
                yield ((u,indices[j]),)+tail


def count_lifts(low, edges, offsets, m):
    """Count full cordial lifts, allowing any low multiplicities and tree order."""
    from itertools import product
    from math import factorial
    if m < 1 or len(edges) != len(offsets) or any(not 0 <= a < m for a in low):
        raise ValueError("invalid residues or offsets")
    vertices = [[] for _ in range(m)]
    weights = [[] for _ in range(m)]
    tokens = []
    for i,a in enumerate(low):
        vertices[a].append(len(tokens))
        tokens.append((1 << i,0))
    for (u,v),bias in zip(edges,offsets):
        carry, a = divmod(low[u]+low[v]+bias,m)
        weights[a].append(len(tokens))
        tokens.append(((1 << u) ^ (1 << v),carry&1))
    for groups in (vertices,weights):
        if max((len(g)+1)//2 for g in groups)-min(len(g)//2 for g in groups) > 1:
            return 0
    multiplicity = 1
    choices = []
    for g in vertices+weights:
        if len(g) > 1:
            choices.append(matchings(tuple(g)))
            multiplicity *= factorial((len(g)+1)//2)
    overall = 0
    for selection in product(*choices):
        rows = []
        for pairs in selection:
            for i,j in pairs:
                p,x = tokens[i]
                q,y = tokens[j]
                rows.append((p^q,1^x^y))
        result = eliminate(rows)
        if result is not None:
            overall += 1 << (len(low)-result[1])
    assert overall % multiplicity == 0
    return overall//multiplicity

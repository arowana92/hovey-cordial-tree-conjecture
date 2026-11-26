"""Exact balanced subdivision of forest edges using two rounds of rational rounding."""

from fractions import Fraction
from itertools import product


# Coefficients of the endpoints p,q and of the two new adjacent labels u,v.
POSITIONS = (
    (0, 0, 1, 0), (0, 0, 0, 1), (0, 0, -1, -1), (1, 0, 1, 0),
    (-1, -1, -1, -1), (0, 1, 0, 1), (1, 0, 0, -1), (-1, 0, -1, 0),
    (0, -1, 0, -1), (0, 1, 1, 1), (0, 0, -1, 0), (0, 0, 1, 1),
)


def evaluate(row, p, q, u, v, k):
    return sum(a*b for a, b in zip(row, (p,q,u,v))) % k


def dependence(columns):
    """Find a rational dependence, using at most one more column than rows."""
    basis = {}
    for j, column in enumerate(columns):
        vector = list(map(Fraction, column))
        coeff = {j: Fraction(1)}
        for i in sorted(basis):
            if not vector[i]:
                continue
            pivot, terms = basis[i]
            ratio = vector[i]/pivot[i]
            vector = [x-ratio*y for x,y in zip(vector, pivot)]
            for h, val in terms.items():
                coeff[h] = coeff.get(h,0)-ratio*val
        first = next((i for i, x in enumerate(vector) if x), None)
        if first is None:
            return {h: val for h,val in coeff.items() if val}
        basis[first] = vector, coeff
    raise ValueError("no dependence among the selected columns")


def round_groups(groups, k, *, probabilities=None):
    """Choose one integer histogram per group near the mean of its options."""
    if not groups:
        return []
    mass = max(sum(c) for g in groups for c in g)
    weights = ([[Fraction(1,len(g))]*len(g) for g in groups] if probabilities is None
               else [list(row) for row in probabilities])
    while True:
        live = [[j for j,w in enumerate(row) if 0 < w < 1] for row in weights]
        moves = [(i, j, js[0]) for i, js in enumerate(live) for j in js[1:]]
        if not moves:
            return [row.index(1) for row in weights]
        hard = [a for a in range(k)
                if sum(groups[i][j][a] for i, js in enumerate(live) for j in js)>2*mass]
        moves = moves[:len(hard)+1]
        columns = [[groups[i][j][a]-groups[i][base][a] for a in hard]
                   for i,j,base in moves]
        terms = dependence(columns)
        delta = {}
        for pos, val in terms.items():
            i,j,base = moves[pos]
            delta[i,j] = val
            delta[i,base] = delta.get((i,base),0)-val
        step = min(weights[i][j]/(-v) for (i,j),v in delta.items() if v < 0)
        for (i,j),v in delta.items():
            weights[i][j] += step*v


def expand(specs, k):
    """For each (p,q,r), return the path from p to q with 12r insertions."""
    values = [[None]*r for _,_,r in specs]
    options = list(product(range(k),repeat=2))
    requests = {}
    # Assign each position to its last undetermined pair, even indices first.
    for s,(p,q,r) in enumerate(specs):
        for j in range(r):
            for row in POSITIONS:
                owner = j-1 if j>0 and j%2==0 and any(row[:2]) else j
                requests.setdefault((s,owner),[]).append((j,row))
    for parity in (0,1):
        keys = [key for key in requests if key[1]%2==parity]
        groups = []
        for s,owner in keys:
            group = []
            for choice in options:
                counts = [0]*k
                for j,row in requests[s,owner]:
                    prev = specs[s][:2] if j==0 else values[s][j-1]
                    if j-1==owner:
                        prev = choice
                    if prev is None:
                        prev = (0,0)  # coefficients on the unknown pair vanish
                    current = choice if j==owner else values[s][j]
                    counts[evaluate(row,*prev,*current,k)] += 1
                group.append(counts)
            groups.append(group)
        for key,chosen in zip(keys,round_groups(groups,k)):
            s,j = key
            values[s][j] = options[chosen]

    paths = []
    for (p,q,r), choices in zip(specs,values):
        left, tails = [p], []
        prev = p,q
        for choice in choices:
            sites = [evaluate(row,*prev,*choice,k) for row in POSITIONS]
            left.append(sites[0])
            tails.append(sites[1:])
            prev = choice
        paths.append(left+[v for tail in reversed(tails) for v in tail]+[q])
    return paths

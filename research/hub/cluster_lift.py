"""Lift a contracted tree into cyclic fibers and restore specified site populations."""

from collections import Counter
from math import gcd

from research.large_order_hall_pools import hall_pair, zero_block


def lift(core, digits, quotient, q, d, populations):
    """Site vertices come first. Their digits include 0 and 1. Total order is q*d."""
    s = len(digits)
    k = q*d
    if len(set(digits)) != s or not {0,1} <= set(digits) <= set(range(d)):
        raise ValueError("distinct site digits including 0 and 1 required")
    if len(populations) != s or min(populations) < 0 or sum(populations)+len(core) != k:
        raise ValueError("leaf counts must give order equal to the modulus")
    if len(quotient) != len(core)-s+1 or quotient[0] != 0:
        raise ValueError("wrong contracted labeling")
    if len(set(quotient)) != len(quotient) or not set(quotient) <= set(range(q)):
        raise ValueError("contracted vertex labels must be distinct residues")
    site_by_digit = {digit:v for v,digit in enumerate(digits)}
    cluster_weights = {(digits[v]+digits[core[v]]) % d for v in range(1,s)}
    cluster_gap, = set(digits)-cluster_weights
    assert cluster_weights == set(digits)-{cluster_gap}

    parents = list(core)
    # The homomorphic section keeps every nonsite edge in the same lift as
    # its quotient weight. At two sites this saves leaves at the second site.
    scale = d*pow(d,-1,q) if gcd(q,d) == 1 else 1
    labels = [q*x for x in digits]+[(scale*x) % k for x in quotient[1:]]
    ordinary = range(s,len(core))
    weight = {v:(labels[v]+labels[core[v]]) % k for v in ordinary}
    zero_edge, = [v for v in ordinary if weight[v] % q == 0]
    assert core[zero_edge] >= s
    labels[zero_edge] = (labels[zero_edge]+cluster_gap*q-weight[zero_edge]) % k
    weight = {v:(labels[v]+labels[core[v]]) % k for v in ordinary}
    weight_by_fiber = {w % q:w//q for w in weight.values()}
    gap, = set(quotient)-set(weight_by_fiber)
    assert gap != 0 and weight_by_fiber[0] == cluster_gap
    assert set(weight_by_fiber) == set(quotient)-{gap}

    remaining = Counter(dict(zip(digits,populations)))

    def leaf(fiber, digit, shift):
        assert remaining[shift] > 0
        parents.append(site_by_digit[shift])
        labels.append(fiber+q*digit)
        remaining[shift] -= 1

    for j in sorted(set(range(d))-set(digits)):
        leaf(0,j,0)
    gap_digit = None
    for v in ordinary:
        a,fiber = divmod(labels[v],q)
        if fiber == gap:
            gap_digit = a
            continue
        c = weight_by_fiber[fiber]
        for j in range(d):
            if j != a:
                shift = int((j-c) % d < (a-c) % d)
                leaf(fiber,j,shift)

    assert gap_digit is not None
    units = sum(x*n for x,n in remaining.items()) % d
    start = (gap_digit-units) % d
    for j in range(d):
        if j != gap_digit:
            leaf(gap,j,int((j-start) % d < units))

    for fiber in sorted(set(range(q))-set(quotient)):
        block = zero_block([remaining[j] for j in range(d)])
        for shift,(p,_) in zip(block,hall_pair(block)):
            leaf(fiber,(-p) % d,shift)
    assert not any(remaining.values())
    return parents,labels

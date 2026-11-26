"""Realize prescribed multisets on equal groups of path centers using Hall layers."""

from collections import Counter
from itertools import accumulate

from research.large_order_primitive import lifted_moment_zero


def edge_split(data):
    """Return epsilon, h, g with f=epsilon*D_1² e_0 + 2h + (1+shift)g."""
    k = len(data)
    f = lifted_moment_zero(data)
    parity = [x%2 for x in accumulate(f)]
    epsilon = sum(i*x for i,x in enumerate(parity))%2
    if epsilon:
        for i,d in enumerate((1,-2,1)):
            f[i] -= d
        parity[0] ^= 1
        parity[1] ^= 1
    positions = [i for i,x in enumerate(parity) if x]
    assert len(positions)%2 == 0
    g = [0]*len(f)
    for a,b in zip(positions[::2],positions[1::2]):
        g[a],g[b] = 1,-1
    missing = -sum(i*x for i,x in enumerate(g))
    assert missing%2 == 0 and 0 <= missing//2 < len(f)
    g[0] -= 2
    g[missing//2] += 2
    h = []
    for i,x in enumerate(f):
        numerator = x-g[i]-(g[i-1] if i else 0)
        assert numerator%2 == 0
        h.append(numerator//2)
    assert g[-1] == 0
    return epsilon,[h[i]+h[i+k] for i in range(k)],[g[i]+g[i+k] for i in range(k)]


def zero_block(counts):
    """Choose k available items with sum zero, using independent cardinality states."""
    k = len(counts)
    dp = {(0,0): ()}
    for residue,amount in enumerate(counts):
        old = list(dp.items())
        for (size,weight),prefix in old:
            for take in range(1,min(amount,k-size)+1):
                key = size+take,(weight+take*residue)%k
                if key not in dp:
                    dp[key] = prefix+(residue,)*take
                if key == (k,0):
                    return dp[key]
    raise ValueError("missing zero-sum block")


def hall_pair(block):
    """Find p,t permutations with their sum list equal to the given zero-sum block."""
    k = len(block)
    pairs = []

    def visit(i,left,right):
        if i == k:
            return True
        for p in range(k) if i else (0,):
            t = (block[i]-p)%k
            if left >> p & 1 or right >> t & 1:
                continue
            pairs.append((p,t))
            if visit(i+1,left|(1<<p),right|(1<<t)):
                return True
            pairs.pop()
        return False

    if not visit(0,0,0):
        raise ValueError("missing Hall permutations")
    return pairs


def pairs_for(counts):
    """Return uniform p,t marginals and prescribed sum counts. Small-k verifier tool."""
    k = len(counts)
    remaining = list(counts)
    if min(counts)<0 or sum(counts)%k or sum(i*x for i,x in enumerate(counts))%k:
        raise ValueError("incompatible sum multiplicities")
    pairs = []
    while sum(remaining):
        block = zero_block(remaining)
        for x,v in Counter(block).items():
            remaining[x] -= v
        pairs.extend(hall_pair(block))
    return pairs

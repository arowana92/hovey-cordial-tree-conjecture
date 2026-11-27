"""Two effective leaf shifts complete a decorated core on the cycles of their difference."""

from itertools import accumulate
from math import gcd


def coarse_labels(parents, offsets, g):
    """The incoming edge takes the preceding vertex label in topological order."""
    x = [0]
    for i,p in enumerate(parents[1:],1):
        x.append((x[-1]-x[p]-offsets[i])%g)
    return x


def finish_two_shifts(k, d, vertices, edges):
    """Return spare labels, labels at each effective shift, and the surplus residue.

    The two input histograms describe a tree. Their differences summed over
    shift cycles must be one unit on one cycle and zero on every other cycle.
    """
    n = sum(vertices)
    if len(vertices) != k or len(edges) != k or sum(edges) != n-1 or not 0 < d < k:
        raise ValueError("invalid histograms or shift")
    span = gcd(k,d)
    m = k//span
    cycles = [[(r+d*i)%k for i in range(m)] for r in range(span)]
    diff = [v-e for v,e in zip(vertices,edges)]
    coarse = [sum(diff[x] for x in cycle) for cycle in cycles]
    if sorted(coarse) != [0]*(span-1)+[1]:
        raise ValueError("the coarse histograms need a single gap")
    index = sum(i*diff[x] for cycle in cycles for i,x in enumerate(cycle))%m
    surplus = cycles[coarse.index(1)][index]
    diff[surplus] -= 1

    move = [0]*k
    for cycle in cycles:
        prefix = list(accumulate(diff[x] for x in cycle))
        assert prefix[-1] == 0
        constant = -((-sum(prefix))//m)
        for x,v in zip(cycle,prefix):
            move[x] = constant-v
    total = sum(move)
    assert total%m == 0 and 0 <= total < k
    for cycle in cycles[:total//m]:
        for x in cycle:
            move[x] -= 1

    spare = list(range((1-n)%k))
    v0 = list(vertices)
    for x in spare:
        v0[x] += 1
    mean = (n+len(spare)-1)//k
    first = [mean+int(i==surplus)-v0[i]-move[i] for i in range(k)]
    layers = max(-min(first),-min(move))
    return spare, [layers+x for x in first], [layers+x for x in move], surplus

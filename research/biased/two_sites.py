"""Signed scalars for a fixed rooted core with two additional populations of leaves."""

from itertools import permutations


def two_site_counts(parents, second, modulus):
    """Return signed counts with first hub 0, second hub 1 and anonymous added leaves."""
    h = len(parents)
    if modulus < h or not 0 < second < h or parents[0] != -1:
        raise ValueError("invalid order or hubs")
    if any(not 0 <= u < v for v,u in enumerate(parents[1:],1)):
        raise ValueError("expected a rooted core in parent order")
    maximum = modulus-h
    by_length = [0]*(maximum+1)
    terms = []
    for perm in permutations(range(h)):
        inversions = sum(x > y for j,x in enumerate(perm) for y in perm[j+1:])
        terms.append((perm[1:],(-1)**inversions))
    other = [i for i in range(1,h) if i != second]
    x = [0]*h
    x[second] = 1
    for labels in permutations(range(2,modulus),h-2):
        for v,t in zip(other,labels):
            x[v] = t
        distances = [[(y-x[v]-x[parents[v]])%modulus for y in x] for v in range(1,h)]
        for perm,sign in terms:
            length = sum(row[image] for row,image in zip(distances,perm))
            if length <= maximum:
                by_length[length] += sign
    prefix = 0
    result = []
    for b, value in enumerate(by_length):
        prefix += value
        result.append((-1)**b*prefix)
    return result


def short_arm_sum(p, b):
    """Normalized scalar, without (-1)^b, for adjacent hubs and a two-edge arm at hub 0."""
    total = sum(max(0,p-2*j-2) for j in range(b//2+1,b+1))
    total -= (b+1)*((p-b-3)//2)
    total -= sum(max(0,(p-b-j-3)//2) for j in range(b+1))
    return total


def short_arm_quadratic(p,b):
    """Twice the preceding count modulo p."""
    if b <= (p-3)//2:
        return (b*b+6*b+6-(b%2))%p
    return (b*b+4*b+3-(b%2))%p

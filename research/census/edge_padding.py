"""Pad an arbitrary forest extension along one chosen edge."""
from .cycle_subdivision import after, half_weights, short


def leaf_packet(k, a, b, parent):
    """One new leaf and k-1 subdivisions, uniform on both histograms."""
    if k < 5:
        raise ValueError("requires at least five residues")
    leaf = (parent + (0 if k%2 else k//2))%k
    return leaf, short(k,a,b,leaf,k-1)


def period(k, a, b, vertex_high, edge_high):
    """One k-subdivision on any cordial core at odd or four-divisible k>=5.

    Also works at k=2 mod 4 whenever the high edge bins contain one member
    of an antipodal pair and omit the other.
    """
    a,b = a%k,b%k
    if k < 5:
        raise ValueError("requires at least five residues")
    if k%2:
        return [(a+i)%k for i in range(1,k+1)]
    half = k//2
    for low in range(k):
        if low not in edge_high and (low+half)%k in edge_high:
            return after(half_weights(k,low),a)
    if k%4:
        raise ValueError("the antipodal edge move is unavailable")
    y = next(x for x in vertex_high if (x+k//4)%k not in vertex_high)
    z = (y+k//4)%k
    row = short(k,a,b,y,k-1)
    i = row.index(z)
    return row[:i]+[z]+row[i:]


def padded_tree(k, parents, padding):
    """Grow any parent-first tree rooted at edge 0--1, subdividing that edge."""
    n = len(parents)
    if k < 5 or n < 2 or parents[:2] != [-1,0] or any(not 0 <= p < j for j,p in enumerate(parents[2:],2)):
        raise ValueError("need a parent-first tree rooted at an edge and k>=5")
    extra = padding-(k-1)*(n-2)
    if extra < 0:
        raise ValueError("below the sufficient bound")
    # Begin with a cordial path of the excess length. Its endpoints represent
    # the two original vertices, and new tree vertices grow as prescribed leaves.
    size = 2+extra
    path = [(i//2+(i%2)*((size+1)//2))%k for i in range(size)]
    original = [path[0],path[-1]]
    inside = path[1:-1]
    last = path[-2]
    for p in parents[2:]:
        leaf,block = leaf_packet(k,last,original[1],original[p])
        original.append(leaf)
        inside.extend(block)
        last = block[-1]
    return original,inside

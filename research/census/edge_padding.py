"""Pad an arbitrary forest extension along one chosen edge."""
from .cycle_subdivision import after, half_weights, short


def leaf_packet(k, a, b, parent):
    """One new leaf and k-1 subdivisions, uniform on both histograms."""
    if k < 5:
        raise ValueError("requires at least five residues")
    leaf = (parent + (0 if k%2 else k//2))%k
    return leaf, short(k,a,b,leaf,k-1)


def exchange(k, a, b, y, z, reflect):
    """Transfer one vertex from high y to low z, with one controlled edge transfer."""
    if not reflect:
        row = short(k,a,b,y,k-1)
        i = row.index(z)
        return row[:i]+[z]+row[i:]
    m = k//2
    cycle = [(y+x)%k for j in range(1,m) for x in (j,j+m)]+[(y+m)%k]
    forward = a != y
    endpoint = a if forward else b
    chain = [endpoint]+after(cycle,endpoint)
    u = (2*y+m-z)%k
    v = (u+m)%k
    i = next(i for i,edge in enumerate(zip(chain,chain[1:])) if edge in ((u,v),(v,u)))
    row = chain[1:i+1]+[z]+chain[i+1:]
    return row if forward else row[::-1]


def period(k, a, b, vertex_high, edge_high):
    """A single k-period at any edge, except at order 1 when k is 2 mod 4."""
    a,b = a%k,b%k
    if k < 5:
        raise ValueError("requires at least five residues")
    if k%2:
        return [(a+i)%k for i in range(1,k+1)]
    m = k//2
    for d in range(k):
        if d not in edge_high and (d+m)%k in edge_high:
            return after(half_weights(k,d),a)
    if k%4 == 0:
        y = next(x for x in vertex_high if (x+k//4)%k not in vertex_high)
        return exchange(k,a,b,y,(y+k//4)%k,False)
    if not edge_high:
        raise ValueError("a one-period insertion cannot preserve an order-one core here")
    bins = set(range(k))
    p = {x for x in bins if 2*x%k in edge_high}
    low = bins-vertex_high
    if vertex_high & p and low-p:
        return exchange(k,a,b,next(iter(vertex_high&p)),next(iter(low-p)),False)
    for y in vertex_high-p:
        if a == b == y:
            continue
        for z in low:
            if (2*y-z)%k in p:
                return exchange(k,a,b,y,z,True)
    raise AssertionError("the reflection lemma supplies an admissible pair")


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

"""Add a forest of matched pairs to a fixed divisible-order cordial core."""

from .rainbow.generate import rainbow


def lift(low, parity, m):
    """The residue mod 2m with the given residue mod odd m and given parity."""
    return low if low % 2 == parity else low+m


def extend(m, boundary, links, deficit):
    """Return the two labels in each pair, in parent-before-child order.

    (p,a,b,h) joins port a of pair p to port b of the current pair, with
    offset h. For p<0 use old label boundary[-1-p] in place of port a.
    deficit is the unique deficient old edge weight modulo 2m.
    """
    values = []
    k = 2*m

    def parent_value(p,a):
        return values[p][a] if p >= 0 else boundary[-1-p]

    for start in range(0,len(links),m):
        end = min(start+m,len(links))
        p,a,b,h = links[start]
        first = (deficit-parent_value(p,a)-h) % m
        parents, biases = [], []
        for p,a,b,h in links[start+1:end]:
            if p <= start:
                old = first if p == start else parent_value(p,a)
                parents.append(-1)
                biases.append(h+old-first)
            else:
                parents.append(p-start-1)
                biases.append(h)
        tail = rainbow(parents,m,biases)
        lows = [first]+[(first+x) % m for x in tail]
        even_weights = set()
        for i,low in enumerate(lows,start):
            p,a,b,h = links[i]
            old = parent_value(p,a)
            target = deficit if i == start else 0
            parity = (target-old-h) % 2
            pair = (lift(low,parity,m),lift(low,1-parity,m))
            values.append(pair[::-1] if b else pair)
            if i != start:
                even_weights.add((old+values[i][b]+h) % k)
        if end-start == m:
            deficit, = set(range(0,k,2))-even_weights
    return values


def replace_edge(m, left, right, ports):
    """Insert a chain of matched pairs. ports[i] gives its incoming and outgoing sites."""
    if len(ports) % m or sum(a != b for a,b in ports) % 2:
        raise ValueError("need a whole number of periods and an even number of crossed pairs")
    pairs = []
    bit = left % 2
    for j,(a,b) in enumerate(ports,1):
        low = (left+j) % m
        row = (lift(low,bit,m),lift(low,1-bit,m))
        pair = row[::-1] if a else row
        pairs.append(pair)
        bit = pair[b] % 2
    assert bit == left % 2
    return pairs

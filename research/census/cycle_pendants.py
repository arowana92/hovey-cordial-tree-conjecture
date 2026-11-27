"""Neutral edge replacements by a cyclic sequence of matched pairs."""

from .caterpillar_leaf import staircase
from ..paired_forest import replace_edge


def read_witnesses(path):
    with open(path) as source:
        return {row[0]:row[1:] for row in (list(map(int,line.split())) for line in source)}


def cycle_block(m, ports, witnesses):
    """Label the ring obtained by joining the last outgoing site to the first incoming site."""
    spine = []
    leaves = {}
    for i,(a,b) in enumerate(ports):
        v = 2*i+a
        spine.append(v)
        leaves[v] = []
        if a != b:
            spine.append(2*i+b)
            leaves[2*i+b] = []
        else:
            leaves[v].append(2*i+1-a)
    if len(spine)%2:
        (A,B),_ = staircase(spine,leaves)
        values = {**A, **{v:len(A)+j for v,j in B.items()}}
    else:
        def key(row):
            word = 1
            for v in row:
                word = 2*word+int(bool(leaves[v]))
            return word
        orders = (row[i:]+row[:i] for row in [spine,spine[::-1]] for i in range(len(row)))
        order = min(orders,key=key)
        perm = witnesses[key(order)]
        nodes = order+[leaf for v in order for leaf in leaves[v]]
        if len(perm) != len(nodes):
            raise ValueError("no harmonious witness for this ring")
        values = dict(zip(nodes,perm))
    return [(values[2*i]%(2*m),values[2*i+1]%(2*m)) for i in range(len(ports))]


def chain(m, left, right, ports, witnesses):
    """Insert a positive multiple of m pairs, using the order-2m records when needed."""
    n = len(ports)
    if not n or n%m or m%2 != 1:
        raise ValueError("expected a positive multiple of an odd modulus")
    through = sum(a != b for a,b in ports)
    if through%2 == 0:
        return replace_edge(m,left,right,ports)
    if n%2 == 0:
        rows = cycle_block(m,ports,{})  # Odd girth at any even number of periods.
    else:
        if through == n:
            raise ValueError("an odd number of pure subdivision periods cannot be uniform")
        start = next(i for i,(a,b) in enumerate(ports) if a == b)
        rotated = ports[start:]+ports[:start]
        rows = cycle_block(m,rotated[:m],witnesses)
        rest = rotated[m:]
        if rest:
            # Glue on the remaining even number of periods. Its final label
            # must agree with the starting label of its entering edge.
            x = rows[-1][rotated[m-1][1]]
            tail = chain(m,x,x,rest,witnesses)
            rows.extend(tail)
        if start:
            rows = rows[-start:]+rows[:-start]
    delta = left-rows[-1][ports[-1][1]]
    return [tuple((x+delta)%(2*m) for x in row) for row in rows]

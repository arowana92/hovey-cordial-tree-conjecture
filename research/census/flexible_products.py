"""Construct alpha-labelings of substituted trees at specified attachment vertices."""

from dataclasses import dataclass
from typing import Callable


@dataclass
class FlexibleTree:
    # The callable returns within-class ranks with the requested rank at the pin.
    sides: tuple
    edges: tuple
    ranks: Callable


def joined_graph(quotient_edges, pieces, ports):
    if not pieces or len(quotient_edges) != len(ports) or len(ports) != len(pieces)-1:
        raise ValueError("expected one port pair per quotient tree edge")
    n = len(pieces[0].sides)
    if n < 2 or any(len(piece.sides) != n for piece in pieces):
        raise ValueError("pieces must share an order of at least two")
    neighbors = [[] for _ in pieces]
    edges = [(i*n+u, i*n+v) for i, piece in enumerate(pieces) for u, v in piece.edges]
    for (a, b), (u, v) in zip(quotient_edges, ports):
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("attachment outside its piece")
        neighbors[a].append((b, u, v))
        neighbors[b].append((a, v, u))
        edges.append((a*n+u, b*n+v))
    return neighbors, tuple(edges)


def local_ranks(pieces, neighbors, root, pin, rank, widths):
    local = [None]*len(pieces)
    local[root] = pieces[root].ranks(pin, rank)
    queue = [root]
    for a in queue:
        for b, u, v in neighbors[a]:
            if local[b] is None:
                width = widths[pieces[b].sides[v]]
                local[b] = pieces[b].ranks(v, width-1-local[a][u])
                queue.append(b)
    return local


def aligned_product(quotient_edges, slots, pieces, ports, root=0, pin=0, rank=0):
    """Use fixed interlaced quotient slots and joins between like named classes."""
    neighbors, edges = joined_graph(quotient_edges, pieces, ports)
    q = len(pieces)
    n = len(pieces[0].sides)
    a = pieces[0].sides.count(0)
    b = n-a
    if any(piece.sides.count(0) != a for piece in pieces):
        raise ValueError("class sizes must agree")
    for (i, j), (u, v) in zip(quotient_edges, ports):
        if pieces[i].sides[u] != pieces[j].sides[v]:
            raise ValueError("join uses different local classes")
    if sorted(slots) != list(range(q)) or sorted(slots[i]+slots[j] for i,j in quotient_edges) != list(range(1,2*q-2,2)):
        raise ValueError("invalid quotient slots")
    lower_size = ((q+1)//2)*a + (q//2)*b
    local = local_ranks(pieces, neighbors, root, pin, rank, (a,b))
    labels = []
    for i, slot in enumerate(slots):
        start = (slot//2)*n
        for side, j in zip(pieces[i].sides, local[i]):
            offset = (b,a)[side] if slot % 2 else 0
            labels.append(start + offset + j + lower_size*(side ^ (slot%2)))
    return labels, edges


def substitute(quotient, pieces, ports):
    """Preserve complete one-vertex rank attainability with arbitrary specified joins."""
    q = len(quotient.sides)
    if len(pieces) != q or 2*sum(quotient.sides) != q:
        raise ValueError("expected a balanced even quotient with one piece per vertex")
    neighbors, edges = joined_graph(quotient.edges, pieces, ports)
    n = len(pieces[0].sides)
    if any(2*sum(piece.sides) != n for piece in pieces):
        raise ValueError("pieces must have equally large color classes")
    half = n//2

    flips = [None]*q
    flips[0] = 0
    order = [0]
    for a in order:
        for b, u, v in neighbors[a]:
            if flips[b] is None:
                flips[b] = 1 ^ flips[a] ^ pieces[a].sides[u] ^ pieces[b].sides[v]
                order.append(b)
    sides = tuple(s ^ flips[i] for i, piece in enumerate(pieces) for s in piece.sides)

    def label(vertex, rank):
        if not (0 <= vertex < q*n and 0 <= rank < q*half):
            raise ValueError("requested vertex or class rank outside tree")
        root, pin = divmod(vertex, n)
        slot, local_rank = divmod(rank, half)
        quotient_ranks = quotient.ranks(root, slot//2)
        even_side = quotient.sides[root] ^ (slot % 2)
        local = local_ranks(pieces, neighbors, root, pin, local_rank, (half,half))
        result = []
        for i in range(q):
            position = 2*quotient_ranks[i] + (quotient.sides[i] ^ even_side)
            result.extend(half*position + j for j in local[i])
        return tuple(result)

    return FlexibleTree(sides, edges, label)

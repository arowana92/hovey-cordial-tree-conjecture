"""Complete an edge-ranked tree by subdivision and label trees one below a power of two."""

from dataclasses import dataclass
from functools import lru_cache

from research.census.flexible_products import FlexibleTree, substitute


EDGE = FlexibleTree((0,1), ((0,1),), lambda vertex, rank: (0,0))


def parts(edges, cut):
    """Partition a connected edge set at a specified original edge."""
    a, b = cut
    reached = {a}
    todo = [a]
    adj = {}
    for u, v in edges:
        if (u,v) != cut:
            adj.setdefault(u, []).append(v)
            adj.setdefault(v, []).append(u)
    for u in todo:
        for v in adj.get(u, ()):
            if v not in reached:
                reached.add(v)
                todo.append(v)
    assert b not in reached
    return (tuple(e for e in edges if e != cut and e[0] in reached),
            tuple(e for e in edges if e != cut and e[0] not in reached))


def optimal_ranking(edges):
    """Exact small-tree algorithm via the unique maximum edge."""
    @lru_cache(None)
    def solve(es):
        if not es:
            return 0, ()
        best = len(es)+1
        for cut in es:
            left, right = (solve(p) for p in parts(es, cut))
            height = 1+max(left[0],right[0])
            if height < best:
                best, ranked = height, left[1]+right[1]+((cut,height),)
        return best, ranked
    height, pairs = solve(tuple(edges))
    return height, dict(pairs)


def split_at_max(edges, ranking):
    height = max(ranking[e] for e in edges)
    cuts = [e for e in edges if ranking[e] == height]
    if len(cuts) != 1:
        raise ValueError("edge ranking has a repeated maximum on a connected part")
    cut = cuts[0]
    return cut, parts(edges, cut)


@lru_cache(None)
def power_path(height):
    if height == 1:
        return EDGE
    half = power_path(height-1)
    return substitute(EDGE, [half,half], [(len(half.sides)-1,0)])


def subdivision(edges, ranking, height):
    """Return a fully attainable subdivision and the map of original vertices."""
    if not edges or min(ranking[e] for e in edges) < 1 or height < max(ranking[e] for e in edges):
        raise ValueError("expected a nontrivial tree and a height covering its positive ranks")

    def build(es, h):
        (u,v), halves = split_at_max(es, ranking)
        if h == 1:
            if len(es) != 1:
                raise ValueError("too many edges at the bottom")
            return EDGE, {u:0,v:1}
        pieces, maps, ports = [], [], []
        size = 1 << (h-1)
        for vertex, half in zip((u,v), halves):
            if half:
                piece, mapping = build(half, h-1)
                port = mapping[vertex]
            else:
                # The new path extends the cut edge. Its far end represents
                # the singleton and can carry further joins higher in the tree.
                piece, mapping, port = power_path(h-1), {vertex:size-1}, 0
            pieces.append(piece)
            maps.append(mapping)
            ports.append(port)
        tree = substitute(EDGE, pieces, [ports])
        mapping = dict(maps[0])
        mapping.update((v,size+i) for v,i in maps[1].items())
        return tree, mapping

    return build(tuple(edges), height)


@dataclass
class LabeledTree:
    sides: tuple
    edges: tuple
    ranks: tuple


def join_after(full, small, a, b):
    """Place a fixed alpha tree after a balanced block when its port rank fits."""
    s = len(full.sides)//2
    if not 0 <= small.ranks[b] < s:
        raise ValueError("joining rank exceeds the available first-piece ranks")
    ranks = full.ranks(a, s-1-small.ranks[b])
    flip = 1 ^ full.sides[a] ^ small.sides[b]
    n = 2*s
    edges = full.edges + tuple((n+u,n+v) for u,v in small.edges) + ((a,n+b),)
    return LabeledTree(full.sides + tuple(flip ^ c for c in small.sides), edges,
                       tuple(ranks) + tuple(s+r for r in small.ranks))


def at_order(edges, ranking, n):
    """Construct an alpha-labeled subdivision at each order above the dyadic threshold."""
    h = max(ranking.values())
    if n < (1<<h):
        raise ValueError("order below the subdivision threshold")
    full, mapping = subdivision(edges, ranking, h)
    rest = n-(1<<h)
    if not rest:
        return LabeledTree(full.sides,full.edges,full.ranks(0,0)), mapping
    path = LabeledTree(tuple(i%2 for i in range(rest)), tuple((i,i+1) for i in range(rest-1)),
                       tuple(i//2 for i in range(rest)))
    incident = [v for e in edges for v in e]
    leaf = next(v for v in mapping if incident.count(v) == 1)
    tree = join_after(full, path, mapping[leaf], 0)
    mapping[leaf] = n-1
    return tree, mapping


def near_power(edges, ranking):
    """At order 2^h-1 with an h-edge-ranking return a labeling of the original tree."""
    n = len(edges)+1
    h = n.bit_length()
    if n != (1<<h)-1 or not edges or max(ranking.values()) != h:
        raise ValueError("expected an extremal tree of order 2^h-1 >= 3")
    cut, halves = split_at_max(tuple(edges), ranking)
    if len(halves[1]) > len(halves[0]):
        cut, halves = cut[::-1], halves[::-1]
    large, small = halves
    full, mapping = subdivision(large, ranking, h-1)
    assert len(mapping) == len(full.sides)
    if small:
        minor, other = near_power(small, {e:ranking[e] for e in small})
    else:
        minor, other = LabeledTree((0,), (), (0,)), {cut[1]:0}
    tree = join_after(full, minor, mapping[cut[0]], other[cut[1]])
    mapping.update((v,len(full.sides)+i) for v,i in other.items())
    return tree, mapping

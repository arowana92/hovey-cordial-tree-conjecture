"""Find small one-vertex witnesses by enumeration and check products on their actual edges."""

from itertools import permutations, product
from random import Random

from research.census.flexible_products import FlexibleTree, aligned_product, substitute
from research.rainbow.verify import rooted_shapes


def tree_sides(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    colors = [-1]*n
    colors[0] = 0
    queue = [0]
    for a in queue:
        for b in adj[a]:
            if colors[b] < 0:
                colors[b] = 1-colors[a]
                queue.append(b)
            assert colors[a] != colors[b]
    assert len(queue) == n and len(edges) == n-1
    return tuple(colors), adj


def catalog(n):
    seen = set()
    balanced = 0
    flexible = []
    for p in rooted_shapes(n).values():
        edges = tuple((u, v) for v, u in enumerate(p[1:], 1))
        sides, adj = tree_sides(n, edges)
        def code(u, parent):
            return "(" + "".join(sorted(code(v, u) for v in adj[u] if v != parent)) + ")"
        key = min(code(i, -1) for i in range(n))
        if key in seen:
            continue
        seen.add(key)
        if sum(sides) != n//2:
            continue
        balanced += 1
        vertices = [[i for i, s in enumerate(sides) if s == side] for side in (0, 1)]
        table = {}
        for left, right in product(permutations(range(n//2)), repeat=2):
            ranks = [0]*n
            for v, r in zip(vertices[0]+vertices[1], left+right):
                ranks[v] = r
            if len({ranks[u]+ranks[v] for u, v in edges}) == n-1:
                row = tuple(ranks)
                for v, r in enumerate(row):
                    table.setdefault((v, r), row)
                if len(table) == n*n//2:
                    break
        if len(table) == n*n//2:
            flexible.append(FlexibleTree(sides, edges, lambda v, r, t=table: t[v, r]))
    return len(seen), balanced, flexible


def verify_product(q, pieces, ports, pins=None):
    n = len(pieces[0].sides)
    total = n*len(pieces)
    actual = substitute(q, pieces, ports)
    edges = [(i*n+a, i*n+b) for i, p in enumerate(pieces) for a, b in p.edges]
    for (a, b), (u, v) in zip(q.edges, ports):
        edges.append((a*n+u, b*n+v))
    sides, _ = tree_sides(total, edges)
    assert actual.edges == tuple(edges)
    assert all(s ^ t == sides[0] ^ actual.sides[0] for s, t in zip(sides, actual.sides))
    count = 0
    for v, r in pins if pins is not None else product(range(total), range(total//2)):
        ranks = actual.ranks(v, r)
        assert ranks[v] == r
        f = [j + (total//2)*s for j, s in zip(ranks, sides)]
        assert sorted(f) == list(range(total))
        assert sorted(f[a]+f[b] for a, b in edges) == list(range(total//2, 3*total//2-1))
        count += 1
    return actual, count


def star(leaves):
    def ranks(vertex, value):
        if vertex == 0:
            assert value == 0
            return (0, *range(leaves))
        others = iter(i for i in range(leaves) if i != value)
        return (0, *(value if i == vertex else next(others) for i in range(1,leaves+1)))
    return FlexibleTree((1,)+(0,)*leaves, tuple((0,i) for i in range(1,leaves+1)), ranks)


def verify_stars(quotient_edges, slots, leaves, ports, root=0, pin=0, rank=0):
    q = len(slots)
    n = leaves+1
    labels, _ = aligned_product(quotient_edges, slots, [star(leaves)]*q, ports, root, pin, rank)
    edges = [(i*n,i*n+v) for i in range(q) for v in range(1,n)]
    edges += [(i*n+u,j*n+v) for (i,j),(u,v) in zip(quotient_edges,ports)]
    sides, _ = tree_sides(n*q, edges)
    cut = sum(sides)
    if any((x < cut) != bool(side) for x,side in zip(labels,sides)):
        cut = len(sides)-cut
        assert all((x < cut) == (not side) for x,side in zip(labels,sides))
    assert sorted(labels) == list(range(n*q))
    assert sorted(labels[u]+labels[v] for u,v in edges) == list(range(cut,cut+n*q-1))
    return labels[root*n+pin] % cut if 2*cut == n*q else None


if __name__ == "__main__":
    bases = {}
    for n in (2, 4, 6, 8, 10):
        shapes, balanced, bases[n] = catalog(n)
        print(f"Order {n}: {shapes} trees, {balanced} balanced, {len(bases[n])} fully attainable")
    edge = bases[2][0]
    path4 = bases[4][0]
    checked = 0
    for flat in product(range(2), repeat=6):
        ports = list(zip(flat[::2], flat[1::2]))
        _, rows = verify_product(path4, [edge]*4, ports)
        checked += rows
    for n, entries in bases.items():
        for a in entries:
            for b in entries:
                for u, v in product(range(n), repeat=2):
                    _, rows = verify_product(edge, [a, b], [(u, v)], [(u, 0), (n+v, n-1)])
                    checked += rows
    rng = Random(8317)
    for _ in range(48):
        q = rng.choice(bases[8])
        pieces = rng.choices(bases[8], k=8)
        ports = [(rng.randrange(8), rng.randrange(8)) for _ in q.edges]
        larger, rows = verify_product(q, pieces, ports)
        checked += rows
        ports = [(rng.randrange(2), rng.randrange(2)) for _ in larger.edges]
        _, rows = verify_product(larger, [edge]*64, ports,
                                 [(rng.randrange(128), r) for r in range(64)])
        checked += rows
    print(f"{checked} independently checked vertex/rank requests on substituted trees")

    count = 0
    for q, leaves in [(3,3), (4,2), (5,2)]:
        edges = [(i,i+1) for i in range(q-1)]
        choices = [(0,0), *product(range(1,leaves+1), repeat=2)]
        for ports in product(choices, repeat=q-1):
            verify_stars(edges, range(q), leaves, ports)
            count += 1
    for _ in range(160):
        q = rng.choice(bases[8])
        leaves = rng.randrange(2,12)
        choices = [(0,0), *product(range(1,leaves+1), repeat=2)]
        ports = rng.choices(choices, k=7)
        root = rng.randrange(8)
        pin = rng.randrange(1,leaves+1)
        for target in range(4*(leaves+1)):
            block, offset = divmod(target, leaves+1)
            odd = int(offset >= leaves)
            quotient_ranks = q.ranks(root, block)
            slots = [2*r + (s ^ q.sides[root] ^ odd) for r,s in zip(quotient_ranks,q.sides)]
            assert verify_stars(q.edges, slots, leaves, ports, root, pin, offset-odd) == target
            count += 1
    print(f"{count} fixed-attachment star products checked, including pins in the larger class")

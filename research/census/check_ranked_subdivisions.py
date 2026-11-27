"""Audit subdivision maps, edge-rank bounds and unchanged near-power trees."""

from itertools import combinations_with_replacement

from research.census.check_flexible_products import tree_sides
from research.census.ranked_subdivisions import at_order, near_power, optimal_ranking, subdivision
from research.rainbow.verify import rooted_shapes


def key(edges):
    n = len(edges)+1
    _, adj = tree_sides(n, edges)
    def word(v, p):
        return "(" + "".join(sorted(word(u,v) for u in adj[v] if u != p)) + ")"
    return min(word(v,-1) for v in range(n))


def bisections(limit):
    """Build all shapes by joining equal halves, then suppress degree-two vertices."""
    layer = [()]
    minimum = {}
    for h in range(1,limit+1):
        m = 1 << (h-1)
        grown = {}
        for left, right in combinations_with_replacement(layer,2):
            base = left + tuple((m+i,m+j) for i,j in right)
            for a in range(m):
                for b in range(m):
                    e = base + ((a,m+b),)
                    grown.setdefault(key(e),e)
        layer = list(grown.values())
        stack = list(layer)
        visited = set()
        while stack:
            e = stack.pop()
            name = key(e)
            if name in visited:
                continue
            visited.add(name)
            minimum.setdefault(name,(h,e))
            _, adj = tree_sides(len(e)+1,e)
            for v, neighbors in enumerate(adj):
                if len(neighbors) == 2:
                    shorter = [uv for uv in e if v not in uv] + [neighbors]
                    stack.append(tuple((u-(u>v),w-(w>v)) for u,w in shorter))
    return minimum


def verify_ranking(edges, ranking):
    # At every threshold, each connected component of the retained edges can
    # contain at most one edge attaining the threshold.
    for level in set(ranking.values()):
        parent = list(range(len(edges)+1))
        def root(x):
            while parent[x] != x:
                x = parent[x]
            return x
        for u,v in edges:
            if ranking[u,v] <= level:
                parent[root(u)] = root(v)
        roots = [root(u) for u,v in edges if ranking[u,v] == level]
        assert len(roots) == len(set(roots))


def verify_map(edges, tree, mapping, n):
    sides, adj = tree_sides(n, tree.edges)
    originals = set(mapping.values())
    assert len(originals) == len(edges)+1 and len(mapping) == len(originals)
    assert all(len(adj[v]) == 2 for v in range(n) if v not in originals)
    reverse = {v:u for u,v in mapping.items()}
    contracted = set()
    for u,start in mapping.items():
        for w in adj[start]:
            prev, v = start, w
            while v not in originals:
                x,y = adj[v]
                prev,v = v, y if x == prev else x
            contracted.add(tuple(sorted((u,reverse[v]))))
    assert contracted == {tuple(sorted(pair)) for pair in edges}
    return sides


def verify_subdivision(edges, tree, mapping, height):
    n = 1 << height
    sides = verify_map(edges, tree, mapping, n)
    for r in range(n//2):
        v = (7*r+3) % n
        ranks = tree.ranks(v,r)
        assert ranks[v] == r
        f = [t+(n//2)*s for t,s in zip(ranks,sides)]
        assert sorted(f) == list(range(n))
        assert sorted(f[u]+f[v] for u,v in tree.edges) == list(range(n//2,3*n//2-1))


def verify_near(edges, ranking):
    out, mapping = near_power(edges, ranking)
    n = len(edges)+1
    assert set(mapping.values()) == set(range(n))
    mapped = {tuple(sorted((mapping[u],mapping[v]))) for u,v in edges}
    assert mapped == {tuple(sorted(pair)) for pair in out.edges}
    colors, _ = tree_sides(n, mapped)
    cut = colors.count(0)
    f = [v+s*cut for v,s in zip(out.ranks,colors)]
    assert sorted(f) == list(range(n))
    assert sorted(f[u]+f[v] for u,v in mapped) == list(range(cut,cut+n-1))


if __name__ == "__main__":
    small = bisections(4)
    checked = set()
    cases = near = additional = 0
    for n in range(2,11):
        for par in rooted_shapes(n).values():
            edges = tuple((p,v) for v,p in enumerate(par[1:],1))
            name = key(edges)
            if name in checked:
                continue
            checked.add(name)
            h, ranked = optimal_ranking(edges)
            verify_ranking(edges,ranked)
            assert (h <= 4) == (name in small)
            if h <= 4:
                assert small[name][0] == h
            for height in range(h,h+2):
                tree, mapping = subdivision(edges,ranked,height)
                verify_subdivision(edges,tree,mapping,height)
                cases += 1
            for rest in (1,3,5,13,(1<<h)+1):
                order = (1<<h)+rest
                tree, mapping = at_order(edges,ranked,order)
                sides = verify_map(edges,tree,mapping,order)
                cut = sides.count(0)
                f = [r+s*cut for r,s in zip(tree.ranks,sides)]
                assert sorted(f) == list(range(order))
                assert sorted(f[u]+f[v] for u,v in tree.edges) == list(range(cut,cut+order-1))
                additional += 1
    for h, edges in small.values():
        rank, ranked = optimal_ranking(edges)
        assert rank == h
        if len(edges)+1 == (1<<h)-1:
            verify_near(edges,ranked)
            near += 1
    print(f"{len(checked)} unrooted input trees, {cases} explicitly verified subdivisions")
    print(f"{additional} further labeled subdivisions at prescribed orders")
    print(f"{len(small)} distinct shapes from independent bisections and suppressions through order 16")
    print(f"{near} original near-power trees with integer alpha-label witnesses")

"""Recompute tree shapes, interval images, speeds, and actual sums independently."""

from collections import Counter, defaultdict

from research.hub.branch_packets import many_site_seed, packet_tree, path_types, seed, star_types


def graph(edges):
    adj = defaultdict(set)
    for x,y in edges:
        assert x != y and y not in adj[x]
        adj[x].add(y)
        adj[y].add(x)
    assert len(edges)+1 == len(adj)
    lo,hi = min(adj),max(adj)
    assert sorted(adj) == list(range(lo,hi+1))
    assert sorted(x+y for x,y in edges) == list(range(lo+1,hi+1))
    return adj


def branch_shape(adj, start, parent, seen):
    assert start not in seen
    seen.add(start)
    return tuple(sorted(branch_shape(adj,y,start,seen) for y in adj[start] if y != parent))


def opposing_triples(d):
    # Perfect Langford sequence at its least possible order, via transpositions.
    s = 2*d-1
    triples = []
    for i in range(s):
        x = d+s+i
        y = d+2*s+2*i%s
        triples.append((x,-y,y-x))
    assert all(sum(triple) == 0 for triple in triples)
    assert sorted(abs(v) for triple in triples for v in triple) == list(range(d,d+3*s))
    return triples


def check_case(parents, offsets, kinds, core_labels=None):
    if core_labels is None:
        edges, original, filler, d = seed(parents,kinds[1][0],offsets)
        num_arms = 2
    else:
        edges, original, filler, d = many_site_seed(parents,core_labels,offsets)
        num_arms = 2*len(core_labels)+1
        assert original[:len(core_labels)] == core_labels
    base = graph(edges)
    width = len(offsets)
    centers = sorted({k[0] for k in kinds})
    assert all(sum(1 for c in offsets if (x-c)%width == 0) == 1 for x in range(width))
    def speed(x):
        c, = [v for v in offsets if (x-v)%width == 0]
        i = (x-c)//width
        return int(i >= d)-int(i <= -d)
    for x,y in edges:
        assert speed(x)+speed(y) == speed(x+y)
    assert all(speed(c) == 0 for c in centers)
    for c in offsets:
        assert min(base)+1 <= width*(1-d)+c <= width*(d-1)+c <= max(base)
    assert len(set(original)) == len(parents) and original[0] == 0 and set(centers) <= set(original)
    original_edges = {frozenset((original[p],original[i])) for i,p in enumerate(parents) if i}
    actual = {frozenset((x,y)) for x,y in edges}
    assert original_edges <= actual and all(base[x] == {0} for x in filler)
    aux = set(base)-set(original)-set(filler)
    assert len(aux) == 2*num_arms
    roots = base[0] & aux
    assert len(roots) == num_arms and all(len(base[x]) == 2 and len(base[x]&aux) == 1 for x in roots)
    assert all(base[x] <= roots and len(base[x]) == 1 for x in aux-roots)
    shapes = []
    for c,root,internal in kinds:
        assert sorted([c+root]+[x+y for x,y in internal]) == sorted(offsets)
        adj = {x:set() for x in offsets}
        for x,y in internal:
            adj[x].add(y)
            adj[y].add(x)
        seen = set()
        shapes.append(branch_shape(adj,root,None,seen))
        assert seen == set(offsets)
    triples = opposing_triples(d)
    # The normalized labels of old vertices move monotonically within each column.
    def old(x):
        return x+3*width*len(triples)*speed(x)
    for phase in (0,1,2):
        assigned = [(j+phase)%len(kinds) if phase == 2 else phase for j in range(len(triples))]
        grown = packet_tree(edges,offsets,d,triples,[kinds[i] for i in assigned])
        hi = max(max(e) for e in grown)
        adj = graph(grown+[(0,hi+1), (0,hi+2)])
        seen = {old(v) for v in base} | {hi+1,hi+2}
        assert all(old(y) in adj[old(x)] for x,y in edges)
        assert adj[hi+1] == adj[hi+2] == {0}
        target = Counter((kinds[i][0],shapes[i]) for i in assigned)
        actual = Counter()
        for c in centers:
            for y in adj[c]-seen:
                actual[c,branch_shape(adj,y,c,seen)] += 1
        assert seen == set(adj) and actual == Counter({k:6*v for k,v in target.items()})


def main():
    families = [star_types(r) for r in range(1,7)]+[path_types(t) for t in range(2,12)]
    # Both seed repairs, arbitrary branching below either hub, and finite mixtures.
    count = 0
    for offsets,kinds in families:
        for parents in ([-1,0], [-1,0,0,0], [-1,0,1,0,2,3,4], [-1,0,1,1,2,0,3,5]):
            check_case(parents,offsets,kinds)
            count += 1
    offsets,kinds = star_types(2)
    extra = (0,1,[(1,-1),(-1,0)])
    check_case([-1,0,0,1,2],offsets,[*kinds,extra])
    count += 1
    # Root three copies of the same three-vertex path at three different vertices.
    offsets = [-2,-1,0]
    # With offsets -1,0,-2 in path order the omitted sum is zero.
    path = [(-1,0),(0,-2)]
    kinds = [(0,0,path),(1,-1,path),(2,-2,path)]
    for parents,labels in (([-1,0,1], [0,1,2]),
                           ([-1,0,1,2,0,2,1,3], [0,1,2,5]),
                           ([-1,0,0,2,3,0,4], [0,1,4,2])):
        check_case(parents,offsets,kinds,labels)
        count += 1
    print(f"Verified {count} interval seeds and {3*count} complete expanded trees.")


if __name__ == "__main__":
    main()

"""Reconstruct segment endpoints and count original edges independently of the constructor."""

from collections import Counter
from random import Random

from research.large_order_gap_paths import leaf_batch
from research.large_order_ranked_hulls import RankedHull, construct


def check_marks(hull):
    edges = {}
    for v in hull.value:
        if v:
            p = hull.tree[v]
            while p not in hull.value:
                p = hull.tree[p]
            edges[v] = p
            assert (hull.depth[v]-hull.depth[p])%2 == 1
    vrows,erows = Counter(),Counter()
    for v,x in hull.value.items():
        s = hull.scale[v]
        vrows[s,x] += 1
        if s >= 128:
            assert s <= 512*abs(x) <= 1024*s
    for v,p in edges.items():
        s = max(hull.scale[v],hull.scale[p])
        w = hull.value[v]+hull.value[p]
        erows[s,w] += 1
        if s >= 128:
            assert s <= 512*abs(w) <= 2048*s
    for s,marks,_,_,_ in hull.stages:
        assert marks <= 1+100*s
    assert max(vrows.values()) < 2**19 and max(erows.values(),default=0) < 2**19
    assert all(hull.value[v] == jump for jump,v in hull.holders.items())
    for s in set(hull.scale.values()):
        assert sum(n for (q,_),n in vrows.items() if q==s) <= 1+100*s
    return len(edges)


def hull_test(tree, ranked, bands, k):
    hull = RankedHull(tree)
    hull.select(ranked,bands)
    for _,r,pop in bands:
        rank = next(rank for rank,rad,_ in bands if rad==r)
        assert all(hull.holders[d] in ranked[:rank] for d in range(1-r,r))
    edge_count = check_marks(hull)
    ids,small,integer,labels,holes = hull.compressed(hull.live,k)
    core_v = Counter(integer.values())
    core_e = Counter(integer[v]+integer[ids[small[i]]] for i,v in enumerate(ids) if i)
    assert max(core_v.values()) < 2**25 and max(core_e.values(),default=0) < 2**25
    actual_v = Counter(labels[v] for v in hull.live)
    actual_e = Counter((labels[v]+labels[tree[v]])%k for v in hull.live if v)
    old_v = Counter(x%k for x in integer.values())
    old_e = Counter((integer[v]+integer[ids[small[i]]])%k for i,v in enumerate(ids) if i)
    for x in range(k):
        assert actual_v[x]-old_v[x] == actual_e[x]-old_e[x]
    return (edge_count, sum(row[2] for row in hull.stages),
            sum(row[3] for row in hull.stages), sum(row[4] for row in hull.stages),len(holes))


def counts(tree,labels,k):
    assert len(tree)==len(labels) and all(0<=x<k for x in labels)
    vertices = [0]*k
    edges = [0]*k
    for i,x in enumerate(labels):
        vertices[x] += 1
        if i:
            p=tree[i]
            assert 0 <= p < i
            edges[(x+labels[p])%k] += 1
    return vertices,edges


def whole(tree,k,ranked,bands,depth=8400):
    built,x,hull,stats = construct(tree,k,ranked,bands,depth)
    v,e = counts(built,x,k)
    assert len(set(e))==1 and sorted(v)==[e[0]]*(k-1)+[e[0]+1]
    assert built[:len(tree)] == tree
    used = Counter(built[len(tree):])
    budget = {p:0 for p in ranked}
    for rank,r,pop in bands:
        for p in ranked[:rank]:
            budget[p] = max(budget[p],pop)
        assert all(hull.holders[d] in ranked[:rank] for d in range(1-r,r))
    assert all(used[p] <= budget[p] for p in used)
    gap = v.index(e[0]+1)
    remaining = []
    for p,n in budget.items():
        # Restore the actual entire population at smaller moduli. The large-k examples
        # separately test the seed against its budget, then restore a fixed partial batch.
        left = n-used[p] if k < 64 else min(1,n-used[p])
        q,tail = divmod(left,k)
        built.extend([p]*(q*k))
        x.extend(list(range(k))*q)
        remaining.extend([p]*tail)
    remaining = remaining if k < 64 else remaining[:7]
    for a in range(0,len(remaining),k):
        batch = remaining[a:a+k]
        extra,gap = leaf_batch([x[p] for p in batch],gap,k)
        built.extend(batch)
        x.extend(extra)
    v,e = counts(built,x,k)
    assert max(v)-min(v)<=1 and max(e)-min(e)<=1
    if k < 64:
        assert Counter(built[len(tree):]) == +Counter(budget)
    return len(built),stats


def stages_at_larger_scales(rng):
    # Recount every intermediate tree, including edges removed by later splits.
    # This ordering puts rich vertices at many unrelated depths in a 140,000-vertex tree.
    tree = [-1]
    for v in range(1,140000):
        tree.append(v-1 if v%13 < 7 else rng.randrange(v))
    hull = RankedHull(tree)
    ranked = [v for v in range(1,len(tree)) if not hull.depth[v]%2]
    rng.shuffle(ranked)
    ranked.insert(0,0)
    counts = []
    for i in range(10):
        s = 1 << i
        candidates = hull.available(ranked[:128*s])
        assert len(candidates) >= 2*s
        hull.add(s,candidates[:2*s],[*range(1-2*s,1-s),*range(s,2*s)])
        counts.append(check_marks(hull))
    return counts


def large_modulus():
    k = 16384
    tree = [-1,0]+[1]*(k-1)
    sites = [0,*range(2,k+1)]
    bands = [(128,2,8192),(2048,32,3072),(k,256,1024)]
    built,labels,hull,stats = construct(tree,k,sites,bands)
    check_marks(hull)
    v,e = counts(built,labels,k)
    assert len(set(e))==1 and sorted(v)==[e[0]]*(k-1)+[e[0]+1]
    budget = Counter()
    for rank,r,pop in bands:
        for p in sites[:rank]:
            budget[p] = max(budget[p],pop)
        assert all(hull.holders[d] in sites[:rank] for d in range(1-r,r))
    used = Counter(built[len(tree):])
    assert all(used[p]<=budget[p] for p in used)
    # Complete each site's prescribed lower bound by full monochromatic-parent batches.
    # Check every shift that occurs in those batches against the actual endpoint formula.
    # Uniform copies of the resulting histograms can be counted without expanding the tree.
    copies = Counter()
    for p,n in budget.items():
        copies[labels[p]] += (n-used[p]+k-1)//k
    for x,c in copies.items():
        if c:
            assert len({(x+y)%k for y in range(k)}) == k
    full = sum(copies.values())
    assert max(v)+full-min(v)-full <= 1 and max(e)+full == min(e)+full
    return len(built),len(built)+k*full,stats[1]


def main():
    rng = Random(20261127)
    totals = [0]*5
    cases = []
    # True radix-to-rank ratio 64. Different depth and BFS orderings exercise all joins.
    for kind in ('path','binary','mixed','broom'):
        n = 66000
        tree = [-1]
        for v in range(1,n):
            if kind=='path':
                p = v-1
            elif kind=='binary':
                p = (v-1)//2
            elif kind=='mixed':
                p = v-1 if v%9<5 else rng.randrange(v)
            else:
                p = v-1 if v%101 else 0
            tree.append(p)
        dep = [0]*n
        for v in range(1,n):
            dep[v] = dep[tree[v]]+1
        ranked = [v for v in range(1,n) if not dep[v]%2]
        rng.shuffle(ranked)
        ranked = [0,*ranked]
        # Keep paths short enough for the independent neutral subdivision solver.
        if kind in ('path','broom'):
            ranked = [0]+sorted(ranked[1:],key=lambda v:(v//1300,rng.random()))
        bands = [(128,2,500),(2048,32,100),(16384,256,40)]
        result = hull_test(tree,ranked,bands,7)
        totals = [a+b for a,b in zip(totals,result)]
    # Tall arms with side branches leave genuine terminals after synchronous peeling.
    for k in (5,7,11):
        tree = [-1]
        ranked = [0]
        for j in range(48):
            p = len(tree)
            tree.extend([0,p])
            ranked.append(p+1)
        bands = [(16,2,1500),(32,4,800)]
        cases.append(whole(tree,k,ranked,bands))
        depth = 8400 if k==5 else 280
        for j in range(5):
            p = 0
            for i in range(depth+4+j):
                tree.append(p)
                p=len(tree)-1
                if i in (7,33):
                    tree.append(p)
        cases.append(whole(tree,k,ranked,bands,depth))
    tree = [-1]+[0]*260
    ranked=[0]
    for v in range(1,261):
        tree.append(v)
        ranked.append(len(tree)-1)
    cases.append(whole(tree,521,ranked,[(128,2,500000),(256,4,250000)]))
    assert all(totals) and any(s[0] for _,s in cases) and any(s[1] for _,s in cases)
    staged = stages_at_larger_scales(rng)
    print(f"Recounted {len(staged)} successive marked trees through {max(staged):,} segments.")
    large = large_modulus()
    print(f"At modulus 16,384: {large[0]:,} seed vertices recounted, {large[2]} repair leaves, "
          f"and a full-batch continuation to order {large[1]:,} checked by residue permutations.")
    print("Four ranked hulls on 66,000-vertex hosts (segments, buffers, parity sites, "
          f"pins on prior paths, neutral subdivisions): {totals}.")
    print(f"{len(cases)} tree replays through {max(n for n,_ in cases):,} vertices. "
          f"{sum(s[0] for _,s in cases)} double paths and {sum(s[1] for _,s in cases)} repair leaves.")


if __name__ == '__main__':
    main()

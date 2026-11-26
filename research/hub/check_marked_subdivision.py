"""Recompute original edges, interval multiplicities, and final marked populations."""

from collections import Counter
from random import Random

from research.hub.check_two_hub_contraction import audit_ranges
from research.hub.marked_leaf_geometry import geometry_seed
from research.hub.marked_leaf_verify import expanded as representative_edges
from research.hub.two_hub_buffer import buffered_complete
from research.hub.uniform_leaf_construct import exact_blocks
from research.hub.marked_leaf_check import check_final, check_seed, graph_of
from research.hub.marked_subdivision import finish_marked, inflate


def check_topology(graph, grown, jobs):
    lengths = {frozenset((u,v)): 5+12*n for u,v,n in jobs}
    for u,neighbors in graph.items():
        found = {}
        for v in grown[u]:
            prev,tip,length = u,v,1
            while tip not in graph:
                assert len(grown[tip])==2
                nxt, = grown[tip]-{prev}
                prev,tip = tip,nxt
                length += 1
            assert tip not in found
            found[tip] = length
        assert found=={v:lengths.get(frozenset((u,v)),1) for v in neighbors}
    assert len(grown)==len(graph)+sum(n-1 for n in lengths.values())


def suffix_cuts():
    rng = Random(37811)
    checks = 0
    for k in range(9,85):
        for s in range(3,9):
            h = rng.randrange(k+1,4*k)
            tree = [-1]+[rng.randrange(v) for v in range(1,h)]
            sites = [0]+rng.sample(range(1,h),s-1)
            counts = sorted((rng.randrange(1,max(2,k//s)) for _ in sites),reverse=True)
            n = h+sum(counts)
            t = (n-1)%k
            if sum(counts)>=t:
                continue
            others = sum(counts[1:])
            keep = h-(t-others)
            assert keep>0
            suffix = set(range(keep,h))
            leaves = suffix-{tree[v] for v in suffix}
            roots = {v for v in suffix if tree[v]<keep}
            assert 1<=len(roots)<=len(leaves)
            assert leaves<=set(range(h))-set(tree[1:])
            full = tree+[v for v,m in zip(sites,counts) for _ in range(m)]
            removed = suffix|set(range(h+counts[0],n))
            crossing = {(full[v],v) for v in removed if full[v] not in removed}
            assert len(removed)==t and (n-t)%k==1
            assert len(crossing)==len(roots)+sum(m for v,m in zip(sites[1:],counts[1:]) if v<keep)
            assert s*(k-1-others)>=k-1
            checks += 1
    return checks


def other_steps():
    found = {}
    marks = list(range(4))
    examples = [
        ([(0,1),(0,2),(0,3)],1,[5,4,3,2],3),
        ([(0,1),(0,4),(2,4),(3,4)],0,[100,90,10,9],4),
    ]
    for edges,mask,profile,wanted in examples:
        populations = {v: n*10**14 for v,n in enumerate(profile)}
        raw = representative_edges(edges,mask)
        graph = graph_of(raw)
        seed = geometry_seed(graph,marks,populations)
        b = max(seed[2])
        assert b==wanted
        grown,seed = inflate(graph,seed,[(*raw[0],2)])
        check_topology(graph,grown,[(*raw[0],2)])
        check_seed(grown,marks,seed)
        check_final(grown,populations,seed,finish_marked(seed,populations))
        found[b] = len(seed[0].edges)
    assert set(found)=={3,4}
    return found


def two_large():
    trees = largest = 0
    for h in (160,2200,6100):
        tree = [-1]+list(range(h-1))
        a,b,other,last = 0,1,h//5,3*h//4
        sites = [a,b,other,last]
        counts = {a:10**60,b:10**20,other:137*h,last:h//7}
        core = tree+sites
        labels,iv,(w,_,_,_) = buffered_complete(core,a,b,pins=sites)
        assert all(abs(labels[v])<=w for v in sites)
        weights = [labels[v]+labels[p] for v,p in enumerate(core) if v]
        audit_ranges(labels,[(x,y) for _,x,y in iv.blocks],iv.lo,iv.hi+1)
        audit_ranges(weights,[(x+p,y+p) for p,x,y in iv.blocks],iv.lo+1,iv.hi+1)
        needs = Counter({labels[v]:n-1 for v,n in counts.items()})
        for p,x,y in iv.blocks:
            needs[p] -= y-x
        blocks = exact_blocks(needs)
        supplied = Counter()
        for block in blocks:
            assert sorted(i+p-block.offset for i,p in enumerate(block.parents))==list(range(len(block.parents)))
            for p,count in Counter(block.parents).items():
                supplied[p] += count*block.copies
        assert needs==supplied and min(needs.values())>=0
        largest = max(largest,len(core))
        trees += 1
    return trees,largest


def main():
    tests = blocks = sites = max_width = max_order = 0
    steps = set()
    for mark_count in (3,4):
        for case in range(4):
            raw = [(0,1),(1,2),(1,3),(3,4)]
            graph = graph_of(raw)
            marks = list(range(mark_count))
            populations = {v: 10**11*(5-v) for v in marks}
            seed = geometry_seed(graph, marks, populations)
            steps.add(max(seed[2]))
            pairs = [raw[case]]
            if case%2:
                pairs.append(raw[(case+2)%4])
            requests = [(u,v,i+case+1) for i,(u,v) in enumerate(pairs)]
            grown_graph, expanded = inflate(graph, seed, requests)
            tree,labels,anchors = expanded
            check_topology(graph,grown_graph,requests)
            check_seed(grown_graph, marks, expanded)
            assert len(labels)==len(graph)+sum(4+12*n for _,_,n in requests)
            extension = finish_marked(expanded,populations)
            check_final(grown_graph,populations,expanded,extension)
            sites += len(pairs)
            blocks += sum(n for _,_,n in requests)
            max_width = max(max_width,tree.hi-tree.lo+1)
            max_order = max(max_order,len(labels))
            tests += 1
    print(f"{tests} complete marked tree certificates through core order {max_order}; "
          f"{sites} elongated segments, {blocks} neutral blocks.")
    more = other_steps()
    steps.update(more)
    cases,h = two_large()
    print(f"{cases} two-large-site completions with pinned minority sites through order {h:,}.")
    print(f"{suffix_cuts()} forest suffixes checked with three through eight attachment sites.")
    print(f"Lattice steps {sorted(steps)}, largest explicitly recounted interval {max(max_width,max(more.values())+1):,}; "
          "all final prescribed leaf counts and permutation blocks verified.")


if __name__=='__main__':
    main()

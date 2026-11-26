"""Independently verify the asymmetric marked construction on the original paths."""

from collections import Counter

from research.hub.check_two_hub_contraction import audit_ranges
from research.hub.dominant_marked import finish, inflate
from research.hub.marked_leaf_check import graph_of
from research.hub.marked_leaf_geometry import geometry_seed


def verify(graph, original, jobs, labels, iv):
    distances = {frozenset((u,v)): 1+12*n+(2 if i==0 else 0) for i,(u,v,n) in enumerate(jobs)}
    for u in original:
        reached = {}
        for v in graph[u]:
            prev,cur,d = u,v,1
            while cur not in original:
                assert len(graph[cur])==2
                nxt, = graph[cur]-{prev}
                prev,cur = cur,nxt
                d += 1
            assert cur not in reached
            reached[cur] = d
        assert reached=={v:distances.get(frozenset((u,v)),1) for v in original[u]}
    assert len(graph)==len(original)+sum(d-1 for d in distances.values())
    assert set(graph)==set(labels)
    weights = [labels[u]+labels[v] for u in graph for v in graph[u] if u<v]
    audit_ranges(list(labels.values()),[(a,b) for _,a,b in iv.blocks],iv.lo,iv.hi+1)
    audit_ranges(weights,[(a+p,b+p) for p,a,b in iv.blocks],iv.lo+1,iv.hi+1)


def main():
    standard = graph_of([(0,1),(1,2),(1,3),(3,4),(4,5),(3,6)])
    extra = graph_of([(1,0),(2,1),(3,2),(4,2),(5,4),(6,3),(7,1)])
    cases = moves = 0
    largest = minority = width = 0
    orientations = set()
    for graph,marks in ((standard,[0,2,4]),(standard,[0,1,2,3]),(standard,[2,0,1,4]),(extra,[7,5,2])):
        for reflect in (False,True):
            for n in (35,240,1500):
                seed = geometry_seed(graph,marks,{v:5-i for i,v in enumerate(marks)})
                tree,old,anc = seed
                possible = [v for v,x in old.items() if x==int(reflect)]
                if not possible:
                    continue
                main_site, = possible
                others = [v for v in graph if old[v] not in anc and v!=main_site]
                sites = set(marks)|{main_site}|set(others[:1])
                edges = [(u,v) for u in graph for v in graph[u] if u<v]
                orient = (lambda x:1-x) if reflect else (lambda x:x)
                usable = [(u,v) for u,v in edges if orient(old[u])*orient(old[v]) and
                          orient(old[u])+orient(old[v])]
                second = usable[-1]
                first = next(e for e in edges if e!=second)
                jobs = [(*first,n),(*second,n//3)]
                grown,labels,iv,anchors,(r,m) = inflate(graph,seed,main_site,jobs)
                verify(grown,graph,jobs,labels,iv)
                assert labels[main_site]==0
                assert m==sum(b-a for p,a,b in iv.blocks if p)
                assert m < 500*(len(grown)+1).bit_length()
                populations = {v:10**10 for v in sites}
                populations[main_site] = 10**70
                positive = next(v for v in marks if labels[v]>0)
                moment = sum(labels[v]*c for v,c in populations.items())
                populations[positive] += max(0,10**11-moment)
                blocks = finish(labels,iv,anchors,populations)
                actual = Counter()
                for p,a,b in iv.blocks:
                    actual[p] += b-a
                for block in blocks:
                    assert sorted(i+p-block.offset for i,p in enumerate(block.parents))==list(range(len(block.parents)))
                    for p,c in Counter(block.parents).items():
                        actual[p] += c*block.copies
                assert actual==Counter({labels[v]:c for v,c in populations.items()})
                cases += 1
                moves += r
                minority = max(minority,m)
                largest = max(largest,len(grown))
                width = max(width,iv.hi-iv.lo+1)
                orientations.add((len(anc),reflect))
    assert {(3,False),(3,True),(4,False),(4,True)}<=orientations
    print(f"{cases} asymmetric interval and exact-population certificates through core order {largest:,}; "
          f"{moves} buffer moves.")
    print(f"Largest recounted interval {width:,}; at most {minority} seed leaves away from zero; "
          f"anchor/orientation cases {sorted(orientations)}.")


if __name__=='__main__':
    main()

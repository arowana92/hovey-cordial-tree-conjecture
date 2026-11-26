"""Audit equal-multiset partial forests and polynomial two-hub completions."""

from collections import Counter
from random import Random
from research.hub.check_two_hub_contraction import audit_ranges
from research.hub.check_two_hub_buffer import audit as audit_buffer
from research.hub.polynomial_two_hubs import complete, forest_seed, polynomial_bound
from research.rainbow.verify import rooted_shapes


def verify(tree,a,b):
    result = complete(tree,a,b)
    if result is None:
        bigger = tree+[a,b]
        degrees = Counter(bigger[1:])+Counter(range(1,len(bigger)))
        core = Counter()
        for v,p in enumerate(bigger[1:],1):
            if min(degrees[v],degrees[p])>1:
                core.update((v,p))
        assert max(core.values(),default=0)<=2
        return None
    labels,iv,stats = result
    assert labels[a]==0 and labels[b]==1 and len(set(labels))==len(tree)
    assert all(p in (0,1) for p,x,y in iv.blocks)
    assert iv.hi-iv.lo+1<=polynomial_bound(len(tree))
    weights = [labels[v]+labels[p] for v,p in enumerate(tree) if v]
    audit_ranges(labels,[(x,y) for _,x,y in iv.blocks],iv.lo,iv.hi+1)
    audit_ranges(weights,[(x+p,y+p) for p,x,y in iv.blocks],iv.lo+1,iv.hi+1)
    return stats


def boundary_test(rng):
    tree = [-1]
    parents = {}
    for arm,pinned in enumerate((0,401,-39,-900,22,22,401)):
        p = 0
        for i in range(520+30*arm):
            if not p:
                parents[len(tree)] = pinned
            tree.append(p)
            p = len(tree)-1
            if i%79==42:
                tree.append(p)
    labels,stats = forest_seed(tree,parents,len(tree),1000,rng)
    weights = []
    for v,x in labels.items():
        actual = labels[tree[v]] if tree[v] else parents[v]
        weights.append(actual+x)
    assert Counter(weights)==Counter(labels.values()) and len(set(weights))==len(weights)
    assert all(1000<abs(x)<2**19*(len(tree)+1001) for x in weights)
    assert min(stats)>0
    return len(tree)-1,stats


def main():
    rng = Random(19843)
    small = residual = 0
    for n in range(2,10):
        for raw in rooted_shapes(n).values():
            tree = list(raw)
            for b in range(1,n):
                for a,b1 in ((0,b),(b,0)):
                    stats = verify(tree,a,b1)
                    small += 1
                    residual += stats is None
    transfers = subdivisions = levels = largest = large_tests = 0
    for size in (120,630,1300,2900):
        tree = [-1]
        tips = []
        for j in range(7):
            p = 0
            for i in range(size+5*j):
                tree.append(p)
                p = len(tree)-1
                if i%61==28:
                    tree.append(p)
            tips.append(p)
        for a,b in ((0,tips[0]),(tips[0],0),(tips[2],tips[1]),(19,tips[-1]//2)):
            w,m,s,d = verify(tree,a,b)
            transfers += m
            subdivisions += s
            levels = max(levels,d)
            largest = max(largest,len(tree))
            large_tests += 1
    buffer_cases = buffer_moves = buffer_blocks = 0
    for length in (37,1800):
        for j in range(4):
            tree = [-1,0,1,2,3,4,5,6]
            for parent0 in (j,5,7,1):
                p = parent0
                for _ in range(length+parent0):
                    tree.append(p)
                    p = len(tree)-1
            a,b = (j,7-j) if j!=3 else (8,8+length+3)
            r,k,_,_ = audit_buffer(tree,a,b,use_polynomial=True)
            assert (r>0)==(length>100) and bool(k)==bool(r)
            buffer_moves += r
            buffer_blocks += k
            buffer_cases += 1
    n,stats = boundary_test(rng)
    print(f"{small:,} ordered marked cores through order 9, including {residual} caterpillar returns.")
    print(f"{large_tests} deep replays through order {largest:,}; {transfers:,} transfers, "
          f"{subdivisions:,} neutral subdivisions, up to {levels} finishing levels.")
    print(f"{buffer_cases} forced polynomial branch replays, {buffer_moves} buffer subdivisions, {buffer_blocks:,} neutral blocks.")
    print(f"Direct boundary-edge audit on {n:,} free vertices with repeated, signed and zero pins: {stats}.")


if __name__=='__main__':
    main()

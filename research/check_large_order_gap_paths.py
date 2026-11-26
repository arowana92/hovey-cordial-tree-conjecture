"""Recount the endpoint sums after path corrections, peeling, and suppression."""

from collections import Counter
from itertools import product
from random import Random

from research.large_order_check import histograms
from research.large_order_gap_paths import common, gap_path, leaf_batch, paired_path


def endpoint_counts(p, walk, k):
    return Counter((a+b) % k for a, b in zip([p]+walk, walk))


def check_steps():
    specs = batches = 0
    for k in range(2, 18):
        for p,s,t in product(range(k), repeat=3):
            for walk in (gap_path(p,s,t), paired_path(p,s,t,(2*p+3*t+1) % k,k)):
                weights = endpoint_counts(p,walk,k)
                weights[t] += 1
                want = Counter(x % k for x in walk)
                want[s] += 1
                assert weights == want
            specs += 1
    for k in range(2, 6):
        for n in range(k+1):
            for shifts in product(range(k), repeat=n):
                for gap in range(k):
                    lab,g = leaf_batch(shifts,gap,k)
                    w = Counter((x+p) % k for x,p in zip(lab,shifts))
                    w[g] += 1
                    v = Counter(lab)
                    v[gap] += 1
                    assert w == v and max(Counter(lab).values(), default=0) <= 2
                    if n == k:
                        assert all(v[x] == 1 + (x == g) for x in range(k))
                    batches += 1
    return specs,batches


def tree_case(k, tree, depth=336):
    lab,g,stats = common(tree,k,depth)
    v,e = histograms(tree,lab,k)
    assert lab[0] == 0 and all(v[i]-e[i] == (i==g) for i in range(k))
    assert max(abs(k*q-len(tree)) for q in v)<=13000*k
    # Give actual additional leaves to the chosen root, then recount their sums.
    target = max(v) + 1
    fill = [x for x in range(k) for _ in range(target+(x==g)-v[x])]
    vf,ef = histograms(tree+[0]*len(fill),lab+fill,k)
    assert max(vf)-min(vf)==1 and len(set(ef))==1
    return len(tree),stats


def main():
    specs,batches = check_steps()
    rng = Random(17703)
    results = []
    for k in range(2, 9):
        for rem in (0, 7, 19, 36):
            tree = [-1]
            for j in range(max(1,k-1)):
                end = 0
                for _ in range(336 + rem + j):
                    tree.append(end)
                    end = len(tree)-1
            results.append(tree_case(k,tree))
        for n in (13,36,97,510):
            tree = [-1]+[rng.randrange(i) for i in range(1,n)]
            results.append(tree_case(k,tree))
    # Branchpoints and leaves off the reserved paths survive in the full tree.
    for k in (5,6,8):
        tree = [-1,0,1]
        for j in range(3):
            end = 1+j%2
            for i in range(341+j):
                tree.append(end)
                end = len(tree)-1
                if i % 54 == 1:
                    tree.append(end)
        results.append(tree_case(k,tree))
    by_kind = list(zip(*(s for _,s in results)))
    assert all(sum(counts) for counts in by_kind)
    print(f"{specs:,} single and double path parameter triples, {batches:,} Hall batches.")
    print(f"{len(results)} entire trees through order {max(n for n,_ in results):,}, "
          f"{sum(by_kind[0]):,} double paths, {sum(by_kind[1])} neutral subdivisions, "
          f"{sum(by_kind[2]):,} complete pruning batches.")


if __name__=='__main__':
    main()

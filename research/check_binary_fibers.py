"""Compare binary elimination with actual full sums and exhaustive fiber orders."""

from collections import defaultdict
from itertools import product
from math import gcd
from random import Random

from research.binary_fibers import count_lifts, cyclic_edges, eliminate, lift, paired_rows


def valid(labels, edges, weights, m):
    return sorted(labels) == list(range(2*m)) and len({
        (labels[u]+labels[v]+b)%(2*m) for (u,v),b in zip(edges,weights)
    }) == len(edges)


def brute(low, edges, weights, m):
    fibers = [[i for i,a in enumerate(low) if a == j] for j in range(m)]
    solutions = 0
    for bits in product((0,1),repeat=m):
        labels = list(low)
        for j,bit in enumerate(bits):
            labels[fibers[j][bit]] += m
        solutions += valid(labels,edges,weights,m)
    return solutions


def split_tree(m, rng):
    # A spanning tree uses first copies; the other m edges attach one leaf
    # clone each via an incidence matching. The first chord cycle spans all colors.
    first = [(x,y) for a in range(m) for x,y in [((a-1)%m,(a+1)%m)]]
    removed = rng.randrange(m)
    # Reserve one first-cycle edge and all m-1 second edges. Give each an
    # endpoint whose clone is still unused using a bipartite matching.
    tree = [(2*x,2*y) for i,(x,y) in enumerate(first) if i != removed]
    spare = [first[removed]]+[((a-3)%m,(a+3)%m) for a in range(1,m)]
    owner = {}
    def match(i,seen):
        for v in spare[i]:
            if v not in seen:
                seen.add(v)
                if v not in owner or match(owner[v],seen):
                    owner[v] = i
                    return True
        return False
    for i in range(m):
        if not match(i,set()):
            return None
    tree.extend((2*v+1,2*(y if x==v else x)) for v,i in owner.items() for x,y in [spare[i]])
    return tree


def main():
    rng = Random(1991)
    trials = solutions = split = 0
    for m in range(1,9):
        low = list(range(m))*2
        for trial in range(300):
            rng.shuffle(low)
            edges = [(rng.randrange(i),i) for i in range(1,2*m)]
            biases = [rng.randrange(-2*m,2*m+1) for _ in edges]
            if trial%2 == 0:
                # Guarantee the required multiplicities of the low weights.
                targets = (list(range(m))*2)[:-1]
                rng.shuffle(targets)
                biases = [m*(b&1)+t-low[u]-low[v] for b,t,(u,v) in zip(biases,targets,edges)]
            predicted = lift(low,edges,biases,m)
            count = brute(low,edges,biases,m)
            assert (predicted is not None) == bool(count)
            if predicted is not None:
                labels,rank = predicted
                assert valid(labels,edges,biases,m) and count == 2**(m-rank)
                solutions += 1
            trials += 1
    rank_tests = 0
    for m in range(3,52,2):
        for r in range(min(m,7)):
            for s in range(r+1,min(m,11)):
                q = cyclic_edges(m,r,s)
                low = [i//2 for i in range(2*m)]
                edges = [(2*x+rng.randrange(2),2*y+rng.randrange(2)) for x,y in q]
                _,rows = paired_rows(low,edges,[0]*len(q),m)
                _,rank = eliminate([(a,0) for a,b in rows])
                assert rank == m-gcd(m,s-r)-gcd(m,s+r)+gcd(gcd(m,s-r),s+r)
                rank_tests += 1
        if m >= 5:
            for _ in range(15):
                edges = split_tree(m,rng)
                if edges is None:
                    continue
                biases = [m*rng.randrange(2) for _ in edges]
                low = [i//2 for i in range(2*m)]
                labels,rank = lift(low,edges,biases,m)
                assert rank == m-1 and valid(labels,edges,biases,m)
                adj = defaultdict(set)
                for a,b in edges:
                    assert a != b and b not in adj[a]
                    adj[a].add(b)
                    adj[b].add(a)
                seen = {0}
                for _ in range(2*m):
                    seen.update(y for x in tuple(seen) for y in adj[x])
                assert len(seen) == 2*m
                split += 1
    counted = 0
    for m in (2,3,4,5):
        for n in range(1,11):
            for trial in range(7):
                low = [j%m for j in range(n)]
                rng.shuffle(low)
                edges = [(rng.randrange(j),j) for j in range(1,n)]
                biases = [0 if trial%2 else rng.randrange(2*m) for _ in edges]
                expected = 0
                for bits in product((0,1),repeat=n):
                    labels = [a+m*b for a,b in zip(low,bits)]
                    vhist = [0]*(2*m)
                    whist = [0]*(2*m)
                    for x in labels:
                        vhist[x] += 1
                    for (u,v),b in zip(edges,biases):
                        whist[(labels[u]+labels[v]+b)%(2*m)] += 1
                    expected += max(vhist)-min(vhist) <= 1 and max(whist)-min(whist) <= 1
                assert count_lifts(low,edges,biases,m) == expected
                counted += 1
    print(f"Checked the all-orders counting identity on {counted} inputs.")
    assert split
    print(f"Checked {trials} systems against exhaustive lifts, {solutions} feasible; "
          f"{rank_tests} exact circulant ranks and {split} whole split trees.")


if __name__ == "__main__":
    main()

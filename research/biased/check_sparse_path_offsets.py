"""Check path permutations, unit-orbit coverage, and serial block expansions."""
import argparse
from collections import defaultdict
from itertools import permutations, product
from math import comb, gcd
from pathlib import Path
from random import Random


def sources(k, path):
    units = [u for u in range(1, k) if gcd(k, u) == 1]
    covered = defaultdict(set)
    records = {}
    with path.open() as stream:
        for line in stream:
            i, j, a, b, *labels = map(int, line.split())
            assert len(labels) == k and set(labels) == set(range(k))
            assert 0 <= i <= j < k and 0 <= a < k and 0 <= b < k
            assert (i == 0) == (a == 0) and (j == 0) == (b == 0)
            assert not i or i < j
            offsets = [0]*k
            offsets[i], offsets[j] = a, b
            weights = {(labels[v-1]+labels[v]+offsets[v]) % k for v in range(1,k)}
            assert len(weights) == k-1
            orbit = {(u*a % k, u*b % k) for u in units}
            seen = covered[i,j]
            assert not seen.intersection(orbit)
            seen.update(orbit)
            # The replay indexes any valid representative, without assuming which
            # one the generator picked or how it ordered the rows.
            records[i,j,a,b] = labels
    total = sum(map(len, covered.values()))
    assert total == 1+(k-1)**2+comb(k-1,2)*(k-1)**2
    return units, records, total


def path_labels(offsets, k, units, records):
    marked = [(i,b % k) for i,b in enumerate(offsets,1) if b % k]
    (i,a),(j,b) = ([(0,0)]*(2-len(marked)) + marked)
    for u in units:
        row = records.get((i,j,u*a % k,u*b % k))
        if row is not None:
            inverse = pow(u,-1,k)
            return [x*inverse % k for x in row[:len(offsets)+1]]
    raise AssertionError("uncovered short path")


def random_block(k, rng):
    # The labels are the vertex IDs. Grow a tree while independently enforcing
    # distinct edge sums. Retry if its partial labeling cannot be completed.
    while True:
        order = list(range(k))
        rng.shuffle(order)
        edges, weights = [], set()
        for i in range(1,k):
            x = order[i]
            options = [v for v in order[:i] if (x+v) % k not in weights]
            if not options:
                break
            parent = rng.choice(options)
            edges.append((parent,x))
            weights.add((parent+x) % k)
        if len(edges) == k-1:
            hole, = set(range(k))-weights
            return edges, hole, rng.randrange(k), rng.randrange(k)


def replay(k, units, records):
    rng = Random(1991+k)
    for trial in range(96):
        n = rng.randint(2,k)
        chains = [[] for _ in range(n-1)]
        slots = [rng.randrange(n-1) for _ in range(2)]
        if trial % 3 == 0:
            slots[1] = slots[0]
        for slot in slots:
            chains[slot].append(random_block(k,rng))
        offsets = [sum(p+q-hole for _,hole,p,q in blocks) % k for blocks in chains]
        labels = path_labels(offsets,k,units,records)
        edges = []
        for i, blocks in enumerate(chains):
            left = i
            for internal,hole,p,q in blocks:
                start = len(labels)
                shift = labels[left]+p-hole
                labels.extend((v+shift) % k for v in range(k))
                edges.extend((start+x,start+y) for x,y in internal)
                edges.append((left,start+p))
                left = start+q
            edges.append((left,i+1))
        counts = [sum(x == c for x in labels) for c in range(k)]
        edge_counts = [0]*k
        for u,v in edges:
            edge_counts[(labels[u]+labels[v]) % k] += 1
        assert len(edges) == len(labels)-1
        assert max(counts)-min(counts) <= 1 and max(edge_counts)-min(edge_counts) <= 1


def four():
    bad = set()
    for offsets in product(range(4), repeat=3):
        if offsets.count(0) < 1:
            continue
        if not any(len({(x[i]+x[i+1]+b) % 4 for i,b in enumerate(offsets)}) == 3
                   for x in permutations(range(4))):
            bad.add(offsets)
    assert bad == {(0,1,0),(0,3,0),(1,0,1),(3,0,3)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("moduli", nargs="+", type=int)
    args = parser.parse_args()
    four()
    for k in args.moduli:
        units, records, total = sources(k,args.directory/f"sparse-path-{k}.txt")
        replay(k,units,records)
        print(f"k={k} witnesses={len(records)} literal_paths={total} expanded_trees=96")

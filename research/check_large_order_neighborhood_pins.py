"""Verify the pin bounds and induced subgraphs against a parent-array edge list."""

from collections import Counter
from itertools import product
from random import Random

from research.large_order_neighborhood_pins import extract, neighborhood_labels


def check_labels(tree, k, pins, limit):
    labels, cap = neighborhood_labels(tree,k,pins,limit)
    assert all(labels[v] == x for v,x in pins.items())
    assert all(0 <= x < k for x in labels)
    vertex = Counter(labels)
    edge = Counter((labels[i]+labels[tree[i]]) % k for i in range(1,len(tree)))
    incident = Counter()
    for i,p in enumerate(tree[1:],1):
        if i in pins:
            incident[p] += 1
        if p in pins:
            incident[i] += 1
    u = sum(n > limit for n in incident.values())
    d = limit+u+1
    assert cap == max(2*u+2,4*((len(tree)+k-1)//k)*(d+1))+d
    assert max(vertex.values()) <= cap and max(edge.values(),default=0) <= cap


def check_subforest(tree, t):
    parts = extract(tree,t)
    degree = Counter(tree[1:])
    degree.update(range(1,len(tree)))
    if not parts:
        populations = Counter()
        for i,p in enumerate(tree[1:],1):
            if degree[i] == 1:
                populations[p] += 1
            if degree[p] == 1:
                populations[i] += 1
        nearby = Counter()
        for i,p in enumerate(tree[1:],1):
            if degree[i]>1 and degree[p]>1:
                nearby[p] += int(populations[i] >= t)
                nearby[i] += int(populations[p] >= t)
        assert sum(n>=2*t-1 for n in nearby.values()) < 2*t-1
        return False
    assert len(parts) == t
    all_sites = []
    claimed = set()
    for center,arms in parts:
        assert len(arms) == t
        all_sites.append(center)
        for parent,tips in arms:
            assert len(tips) == t and all(degree[v] == 1 for v in tips)
            all_sites.extend([parent,*tips])
            claimed.add(tuple(sorted((center,parent))))
            claimed.update(tuple(sorted((parent,v))) for v in tips)
    sites = set(all_sites)
    assert len(sites) == len(all_sites) == t*(1+t+t*t)
    actual = {(p,i) for i,p in enumerate(tree[1:],1) if p in sites and i in sites}
    assert claimed == actual
    return True


def crowded_tree(t, rng):
    # Consecutive centers share a rich neighbor. Additional arms have spare leaves.
    tree = [-1]
    centers = [0]
    for _ in range(2*t-2):
        bridge = len(tree)
        tree += [centers[-1],bridge]
        centers.append(bridge+1)
        tree.extend([bridge]*t)
    for center in centers:
        for _ in range(2*t-1):
            parent = len(tree)
            tree.append(center)
            tree.extend([parent]*(t+rng.randrange(3)))
    return tree


def main():
    rng = Random(20261127)
    pinned = inspected = induced = 0
    for n in range(1,8):
        for row in product(*(range(i) for i in range(1,n))):
            tree = [-1,*row]
            parity = [0]*n
            for i in range(1,n):
                parity[i] = 1-parity[tree[i]]
            for side in (0,1):
                sites = [i for i in range(n) if parity[i]==side]
                for mask in range(1<<len(sites)):
                    subset = [v for i,v in enumerate(sites) if mask >> i & 1]
                    k = max(1,len(subset)+rng.randrange(3))
                    pins = dict(zip(subset,rng.sample(range(k),len(subset))))
                    check_labels(tree,k,pins,rng.randrange(4))
                    pinned += 1
            for t in (1,2):
                induced += int(check_subforest(tree,t))
                inspected += 1
    max_order = 0
    for t in range(2,15):
        tree = crowded_tree(t,rng)
        assert check_subforest(tree,t)
        max_order = max(max_order,len(tree))
        inspected += 1
        induced += 1
    # Few prescribed neighbors despite many vertices of unbounded ordinary degree.
    for k in (11,37,101):
        tree = [-1]
        pins = {}
        for x in range(k):
            center = len(tree)
            tree.append(0)
            pins[len(tree)] = x
            tree.extend([center]*(3*k))
        check_labels(tree,k,pins,1)
        pinned += 1
    print(f"{pinned:,} pinned trees with independently recounted bins.")
    print(f"{inspected:,} extraction checks, {induced:,} induced forests, "
          f"structured hosts through {max_order:,} vertices.")


if __name__ == "__main__":
    main()

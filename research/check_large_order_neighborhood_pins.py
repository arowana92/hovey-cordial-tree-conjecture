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
    exceptions = {v for v,n in incident.items() if n > limit}
    u = len(exceptions)
    size = 1
    while size*size < u:
        size += 1
    d = limit+2*size+1
    average = (len(tree)+k-1)//k
    adjacent = Counter()
    for i,p in enumerate(tree[1:],1):
        if i in exceptions:
            adjacent[p] += 1
        if p in exceptions:
            adjacent[i] += 1
    extra = {v for v,n in adjacent.items() if v not in pins and n>size}
    assert len(extra) <= size
    other_fixed = set(pins) | extra
    pin_children, extra_children, exceptional_children = Counter(), Counter(), Counter()
    for i,p in enumerate(tree[1:],1):
        weight = (labels[i]+labels[p]) % k
        if i in exceptions and p in other_fixed:
            exceptional_children[weight] += 1
        if p in exceptions and i in pins:
            pin_children[weight] += 1
        if p in exceptions and i in extra:
            extra_children[weight] += 1
    assert max(exceptional_children.values(),default=0) <= 3*size+average
    assert max(pin_children.values(),default=0) <= size
    assert sum(extra_children.values()) <= size
    assert max(Counter(labels[v] for v in exceptions).values(),default=0) <= 2*size+average
    assert cap == max(6*size+average+2,4*average*(d+1))+d
    assert max(vertex.values()) <= cap and max(edge.values(),default=0) <= cap


def check_subforest(tree, t, count=None):
    if count is None:
        count = t
    parts = extract(tree,t,count)
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
        assert sum(n>=t+3 for n in nearby.values()) < 4*count-1
        return False
    assert len(parts) == count
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
    assert len(sites) == len(all_sites) == count*(1+t+t*t)
    actual = {(p,i) for i,p in enumerate(tree[1:],1) if p in sites and i in sites}
    assert claimed == actual
    return True


def crowded_tree(t, count, rng):
    # Consecutive centers share a rich neighbor. Additional arms have spare leaves.
    tree = [-1]
    centers = [0]
    for _ in range(2*count-1):
        bridge = len(tree)
        tree += [centers[-1],bridge]
        centers.append(bridge+1)
        tree.extend([bridge]*t)
    for center in centers:
        for _ in range(t+3):
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
        count = t*t if t <= 9 else t
        tree = crowded_tree(t,count,rng)
        assert check_subforest(tree,t,count)
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
    # Many exceptional vertices, overlapping neighborhoods and nonzero sorted parent labels.
    for k in (3,13,47,127):
        tree = [-1]
        pins = {}
        for j in range(k):
            center = len(tree)
            tree.append(0)
            tree.append(center)
            pins[center+1] = (5*j+1) % k
            for _ in range(3):
                other = len(tree)
                tree.extend([center+1,other])
        check_labels(tree,k,pins,0)
        pinned += 1
    for k in (2,4,7):
        tree = [-1] + [0]*(5*k*k)
        check_labels(tree,k,{0:k-1},0)
        pinned += 1
    print(f"{pinned:,} pinned trees with independently recounted bins.")
    print(f"{inspected:,} extraction checks, {induced:,} induced forests, "
          f"structured hosts through {max_order:,} vertices.")


if __name__ == "__main__":
    main()

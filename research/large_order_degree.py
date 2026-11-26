"""Construct the high-degree labeling, including restoration of all deleted leaves."""

from collections import Counter
from random import Random


def walk(d):
    odd = d if d % 2 else d-1
    r = odd//2
    arr = [0]
    for j in range(r):
        arr.extend([j-r, 1+j])
    arr.append(0)
    if d % 2 == 0:
        arr.append(0)
    return arr


def counts(parents, labels, k):
    vert, edge = [0]*k, [0]*k
    for i, label in enumerate(labels):
        if label is not None:
            vert[label] += 1
            if i:
                edge[(label+labels[parents[i]]) % k] += 1
    return vert, edge


def balanced(v):
    return max(v)-min(v) <= 1


def attach_batch(parents, labels, batch, k):
    vert, edge = counts(parents, labels, k)
    surplus = vert.index(max(vert))
    assert balanced(vert) and vert.count(max(vert)) == 1 and len(set(edge)) == 1
    first = batch[:k-1]

    def search(j, available, used):
        if j == len(first):
            return True
        v = first[j]
        for x in available:
            w = (labels[parents[v]]+x) % k
            if w not in used:
                labels[v] = x
                if search(j+1, available-{x}, used|{w}):
                    return True
        labels[v] = None
        return False

    assert search(0, set(range(k))-{surplus}, set())
    if len(batch) == k:
        v = batch[-1]
        edge = counts(parents, labels, k)[1]
        labels[v] = (edge.index(min(edge))-labels[parents[v]]) % k
    assert all(balanced(a) for a in counts(parents, labels, k))


def label_tree(parents, k):
    children = [[] for _ in parents]
    for i, p in enumerate(parents[1:], 1):
        children[p].append(i)
    assert len(children[0]) >= 4*k*k
    active = set(range(len(parents)))
    seed = {0, *children[0]}
    degree = list(map(len, children))
    leaves = {v for v in active-seed if degree[v] == 0}
    batches = []
    size = (len(parents)-1) % k or k
    while len(leaves) >= size:
        batch = [leaves.pop() for _ in range(size)]
        active.difference_update(batch)
        batches.append(batch)
        for v in batch:
            p = parents[v]
            degree[p] -= 1
            if degree[p] == 0 and p not in seed:
                leaves.add(p)
        size = k
    reserve = [v for v in children[0] if degree[v] == 0]
    core = active-set(reserve)
    lab = [None]*len(parents)
    lab[0] = 0
    for v in sorted(core):
        if v and degree[v] == 1:
            continue
        for child in children[v]:
            if child not in core:
                continue
            path = [child]
            while degree[path[-1]] == 1:
                path.append(next(x for x in children[path[-1]] if x in core))
            for x, label in zip(path, walk(len(path))[1:]):
                lab[x] = label % k
    assert all(lab[v] is not None for v in core)
    vert, edge = counts(parents, lab, k)
    assert vert == [edge[0]+1, *edge[1:]]
    q, r = divmod(len(active), k)
    slots = [x for x in range(k) for _ in range(q+(x < r)-vert[x])]
    assert len(slots) == len(reserve)
    for v, x in zip(reserve, slots):
        lab[v] = x
    for batch in reversed(batches):
        attach_batch(parents, lab, batch, k)
    assert None not in lab and all(balanced(a) for a in counts(parents, lab, k))
    return len(batches)


def main():
    for d in range(1, 101):
        seq = walk(d)
        assert len(seq) == d+1 and seq[0] == seq[-1] == 0
        for k in range(1, 25):
            v = Counter(x % k for x in seq[1:])
            e = Counter((a+b) % k for a, b in zip(seq, seq[1:]))
            assert v == e and max(v.values()) <= d/k+2
    rng = Random(1991)
    batches = []
    for k in range(2, 10):
        for case in range(3):
            stem = 4*k*k
            parents = [-1]+[0]*stem
            for j in range(9*k):
                parents.append(1+j % (k+2) if case == 0 or rng.randrange(3) == 0
                               else len(parents)-1)
            batches.append(label_tree(parents, k))
    print("2400 segment histograms; 24 whole high-degree trees;",
          sum(batches), "outside batches restored")


if __name__ == "__main__":
    main()

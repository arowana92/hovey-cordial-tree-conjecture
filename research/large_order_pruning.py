"""Construct depth-pruned cores, restore the batches, and count both histograms."""

from math import isqrt
from random import Random
from research.large_order_degree import walk, attach_batch, counts, balanced


def check(branches, k):
    b = len(branches)
    h = 1+isqrt(b-1)
    p = k*(5*h+2)
    parents = branches+[0]*p
    children = [[] for _ in parents]
    for i in range(1, b):
        children[parents[i]].append(i)
    live = set(range(b))
    reserve = list(range(b, b+p))
    undo = []
    first = (len(parents)-1) % k
    if first:
        undo.append([reserve.pop() for _ in range(first)])
    for _ in range(h):
        leaves = [v for v in live if v and not live.intersection(children[v])]
        if not leaves:
            break
        assert len(leaves) <= k
        undo.append(leaves+[reserve.pop() for _ in range(k-len(leaves))])
        live.difference_update(leaves)
    kids = {v: [w for w in children[v] if w in live] for v in live}
    terminals = sum(not kids[v] for v in live if v)
    assert terminals <= b//(h+1)
    labels = [None]*len(parents)
    labels[0] = 0
    segments = 0
    for v in sorted(live):
        if v and len(kids[v]) == 1:
            continue
        for w in kids[v]:
            path = [w]
            while len(kids[path[-1]]) == 1:
                path.append(kids[path[-1]][0])
            for w, x in zip(path, walk(len(path))[1:]):
                labels[w] = x % k
            segments += 1
    assert segments <= 2*terminals
    vert, weights = counts(parents, labels, k)
    assert vert == [weights[0]+1, *weights[1:]]
    target, rem = divmod(len(live)+len(reserve), k)
    fill = [x for x in range(k) for _ in range(target+(x < rem)-vert[x])]
    assert len(fill) == len(reserve)
    for v, x in zip(reserve, fill):
        labels[v] = x
    for batch in reversed(undo):
        attach_batch(parents, labels, batch, k)
    assert None not in labels and all(balanced(hist) for hist in counts(parents, labels, k))
    return len(undo), terminals


if __name__ == '__main__':
    rng = Random(17)
    restored = cases = nonempty = 0
    for k in range(2, 9):
        for arms in range(1, k+1):
            for upper in (2, 11, 35):
                parents = [-1]
                for _ in range(arms):
                    at = rng.randrange(len(parents))
                    for _ in range(rng.randint(1, upper)):
                        parents.append(at)
                        at = len(parents)-1
                steps, leaves = check(parents, k)
                restored += steps
                nonempty += leaves > 0
                cases += 1
    print(f"{cases} entire trees; {restored} restored batches; {nonempty} residual cores with branches")

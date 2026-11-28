"""Complete arbitrary edge offsets using leaves at matched physical sites."""
from collections import Counter
from math import ceil, log, sqrt
from random import Random

from research.hub.breadth_first_leaves import finish_from_divisible


def complete(k, core, parents, offsets, leaves, deficient=None):
    """Leaves are (old vertex, offset) pairs. Return None if the supply test fails."""
    h = len(core)
    assert len(parents) == len(offsets) == h-1 and k >= 1
    vertex = Counter(core)
    edge = Counter((core[p]+core[v]+b) % k for v, (p, b) in enumerate(zip(parents, offsets), 1))
    a = max(max(vertex.values()), max(edge.values(), default=0))
    depth = a-min(vertex[x] for x in range(k))
    slots = [[] for _ in range(k)]
    for j, (p, b) in enumerate(leaves, h):
        slots[(core[p]+b) % k].append(j)
    if min(map(len, slots)) < 2*depth:
        return None
    d = next(w for w in range(k) if edge[w] < a) if deficient is None else deficient
    assert edge[d] < a
    missing = [w for w in range(k) for _ in range(a-edge[w]-int(w == d))]
    labels = list(core)+[-1]*len(leaves)
    for layer in range(depth):
        inputs = [x for x in range(k) if vertex[x]+layer < a]
        for x in inputs:
            # The whole list is increasing, so each layer receives decreasing weights.
            w = missing.pop()
            s = (w-x) % k
            labels[slots[s].pop()] = x
    assert not missing
    spare = [(s, v) for s, bucket in enumerate(slots) for v in bucket]
    finish_from_divisible(k, labels, spare, d)
    return labels


def check(k, labels, parents, offsets, leaves):
    assert len(labels) == len(parents)+1+len(leaves)
    assert all(0 <= x < k for x in labels)
    edges = list(zip(parents, offsets))+leaves
    weights = [(labels[v]+labels[p]+b) % k for v, (p,b) in enumerate(edges, 1)]
    for histogram in (Counter(labels), Counter(weights)):
        bins = [histogram[x] for x in range(k)]
        assert max(bins)-min(bins) <= 1


def checks():
    geometry = Random(271953)
    palette = Random(270819)
    large = small = 0
    for k in (2, 3, 5, 8, 12, 16, 27, 32):
        h = ceil(300*k*log(8*k))
        sites = ceil(8*sqrt(h*k*log(8*k)))
        for style in ('star', 'path', 'branching'):
            if style == 'star':
                parents = [0]*(h-1)
            elif style == 'path':
                parents = list(range(h-1))
            else:
                parents = [geometry.randrange(v) for v in range(1, h)]
            offsets = [geometry.randrange(k) for _ in parents]
            selected = geometry.sample(range(h), sites)
            leaves = [(p, geometry.randrange(k)) for p in selected]
            leaves.extend((p, geometry.randrange(k)) for p in selected[:k] for _ in range(3))
            for _ in range(50):
                core = [palette.randrange(k) for _ in range(h)]
                labels = complete(k, core, parents, offsets, leaves)
                if labels is not None:
                    break
            else:
                raise AssertionError("no usable initial coloring")
            check(k, labels, parents, offsets, leaves)
            large += 1
    for k in range(2, 16):
        for h in (k, 2*k+1, 2*k+k//2, 3*k-1):
            parents = [geometry.randrange(v) for v in range(1, h)]
            offsets = [geometry.randrange(k) for _ in parents]
            core = [palette.randrange(k) for _ in range(h)]
            # Supply every effective shift with enough multiplicity at one old site.
            leaves = [(0, b) for _ in range(2*h) for b in range(k)]
            labels = complete(k, core, parents, offsets, leaves)
            check(k, labels, parents, offsets, leaves)
            small += 1
    print(f'{large} trees meeting the site bound, {small} fixed cores with prescribed offsets')


if __name__ == '__main__':
    checks()

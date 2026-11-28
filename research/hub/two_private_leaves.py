"""Construct the two-leaf extensions using restricted sums or the upper-range bound."""
from collections import Counter
from random import Random

from research.hub.breadth_first_leaves import breadth_first, finish_batches, ordered_trees


def helper_weights(k, old, length):
    counts = Counter(old)
    allowed = [w for w in range(k) if counts[w] < 3]
    assert max(counts.values()) <= 3 and len(counts) >= k-length
    assert 0 < length < len(allowed)
    # One bit mask witnesses each attainable cardinality and sum.
    choices = [{0: 0}] + [{} for _ in range(length)]
    for i, w in enumerate(allowed):
        for n in range(min(length, i+1), 0, -1):
            for total, mask in choices[n-1].items():
                choices[n].setdefault((total+w) % k, mask | (1 << i))
    for total, mask in choices[length].items():
        d = (3*sum(range(k))-sum(old)-total) % k
        if counts[d] < 2:
            return [w for i, w in enumerate(allowed) if mask >> i & 1]
    raise AssertionError("missing attainable deficiency")


def distinct_shifts(k, inputs, outputs):
    """Search the finite transversal; each result is (physical shift, input)."""
    def match(xs, ys, shifts):
        if not xs:
            return []
        def options(x):
            return [(y, (y-x) % k) for y in ys if (y-x) % k not in shifts]
        candidates, x = min(((options(x), x) for x in xs), key=lambda pair: len(pair[0]))
        for y, s in candidates:
            rest = match(xs-{x}, ys-{y}, shifts | {s})
            if rest is not None:
                return [(s, x)] + rest
        return None
    rows = match(set(inputs), set(outputs), set())
    assert rows is not None
    return rows


def suffix_labels(k, parents):
    h = len(parents)+1
    size = [1]*h
    children = [[] for _ in range(h)]
    for v in range(h-1, 0, -1):
        p = parents[v-1]
        size[p] += size[v]
        children[p].append(v)
    todo = [0]
    preorder = []
    while todo:
        v = todo.pop()
        preorder.append(v)
        todo.extend(sorted(children[v], key=lambda w: (-size[w], -w)))
    prefix, suffix = preorder[:k], preorder[k:]
    number = {v: i for i, v in enumerate(prefix)}
    core = [-1]*h
    for i, j in enumerate(breadth_first([number[parents[v-1]] for v in prefix[1:]])):
        core[prefix[j]] = i
    # Direct search on the small physical forest with the two forbidden inputs.
    def grow(i, used, weights):
        if i == len(suffix):
            return True
        v = suffix[i]
        s = core[parents[v-1]]
        for x in range(k):
            y = (s+x) % k
            if x not in used and y not in weights:
                core[v] = x
                if grow(i+1, used | {x}, weights | {y}):
                    return True
        return False
    assert grow(0, {0, 1}, set())
    return core


def tail_helpers(k, r, old):
    counts = Counter(old)
    shifts = Counter()
    rows = []
    for x in range(r, k-1):
        s = next(s for s in range(r) if shifts[s] < 2 and counts[(s+x) % k] < 3)
        shifts[s] += 1
        counts[(s+x) % k] += 1
        rows.append((s, x))
    total = sum(w*c for w, c in counts.items())
    for s in range(r):
        w = (s+k-1) % k
        d = (4*sum(range(k))-total-w) % k
        if shifts[s] < 2 and counts[w] < 4 and counts[d] < 4 and d != w:
            return rows+[(s, k-1)]
    raise AssertionError("missing final helper")


def verify(k, parents, populations, mode):
    h = len(parents)+1
    r = h-k
    core = [-1]*h
    if mode == "forest":
        core = suffix_labels(k, parents)
    else:
        for i, v in enumerate(breadth_first(parents)):
            core[v] = i % k
    old = [(core[v]+core[p]) % k for v, p in enumerate(parents, 1)]
    if mode == "tail":
        rows = tail_helpers(k, r, old)
        batches = 2
    else:
        inputs = [v for v, n in sorted(Counter(core).items()) if n == 1]
        outputs = helper_weights(k, old, len(inputs))
        rows = distinct_shifts(k, inputs, outputs)
        batches = 1
    labels = finish_batches(k, core, populations, old, batches, rows)
    physical = list(parents) + [v for v, n in enumerate(populations) for _ in range(n)]
    assert len(labels) == len(physical)+1 and all(0 <= x < k for x in labels)
    edge_weights = [(labels[v]+labels[p]) % k for v, p in enumerate(physical, 1)]
    for values in (labels, edge_weights):
        hist = Counter(values)
        assert max(hist.values()) - min(hist[w] for w in range(k)) <= 1


def checks():
    rng = Random(27041952)
    counts = Counter()
    for h in range(3, 9):
        for parents in ordered_trees(h):
            for k in range(2, h):
                r = h-k
                if r >= k:
                    continue
                if 2*r <= k:
                    mode = "lower"
                elif 5*r >= 4*k:
                    mode = "tail"
                elif k-r >= 2:
                    mode = "forest"
                else:
                    continue
                verify(k, parents, [2]*h, mode)
                counts[mode] += 1
    for k in (9, 12, 15, 16, 18, 21):
        for r in sorted({2, k//2, k//2+1, (3*k)//4, (4*k+4)//5, k-1}):
            h = k+r
            for parents in ([0]*(h-1), list(range(h-1)), [rng.randrange(v) for v in range(1,h)]):
                mode = "lower" if 2*r <= k else "tail" if 5*r >= 4*k else "forest"
                verify(k, parents, [2+rng.randrange(3) for _ in range(h)], mode)
                counts[mode] += 1
    print(dict(sorted(counts.items())))


if __name__ == "__main__":
    checks()

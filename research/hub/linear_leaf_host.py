"""Construct a super edge-magic host by attaching leaves to original vertices."""
from collections import Counter, deque
from random import Random

from research.hub.breadth_first_leaves import finish_from_divisible, ordered_trees


def consecutive_host(parents, tip):
    h = len(parents)+1
    graph = [[] for _ in range(h)]
    edges = [(p, v) for v, p in enumerate(parents, 1)]
    for p, v in edges:
        graph[p].append(v)
        graph[v].append(p)
    assert h >= 3 and len(graph[tip]) == 1
    root, = graph[tip]
    order = []
    queue = deque([(root, tip)])
    while queue:
        v, previous = queue.popleft()
        order.append(v)
        queue.extend((w, v) for w in graph[v] if w != previous)
    label = [0]*h
    for i, v in enumerate(order):
        label[v] = i
    occupied = {label[p]+label[v] for p, v in edges if tip not in (p, v)}
    assert len(occupied) == h-2
    center = h-1
    while center in occupied:
        center += 1
    width = center-(h-1)
    label[tip] = center
    occupied.add(center)
    y = center+1
    for x in range(h-1, center):
        while y in occupied:
            y += 1
        edges.append((order[y-x], len(label)))
        label.append(x)
        occupied.add(y)
        y += 1
    assert len(occupied) == center
    offset = center-sum(y < center for y in occupied)
    padding = int(bool(width) and offset-1 == width and h-2 not in occupied)
    left = [y for y in range(1-padding, center) if y not in occupied]
    right = [y for y in range(center+1, max(occupied)+1) if y not in occupied]
    xs = list(range(-len(left), 0))
    if width:
        tail = sum(y-x == h-1 for y, x in zip(left, xs))
        if tail:
            size = max(width+1, tail)
            assert size <= len(left)
            block = xs[-size:]
            xs[-size:] = block[size-width:] + block[:size-width]
    originals = {label[v]: v for v in range(h)}
    for y, x in zip(left+right, xs+list(range(center+1, center+1+len(right)))):
        edges.append((originals[y-x], len(label)))
        label.append(x)
    return label, edges, originals[offset], originals[offset-1]


def short_host(parents):
    h = len(parents)+1
    edges = [(p, v) for v, p in enumerate(parents, 1)]
    neighbors = [[] for _ in range(h)]
    for p, v in edges:
        neighbors[p].append(v)
        neighbors[v].append(p)
    tips = [[v for v in nbrs if len(neighbors[v]) == 1] for nbrs in neighbors]
    interior = {v for v in range(h) if len(neighbors[v]) > 1}
    if any(len(interior.intersection(neighbors[v])) > 2 for v in interior):
        hub = max(interior, key=lambda v: len(tips[v]))
        return consecutive_host(parents, tips[hub][0])

    # Visit a caterpillar's edges along its spine, assigning within-class
    # ranks in order of first occurrence on each side of the bipartition.
    start = next(v for v in sorted(interior) if len(interior.intersection(neighbors[v])) <= 1)
    sides = [[start], []]
    side, previous, v = 0, -1, start
    while True:
        sides[1-side].extend(tips[v])
        following = [w for w in neighbors[v] if w in interior and w != previous]
        if not following:
            break
        previous, v = v, following[0]
        side = 1-side
        sides[side].append(v)
    label = [0]*h
    for i, v in enumerate(sides[0]+sides[1]):
        label[v] = i
    return label, edges, sides[1][0], sides[0][-1]


def verify(parents, tip, extend):
    h = len(parents)+1
    if tip is None:
        label, edges, lower, upper = short_host(parents)
        assert len(label) <= 2*h-3
    else:
        label, edges, lower, upper = consecutive_host(parents, tip)
        assert len(label) <= 2*h-1
    assert lower != upper
    assert edges[:h-1] == [(p, i) for i, p in enumerate(parents, 1)]
    assert all(p < h and v == j for j, (p, v) in enumerate(edges[h-1:], h))
    def intervals():
        n = len(label)
        sums = {label[p]+label[v] for p, v in edges}
        assert sorted(label) == list(range(min(label), min(label)+n))
        assert len(edges) == n-1 and sorted(sums) == list(range(min(sums), min(sums)+n-1))
    intervals()
    for site, count, step in ((lower, extend[0], -1), (upper, extend[1], 1)):
        x = min(label) if step == -1 else max(label)
        for _ in range(count):
            x += step
            edges.append((site, len(label)))
            label.append(x)
    intervals()


def modular_check(k, parents, populations):
    h = len(parents)+1
    labels, edges, lower, upper = short_host(parents)
    left = list(populations)
    for p, _ in edges[h-1:]:
        left[p] -= 1
    assert min(left) >= 0
    need = -len(labels) % k
    for p, step in ((lower, -1), (upper, 1)):
        take = min(need, left[p])
        need -= take
        left[p] -= take
        end = min(labels) if step < 0 else max(labels)
        for _ in range(take):
            end += step
            edges.append((p, len(labels)))
            labels.append(end)
    assert need == 0
    labels = [x % k for x in labels]
    old = Counter((labels[p]+labels[v]) % k for p, v in edges)
    d, = [w for w in range(k) if old[w] < len(labels)//k]
    spare = []
    for p, n in enumerate(left):
        for _ in range(n):
            spare.append((labels[p], len(labels)))
            edges.append((p, len(labels)))
            labels.append(-1)
    finish_from_divisible(k, labels, spare, d)
    assert Counter(p for p, v in edges[h-1:]) == Counter({v:n for v, n in enumerate(populations) if n})
    assert all(0 <= x < k for x in labels)
    for hist in (Counter(labels), Counter((labels[p]+labels[v]) % k for p, v in edges)):
        counts = [hist[x] for x in range(k)]
        assert max(counts)-min(counts) <= 1


def checks():
    small = broad = repaired = choices = 0
    rng = Random(270523)
    for h in range(3, 10):
        for parents in ordered_trees(h):
            verify(parents, None, (3, 4))
            choices += 1
            for tip in range(h):
                if parents.count(tip)+int(tip != 0) != 1:
                    continue
                verify(parents, tip, (2, 3))
                small += 1
    for h in (10, 17, 27, 41, 80, 151):
        for _ in range(80):
            parents = [rng.randrange(v) for v in range(1, h)]
            tip = rng.choice([i for i in range(1, h) if i not in parents])
            verify(parents, tip, (rng.randrange(12), rng.randrange(12)))
            verify(parents, None, (7, 1))
            choices += 1
            broad += 1
            label, _, _, _ = consecutive_host(parents, tip)
            repaired += label[tip] > h-1
    assert repaired
    modular = 0
    for h in (3, 7, 13, 19, 24):
        for k in (3, 8, 17, 27, 38):
            for _ in range(5):
                parents = [rng.randrange(v) for v in range(1, h)]
                least = max(h-3, (k+h-3)//2)
                modular_check(k, parents, [least+rng.randrange(k) for _ in range(h)])
                modular += 1
    print(f'{small} small marked trees, {broad} larger marked trees; '
          f'{repaired} larger cases needed preliminary leaves, {choices} short hosts, '
          f'{modular} prescribed-population modular labelings')


if __name__ == '__main__':
    checks()

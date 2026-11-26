"""Check the disjoint path reservoir and the pinned-star reduction on small hosts."""

from itertools import combinations, product


def path_family(colors, u, v):
    n = len(colors)
    used_vertices = {u, v}
    used_colors = set()
    family = []
    for _ in range(n // 30):
        a = next(a for a in range(n) if a not in used_vertices and colors[u][a] not in used_colors)
        blocked = used_colors | {colors[u][a]}
        b = next(b for b in range(n) if b not in used_vertices and b != a
                 and colors[a][b] not in blocked and colors[b][v] not in blocked)
        family.append((u, a, b, v))
        used_vertices.update((a, b))
        used_colors.update((colors[u][a], colors[a][b], colors[b][v]))
    inner = [x for p in family for x in p[1:3]]
    weights = [colors[x][y] for p in family for x, y in zip(p, p[1:])]
    assert len(set(inner)) == 2 * len(family) and not {u, v}.intersection(inner)
    assert len(set(weights)) == 3 * len(family)


def check_forest(parents, colors, forbidden, k):
    """Embed the auxiliary tree, then rescore the original forest from scratch."""
    hub_values = sorted(set(colors) | {forbidden})
    center = next(x for x in range(k) if x not in hub_values)
    labels = [center] + hub_values
    tree = [-1] + [0] * len(hub_values)
    start = len(tree)
    boundary = iter(colors)
    original_parents = []
    for p in parents:
        if p == -1:
            c = next(boundary)
            tree.append(1 + hub_values.index(c))
            original_parents.append(-1 - c)
        else:
            tree.append(start + p)
            original_parents.append(p)
    used = {(center + c) % k for c in hub_values}
    def complete():
        if len(labels) == len(tree):
            return True
        parent = labels[tree[len(labels)]]
        for x in range(k):
            w = (x + parent) % k
            if x in labels or w in used:
                continue
            used.add(w)
            labels.append(x)
            if complete():
                return True
            labels.pop()
            used.remove(w)
        return False
    assert complete()
    free = labels[start:]
    assert len(set(free)) == len(parents) and forbidden not in free
    weights = [(x + (free[p] if p >= 0 else -1-p)) % k for x, p in zip(free, original_parents)]
    assert len(set(weights)) == len(parents)


if __name__ == '__main__':
    pairs = forests = 0
    for n in (30, 61, 95, 127):
        for colors in ( [[(i+j) % n for j in range(n)] for i in range(n)],
                        [[(min(i, j), max(i, j)) for j in range(n)] for i in range(n)] ):
            for u, v in combinations(range(n), 2):
                path_family(colors, u, v)
                pairs += 1
    for size in range(1, 5):
        for parents in product(*(range(-1, i) for i in range(size))):
            for colors in product((0, 2, 5), repeat=parents.count(-1)):
                for forbidden in (0, 3):
                    check_forest(parents, colors, forbidden, 16)
                    forests += 1
    print(f"{pairs} endpoint pairs; {forests} forests with prescribed boundaries and a forbidden label")

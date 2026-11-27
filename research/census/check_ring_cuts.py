"""Recount the possible corridor pieces by deleting pairs of actual tree edges."""

from itertools import combinations
from random import Random

from ..rainbow.verify import rooted_shapes


def check(parents):
    n = len(parents)
    neighbors = [[] for _ in range(n)]
    for v in range(1,n):
        u = parents[v]
        neighbors[u].append(v)
        neighbors[v].append(u)

    # Check all choices of through directions, including the chosen largest child.
    tests = 0
    targets = {26: 0, 27: 0}
    for v, adj in enumerate(neighbors):
        if len(adj) < 3:
            continue
        ways = {}
        for u in adj:
            stack = [(u,v)]
            mass = leaves = 0
            while stack:
                x, old = stack.pop()
                mass += 1
                leaves += len(neighbors[x]) == 1
                stack.extend((y,x) for y in neighbors[x] if y != old)
            corridor = [v,u]
            while len(neighbors[corridor[-1]]) == 2:
                corridor.append(next(y for y in neighbors[corridor[-1]] if y != corridor[-2]))
            ways[u] = mass, leaves, corridor
        for left, right in combinations(adj,2):
            a, b = ways[left][2], ways[right][2]
            w = sum(ways[u][0] for u in adj if u not in (left,right))
            q = sum(ways[u][1] for u in adj if u not in (left,right))
            attainable = set()
            for i in range(len(a)-1):
                for j in range(len(b)-1):
                    # Remove the edge just beyond the i-th and j-th kept vertices.
                    stops = {a[i+1],b[j+1]}
                    piece = {v}
                    todo = [v]
                    for x in todo:
                        for y in neighbors[x]:
                            if y not in stops and y not in piece:
                                piece.add(y)
                                todo.append(y)
                    assert sum(len(neighbors[x]) == 1 for x in piece) == q
                    assert len(piece) == 1+w+i+j
                    if a[i] != b[j] and b[j] not in neighbors[a[i]]:
                        attainable.add(len(piece))
                        if len(piece) in targets and q in (2,3,4):
                            targets[len(piece)] += 1
                    tests += 1
            predicted = {s for s in range(1+w, 1+w+len(a)-2+len(b)-2+1) if s-w >= 3}
            assert predicted == attainable
    return tests, targets


def main():
    trees = cases = 0
    counts = {26: 0, 27: 0}
    rng = Random(1991)

    def record(tree):
        nonlocal trees, cases
        checked, targets = check(tree)
        trees += 1
        cases += checked
        for k in counts:
            counts[k] += targets[k]

    for n in range(3,12):
        for parent in rooted_shapes(n).values():
            record(parent)
    for _ in range(200):
        base = [-1] + [rng.randrange(v) for v in range(1,rng.randrange(6,17))]
        parent, ends = [-1], [0]
        for u in base[1:]:
            last = ends[u]
            for _ in range(rng.randrange(1,11)):
                parent.append(last)
                last = len(parent)-1
            ends.append(last)
        record(parent)
    assert all(counts.values())
    print(trees, "trees,", cases, "two-edge cuts, removable pieces", counts)


if __name__ == "__main__":
    main()

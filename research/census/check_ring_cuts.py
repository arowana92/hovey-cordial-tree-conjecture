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
    directions = {}
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
        directions[v] = ways
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
    pair_tests = 0
    total_leaves = sum(len(adj)==1 for adj in neighbors)
    for u, ways in directions.items():
        for link, (_,_,middle) in ways.items():
            v = middle[-1]
            if v<=u or v not in directions:
                continue
            gap = len(middle)-2
            for outer,(first_mass,first_tips,a) in ways.items():
                if outer == link:
                    continue
                for end,(last_mass,last_tips,b) in directions[v].items():
                    if end == middle[-2]:
                        continue
                    low = n-first_mass-last_mass
                    forest = low-2-gap
                    q = total_leaves-first_tips-last_tips
                    actual = set()
                    for i in range(len(a)-1):
                        for j in range(len(b)-1):
                            stops = {a[i+1],b[j+1]}
                            seen = {u}
                            todo = [u]
                            for x in todo:
                                for y in neighbors[x]:
                                    if y not in stops and y not in seen:
                                        seen.add(y)
                                        todo.append(y)
                            assert len(seen)==low+i+j
                            assert sum(len(neighbors[x])==1 for x in seen)==q
                            if b[j] not in neighbors[a[i]]:
                                actual.add(len(seen))
                            pair_tests += 1
                    high = low+len(a)+len(b)-4
                    assert actual=={s for s in range(low,high+1) if s-forest>=3}
    return tests, targets, pair_tests


def main():
    trees = cases = pairs = 0
    counts = {26: 0, 27: 0}
    rng = Random(1991)

    def record(tree):
        nonlocal trees, cases, pairs
        checked, targets, paired = check(tree)
        pairs += paired
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
    print(trees, "trees,", cases, "single-joint cuts, removable pieces", counts,
          "and", pairs, "two-joint cuts")


if __name__ == "__main__":
    main()

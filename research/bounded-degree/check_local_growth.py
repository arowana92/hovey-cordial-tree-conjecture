"""Check the three covering subtrees on actual consecutive preorder intervals."""
from collections import Counter
from itertools import product
from random import Random


def prepare(parents):
    n = len(parents)
    children = [[] for _ in range(n)]
    for v in range(1, n):
        children[parents[v]].append(v)
    order, descendants = {}, {}
    for v in reversed(range(n)):
        children[v].sort(key=lambda w: len(order[w]))
        order[v] = [v] + [x for w in children[v] for x in order[w]]
        descendants[v] = set(order[v])
    return order[0], descendants


def check(parents, starts=None):
    order, descendants = prepare(parents)
    total = deepest = cover_three = 0
    n = len(order)
    for a in range(1,n) if starts is None else starts:
        prefix = set(order[:a])
        group = {}
        for b in range(a,n if starts is None else min(n,a+200)):
            v = order[b]
            p = parents[v]
            if p in prefix:
                group[p] = group.get(p, {p})
                current = p
            group[current].add(v)
            last = list(group)[-2:]
            cover = [group[x] for x in last]
            if len(group)>2:
                previous = list(group)[-3]
                r = last[0]
                child = previous
                while parents[child]!=r:
                    child = parents[child]
                cover.append(descendants[child])
                cover_three += 1
            t = b-a+1
            for tree in cover:
                assert len(tree) <= t+1
                assert sum(parents[v] not in tree for v in tree) == 1
            for x in order[a:b+1]:
                assert any(x in tree and parents[x] in tree for tree in cover)
            deepest = max(deepest,len(group))
            total += 1
    return total, deepest, cover_three


def packets(parents, m):
    # Edges are identified by their child. Each exported packet is connected.
    children = [[] for _ in parents]
    for v in range(1, len(parents)):
        children[parents[v]].append(v)
    pending = {}
    batch = []
    threshold = m//2
    for v in reversed(range(len(parents))):
        rest = []
        for w in children[v]:
            rest.extend(pending.pop(w))
            rest.append(w)
            if len(rest) >= threshold:
                batch.append(rest)
                rest = []
        pending[v] = rest
    if pending[0]:
        batch.append(pending[0])
    return batch


def check_packets():
    rng = Random(270214)
    tests = 0
    for n in (8, 17, 95, 400):
        for parents in ([None]+list(range(n-1)), [None]+[0]*(n-1),
                        [None]+[(v-1)//3 for v in range(1,n)],
                        [None]+[rng.randrange(v) for v in range(1,n)]):
            for m in range(2,min(47,n)+1):
                chunks = packets(parents,m)
                flat = [v for chunk in chunks for v in chunk]
                assert sorted(flat) == list(range(1,n))
                total_degree = Counter()
                copies = Counter()
                excess = 0
                for i,chunk in enumerate(chunks):
                    degree = Counter(chunk)
                    degree.update(parents[v] for v in chunk)
                    assert len(degree) == len(chunk)+1 <= m
                    assert i == len(chunks)-1 or len(chunk) >= m//2
                    assert sum(parents[v] not in degree for v in degree) == 1
                    copies.update(degree.keys())
                    total_degree.update(degree)
                    excess += sum(max(0,d-3) for d in degree.values())
                assert sum(r-1 for r in copies.values()) == len(chunks)-1
                assert sum(max(0,d-3) for d in total_degree.values()) <= excess+3*(len(chunks)-1)
                tests += 1
    return tests


def main():
    total = triple = depth = 0
    for n in range(2,9):
        for p in product(*(range(i) for i in range(1,n))):
            count, d, three = check((None,)+p)
            total += count
            triple += three
            depth = max(depth, d)
    # Complete binary tree gives many distinct boundary parents in one block.
    p = [None]+[(v-1)//2 for v in range(1,2047)]
    count, d, three = check(p, [11, 38, 77, 1000, 1969])
    total += count
    triple += three
    depth = max(depth,d)
    assert triple and depth >= 5
    print(f"edge partition and excess checks={check_packets()}")
    print(f"connected three-subtree covers={total} three used={triple} maximum parents={depth}")


if __name__ == "__main__":
    main()

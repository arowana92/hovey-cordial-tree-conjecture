"""Choose the component sizes on the boundary of a connected subtree."""

from collections import deque


def choose_fringe(parents, size, target):
    """Exclude size vertices, in at least three components or a prescribed pair."""
    n = len(parents)
    if not (2 <= size <= n-2 and 1 <= target < size):
        raise ValueError("Expected room for two components and two retained vertices")
    if parents[0] != -1 or any(not 0 <= p < v for v,p in enumerate(parents[1:],1)):
        raise ValueError("Expected a tree in parent order")
    neighbors = [[] for _ in parents]
    for v,p in enumerate(parents[1:],1):
        neighbors[p].append(v)
        neighbors[v].append(p)
    degrees = list(map(len,neighbors))
    queue = deque(v for v,d in enumerate(degrees) if d == 1)
    removed = set()
    while len(removed) < size:
        v = queue.popleft()
        removed.add(v)
        for u in neighbors[v]:
            if u not in removed:
                degrees[u] -= 1
                if degrees[u] == 1:
                    queue.append(u)

    def boundary():
        groups = []
        for root in removed:
            for anchor in neighbors[root]:
                if anchor in removed:
                    continue
                count = 0
                stack = [(root,anchor)]
                while stack:
                    v,prev = stack.pop()
                    count += 1
                    stack.extend((u,v) for u in neighbors[v] if u != prev and u in removed)
                groups.append((count,root,anchor))
        return sorted(groups)

    target = min(target,size-target)
    while True:
        groups = boundary()
        if len(groups) >= 3 or groups[0][0] == target:
            return removed
        assert len(groups) == 2
        small,big = groups
        grow,shrink = (small,big) if small[0] < target else (big,small)
        removed.remove(shrink[1])
        removed.add(grow[2])

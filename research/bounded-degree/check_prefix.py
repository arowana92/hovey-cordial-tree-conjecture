"""Exhaustively check suffix components and the degree-excess bound on small trees."""

from itertools import product


def check(parents):
    n = len(parents) + 1
    children = [[] for _ in range(n)]
    for i, p in enumerate(parents, 1):
        children[p].append(i)
    size = [1] * n
    for i in reversed(range(1, n)):
        size[parents[i - 1]] += size[i]
    order, pending = [], [0]
    while pending:
        v = pending.pop()
        order.append(v)
        pending.extend(sorted(children[v], key=size.__getitem__, reverse=True))
    degrees = [len(row) + int(i != 0) for i, row in enumerate(children)]
    excess = sum(max(0, d - 3) for d in degrees)
    prefix = set()
    for i, v in enumerate(order[:-1], 1):
        prefix.add(v)
        t = n - i
        crossing = [(p, j) for j, p in enumerate(parents, 1) if (j in prefix) != (p in prefix)]
        sources = {p for p, _ in crossing}
        if not sources <= prefix or len(sources) > 1 + t.bit_length():
            raise ValueError((parents, prefix, crossing))
        if len(crossing) > 3 * (1 + t.bit_length()) + excess:
            raise ValueError("excess bound failed")
    return n - 1


if __name__ == "__main__":
    checks = 0
    for n in range(1, 10):
        for parents in product(*(range(i) for i in range(1, n))):
            checks += check(parents)
    print(f"Verified {checks} cuts of parent-first trees through order nine.")

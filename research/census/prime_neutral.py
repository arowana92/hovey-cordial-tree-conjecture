"""Exact uniform increments for two positive grandchild populations at a prime."""

from heapq import heappop, heappush


def distances(k, steps):
    """Smallest nonnegative sum of the generators in each residue class."""
    dist = [None] * k
    dist[0] = 0
    pending = [(0, 0)]
    while pending:
        value, i = heappop(pending)
        if value != dist[i]:
            continue
        for step in steps:
            j = (i + step) % k
            candidate = value + step
            if dist[j] is None or candidate < dist[j]:
                dist[j] = candidate
                heappush(pending, (candidate, j))
    return dist


def construct(a, b, ordinary):
    """Return full vertex rows with the joint at zero, or None if impossible."""
    if a < 1 or b < 1 or ordinary < 0:
        raise ValueError("expected two positive populations and nonnegative ordinary leaves")
    t = a + b
    h = ordinary + 2
    k = t + h  # Assumed prime.
    j = -a * pow(t, -1, k) % k
    q = (j * h - a) // k
    dist = distances(k, (a, b, h))
    if dist[2 * t % k] < 2 * t:
        return None

    # Prefix counts are defined on all integers and rise by h after k steps.
    start = j - 1
    def prefix(i):
        offset = i - start
        return (dist[t * offset % k] + h * offset) // k

    holes = {i for i in range(k) if prefix(i) - prefix(i - 1)}
    left = {i for i in range(k) if prefix(i + j) - prefix(i) - q}
    right = set(range(k)) - holes - left
    rows = [(0, -1, j + 1), (1, -1, j)]
    for parent, values in ((0, left), (1, right), (-1, holes - {j, j + 1})):
        for v in sorted(values):
            rows.append((len(rows), parent, v))
    return rows

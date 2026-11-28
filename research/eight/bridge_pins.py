"""Find a short path between two fixed divisible-order cordial cores."""
from functools import lru_cache
from itertools import combinations


@lru_cache(None)
def profiles(k, total):
    low, extra = divmod(total, k)
    return [tuple(low + (x in high) for x in range(k))
            for high in combinations(range(k), extra)]


def path_row(k, start, end, vertices, edges):
    """Use the requested vertex and edge multisets, including both end edges."""
    free, weights = list(vertices), list(edges)
    row = []

    def visit(last, left):
        if not left:
            return weights[(last + end) % k] == 1
        for x in range(k):
            w = (last + x) % k
            if not free[x] or not weights[w]:
                continue
            free[x] -= 1
            weights[w] -= 1
            row.append(x)
            if visit(x, left - 1):
                return True
            row.pop()
            weights[w] += 1
            free[x] += 1
        return False

    return tuple(row) if visit(start, sum(free)) else None


@lru_cache(None)
def normalized(k, end, first_gap, second_gap, size):
    if k not in (8,9) or not 0 <= size <= k+2:
        raise ValueError("Expected modulus 8 or 9 and at most k+2 internal vertices")
    for vertices in profiles(k, size):
        moment = end + 2 * sum(x * vertices[x] for x in range(k))
        for final in profiles(k, size - 1):
            edges = list(final)
            edges[first_gap] += 1
            edges[second_gap] += 1
            if min(edges) < 0 or (sum(x * edges[x] for x in range(k)) - moment) % k:
                continue
            row = path_row(k, 0, end, vertices, edges)
            if row is not None:
                return row
    return None


def bridge(k, start, end, first_gap, second_gap, size):
    """Return the internal labels, or None if no such short bridge works."""
    gaps = sorted(((first_gap - 2 * start) % k, (second_gap - 2 * start) % k))
    row = normalized(k, (end - start) % k, *gaps, size)
    return None if row is None else tuple((start + x) % k for x in row)


def path_endpoints(k, order, end):
    """Find a short cordial path from zero to the requested endpoint."""
    for bins in profiles(k, order):
        interior = list(bins)
        interior[0] -= 1
        interior[end] -= 1
        if min(interior) < 0:
            continue
        moment = 2 * sum(x * bins[x] for x in range(k)) - end
        for edges in profiles(k, order - 1):
            if (sum(x * edges[x] for x in range(k)) - moment) % k:
                continue
            row = path_row(k, 0, end, interior, edges)
            if row is not None:
                return (0,) + row + (end,)
    return None

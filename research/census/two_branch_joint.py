"""A full modular block at a joint with at most two nonleaf neighbors at depth one."""

from math import gcd


def block(a, b, p, c, deficit):
    """Return (vertex, parent, label) for k free vertices; joint -1 has label c.

    Vertices 0,1 are its neighbors with a,b children. It has p other leaves.
    """
    k = a + b + p + 2
    if min(a, b, p) < 0 or not 0 <= c < k or not 0 <= deficit < k:
        raise ValueError("invalid populations, root label or deficit")
    if a < b:
        large, small = 1, 0
    else:
        large, small = 0, 1
    h = min(a, b)
    d = (deficit - 2 * c) % k
    sign = 1 if d == 0 or d >= k - d else -1
    x, y = 0, sign % k
    if h == 0 or d == 0 or (sign * d) % k >= h + 2:
        small_tips = {(d - j * sign) % k for j in range(1, h + 1)}
        large_tips = None
    else:
        s = k // 2
        assert k == 2 * s and d == s and a == b == s - 1 and p == 0
        y = s
        if s % 2:
            small_tips = {u + shift for u in range(1, (s + 1) // 2)
                          for shift in (0, s)}
            large_tips = None
        else:
            x = 1
            large_tips = {(s + 1 + j * (1 - s)) % k for j in range(s - 1)}
            small_tips = set(range(k)) - {x, y} - large_tips

    rest = sorted(set(range(k)) - {x, y} - small_tips)
    if large_tips is None:
        large_tips = rest[:max(a, b)]
    direct = set(rest) - set(large_tips)
    groups = {large: sorted(large_tips), small: sorted(small_tips)}
    centers = {large: x, small: y}
    rows = [(v, -1, centers[v]) for v in (0, 1)]
    for parent in (0, 1):
        for value in groups[parent]:
            rows.append((len(rows), parent, value))
    for value in sorted(direct):
        rows.append((len(rows), -1, value))
    return [(v, parent, (value + c) % k) for v, parent, value in rows]


def neutral(a, b):
    """With no ordinary root leaves, construct a uniform block or return None."""
    k = a + b + 2
    for center, children in enumerate((a, b)):
        length = gcd(k, children)
        if length <= 1:
            continue
        y = k // length
        tips = [i + j * y for i in range(1, children // length + 1)
                for j in range(length)]
        remaining = sorted(set(range(k)) - {0, y} - set(tips))
        groups = {center: tips, 1 - center: remaining}
        rows = [(v, -1, y if v == center else 0) for v in (0, 1)]
        for parent in (0, 1):
            for value in groups[parent]:
                rows.append((len(rows), parent, value))
        return rows
    return None

"""Integer witnesses for every tree with at most four leaves."""

from itertools import combinations
import json
from pathlib import Path

DATA = json.loads(Path(__file__).with_name("four-leaf-certificates.json").read_text())
NO_ONE = {(1, 1), (1, 4), (4, 4)}


def key(values):
    return ",".join(map(str, values))


def staircase(n):
    return [i // 2 for i in range(n)]


def reflect_path(row):
    n = len(row)
    return [(n + 1 - i % 2) // 2 - 1 - x for i, x in enumerate(row)]


def available(n, depth):
    return 0 <= depth < (n + 1) // 2 and (depth == 0 or n != 4 * depth + 1)


def endpoint(n, depth):
    """A path in order, starting at depth and ending at deficiency depth."""
    if not available(n, depth):
        raise ValueError((n, depth))
    if depth == 0:
        return staircase(n)
    last = (n - 1) // 2
    if depth > last - depth:
        return reflect_path(endpoint(n, last - depth))
    m = n // 2
    if n % 2:
        head = staircase(2 * depth + 1)[::-1]
        tail = endpoint(2 * (m - depth), depth)
        return head + [x + depth + i % 2 for i, x in enumerate(tail)]
    if m == 2 * depth + 1:
        head = staircase(2 * depth + 1)[::-1]
        tail = [2 * depth - i // 2 for i in range(2 * depth + 1)]
        return head + tail

    width = depth + 1
    count = m // width - 1
    block = staircase(2 * width)[::-1]
    head = [x + j * width for j in range(count) for x in block]
    shift = count * width
    return head + [x + shift for x in endpoint(2 * (m - shift), depth)]


def extend_tip(row, length, left=False):
    """Append a disjoint path block, preserving every old rank."""
    if not length:
        return row
    base = row[::-1] if left else row
    n = len(base)
    own = (n + 1) // 2  # Both tips are in a class of this size.
    tail = endpoint(length, own - 1 - base[-1])
    out = base + [x + (own if i % 2 else n - own) for i, x in enumerate(tail)]
    return out[::-1] if left else out


ZERO_SEEDS = {
    (1, 0): (1, 0, [0, 0]),
    (0, 1): (4, 1, [1, 2, 2, 0, 0, 1]),
    (1, 1): (5, 1, [1, 2, 3, 1, 0, 0, 2]),
    (0, 0): (6, 2, [1, 2, 4, 3, 2, 0, 0, 1, 3]),
}


def marked(a, b, depth):
    """Construct within-class ranks for two arms meeting at the given depth."""
    if a > b:
        return marked(b, a, depth)[::-1]
    if a == 0:
        return endpoint(b + 1, depth)
    if depth == 0:
        u, v, seed = ZERO_SEEDS[a % 2, b % 2]
        if a >= u + 2 * ((len(seed) + 1) // 2 - seed[0]):
            return extend_tip(extend_tip(seed, a - u, left=True), b - v)
        # Starting at the mark leaves only the longer arm to be appended.
        if available(b, a // 2):
            return extend_tip(staircase(a + 1)[::-1], b)
        return DATA["rank_zero"][key((a, b))]
    if a >= 4 * depth + 5:
        u, v = 2 * depth + a % 2, b % 2
        row = extend_tip(staircase(u + v + 1), a - u, left=True)
        return extend_tip(row, b - v)
    if b >= a + 4 * depth + 4:
        v = 2 * depth + b % 2
        return extend_tip(staircase(a + v + 1)[::-1], b - v)
    if depth == 1:
        return DATA["rank_one"][key((a, b))]
    raise ValueError("This finite higher-depth case is outside the construction")


def grow(parents, root, length):
    arm = []
    for _ in range(length):
        parents.append(root)
        root = len(parents) - 1
        arm.append(root)
    return arm


def fork(lengths):
    parents = [-1]
    return parents, [grow(parents, 0, length) for length in lengths]


def kernel(lengths, pin, depth):
    return DATA["kernels"][key((*lengths, pin, depth))]


def path_piece(left, center, right, depth):
    return left[::-1] + [center] + right, marked(len(left), len(right), depth)


def colors(parents):
    sides = [0]
    for p in parents[1:]:
        sides.append(1 - sides[p])
    return sides


def reflect(piece, sides):
    ids, row = piece
    width = [sum(sides[v] == c for v in ids) for c in (0, 1)]
    return ids, [width[sides[v]] - 1 - x for v, x in zip(ids, row)]


def assemble(sides, pieces):
    """Lay down two rows of ranks, sharing an extreme at an identified vertex."""
    widths = [0, 0]
    ranks = {}
    for vertices, row in pieces:
        shared = ranks.keys() & vertices
        if len(shared) > 1 or len(vertices) != len(row):
            raise ValueError("Invalid block")
        offsets = widths.copy()
        for v in shared:
            offsets[sides[v]] -= 1
        for v, x in zip(vertices, row):
            c = sides[v]
            rank = offsets[c] + x
            if v in shared:
                if ranks[v] != rank:
                    raise ValueError("Incompatible shared rank")
            else:
                ranks[v] = rank
                widths[c] += 1
    return [ranks[v] + sides[v] * widths[0] for v in range(len(sides))]


def spider(lengths):
    """Return (parents, integer labels), with arms in the input order."""
    if len(lengths) not in (3, 4) or min(lengths) < 1:
        raise ValueError("Expected three or four positive arm lengths")
    parents, arms = fork(lengths)
    sides = colors(parents)
    for i, j in combinations(range(len(arms)), 2):
        if lengths[i] == lengths[j] == 2:
            continue
        other = [arm for k, arm in enumerate(arms) if k not in (i, j)]
        if len(other) == 1:
            other.append([])
        if len(other[0]) == len(other[1]) == 2:
            continue
        left = path_piece(arms[i], 0, arms[j], 0)
        right = path_piece(other[0], 0, other[1], 0)
        return parents, assemble(sides, [reflect(left, sides), right])
    # Canonical certificate order is 2,2,2,t (or 2,2,2).
    arms.sort(key=lambda arm: len(arm) != 2)
    lengths = tuple(map(len, arms))
    ids = [0] + sum(arms, [])
    t = lengths[-1]
    if len(arms) == 4 and (t == 5 or available(t - 5, 2)):
        first = ids[:12], kernel((2, 2, 2, 5), 11, 2)
        pieces = [reflect(first, sides)]
        if t > 5:
            pieces.append((ids[12:], endpoint(t - 5, 2)))
        return parents, assemble(sides, pieces)
    labels = [0] * len(ids)
    for v, x in zip(ids, DATA["intervals"]["s:" + key(lengths)]):
        labels[v] = x
    return parents, labels


def double_fork(a, b, g, c, d):
    """Two degree-three vertices distance g apart with arms a,b and c,d."""
    if min(a, b, g, c, d) < 1:
        raise ValueError("Expected five positive lengths")
    parents, (left_a, left_b, link) = fork((a, b, g))
    v = link[-1]
    right_c, right_d = grow(parents, v, c), grow(parents, v, d)
    if (c, d) == (2, 2) and (a, b) != (2, 2):
        left_a, left_b, right_c, right_d = right_c, right_d, left_a, left_b
        link = ([0] + link)[::-1]
    else:
        link = [0] + link
    u, v = link[0], link[-1]
    sides = colors(parents)
    if len(right_c) > len(right_d):
        right_c, right_d = right_d, right_c
    c, d = len(right_c), len(right_d)
    left = path_piece(left_a, u, left_b, 1 if len(left_a) == len(left_b) == 2 else 0)
    if len(left_a) != 2 or len(left_b) != 2:
        right = path_piece(right_c, v, right_d, 0)
        mid = [(link[1:-1], endpoint(g - 1, 0))] if g > 1 else []
        return parents, assemble(sides, [reflect(left, sides)] + mid + [right])

    prefix = [u] + left_a + left_b
    case = "d:" + key((c, d, g))
    if case in DATA["intervals"]:
        output = [0] * len(parents)
        for vertex, x in zip(prefix + link[1:] + right_c + right_d, DATA["intervals"][case]):
            output[vertex] = x
        return parents, output
    if (c, d) in NO_ONE:
        right = [v] + right_c + right_d + [link[-2]], kernel((c, d, 1), c + d + 1, 1)
        link = link[:-1]
    else:
        right = path_piece(right_c, v, right_d, 1)
    distance = len(link) - 1
    if distance == 3:
        if c <= 2:
            first = prefix + link[1:] + right_c, kernel((2, 2, 3 + c), 7, 0)
            pieces = [reflect(first, sides), (right_d, endpoint(d, 0))]
        else:
            if not (available(c, 1) and available(d, 2)):
                right_c, right_d, c, d = right_d, right_c, d, c
            middle = prefix + link[1:], kernel((2, 2, 3), 7, 1)
            pieces = [(right_c[::-1], endpoint(c, 1)), middle, (right_d, endpoint(d, 2))]
    elif distance in (2, 6):
        j = distance - 1
        first = prefix + link[1:-1], kernel((2, 2, j), 4 + j, 1)
        pieces = [reflect(first, sides), right]
    else:
        pieces = [reflect(left, sides)]
        if distance > 1:
            pieces.append((link[1:-1], endpoint(distance - 1, 1)))
        pieces.append(right)
    return parents, assemble(sides, pieces)

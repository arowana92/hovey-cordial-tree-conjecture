"""Execute the two dyadic rectangle constructions on ordinary labeled trees."""

from collections import defaultdict
from random import Random
from research.large_order_check import balanced_target, histograms, moment
from research.large_order_dyadic import terms


def run(k, leaves, seed):
    rng = Random(seed)
    powers = [1 << j for j in range((2*k).bit_length()+2)]
    lab, parents = [0], [-1]
    inventory = defaultdict(list)
    def vertex(p, x):
        parents.append(p)
        lab.append(x % k)
        return len(lab)-1

    def triple(p, x, q):
        apex = vertex(vertex(0, p), x)
        vertex(apex, q)
        return apex

    reserve = 6
    for s in powers:
        for x in range(k):
            for t in powers:
                for sign in (-1, 1):
                    for z in (0, 1):
                        for kind in ('vertex', 'edge'):
                            if leaves:
                                p = -x+z if kind == 'edge' else x+z
                                q = p+t if kind == 'edge' else p-t
                                u, v = vertex(0, p), vertex(0, q)
                            for _ in range(reserve):
                                if leaves:
                                    a, b = (x+s, x+t) if sign == 1 else (x, x+s+t)
                                    if kind == 'edge':
                                        a, b = a-p, b-q
                                    i, j = vertex(u, a), vertex(v, b)
                                elif kind == 'vertex':
                                    a, b = (x+s, x+t) if sign == 1 else (x, x+s+t)
                                    i = triple(x+z, a, x+z)
                                    j = triple(x+z-t, b, x+z-t)
                                else:
                                    a, p = -x+z, 2*x-z
                                    i = triple(p, a+(s if sign == 1 else 0), p)
                                    j = triple(p, a+(0 if sign == 1 else s), p+t)
                                if not z:
                                    inventory[kind, s, t, x, sign].append((i, j, -sign*s))
    uniform = histograms(parents, lab, k)
    assert max(uniform[0])-min(uniform[0]) == 1 and len(set(uniform[1])) == 1
    # Every construction was balanced before adjoining this unbalanced part.
    at = 0
    for _ in range(2*k+3):
        at = vertex(at if rng.randrange(3) else 0, rng.randrange(k))
    middle = vertex(at, rng.randrange(k))
    at = vertex(middle, rng.randrange(k))
    v, e = histograms(parents, lab, k)
    n = len(lab)
    vt, et = balanced_target(n, k), balanced_target(n-1, k)
    if leaves:
        if n % k:
            vt = balanced_target(n, k, moment(v)+moment(et)-moment(e))
        else:
            et = balanced_target(n-1, k, moment(e)+moment(vt)-moment(v))
        change = moment(vt)-moment(v)
    else:
        a, b = moment(vt)-moment(v), moment(et)-moment(e)
        lab[middle] = (lab[middle]+b-a) % k
        change = 2*a-b
    lab[at] = (lab[at]+change) % k
    v, e = histograms(parents, lab, k)
    def rectangles(kind, diff):
        used = 0
        for s, t, w in terms(diff):
            for x, val in enumerate(w):
                sign = 1 if val > 0 else -1
                for _ in range(abs(val)):
                    i, j, d = inventory[kind, s, t, x, sign].pop()
                    lab[i], lab[j] = (lab[i]+d) % k, (lab[j]-d) % k
                    used += 1
        return used
    diff = [y-x for x, y in zip(v, vt)]
    used = rectangles('vertex', diff)
    v, e = histograms(parents, lab, k)
    assert v == vt
    used += rectangles('edge', [y-x for x, y in zip(e, et)])
    assert histograms(parents, lab, k) == (vt, et)
    return n, used


if __name__ == '__main__':
    for k in (5, 6, 8, 9, 10, 13):
        print(k, 'leaf pairs', run(k, True, 25), 'degree-two pairs', run(k, False, 61))

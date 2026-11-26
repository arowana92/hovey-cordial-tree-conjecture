"""Integer decompositions into cyclic differences at powers of two."""

from collections import defaultdict
from itertools import product
from random import Random


def add(out, i, amount):
    out[i] = out.get(i, 0)+amount


def moment_adjust(vector, indices, value):
    """Change the ordinary first moment in local parity coordinates."""
    if not value:
        return
    sign = 1 if value > 0 else -1
    size = len(indices)
    r = size//2
    cap = r*(size-r)
    assert cap
    turns, remaining = divmod(abs(value), cap)
    for j in range(r):
        vector[indices[j]] -= sign*turns
        vector[indices[size-r+j]] += sign*turns
    for j in reversed(range(r)):
        step = min(remaining, size-r)
        vector[indices[j]] -= sign
        vector[indices[j+step]] += sign
        remaining -= step
    assert not remaining


def decompose(data, constrained):
    k = len(data)
    assert sum(data) == 0
    f = list(data)
    if constrained:
        moment = sum(j*a for j, a in enumerate(data))
        assert moment % k == 0
        q, rem = divmod(-moment//k, k)
        tail = [q+(i < rem) for i in range(k)]
        f = [x-y for x, y in zip(f, tail)]+tail
    result = defaultdict(dict)

    def visit(arr, origin, stride):
        m = len(arr)
        if not any(arr):
            return
        if m <= 2:
            assert not constrained and m == 2 and arr[0] == -arr[1]
            add(result[stride], origin % k, -arr[0])
            return
        h = [0]*m
        # Use the same floor offset for both parity totals when moment is free.
        for parity in (0, 1):
            prefix = 0
            for i in range(parity, m, 2):
                before = prefix//2
                prefix -= arr[i]
                h[i] = prefix//2-before
        def residual():
            return [a+b-c for a, b, c in zip(arr+[0], h+[0], [0]+h)]
        if constrained:
            g = residual()[::2]
            amt = -sum(j*x for j, x in enumerate(g))
            moment_adjust(h, list(range(0, m, 2)), amt)
            assert sum(h) == 0
        g = residual()
        for j, x in enumerate(h):
            add(result[stride], (origin+j*stride) % k, x)
        for parity in (0, 1):
            sub = g[parity::2]
            assert sum(sub) == 0
            if constrained:
                assert sum(i*x for i, x in enumerate(sub)) == 0
            visit(sub, origin+parity*stride, 2*stride)

    visit(f, 0, 1)
    return {s: [table.get(i, 0) for i in range(k)] for s, table in result.items()}


def difference(v, step):
    return [v[(i-step) % len(v)]-x for i, x in enumerate(v)]


def terms(data):
    for s, h in decompose(data, True).items():
        for t, v in decompose(h, False).items():
            yield s, t, v


def verify():
    rng = Random(823)
    checks = maximum = 0
    for k in range(2, 78):
        for _ in range(12):
            # Mix positive and negative rectangle counts, including wraparound.
            f = [0]*k
            for _ in range(4*k):
                i, a, b = (rng.randrange(k) for _ in range(3))
                f[i] += 1
                f[(i+a+b) % k] += 1
                f[(i+a) % k] -= 1
                f[(i+b) % k] -= 1
            direct = [0]*k
            for s, t, w in terms(f):
                for j, x in enumerate(difference(difference(w, t), s)):
                    direct[j] += x
                maximum = max(maximum, max(map(abs, w)))
            assert direct == f
            checks += 1
    exhaustive = 0
    for k in range(2, 10):
        for f in product((-1, 0, 1), repeat=k):
            if sum(f) or sum(j*x for j, x in enumerate(f)) % k:
                continue
            rebuilt = [0]*k
            for s, t, w in terms(f):
                for j, x in enumerate(difference(difference(w, t), s)):
                    rebuilt[j] += x
            assert tuple(rebuilt) == f
            exhaustive += 1
    print(f"{exhaustive} exhaustive small moment-zero vectors")
    print(f"{checks} complete integer decompositions; maximum coefficient {maximum}")


if __name__ == '__main__':
    verify()

"""Construct translated local repairs and verify both full histograms."""

from collections import defaultdict
from itertools import accumulate, chain
from random import Random

from research.large_order_check import balanced_target, changes, histograms, moment

CAPACITY = 32


def fill_list(vertices, lab, k):
    n = len(vertices)
    for x in range(k):
        for i in range(x*n//k, (x+1)*n//k):
            lab[vertices[i]] = x


def split(f, r, part):
    prev = 0
    out = []
    for total in accumulate(f):
        rounded = (total+part)//r
        out.append(rounded-prev)
        prev = rounded
    return out


def chunks(left, right, base):
    count = min(map(len, chain(left, right)))//CAPACITY
    for j in range(count):
        s = slice(j*CAPACITY, (j+1)*CAPACITY)
        yield base, [b[s] for b in left], [b[s] for b in right]


def forest_partition(variable, parents, internal):
    edges, nbrs = [], defaultdict(list)
    loops = 0
    for v in internal:
        if v == 0:
            continue
        i, j = variable[v], variable[parents[v]]
        if i == j:
            loops += 1
            continue
        edge = len(edges)
        edges.append((i, j))
        nbrs[i].append(edge)
        nbrs[j].append(edge)
    assert loops <= 1
    degree = {i: len(n) for i, n in nbrs.items()}
    done = set()
    ready = [i for i, d in degree.items() if d <= 3]
    forests = [[], [], []]
    for i in ready:
        if i in done:
            continue
        done.add(i)
        later = []
        for e in nbrs[i]:
            a, b = edges[e]
            j = a if b == i else b
            if j not in done:
                later.append((i, j))
                degree[j] -= 1
                if degree[j] == 3:
                    ready.append(j)
        assert len(later) <= 3
        for forest, edge in zip(forests, later):
            forest.append(edge)
    assert len(done) == len(nbrs) and sum(map(len, forests)) == len(edges)
    for forest in forests:
        leader = {}
        def find(i):
            while i in leader:
                i = leader[i]
            return i
        for i, j in forest:
            x, y = find(i), find(j)
            assert x != y
            leader[x] = y


def leaf_setup(parents, k, rng):
    n = len(parents)
    internal = set(parents[1:])
    leaves = defaultdict(list)
    side = [0]*n
    for v in range(1, n):
        side[v] = 1-side[parents[v]]
        if v not in internal:
            leaves[parents[v]].append(v)
    ordered = sorted(leaves, key=lambda i: -len(leaves[i]))
    pairs = [ordered[:2]]
    for color in [0, 1]:
        group = [i for i in ordered[2:] if side[i] == color]
        pairs.extend(zip(group[::2], group[1::2]))
    lab = [None]*n
    variable = {v: v for v in internal}
    pools = [[[] for _ in range(k)] for _ in range(2)]
    for i, j in pairs:
        variable[j] = i
        x = rng.randrange(k)
        lab[i], lab[j] = x, (x+1) % k
        count = min(len(leaves[i]), len(leaves[j]))
        for pool, v in zip(pools, (i, j)):
            pool[x].extend(leaves[v][:count])
            leaves[v] = leaves[v][count:]
    forest_partition(variable, parents, internal)
    for v in internal:
        if lab[v] is None:
            lab[v] = rng.randrange(k)
    extra = [[] for _ in range(k)]
    for v, rest in leaves.items():
        extra[lab[v]].extend(rest)
    for bucket in extra:
        fill_list(bucket, lab, k)
    groups = []
    for j in range(k):
        by_type = []
        for pool in pools:
            fill_list(pool[j], lab, k)
            bins = [[] for _ in range(k)]
            for v in pool[j]:
                bins[lab[v]].append(v)
            by_type.append(bins)
        groups.extend(chunks(*by_type, j))
    return lab, groups


def triple_setup(parents, k, rng):
    n = len(parents)
    adj = [[] for _ in parents]
    for v in range(1, n):
        p = parents[v]
        adj[p].append(v)
        adj[v].append(p)
    fan = [i for i in adj[0] if len(adj[i]) == 1]
    blocks = []
    # Zero is the fan center in these fixtures. Stop at it even if it has degree two.
    for start, near in enumerate(adj):
        if start and len(near) == 2:
            continue
        for v in near:
            path, prev = [], start
            while v and len(adj[v]) == 2:
                path.append(v)
                i, j = adj[v]
                prev, v = v, (j if i == prev else i)
            if v > start:
                blocks.extend(path[i:i+5] for i in range(0, len(path)-4, 5))
    lab = [rng.randrange(k) for _ in parents]
    lab[0] = 0
    fill_list(fan, lab, k)
    by_base = [[[[] for _ in range(k)] for _ in range(2)] for _ in range(k)]
    buffers, planted = set(), set()
    for batch in range(len(blocks)//(2*k*k)):
        for j in range(k):
            for t in range(2):
                for x in range(k):
                    a, b, v, c, e = blocks[(2*k*batch+2*j+t)*k+x]
                    lab[b], lab[v], lab[c] = j, x, (j+t) % k
                    by_base[j][t][x].append(v)
                    buffers.update([a, e])
                    planted.update([b, v, c])
    assert buffers.isdisjoint(planted)
    cut = [w for v in planted for w in adj[v] if w not in planted]
    assert set(cut) == buffers and len(cut) == len(buffers)
    groups = list(chain.from_iterable(chunks(*ts, j) for j, ts in enumerate(by_base)))
    return lab, groups, fan[0]


def apply(parents, k, d, lab, groups, leaf=None):
    v, e = histograms(parents, lab, k)
    vt, et = balanced_target(len(lab), k), balanced_target(len(lab)-1, k)
    old = moment(e)-d*moment(v)
    if d == 2:
        lab[leaf] = (lab[leaf]+old-moment(et)+2*moment(vt)) % k
        v, e = histograms(parents, lab, k)
    elif len(lab) % k:
        vt = balanced_target(len(lab), k, moment(et)-old)
    else:
        et = balanced_target(len(lab)-1, k, old+moment(vt))
    a = [x-y for x, y in zip(vt, v)]
    z = [x-y for x, y in zip(et, e)]
    r = len(groups)
    assert r > 0
    for i, (j, _, _) in enumerate(groups):
        part = split(a, r, i)
        for x in range(k):
            z[(x+j) % k] -= d*part[x]
    _, h = changes([0]*k, z, 1)
    moves = []
    for i, (j, left, right) in enumerate(groups):
        part, hpart = split(a, r, i), split(h, r, i)
        at_right = [hpart[(x+j) % k] for x in range(k)]
        at_left = [x-y for x, y in zip(part, at_right)]
        for supply, net in [(left, at_left), (right, at_right)]:
            dst = iter(x for x, amount in enumerate(net) for _ in range(max(0, amount)))
            for x, amount in enumerate(net):
                if -amount > len(supply[x]):
                    return None
                for vertex in supply[x][:max(0, -amount)]:
                    moves.append((vertex, next(dst)))
            assert next(dst, None) is None
    for v, x in moves:
        lab[v] = x
    assert (vt, et) == histograms(parents, lab, k)
    assert max(vt)-min(vt) <= 1 and max(et)-min(et) <= 1
    return r, len(moves)


def main():
    rng = Random(1991)
    counts = []
    for k in [2, 3, 5, 8, 12]:
        for d in [1, 2]:
            if d == 1:
                spine = 400
                parents = [-1]+list(range(spine-1))+[i % spine for i in range(60000+k)]
                parents += [0]*15000
            else:
                parents = [-1]+list(range(130000))+[0]*12000
            for _ in range(30):
                if d == 1:
                    lab, g = leaf_setup(parents, k, rng)
                    result = apply(parents, k, d, lab, g)
                else:
                    lab, g, v = triple_setup(parents, k, rng)
                    result = apply(parents, k, d, lab, g, v)
                if result is not None:
                    counts.append((k, d, *result))
                    break
            else:
                raise RuntimeError("insufficient supply on fixture")
    for k in range(2, 30):
        f = [rng.randrange(-60, 61) for _ in range(k-1)]
        f.append(-sum(f))
        for r in [2, 7, 16]:
            parts = [split(f, r, i) for i in range(r)]
            assert list(map(sum, zip(*parts))) == f
            for p in parts:
                assert sum(p) == 0
                for i in range(k):
                    diff = 0
                    for size in range(1, k+1):
                        j = (i+size-1) % k
                        diff += r*p[j]-f[j]
                        assert abs(diff) < r
    print("Full tree checks (modulus, site degree, groups, relabeled sites):", counts)


if __name__ == "__main__":
    main()

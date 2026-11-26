"""Construct and independently audit local histogram repairs on ordinary trees."""

from itertools import accumulate
from random import Random


def moment(a):
    return sum(i*v for i, v in enumerate(a))


def balanced_target(n, k, wanted=None):
    q, r = divmod(n, k)
    counts = [q]*k
    picks = list(range(r))
    if wanted is not None:
        delta = (wanted-moment(counts)-sum(picks)) % k
        for i in reversed(range(r)):
            step = min(delta, k-r)
            picks[i] += step
            delta -= step
        if delta:
            raise ValueError("unattainable moment at a uniform target")
    for i in picks:
        counts[i] += 1
    return counts


def changes(a, b, degree):
    k = len(a)
    prefix = list(accumulate(y-degree*x for x, y in zip(a, b)))
    if sum(a) or sum(b) or sum(prefix) % k:
        raise ValueError("incompatible totals or moment")
    average = sum(prefix)//k
    at_one = [average-v for v in prefix]
    at_zero = [x-y for x, y in zip(a, at_one)]
    return at_zero, at_one


def histograms(parents, labels, k):
    vertices, edges = [0]*k, [0]*k
    for i, x in enumerate(labels):
        vertices[x] += 1
        if i:
            edges[(x+labels[parents[i]]) % k] += 1
    return vertices, edges


def make_sites(parents, degree):
    neighbors = [[] for _ in parents]
    for i, p in enumerate(parents[1:], 1):
        neighbors[i].append(p)
        neighbors[p].append(i)
    leaves = [v for v, adj in enumerate(neighbors) if len(adj) == 1]
    if degree == 1:
        return leaves[0], [(v, neighbors[v]) for v in leaves]
    sites = []
    for start, adj in enumerate(neighbors):
        if len(adj) == 2:
            continue
        for v in adj:
            if len(neighbors[v]) != 2:
                continue
            run, previous = [], start
            while len(neighbors[v]) == 2:
                run.append(v)
                x, y = neighbors[v]
                previous, v = v, (y if x == previous else x)
            if v > start:
                for j in range(1, len(run)-1, 3):
                    sites.append((run[j], neighbors[run[j]]))
    return leaves[0], sites


def repair(parents, k, degree, rng):
    n = len(parents)
    leaf, sites = make_sites(parents, degree)
    for attempt in range(1, 65):
        lab = [rng.randrange(k) for _ in parents]
        vert, edge = histograms(parents, lab, k)
        vtarget, etarget = balanced_target(n, k), balanced_target(n-1, k)
        old = moment(edge)-degree*moment(vert)
        if degree == 2:
            delta = (old-moment(etarget)+2*moment(vtarget)) % k
            lab[leaf] = (lab[leaf]+delta) % k
            vert, edge = histograms(parents, lab, k)
        elif n % k:
            vtarget = balanced_target(n, k, moment(etarget)-old)
        else:
            etarget = balanced_target(n-1, k, old+moment(vtarget))
        nets = changes([a-b for a, b in zip(vtarget, vert)],
                       [a-b for a, b in zip(etarget, edge)], degree)
        supply = [[[] for _ in range(k)] for _ in nets]
        for v, adj in sites:
            # The actual neighbor values classify the sites, even if neighbors coincide
            # across different sites. Nonnegative labels let sums 0 and 1 specify type.
            kind = sum(lab[w] for w in adj)
            if kind < 2:
                supply[kind][lab[v]].append(v)
        if any(len(bucket) < -amount for buckets, net in zip(supply, nets)
               for bucket, amount in zip(buckets, net)):
            continue
        changed = 0
        for buckets, net in zip(supply, nets):
            dest = iter(v for v, amount in enumerate(net) for _ in range(max(0, amount)))
            for i, amount in enumerate(net):
                for v in buckets[i][:max(0, -amount)]:
                    lab[v] = next(dest)
                    changed += 1
            assert next(dest, None) is None
        got_v, got_e = histograms(parents, lab, k)
        assert got_v == vtarget and got_e == etarget
        assert max(got_v)-min(got_v) <= 1 and max(got_e)-min(got_e) <= 1
        return attempt, changed
    raise RuntimeError("fixture exhausted its attempts below the asymptotic bound")


def main():
    rng = Random(1991)
    vectors = targets = 0
    for k in range(2, 65):
        for n in range(k, 2*k):
            for wanted in (range(k) if n % k else [None]):
                target = balanced_target(n, k, wanted)
                assert sum(target) == n and max(target)-min(target) <= 1
                assert wanted is None or moment(target) % k == wanted
                targets += 1
        for d in [1, 2]:
            for _ in range(20):
                a, h = [[rng.randrange(-100, 101) for _ in range(k-1)] for _ in range(2)]
                a.append(-sum(a))
                h.append(-sum(h))
                b = [d*x+h[i-1]-h[i] for i, x in enumerate(a)]
                left, right = changes(a, b, d)
                assert all(left[i]+right[i] == x for i, x in enumerate(a))
                assert [d*x+(d-1)*right[i]+right[i-1] for i, x in enumerate(left)] == b
                vectors += 1
    fixtures = []
    for k in [2, 3, 5, 8, 12]:
        spine = 700
        parents = [-1]+list(range(spine-1))+[i % spine for i in range(60000+k)]
        fixtures.append((k, 1, *repair(parents, k, 1, rng)))
        # Test the uniform-vertex residue case as well.
        parents = parents[:len(parents)//k*k]
        fixtures.append((k, 1, *repair(parents, k, 1, rng)))
    for k in [2, 3, 4, 5]:
        parents = [-1]+list(range(120000))+[0]*8000
        fixtures.append((k, 2, *repair(parents, k, 2, rng)))
    # Direct fan construction: choose zero as a high bin whenever one is required.
    for k in range(2, 31):
        for r in range(k):
            n = k*(k+1)+r
            parents = [-1]+list(range(k-1))+[0]*(n-k)
            target = balanced_target(n, k)
            lab = [0]*k + [a for a, h in enumerate(target)
                           for _ in range(h-(k if a == 0 else 0))]
            v, e = histograms(parents, lab, k)
            assert v == target and max(e)-min(e) <= 1
    print("Prescribed targets:", targets, "integer repairs:", vectors)
    print("Actual tree repairs (modulus, degree, attempts, relabeled sites):", fixtures)


if __name__ == "__main__":
    main()

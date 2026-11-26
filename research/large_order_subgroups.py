"""Check subgroup padding and all target remainders on small ordinary trees."""

from random import Random
from research.large_order_check import histograms


def padded_witness(tree, m, rng):
    parents = tree+[0]*(-len(tree) % m)
    n = len(parents)
    v = [0]*m
    e = [0]*m
    v[0] = 1
    labels = [0]*n
    order = list(range(m))
    rng.shuffle(order)
    def extend(i):
        if i == n:
            return max(e)-min(e) <= 1
        for x in order:
            w = (labels[parents[i]]+x) % m
            if v[x] >= n//m or e[w] >= n//m:
                continue
            labels[i] = x
            v[x] += 1
            e[w] += 1
            if extend(i+1):
                return True
            v[x] -= 1
            e[w] -= 1
        return False
    assert extend(1)
    return labels[:len(tree)]


def check(tree, m, k, root_labels):
    labels = [x*(k//m) for x in root_labels]
    v, e = histograms(tree, labels, k)
    x, = (i for i in range(k) if v[i] != e[i])
    assert v[x] == e[x]+1
    base = k*((len(tree)+m-1)//m)
    for extra in range(base, base+k):
        q, r = divmod(len(tree)+extra, k)
        target = [q]*k
        for i in range(r):
            target[(x+i) % k] += 1
        fill = [i for i in range(k) for _ in range(target[i]-v[i])]
        assert len(fill) == extra
        vv, ee = histograms(tree+[0]*extra, labels+fill, k)
        assert vv == target and max(ee)-min(ee) <= 1


if __name__ == '__main__':
    rng = Random(86)
    cases = 0
    for m in (1, 2, 3, 4, 5, 6):
        for n in range(1, 10):
            for _ in range(4):
                tree = [-1]+[rng.randrange(i) for i in range(1, n)]
                labels = padded_witness(tree, m, rng)
                for factor in (2, 3, 5):
                    k = m*factor
                    check(tree, m, k, labels)
                    cases += k
    print(f"{cases} padded, restricted and extended tree labelings")

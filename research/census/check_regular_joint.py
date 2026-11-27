"""Rebuild the tree and count ordinary endpoint sums, including the shared vertex."""

from collections import Counter
from itertools import combinations_with_replacement
from random import Random

from research.census.regular_joint import extend, prefix, seeds
from research.census.check_two_branch_joint import brute
from research.large_order_hall_pools import hall_pair


def check_prefix(m, q, e, p, size):
    branch, direct = prefix(m, q, e, p, size)
    assert len(branch) == m and len(direct) <= p
    assert all(len(xs) <= cap for (_, xs), cap in zip(branch, [e] + [q]*(m-1)))
    vertices, edges = direct.copy(), direct.copy()
    for v, xs in branch:
        vertices.extend([v, *xs])
        edges.extend([v, *(v+x for x in xs)])
    interval = list(range(min(vertices), min(vertices) + size))
    assert sorted(vertices) == sorted(edges) == interval
    if size == m + e + (m-1)*q + p:
        assert any(v == 0 and len(xs) for v, xs in branch)


def check_attachment(m, q, e, p, k, c, d):
    label = extend(m, q, e, p, k, c, d)
    # Build the shared vertex and its level sets in the original order.
    n = len(label)-1
    assert label[0] == c and n == m + e + (m-1)*q + p
    edges = [(0,i) for i in range(1,m+1)]
    next_vertex = m+1
    for v in range(1,m+1):
        count = e if v == 1 else q
        edges.extend((v,i) for i in range(next_vertex,next_vertex+count))
        next_vertex += count
    edges.extend((0,i) for i in range(next_vertex,n+1))
    assert len(edges) == n and all(0 <= x < k for x in label)
    vertices = Counter(label[1:])
    weights = Counter((label[a]+label[b]) % k for a,b in edges)
    end_v = [2 + vertices[i] for i in range(k)]
    end_e = [2 - (i == d) + weights[i] for i in range(k)]
    assert max(end_v)-min(end_v) <= 1 and max(end_e)-min(end_e) <= 1


def hall_checks():
    rng = Random(1991)
    count = 0
    def check(values):
        k = len(values)
        pairs = hall_pair(values)
        assert sorted(a for a,_ in pairs) == sorted(b for _,b in pairs) == list(range(k))
        assert [x % k for x in values] == [(a+b) % k for a,b in pairs]
        assert pairs[0][0] == 0
    for k in range(1,11):
        for request in combinations_with_replacement(range(k), k):
            if sum(request) % k == 0:
                seq = list(request)
                rng.shuffle(seq)
                check(seq)
                count += 1
    for k in range(11,513):
        seq = [rng.randrange(-2*k,3*k) for _ in range(k-1)]
        seq.append(-sum(seq))
        check(seq)
    return count


def main():
    frame = seeds()[8]["tips"]
    speed = lambda x: (x >= 4) - (x <= -4)
    for p,x in zip((-5,-4,-3,0,1,2,4,5),frame):
        assert speed(p)+speed(x)==speed(p+x)
    tested = lifts = 0
    for m in range(3,49):
        for q in (1,2,3,4,5):
            for e in sorted({1, q, 7}):
                n = m + (m-1)*q + e + 2
                for size in range(m,n+1):
                    check_prefix(m,q,e,2,size)
                    tested += 1
    rng = Random(1952)
    for m in range(3,41):
        for q in range(1,6):
            for e in sorted({1,q,7}):
                for p in (0,3):
                    n = m+(m-1)*q+e+p
                    ks = {1,2,m-1,m,m+1,n-1,n,n+1,2*n+3,rng.randrange(1,2*n)}
                    for k in sorted(ks):
                        c,d = rng.randrange(k),rng.randrange(k)
                        check_attachment(m,q,e,p,k,c,d)
                        lifts += 1
    # Enumerate labels of both centers and subsets of actual child labels.
    for q in range(1,6):
        assert brute(q,q) == (q % 2 == 0)
    count = hall_checks()
    print(f"{tested} integer prefixes, {lifts} prescribed core extensions, "
          f"5 exhaustive two-center comparisons.")
    print(f"{count} zero-sum request multisets through modulus 10 and "
          "502 larger Hall exchanges through modulus 512.")


if __name__ == "__main__":
    main()

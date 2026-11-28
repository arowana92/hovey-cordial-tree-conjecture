"""Parse every unicyclic graph and verify every prescribed difference on every vertex pair."""
import argparse
from collections import Counter
from pathlib import Path

from .branched_rings import canonical, children
from .count_few_leaf_rings import count_by_cycle


K = 27
RESIDUES = set(range(K))
UNITS = tuple(a for a in RESIDUES if a % 3)
ORBITS = [sum(1 << x for x in {a*d % K for a in UNITS}) for d in range(K)]


def parse(key):
    sites = tuple(key.split('.'))
    c = len(sites)
    assert 3 <= c <= K and canonical(sites) == sites
    edges = [(v, (v+1) % c) for v in range(c)]
    def visit(word, v):
        branches = children(word)
        assert tuple(sorted(branches)) == branches and '(' + ''.join(branches) + ')' == word
        for branch in branches:
            w = len(edges)
            edges.append((v, w))
            visit(branch, w)
    for i, word in enumerate(sites):
        visit(word, i)
    assert len(edges) == K
    return c, edges


def hist(labels, edges, modulus):
    return (Counter(labels),
            Counter((labels[i]+labels[j]) % modulus for i, j in edges))


def check_transfer(f, edges, u, v, w, d, small_order=None):
    a, b = 0, 1
    if small_order is None:
        # Two adjacent hubs in a 55-vertex cordial tree.
        base = [0, d, *sorted(RESIDUES-{d}), *range(K)]
        first = [(a, i) for i in range(2, K+1)]
        second = [(b, i) for i in range(K+1, len(base))]
    else:
        # Move the leaf -d to b. Its new weight zero is free on the original star.
        other = sorted(RESIDUES-{0,d,(-d) % K})
        base = [0,d,(-d) % K,*other[:small_order-3]]
        first = [(a,i) for i in range(3,len(base))]
        second = [(b,2)]
    base_edges = [(a,b)] + first + second
    start = len(base)
    unit = next(t for t in UNITS if t*(f[w]-f[v]) % K == d)
    labels = base + [unit*(x-f[v]) % K for x in f]
    assert labels[start+v] == base[a] and labels[start+w] == base[b]
    actual = [(a, start+u), (b, start+v)]
    for i, (x,y) in enumerate(first+second):
        port = v if x == a else w
        actual.append((start+port if i % 3 or y == 2 else x, y))
    actual.extend((start+i, start+j) for i,j in edges if {i,j} != {u,v})
    old = hist(base, base_edges, K)
    assert all(max(h[i] for i in RESIDUES)-min(h[i] for i in RESIDUES) <= 1 for h in old)
    assert hist(labels, actual, K) == tuple(h+Counter(RESIDUES) for h in old)
    assert len(actual) == len(labels)-1
    seen = {0}
    while True:
        reach = seen | {w for i,j in actual if i in seen or j in seen for w in (i,j)}
        if seen == reach:
            break
        seen = reach
    assert len(seen) == len(labels)


def check_cover(f, edges, c):
    # Rotate the sheet numbering at the closing edge to make a connected cover.
    for d in (3,5):
        for target in range(d):
            shifts = [v*v % d for v in range(K)]
            shifts[1] = target
            labels = [x+K*((i+shifts[v]) % d) for i in range(d) for v,x in enumerate(f)]
            lifted = [(K*i+u, K*((i+int(u==c-1 and v==0)) % d)+v)
                      for i in range(d) for u,v in edges]
            assert labels[1]-labels[0] == f[1]-f[0]+K*target
            assert hist(labels, lifted, d*K) == (Counter(range(d*K)),)*2


def verify(path, tips):
    assert ORBITS[1] | ORBITS[3] | ORBITS[9] == (1<<K)-2
    expected = Counter(dict(count_by_cycle(K, tips)))
    found = Counter()
    seen = set()
    rows = marks = transfers = short = 0
    with path.open() as source:
        for line in source:
            key, *words = line.split()
            assert key not in seen and words
            seen.add(key)
            c, edges = parse(key)
            degree = Counter(v for edge in edges for v in edge)
            assert sum(x == 1 for x in degree.values()) == tips
            # Track vertices reachable from each mark for the three unit orbits.
            full = (1<<K)-1
            coverage = [[0]*K for _ in (1,3,9)]
            probes = {}
            if found[c] == 0:
                for u,v in edges[:c]:
                    other = (u+2) % K
                    if other == v:
                        other = (other+1) % K
                    for w in {u,other}:
                        probes[u,v,w] = 0
            first = found[c] == 0
            for word in words:
                f = [ord(z)-65 for z in word]
                assert len(f) == K and set(f) == RESIDUES
                assert {(f[i]+f[j]) % K for i,j in edges} == RESIDUES
                group3,group9 = [0]*3,[0]*9
                for i,x in enumerate(f):
                    group3[x%3] |= 1<<i
                    group9[x%9] |= 1<<i
                for i,x in enumerate(f):
                    same3, same9 = group3[x%3], group9[x%9]
                    coverage[0][i] |= full ^ same3
                    coverage[1][i] |= same3 ^ same9
                    coverage[2][i] |= same9 ^ (1<<i)
                if first:
                    for (u,v,w), old in probes.items():
                        orbit = ORBITS[(f[w]-f[v]) % K]
                        fresh = orbit & ~old
                        while fresh:
                            bit = fresh & -fresh
                            d = bit.bit_length()-1
                            check_transfer(f, edges, u, v, w, d)
                            if len(seen) == 1 and (u,v) == edges[0] and w != u:
                                for size in (26,27):
                                    check_transfer(f, edges, u, v, w, d, size)
                                    short += 1
                            transfers += 1
                            fresh ^= bit
                        probes[u,v,w] |= orbit
            assert all(mask == full ^ (1<<i) for row in coverage for i,mask in enumerate(row))
            assert all(mask == full-1 for mask in probes.values())
            if first:
                check_cover(f, edges, c)
            found[c] += 1
            rows += len(words)
            marks += K*(K-1)//2
    assert all(found[c] == expected[c] for c in range(3,K+1))
    print(tips, 'leaves, graphs', len(seen), 'rows', rows, 'marked differences', (K-1)*marks,
          'whole trees', transfers, 'order 53 or 54', short)


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('tips', type=int, choices=(0,2,3))
    cli.add_argument('stream', type=Path)
    args = cli.parse_args()
    verify(args.stream, args.tips)

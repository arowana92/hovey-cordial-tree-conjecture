"""Realize the multiset reduction and check the resulting labels on whole trees."""
import argparse
import subprocess
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from random import Random

from .check_four_hole_matchings import K, RECORD, UNITS, catalog
from research.census.check_order_fifty_samples import core

G = set(range(K))
HOLES, IMAGES = catalog()
INDEX = {mask: i for i, mask in enumerate(HOLES)}


def prepare(shores):
    bags = [Counter(values) for values in shores]
    m, = {sum(b.values()) for b in bags}
    assert m - sum(m - len(b) for b in bags) >= 23
    assert sum(sum(x*n for x, n in b.items()) for b in bags) % K == 0
    fixed = []
    while m > 23:
        special = next(((i, x) for i, b in enumerate(bags) for x, n in b.items() if n > 1), None)
        i, x = special or (0, next(iter(bags[0])))
        j, k = (i+1) % 3, (i+2) % 3
        y = next(y for y in bags[j] if (-x-y) % K in bags[k])
        row = [0]*3
        row[i], row[j], row[k] = x, y, (-x-y) % K
        for b, v in zip(bags, row):
            b[v] -= 1
            if not b[v]:
                del b[v]
        fixed.append(tuple(row))
        m -= 1
    assert all(len(b) == 23 for b in bags)
    center = [(-sum(b) * pow(23, -1, K)) % K for b in bags]
    assert sum(center) % K == 0
    ids = [INDEX[sum(1 << x for x in G - {(v+t) % K for v in b})] for b, t in zip(bags, center)]
    key, unit, perm = min(
        (tuple(IMAGES[ids[i]][col] for i in order), u, order)
        for col, u in enumerate(UNITS)
        for order in [tuple(sorted(range(3), key=lambda i: IMAGES[ids[i]][col]))])
    return key, unit, perm, center, fixed


def interpret(data, record, shores):
    key, unit, perm, center, fixed = data
    assert tuple(record[:3]) == key
    middle = sorted(x for x in G if not (HOLES[key[1]] >> x & 1))
    rows = fixed.copy()
    for x, s in zip(record[3:], middle):
        row = [0]*3
        for j, value in zip(perm, (x, s, -x-s)):
            row[j] = (value*pow(unit, -1, K) - center[j]) % K
        rows.append(tuple(row))
    assert all(sum(row) % K == 0 for row in rows)
    assert all(Counter(col) == Counter(original) for col, original in zip(zip(*rows), shores))
    return rows


def balanced(labels, edges, offsets):
    h = Counter(labels)
    w = Counter((labels[a]+labels[b]+o) % K for (a, b), o in zip(edges, offsets))
    assert len(edges) == len(offsets) == len(labels)-1
    for hist in (h, w):
        assert max(hist[x] for x in G) - min(hist[x] for x in G) <= 1
    return h, w


def cores(h):
    for period in (1, 2):
        n = period*K + h
        labels = [(i//2 + ((n+1)//2 if i%2 else 0)) % K for i in range(n)]
        yield labels, [(i-1, i) for i in range(1, n)]
    for run in (3, 8):
        labels, edges = core(run)
        for i in range(1, h):
            vs, ws = balanced(labels, edges, [0]*len(edges))
            parent = (i+run) % K
            x = next(v for v in range(K) if vs[v] == 1 and ws[(v+labels[parent]) % K] == 1)
            edges.append((parent, len(labels)))
            labels.append(x)
        yield labels, edges


def match_shores(generator, shores_list):
    prepared = [prepare(shores) for shores in shores_list]
    keys = sorted({data[0] for data in prepared})
    query = ''.join('%d %d %d\n' % key for key in keys)
    raw = subprocess.run([str(generator.resolve()), '--keys'], input=query.encode(),
                         stdout=subprocess.PIPE, check=True).stdout
    records = {key: row for key, row in zip(keys, RECORD.iter_unpack(raw))}
    assert len(raw) == RECORD.size*len(keys)
    return len(keys), [interpret(data, records[data[0]], shores)
                       for data, shores in zip(prepared, shores_list)]


def checks(generator):
    rng = Random(231627)
    cases = []
    trees, blocked = 0, 0
    for h in range(1, 5):
        for f, edges in cores(h):
            vs, ws = balanced(f, edges, [0]*len(edges))
            m = len(f)//K
            U = {x for x in G if vs[x] > m}
            W = {x for x in G if ws[x] > m}
            assert (len(U), len(W)) == (h, h-1)
            for r in (K-h-2, K-h-1, K-h):
                for excess in range(5-h):
                    for use_offsets in (False, True):
                        for _ in range(4):
                            shifts = rng.sample(range(K), r-excess)
                            shifts += rng.choices(shifts, k=excess)
                            rng.shuffle(shifts)
                            parents = [rng.randrange(len(f)) if use_offsets else f.index(s) for s in shifts]
                            offsets = [(s-f[p]) % K for s, p in zip(shifts, parents)]
                            ext = shifts.copy()
                            while len(ext) < K-h:
                                candidates = sorted(G - set(ext))
                                if len(ext) == K-h-1:
                                    candidates = [v for v in candidates if (sum(U)-sum(W)-sum(ext)-v) % K not in W]
                                ext.append(rng.choice(candidates))
                            z = (sum(U)-sum(W)-sum(ext)) % K
                            if z in W:
                                assert r == K-h
                                blocked += 1
                                continue
                            shores = (sorted(G-U), ext, sorted((-w) % K for w in G-W-{z}))
                            cases.append((shores, (f, edges, parents, shifts, offsets)))
    # Twenty-three actual leaves, all with different parents, on 29-vertex cores.
    actual = 0
    for f, edges in cores(2):
        if len(f) != 29:
            continue
        deg = Counter(v for edge in edges for v in edge)
        tips = {v for v in range(29) if deg[v] == 1}
        for _ in range(40):
            parents = sorted(tips) + rng.sample(sorted(set(range(29))-tips), 23-len(tips))
            shifts = [f[i] for i in parents]
            vs, ws = balanced(f, edges, [0]*len(edges))
            U = {x for x in G if vs[x] == 2}
            W = {x for x in G if ws[x] == 2}
            a, b = next((a, b) for a, b in combinations(sorted(G-set(shifts)), 2)
                        if (sum(U)-sum(W)-sum(shifts)-a-b) % K not in W)
            ext = shifts+[a, b]
            z = (sum(U)-sum(W)-sum(ext)) % K
            cases.append(((sorted(G-U), ext, sorted((-w) % K for w in G-W-{z})),
                          (f, edges, parents, shifts, [0]*23)))
            actual += 1
    # Choose the added core labels from sites that receive no exterior leaf.
    controlled = 0
    for leaves, sites in ((23, 22), (22, 22)):
        h = 52 - leaves - K
        for run in (2, 5, 9):
            initial, original_edges = core(run)
            for _ in range(30):
                f, edges = initial.copy(), original_edges.copy()
                old_tips = {v for v in range(28) if sum(v in edge for edge in edges) == 1}
                origins = rng.sample(range(28), h-1)
                tips = old_tips-set(origins)
                parents = sorted(tips) + rng.sample(sorted(set(range(28))-tips), sites-(h-1)-len(tips))
                parents += list(range(28, K+h))
                parents += rng.choices(parents, k=leaves-sites)
                old_counts = Counter(f)
                unused = {f[v] for v in range(28) if v not in parents and old_counts[f[v]] == 1}
                W = set()
                for origin in origins:
                    x = next(x for x in sorted(unused) if (x+f[origin]) % K not in W)
                    unused.remove(x)
                    W.add((x+f[origin]) % K)
                    edges.append((origin, len(f)))
                    f.append(x)
                vs, ws = balanced(f, edges, [0]*len(edges))
                U = {x for x in G if vs[x] == 2}
                assert W == {x for x in G if ws[x] == 2}
                shifts = [f[v] for v in parents]
                assert len(set(shifts)) >= sites-1
                a, b = next((a, b) for a, b in combinations(sorted(G-set(shifts)), 2)
                            if (sum(U)-sum(W)-sum(shifts)-a-b) % K not in W)
                ext = shifts+[a, b]
                z = (sum(U)-sum(W)-sum(ext)) % K
                cases.append(((sorted(G-U), ext, sorted((-w) % K for w in G-W-{z})),
                              (f, edges, parents, shifts, [0]*leaves)))
                controlled += 1
    # At order 54 the last core leaf (with one exterior child) tunes the gap.
    divisible = 0
    for leaves, sites in ((25, 24), (25, 25), (24, 24)):
        h = 54-leaves-K
        for run in (3, 7):
            for _ in range(40):
                f, edges = core(run)
                origins = rng.sample(range(28), h-1)
                must = {v for v in range(28) if sum(v in edge for edge in edges) == 1} - set(origins)
                selected = sorted(must) + rng.sample(sorted(set(range(28))-must), sites-(h-1)-len(must))
                parents = selected + list(range(28, K+h))
                if sites < leaves:
                    parents.append(rng.choice(selected))
                old, _ = balanced(f, edges, [0]*len(edges))
                pool = {f[v] for v in range(28) if v not in parents and old[f[v]] == 1}
                for origin in origins[:-1]:
                    x = min(pool)
                    pool.remove(x)
                    edges.append((origin, len(f)))
                    f.append(x)
                vcount, wcount = balanced(f, edges, [0]*len(edges))
                U = {x for x in G if vcount[x] == 2}
                W = {x for x in G if wcount[x] == 2}
                prior = [f[v] for v in parents if v < len(f)]
                assert len(prior) == leaves-1
                for a in sorted(pool) + sorted(G-pool):
                    w = (a+f[origins[-1]]) % K
                    shifts = prior+[a]
                    z = (sum(U)+a-sum(W)-w-sum(shifts)) % K
                    if a not in U and w not in W and z not in W|{w} and h+leaves-len(set(shifts)) <= 4:
                        break
                else:
                    raise AssertionError("missing full-size repair")
                edges.append((origins[-1], len(f)))
                f.append(a)
                shifts = [f[v] for v in parents]
                cases.append(((sorted(G-U-{a}), shifts, sorted((-x) % K for x in G-W-{w,z})),
                              (f, edges, parents, shifts, [0]*leaves)))
                divisible += 1
    # Three repeated shores, including valid multisets larger than the group.
    for m in range(24, 30):
        for _ in range(45):
            extras = m-23
            while True:
                base = K if m >= K else m-1
                rows = [(x, x, -2*x % K) for x in rng.sample(range(K), base)]
                for j in range(m-base):
                    a, b = rng.randrange(K), rng.randrange(K)
                    rows.append((a, b, (-a-b) % K))
                shores = tuple(list(col) for col in zip(*rows))
                if sum(m-len(set(col)) for col in shores) <= extras:
                    break
            cases.append((shores, None))
    key_count, solutions = match_shores(generator, [shores for shores, _ in cases])
    for (_, tree), rows in zip(cases, solutions):
        if tree:
            f, edges, parents, shifts, offsets = tree
            by_shift = defaultdict(list)
            for x, s, _ in rows:
                by_shift[s].append(x)
            g = f + [by_shift[s].pop() for s in shifts]
            joins = [(p, len(f)+j) for j, p in enumerate(parents)]
            balanced(g, edges+joins, [0]*len(edges)+offsets)
            trees += 1
    assert blocked and actual
    print(f'{key_count} orbit witnesses, {trees} whole trees, including {actual} with '
          f'23 different leaf parents at order 52, {controlled} with controlled core labels at order 52, '
          f'{divisible} tuned at order 54, {blocked} forced collisions, '
          f'{len(cases)-trees} multiset checks')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('generator', type=Path)
    checks(parser.parse_args().generator)

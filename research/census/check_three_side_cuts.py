"""Verify the three cuts, compressed labeling and original histograms in five trees."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

from .check_order_fifty_one import cut_checker
from .check_order_fifty_two import singleton_cut
from .check_order_fifty_two_eighteen import common_or_pair
from .check_order_fifty_two_frontier import published


def check(path):
    old_cut = cut_checker(published(), 24, common_or_pair)
    for leaves, line in enumerate(path.read_text().splitlines(), 19):
        data = json.loads(line)
        parent = data['parents']
        edges = [(p, i) for i, p in enumerate(parent, 1)]
        assert len(edges) == 51 and all(0 <= p < i for p, i in edges)
        sub = [{i} for i in range(52)]
        for p, i in reversed(edges):
            sub[p].update(sub[i])
        all_vertices = sub[0]
        tips = all_vertices - set(parent)
        assert len(tips) == leaves
        profile = tuple(sorted((len(sub[i]), len(sub[i] & tips)) for p, i in edges if p == 0))
        assert max(s for s, _ in profile) < 26
        assert not singleton_cut(profile) and not old_cut(profile)

        # Try both orientations of every single-edge side in the original tree.
        sides = [a for _, i in edges for a in (sub[i], all_vertices-sub[i]) if len(a) < 25]
        assert not any(len(a)+len(b) == 25 and a.isdisjoint(b) for a, b in combinations(sides, 2))
        for v in all_vertices:
            sizes = [len(sub[i]) for p, i in edges if p == v]
            if v:
                sizes.append(52-len(sub[v]))
            sums = {0}
            for s in sizes:
                sums |= {old+s for old in sums}
            assert sums.isdisjoint({22, 24})

        a, b, t = data['sides']
        u, v, w = (parent[i-1] for i in (a, b, t))
        exterior = sub[a] | sub[b] | sub[t]
        middle = all_vertices-exterior
        assert len(exterior) == sum(len(sub[i]) for i in (a, b, t)) == 25
        assert {u, v, w} <= middle and u != v
        assert (u, v) not in edges and (v, u) not in edges
        internal = [(x, y) for x, y in edges if x in middle and y in middle]
        closed = internal + [(u, v)]
        degrees = Counter(i for edge in closed for i in edge)
        ring_leaves = sum(d == 1 for d in degrees.values())
        assert ring_leaves in (0, 2, 3, 4, 5, 6)

        f = data['labels']
        assert len(f) == 52 and all(0 <= x < 27 for x in f)
        residues = set(range(27))
        def weight(x, y):
            return (f[x]+f[y]) % 27
        assert {f[x] for x in middle} == {weight(x, y) for x, y in closed} == residues
        assert f[a] == f[v]
        delta = (f[w]-f[v]) % 27
        base = [weight(x, y) for x, y in edges if x in exterior and y in exterior]
        base += [weight(a, b), (weight(a, t)+delta) % 27]
        assert len(set(base)) == len(base) == 24 and len({f[x] for x in exterior}) == 25
        original = Counter(weight(x, y) for x, y in edges)
        assert original == Counter(base) + Counter(residues)
        assert Counter(f) == Counter(f[x] for x in exterior) + Counter(residues)
        for hist in (Counter(f), original):
            assert max(hist[x] for x in residues)-min(hist[x] for x in residues) == 1
        print(leaves, 'leaves, exterior orders', [len(sub[i]) for i in (a,b,t)],
              'closed leaves', ring_leaves, 'offset', delta)
    assert leaves == 23


if __name__ == '__main__':
    check(Path(__file__).with_name('three-side-examples.jsonl'))

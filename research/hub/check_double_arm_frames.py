"""Verify the finite grid, propagation data, and both intervals on expanded trees."""

from collections import Counter
from itertools import combinations
import json
from pathlib import Path

from research.hub.all_radius_two import minimal_shell
from research.hub.double_arm_frames import expand, seed_tree


def direct_check(edges, a, b, plain=(0, 0)):
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    lo, hi = min(adj), max(adj)
    assert sorted(adj) == list(range(lo, hi+1))
    assert sorted(u+v for u, v in edges) == list(range(lo+1, hi+1))
    assert len(adj) == 2+2*(a+b)+sum(plain) and 1 in adj[0]
    seen = {0, 1}
    for c, count in enumerate((a, b)):
        kinds = Counter()
        for p in adj[c]:
            if p == 1-c:
                continue
            assert p not in seen
            seen.add(p)
            children = [v for v in adj[p] if v != c]
            kinds[len(children)] += 1
            for x in children:
                assert x not in seen and adj[x] == [p]
                seen.add(x)
        assert kinds[0] == plain[c] and kinds[1] == count and sum(kinds.values()) == plain[c]+count
    assert seen == set(adj)


def triples_at_minimum(d):
    tau = minimal_shell(d)
    remaining = set(tau)
    triples = []
    while remaining:
        u = min(remaining)
        v = -tau[u]
        w = -tau[v]
        assert u+v+w == 0 and -tau[w] == u and len({u, v, w}) == 3
        remaining.difference_update((u, v, w))
        triples.append((u, v, w))
    return triples


def main():
    rows = [json.loads(line) for line in Path(__file__).with_name("double-arm-seeds.jsonl").read_text().splitlines()]
    frames = {}
    bases = set()
    expanded = 0
    for record in rows:
        a, b, cutoff, lo, arms = record
        assert (a,b) not in bases and 1 <= b <= a
        bases.add((a,b))
        edges = seed_tree(record)
        direct_check(edges, a, b)
        hi = lo+2*(a+b)+1
        assert (lo, hi) == (min(min(e) for e in edges), max(max(e) for e in edges))
        if not cutoff:
            continue
        assert cutoff in (4, 6)
        def speed(x):
            centered = x if x%2 == 0 else x+1
            return -1 if centered <= -cutoff else int(centered >= cutoff)
        for c,p,x in arms:
            assert speed(c) == 0 and speed(p) == speed(c+p) and speed(p)+speed(x) == speed(p+x)
        # Both old intervals contain the whole fixed central progression of each parity.
        for x in range(-cutoff+1, cutoff-1):
            assert lo+1 <= x <= hi
        frames[a,b] = cutoff
        triples = triples_at_minimum(cutoff//2)
        for count in range(len(triples)+1):
            for selection in combinations(range(len(triples)), count):
                tree = expand(record, triples, set(selection))
                low = min(min(e) for e in tree)
                high = max(max(e) for e in tree)
                tree.extend([(1,low-1), (1,low-2), (0,high+1)])
                direct_check(tree, a+3*(len(triples)-count), b+3*count, (1,2))
                expanded += 1
    assert set(frames) == {(x,y) for x in range(4,10) for y in (1,2,3)}
    for n in range(2,42):
        for b in range(1,n//2+1):
            a = n-b
            assert (a,b) in bases or any(
                a>=x and b>=y and (a-x)%3 == (b-y)%3 == 0
                and (n-x-y)%6 == 0 and n-x-y >= 6*(cutoff-1)
                for (x,y),cutoff in frames.items())
    print(f"Verified {len(rows)} base trees including {len(frames)} frames, and {expanded} expanded trees.")


if __name__ == "__main__":
    main()

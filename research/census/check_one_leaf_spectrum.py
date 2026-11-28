"""Verify prescribed one-bin transfers for a cycle with one pendant path."""
from argparse import ArgumentParser
from collections import Counter
from itertools import permutations
from math import gcd
from pathlib import Path

from check_one_leaf_period import graph


def targets(k):
    s = sum(range(k)) % k
    values = {(p,q) for p in range(k) for q in range(k) if p != q and (p-q)%k != s}
    if s:
        values.add(None)  # Uniform edge increments.
    return values


def classify(bins, k):
    """None denotes uniformity. False denotes any other out-of-scope histogram."""
    over = under = None
    for i in range(k):
        amount = bins[i]
        if amount == 2 and over is None:
            over = i
        elif amount == 0 and under is None:
            under = i
        elif amount != 1:
            return False
    if over is None and under is None:
        return None
    return (over,under) if over is not None and under is not None else False


def translate(pair, shift, k):
    return None if pair is None else tuple((v+shift)%k for v in pair)


def small(k, c, failures):
    expected = targets(k)
    es = graph(k,c)
    at = [set() for _ in range(c)]
    for other in permutations(range(1,k)):
        x = (0,)+other
        pair = classify(Counter((x[a]+x[b])%k for a,b in es),k)
        if pair is False:
            continue
        assert pair in expected
        for v in range(c):
            at[v].add(translate(pair,-2*x[v],k))
    bad_anchors = sum(len(expected-at[v]) for v in range(1,c))
    missing = {}
    for cut,(u,v) in enumerate(es[:c]):
        for d in range(k):
            found = at[v] | {translate(pair,2*d,k) for pair in at[u]}
            if found != expected:
                missing[cut,d] = expected-found
    before = sum(map(len,missing.values()))
    if missing:
        for x in permutations(range(k)):
            weights = [(x[u]+x[v])%k for u,v in es]
            closed = Counter(weights)
            for (cut,d), left in list(missing.items()):
                u,v = es[cut]
                net = closed.copy()
                net[weights[cut]]-=1
                net[d]-=1
                net[x[u]]+=1
                net[(x[v]+d)%k]+=1
                pair = classify(net,k)
                if pair is not False:
                    assert pair in expected
                    left.discard(pair)
                    if not left:
                        del missing[cut,d]
            if not missing:
                break
    gaps = sum(map(len,missing.values()))
    if failures is not None:
        for (cut,d), pairs in sorted(missing.items()):
            for pair in sorted(pairs, key=lambda x:(-1,-1) if x is None else x):
                p,q = (-1,-1) if pair is None else pair
                print(k,c,cut,d,p,q,file=failures)
    return bad_anchors, before, gaps, c*k*len(expected)


def small_range(failures):
    for k in range(4,10):
        result = [small(k,c,failures) for c in range(3,k)]
        anchors, direct, gaps, inputs = map(sum,zip(*result))
        print(f"k={k} unattained regular-anchor targets={anchors} direct tests={direct} "
              f"unattained openings={gaps} opening targets={inputs}",flush=True)


def streamed(k, path):
    expected = targets(k)
    units = [u for u in range(1,k) if gcd(u,k)==1]
    images = {pair:{None} if pair is None else {(u*pair[0]%k,u*pair[1]%k) for u in units}
              for pair in expected}
    hits = {c:[set() for _ in range(c)] for c in range(3,k)}
    edges = {c:graph(k,c) for c in hits}
    palette = set(range(k))
    rows = 0
    with path.open() as handle:
        for line in handle:
            mod,c,kind,*x = map(int,line.split())
            assert mod==k and c in hits and kind in (-2,-3) and len(x)==k and set(x)==palette
            weights = [(x[a]+x[b])%k for a,b in edges[c]]
            pair = classify(Counter(weights),k)
            assert pair is not False and pair in expected and (pair is None)==(kind==-3)
            for v in range(1,c):
                hits[c][v].add(translate(pair,-2*x[v],k))
            rows+=1
    anchor_inputs = 0
    for c in hits:
        for v in range(1,c):
            raw = hits[c][v] | hits[c][c-v]
            for pair in expected:
                assert not images[pair].isdisjoint(raw), (k,c,v,pair)
            anchor_inputs += len(expected)
    openings = sum(c*k*len(expected) for c in hits)
    print(f"k={k} rows={rows} normalized anchor targets={anchor_inputs} opening targets={openings}",flush=True)


def routing():
    """Compare the minimum number of transfers with sums of actual allowed steps."""
    checks = 0
    for k in range(4, 10):
        zero = (0,) * k
        steps = {(p, q) for p in range(k) for q in range(k)}
        legal = {(p, q) for p, q in steps if (p-q) % k != sum(range(k)) % k}

        def extend(states, arcs):
            next_states = set()
            for state in states:
                for p, q in arcs:
                    row = list(state)
                    row[q] -= 1
                    row[p] += 1
                    next_states.add(tuple(row))
            return next_states

        candidates = attained = {zero}
        for t in range(1, 5):
            candidates = extend(candidates, steps)
            attained = extend(attained, legal)
            for net in candidates:
                h = sum(max(0, x) for x in net)
                if k % 2:
                    feasible = h <= t and (h > 0 or t != 1)
                else:
                    cost = max(max(0, -net[q]) + max(0, net[(q+k//2) % k]) for q in range(k))
                    feasible = max(h, cost) <= t
                assert feasible == (net in attained), (k, t, net)
            checks += len(candidates)
    print(f"exact transfer-count tests={checks}")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--routing", action="store_true")
    cli.add_argument("--failures", type=Path)
    cli.add_argument("--stream", type=Path)
    cli.add_argument("--modulus", type=int)
    args = cli.parse_args()
    if args.routing:
        routing()
    elif args.stream is not None:
        if args.modulus is None:
            cli.error("--stream requires --modulus")
        streamed(args.modulus,args.stream)
    elif args.failures:
        with args.failures.open("w") as f:
            small_range(f)
    else:
        small_range(None)

"""Verify actual opened-edge counts, degree cores and simultaneous transfers."""
from collections import Counter
from itertools import permutations, product
from functools import reduce
from math import gcd
from random import Random

from check import adjacency
from check_shifted_ring import graphs, verify
from edge_histogram import construct, uniform_transfers


def cycle_edges(edges):
    # An edge lies on the unique cycle exactly when its endpoints stay connected.
    ns = adjacency(len(edges), edges)
    result = []
    for a,b in edges:
        seen, queue = {a}, [a]
        for v in queue:
            for w in ns[v]-seen:
                if v == a and w == b:
                    continue
                seen.add(w)
                queue.append(w)
        if b in seen:
            result.append((a,b))
    return result


def targets(k, m, wanted, rng):
    # Force the sum difference. Repeated extra bins deliberately occur often.
    while True:
        q = rng.sample(range(k), m)
        if not m:
            return q, []
        value = rng.randrange(k)
        p = [value]*(m-1)
        p.append((wanted+sum(q)-sum(p)) % k)
        if not set(q) & set(p):
            return q, p
        if m == 1 and not wanted:
            return [], []


def embedding_cores():
    rng = Random(13805)
    counts = Counter()
    for k in (311, 420, 503, 625, 810):
        for edges in graphs(k):
            ns = adjacency(k, edges)
            leaves = sum(len(row) == 1 for row in ns)
            ring = cycle_edges(edges)
            for m in (0, 1, 3, 8):
                opening = rng.choice(ring)
                anchor = rng.choice([v for v in opening if leaves != 1 or len(ns[v]) == 2])
                label = rng.randrange(k)
                s = sum(range(k)) % k
                differences = [s, (s+1) % k] if m else [0]
                for difference in differences:
                    q, p = targets(k, m, difference, rng)
                    d = (sum(p)-sum(q)) % k
                    possible = (d == s if not leaves else d != s if leaves == 1 else True)
                    common = reduce(gcd, (len(row)-1 for v,row in enumerate(ns) if v != anchor), k)
                    possible &= (d-(len(ns[anchor])-1)*label) % common == 0
                    result = construct(edges, opening, anchor, label, q, p, rng, cap=4)
                    assert (result is not None) == possible
                    counts["accepted" if possible else "rejected"] += 1
                    if not possible:
                        continue
                    aux, donors, bias = result
                    verify(edges, {frozenset(pair): x for pair,x in bias.items()}, aux)
                    _, _, _, pins, labels = aux
                    assert pins[anchor] == label
                    assert [(pins[a]+pins[b]) % k for a,b in donors] == p
                    assert [(pins[a]+pins[b]+bias[a,b]) % k for a,b in donors] == q
                    # On all old edges induced by the larger embedding core, undo the biases.
                    original = Counter((labels[a]+labels[b]) % k for a,b in edges
                                       if a in labels and b in labels)
                    shifted = Counter((labels[a]+labels[b]+bias.get(tuple(sorted((a,b))),0)) % k
                                      for a,b in edges if a in labels and b in labels)
                    original.update(q)
                    shifted.update(p)
                    assert original == shifted
                    if len(set(p)) < len(p):
                        counts["repeated extras"] += 1
    return counts


def tree_cases(k):
    yield [(v-1,v) for v in range(1,k)], 0
    yield [(v-1,v) for v in range(1,k)], k//2
    for edges in graphs(k):
        tree = edges[1:]
        yield tree, tree[len(tree)//3][0]
    if k % 3 == 0:
        # All degrees except the root are one or four.
        edges = [(0,1),(0,2)]
        for first in range(3,k,3):
            parent = first//3
            edges.extend((parent,v) for v in range(first,first+3))
        yield edges, 0


def tree_cores():
    rng = Random(45829)
    counts = Counter()
    for k in (420,503,625):
        for edges, anchor in tree_cases(k):
            ns = adjacency(k, edges)
            h = reduce(gcd,(len(row)-1 for v,row in enumerate(ns) if v!=anchor),k)
            path_end = len(ns[anchor]) == 1 and max(map(len,ns)) == 2
            s = sum(range(k)) % k
            for many in (False,True):
                offsets = {tuple(sorted(pair)): rng.randrange(1,k) for pair in rng.sample(edges,6)} if many else {}
                total = sum(offsets.values())
                label = rng.randrange(k)
                for wanted in (0,(len(ns[anchor])-1)*label,1,s-2*label):
                    for m in (0,6):
                        delta = (wanted+total) % k
                        if m:
                            while True:
                                w = rng.randrange(k)
                                q,p = targets(k,m,(delta+w)%k,rng)
                                if w not in q and w not in p:
                                    break
                        else:
                            w, q, p = (-delta)%k, [], []
                        omitted = q+[w]
                        result = construct(edges,None,anchor,label,omitted,p,rng,cap=4,offsets=offsets)
                        possible = (wanted-(len(ns[anchor])-1)*label) % h == 0
                        if path_end and (s-wanted-2*label)%k == 0:
                            possible = False
                        assert (result is not None) == possible
                        counts["accepted" if possible else "rejected"] += 1
                        if not possible:
                            continue
                        aux, donors, adjusted = result
                        tree, closing, gap, pins, labels = aux
                        assert closing is None and gap == w and pins[anchor] == label
                        assert all(labels[v]==x for v,x in pins.items())
                        assert len(labels)==len(set(labels.values())) and sum(labels.values())%k==s
                        adj = adjacency(k,tree)
                        reach, order = {0}, [0]
                        for v in order:
                            for u in adj[v]-reach:
                                reach.add(u)
                                order.append(u)
                        assert len(reach)==k and len(tree)==k-1 and max(map(len,adj))<=6
                        assert (sum(len(adj[v])*x for v,x in labels.items())+w)%k==s
                        for d,n in Counter(map(len,adj)).items():
                            inside=sum(len(adj[v])==d for v in labels)
                            assert inside==n or min(inside,n-inside)>=6
                        old, new = set(map(frozenset,edges)), set(map(frozenset,tree))
                        assert all(e<=pins.keys() for e in (old^new)|set(map(frozenset,adjusted)))
                        for point in (pins,labels):
                            weighted = Counter((point[a]+point[b]+offsets.get(tuple(sorted((a,b))),0))%k
                                               for a,b in edges if a in point and b in point)
                            bounded = Counter((point[a]+point[b])%k for a,b in tree if a in point and b in point)
                            assert w not in bounded and all(amount==1 for amount in bounded.values())
                            weighted.update(q)
                            bounded.update(p)
                            assert weighted==bounded
                        assert [(pins[a]+pins[b])%k for a,b in donors] == p
                        if h>1:
                            counts["proper divisor"]+=1
    return counts


def small_insertions():
    inputs = opened = 0
    for k in range(3, 9):
        for edges in graphs(k):
            ns = adjacency(k, edges)
            leaves = sum(len(row)==1 for row in ns)
            ring = cycle_edges(edges)
            u, v = ring[-1]
            if leaves == 1 and len(ns[v]) != 2:
                u, v = v, u
            vertices = [i for i in range(k) if i != v]
            seen = set()
            for values in permutations(range(1,k)):
                labels = dict(zip(vertices, values))
                labels[v] = 0
                weights = [(labels[a]+labels[b]) % k for a,b in edges]
                delta = (sum(weights)-sum(range(k))) % k
                s = sum(range(k)) % k
                assert leaves or delta == s
                assert leaves != 1 or delta != s
                inputs += 1
                bins = Counter(weights)
                hist = tuple(bins.get(i,0) for i in range(k))
                if hist in seen:
                    continue
                seen.add(hist)
                # Translate the whole piece. Keep both old labels, including equal labels.
                a = len(seen) % k
                labels = {i:(x+a)%k for i,x in labels.items()}
                target = Counter((weight+2*a)%k for weight in weights)
                for b in (a,(a+1)%k):
                    actual = Counter((labels[i]+labels[j])%k for i,j in edges if {i,j} != {u,v})
                    actual[(a+labels[u])%k] += 1
                    actual[(labels[v]+b)%k] += 1
                    actual[(a+b)%k] -= 1
                    assert all(actual[x]==target[x] for x in range(k))
                    opened += 1
    return inputs, opened


def attachment_prefixes():
    rng = Random(93411)
    totals = Counter()
    for k in range(4,9):
        for edges, anchor in tree_cases(k):
            adj = adjacency(k,edges)
            if max(map(len,adj)) == 0:
                continue
            parents, order = {anchor:None}, [anchor]
            for v in order:
                for u in sorted(adj[v]-parents.keys()):
                    parents[u] = v
                    order.append(u)
            free = order[1:]
            h = reduce(gcd,(len(adj[v])-1 for v in free),k)
            path_end = len(adj[anchor]) == 1 and max(map(len,adj)) == 2
            for uniform in (False,True):
                boundaries = {v:(0 if uniform else rng.randrange(k)) for v in adj[anchor]}
                allowed = {w for w in range(k) if (w+sum(boundaries.values()))%h == 0}
                if path_end:
                    allowed.discard((-sum(range(k))-sum(boundaries.values()))%k)
                seen = set()
                for values in permutations(range(1,k)):
                    x = dict(zip(free,values))
                    weights = [(x[v]+(boundaries[v] if v in boundaries else x[parents[v]]))%k for v in free]
                    if len(set(weights)) != k-1:
                        continue
                    w = next(iter(set(range(k))-set(weights)))
                    assert w in allowed
                    if w in seen:
                        continue
                    seen.add(w)
                    # A star with center zero and leaves of every residue realizes the core.
                    vertices, sums = [2]+[1]*(k-1), [1]*k
                    for v, weight in zip(free,weights):
                        vertices[x[v]] += 1
                        sums[weight] += 1
                        assert max(vertices)-min(vertices)<=1 and max(sums)-min(sums)<=1
                        totals["balanced prefixes"] += 1
                totals["forests with boundaries"] += 1
                totals["attained gaps"] += len(seen)
                totals["extra small-order failures"] += len(allowed-seen)
    return totals


def simultaneous():
    choices = 0
    for k in range(3,32):
        s = sum(range(k)) % k
        for size in range(1,6):
            for leaves in product(range(3), repeat=size):
                accessible = {0}
                for count in leaves:
                    possible = [s] if not count else [d for d in range(k) if count == 2 or d != s]
                    accessible = {(x+d)%k for x in accessible for d in possible}
                moves = uniform_transfers(k, leaves)
                assert (moves is not None) == (0 in accessible)
                if moves is not None:
                    plus, minus = zip(*moves)
                    assert Counter(plus) == Counter(minus)
                    for (p,q), count in zip(moves, leaves):
                        assert count or (p-q)%k == s
                        assert count != 1 or (p-q)%k != s
                choices += 1
    return choices


if __name__ == "__main__":
    print(dict(embedding_cores()), flush=True)
    print("tree cores", dict(tree_cores()), flush=True)
    print("vertex permutations and opened labeled pieces", small_insertions(), flush=True)
    print("attachment replay", dict(attachment_prefixes()), flush=True)
    print("simultaneous moment tests", simultaneous())

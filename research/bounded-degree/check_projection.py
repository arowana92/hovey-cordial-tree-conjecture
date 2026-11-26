"""Verify the omission-set construction and the projected embedding hypotheses."""

from collections import Counter
from random import Random

from check import adjacency, require
from check_excess import construct


def reservoir(k, N):
    return set(range(k, 2 * k)).union(range(1, N, k), range(2, N, k))


def omissions(k, N, r, target):
    if r == 2:
        a = next(i for i in (1, 2) if 2 * i % k != target % k)
        residues = [a, (target - a) % k]
    elif r == k - 1:
        excluded = (sum(range(k)) - target) % k
        residues = [i for i in range(k) if i != excluded]
    else:
        others = list(range(1, r))
        extra = (target - r - sum(others)) % k
        for i in reversed(range(len(others))):
            room = k - len(others) + i - others[i]
            added = min(room, extra)
            others[i] += added
            extra -= added
        require(extra == 0, "subset sum interval exhausted")
        residues = [1] + [(1 + i) % k for i in others]
    free = next(i for i in (1, 2) if i in residues)
    selected = {k + i for i in residues if i != free}
    selected.add((target - sum(selected)) % N)
    return selected


def check_reservoir():
    count = 0
    for k in range(5, 23):
        for m in range(2, 7):
            N = k * m
            R = reservoir(k, N)
            for r in range(2, k):
                for s in range(N):
                    B = omissions(k, N, r, s)
                    require(len(B) == r and B <= R and sum(B) % N == s, "invalid omissions")
                    require(len({x % k for x in B}) == r, "repeated projection")
                    count += 1
    return count


def core_assignment(N, aux, n, pins, R, vertex_target, rng):
    graph = adjacency(n, aux)
    degrees = list(map(len, graph))
    Q = set(pins)
    for d in set(degrees):
        outside = [i for i, deg in enumerate(degrees) if deg == d and i not in Q]
        inside = degrees.count(d) - len(outside)
        take = max(0, 6 - inside)
        Q.update(outside if len(outside) - take < 6 else outside[:take])
    d = max(set(degrees), key=degrees.count)
    candidates = [v for v in range(n) if degrees[v] == d and v not in Q and not graph[v] & Q]
    z = candidates[0]
    zz = next(v for v in candidates if v != z and v not in graph[z])
    Q.update((z, zz))
    labels = dict(pins)
    for v in sorted(Q - set(labels) - {z, zz}):
        used = {(labels[a] + labels[b]) % N for a, b in aux if a in labels and b in labels}
        banned = R.union(labels.values())
        for w in graph[v].intersection(labels):
            banned.update((a - labels[w]) % N for a in used | R)
        labels[v] = rng.choice([x for x in range(N) if x not in banned])
    pair_sum = (sum(vertex_target) - sum(labels.values())) % N
    banned = R.union(labels.values())
    choices = [x for x in range(N) if x not in banned and (pair_sum - x) % N not in banned
               and 2 * x % N != pair_sum]
    labels[z] = rng.choice(choices)
    labels[zz] = (pair_sum - labels[z]) % N
    return labels


def check_targets():
    rng = Random(825)
    cases = 0
    for k, m in ((29, 39), (32, 32), (45, 25)):
        N = k * m
        G, R = set(range(N)), reservoir(k, N)
        for e in (1, 2, k // 2, k - 2):
            n = N - e
            for binary in (False, True):
                parents = [-1] + [(v - 1) // 2 if binary else v - 1 for v in range(1, n - 1)]
                parents[3:17] = [0] * 14
                parents[17:32] = [15] * 15
                roots, kept, aux, pins, _, _ = construct(parents, N, 3, rng, R)
                A = {k + a for a in range(e)}
                V = G - A
                labels = core_assignment(N, aux, n, pins, R, V, rng)
                graph = adjacency(n, aux)
                weighted = sum(len(graph[i]) * x for i, x in labels.items()) % N
                B = omissions(k, N, e + 1, (sum(G) - weighted) % N)
                C = G - B
                # Independently check the actual targets and the cut-edge transfer.
                require(len(V) == n and len(C) == n - 1, "wrong target sizes")
                require(len(set(labels.values())) == len(labels) and set(labels.values()) <= V,
                        "vertex-target inclusion")
                weights = [(labels[a] + labels[b]) % N for a, b in aux if a in labels and b in labels]
                require(len(weights) == len(set(weights)) and set(weights) <= C, "edge-target inclusion")
                require(sum(labels.values()) % N == sum(V) % N and weighted == sum(C) % N,
                        "target sum mismatch")
                for d in set(map(len, graph)):
                    inside = sum(len(graph[i]) == d for i in labels)
                    outside = sum(len(row) == d for row in graph) - inside
                    require(outside == 0 or min(inside, outside) >= 6, "degree-class condition")
                old = Counter((labels[i] + (labels[parents[i]] if parents[i] >= 0 else 0)) % N
                              for i in roots)
                added = set(tuple(sorted(edge)) for edge in aux) - set(tuple(sorted(edge)) for edge in kept)
                require(old == Counter((labels[a] + labels[b]) % N for a, b in added), "edge transfer")
                for target in (V, C):
                    hist = Counter(x % k for x in target)
                    require(all(hist[i] in (m - 1, m) for i in range(k)), "unbalanced projection")
                cases += 1
    return cases


if __name__ == "__main__":
    print(f"Checked {check_reservoir()} prescribed omission sums and {check_targets()} projected core assignments.")

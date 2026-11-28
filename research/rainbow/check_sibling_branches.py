"""Check the size bound for a gcd class and replay sibling-padded joins."""
from itertools import combinations
from math import gcd


def least_prime(n):
    return next(d for d in range(2, n+1) if n % d == 0)


def small_sets():
    tested = 0
    for k in range(2, 13):
        classes = {gcd(b, k) for b in range(1, k)}
        largest = dict.fromkeys(classes, 0)
        # Translate a largest avoiding set to contain zero.
        for mask in range(1 << (k-1)):
            subset = [0] + [x for x in range(1, k) if mask & (1 << (x-1))]
            present = {gcd(y-x, k) for x, y in combinations(subset, 2)}
            for g in classes-present:
                largest[g] = max(largest[g], len(subset))
            tested += 1
        for g in classes:
            assert largest[g] == k // least_prime(k//g)
    return tested


def padded_tree(k, f):
    edges = [(x, f) for x in range(f)]
    edges.extend((f-1, x) for x in range(f+1, k))
    assert sorted(x+y for x, y in edges) == list(range(f, f+k-1))
    return edges


def choose(k, b, siblings, hole, q):
    # The root has color zero. Work with literal residues and try every scale.
    for z in siblings:
        targets = [hole] if q == 1 else [hole, *siblings]
        for w in targets:
            for u in range(1, k):
                if gcd(u, k) == 1 and (u*(w-z)-b) % k == 0:
                    removed = [z]
                    if w != hole and w != z:
                        removed.append(w)
                    removed.extend(x for x in siblings if x not in (z, w))
                    return u, z, set(removed[:q])
    raise AssertionError((k, b, siblings, hole, q))


def histogram(labels, edges, k):
    vertices, weights = [0]*k, [0]*k
    for x in labels:
        vertices[x] += 1
    for x, y in edges:
        weights[(labels[x]+labels[y]) % k] += 1
    assert max(vertices)-min(vertices) <= 1 and max(weights)-min(weights) <= 1


def whole_trees():
    examples = prime_endpoints = movable_pairs = 0
    for k in range(2, 41):
        for f in sorted({1, max(1, k//3), max(1, k//2), k-1}):
            edges = padded_tree(k, f)
            degree = [0]*k
            for i, j in edges:
                degree[i] += 1
                degree[j] += 1
            for root in (f-1, f):
                siblings = [(i+j-2*root) % k for i, j in edges
                            if root in (i, j) and degree[i+j-root] == 1]
                hole = (f-1-2*root) % k
                assert hole not in siblings
                for q in sorted({1, 2, 3, len(siblings)} & set(range(1, len(siblings)+1))):
                    for b in range(k):
                        if b:
                            g = gcd(b, k)
                            orbit_size = sum(gcd(x, k) == g for x in range(k))
                            via_hole = len(siblings) >= k-orbit_size
                            via_pair = q >= 2 and len(siblings) >= k//least_prime(k//g)
                            if not (via_hole or via_pair):
                                continue
                            u, z, deleted = choose(k, b, siblings, hole, q)
                            movable_pairs += not via_hole
                        else:
                            deleted = set(siblings[:q])
                            u, z = 1, siblings[0]
                        assert len(deleted) == q
                        # Core is a star of order k+1 with surplus zero.
                        labels = [0, *range(k)]
                        joined = [(0, i) for i in range(1, k+1)]
                        ids = {}
                        for i in range(k):
                            x = (i-root) % k
                            if x not in deleted:
                                ids[i] = len(labels)
                                labels.append(u*(x-z) % k)
                        joined.extend((ids[i], ids[j]) for i, j in edges if i in ids and j in ids)
                        joined.append((1+b, ids[root]))
                        histogram(labels, joined, k)
                        examples += 1
                        prime_endpoints += q == 1 and least_prime(k) == k and b != 0
    return examples, prime_endpoints, movable_pairs


if __name__ == '__main__':
    print('subsets containing zero', small_sets())
    print('whole trees, nonzero prime endpoint cases, cases using the pair bound', *whole_trees())

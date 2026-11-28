"""Check prescribed bridges on actual trees and the short-distance pin tables."""
from collections import Counter
from itertools import combinations, permutations, product

from .bridge_pins import bridge, path_endpoints


def histogram(k, values):
    counts = Counter(values)
    return [counts[x] for x in range(k)]


def cordial(k, labels, edges):
    for values in (labels, [(labels[u] + labels[v]) % k for u,v in edges]):
        bins = histogram(k, values)
        if max(bins) - min(bins) > 1:
            return False
    return True


def shapes(k):
    # Breadth or depth numbering supplies a parent-before-child representation.
    # Minimize over all choices of the root to keep one unrooted representative.
    seen = set()
    for parents in product(*(range(i) for i in range(1,k))):
        adj = [[] for _ in range(k)]
        edges = list(enumerate(parents,1))
        for v,u in edges:
            adj[v].append(u)
            adj[u].append(v)

        def word(v, parent):
            return '(' + ''.join(sorted(word(u,v) for u in adj[v] if u != parent)) + ')'

        key = min(word(v,-1) for v in range(k))
        if key not in seen:
            seen.add(key)
            yield adj,edges


def short_distances(k):
    all_nonzero = set(range(1,k))
    if k == 8:
        return [set(), {1,3,5,7}, set()] + [all_nonzero-{4}]*3 + [all_nonzero]
    return [set()] + [all_nonzero-{3,6}]*3 + [all_nonzero]*4


def base_census(k):
    cores = {}
    universal = [set(range(1,k)) for _ in range(k)]
    triples = set(combinations(range(1,k),2))
    shape_count = pair_tests = three_tests = 0
    for adj,edges in shapes(k):
        shape_count += 1
        rows = []
        for tail in permutations(range(1,k)):
            x = (0,) + tail
            weights = {(x[v] + x[u]) % k for v,u in edges}
            if len(weights) == k-1:
                rows.append(x)
                gap, = set(range(k)) - weights
                # A global translation creates genuine old cores of all port colors.
                for shift in range(k):
                    key = shift, (gap + 2 * shift) % k
                    if len(cores) < k*k and key not in cores:
                        cores[key] = ([(a+shift)%k for a in x], edges)
        for v in range(k):
            dist, todo = {v:0}, [v]
            for u in todo:
                for j in adj[u]:
                    if j not in dist:
                        dist[j] = dist[u]+1
                        todo.append(j)
            for u in range(v+1,k):
                universal[dist[u]] &= {(x[u]-x[v]) % k for x in rows}
                pair_tests += 1
            for u,w in combinations(adj[v],2):
                # Both assignments to the two specified neighbors must work.
                possible = {((x[u]-x[v])%k, (x[w]-x[v])%k) for x in rows}
                triples = {(a,b) for a,b in triples if (a,b) in possible and (b,a) in possible}
                three_tests += 1
    targets = short_distances(k)
    assert all(universal[i] == targets[i-1] for i in range(1,k))
    assert shape_count == {8:23, 9:47}[k] and len(cores) == k*k and not triples
    return cores, pair_tests, three_tests


def expected(k,a,b,d,e,t):
    if t == 0:
        return (a+b)%k in (d,e)
    if t == 1:
        return (b-a)%k in ((e-d)%k, (d-e)%k)
    if t == 2:
        return not (a == b and d == e == 2*a%k)
    return k%2 == 1 or t != k+1 or (a+b-d-e)%2 == 0


def check_bridges(k,cores):
    passed = rejected = 0
    for a,b,d,e in product(range(k),repeat=4):
        left, left_edges = cores[a,d]
        right, right_edges = cores[b,e]
        both = left_edges + [(u+k,v+k) for u,v in right_edges]
        for t in range(k+3):
            chain = [0] + list(range(2*k,2*k+t)) + [k]
            edges = both + list(zip(chain,chain[1:]))
            row = bridge(k,a,b,d,e,t)
            assert (row is not None) == expected(k,a,b,d,e,t), (a,b,d,e,t)
            if row is None:
                rejected += 1
                if t <= 2:
                    assert not any(cordial(k,left+right+list(x),edges) for x in permutations(range(k),t))
            else:
                assert len(row) == t and cordial(k,left+right+list(row),edges)
                passed += 1
    return passed,rejected


if __name__ == '__main__':
    for k in (8,9):
        cores,pairs,triples = base_census(k)
        print(f"{k} labels, {pairs} marked pairs, {triples} marked three-vertex paths", flush=True)
        passed,rejected = check_bridges(k,cores)
        print(f"{passed} verified bridges, {rejected} excluded inputs", flush=True)
        for n in range(2,2*k+2):
            ends = set()
            for b in range(k):
                row = path_endpoints(k,n,b)
                if row is None:
                    continue
                assert row[0] == 0 and row[-1] == b and len(row) == n
                assert cordial(k,row,list(zip(range(n-1),range(1,n))))
                ends.add(b)
            allowed = set(range(1 if n <= k else 0,k))
            if k == 8 and n%8 == 1:
                allowed &= {0,2,4,6}
                if n == 9:
                    allowed.discard(0)
            assert ends == allowed, (k,n,ends)
        print(f"Verified endpoint differences through order {2*k+1}")

"""Recount full trees and uniform forest attachments for the private-leaf constructions."""
import argparse
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from random import Random

from research.biased.check_four_hole_trees import G, K, match_shores
from research.census.check_order_fifty_samples import core


def increments(vertex, edge, parents, vt, et):
    # Check the requirements of the separate 27-label multiset theorem.
    if any(vt[x] < vertex[x] or et[x] < edge[x] for x in G):
        return None
    shores = (list((vt-vertex).elements()), parents, [(-x) % K for x in (et-edge).elements()])
    m = len(parents)
    if any(len(b) != m for b in shores):
        return None
    if sum(map(sum, shores)) % K or m-sum(m-len(set(b)) for b in shores) < 23:
        return None
    return shores


def targets(labels, edges, sites, rng):
    vertex = Counter(labels)
    edge = Counter((labels[a]+labels[b]) % K for a, b in edges)
    shifts = [labels[p] for p in sites]
    t = 2*K - len(labels)-len(shifts)
    double = Counter({x: 2 for x in G})
    if max(vertex.values()) > 2 or max(edge.values()) > 2:
        return None
    available = sorted(x for x in G if vertex[x] < 2)
    low = rng.sample(available, t)
    q = (sum(low) + sum(labels)-sum(x*n for x, n in edge.items())-sum(shifts)) % K
    for missing in combinations(sorted(x for x in G if edge[x] < 2), t+1):
        if sum(missing) % K == q:
            result = increments(vertex, edge, shifts, double-Counter(low), double-Counter(missing))
            if result:
                return result
    return None


def ordinary(rng):
    output = []
    changed = 0
    for run in range(1, 12):
        f, edges = core(run)
        f, edges = f[:K], edges[:-1]
        for t in range(3):
            for rep in range(12):
                sites = rng.sample(range(K), K-t)
                if rep % 3:
                    sites[-1] = sites[0]
                g = f.copy()
                if rep % 2 == 0:
                    g[rng.randrange(K)] = g[rng.randrange(K)]
                incoming = targets(g, edges, sites, rng)
                if not incoming:
                    # Recompute the forced gap after each one-vertex change.
                    for v in sorted(range(K), key=lambda v: sum(v in pair for pair in edges)+sites.count(v)):
                        prev = g[v]
                        for x in range(K):
                            g[v] = x
                            incoming = targets(g, edges, sites, rng)
                            if incoming:
                                break
                        if incoming:
                            changed += 1
                            break
                        g[v] = prev
                if incoming:
                    output.append((incoming, g.copy(), edges, sites, 0))
    assert changed > 0
    return output, changed


def packets(rng):
    output = []
    for run in range(1, 12):
        f, original = core(run)
        f, original = f[:K], original[:-1]
        adj = [[] for _ in f]
        for a, b in original:
            adj[a].append(b)
            adj[b].append(a)
        gap, = G-{(f[a]+f[b]) % K for a, b in original}
        for root in (0, 5, 13, 26):
            parent = [None]*K
            order = [root]
            boundary = {root: (gap-f[root]) % K}
            for v in order:
                for w in adj[v]:
                    if w != parent[v]:
                        parent[w] = v
                        order.append(w)
            for v in rng.sample(order[1:], 4):
                boundary[v] = f[parent[v]]
                parent[v] = None
            children = Counter(p for p in parent if p is not None)
            # Remove an ordinary terminal and replace its missing weight by the sum
            # of two extra parent shifts. All remaining sites keep a private leaf.
            removed = next(v for v in order if not children[v] and v != root)
            nodes = [v for v in range(K) if v != removed]
            source = boundary[removed] if removed in boundary else f[parent[removed]]
            missing = (f[removed]+source) % K
            left, right = next((v, w) for v, w in combinations(nodes, 2)
                               if (f[v]+f[w]) % K == missing)
            labels = [f[v] for v in nodes]
            location = {v: K+j for j, v in enumerate(nodes)}
            ends = [location[v] for v in nodes+[left, right]]
            edges = [(i-1, i) for i in range(1, K)]
            edges += [(boundary[v] if v in boundary else location[parent[v]], location[v]) for v in nodes]
            old_and_free = list(range(K)) + labels
            weights = Counter((old_and_free[a]+old_and_free[b]) % K for a, b in edges[K-1:])
            double = Counter({x: 2 for x in G})
            selected = increments(Counter(labels), weights, [old_and_free[v] for v in ends], double, double)
            assert selected
            output.append((selected, old_and_free, edges, ends, K))
            for j in range(6):
                v = rng.choice([v for v in order if not children[v]])
                w = rng.choice([w for w in order if w != v and parent[v] != w and children[w] <= 3])
                g = f.copy()
                g[v], g[w] = rng.randrange(K), rng.randrange(K)
                coefficient = 1+children[w]
                fixed = sum(boundary.values())+sum((1+children[i])*g[i] for i in range(K) if i not in (v,w))
                for y in rng.sample(range(K), K):
                    g[v], g[w] = (-fixed-coefficient*y) % K, y
                    weights = Counter((g[i]+(boundary[i] if p is None else g[p])) % K
                                      for i, p in enumerate(parent))
                    double = Counter({x: 2 for x in G})
                    selected = increments(Counter(g), weights, g.copy(), double, double)
                    if selected:
                        break
                assert selected
                # Attach to a concrete path containing a vertex of every boundary color.
                base = list(range(K))
                edges = [(i-1, i) for i in range(1,K)]
                edges += [(boundary[i] if p is None else K+p, K+i) for i, p in enumerate(parent)]
                output.append((selected, base+g, edges, list(range(K, 2*K)), K))
    return output


def check(generator):
    rng = Random(270223)
    trees, changed = ordinary(rng)
    blocks = packets(rng)
    all_cases = trees+blocks
    _, answers = match_shores(generator, [case[0] for case in all_cases])
    for (_, g, edges, sites, old), rows in zip(all_cases, answers):
        choices = defaultdict(list)
        for x, s, _ in rows:
            choices[s].append(x)
        labels = g+[choices[g[v]].pop() for v in sites]
        actual_edges = edges+[(p, len(g)+i) for i, p in enumerate(sites)]
        assert len(actual_edges) == len(labels)-1
        weights = [(labels[a]+labels[b]) % K for a, b in actual_edges]
        if old:
            assert Counter(labels[old:]) == Counter(weights[old-1:]) == Counter({x: 2 for x in G})
        else:
            for f in (Counter(labels), Counter(weights)):
                assert max(f[x] for x in G)-min(f[x] for x in G) <= 1
    print(f'{len(trees)} whole trees at orders 52 through 54, {changed} repaired by recoloring, '
          f'{len(blocks)} uniform two-period attachments on the original edges')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('generator', type=Path)
    check(parser.parse_args().generator)

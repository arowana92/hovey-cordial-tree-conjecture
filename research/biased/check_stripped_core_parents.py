"""Restore leaves on 27-cordial cores with a surplus at an inactive original site."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from random import Random

from .check_four_hole_trees import G, K, balanced, core, match_shores


def construct(rng, order, leaves, run, chain, copies, both_inactive):
    sites = order-32
    h = order-leaves-K
    f, edges = core(run)
    marks = [v for v in range(28) if f[v] == 0]
    internal, tip = marks
    n = K+h
    peripheral = run >= 4
    first = tip if peripheral else rng.randrange(27)
    for i in range(h-1):
        p = first if not i else (27+i if chain else rng.randrange(27))
        edges.append((p,28+i))
    degree = Counter(x for edge in edges for x in edge)
    must = {v for v in range(n) if degree[v] == 1}
    inactive = {tip} if peripheral else {internal}
    if both_inactive:
        inactive.update(marks)
    else:
        must.update(set(marks)-inactive)
    # Force an internal returning vertex to be inactive on the chain examples.
    if chain and h>=3:
        inactive.add(28)
    assert not must & inactive
    active = sorted(must | set(rng.sample(sorted(set(range(n))-must-inactive),sites-len(must))))
    last = n-1
    assert last in active
    parents = active + [last]*(copies-1)
    parents += rng.choices([v for v in active if v!=last], k=leaves-len(parents))
    old = Counter(f)
    high_weights = set()
    used = set()
    for i in range(28,n):
        p = edges[i-1][0]
        if i == last and order == 54:
            prior_active = {f[v] for v in active if v != last}
            available = G-prior_active
            assert len(available) == 6
        else:
            available = {f[v] for v in range(28) if (v in active) != (i in active) and old[f[v]]==1}
        for x in sorted(available-used):
            w = (f[p]+x) % K
            if w in high_weights or x == 0:
                continue
            if i == last and order == 54:
                u = {a for a,c in Counter(f+[x]).items() if c==2}
                z = (sum(u)-sum(high_weights)-w-sum(f[v] for v in parents if v!=last)-copies*x) % K
                if z in high_weights | {w}:
                    continue
            break
        else:
            raise AssertionError("no admissible restoration")
        used.add(x)
        f.append(x)
        high_weights.add(w)
    vs, ws = balanced(f,edges,[0]*(n-1))
    U = {v for v in G if vs[v]==2}
    W = {w for w in G if ws[w]==2}
    assert W==high_weights and len({f[v] for v in active})==sites
    shifts = [f[v] for v in parents]
    padding = K-h-leaves
    dummy = next(d for d in combinations(sorted(G-set(shifts)),padding)
                 if (sum(U)-sum(W)-sum(shifts)-sum(d)) % K not in W)
    ext = shifts+list(dummy)
    z = (sum(U)-sum(W)-sum(ext)) % K
    shores = (sorted(G-U),ext,sorted((-w)%K for w in G-W-{z}))
    return shores,(f,edges,parents)


def checks(generator):
    rng = Random(27525354)
    cases = []
    counts = Counter()
    for n in (52,53,54):
        p = n-32
        for l in range(n-31,n-28):
            h = n-l-K
            max_copies = (1 if h==4 else 2 if h==3 else 4) if n==54 else l-p+1
            for run in ((0,2) if n==54 else (0,2,4,6)):
                for chain in (False,True):
                    for copies in range(1,min(max_copies,l-p+1)+1):
                        for both_inactive in ((False,True) if run>=4 else (False,)):
                            for _ in range(4):
                                cases.append(construct(rng,n,l,run,chain,copies,both_inactive))
                                counts[(n,l)] += 1
    keys, solutions = match_shores(generator,[s for s,_ in cases],5)
    for (_, (f,edges,parents)), rows in zip(cases,solutions):
        by_shift = defaultdict(list)
        for x,s,_ in rows:
            by_shift[s].append(x)
        labels = f + [by_shift[f[p]].pop() for p in parents]
        final = edges + [(p,len(f)+i) for i,p in enumerate(parents)]
        balanced(labels,final,[0]*len(final))
        deg = Counter(v for edge in final for v in edge)
        assert sum(c==1 for c in deg.values())==len(parents)
        assert len(set(parents)) == len(labels)-32
    print(keys,'matching orbits;',len(cases),'whole trees by order and leaves',sorted(counts.items()))


if __name__ == '__main__':
    cli = ArgumentParser(description=__doc__)
    cli.add_argument('generator',type=Path)
    checks(cli.parse_args().generator)

"""Check the two weighted cuts used to isolate a dense ordinary suffix."""

from collections import Counter
from random import Random

from research.hub.branching_pools import rooted_order, two_suffixes
from research.hub.check_branching_pools import graph_of
from research.hub.check_subdivided_blocks import traversal


def leaf_sets(graph, vertices, d):
    count = {v:sum(w in vertices for w in graph[v]) for v in vertices}
    high = {v for v in vertices if count[v]>d}
    leaves = {v for v in vertices if count[v]==1}
    near = {v for v in leaves if any(w in high for w in graph[v] if w in vertices)}
    return high,leaves,near


def audit(graph, high, leaves, near, sites, chosen, decorations, k, t, removed):
    available = set(range(len(graph)))
    prefix = available - chosen
    old,rest,near2 = leaf_sets(graph,prefix,3)
    assert old <= high and len(rest-leaves) <= 2 and len(near2)<=len(near)+2
    origin = next(iter(prefix))
    _,par,_ = rooted_order(graph,origin)
    assert all(par[v] in prefix for v in prefix if v != origin)
    boundary = {par[v] for v in chosen if par[v] not in chosen}
    assert len(boundary) <= 3+k.bit_length()
    cut = chosen & (high|sites)
    roots = {v for v in chosen if par[v] not in chosen or par[v] in cut}
    has_children = {par[v] for v in chosen if v not in roots}
    single = roots-has_children
    assert all(v in cut or v in near or par[v] in (boundary|sites)-high for v in single)
    assert len(single)<=len(cut)+len(near)+3*len((boundary|sites)-high)
    internal = len(chosen)-len(roots)
    assert 2*internal >= len(chosen)-len(single)
    assert sum(decorations.get(v,0) for v in chosen) <= removed <= sum(decorations.values())
    assert len(chosen)+removed==t
    assert (len(graph)+sum(decorations.values())-t)%k==1
    # Append explicit temporary vertices. Check each remaining ordinary edge.
    parent = {v:par[v] for v in chosen}
    terminal = next(v for v in chosen if v not in parent.values())
    for v in range(len(graph),len(graph)+k-1-t):
        parent[v] = terminal
        terminal = v
    padded_internal = sum(p in parent and p not in cut for p in parent.values())
    assert len(parent)>=k//8 and padded_internal >= internal + k-1-t-1
    assert 2*padded_internal >= len(parent)-len(single)-2
    return len(cut),len(single),len(rest-leaves)


def main():
    rng = Random(99381)
    modes = Counter()
    maxima = [0,0,0]
    for k in (17,31,64,97,193):
        for n in (k+k//3,2*k-1,2*k+3,3*k+k//2,4*k-2):
            for i in range(6):
                tree = [-1]+[([v-1,0,(v-1)//3,v//17,rng.randrange(v),min(v-1,5)][i])
                             for v in range(1,n)]
                graph = graph_of(tree)
                ids = set(range(n))
                high, leaves, near = leaf_sets(graph,ids,3)
                order,_,_ = traversal(tree,3)
                for m in range(0,k,max(1,k//27)):
                    t = (n+m-1)%k
                    if m>=t:
                        continue
                    sites = set(rng.sample(range(n),rng.randrange(1,min(8,n))))
                    if high:
                        sites.add(rng.choice(sorted(high)))
                    entries = sorted(sites)
                    decorations = Counter(rng.choice(entries) for _ in range(m))
                    a = k//8
                    if t<2*a or t-m>=a:
                        tag = 'all'
                        chosen = set(order[-(t-m):])
                        remove = m
                    else:
                        tag = 'split'
                        _,sides = two_suffixes(graph,a)
                        chosen = min(sides,key=lambda side:sum(decorations[v] for v in side))
                        remove = t-a
                    stats = audit(graph,high,leaves,near,sites,chosen,decorations,k,t,remove)
                    maxima = list(map(max,zip(maxima,stats)))
                    modes[tag] += 1
    assert all(modes[x]>0 for x in ('all','split'))
    assert maxima[0]>1 and maxima[1]>3 and maxima[2]>=1
    print(f"{sum(modes.values()):,} decorated cuts, including {modes['split']:,} chosen "
          f"by comparing two suffixes; up to {maxima[0]} cut sites and {maxima[1]} singletons.")


if __name__ == '__main__':
    main()

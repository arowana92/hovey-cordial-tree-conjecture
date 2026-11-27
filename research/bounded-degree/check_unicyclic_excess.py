"""Construct edge replacements and audit the moments on the resulting bounded-degree graph."""
from collections import Counter
from math import gcd
from random import Random

from check import adjacency
from check_excess import choose_variables, difference, expression, match
from check_unicyclic_core import inspect
from unicyclic_core import core


def redistribute(parent,cap,rng):
    # The cycle starts with vertex 0; all other parents precede their children.
    k = len(parent)
    children = [[] for _ in parent]
    for i,p in enumerate(parent):
        children[p].append(i)
    leaves = [i for i,group in enumerate(children) if not group][:2]
    assert len(leaves)==2
    roots = {0}
    for group in children:
        preferred = sorted(group,key=lambda i:i not in leaves)
        roots.update(preferred[cap-1:])
    blocked = roots|{parent[i] for i in roots}|set(leaves)
    extra = 0
    for i,p in enumerate(parent):
        if i not in blocked and p not in blocked:
            roots.add(i)
            blocked.update((i,p))
            extra += 1
            if extra==5:
                break
    assert extra==5
    fixed = roots|{parent[i] for i in roots}
    kept = [(p,i) for i,p in enumerate(parent) if i not in roots]
    tree = adjacency(k,kept)
    marked = fixed|set(leaves)
    unavailable = marked.union(*(tree[i] for i in marked))
    pools = {r:[] for r in roots}
    component = {}
    for i,p in enumerate(parent):
        r = i if i in roots else component[p]
        component[i] = r
        if i not in unavailable:
            pools[r].append(i)
            unavailable.update(tree[i])
    order = sorted(roots,key=lambda r:(-len(pools[r]),r))
    matching = match(order,parent)
    forms = {v:expression((v,1)) for v in fixed}
    weights = {r:expression((r,1),(parent[r],1)) for r in roots}
    sites = pools[order[0]][:]
    wires = []
    for i,r in enumerate(order):
        site = sites.pop()
        forms[site] = difference(weights[matching[r]],forms[r])
        wires.append((site,r))
        if i:
            sites.extend(pools[r])
    auxiliary = kept+wires
    neighbors = adjacency(k,auxiliary)
    d = Counter(len(row) for row in neighbors if len(row)>=2).most_common(1)[0][0]
    g = gcd(k,d-1)
    edge_forms = list(weights.values())+[expression((v,1),(p,1))
                                         for p,v in kept if p in fixed and v in fixed]
    evaluate = choose_variables(list(forms.values()),edge_forms,k//g,rng)
    pins = {i:g*evaluate(form) for i,form in forms.items()}
    return auxiliary,len(kept),pins,leaves,roots,g


def check(parent,cap,rng):
    n = len(parent)
    edges,cut,pins,leaves,roots,g = redistribute(parent,cap,rng)
    assert len(edges)==n and len({frozenset(e) for e in edges})==n
    assert all(a!=b for a,b in edges)
    graph = adjacency(n,edges)
    assert max(map(len,graph))<=cap+1
    # Independently remove the designated closing edge, verify a spanning tree.
    opened = adjacency(n,edges[:cut]+edges[cut+1:])
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for u in opened[v]:
            if u not in seen:
                seen.add(u)
                stack.append(u)
    assert len(seen)==n
    labels = core(n,edges,cut,pins,leaves)
    inspect(n,edges,cut,labels)
    assert all(labels[i]==a for i,a in pins.items())
    before = [(labels[r]+labels[parent[r]])%n for r in roots]
    after = [(labels[a]+labels[b])%n for a,b in edges[cut:]]
    assert Counter(before)==Counter(after)
    assert {frozenset(e) for e in edges[:cut]}=={frozenset((i,p)) for i,p in enumerate(parent) if i not in roots}
    return len(roots),len(labels),g


def main():
    rng = Random(25091991)
    tests = largest = maximum = nonunit = 0
    for n in (501,576,729,900,1024,1600):
        for c in (3,4,23,n//2):
            for cap in (3,4,5):
                parent = [(i-1)%c for i in range(c)]+[i-1 for i in range(c,n)]
                # Large degrees on the cycle and at successive adjacent tail hubs.
                for start,hub,count in ((c+1,0,12),(c+15,c+1,10),(c+31,c+15,12)):
                    for i in range(start,start+count):
                        parent[i] = hub
                q,size,g = check(parent,cap,rng)
                largest = max(largest,q)
                maximum = max(maximum,size)
                nonunit += g>1
                tests += 1
        if n%2==0:
            c = n//2
            # Mostly degree three: the abundant coefficient d-1 shares a factor with n.
            parent = [(i-1)%c for i in range(c)]+list(range(c))
            for i in range(c+1,c+15):
                parent[i] = 0
            q,size,g = check(parent,4,rng)
            assert g==2
            nonunit += 1
            tests += 1
    print('redistributed cores',tests,'maximum cut edges',largest,'largest core',maximum,
          'nonunit coefficient cases',nonunit)


if __name__=='__main__':
    main()

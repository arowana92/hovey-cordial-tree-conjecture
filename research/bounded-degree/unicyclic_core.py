"""Small prescribed rainbow cores for bounded-degree unicyclic graphs."""
from collections import Counter
from math import gcd


def core(k,edges,cut,pins=None,spare_leaves=None,buffer_degree=None,
         *, absent=None, forbidden_vertex=None, holes=()):
    """Return a partial labeling satisfying the two embedding moments.

    With cut=None the active graph is a tree. Its palettes may omit one
    vertex label and the corresponding number of edge colors. Otherwise
    cut indexes the edge to open in the spanning unicyclic graph. The theorem
    guarantees room for these choices at sufficiently large orders.
    """
    neighbors = [set() for _ in range(k)]
    for a,b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    deg = [len(row) for row in neighbors]
    opened = set(edges[cut]) if cut is not None else set()
    active = [i for i in range(k) if i!=absent]
    leaves = [i for i in range(k) if deg[i]==1]
    if len(leaves)<2:
        raise ValueError('expected at least two leaves')
    p,q = leaves[:2] if spare_leaves is None else spare_leaves
    pins = {} if pins is None else pins
    assert p in leaves and q in leaves and p!=q and p not in pins and q not in pins
    marked = set(pins)|opened|{p,q}
    tree_degree = [d-int(i in opened) for i,d in enumerate(deg)]
    for degree in sorted({tree_degree[i] for i in active}):
        group = [i for i in active if tree_degree[i]==degree]
        inside = sum(i in marked for i in group)
        rest = [i for i in group if i not in marked]
        need = max(0,6-inside)
        marked.update(rest if len(rest)-need<6 else rest[:need])

    d = buffer_degree or Counter(x for x in deg if x>=2).most_common(1)[0][0]
    outside = [i for i in range(k) if deg[i]==d and i not in marked
               and neighbors[i].isdisjoint(marked)]
    y = outside[0]
    z = next(i for i in outside[1:] if i not in neighbors[y])

    labels = {}
    used = set() if forbidden_vertex is None else {forbidden_vertex}
    weights = set(holes)

    def weight_list(i,a):
        return [(a+labels[j])%k for j in neighbors[i] if j in labels]

    def assign(i,a):
        weights.update(weight_list(i,a))
        labels[i] = a
        used.add(a)

    modulus = d-1
    g = gcd(k,modulus)
    for i,a in pins.items():
        assert a not in used and weights.isdisjoint(weight_list(i,a))
        assign(i,a)
    for i in sorted(marked-{p,q}-set(pins)):
        a = next(a for a in range(0,k,g) if a not in used
                 and weights.isdisjoint(weight_list(i,a)))
        assign(i,a)
    total = sum((deg[i]-1)*a for i,a in labels.items())
    difference = (forbidden_vertex or 0)-sum(holes)-total
    assert difference%g==0
    pair_sum = (difference//g)*pow(modulus//g,-1,k//g)%(k//g)
    a = next(a for a in range(k) if a not in used and (pair_sum-a)%k not in used
             and a!=(pair_sum-a)%k)
    assign(y,a)
    assign(z,(pair_sum-a)%k)
    pair_sum = (k*(k-1)//2-(forbidden_vertex or 0)-sum(labels.values()))%k
    for a in range(k):
        b = (pair_sum-a)%k
        if a==b or a in used or b in used:
            continue
        new = weight_list(p,a)+weight_list(q,b)
        if len(set(new))==len(new) and weights.isdisjoint(new):
            assign(p,a)
            assign(q,b)
            return labels
    raise ValueError('insufficient space for two leaves')

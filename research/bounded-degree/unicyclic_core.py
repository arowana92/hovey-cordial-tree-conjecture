"""Small prescribed rainbow cores for bounded-degree unicyclic graphs."""
from collections import Counter


def core(k,edges,cut):
    """Return a partial labeling satisfying the two embedding moments.

    Edges are pairs on range(k), and cut is a cycle-edge index. The theorem
    guarantees room for these choices at sufficiently large orders.
    """
    neighbors = [set() for _ in range(k)]
    for a,b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    deg = [len(row) for row in neighbors]
    u,v = edges[cut]
    leaves = [i for i in range(k) if deg[i]==1]
    if len(leaves)<2:
        raise ValueError('expected at least two leaves')
    p,q = leaves[:2]
    marked = {u,v,p,q}
    tree_degree = [d-int(i in (u,v)) for i,d in enumerate(deg)]
    for degree in sorted(set(tree_degree)):
        group = [i for i in range(k) if tree_degree[i]==degree]
        inside = sum(i in marked for i in group)
        rest = [i for i in group if i not in marked]
        need = max(0,6-inside)
        marked.update(rest if len(rest)-need<6 else rest[:need])

    d = Counter(x for x in deg if x>=2).most_common(1)[0][0]
    outside = [i for i in range(k) if deg[i]==d and i not in marked
               and neighbors[i].isdisjoint(marked)]
    y = outside[0]
    z = next(i for i in outside[1:] if i not in neighbors[y])

    labels = {}
    used = set()
    weights = set()

    def weight_list(i,a):
        return [(a+labels[j])%k for j in neighbors[i] if j in labels]

    def assign(i,a):
        weights.update(weight_list(i,a))
        labels[i] = a
        used.add(a)

    modulus = d-1
    for i in sorted(marked-{p,q}):
        a = next(a for a in range(0,k,modulus) if a not in used
                 and weights.isdisjoint(weight_list(i,a)))
        assign(i,a)
    total = sum((deg[i]-1)*a for i,a in labels.items())
    assert total%modulus==0
    pair_sum = (-total//modulus)%k
    a = next(a for a in range(k) if a not in used and (pair_sum-a)%k not in used
             and a!=(pair_sum-a)%k)
    assign(y,a)
    assign(z,(pair_sum-a)%k)
    pair_sum = (k*(k-1)//2-sum(labels.values()))%k
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

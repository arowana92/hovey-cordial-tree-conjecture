"""Prescribed root and omitted edge color for a tree with small total degree excess."""
from collections import Counter
from functools import reduce
from math import gcd

from check import adjacency
from check_excess import expression
from multiport import lift_marks,neighborhood,residue_sums
from port_degree_reduction import reduce_degree
from unicyclic_core import core


def path_case(k,edges,graph,root,tip,gap):
    end = (sum(range(k))+gap)%k
    if not end: return None
    labels = {root:0,tip:end}
    blocked = neighborhood(graph,labels,1)
    spare = []
    for v in range(k):
        if len(graph[v])==2 and v not in blocked:
            spare.append(v)
            blocked.update(graph[v])
            if len(spare)==6: break
    assert len(spare)==6
    used = {0,end}
    for v in spare[:4]:
        labels[v] = next(x for x in range(k) if x not in used)
        used.add(labels[v])
    total = sum(range(k))-sum(labels.values())
    x = next(x for x in range(k) if x not in used and (total-x)%k not in used and (total-x)%k!=x)
    labels[spare[4]],labels[spare[5]] = x,(total-x)%k
    return edges,labels


def build(edges,root,gap,degree_bound,rng):
    """Normalize the desired root label to zero; gap is in those coordinates."""
    k = len(edges)+1
    adj = adjacency(k,edges)
    c = [len(row)-1 for row in adj]
    leaves = [i for i in range(k) if c[i]==0 and i!=root]
    if len(leaves)==1:
        return path_case(k,edges,adj,root,leaves[0],gap)
    h = reduce(gcd,(c[i] for i in range(k) if i!=root),k)
    if gap%h: return None
    d = Counter(len(row) for row in adj if 2<=len(row)<=degree_bound).most_common(1)[0][0]
    g = gcd(k,d-1)
    reps = {b%g:i for i,b in enumerate(c) if i!=root and b%g}
    tree,base,sites = reduce_degree(edges,set(reps.values())|{root},root=root,
                                    degree_bound=degree_bound,reserved=leaves[:2],site_degree=d)
    bfs = [root]
    index = {root:-1}
    for v in bfs:
        for w in sorted(adj[v]):
            if w not in index:
                index[w] = len(bfs)
                bfs.append(w)
    residues = dict.fromkeys(base,0)
    residues.update(dict(zip(reps.values(),residue_sums(g,reps,-gap))))
    forms = {v:expression((index[v],1),constant=residues[v]) for v in base if v!=root}
    forms[root] = {}
    for site,(a,b,r) in sites.items():
        forms[site] = expression(*forms[a].items(),*forms[b].items(),*((i,-n) for i,n in forms[r].items()))
    sums = [expression(constant=gap)]
    sums += [expression(*forms[a].items(),*forms[b].items()) for a,b in tree if a in forms and b in forms]
    pins = lift_marks(k,g,[index[v] for v in base if v!=root],forms,(list(forms.values()),sums),rng)
    labels = core(k,tree,None,pins,leaves[:2],d,holes=[gap])
    return tree,labels

"""Embedding core for a unicyclic graph with sparse offsets and degree excess."""
from collections import Counter, deque
from functools import reduce
from math import gcd

from check import adjacency
from check_excess import choose_variables, expression
from multiport import residue_sums
from partial_gap import build
from sparse_offsets import cap_tree, edge, move_pairs


def cycle_edge(graph):
    degrees = list(map(len, graph))
    ends = deque(v for v,d in enumerate(degrees) if d==1)
    while ends:
        v = ends.popleft()
        degrees[v] = 0
        for w in graph[v]:
            if degrees[w]:
                degrees[w] -= 1
                if degrees[w]==1:
                    ends.append(w)
    return next(edge(v,w) for v,row in enumerate(graph) if degrees[v]
                for w in sorted(row) if degrees[w])


def construct(edges, offsets, rng, cap=3):
    k = len(edges)
    graph = adjacency(k,edges)
    off = {edge(a,b): x%k for (a,b),x in offsets.items() if x%k}
    leaves = [v for v,row in enumerate(graph) if len(row)==1]
    correction = (sum(range(k))+sum(off.values()))%k
    if not leaves and correction:
        return None
    if len(leaves)==1 and not correction:
        return None
    if len(leaves)>=2 and sum(off.values())%reduce(gcd,(len(row)-1 for row in graph),k):
        return None
    closing = cycle_edge(graph)
    tree = [e for e in edges if edge(*e)!=closing]
    tree_off = {e:x for e,x in off.items() if e!=closing}
    tree_graph = adjacency(k,tree)
    main,remaining = cap_tree(tree_graph,tree_off,cap)
    fixed = {v for e in main for v in e} | set(closing)
    free = [v for v in leaves if v not in fixed]
    site_degree = None
    modulus = 1
    residues = {}
    if len(free)>=2:
        site_degree = Counter(len(row) for row in graph if 2<=len(row)<=cap).most_common(1)[0][0]
        modulus = gcd(k,site_degree-1)
        reps = {(len(row)-1)%modulus:v for v,row in enumerate(graph) if (len(row)-1)%modulus}
        residues = dict(zip(reps.values(),residue_sums(modulus,reps,-sum(off.values()))))
        fixed.update(reps.values())
        reserved = free[:2]
        selected = []
    else:
        fixed.update(v for v,row in enumerate(graph) if len(row)!=2)
        reserved = []
        selected = leaves[:2]
    kept,sites,buffers,order = move_pairs(tree,tree_graph,remaining,main,fixed,reserved,site_degree)
    # In the exhausted-degree case private variables have degree two in the
    # original ring and therefore do not enter the eliminated leaf label.
    ordinary = fixed-set(selected)-buffers
    variables = [v for v in order if v in ordinary]+sorted(buffers)
    if len(selected)==2:
        variables.append(selected[0])
    index = {v:i for i,v in enumerate(variables)}
    forms = {v:expression((i,modulus),constant=residues.get(v,0)) for v,i in index.items()}
    if len(selected)==1:
        y = selected[0]
        j = next(v for v,row in enumerate(graph) if len(row)==3)
        z = next(iter(graph[y]))
        if z in graph[j] and (correction+off.get(edge(z,y),0)-off.get(edge(z,j),0))%k==0:
            return None
        forms[y] = expression((index[j],1),constant=correction)
    elif len(selected)==2:
        y = selected[1]
        forms[y] = expression(*[(i,len(graph[v])-2) for v,i in index.items()],
                              constant=correction)

    def weight(pair):
        a,b = pair
        return expression(*forms[a].items(),*forms[b].items(),constant=off.get(edge(a,b),0))

    for s,(pair,r) in sites.items():
        forms[s] = expression(*weight(pair).items(),*((i,-v) for i,v in forms[r].items()))
    weights = [weight((a,b)) for a,b in edges if a in fixed and b in fixed]
    evaluate = choose_variables(list(forms.values()),weights,k,rng)
    pins = {v:evaluate(f) for v,f in forms.items()}
    missing = evaluate(weight(closing))
    labels = build(kept,pins,missing,rng)
    assert labels is not None
    return kept,closing,missing,pins,labels

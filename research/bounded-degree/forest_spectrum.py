"""Construct the auxiliary embedding for a prescribed gap on a rooted forest."""
from collections import Counter
from functools import reduce
from math import gcd

from check import adjacency
from check_excess import expression
from excess_pins import build as complete_tree
from multiport import lift_marks, residue_sums
from partial_gap import groups


def weight_forms(parents,boundary,pins,k):
    # Constants and free vertex names determine which collisions are forced.
    forms = [expression(constant=pins[v]) if v in pins else expression((v,1))
             for v in range(len(parents))]
    weights = []
    for v,p in enumerate(parents):
        w = expression(*forms[v].items(),*forms[p].items()) if p>=0 else expression(
            *forms[v].items(),constant=boundary[v])
        w[-1] = w.get(-1,0)%k
        weights.append(tuple(sorted((i,x) for i,x in w.items() if x)))
    return weights


def build(parents,boundary,pins,gap,bound,rng):
    n = len(parents)
    k = n+1
    roots = sorted(v for v,p in enumerate(parents) if p<0)
    if set(roots)!=set(boundary):
        raise ValueError("boundary labels must name precisely the component roots")
    if len(set(pins.values()))!=len(pins) or any(x<=0 or x>=k for x in pins.values()):
        return None
    weights = weight_forms(parents,boundary,pins,k)
    gap_form = ((-1,gap),) if gap else ()
    if gap_form in weights or len(weights)!=len(set(weights)):
        return None
    edges = [(p,v) for v,p in enumerate(parents) if p>=0]
    graph = adjacency(n,edges)
    children = Counter(p for p in parents if p>=0)
    leaves = [v for v,p in enumerate(parents) if p>=0 and children[v]==0 and v not in pins]
    if len(leaves)<2:
        raise ValueError("expected two free nonroot terminals")
    target = -gap-sum(boundary.values())-sum(children[v]*x for v,x in pins.items())
    h = reduce(gcd,(children[v] for v in range(n) if v not in pins),k)
    if target%h:
        return None
    d = Counter(children[v]+1 for v,p in enumerate(parents)
                if p>=0 and 1<=children[v]<bound).most_common(1)[0][0]
    g = gcd(k,d-1)
    reps = {children[v]%g:v for v in range(n) if v not in pins and children[v]%g}
    fixed = set(roots)|set(pins)|set(reps.values())
    high = {v for v in range(n) if children[v]+1>bound}
    avoid = fixed|high|set(leaves[:2])
    blocked = avoid.union(*(graph[v] for v in avoid))
    clean = []
    for a,b in edges:
        if a not in blocked and b not in blocked:
            clean.append((a,b))
            blocked.update((a,b))
            if len(clean)==len(roots)+4:
                break
    assert len(clean)==len(roots)+4
    cut = set(clean)
    retained = [(a,b) for a,b in edges if (a,b) not in cut]
    capped = adjacency(n,retained)
    special = [(r,(-1,r,boundary[r])) for r in roots]
    special.extend((b,(a,b,0)) for a,b in clean[:2])
    assignments = {}
    paired = {}
    for (r,target_edge),(a,b) in zip(special,clean[2:]):
        assignments[r] = (a,b,0)
        assignments[b] = target_edge
        paired[b] = r
    base = fixed|{v for edge in clean for v in edge}
    unavailable = base|high|set(leaves[:2])
    unavailable = unavailable.union(*(graph[v] for v in unavailable))
    pools = {}
    for r in assignments:
        pools[r] = []
        queue = [r]
        for v in queue:
            queue.extend(w for w in sorted(capped[v]) if parents[w]==v)
            if v not in unavailable and children[v]+1==d:
                pools[r].append(v)
                unavailable.add(v)
                unavailable.update(capped[v])
    order = sorted(assignments,key=lambda r:(-len(pools[r]),r))
    first = order[0]
    if first in paired:
        # Give the dummy vertex a private two-variable sum. The displaced
        # target goes to an extra free root disjoint from its two endpoints.
        j = next(b for a,b in clean[:2] if b!=paired[first])
        assignments[first],assignments[j] = assignments[j],assignments[first]
    residues = dict(zip(reps.values(),residue_sums(g,reps,target)))
    forms = {v:expression(constant=x) for v,x in pins.items()}
    variables = sorted(base-set(pins))
    forms.update({v:expression((v,1),constant=residues.get(v,0)) for v in variables})
    forms[n] = {}
    tree = retained[:]
    available = pools[first][:]
    for r in order:
        a,b,offset = assignments[r]
        old = expression(*forms[b].items(),constant=offset)
        if a>=0:
            old = expression(*old.items(),*forms[a].items())
        endpoint = n if r==first else r
        site = available.pop()
        forms[site] = expression(*old.items(),*((i,-c) for i,c in forms[endpoint].items()))
        tree.append((endpoint,site))
        if r!=first:
            available.extend(pools[r])
    marks = lift_marks(k,g,variables,forms,groups(forms,tree,gap),rng)
    result = complete_tree(tree,marks,gap,bound+2,rng)
    if result is None:
        raise ValueError("auxiliary tree failed the local or moment test")
    final,labels = result
    return tree,final,labels

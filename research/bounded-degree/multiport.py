"""Build a small prescribed embedding for a tree insertion at distinct ports."""
from collections import Counter, defaultdict
from functools import reduce
from itertools import combinations
from math import gcd

from check import adjacency
from check_excess import difference, expression
from unicyclic_core import core


def neighborhood(graph,seeds,radius):
    region = set(seeds)
    for _ in range(radius):
        region.update(set().union(*(graph[v] for v in region)))
    return region


def residue_sums(modulus,coefficients,target):
    """Represent target as a linear combination in the small quotient group."""
    solutions = {0:[]}
    for c in coefficients:
        previous,solutions = solutions,{}
        for total,x in previous.items():
            for b in range(modulus):
                solutions.setdefault((total+c*b)%modulus,x+[b])
    return solutions[target%modulus]


def routing(edges,adj,t,protected,d,*,closed=True):
    """Build t wires on a cut forest, optionally closing a cycle in the first component."""
    k = len(adj)
    unavailable = neighborhood(adj,protected,3)
    pairs = []
    cut_count = t-int(closed)
    for a,b in (edges if cut_count else ()):
        if min(len(adj[a]),len(adj[b]))>=2 and a not in unavailable and b not in unavailable:
            pairs.append((a,b))
            unavailable.update(neighborhood(adj,(a,b),4))
            if len(pairs)==cut_count:
                break
    assert len(pairs)==cut_count
    pair_set = set(pairs)
    kept = [edge for edge in edges if edge not in pair_set]
    forest = adjacency(k,kept)
    around_cut = {v for pair in pairs for v in pair}
    fixed = protected|around_cut
    owner = {}
    anchors = []
    for end in sorted(around_cut):
        if end in owner:
            continue
        root = next(iter(forest[end]))
        assert root not in fixed
        anchors.append(root)
        owner[root] = root
        stack = [root]
        while stack:
            v = stack.pop()
            for u in forest[v]:
                if u not in owner:
                    owner[u] = root
                    stack.append(u)
    if not pairs:
        root = next(v for v in range(k) if v not in unavailable)
        anchors.append(root)
        owner = dict.fromkeys(range(k),root)
    assert len(anchors)==cut_count+1 and len(owner)==k
    unavailable = neighborhood(forest,fixed|set(anchors),1)
    pools = {a:[] for a in anchors}
    for v in range(k):
        if len(adj[v])==d and v not in unavailable:
            pools[owner[v]].append(v)
            unavailable.update(forest[v])
    order = sorted(anchors,key=lambda a:(-len(pools[a]),a))
    available = pools[order[0]][:]
    wires = []
    for j,a in enumerate(order):
        if j or closed:
            wires.append((a,available.pop()))
        if j:
            available.extend(pools[a])
    return pairs,kept,anchors,wires


def lift_marks(k,g,variables,forms,groups,rng):
    # The variables range over a coset of gG. A comparison whose
    # constant is nonzero modulo g is already decided. Otherwise divide by g.
    inequalities = defaultdict(list)
    for group in groups:
        for left,right in combinations(group,2):
            row = difference(left,right)
            constant = row.pop(-1,0)
            if constant%g:
                continue
            if not row:
                assert constant%k, "identical forms in a distinctness constraint"
                continue
            inequalities[max(row)].append((constant//g,row))
    point = {}
    size = k//g
    for i in sorted(variables):
        banned = set()
        for constant,row in inequalities[i]:
            a = row[i]
            rhs = -constant-sum(c*point[v] for v,c in row.items() if v!=i)
            factor = gcd(a,size)
            if rhs%factor==0:
                period = size//factor
                x = (rhs//factor)*pow(a//factor,-1,period)%period
                banned.update(range(x,size,period))
        point[i] = rng.choice([x for x in range(size) if x not in banned])
    return {v:(form.get(-1,0)+g*sum(c*point[i] for i,c in form.items() if i>=0))%k
            for v,form in forms.items()}


def construct(edges,ports,old_labels,deleted,rng):
    k = len(edges)+1
    t = len(ports)
    assert len(set(ports))==t==len(old_labels)==len(deleted)+1 and t>=2
    adj = adjacency(k,edges)
    coefficients = [len(row)-1 for row in adj]
    for v in ports:
        coefficients[v] += 1
    target = sum(deleted)-sum(old_labels)
    divisor = reduce(gcd,coefficients,k)
    if target%divisor:
        return None
    leaves = [i for i,c in enumerate(coefficients) if c==0][:2]
    assert len(leaves)==2
    representatives = {c:i for i,c in enumerate(coefficients) if c}
    protected = set(ports)|set(representatives.values())|set(leaves)
    d = Counter(len(row) for row in adj if len(row)>=2).most_common(1)[0][0]
    g = gcd(k,d-1)
    pairs,kept,anchors,wires = routing(edges,adj,t,protected,d)
    # Base variables are lifted from assigned quotient residues to the full group.
    base_vertices = (set(ports)|set(anchors)|set(representatives.values())|
                     {a for a,b in pairs})
    residues = {i:0 for i in base_vertices}
    fixed_total = sum(coefficients[b]*w for (_,b),w in zip(pairs,deleted))
    values = residue_sums(g,representatives,target-fixed_total)
    residues.update({i:b for i,b in zip(representatives.values(),values)})
    forms = {i:expression((i,1),constant=b) for i,b in residues.items()}
    for (a,b),w in zip(pairs,deleted):
        forms[b] = expression((a,-1),constant=w-residues[a])
    entering = [expression((v,1),constant=a+residues[v]) for v,a in zip(ports,old_labels)]
    for (root,site),v,a in zip(wires,ports,old_labels):
        forms[site] = expression((v,1),(root,-1),constant=a+residues[v]-residues[root])
    sums = entering[:]
    for a,b in kept:
        if a in forms and b in forms:
            sums.append(expression(*forms[a].items(),*forms[b].items()))
    pins = lift_marks(k,g,residues,forms,(list(forms.values()),sums),rng)
    auxiliary = kept+wires
    cut = len(kept)
    labels = core(k,auxiliary,cut,pins,leaves,d)
    return auxiliary,cut,labels,pairs,wires,g

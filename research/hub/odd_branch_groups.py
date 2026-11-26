"""Neutral repeated branches over odd fibers and a sparse two-site certificate."""

from random import Random

from research.check_large_order_subdivision import children
from research.hub.cluster_lift import lift
from research.hub.linear_hub_batches import residual_labels
from research.hub.modular_injection import finish, specialize
from research.hub.polynomial_hub import bottom_fringe
from research.hub.signed_tree import construct as signed
from research.hub.universal_hub import construct as integer


def group_branches(tree,d,protect_four=False):
    kids = children(tree)
    height = [1]*len(tree)
    shape = {}
    codes = {}
    for v in reversed(range(2,len(tree))):
        height[v] += max((height[w] for w in kids[v]),default=0)
        if height[v] < 10:
            key = tuple(sorted(shape[w] for w in kids[v]))
            shape[v] = codes.setdefault(key,len(codes))
    tops = [v for v in range(2,len(tree)) if tree[v] < 2]
    deepest = max(tops,key=height.__getitem__)
    protected = {deepest}
    secondary = [v for v in tops if tree[v] == 1 and kids[v]]
    protected.update(secondary[:2])
    if protect_four and height[deepest] < 5:
        by_shape = {}
        for v in secondary:
            copies = by_shape.setdefault(shape[v],[])
            copies.append(v)
            if len(copies) == 4:
                protected.update(copies)
                break
    waiting = {}
    groups = []
    omitted = set()
    for v in tops:
        if v in protected or height[v] >= 10:
            continue
        batch = waiting.setdefault((tree[v],shape[v]),[])
        batch.append(v)
        if len(batch) == 2*d:
            rows = []
            for root in batch:
                row = [root]
                for p in row:
                    row.extend(sorted(kids[p],key=shape.__getitem__))
                rows.append(row)
                omitted.update(row)
            index = {p:i for i,p in enumerate(rows[0])}
            local = [-1]+[index[tree[p]] for p in rows[0][1:]]
            groups.append((local,rows))
            batch.clear()
    keep = [v for v in range(len(tree)) if v not in omitted]
    index = {v:i for i,v in enumerate(keep)}
    residual = [-1]+[index[tree[v]] for v in keep[1:]]
    return keep,residual,groups,height[deepest]


def construct(core,d,q,second,seed=76539):
    """Sites 0,1 are adjacent. The trimmed core has a nontrivial exterior branch."""
    if d < 3 or d % 2 == 0 or tuple(core[:2]) != (-1,0) or len(core) <= 2:
        raise ValueError("expected an odd divisor and a nonempty two-site exterior")
    k = d*q
    rng = Random(seed)
    keep,residual,groups,depth = group_branches(core,d)
    rem = second % d
    tree = residual+[1]*rem
    kids = children(tree)
    if depth >= 5:
        values,gap,stats = residual_labels(tree,k,rng,{0:0,1:q})
        pending = second-rem
        rounds = stats[0]
    elif sum(bool(kids[v]) for v in kids[1]) >= 2:
        # Start at the fixed secondary site. Its two surviving support children
        # guarantee a fork in this subtree, possibly at the site itself.
        fringe = bottom_fringe(tree,kids,1,height=0)
        values,gap,_,_ = finish(tree,kids,{0:0,1:q},fringe,k,rng)
        pending = second-rem
        rounds = 0
    else:
        quotient_tree = [-1]+[max(0,p-1) for p in residual[2:]]
        x,_,_ = integer(quotient_tree)
        populations = [k-len(residual)-second,second]
        _,values = lift(residual,[0,1],[v % q for v in x],q,d,populations,
                        omit_zero_leaves=True)
        edges = {(values[v]+values[p]) % k for v,p in enumerate(residual+[1]*second) if v}
        gap, = set(values)-edges
        pending = rounds = 0
    labels = dict(zip(keep,values[:len(keep)]))
    extras = values[len(keep):]
    occupied = {x % q for x in values}
    for local,rows in groups:
        template = signed(local)
        forms = {(sign,j):(sign*x,0) for sign in (-1,1) for j,x in enumerate(template)}
        scale,projection = specialize(forms,occupied,q,rng)
        occupied.update(projection.values())
        for i,row in enumerate(rows):
            sign = 1 if i < d else -1
            for v,x in zip(row,template):
                labels[v] = (sign*scale*x+(i % d)*q) % k
    for fiber in range(q):
        if not pending:
            break
        if fiber not in occupied:
            extras.extend(fiber+j*q for j in range(d))
            pending -= d
    assert pending == 0 and len(extras) == second
    return [labels[v] for v in range(len(core))]+extras,gap,(depth,len(groups),rounds)

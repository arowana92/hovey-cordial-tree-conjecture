"""Neutral branches at the involution and bounded two-site completions."""

from random import Random

from research.check_large_order_subdivision import children
from research.hub.cluster_lift import lift
from research.hub.linear_hub_batches import residual_labels
from research.hub.modular_injection import bulk_forms, finish, specialize
from research.hub.odd_branch_groups import group_branches
from research.hub.polynomial_hub import bottom_fringe
from research.hub.signed_tree import BLOCKS, construct as signed, decomposition
from research.hub.universal_hub import construct as integer


def packet(branch,k,occupied,rng):
    """Return twelve copies at k/2, adding both signs of every chosen residue."""
    p = k//2
    tree = [-1]
    for _ in range(6):
        start = len(tree)
        tree.extend([0]+[start+i for i in branch[1:]])
    initial,blocks = decomposition(children(tree),0)
    assert k % 2 == 0 and initial == [0]
    labels = {0:p}
    occupied.update((0,p))
    for kind,nodes in blocks:
        parent = labels[tree[nodes[0]]]
        _,entries,_ = BLOCKS[kind]
        forms = {(v,sign):(sign*a,sign*b*parent)
                 for v,(a,b) in zip(nodes,entries) for sign in (-1,1)}
        _,row = specialize(forms,occupied,k,rng)
        occupied.update(row.values())
        labels.update((v,row[v,1]) for v in nodes)
    m = len(branch)
    return [[(sign*labels[v]) % k for v in range(1+i*m,1+(i+1)*m)]
            for sign in (1,-1) for i in range(6)]


def four_roots(kids):
    def code(v):
        return tuple(sorted(code(w) for w in kids[v]))
    seen = {}
    for v in kids[1]:
        if kids[v]:
            group = seen.setdefault(code(v),[])
            group.append(v)
            if len(group) == 4:
                return group
    return None


def spine(kids,v):
    """A caterpillar arm with its terminal leaves at each spine position."""
    path,sides = [],[]
    while kids[v]:
        path.append(v)
        continuing = [w for w in kids[v] if kids[w]]
        if len(continuing) > 1:
            return None
        child = continuing[0] if continuing else kids[v][0]
        sides.append([w for w in kids[v] if w != child])
        v = child
    return path+[v],sides


def shallow(tree,roots,k,rng):
    p = k//2
    kids = children(tree)
    arms = [spine(kids,v) for v in roots[:3]]
    if arms[0] is None:
        fringe = bottom_fringe(tree,kids,roots[0],height=0)
        assert fringe[1] > 1
        values,gap,_,_ = finish(tree,kids,{0:0,1:p},fringe,k,rng)
        return values,gap,'fork'
    height = len(arms[0][0])
    assert 2 <= height <= 4
    virtual = 0
    if height == 4:
        arms = arms[:1]
        a,b,c = arms[0][1]
        virtual = min(len(a),max(0,len(c)-len(b)))
    removed = {v for path,sides in arms for v in path}
    removed.update(v for _,sides in arms for leaves in sides for v in leaves)
    augmented = tree+[1]*virtual
    bulk,(s,offset),_ = bulk_forms(augmented,children(augmented),{0:0,1:p},
                                   removed,k,rng,guard=roots[3])
    assert s >= 2
    virtual_forms = [bulk.pop(v) for v in range(len(tree),len(augmented))]
    assert all(j == 1 and c not in (0,p) for j,c in virtual_forms)
    margin = 10*(len(tree)+1)*(s+1)

    def local(x):
        L = s*x+offset
        row = {}
        unpaired = []
        pairs = []
        if height == 4:
            path,(a,b,c) = arms[0]
            row.update(zip(path,(-p-L,-L,L,-p-2*L)))
            common = min(len(b),len(c))
            pairs.extend(zip(c[:common],b[:common]))
            for v,w,(j,t) in zip(c[common:],a,virtual_forms):
                row[v] = j*x+t
                row[w] = row[v]+L
            unpaired.extend(b[common:]+c[common+virtual:]+a[virtual:])
        else:
            T = -margin*x
            root_values = (p-L,-L,L)
            children_values = (p+L,T+L,T)
            for i,(path,_) in enumerate(arms):
                row[path[0]],row[path[1]] = root_values[i],children_values[i]
            r0,r1,r2 = [entry[1][0] for entry in arms]
            pairs.extend(zip(r2,r1))
            if height == 3:
                h0,h1,h2 = [path[2:]+sides[1] for path,sides in arms]
                # Both large negative parents move the gap up before the
                # smaller remaining parents, which all have the same sign.
                unpaired.extend(h1+h2)
                common = min(len(r0),len(h0))
                pairs.extend(zip(h0[:common],r0[:common]))
                unpaired.extend(r0[common:]+h0[common:])
            else:
                unpaired.extend(r0)
        gap = x
        for v in unpaired:
            gap -= row[tree[v]]
            row[v] = gap
        for i,(v,w) in enumerate(pairs):
            start = (margin**2+(2*s+2)*i)*x
            row[v] = start
            row[w] = start+row[tree[v]]
        return row,gap

    first,g0 = local(0)
    second,g1 = local(1)
    forms = dict(bulk)
    forms.update({v:(second[v]-y,y % k) for v,y in first.items()})
    x,row = specialize(forms,set(),k,rng)
    return [row[v] for v in range(len(tree))],((g1-g0)*x+g0) % k,f'height-{height}'


def construct(core,q,second,seed=49119):
    """Injective sparse core at 0 and q modulo 2q, including leaves at q."""
    k = 2*q
    keep,residual,groups,depth = group_branches(core,6,protect_four=True)
    rng = Random(seed)
    rem = second % 2
    tree = residual+[1]*rem
    roots = four_roots(children(tree)) if depth < 5 else None
    if depth >= 5:
        values,gap,_ = residual_labels(tree,k,rng,{0:0,1:q})
        mode = 'deep'
    elif roots:
        values,gap,mode = shallow(tree,roots,k,rng)
    else:
        contracted = [-1]+[max(0,p-1) for p in residual[2:]]
        x,_,_ = integer(contracted)
        _,values = lift(residual,[0,1],[v % q for v in x],q,2,
                        [k-len(residual)-second,second],omit_zero_leaves=True)
        edges = {(values[v]+values[p]) % k for v,p in enumerate(residual+[1]*second) if v}
        gap, = set(values)-edges
        mode = 'bounded'
    labels = dict(zip(keep,values[:len(keep)]))
    extras = values[len(keep):]
    occupied = set(values)
    for branch,rows in groups:
        if core[rows[0][0]] == 1:
            copies = packet(branch,k,occupied,rng)
            for ids,copy in zip(rows,copies):
                labels.update(zip(ids,copy))
        else:
            template = signed(branch)
            for left,right in zip(rows[::2],rows[1::2]):
                forms = dict(zip(left,((v,0) for v in template)))
                forms.update(zip(right,((-v,0) for v in template)))
                _,copy = specialize(forms,occupied,k,rng)
                occupied.update(copy.values())
                labels.update(copy)
    pending = second-len(extras)
    for j in range(q):
        if not pending:
            break
        if j not in occupied and j+q not in occupied:
            extras.extend((j,j+q))
            pending -= 2
    assert not pending
    return [labels[v] for v in range(len(core))]+extras,gap,mode

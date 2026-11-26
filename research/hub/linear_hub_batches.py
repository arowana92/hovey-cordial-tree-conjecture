"""A linear-in-order modular threshold for bounded nonroot degree."""

from random import Random

from research.check_large_order_subdivision import children
from research.hub.modular_injection import finish, place_cycle, specialize, walks
from research.hub.polynomial_hub import bottom_fringe, construct as integer_certificate
from research.hub.signed_tree import construct as signed_certificate
from research.large_order_gap_paths import gap_path


def paired_branches(tree):
    """Pair equal short root branches and retain the identifications of their vertices."""
    kids = children(tree)
    depth = [0]*len(tree)
    shape = [None]*len(tree)
    types = {}
    for v in reversed(range(1,len(tree))):
        depth[v] = 1+max((depth[w] for w in kids[v]),default=0)
        if depth[v]<=15:
            key = tuple(sorted(shape[w] for w in kids[v]))
            shape[v] = types.setdefault(key,len(types))
    waiting = {}
    pairs = []
    omitted = set()
    for root in kids[0]:
        code = shape[root]
        if code is None:
            continue
        if code not in waiting:
            waiting[code] = root
            continue
        roots = [waiting.pop(code),root]
        rows = []
        for start in roots:
            row = [start]
            for v in row:
                row.extend(sorted(kids[v],key=shape.__getitem__))
            rows.append(row)
            omitted.update(row)
        index = {v:i for i,v in enumerate(rows[0])}
        local = tuple([-1]+[index[tree[v]] for v in rows[0][1:]])
        pairs.append((local,*rows))
    keep = [v for v in range(len(tree)) if v not in omitted]
    index = {v:i for i,v in enumerate(keep)}
    residual = [-1]+[index[tree[v]] for v in keep[1:]]
    return keep,residual,pairs


def attach_batch(tree, labels, occupied, ordinary, path, k, rng):
    """Cancel the discrepancy from the ordinary forest on the last seven path sites."""
    nodes = set(ordinary)|set(path[:3])
    group = sorted(v for v in nodes if tree[v] in labels)
    cycles,residual,delta = walks(group,tree,labels,k)
    forms = {v:(1,a) for v,a in residual}
    used = {delta}|{b for _,b in forms.values()}
    for cycle in cycles:
        row = place_cycle(cycle,used,k,rng)
        forms.update((v,(1,a)) for v,a in row.items())
    terminal = (1,delta)
    for v in sorted(nodes-forms.keys()):
        pa,pb = forms[tree[v]]
        forms[v] = terminal
        a,b = terminal
        terminal = a+pa,(b+pb)%k
    parent = forms[path[2]]
    assert 1<parent[0]<terminal[0]
    low = gap_path(parent[1],0,terminal[1])
    high = gap_path(sum(parent),1,sum(terminal))
    forms.update((v,(b-a,a%k)) for v,a,b in zip(path[3:],low,high))
    assert len(set(forms.values()))==len(forms)
    _,row = specialize(forms,occupied,k,rng)
    labels.update(row)
    occupied.update(row.values())
    return len(row),len(cycles)


def residual_labels(tree, k, rng):
    kids = children(tree)
    depth = [0]*len(tree)
    for v,p in enumerate(tree[1:],1):
        depth[v] = depth[p]+1
    tip = max(range(len(tree)),key=depth.__getitem__)
    if depth[tip]<=4:
        values,gap,_ = integer_certificate(tree)
        reduced = [x%k for x in values]
        if len(set(reduced))!=len(tree):
            raise ValueError("bounded residual certificate collides")
        return reduced,gap%k,(0,0,0,len(tree))

    fringe = bottom_fringe(tree,kids,tip,height=4)
    eligible = [True]*len(tree)
    eligible[fringe[1]] = False
    height = [1]*len(tree)
    below = [None]*len(tree)
    for v,p in enumerate(tree[1:],1):
        eligible[v] = eligible[v] and eligible[p]
    for v in reversed(range(1,len(tree))):
        p = tree[v]
        if eligible[v] and height[v]+1>height[p]:
            height[p],below[p] = height[v]+1,v
    short,tall = [],[]

    def expose(v):
        if eligible[v]:
            (short if height[v]<10 else tall).append(v)

    for v in kids[0]:
        expose(v)
    labels = {0:0}
    occupied = {0}
    rounds = largest = cycles = 0
    while tall:
        start = tall.pop()
        path = [start]
        while len(path)<10:
            path.append(below[path[-1]])
        ordinary = short
        short = []
        for v in ordinary:
            ordinary.extend(w for w in kids[v] if eligible[w])
        n,c = attach_batch(tree,labels,occupied,ordinary,path,k,rng)
        rounds += 1
        largest = max(largest,n)
        cycles += c
        path_set = set(path)
        for v in path:
            for w in kids[v]:
                if w not in path_set:
                    expose(w)
    final_size = len(tree)-len(labels)
    values,gap,_,_ = finish(tree,kids,labels,fringe,k,rng,max_levels=14)
    return values,gap,(rounds,largest,cycles,final_size)


def construct(tree, k, seed=1952, *, nonzero_gap=False):
    if not tree or tree[0]!=-1 or any(not 0<=p<v for v,p in enumerate(tree[1:],1)):
        raise ValueError("need a parent-before-child tree")
    if k<len(tree):
        raise ValueError("modulus smaller than tree")
    rng = Random(seed)
    keep,residual,pairs = paired_branches(tree)
    if nonzero_gap and not any(p > 0 for p in residual):
        if not any(p > 0 for p in tree):
            raise ValueError("a star at zero must omit zero")
        # Retain one nontrivial pair so the bounded residual uses weight zero.
        j = next(j for j,(local,_,_) in enumerate(pairs) if len(local) > 1)
        _,left,right = pairs.pop(j)
        keep = sorted(keep+left+right)
        index = {v:i for i,v in enumerate(keep)}
        residual = [-1]+[index[tree[v]] for v in keep[1:]]
    values,gap,stats = residual_labels(residual,k,rng)
    assert not nonzero_gap or gap != 0
    labels = dict(zip(keep,values))
    occupied = set(values)
    templates = {}
    for local,left,right in pairs:
        if local not in templates:
            templates[local] = signed_certificate(local)
        forms = {v:(s,0) for v,s in zip(left,templates[local])}
        forms.update((v,(-s,0)) for v,s in zip(right,templates[local]))
        _,row = specialize(forms,occupied,k,rng)
        labels.update(row)
        occupied.update(row.values())
    return [labels[v] for v in range(len(tree))],gap,(*stats,len(pairs))

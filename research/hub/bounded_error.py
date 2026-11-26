"""Construct order-equals-modulus labelings with a bounded number of corrected weights."""

from collections import defaultdict, deque
from random import Random

from research.check_large_order_subdivision import children
from research.hub.linear_hub_batches import attach_batch
from research.hub.modular_injection import candidates
from research.hub.signed_tree import construct as signed


def site_cells(core,sites):
    graph = [[] for _ in core]
    for v,p in enumerate(core[1:],1):
        graph[v].append(p)
        graph[p].append(v)
    owner = {v:v for v in sites}
    parent = {}
    ordered = {v:[v] for v in sites}
    queue = deque(sites)
    while queue:
        v = queue.popleft()
        for w in graph[v]:
            if w in owner:
                continue
            owner[w] = owner[v]
            parent[w] = v
            ordered[owner[v]].append(w)
            queue.append(w)
    for site,ids in ordered.items():
        index = {v:j for j,v in enumerate(ids)}
        yield site,ids,[-1]+[index[parent[v]] for v in ids[1:]]


def packet_layout(tree):
    kids = children(tree)
    heights = [1]*len(tree)
    shape = {}
    codes = {}
    for v in reversed(range(1,len(tree))):
        heights[v] += max((heights[w] for w in kids[v]),default=0)
        if heights[v] < 10:
            key = tuple(sorted(shape[w] for w in kids[v]))
            shape[v] = codes.setdefault(key,len(codes))
    groups = defaultdict(list)
    for v in kids[0]:
        if v in shape:
            groups[shape[v]].append(v)
    packets = []
    for group in groups.values():
        w = (len(group)-2)//4*2+1
        if w <= 0:
            continue
        rows = []
        for v in group[:2*w]:
            row = [v]
            for x in row:
                row.extend(sorted(kids[x],key=shape.__getitem__))
            rows.append(row)
        index = {v:j for j,v in enumerate(rows[0])}
        branch = [-1]+[index[tree[v]] for v in rows[0][1:]]
        packets.append((branch,rows))
    return kids,heights,packets


def place_packet(branch,rows,k,blocked,rng,*,accept=None):
    w = len(rows)//2
    m = w//2
    template = signed(branch)
    for scale in candidates(k,rng):
        present = {(sign*x*scale+j) % k for sign in (-1,1) for x in template
                   for j in range(-m,m+1)}
        if len(present) != len(rows)*len(branch) or not blocked.isdisjoint(present):
            continue
        starts = [(sign*scale*template[0]-m) % k for sign in (-1,1)]
        if accept is None or accept(present,starts,w):
            break
    else:
        raise ValueError("no available packet placement in this palette")
    labels = {}
    for j,row in enumerate(rows):
        sign = 1 if j < w else -1
        offsets = [j % w-m]
        for p in branch[1:]:
            offsets.append((offsets[p]+2*m) % w-m)
        for v,x,offset in zip(row,template,offsets):
            labels[v] = (sign*scale*x+offset) % k
    blocked.update(present)
    return labels


def construct(core,sites,counts,k,reserve,seed=3691):
    """The reserve is a union of intervals for leaves at the nonzero sites."""
    if len(core)+sum(counts) != k:
        raise ValueError("the expanded order must equal the modulus")
    rng = Random(seed)
    sites_counts = sorted(zip(sites,counts),key=lambda pair:-pair[1])
    sites,counts = map(list,zip(*sites_counts))
    digits = {v:i for i,v in enumerate(sites)}
    reserve = set(reserve)-set(digits.values())
    if len(reserve) < sum(counts[1:]):
        raise ValueError("reserve too small for the nonzero leaf sites")
    blocked = reserve|set(digits.values())
    cells = []
    budget = len(sites)-1
    stats = [0,0,0]
    for site,ids,tree in site_cells(core,sites):
        kids,heights,packets = packet_layout(tree)
        local = {0:digits[site]}
        for branch,rows in packets:
            local.update(place_packet(branch,rows,k,blocked,rng))
            budget += 2*digits[site]
            stats[0] += 1
        cells.append((ids,tree,kids,heights,local))

    labels = [None]*len(core)
    available = (x for x in range(k) if x not in blocked)
    for ids,tree,kids,heights,local in cells:
        short,tall = [],[]

        def expose(v):
            (short if heights[v]<10 else tall).append(v)

        for v in kids[0]:
            if v not in local:
                expose(v)
        while tall:
            path = [tall.pop()]
            while len(path) < 10:
                path.append(max(kids[path[-1]],key=heights.__getitem__))
            ordinary,short = short,[]
            for v in ordinary:
                ordinary.extend(kids[v])
            attach_batch(tree,local,blocked,ordinary,path,k,rng)
            for v in path:
                for w in kids[v]:
                    if w not in path:
                        expose(w)
            stats[1] += 1
        for v in short:
            local[v] = next(available)
            blocked.add(local[v])
            short.extend(kids[v])
            budget += 1
            stats[2] += 1
        for j,v in enumerate(ids):
            labels[v] = local[j]

    parents = list(core)
    free = iter(sorted(reserve))
    for site,count in zip(sites[1:],counts[1:]):
        previous = None
        for _ in range(count):
            x = next(free)
            if previous is None or x != previous+1:
                budget += digits[site]
            previous = x
            labels.append(x)
            parents.append(site)
    rest = sorted(set(range(k))-set(labels))
    assert len(rest) == counts[0]
    labels.extend(rest)
    parents.extend([sites[0]]*len(rest))
    return parents,labels,budget,stats

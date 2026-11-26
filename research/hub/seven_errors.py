"""Sparse rooted labeling with at most seven protected surplus weights."""

from random import Random

from research.check_large_order_subdivision import children
from research.hub.linear_hub_batches import attach_batch
from research.hub.modular_injection import advance, candidates, place_cycle, walks
from research.hub.pendant_repair import bridge
from research.large_order_gap_paths import paired_path


def prepare(tree,k,rng):
    """Return an injection, protected (deficit, surplus) pairs, and occupied values."""
    kids = children(tree)
    height = [1]*len(tree)
    below = [None]*len(tree)
    for v in reversed(range(1,len(tree))):
        p = tree[v]
        if height[v]+1>height[p]:
            height[p],below[p] = height[v]+1,v
    labels = {0:0}
    labels.update((v,i) for i,v in enumerate(kids[0],1))
    blocked = set(labels.values())
    bills = []
    rounds = levels = 0
    while len(labels)<len(tree):
        front = [v for v,p in enumerate(tree) if v not in labels and p in labels]
        start = next((v for v in front if height[v]>=8),None)
        if start is not None:
            path = [start]
            while len(path)<8:
                path.append(below[path[-1]])
            front.remove(start)
            advance(front,path,tree,labels,blocked,k,rng)
            rounds += 1
            continue
        levels += 1
        cycles,residual,end = walks(front,tree,labels,k)
        if not end:
            for cycle in cycles:
                labels.update(place_cycle(cycle,blocked,k,rng))
            continue
        offsets = dict(residual)
        occupied = set(offsets.values())|{end}
        for cycle in cycles:
            offsets.update(place_cycle(cycle,occupied,k,rng))
        for x in candidates(k,rng):
            t = (x+end)%k
            if t==(-t)%k or (x+2*t)%k==0 or t in blocked or (-t)%k in blocked:
                continue
            row = {v:(x+a)%k for v,a in offsets.items()}
            used = set(row.values())
            if t not in used and (-t)%k not in used and blocked.isdisjoint(used):
                labels.update(row)
                blocked.update(used|{t,(-t)%k})
                bills.append((x,t))
                break
        else:
            raise ValueError("unable to protect the new layer endpoint")
    assert levels<=7
    return labels,bills,blocked,(rounds,levels)


def restore(core,child,k,seed=189):
    """Insert 129 bare internal vertices in the given compressed edge."""
    rng = Random(seed)
    labels,bills,blocked,stats = prepare(core,k,rng)
    start = len(core)
    parent = core[child]
    path = list(range(start,start+129))
    parents = list(core)+[parent]+path[:-1]
    attach_batch(parents,labels,blocked,[],path[:10],k,rng)
    for i in range(7):
        segment = path[10+14*i:24+14*i]
        if i>=len(bills):
            attach_batch(parents,labels,blocked,segment[:4],segment[4:],k,rng)
            continue
        b,t = bills[i]
        p = labels[parents[segment[0]]]
        for z in candidates(k,rng):
            values = paired_path(p,b,t,z,k)
            if len(set(values))==14 and blocked.isdisjoint(values[:7]+values[8:11]+values[12:]):
                labels.update(zip(segment,values))
                blocked.update(values)
                break
        else:
            raise ValueError("no specialization of the paired transfer")
    w = (labels[parent]+labels[child])%k
    values = bridge(labels[path[-22]],labels[child],w,k,blocked,rng)
    labels.update(zip(path[-21:],values))
    parents[child] = path[-1]
    return parents,[labels[v] for v in range(len(parents))],stats,len(bills)

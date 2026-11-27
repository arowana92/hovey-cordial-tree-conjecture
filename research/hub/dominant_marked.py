"""Elongate a marked interval seed with a linear cost at zero and logarithmic cost elsewhere."""

from bisect import bisect_right
from collections import Counter
from random import Random

from research.hub.marked_leaf_blocks import complete, insertion
from research.hub.marked_leaf_geometry import at_target, child_label, pad
from research.hub.two_hub_buffer import insert_neutral
from research.hub.two_hub_contraction import Interval, remove_fillers
from research.hub.two_hubs import edge


def orient(seed, main):
    tree, labels, anchors = seed
    if labels[main]==0:
        return seed
    if labels[main]!=1:
        raise ValueError("a dominant population must have seed label zero or one")
    tree.lo,tree.hi = 1-tree.hi,1-tree.lo
    tree.path = [1-x for x in tree.path]
    tree.edges = {edge(1-p,1-q) for p,q in tree.edges}
    tree.added = [(1-p,1-v) for p,v in tree.added]
    return tree,{v:1-x for v,x in labels.items()},tuple(sorted({1-p for p in anchors}|{0}))


def initial_edge(tree, anchors, p, q):
    """Prepare a bounded negative and positive edge and a second eligible edge p,x."""
    low = child_label(tree,anchors,p,1)
    high = child_label(tree,anchors,q,0)
    x = min(low-2,-abs(p)-2,p+q-high,p+q-2)
    y = p+q-x
    at_target(tree,anchors,p,1,x)
    at_target(tree,anchors,q,0,y)
    tree.edges.remove(edge(p,q))
    tree.edges.add(edge(x,y))
    return x,y


def buffer(tree, anchors, positive, negative, h, capacity):
    parents,slot = insertion(anchors,negative,0)
    initial_x = min(negative-len(parents)-2,positive+negative-tree.hi-1-slot)
    gap = tree.lo-positive-initial_x
    if gap>0:
        pad(tree,anchors,max(2,gap),1)
    return buffer_interval(Interval(tree),parents,slot,positive,negative,h,capacity)


def buffer_interval(iv, parents, slot, positive, negative, h, capacity):
    """Grow a prepared opposite-sign edge from a range-compressed interval."""
    tail = len(parents)-1-slot
    minor = sum(stop-start for p,start,stop in iv.blocks if p)
    original_width = iv.hi-iv.lo+1
    p = positive
    path = [p]
    for moves in range(capacity+1):
        limit = 100*(h+minor+1)
        if moves and moves%6==0 and min(-iv.lo,iv.hi)>=16*limit+4*original_width:
            return iv,path+[negative],limit,moves,minor
        if moves==capacity:
            break
        x = iv.lo-p
        y = p+negative-x
        start = y-slot
        assert start>iv.hi
        iv.fill(0,x+1,iv.lo)
        iv.fill(0,iv.hi+1,start)
        for i,parent in enumerate(parents):
            if i!=slot:
                iv.fill(parent,start+i,start+i+1)
                minor += int(parent!=0)
        iv.lo,iv.hi = x,y+tail
        path.extend((x,y))
        p = y
    raise ValueError("segment too short for this sufficient buffer construction")


def inflate(graph, seed, main, jobs):
    """Insert 2+12n vertices at the first edge, 12n at each subsequent edge."""
    if not jobs:
        raise ValueError("need a distinguished edge")
    tree,labels,anchors = orient(seed,main)
    graph = {v:set(neighbors) for v,neighbors in graph.items()}
    labels = labels.copy()
    jobs = list(jobs)
    u,v,n = jobs[0]
    if not labels[u]:
        u,v = v,u
        jobs[0] = u,v,n
    h = len(graph)+2+12*sum(count for _,_,count in jobs)
    p,q = labels[u],labels[v]
    x,y = initial_edge(tree,anchors,p,q)
    iv,row,limit,moves,minor = buffer(tree,anchors,y,x,h,6*n)
    core = set(labels.values())|set(row)
    original = core.copy()
    forbidden = sorted((a,b) for parent,a,b in iv.blocks if parent)
    starts = [a for a,_ in forbidden]

    def minority(z):
        i = bisect_right(starts,z)-1
        return i>=0 and z<forbidden[i][1]

    rng = Random(9017)
    first_unused = max(graph)+1
    for j,(u,v,count) in enumerate(jobs):
        if v not in graph[u] or count<0:
            raise ValueError("invalid marked subdivision")
        graph[u].remove(v)
        graph[v].remove(u)
        if j==0:
            prefix = insert_neutral((labels[u],x),count-moves//6,limit,core,minority,rng)
            inside = prefix[1:-1]+row[::-1]
        else:
            path = insert_neutral((labels[u],labels[v]),count,limit,core,minority,rng)
            inside = path[1:-1]
        before = u
        for z in inside:
            labels[first_unused] = z
            graph[before].add(first_unused)
            graph[first_unused] = {before}
            before = first_unused
            first_unused += 1
        graph[before].add(v)
        graph[v].add(before)
    remove_fillers(iv,core-original)
    return graph,labels,iv,anchors,(moves,minor)


def finish(labels, iv, anchors, populations):
    remaining = Counter({labels[v]:n for v,n in populations.items()})
    for p,a,b in iv.blocks:
        remaining[p] -= b-a
    if min(remaining.values())<0:
        raise ValueError("insufficient population for the constructed seed")
    return complete(remaining,anchors)

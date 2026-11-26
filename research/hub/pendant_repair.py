"""Use an actual pendant path to repair a sparse multisite labeling."""

from collections import defaultdict
from random import Random

from research.check_large_order_subdivision import children
from research.hub.bounded_error import place_packet
from research.hub.linear_hub_batches import attach_batch
from research.hub.modular_injection import candidates
from research.large_order_gap_paths import gap_path, paired_path


def interval_bills(start, length, shift, k):
    return [((start+j) % k, (start+max(length,shift)+j) % k)
            for j in range(min(length,shift))]


def targets(bills,k):
    return {x for _,t in bills for x in (t,(-t) % k)}


def admissible(bills,k,blocked,arrivals):
    reserved = targets(bills,k)
    return (len(reserved) == 2*len(bills) and reserved.isdisjoint(arrivals)
            and blocked.isdisjoint(reserved) and all((s+2*t) % k for s,t in bills))


def leaf_runs(counts,digits,palette,blocked,k):
    """Pack reflected intervals and allow a single unmatched leaf for odd counts."""
    half = [x for x in range(1,(k+1)//2) if x in palette and k-x in palette
            and x not in blocked and k-x not in blocked]
    intervals = []
    for x in half:
        if intervals and intervals[-1][1] == x:
            intervals[-1][1] += 1
        else:
            intervals.append([x,x+1])
    leaves = defaultdict(list)
    bills = []
    cursor = 0
    for v,count in counts.items():
        if v == 0:
            continue
        shift = digits[v]
        for required,mirror in ((count//2,True),(count%2,False)):
            while required:
                if cursor == len(intervals):
                    raise ValueError("insufficient interval capacity")
                left,right = intervals[cursor]
                margin = 6*shift+1
                width = min(required,right-left-2*shift-margin)
                if width <= 0:
                    cursor += 1
                    continue
                for start in range(left+shift,left+shift+margin):
                    starts = [start,(-start-width+1) % k] if mirror else [start]
                    jobs = [pair for a in starts for pair in interval_bills(a,width,shift,k)]
                    if all((s+2*t) % k for s,t in jobs):
                        break
                else:
                    raise AssertionError("no translate separates the equal slopes")
                for a in starts:
                    leaves[v].extend(range(a,a+width))
                bills.extend(jobs)
                intervals[cursor][0] = start+width+shift
                required -= width
    return leaves,bills


def layout(tree,sites):
    kids = children(tree)
    spine = set(sites)
    for v in reversed(range(1,len(tree))):
        if v in spine:
            spine.add(tree[v])
    marks = sites | {v for v in spine if sum(w in spine for w in kids[v]) >= 2}
    chains = []
    for v in sorted(marks-{0}):
        reverse = []
        p = tree[v]
        while p not in marks:
            reverse.append(p)
            p = tree[p]
        chains.append((p,list(reversed(reverse)),v))
    height = [1]*len(tree)
    shape = {}
    types = {}
    for v in reversed(range(len(tree))):
        if v in spine:
            continue
        height[v] += max((height[w] for w in kids[v]),default=0)
        if height[v] < 10:
            key = tuple(sorted(shape[w] for w in kids[v]))
            shape[v] = types.setdefault(key,len(types))
    return kids,spine,marks,chains,height,shape


def neutral_arm(parent,parameter,ordinary):
    """The first ordinary labels walk forward, the last seven close the walk."""
    first = parameter if parent else parameter+1
    terminal = parameter+parent
    row = [first]
    for _ in range(1,ordinary):
        row.append(terminal)
        terminal += row[-2]
    return row+gap_path(row[-1],parameter,terminal)


def bridge(left,right,weight,k,blocked,rng):
    constant = weight-neutral_arm(left,0,3)[-1]-neutral_arm(right,0,4)[-1]
    for z in candidates(k,rng):
        x,y = -3*constant+14*z,2*constant-9*z
        row = [u % k for u in neutral_arm(left,x,3)+list(reversed(neutral_arm(right,y,4)))]
        if len(set(row)) == len(row) and blocked.isdisjoint(row):
            return row
    raise ValueError("no bridge specialization")


def construct(core,counts,anchor,length,k,palette,seed=81,*,subdivide=None):
    """Append length bare path vertices at anchor and counts[v] leaves at each site.

    If subdivide is a child of anchor, insert the path inside that core edge.
    The parent-before-child core starts at its largest leaf site 0 and excludes
    the supplied path and direct leaves. The expanded order must equal k.
    """
    bridge_size = 0 if subdivide is None else 21
    if subdivide is not None and (subdivide == 0 or core[subdivide] != anchor):
        raise ValueError("the specified edge is absent")
    if (len(core)+length+sum(counts.values()) != k or counts[0] != max(counts.values())
            or length < 10+bridge_size or (length-10-bridge_size) % 14):
        raise ValueError("incompatible order, path length or choice of root")
    rng = Random(seed)
    kids,spine,marks,chains,height,shape = layout(core,set(counts))
    labels = {0:0}
    for j,v in enumerate(sorted(marks-{0})):
        labels[v] = 3**j
    if 5*max(labels.values()) >= k:
        raise ValueError("fixed labels too large for the modulus")
    bills = [(labels[b],labels[a]+labels[b]) for a,chain,b in chains if not chain and a]
    blocked = set(labels.values())
    assert admissible(bills,k,blocked,set())
    blocked.update(targets(bills,k))
    leaves,leaf_bills = leaf_runs(counts,labels,set(palette),blocked,k)
    leaf_values = {x for row in leaves.values() for x in row}
    assert len(leaf_values) == sum(counts.values())-counts[0]
    assert blocked.isdisjoint(leaf_values) and admissible(leaf_bills,k,blocked,leaf_values)
    bills.extend(leaf_bills)
    blocked.update(leaf_values|targets(leaf_bills,k))
    statistics = defaultdict(int)
    statistics['leaf errors'] = len(leaf_bills)
    statistics['fixed errors'] = len(bills)-len(leaf_bills)
    short,tall = [],[]

    def expose(v):
        (short if height[v]<10 else tall).append(v)

    for v in sorted(marks):
        groups = defaultdict(list)
        for w in kids[v]:
            if w not in spine:
                if w in shape:
                    groups[shape[w]].append(w)
                else:
                    expose(w)
        for group in groups.values():
            width = (len(group)-2)//4*2+1
            if width <= 0:
                short.extend(group)
                continue
            rows = []
            for w in group[:2*width]:
                row = [w]
                for u in row:
                    row.extend(sorted(kids[u],key=shape.__getitem__))
                rows.append(row)
            index = {u:i for i,u in enumerate(rows[0])}
            branch = [-1]+[index[core[u]] for u in rows[0][1:]]
            jobs = []

            def accept(present,starts,size):
                jobs[:] = [pair for a in starts for pair in interval_bills(a,size,labels[v],k)]
                return admissible(jobs,k,blocked,present)

            labels.update(place_packet(branch,rows,k,blocked,rng,accept=accept))
            blocked.update(targets(jobs,k))
            bills.extend(jobs)
            statistics['packets'] += 1
            statistics['packet errors'] += len(jobs)
            short.extend(group[2*width:])

    def batch(path):
        for v in short:
            short.extend(kids[v])
        attach_batch(core,labels,blocked,short,path,k,rng)
        short.clear()
        statistics['batches'] += 1
        for v in path:
            for w in kids[v]:
                if w not in spine and w not in path:
                    expose(w)

    def single(v,other=None):
        p = labels[core[v]]
        for y in candidates(k,rng):
            if y in blocked:
                continue
            jobs = [(y,(p+y) % k)] if p else []
            if other is not None:
                b = labels[other]
                jobs.append((b,(b+y) % k))
            if admissible(jobs,k,blocked,{y}):
                break
        else:
            raise ValueError("no place for a single vertex and its targets")
        labels[v] = y
        blocked.add(y)
        blocked.update(targets(jobs,k))
        bills.extend(jobs)
        statistics['single errors'] += len(jobs)

    for _,chain,b in chains:
        j = 0
        while len(chain)-j > 10:
            batch(chain[j:j+10])
            j += 10
        for v in chain[j:]:
            single(v,b if v == chain[-1] else None)
            for w in kids[v]:
                if w not in spine:
                    expose(w)
    while tall:
        path = [tall.pop()]
        while len(path) < 10:
            path.append(max(kids[path[-1]],key=height.__getitem__))
        batch(path)
    for v in short:
        single(v)
        short.extend(kids[v])

    if 10+14*len(bills)+bridge_size > length:
        raise ValueError(f"path needs {10+14*len(bills)+bridge_size} vertices for these choices")
    parents = list(core)+[anchor]+list(range(len(core),len(core)+length-1))
    offset = len(core)
    attach_batch(parents,labels,blocked,[],list(range(offset,offset+10)),k,rng)
    offset += 10
    for s,t in bills:
        p = labels[parents[offset]]
        for z in candidates(k,rng):
            row = paired_path(p,s,t,z,k)
            moving = row[:7]+row[8:11]+row[12:]
            if len(set(row)) == 14 and blocked.isdisjoint(moving):
                break
        else:
            raise ValueError("no path specialization")
        labels.update(zip(range(offset,offset+14),row))
        blocked.update(row)
        offset += 14
    while offset < len(parents)-bridge_size:
        attach_batch(parents,labels,blocked,list(range(offset,offset+4)),
                     list(range(offset+4,offset+14)),k,rng)
        offset += 14
        statistics['unused slots'] += 1
    if subdivide is not None:
        weight = (labels[anchor]+labels[subdivide]) % k
        row = bridge(labels[parents[offset]],labels[subdivide],weight,k,blocked,rng)
        labels.update(zip(range(offset,offset+21),row))
        parents[subdivide] = len(parents)-1
    values = [labels[v] for v in range(len(parents))]
    for v,row in leaves.items():
        parents.extend([v]*len(row))
        values.extend(row)
    rest = sorted(set(range(k))-set(values))
    assert len(rest) == counts[0]
    parents.extend([0]*len(rest))
    values.extend(rest)
    return parents,values,dict(statistics)

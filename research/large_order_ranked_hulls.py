"""Grow the subtree joining selected leaf parents, keeping integer bin counts bounded."""

from collections import Counter, defaultdict, deque

from research.check_large_order_subdivision import children
from research.large_order_gap_paths import core_data, expand_core, prune, repair_paths, restore_layers
from research.large_order_interval_paths import interval_walks
from research.large_order_leaf_routing import diagonal_leaves


class RankedHull:
    def __init__(self, tree):
        self.tree = tree
        self.kids = children(tree)
        self.depth = [0] * len(tree)
        for i in range(1,len(tree)):
            self.depth[i] = self.depth[tree[i]] + 1
        self.live = {0}
        self.value = {0:0}
        self.scale = {0:1}
        self.holders = {0:0}
        self.stages = []

    def paths(self, marks):
        """Full original path of each edge between consecutive marks."""
        result = {}
        for v in sorted(marks - {0}):
            path = [v,self.tree[v]]
            while path[-1] not in marks:
                path.append(self.tree[path[-1]])
            result[v] = path[::-1]
        return result

    def available(self, candidates):
        blocked = set(self.value)
        for path in self.paths(set(self.value)).values():
            blocked.update((path[1],path[-2]))
        return [v for v in candidates if v not in blocked]

    def add(self, s, sites, jumps=()):
        """The sites are pins for the indicated jump shell, or extra free endpoints."""
        old = set(self.value)
        live = self.live.copy()
        for v in sites:
            while v not in live:
                live.add(v)
                v = self.tree[v]
        marks = old | set(sites)
        marks.update(v for v in live if sum(w in live for w in self.kids[v]) >= 2)
        pins = set(sites) if jumps else set()
        assert not pins.intersection(old)
        # Insert a free buffer if splitting an old segment places a pin at its end.
        buffers = set()
        for v,path in self.paths(marks).items():
            p = path[0]
            if v not in self.live or p not in self.live:
                continue
            if (v in pins and p in old) or (p in pins and v in old):
                assert len(path) > 2
                buffers.add(path[1] if p in old else path[-2])
        marks.update(buffers)
        # An even segment gets one additional original vertex, making both lengths odd.
        parity = {path[1] for path in self.paths(marks).values() if len(path)%2}
        marks.update(parity)
        edges = self.paths(marks)
        parent = {v:path[0] for v,path in edges.items()}
        assert all((self.depth[v]-self.depth[p])%2 for v,p in parent.items())
        inside = marks & self.live
        new = marks-old
        for v in new:
            self.scale[v] = s
        inside_pins = sorted(pins & inside)
        signed = sorted(jumps)
        for v,x in zip(inside_pins,signed):
            self.value[v] = x
            self.holders[x] = v
        vertex = Counter(self.value[v] for v in inside_pins)
        edge = Counter()
        nbr = defaultdict(list)
        for v,p in parent.items():
            if v in inside:
                nbr[p].append(v)
                nbr[v].append(p)
                assert not (v in pins and p in old or p in pins and v in old)
        unit = s//128
        cap = 12*(len(marks)+1)//max(1,unit) + 10
        for v in sorted(inside-old-pins):
            known = [self.value[w] for w in nbr[v] if w in self.value]
            assert len(known) <= 2
            low,high = self.band(v,unit)
            if unit:
                x = next(x for x in range(low,high) if vertex[x] < cap and
                         all(4*abs(x+y) >= unit and edge[x+y] < cap for y in known))
            else:
                x = 0
            self.value[v] = x
            vertex[x] += 1
            edge.update(x+y for y in known)

        # All hanging components have one labeled attachment. Sort the initial parents.
        kids = defaultdict(list)
        for v,p in parent.items():
            if v not in inside:
                kids[p].append(v)
        roots = sorted((p for p in inside if kids[p]),key=lambda p:(self.value[p],p))
        todo = deque(v for p in roots for v in kids[p])
        order = []
        while todo:
            v = todo.popleft()
            order.append(v)
            todo.extend(kids[v])
        assert set(order) == marks-inside
        outside_values = signed[len(inside_pins):]
        it = iter(outside_values)
        types = defaultdict(list)
        for v in order:
            if v in pins:
                x = next(it)
                self.value[v] = x
                self.holders[x] = v
            else:
                p = parent[v]
                sign = -1 if p in inside and self.value[p]<0 else 1
                types[self.depth[v]%2,sign].append(v)
        for (_,sign),vs in types.items():
            low,high = self.band(vs[0],unit)
            if sign < 0:
                low,high = 1-high,1-low
            for j,v in enumerate(vs):
                self.value[v] = low+j*(high-low)//len(vs) if unit else 0
        self.stages.append((s,len(marks),len(buffers),len(parity),len(inside_pins)))
        self.live = live

    def band(self, v, unit):
        return (16*unit,24*unit) if self.depth[v]%2 else (4*unit,8*unit)

    def select(self, ranked, bands):
        if not ranked or ranked[0] != 0 or any(self.depth[v]%2 for v in ranked):
            raise ValueError("ranked sites must be in the zero root's bipartition")
        s = 1
        for rank,radius,pop in bands:
            assert radius >= 2 and radius & (radius-1) == 0 and pop > 0
            while s < radius:
                available = self.available(ranked[:rank])
                if len(available) < 2*s:
                    raise ValueError("not enough eligible sites at this rank")
                jumps = [*range(1-2*s,1-s),*range(s,2*s)]
                self.add(s,available[:2*s],jumps)
                s *= 2

    def compressed(self, live, k):
        ids,small,holes = core_data(self.tree,live,set(self.value))
        reduced = {ids[j]:ids[p] for j,p in enumerate(small) if j}
        kids = defaultdict(list)
        for v,p in reduced.items():
            kids[p].append(v)
        groups = defaultdict(list)
        for v in self.value:
            if v == 0:
                continue
            path = []
            p = reduced[v]
            while p not in self.value:
                path.append(p)
                p = reduced[p]
            if path:
                groups[max(self.scale[v],self.scale[p])].append((p,v,path[::-1]))
        integers = self.value.copy()
        for s,items in groups.items():
            vertex,edge = Counter(),Counter()
            cap = 6*sum(len(path)+1 for _,_,path in items)//s + 6
            for p,v,path in items:
                for w in path:
                    known = [integers[z] for z in [reduced[w],*kids[w]] if z in integers]
                    x = next(x for x in range(8*s,10*s) if vertex[x] < cap
                             and all(edge[x+y] < cap for y in known))
                    integers[w] = x
                    vertex[x] += 1
                    edge.update(x+y for y in known)
        assert integers.keys() == set(ids)
        labels = [None]*len(self.tree)
        for v,x in integers.items():
            labels[v] = x % k
        expand_core(labels,holes,k)
        return ids,small,integers,labels,holes


def construct(tree, k, ranked, bands, depth=8400, seed=1):
    hull = RankedHull(tree)
    hull.select(ranked,bands)
    live,_,layers,chains = prune(tree,set(hull.holders.values()),depth)
    tips = [tree[path[0]] for path in chains]
    radius = bands[-1][1]
    if tips:
        scale = 1 << (max(radius,len(tips))-1).bit_length()
        hull.add(scale,tips)
    assert hull.live == live
    ids,small,integers,labels,holes = hull.compressed(live,k)
    result = tree.copy()
    repairs = routed = 0
    if len(tips) >= radius:
        repairs = repair_paths(tree,labels,ids,small,chains,k,seed)
    else:
        pairs = [(integers[v]+integers[ids[small[j]]],integers[v])
                 for j,v in enumerate(ids) if j]
        for walk in interval_walks(pairs,radius,seed):
            for x,y in zip(walk,walk[1:]):
                result.append(hull.holders[y-x])
                labels.append(x % k)
                routed += 1
    gap = restore_layers(tree,labels,layers,labels[0],k)
    counts = Counter(labels)
    level = max(counts.values())
    missing = [level+(x==gap)-counts[x] for x in range(k)]
    total = sum(rank*pop for rank,_,pop in bands)
    start = cumulative = 0
    for rank,r,pop in bands:
        cumulative += rank*pop
        end = k*cumulative//total
        for (_,jump),x in diagonal_leaves(missing[start:end],r):
            result.append(hull.holders[jump])
            labels.append(start+x)
        start = end
    return result, labels, hull, (repairs,routed,len(holes))

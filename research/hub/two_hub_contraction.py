"""Complete a two-hub core to integer intervals, recording whole filler ranges."""

from collections import deque
from bisect import bisect_left

from research.hub.two_hubs import path_seed, short_seed


class Interval:
    def __init__(self, seed):
        self.lo = seed.lo
        self.hi = seed.hi
        self.blocks = [(hub,x,x+1) for hub,x in seed.added]

    def fill(self, hub, first, stop, reflected=False):
        if first>=stop:
            return
        if reflected:
            hub,first,stop = 1-hub,2-stop,2-first
        self.blocks.append((hub,first,stop))

    def child(self, p):
        if p>0:
            x = self.lo-p
            self.fill(0,x+1,self.lo)
            self.lo = x
        else:
            x = self.hi+1-p
            self.fill(1,self.hi+1,x)
            self.hi = x
        return x

    def stretch(self, left, right):
        assert min(left,right)<=0<max(left,right) and {left,right}!={0,1}
        reflected = min(left,right)==0
        flip = (lambda x:1-x) if reflected else (lambda x:x)
        a,b = flip(left),flip(right)
        lo,hi = sorted((flip(self.lo),flip(self.hi)))
        p,q = max(a,b),min(a,b)
        assert p>0>q
        x = min(lo-p,p+2*q-hi-1)
        y = p+q-x
        self.fill(1,x+p,lo,reflected)
        self.fill(0,x+1,x+p,reflected)
        self.fill(0,hi+1,y+q,reflected)
        self.fill(1,y+q,y,reflected)
        self.lo,self.hi = sorted((flip(x),flip(y)))
        return (flip(x),flip(y)) if a==p else (flip(y),flip(x))


def remove_fillers(interval, removed):
    removed = sorted(removed)
    fresh = []
    count = 0
    for p,start,stop in interval.blocks:
        if p==1:
            fresh.append((p,start,stop))
            continue
        a,b = bisect_left(removed,start),bisect_left(removed,stop)
        count += b-a
        for x in removed[a:b]:
            if start<x:
                fresh.append((p,start,x))
            start = x+1
        if start<stop:
            fresh.append((p,start,stop))
    assert count==len(removed)
    interval.blocks = fresh


def elongate_group(interval, jobs):
    """Replace distinct crossing edges by odd paths in disjoint integer ranges."""
    if not jobs:
        return []
    width = interval.hi-interval.lo+1
    largest = max(s for _,_,s in jobs)
    lower, upper, paths = [], [], []
    for number,(left,right,s) in enumerate(jobs,1):
        p,q = max(left,right),min(left,right)
        assert p>=1 and q<=0 and s>=1
        code = 1 if len(jobs)==1 else largest*len(jobs)+number
        step = 8*(width+1)*code
        order = [i//2 if i%2==0 else s-i//2 for i in range(s+1)]
        outbound = [p+j*step if (i%2==0)==(left==p) else q-j*step
                    for i,j in enumerate(order)]
        paths.append(outbound+[p+q-x for x in reversed(outbound)])
        for i in range(1,s+1):
            lower.append((q-i*step,p+q-i*step))
            upper.append((p+i*step,p+q+i*step))
    lower.sort()
    upper.sort()
    def fill_gap(x,y,weight):
        assert x<weight<=y
        interval.fill(0,x+1,weight)
        interval.fill(1,weight,y)
    for (v,w),nxt in zip(lower,[x for x,_ in lower[1:]]+[interval.lo]):
        fill_gap(v,nxt,w)
    for prev,(v,w) in zip([interval.hi]+[x for x,_ in upper[:-1]],upper):
        fill_gap(prev,v,w)
    interval.lo,interval.hi = lower[0][0],upper[-1][0]
    return paths


def long_seed(distance):
    if distance%2:
        seed = path_seed(distance)
        return Interval(seed),seed.path,0
    seed = path_seed(6)
    interval,path = Interval(seed),seed.path
    if distance==6:
        return interval,path,0
    long_path, = elongate_group(interval,[(path[1],path[2],(distance-6)//2)])
    return interval,path[:1]+long_path+path[3:],1


def contraction(parent):
    """Remove pendant layers or separated pairs of unary vertices outside the seed."""
    parent = parent.copy()
    rounds = []
    while parent:
        kids = {v:[] for v in parent}
        for v,p in parent.items():
            if p in kids:
                kids[p].append(v)
        leaves = [v for v,children in kids.items() if not children]
        before = len(parent)
        if 8*len(leaves)>=before:
            rounds.append(('leaves',[(parent[v],v) for v in leaves]))
            for v in leaves:
                del parent[v]
        else:
            pairs = []
            for v,p in parent.items():
                if len(kids[v])!=1 or (p in kids and len(kids[p])==1):
                    continue
                chain = []
                while len(kids[v])==1:
                    chain.append(v)
                    v = kids[v][0]
                for i in range(0,len(chain)-1,3):
                    a,b = chain[i:i+2]
                    pairs.append((parent[a],a,b,kids[b][0]))
            rounds.append(('pairs',pairs))
            for top,a,b,base in pairs:
                del parent[a],parent[b]
                parent[base] = top
        assert 8*len(parent)<=7*before
    return rounds


def bound(h):
    ceil_log = (2*h-1).bit_length()
    return (100*(h+1))**(8*ceil_log+1)


def complete(tree, a, b):
    if not tree or tree[0]!=-1 or any(not 0<=p<v for v,p in enumerate(tree[1:],1)):
        raise ValueError("need a parent-before-child tree")
    if a==b or not (0<=a<len(tree) and 0<=b<len(tree)):
        raise ValueError("need two different vertices")
    graph = [[] for _ in tree]
    for v in range(1,len(tree)):
        p = tree[v]
        graph[v].append(p)
        graph[p].append(v)
    prev = {a:None}
    queue = deque([a])
    while b not in prev:
        v = queue.popleft()
        for w in graph[v]:
            if w not in prev:
                prev[w] = v
                queue.append(w)
    path = [b]
    while path[-1]!=a:
        path.append(prev[path[-1]])
    path.reverse()
    distance = len(path)-1
    if distance in (2,4):
        short = short_seed(graph,path)
        if short is None:
            return None
        seed,labels = short
        interval,path_rounds = Interval(seed),0
    else:
        interval,values,path_rounds = long_seed(distance)
        labels = dict(zip(path,values))

    parent = {}
    queue = deque(labels)
    while queue:
        v = queue.popleft()
        for w in graph[v]:
            if w not in labels and w not in parent:
                parent[w] = v
                queue.append(w)
    rounds = contraction(parent)
    for kind,moves in reversed(rounds):
        before = interval.hi-interval.lo+1
        if kind=='leaves':
            for p,v in moves:
                labels[v] = interval.child(labels[p])
        else:
            for top,u,v,base in moves:
                labels[u],labels[v] = interval.stretch(labels[top],labels[base])
        assert interval.hi-interval.lo+1<=100*(len(tree)+1)*before
    return [labels[v] for v in range(len(tree))],interval,(path_rounds,len(rounds))


def segment_core(tree, a, b, keep_length, pins=()):
    """Compress chains between marked vertices using the supplied length rule."""
    graph = [[] for _ in tree]
    for v,p in enumerate(tree[1:],1):
        graph[p].append(v)
        graph[v].append(p)
    marks = {v for v,nb in enumerate(graph) if len(nb)!=2} | {a,b} | set(pins)
    marked_ids = {a:0}
    compact = [-1]
    segments = []
    stack = [(a,None)]
    while stack:
        v,previous = stack.pop()
        for w in graph[v]:
            if w==previous:
                continue
            full = [v,w]
            while full[-1] not in marks:
                full.append(next(x for x in graph[full[-1]] if x!=full[-2]))
            length = len(full)-1
            retained = keep_length(length)
            short = [marked_ids[v]]
            for _ in range(retained):
                compact.append(short[-1])
                short.append(len(compact)-1)
            marked_ids[full[-1]] = short[-1]
            segments.append((full,short))
            stack.append((full[-1],full[-2]))

    return compact,marked_ids[b],segments


def compact_complete(tree, a, b):
    """Run the interval algorithm on a parity representative, then restore all segments."""
    compact,other,segments = segment_core(tree,a,b,lambda n:n if n<=6 else 6-n%2)
    witness = complete(compact,0,other)
    if witness is None:
        assert all(len(full)==len(short) for full,short in segments)
        return None
    base,interval,rounds = witness
    jobs,placements = [],[]
    for full,short in segments:
        extra = len(full)-len(short)
        if extra:
            i = next(i for i,(u,v) in enumerate(zip(short,short[1:]))
                     if min(base[u],base[v])<=0<max(base[u],base[v]))
            jobs.append((base[short[i]],base[short[i+1]],extra//2))
            placements.append((i,len(jobs)-1))
        else:
            placements.append(None)
    expanded = elongate_group(interval,jobs)
    labels = [None]*len(tree)
    for (full,short),where in zip(segments,placements):
        row = [base[v] for v in short]
        if where is not None:
            i,j = where
            row[i:i+2] = expanded[j]
        assert len(full)==len(row)
        for v,x in zip(full,row):
            assert labels[v] in (None,x)
            labels[v] = x
    return labels,interval,(len(compact),len(jobs),*rounds)

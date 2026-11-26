"""Independently audit the symbolic path, the rounding and complete rooted trees."""

from collections import Counter
from itertools import product
from random import Random
from research.large_order_degree import attach_batch, counts, balanced
from research.large_order_subdivision import POSITIONS, expand, round_groups


def symbolic():
    p,q = (1,0,0,0), (0,1,0,0)
    path = (p,*POSITIONS,q)
    sums = Counter(tuple(x+y for x,y in zip(a,b)) for a,b in zip(path,path[1:]))
    assert sums == Counter((*POSITIONS,(1,1,0,0)))
    assert POSITIONS[:2] == ((0,0,1,0),(0,0,0,1))
    assert all(1 in map(abs, row[2:]) for row in POSITIONS)
    assert all(not any(row[:2]) or 1 in map(abs,row[:2]) for row in POSITIONS)


def check_paths(specs, k):
    hist = [0]*k
    for (p,q,r),path in zip(specs,expand(specs,k)):
        assert (path[0],path[-1])==(p,q) and len(path)==12*r+2
        sums = Counter((a+b)%k for a,b in zip(path,path[1:]))
        assert sums==Counter([*path[1:-1],(p+q)%k])
        for a in path[1:-1]:
            hist[a]+=1
    assert all(abs(x*k-sum(hist))<=96*k for x in hist)


def children(tree):
    kids = [[] for _ in tree]
    for i,p in enumerate(tree[1:],1):
        kids[p].append(i)
    return kids


def compress(tree, kids, live):
    paths = []
    keep = {0}
    for i in sorted(live):
        current = [u for u in kids[i] if u in live]
        if i and len(current)==1:
            continue
        for u in current:
            path = [i,u]
            nexts = [v for v in kids[u] if v in live]
            while len(nexts)==1:
                u, = nexts
                path.append(u)
                nexts = [v for v in kids[u] if v in live]
            omitted = 12*((len(path)-2)//12)
            keep.update(path[:len(path)-omitted-1])
            keep.add(path[-1])
            if omitted:
                paths.append(path[-omitted-2:])
    ids = sorted(keep)
    number = {v:i for i,v in enumerate(ids)}
    smaller = [-1]
    for v in ids[1:]:
        p = tree[v]
        while p not in keep:
            p = tree[p]
        smaller.append(number[p])
    return ids,smaller,paths


def restore(tree, labels, undo, k):
    if not undo:
        return labels
    v,e = counts(tree,labels,k)
    gap, = [x for x in range(k) if v[x]-e[x]==1]
    top = max(v)
    fill = [x for x in range(k) for _ in range(top+(x==gap)-v[x])]
    extended = list(tree)+[0]*len(fill)
    labels = labels+fill
    for batch in reversed(undo):
        dummy = k-len(batch)
        ids = list(range(len(extended),len(extended)+dummy))
        extended += [0]*dummy
        labels += [None]*dummy
        attach_batch(extended,labels,batch+ids,k)
    return labels[:len(tree)]


def peel(tree, kids, k, rounds):
    live = set(range(len(tree)))
    undo = []
    while True:
        leaves = sorted(v for v in live if v and not live.intersection(kids[v]))
        if rounds is None:
            if len(leaves)<k:
                break
            leaves=leaves[:k]
        else:
            if not leaves or len(undo)==rounds:
                break
            assert len(leaves)<=k
        undo.append(leaves)
        live.difference_update(leaves)
    return live,undo


def construct(tree,k,depth_rounds,stats,unrestricted=True):
    if len(tree)<=3:
        return [0]*len(tree)
    kids=children(tree)
    live,undo=peel(tree,kids,k,None if unrestricted else depth_rounds)
    ids,smaller,paths=compress(tree,kids,live)
    if not unrestricted:
        assert len(smaller)<len(tree)
    sub=construct(smaller,k,depth_rounds,stats,False)
    labels=[None]*len(tree)
    for i,x in zip(ids,sub):
        labels[i]=x
    specs=[(labels[path[0]],labels[path[-1]],(len(path)-2)//12) for path in paths]
    for path,walk in zip(paths,expand(specs,k)):
        for i,x in zip(path,walk):
            labels[i]=x
    stats[0] += len(undo)
    stats[1] += sum(r for _,_,r in specs)
    labels=restore(tree,labels,undo,k)
    v,e=counts(tree,labels,k)
    assert labels[0]==0 and sorted(a-b for a,b in zip(v,e))==[0]*(k-1)+[1]
    return labels


if __name__=='__main__':
    symbolic()
    # Nonuniform target rows exercise the floating-variable proof separately.
    rng=Random(1539)
    for _ in range(20):
        groups=[[[rng.randrange(3) for _ in range(4)] for _ in range(3)] for _ in range(24)]
        choices=round_groups(groups,4)
        mass=max(sum(c) for g in groups for c in g)
        for a in range(4):
            actual=sum(g[j][a] for g,j in zip(groups,choices))
            assert abs(3*actual-sum(c[a] for g in groups for c in g))<=6*mass
    for k in range(2,8):
        # Every pair includes equal endpoints and zero, even and composite k.
        check_paths([(p,q,1) for p,q in product(range(k),repeat=2)],k)
        check_paths([(1,0,8),(0,0,7),(0,1,4)],k)
    stats=[0,0]
    cases=0
    for k in range(2,8):
        for b in (15,43,98,177):
            # A reduced first cutoff exercises several recursion levels.
            for t in ([-1]+list(range(b-1)),[-1]+[rng.randrange(i) for i in range(1,b)]):
                x=construct(t,k,2,stats)
                v,e=counts(t,x,k)
                gap,=[a for a in range(k) if v[a]!=e[a]]
                slots=[a for a in range(k) for _ in range(max(v)+(a==gap)-v[a])]
                t=list(t)+[0]*len(slots)
                x+=slots
                assert all(balanced(row) for row in counts(t,x,k))
                cases+=1
    print(f"Symbolic identity, general rounding, all endpoint pairs at moduli 2–7; "
          f"{cases} full trees, {stats[0]} restored batches and {stats[1]} path blocks.")

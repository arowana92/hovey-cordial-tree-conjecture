"""Account for both sides of every cut in the subtree spanned by exposed leaves."""

from random import Random


def partitions(total, largest):
    if total==0:
        yield ()
    for size in range(min(total,largest),0,-1):
        for rest in partitions(total-size,size):
            yield (size,)+rest


def pack(weights,H):
    bins=[]
    for size in sorted(weights,reverse=True):
        for group in bins:
            if sum(group)+size<=H:
                group.append(size)
                break
        else:
            bins.append([size])
    assert all(sum(g)<=H for g in bins)
    return len(bins)


def periods(H,d):
    maximum=0
    patterns=0
    for weights in partitions(d,H):
        groups=pack(weights,H)
        K=max(1,min(d-2*H,len(weights)-2))
        span=11 if H%2 else 12
        pairs=groups*(12-H)+K+span*(K-1)
        maximum=max(maximum,(2*pairs+d+H)//26)
        patterns+=1
    return maximum,patterns


def grow(rng,d):
    # Random subdivisions and varying branching degrees, starting with a tripod.
    tree=[{1,2,3},{0},{0},{0}]
    for _ in range(3,d):
        if rng.randrange(3):
            v=rng.randrange(len(tree))
            w=rng.choice(sorted(tree[v]))
            joint=len(tree)
            tree[v].remove(w)
            tree[w].remove(v)
            tree[v].add(joint)
            tree[w].add(joint)
            tree.append({v,w})
        else:
            joint=rng.choice([v for v,adj in enumerate(tree) if len(adj)>=3])
        tip=len(tree)
        tree[joint].add(tip)
        tree.append({joint})
    return tree


def component(tree,a,b):
    seen={a,b}
    queue=[b]
    for v in queue:
        for w in tree[v]-seen:
            seen.add(w)
            queue.append(w)
    return set(queue)


def check_split(tree,H,d):
    tips={v for v,adj in enumerate(tree) if len(adj)==1}
    assert len(tips)==d
    main=[set() for _ in tree]
    for v,adj in enumerate(tree):
        for w in adj:
            if w<v:
                continue
            count=len(tips&component(tree,v,w))
            if min(count,d-count)>H:
                main[v].add(w)
                main[w].add(v)
    core={v for v,x in enumerate(main) if x}
    if not core:
        center=next(v for v in range(len(tree)) if v not in tips and all(
            len(tips&component(tree,v,w))<=H for w in tree[v]))
        core={center}
    branches=[tips&component(tree,v,w) for v in core for w in tree[v]-core]
    assert set.union(*branches)==tips and sum(map(len,branches))==d
    assert max(map(len,branches))<=H
    special={v for v in core if len(main[v])!=2 or tree[v]-core}
    assert len(special)<=max(1,min(d-2*H,len(branches)-2))
    if len(core)>1:
        ends=[v for v in core if len(main[v])==1]
        assert all(sum(len(tips&component(tree,v,w)) for w in tree[v]-core)>=H+1 for v in ends)


if __name__=='__main__':
    rng=Random(261992)
    total=patterns=0
    for H in range(1,6):
        values=[]
        for d in range(H+4,23-H,2):
            q,count=periods(H,d)
            values.append((d,q))
            patterns+=count
            for _ in range(60):
                check_split(grow(rng,d),H,d)
                total+=1
        print('H',H,'deficiency and maximum period',values)
    print('tip partitions',patterns,'literal spanning trees',total)

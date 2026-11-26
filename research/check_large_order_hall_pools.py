"""Check the modular decomposition and physically relabel all centers of actual trees."""

from collections import Counter
from itertools import product
from random import Random

from research.large_order_check import balanced_target, histograms, moment
from research.large_order_hall_pools import edge_split, pairs_for


def check_split(f):
    k = len(f)
    e,h,g = edge_split(f)
    assert e in (0,1)
    for row in (h,g):
        assert sum(row)==0 and moment(row)%k==0
    out = [2*h[i]+g[i]+g[i-1] for i in range(k)]
    for i,x in enumerate((1,-2,1)):
        out[i%k] += e*x
    assert list(f)==out and max(map(abs,g))<=6
    assert max(map(abs,h))<=3*(max(map(abs,f))+5)
    return e


def assign(pool, labels, desired, which):
    k = len(desired)
    by_parent = [[] for _ in desired]
    for p,t in pairs_for(desired):
        if which == 'vertices':
            # p+t is the desired vertex, t becomes its incident edge weight.
            by_parent[(-p)%k].append((p+t)%k)
        else:
            by_parent[p].append(t)
    for i,p in pool:
        labels[i] = by_parent[p].pop()
    assert not any(by_parent)


def whole(k, rng):
    copies = 24
    parents = [-1]
    labels = [0]
    def add(p,x):
        parents.append(p)
        labels.append(x%k)
        return len(labels)-1

    # Attach consecutive five-site blocks along an actual degree-two spine.
    end = 0
    def site(left,center,right):
        nonlocal end
        buf = add(end,rng.randrange(k))
        u = add(buf,left)
        i = add(u,center)
        v = add(i,right)
        end = add(v,rng.randrange(k))
        return i
    pools = []
    # Place the buffers after recording their incident triplets.
    for d in (0,0,1):
        pool = []
        for p in range(k):
            for _ in range(copies):
                pool.append((site(p,0,p+d),p))
        pools.append(pool)
    exceptional = (site(0,1,0),site(0,0,1))
    spare = add(end,rng.randrange(k))
    tail = add(spare,rng.randrange(k))
    for j in range(k+1):
        tail = add(tail,rng.randrange(k))
    for i,d in enumerate((0,0,1)):
        assign(pools[i],labels,[copies]*k,'vertices' if i==0 else 'edges')
    # The unplanted spine buffers have bounded initial discrepancy by an
    # explicit periodic placement on each side of the triplets.
    for pool in pools:
        for offset,(v,p) in enumerate(pool):
            j = offset%copies
            labels[v-2] = j%k
            labels[v+2] = (j+p)%k
    v,e = histograms(parents,labels,k)
    vt,et = balanced_target(len(labels),k),balanced_target(len(labels)-1,k)
    a,b = moment(vt)-moment(v),moment(et)-moment(e)
    labels[spare] = (labels[spare]+b-a)%k
    labels[tail] = (labels[tail]+2*a-b)%k
    v,e = histograms(parents,labels,k)
    dv,de = [x-y for x,y in zip(vt,v)],[x-y for x,y in zip(et,e)]
    flag,h,g = edge_split(de)
    if flag:
        i,j = exceptional
        labels[i],labels[j] = labels[j],labels[i]
    for pool,delta,kind in zip(pools,(dv,h,g),('vertices','edges','edges')):
        assign(pool,labels,[copies+x for x in delta],kind)
    assert histograms(parents,labels,k)==(vt,et)
    return len(labels),flag


def whole_leaf(k,rng):
    parents,labels = [-1],[0]
    pools = [[],[]]
    copies = 8
    for pool in pools:
        for shift in range(k):
            for _ in range(copies):
                parent = len(parents)
                parents.extend((0,parent))
                labels.extend((shift,0))
                pool.append((parent+1,shift))
    for pool,kind in zip(pools,('vertices','edges')):
        assign(pool,labels,[copies]*k,kind)
    last = 0
    for _ in range(k+3):
        parents.append(last)
        labels.append(rng.randrange(k))
        last = len(parents)-1
    v,e = histograms(parents,labels,k)
    vt,et = balanced_target(len(labels),k),balanced_target(len(labels)-1,k)
    if len(labels)%k:
        vt = balanced_target(len(labels),k,moment(v)+moment(et)-moment(e))
    else:
        et = balanced_target(len(labels)-1,k,moment(e)+moment(vt)-moment(v))
    labels[last] = (labels[last]+moment(vt)-moment(v))%k
    v,e = histograms(parents,labels,k)
    for pool,src,dst,kind in zip(pools,(v,e),(vt,et),('vertices','edges')):
        assign(pool,labels,[copies+y-x for x,y in zip(src,dst)],kind)
    assert histograms(parents,labels,k)==(vt,et)
    return len(labels)


if __name__=='__main__':
    rng = Random(88932)
    tested = toggles = 0
    for k in range(2,11):
        for f in product((-1,0,1),repeat=k):
            if not sum(f) and not moment(f)%k:
                toggles += check_split(f)
                tested += 1
    for k in range(2,505):
        f = [0]*k
        for _ in range(2*k):
            a,b,c = (rng.randrange(k) for _ in range(3))
            for i,d in ((a,1),(a+b,-1),(a+c,-1),(a+b+c,1)):
                f[i%k] += d
        toggles += check_split(f)
    layers = 0
    for k in range(2,10):
        for _ in range(12):
            values = [rng.randrange(k) for _ in range(3*k-1)]
            values.append(-sum(values)%k)
            want = [values.count(i) for i in range(k)]
            pairs = pairs_for(want)
            for j in (0,1):
                assert Counter(item[j] for item in pairs)==Counter({i:3 for i in range(k)})
            assert Counter((a+b)%k for a,b in pairs)==Counter(values)
            layers += len(pairs)//k
    trees = [whole(k,rng) for k in (3,4,6,8) for _ in range(3)]
    print(f"{tested} exhaustive and 503 larger splits, {toggles} parity toggles; "
          f"{layers} independently recounted Hall layers.")
    leaves = [whole_leaf(k,rng) for k in range(2,10) for _ in range(3)]
    print(f"{len(leaves)} whole trees repaired with leaf pools.")
    print(f"{len(trees)} full trees through order {max(n for n,_ in trees)}, both histograms verified.")

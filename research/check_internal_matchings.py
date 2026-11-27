"""Verify the interval of matching sizes and the full-period leaf extensions."""

from random import Random

from .check_near_matching import maximum
from .large_order_gap_paths import leaf_batch
from .rainbow.verify import rooted_shapes


def interval(parent):
    deg = [0]*len(parent)
    for v,p in enumerate(parent[1:],1):
        deg[p] += 1
        deg[v] += 1
    core = [v for v,d in enumerate(deg) if d>1]
    index = {v:j for j,v in enumerate(core)}
    induced = [index.get(parent[v],-1) for v in core]
    return len(core)-maximum(induced),maximum(parent)


def possible_sizes(parent):
    # Independently enumerate all matchings, keeping only those covering
    # each original nonleaf. Rooted tree catalogs here have at least 3 nodes.
    deg = [0]*len(parent)
    used = [False]*len(parent)
    for v,p in enumerate(parent[1:],1):
        deg[p] += 1
        deg[v] += 1
    sizes = set()

    def visit(v,size):
        if v == len(parent):
            if all(d<=1 or u for d,u in zip(deg,used)):
                sizes.add(size)
            return
        visit(v+1,size)
        p = parent[v]
        if not used[p]:
            used[v] = used[p] = True
            visit(v+1,size+1)
            used[v] = used[p] = False

    visit(1,0)
    return sizes


def check_leaves(k, periods, additions, rng):
    n = k*periods
    f = [(v//2 + ((n+1)//2 if v%2 else 0))%k for v in range(n)]
    parents = [rng.randrange(n) for _ in range(additions)]
    weights = [0]*k
    for v in range(1,n):
        weights[(f[v-1]+f[v])%k] += 1
    vertices = [periods]*k
    for start in range(0,len(parents),k):
        batch = parents[start:start+k]
        deficit = weights.index(min(weights))
        first = (deficit-f[batch[0]])%k
        others,_ = leaf_batch([f[w] for w in batch[1:]],first,k)
        for x,p in zip([first]+others,batch):
            vertices[x] += 1
            weights[(f[p]+x)%k] += 1
            assert max(vertices)-min(vertices)<=1 and max(weights)-min(weights)<=1


def main():
    trees = hairy = batches = 0
    for n in range(3,12):
        for parent in rooted_shapes(n).values():
            low,high = interval(parent)
            assert possible_sizes(parent)==set(range(low,high+1))
            trees += 1
    rng = Random(130026)
    for c in range(2,85):
        for _ in range(8):
            base = [-1]+[rng.randrange(i) for i in range(1,c)]
            tree = base+[v for v in range(c) for _ in range(rng.randrange(1,7))]
            assert interval(tree)==(c-maximum(base),c)
            hairy += 1
    for k in (26,30,34,38,42,46,50):
        for t in range(k):
            for q in (0,1,3):
                check_leaves(k,rng.randint(1,4),q*k+t,rng)
                batches += 1
    print(trees,'rooted trees with every attainable size checked')
    print(hairy,'arbitrary cores with independent positive leaf populations')
    print(batches,'leaf extensions with every intermediate prefix checked')


if __name__ == '__main__':
    main()

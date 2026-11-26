"""Recompute edge residues and audit the modular construction on original trees."""

from collections import Counter
from itertools import product
from random import Random

from research.hub.modular_injection import advance, construct, walks
from research.rainbow.verify import rooted_shapes


def audit(tree, k, x, g):
    assert x[0]==0 and len(set(x))==len(x)==len(tree)
    assert all(0<=v<k for v in x)
    weights = Counter((x[i]+x[p])%k for i,p in enumerate(tree) if i)
    weights[g] += 1
    assert weights==Counter(x)


def walk_checks():
    total = 0
    for k in (4,6,9,10):
        for n in range(6):
            for steps in product((-2,-1,0,1,2),repeat=n):
                tree = [-1]+list(range(1,n+1))
                labels = {i+1:x%k for i,x in enumerate(steps)}
                cycles,path,end = walks(list(range(1,n+1)),tree,labels,k)
                assert end==sum(steps)%k and sorted(v for c in [*cycles,path] for v,x in c)==list(range(1,n+1))
                for piece,is_path in [(c,False) for c in cycles]+[(path,True)]:
                    tails = [x for v,x in piece]
                    assert len(set(tails))==len(tails)
                    heads = [(x+labels[tree[v]])%k for v,x in piece]
                    if piece:
                        assert heads==tails[1:]+([end] if is_path else tails[:1])
                    if is_path:
                        assert end not in tails and (not tails or tails[0]==0)
                total += 1
    return total


def local_round(p, jumps, k):
    # Make a star holding every prescribed parent, then hang the actual
    # batch and an eight-vertex downward path from the indicated parents.
    values = sorted({p,*jumps}-{0})
    labels = {0:0, **{i:x for i,x in enumerate(values,1)}}
    inverse = {x:i for i,x in labels.items()}
    tree = [-1]+[0]*len(values)
    front = []
    for x in jumps:
        front.append(len(tree))
        tree.append(inverse[x])
    path = []
    parent = inverse[p]
    for _ in range(8):
        path.append(len(tree))
        tree.append(parent)
        parent = path[-1]
    occupied = set(labels.values())
    mode,_ = advance(front,path,tree,labels,occupied,k,Random(588))
    ids = sorted(labels)
    assert ids==list(range(len(ids))) and len(occupied)==len(ids)
    audit(tree[:len(ids)],k,[labels[v] for v in ids],0)
    return mode


def main():
    modes = Counter()
    for k in (3072,4096,4620,5003):
        p = 17
        for jumps in ([1,k-1],[0,0],[1,k-1,5],[3,5,k-5],[2,k-2,k-p],[0,k-p],[5,7]):
            modes[local_round(p,jumps,k)] += 1
    assert set(modes)=={'cycle','residual','neutral'}
    shape_count = 0
    for n in range(1,14):
        for tree in rooted_shapes(n).values():
            x,g,stats = construct(tree,65536)
            audit(tree,65536,x,g)
            shape_count += 1

    rng = Random(4097)
    max_h = max_rounds = max_layers = 0
    trials = 0
    for n in (55,167,610,1370):
        for _ in range(12):
            spine = rng.randrange(n//3,n-6)
            tree = [-1]+list(range(spine-1))
            while len(tree)<n:
                tree.append(rng.randrange(len(tree)))
            for k in (2**32,3**16,2**9 * 3**5 * 5**2,2147483647,101*(n+1)**14):
                x,g,stats = construct(tree,k,rng.randrange(100000))
                audit(tree,k,x,g)
                max_h = max(max_h,n)
                max_rounds = max(max_rounds,stats[0])
                max_layers = max(max_layers,stats[-2])
                assert stats[-1] <= 7*(n+1)**12
                trials += 1
    # A shallow but very wide suffix forces several large integer slopes
    # and exercises the composite-modulus affine specialization.
    wide = [-1]+list(range(6))
    for _ in range(72):
        parent = 3
        for _ in range(4):
            wide.append(parent)
            parent = len(wide)-1
    for k in (2**24,3**15,5**12,2**10*3**8,101*(len(wide)+1)**14):
        x,g,stats = construct(wide,k)
        audit(wide,k,x,g)
        assert stats[-1]>100000
    print(f"{shape_count:,} rooted shapes through order 13 at modulus 65,536.")
    print(f"{walk_checks():,} modular jump lists; local path cases {dict(modes)}.")
    print(f"{trials} full replays through order {max_h:,}, up to {max_rounds} rounds and {max_layers} closing levels; five wide suffixes.")


if __name__=='__main__':
    main()

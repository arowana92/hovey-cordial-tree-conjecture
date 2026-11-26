"""Check the two complete integer intervals and the prescribed-boundary reduction."""

from collections import Counter
from random import Random

from research.hub.check_two_hub_contraction import audit_ranges
from research.hub.two_hub_buffer import buffered_complete
from research.hub.two_hub_contraction import complete


def audit(tree,a,b):
    witness = buffered_complete(tree,a,b)
    if witness is None:
        enlarged = tree+[a,b]
        degree = Counter(range(1,len(enlarged)))+Counter(enlarged[1:])
        internal = Counter()
        for v,p in enumerate(enlarged[1:],1):
            if min(degree[v],degree[p])>1:
                internal.update((v,p))
        assert max(internal.values(),default=0)<=2
        return (0,0,0,0)
    labels,iv,(w,cap,rotations,subdivisions) = witness
    assert len(set(labels))==len(tree) and labels[a]==0 and labels[b]==1
    edges = [labels[v]+labels[p] for v,p in enumerate(tree) if v]
    audit_ranges(labels,[(x,y) for _,x,y in iv.blocks],iv.lo,iv.hi+1)
    audit_ranges(edges,[(x+p,y+p) for p,x,y in iv.blocks],iv.lo+1,iv.hi+1)
    costs = [sum(y-x for p,x,y in iv.blocks if p==site) for site in (0,1)]
    assert sum(costs)+len(tree)==iv.hi-iv.lo+1
    if rotations:
        assert rotations<=cap and rotations%6==0
        assert costs[1]<=(cap+8)*(w+1)
        assert iv.hi-iv.lo+1<=2**30*(len(tree)+(cap+8)*(w+1)+1)
    return rotations,subdivisions,*costs


def cuts(rng):
    tests = 0
    for k in range(5,80):
        for _ in range(22):
            h = rng.randrange(k+1,3*k+1)
            tree = [-1]+[rng.randrange(v) for v in range(1,h)]
            # In this order the first hub is the root, as required by the cut.
            minor = rng.randrange(1,h)
            m0,m1 = sorted((rng.randrange(k),rng.randrange(k)),reverse=True)
            n = h+m0+m1
            t = (n-1)%k
            if not t or m0+m1>=t:
                continue
            take = t-m1
            keep = h-take
            free = set(range(keep,h))
            parent_labels = {v:rng.randrange(k) for v in range(keep)}
            boundaries = {v:parent_labels[tree[v]] for v in free if tree[v]<keep}
            assert boundaries
            # Recompute the actual edges into the suffix in the full decorated tree.
            full = tree+[0]*m0+[minor]*m1
            out = free|set(range(h+m0,n))
            incoming = [(full[v],v) for v in out if full[v] not in out]
            assert len(out)==t and (n-t)%k==1
            assert {v for p,v in incoming if v<h}==set(boundaries)
            assert len(incoming)==len(boundaries)+(m1 if minor<keep else 0)
            assert len(free)+k-1-t==k-1-m1>=(k-1)//2
            original_leaves = set(range(h))-set(tree[1:])
            free_leaves = free-{tree[v] for v in free}
            assert free_leaves<=original_leaves
            tests += 1
    return tests


def forest_moments():
    tests = 0
    for d in (7,12,19,28):
        tree = [-1]+list(range(d))
        labels,iv,_ = complete(tree,0,d)
        for root in (0,d//2,d):
            legs = [(p,x) for p,a,b in iv.blocks for x in range(a,b)]
            legs += [(0,x) for x in range(iv.hi+1,iv.hi+12)]
            legs += [(1,x) for x in range(iv.lo-13,iv.lo)]
            k = len(tree)+len(legs)
            X = [x%k for x in labels]
            edges = [(u,u+1) for u in range(d)]
            A = set(X)
            # Delete root from the core. Every incident weight becomes an
            # external boundary edge using the deleted vertex's residue.
            fixed = [(X[u]+X[v])%k for u,v in edges if root in (u,v)]
            ordinary = [x for i,x in enumerate(X) if i!=root]
            assert len(ordinary)==len(tree)-1 and X[root] not in ordinary
            weights = [(X[u]+X[v])%k for u,v in edges if root not in (u,v)]
            leaf_weights = [(p+x)%k for p,x in legs]
            gap, = set(range(k))-set(fixed+weights+leaf_weights)
            C = set(fixed+weights+[gap])
            shifts = sum(p for p,_ in legs)
            assert (sum(C)-sum(A)+shifts)%k==0
            ends = sum(X[part[0]]+X[part[-1]] for part in
                       [list(range(root)),list(range(root+1,d+1))] if part)
            assert gap==(2*X[root]+ends-sum(fixed)-sum(A)-shifts)%k
            tests += 1
    return tests


def main():
    rng = Random(75)
    cases = rotations = neutral = 0
    max_h = 0
    for n in (48,500,1600,6060,12034):
        for mode in range(5):
            tree = [-1]
            end = 0
            branches = 1+mode
            for j in range(branches):
                parent = 0 if j<2 else rng.randrange(len(tree))
                for _ in range((n-1)//branches):
                    tree.append(parent)
                    parent = len(tree)-1
                end = parent
            a,b = ((0,end),(end,0),(len(tree)//3,2*len(tree)//3))[mode%3]
            r,s,_,_ = audit(tree,a,b)
            rotations += r
            neutral += s
            max_h = max(max_h,len(tree))
            cases += 1
    assert rotations and neutral
    print(f"{cases} two-hub interval certificates through order {max_h:,}, "
          f"{rotations} buffer subdivisions, {neutral:,} neutral blocks.")
    print(f"{cuts(rng)} suffix cuts and {forest_moments()} prescribed-forest moment checks.")


if __name__=='__main__':
    main()

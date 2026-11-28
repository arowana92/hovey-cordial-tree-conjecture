"""Verify diameter-four obstructions on two periods and their ordinary labelings."""
from itertools import permutations
from math import gcd

from research.eight.check_dfs_obstructions import add_star, cordial, is_preorder
from research.hub.branch_levels import odd_core, verify_tree


def example(k,r,s):
    parents = [-1]
    first = add_star(parents,0,r)
    direct = range(len(parents),k)
    parents.extend([0]*len(direct))
    second = add_star(parents,0,k-s)
    third = add_star(parents,0,s)
    assert len(parents) == 2*k and is_preorder(parents)
    return parents,direct,[first,second,third]


def ordinary(k,parents,direct,branches):
    branches = sorted(branches,key=len,reverse=True)
    counts = tuple(len(b)-1 for b in branches)
    tree = odd_core(counts)
    verify_tree(tree,counts)
    labels = [None]*len(parents)
    labels[0] = 0
    for b,(x,children) in zip(branches,tree.children.items()):
        labels[b.start] = x
        labels[b.start+1:b.stop] = children
    for i,v in enumerate(direct,1):
        labels[v] = tree.hi+i
    assert len(set(labels)) == 2*k and max(labels)-min(labels) == 2*k-1
    labels = [x%k for x in labels]
    assert cordial(k,parents,labels)


def allowed(k,r,s):
    d = gcd(k,s)
    return r % (k*gcd(d,r-1)//d) != 0


def literal(k):
    available = set(range(k))
    first = {}
    last = {}
    # The two parts depend separately on r and s. Check actual edge sums of
    # their permutations before intersecting the permitted joining labels.
    for t in range(1,k):
        parents,_,_ = example(k,t,t)
        possible = set()
        for x in range(k):
            for tail in permutations(available-{x}):
                new = (x,)+tail
                weights = [(new[j]+(new[w-k] if w>=k else 0))%k
                           for j,w in enumerate(parents[k+1:],1)]
                if len(set(weights)) == k-1:
                    possible.add(x)
                    break
        last[t] = possible
        deficits = set()
        for suffix in permutations(range(1,k)):
            word = (0,)+suffix
            weights = {(word[j]+word[parents[j]])%k for j in range(1,k)}
            if len(weights) == k-1:
                deficit, = available-weights
                deficits.add(deficit)
        first[t] = deficits
        predicted = {(-(t-1)*y)%k for y in range(1,k) if t%(k//gcd(k,y))}
        assert predicted == deficits
    failures = 0
    for r,ds in first.items():
        for s,xs in last.items():
            assert bool(ds & xs) == allowed(k,r,s)
            failures += not (ds & xs)
    return failures


if __name__ == '__main__':
    examples = total = 0
    for k in range(4,257):
        p = next((v for v in range(2,k) if k%v==0),None)
        if p is not None:
            parents,direct,branches = example(k,p,k//p)
            assert not allowed(k,p,k//p)
            ordinary(k,parents,direct,branches)
            total += len(parents)
            examples += 1
    print('ordinary labelings',examples,'vertices',total)
    for k in range(2,10):
        print('modulus, failed two-period parameter pairs',k,literal(k))

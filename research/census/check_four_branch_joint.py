"""Independently check full, padded, pruned and reduced four-branch trees."""

from collections import Counter
from itertools import combinations_with_replacement
from random import Random

from research.census.four_branch_joint import four_branch


def graph(pops, plain, root):
    branches,direct = four_branch(pops,plain)
    n = 4+sum(pops)+plain
    assert len(branches)==4 and sorted(len(xs) for _,xs in branches)==sorted(pops)
    assert len(direct)==plain
    labels = [root]+[(v+root)%n for v,_ in branches]
    parent = [-1,0,0,0,0]
    for i,(_,tips) in enumerate(branches,1):
        labels.extend((x+root)%n for x in tips)
        parent.extend([i]*len(tips))
    labels.extend((x+root)%n for x in direct)
    parent.extend([0]*len(direct))
    return labels,parent


def verify(pops, plain, root=0, modulus=None):
    f,par = graph(pops,plain,root)
    n = len(f)-1
    k = modulus or n
    V = Counter(x%k for x in f[1:])
    E = Counter((f[i]+f[par[i]])%k for i in range(1,n+1))
    assert n%k==0 and V==E==Counter({x:n//k for x in range(k)})


def partial(pops, plain, k, c, d):
    """Pad one positive population, then restrict actual original edges."""
    n = 4+sum(pops)+plain
    diff = k-n
    assert diff>0
    extended = list(pops)
    extended[-1] += diff
    f,par = graph(extended,plain,c)
    v = next(i for i in range(1,5) if par.count(i)==extended[-1])
    kids = [j for j,p in enumerate(par) if p==v]
    kids.sort(key=lambda j:(f[j]+f[v])%k!=d)
    omit = set(kids[pops[-1]:])
    ordinary = [i for i in range(1,k+1) if i not in omit]
    assert len(ordinary)==n and len({f[i] for i in ordinary})==n
    sums = [(f[i]+f[par[i]])%k for i in ordinary]
    assert d in sums and len(set(sums))==n


def main():
    full = resonance = reduced = short = 0
    for pops in combinations_with_replacement(range(1,25),4):
        for plain in (0,1,4):
            verify(pops,plain)
            full += 1
    rng = Random(1991)
    for _ in range(1500):
        a = rng.randrange(2,70)
        b = rng.randrange(a,300)
        for plain in (max(0,a-4),2*a-4,max(0,2*a-5),2*a-3):
            verify([a,b,a+b,a+b],plain,rng.randrange(1000))
            resonance += 1
        verify([a,b,b,a+b],rng.randrange(25))
        resonance += 1
        pops = [rng.randrange(1,50) for _ in range(4)]
        k = rng.randrange(2,30)
        plain = -(sum(pops)+4)%k
        verify(pops,plain,rng.randrange(k),k)
        reduced += 1
        n = 4+sum(pops)+plain
        k = n+rng.randrange(1,40)
        partial(pops,plain,k,rng.randrange(k),rng.randrange(k))
        short += 1
    print(f"{full} full blocks, {resonance} sum-family blocks, {reduced} proper-divisor "
          f"reductions, and {short} prescribed short extensions.")


if __name__ == '__main__':
    main()

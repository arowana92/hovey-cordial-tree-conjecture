"""Check simultaneous insertion of arbitrary prescribed coefficient orbits at a prime power."""
from collections import Counter
from itertools import product
from math import gcd
from random import Random

from .check_period_chains import exact_sums,multipliers


def accepts(k,p,weights,chains):
    """Return whether unit scalings of the given coefficients can keep the core balanced."""
    if k<2 or p<2 or any(p%d==0 for d in range(2,int(p**0.5)+1)):
        raise ValueError('expected a prime power')
    powers=[1]
    while powers[-1]<k:
        powers.append(p*powers[-1])
    if powers[-1]!=k:
        raise ValueError('expected a prime power')
    if len(weights)!=len(chains):
        raise ValueError('one coefficient sequence per edge required')
    # At level j, a moving edge must leave its child class modulo p^(j+1)
    # while remaining in the same parent class modulo p^j.
    moves=[[0]*size for size in powers[1:]]
    free=[[0]*size for size in powers[:-1]]
    fixed=[0]*k
    levels={size:j for j,size in enumerate(powers[:-1])}
    for w,chain in zip(weights,chains):
        w%=k
        ds=[gcd(c,k) for c in chain]
        divisor=min(ds,default=k)
        if divisor==k:
            fixed[w]+=1
            continue
        j=levels[divisor]
        count=ds.count(divisor)
        if (p==2 and count%2) or count==1:
            moves[j][w%powers[j+1]]+=1
        else:
            level=j+int(p==2)
            if level==len(free):
                fixed[w]+=1
            else:
                free[level][w%powers[level]]+=1
    q,r=divmod(len(weights),k)
    low=[max(0,q-f) for f in fixed]
    high=[q+bool(r)-f for f in fixed]
    if any(u<0 for u in high):
        return False
    for j in reversed(range(len(moves))):
        width=powers[j]
        next_low,next_high=[],[]
        for parent in range(width):
            children=range(parent,p*width,width)
            m=free[j][parent]+sum(moves[j][i] for i in children)
            capacity=sum(high[i] for i in children)
            if any(moves[j][i]>capacity-high[i] for i in children):
                return False
            need=max(m,sum(low[i] for i in children),max(low[i]+moves[j][i] for i in children))
            if need>capacity:
                return False
            next_low.append(need-m)
            next_high.append(capacity-m)
        low,high=next_low,next_high
    return low[0]==0


def matching(k,weights,chains):
    # Independent lower/upper-capacity matching on literal bins, without residue classes.
    q,r=divmod(len(weights),k)
    orbits=[exact_sums(k,chain) for chain in chains]
    fixed=Counter(w for w,options in zip(weights,orbits) if options=={0})
    selected=[i for i,options in enumerate(orbits) if options!={0}]
    slots=[(w,j<q-fixed[w]) for w in range(k) for j in range(q+bool(r)-fixed[w])]
    choices=[]
    for i in selected:
        allowed={(weights[i]+d)%k for d in orbits[i]}
        choices.append([j for j,(w,_) in enumerate(slots) if w in allowed])
    choices.extend([[j for j,(_,required) in enumerate(slots) if not required]]
                   *(len(slots)-len(choices)))
    used={}
    def assign(i,seen):
        for j in choices[i]:
            if j not in seen:
                seen.add(j)
                if j not in used or assign(used[j],seen):
                    used[j]=i
                    return True
        return False
    if not all(assign(i,set()) for i in range(len(choices))):
        return None
    result=weights[:]
    for j,i in used.items():
        if i<len(selected):
            result[selected[i]]=slots[j][0]
    return result


def verify(k,p,weights,chains):
    yes=accepts(k,p,weights,chains)
    targets=matching(k,weights,chains)
    assert yes==(targets is not None)
    if yes:
        hist=Counter(targets)
        counts=[hist[v] for v in range(k)]
        assert max(counts)-min(counts)<=1
    return targets


def check():
    cases=failed=trees=pieces=0
    for n in range(8):
        weights=[(i+1)%4 for i in range(n)]
        for cs in product((0,1,2),repeat=n):
            failed+=verify(4,2,weights,[(c,) for c in cs]) is None
            cases+=1
    rng=Random(2719532)
    for k,p in ((4,2),(8,2),(9,3),(16,2),(25,5),(27,3),(32,2),(49,7)):
        divisors=sorted({gcd(x,k)%k for x in range(k)})
        for trial in range(220):
            n=rng.randrange(1,2*k+1)
            weights=[(i+1)%k for i in range(n)]
            chains=[tuple(rng.choice(divisors) for _ in range(1 if trial%2 else rng.randrange(4)))
                    for w in weights]
            destinations=verify(k,p,weights,chains)
            cases+=1
            if destinations is None:
                failed+=1
                continue
            labels=[0,*weights]
            edges=[]
            for i,(chain,w,z) in enumerate(zip(chains,weights,destinations),1):
                left=0
                for c,u in zip(chain,multipliers(k,chain,(z-w)%k)):
                    # Translate the star so its entry fills its missing weight.
                    start=len(labels)
                    labels.extend((labels[left]+u*x)%k for x in range(k))
                    edges.extend((start,start+j) for j in range(1,k))
                    edges.append((left,start))
                    left=start+c
                    pieces+=1
                edges.append((left,i))
            assert len(labels)==len(edges)+1
            for hist in (Counter(labels),Counter((labels[a]+labels[b])%k for a,b in edges)):
                bins=[hist[v] for v in range(k)]
                assert max(bins)-min(bins)<=1
            trees+=1
    print('independent matching comparisons',cases,'infeasible',failed,
          'ordinary expansions',trees,'inserted pieces',pieces)


if __name__=='__main__':
    check()

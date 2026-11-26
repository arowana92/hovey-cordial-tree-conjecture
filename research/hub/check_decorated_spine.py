"""Check the window criterion, expanded tree shapes, and all actual modular sums."""

from collections import Counter
from itertools import accumulate
from random import Random

from research.hub.decorated_spine import construct, path_values, SLOPES


def determinant(matrix):
    """Fraction-free elimination over the integers."""
    a = [row[:] for row in matrix]
    previous = sign = 1
    for i in range(len(a)-1):
        pivot = next((j for j in range(i,len(a)) if a[j][i]),None)
        if pivot is None:
            return 0
        if pivot!=i:
            a[i],a[pivot] = a[pivot],a[i]
            sign = -sign
        for j in range(i+1,len(a)):
            for u in range(i+1,len(a)):
                value = a[i][i]*a[j][u]-a[j][i]*a[i][u]
                assert value%previous==0
                a[j][u] = value//previous
            a[j][i] = 0
        previous = a[i][i]
    return sign*a[-1][-1]


def bridge_checks():
    # Obtain the coefficients by differencing actual vertex labels.
    k = 1000003
    count = 0
    for p in (0,1,41,k-5):
        for q in (0,2,261,k-13):
            for weight in (0,117,k-31):
                for z in (0,8,347,k-257):
                    row = path_values(p,q,weight,z,k)
                    unit = path_values(p,q,weight,z+1,k)
                    coeff = tuple((b-a+k//2)%k-k//2 for a,b in zip(row,unit))
                    assert coeff==SLOPES
                    path = [p]+row+[q]
                    assert Counter((a+b)%k for a,b in zip(path,path[1:]))==Counter(row+[weight])
                    count += 1
    matrix = [[0]*j+list(v)+[0]*(19-j) for j in range(20) for v in (coeff,coeff[::-1])]
    assert all(sum(r)==0 for r in matrix)
    minor = determinant([r[:-1] for r in matrix[1:]])
    assert minor%5==2
    # Test the ordering of every signed guard prefix, including zero totals.
    rng = Random(284)
    for _ in range(2000):
        arities = [rng.randrange(7) for _ in coeff]
        for row in (coeff,coeff[::-1]):
            terms = [a for a,m in zip(row,arities) for _ in range(m)]
            sign = -1 if sum(terms)<0 else 1
            assert all(x>0 for x in list(accumulate(sorted((a*sign for a in terms),reverse=True)))[:-1])
    return count,minor


def fixture(kind,k,variant):
    rng = Random(94+variant)
    sizes = {'starred':[43]*12,'active':[21,21,43,43],'uniform':[87]}[kind]
    n_jobs = 3
    slots = len(sizes)*n_jobs
    branches = slots+(2-slots)%4
    core = [-1,0]
    for _ in range(branches):
        core.extend([0,len(core)])
    jobs = []
    for j in range(n_jobs):
        edges = []
        for i,length in enumerate(sizes):
            shape = []
            for h in range(length):
                if kind=='starred':
                    leaves = rng.randrange(2)
                    arities = (1+rng.randrange(3),) if h==21 or rng.randrange(10)==0 else ()
                elif kind=='uniform':
                    leaves,arities = (variant+j)%3,()
                elif i==0:
                    # The first orientation vanishes, and the reverse is active.
                    leaves,arities = 1+3*(h==0)+(h==7),()
                elif i==1:
                    leaves,arities = int(h==4),()
                else:
                    leaves,arities = rng.randrange(4),()
                shape.append((leaves,arities))
            index = j*len(sizes)+i
            child = 2+2*index+(index+variant)%2
            edges.append((child,shape))
        jobs.append((kind,edges))
    ordinary = len(core)+sum(1+l+sum(1+m for m in stars) for _,edges in jobs
                             for _,profile in edges for l,stars in profile)
    return core,{0:k-ordinary-2,1:2},jobs


def check_shape(core,counts,jobs,parents):
    ordinary = len(parents)-sum(counts.values())
    kids = [[] for _ in range(ordinary)]
    for v in range(1,ordinary):
        kids[parents[v]].append(v)
    assigned = set(range(len(core)))
    original = list(parents[:len(core)])
    for _,edges in jobs:
        for child,profile in edges:
            left = core[child]
            path = []
            v = parents[child]
            while v!=left:
                assert len(path)<len(profile) and v not in assigned
                path.append(v)
                assigned.add(v)
                v = parents[v]
            path.reverse()
            original[child] = left
            assert len(path)==len(profile)
            for v,next_v,(l,arities) in zip(path,path[1:]+[child],profile):
                side = [w for w in kids[v] if w!=next_v]
                assert sum(not kids[w] for w in side)==l
                assert sorted(len(kids[w]) for w in side if kids[w])==sorted(arities)
                for w in side:
                    assert w not in assigned
                    assigned.add(w)
                    for tip in kids[w]:
                        assert tip not in assigned and not kids[tip]
                        assigned.add(tip)
    assert original==core and len(assigned)==ordinary
    assert Counter(parents[ordinary:])==Counter(counts)


def main():
    count,minor = bridge_checks()
    print(f"{count} weighted paths and slope vectors. Integer minor mod 5 is {minor%5}.",flush=True)
    cases = edges = repairs = neutral = cycles = 0
    for variant,k in enumerate((262139,262140,262144)):
        for kind in ('active','uniform','starred'):
            core,counts,jobs = fixture(kind,k,variant)
            parents,labels,gap,stats = construct(core,counts,jobs,k,range(k),seed=37+variant)
            check_shape(core,counts,jobs,parents)
            assert len(parents)==len(labels)==k
            seen = bytearray(k)
            weights = bytearray(k)
            for v,x in enumerate(labels):
                assert 0<=x<k and not seen[x]
                seen[x] = 1
                if v:
                    y = (x+labels[parents[v]])%k
                    assert not weights[y]
                    weights[y] = 1
            assert not weights[gap] and weights.count(0)==1
            assert stats['repairs']==2 and stats['neutral']==1
            cases += 1
            edges += k-1
            repairs += stats['repairs']
            neutral += stats['neutral']
            cycles += stats['root cycles']+stats['leaf cycles']
    print(f"{cases} complete trees, {edges:,} endpoint sums, {repairs} surplus and "
          f"{neutral} neutral jobs, {cycles} translated cycles.")


if __name__=='__main__':
    main()

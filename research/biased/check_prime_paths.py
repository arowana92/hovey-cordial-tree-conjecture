"""Recount signed permutations and independently check biased blocks and subdivisions."""

from itertools import permutations,product
from random import Random

from research.biased.prime_paths import block, path, pendant, subdivision


def sign(xs):
    return (-1)**sum(x>y for i,x in enumerate(xs) for y in xs[i+1:])


def direct(coeff, offset):
    p = len(coeff)
    total = 0
    for rest in permutations(range(1,p)):
        x = (0,*rest)
        y = [(offset[i]+sum(a*x[(i+j)%p] for j,a in enumerate(coeff)))%p for i in range(p)]
        if len(set(y))==p:
            total += sign(x)*sign(y)
    return total%p


def check_offsets():
    rng = Random(2509)
    count = 0
    for p in (3,5,7):
        if p==3:
            matrices = list(product(range(p),repeat=p))
        elif p==5:
            matrices = [(1,1,0,0,0),(1,3,2,0,1),(0,0,2,0,0)]
        else:
            matrices = [[rng.randrange(p) for _ in range(p)] for _ in range(14)]
        for a in matrices:
            A = sum(a)%p
            if not A:
                continue
            offsets = (product(range(p),repeat=p-1) if p<=5 else
                       [tuple(rng.randrange(p) for _ in range(p-1)) for _ in range(4)])
            for row in offsets:
                b = (-sum(row)%p,*row)
                expected = -sign([(A*i)%p for i in range(p)])%p
                assert direct(a,b)==expected
                count += 1
    return count


def balanced(xs,p):
    counts = [xs.count(i) for i in range(p)]
    return max(counts)-min(counts)<=1


def main():
    rng = Random(1909)
    checks = check_offsets()
    paths = closed = inserts = 0
    for p in (2,3,5,7,11,13,17,19,23):
        for n in (1,p-1,p,p+1,2*p,3*p+4):
            offsets = [rng.randrange(-p,2*p) for _ in range(n-1)]
            f = path(p,offsets)
            assert len(f)==n
            w = [(a+b+c)%p for a,b,c in zip(f,f[1:],offsets)]
            assert balanced(f,p) and balanced(w,p)
            paths += 1
        for _ in range(12):
            offsets = [rng.randrange(p) for _ in range(p)]
            u,v = rng.randrange(p),rng.randrange(p)
            s = sum(range(p))%p
            full = pendant(p,u,offsets)
            assert sorted(full)==list(range(p)) and full[-1]==(u+sum(offsets)-s)%p
            extra = rng.randrange(p)
            chain = [u,*full,v]
            w = [(a+b+c)%p for a,b,c in zip(chain,chain[1:],offsets+[extra])]
            assert sorted(w)==sorted([*range(p),(u+v+sum(offsets)+extra-s)%p])
            inserts += 1
            if p>2:
                f,_ = block(p,offsets[1:])
                offsets[0] = -sum(offsets[1:])%p
                assert len({(f[i-1]+f[i]+b)%p for i,b in enumerate(offsets)})==p
                closed += 1
    trees = 0
    for p in (2,3,5,7,11,17):
        for h in range(2,18):
            E = [(rng.randrange(i),i) for i in range(1,h)]
            B = [[rng.randrange(p) for _ in range(rng.randrange(p-1,2*p+2))] for _ in E]
            f = subdivision(p,h,E,B)
            weights = []
            n = h
            for (u,v),bs in zip(E,B):
                seq = [u,*range(n,n+len(bs)-1),v]
                n += len(bs)-1
                weights.extend((f[a]+f[b]+c)%p for a,b,c in zip(seq,seq[1:],bs))
            assert len(f)==n and len(weights)==n-1 and balanced(f,p) and balanced(weights,p)
            trees += 1
    print(f"{checks} signed circulant counts, {paths} whole paths, {closed} cycles, {inserts} edge replacements, {trees} subdivided trees.")


if __name__=='__main__':
    main()

"""Independent checks of the signed lift count, character sum, and actual cover trees."""

from itertools import permutations,product
from random import Random

from research.biased.cyclic_covers import criterion,lift
from research.biased.check_prime_paths import sign


def direct(blocks,b,p):
    m = len(blocks)
    perms = [(0,*q) for q in permutations(range(1,p))]
    total = 0
    for inputs in product(perms,repeat=m):
        epsilon = 1
        for x in inputs:
            epsilon *= sign(x)
        for s,row in enumerate(blocks):
            y = [(b[s][i]+sum(a*inputs[r][(i+j)%p] for r,j,a in row))%p for i in range(p)]
            if len(set(y))!=p:
                break
            epsilon *= sign(y)
        else:
            total += epsilon
    return total%p


def coefficient(blocks,p):
    m,h = len(blocks),(p-1)//2
    zero = (0,)*m
    poly = {zero:1}
    for row in blocks:
        S = [sum(a for j,_,a in row if j==r)%p for r in range(m)]
        for _ in range(h):
            new = {}
            for powers,c in poly.items():
                for i,a in enumerate(S):
                    if a and powers[i]<h:
                        q = (*powers[:i],powers[i]+1,*powers[i+1:])
                        new[q] = (new.get(q,0)+a*c)%p
            poly = new
    return (-1)**m*poly.get((h,)*m,0)%p


def verify_tree(p,low,edges,offsets,deleted,lows):
    m = len(low)
    label = lift(p,low,edges,offsets,deleted,lows)
    assert label is not None
    K = m*p
    assert sorted(x for row in label for x in row)==list(range(K))
    adj = [set() for _ in range(K)]
    weights = []
    for e,(u,v,t) in enumerate(edges):
        for i in range(p):
            if (e,i)==deleted:
                continue
            j = (i+t)%p
            a,b = p*u+i,p*v+j
            adj[a].add(b)
            adj[b].add(a)
            weights.append((label[u][i]+label[v][j]+lows[e]+m*offsets[e][i])%K)
    seen,stack = {0},[0]
    while stack:
        for v in adj[stack.pop()]-seen:
            seen.add(v)
            stack.append(v)
    assert len(seen)==K and len(weights)==len(set(weights))==K-1


def main():
    rng = Random(2017)
    cases = trees = traces = 0
    for p,m,tries in ((3,1,30),(3,3,40),(3,5,30),(5,2,31),(7,1,16)):
        for _ in range(tries):
            blocks = [[(rng.randrange(m),rng.randrange(p),rng.randrange(1,p))
                       for j in range(rng.randrange(1,7))] for s in range(m)]
            b = [[rng.randrange(p) for i in range(p-1)] for s in range(m)]
            for row in b:
                row.append(-sum(row)%p)
            assert direct(blocks,b,p)==coefficient(blocks,p)
            cases += 1
    for p in (3,5,7,11,13):
        for m in range(1,7):
            for n in range(m,m+3):
                E = [(i,(i+1)%m) for i in range(m)] + [(i-1,i) for i in range(m,n)]
                # Evaluate the multiplicative-character transfer on a cycle
                # by its (p-1)-state matrix, with no binomial coefficients.
                chars = [0]+[sign([(x*i)%p for i in range(p)]) for x in range(1,p)]
                K = [[chars[x]*chars[(x+y)%p]%p for y in range(1,p)] for x in range(1,p)]
                A = [[int(i==j) for j in range(p-1)] for i in range(p-1)]
                for i in range(m):
                    A = [[sum(A[x][z]*K[z][y] for z in range(p-1))%p
                          for y in range(p-1)] for x in range(p-1)]
                expected = (-1)**(n-m)*sum(A[i][i] for i in range(p-1))%p
                assert expected==(-1)**n*criterion(p,m)%p
                if p*m<=40:
                    assert expected==coefficient([[(u,0,1),(v,0,1)] for u,v in E],p)
                traces += 1
    for p in (3,5,7):
        for m in range(1,8):
            for l in range(1,m+1):
                if not criterion(p,l):
                    continue
                low = list(range(m))
                edges = [(i,(i+1)%l,int(i==l-1)) for i in range(l)]
                edges += [(rng.randrange(i),i,rng.randrange(p)) for i in range(l,m)]
                lows = [(e-low[u]-low[v])%m for e,(u,v,_) in enumerate(edges)]
                offsets = [[rng.randrange(p) for i in range(p-1)] for _ in range(m)]
                for row in offsets:
                    row.append(-sum(row)%p)
                    rng.shuffle(row)
                deleted = (rng.randrange(l),rng.randrange(p))
                offsets[deleted[0]][deleted[1]]=p+9
                verify_tree(p,low,edges,offsets,deleted,lows)
                if m>1:
                    other = (deleted[0]+1)%m
                    offsets[other][0]+=1
                    assert lift(p,low,edges,offsets,deleted,lows) is None
                trees += 1
    print(f"{cases} block-circulant signed counts, {traces} cycle character traces, {trees} lifted trees.")


if __name__=='__main__':
    main()

"""Rebuild actual joint edges, including restrictions at a prescribed deficit."""

from collections import Counter
from random import Random
from research.census.scaled_joints import construct,plan


def check(block,direct,n):
    vertices = [z for z,_ in block]+[v for _,xs in block for v in xs]+direct
    weights = [z for z,_ in block]+[z+v for z,xs in block for v in xs]+direct
    assert len(vertices)==n and len(set(vertices))==n
    assert sorted(vertices)==sorted(weights)==list(range(min(vertices),min(vertices)+n))
    return vertices,weights


def main():
    rng = Random(2608)
    cases = short = reductions = 0
    for m in range(3,24):
        groups = []
        next_id = 1
        if m%2==0:
            groups.append([1,2,3])
            next_id = 4
        groups.extend([j,j+1] for j in range(next_id,m,2))
        for t in range(14):
            counts = [rng.randrange(1,25)]
            for group in groups:
                mult = rng.randrange(1,13)
                base = [1]*len(group) if t%5==0 else [rng.randrange(1,10) for _ in group]
                counts.extend(mult*a for a in base)
            spec,blocks,B = plan(counts,groups)
            L = max(sum(s) for _,s,_,_,_ in blocks)
            plain = max(0,B+L-counts[0])+rng.randrange(20)
            full = m+sum(counts)+plain
            for n in (m,m+1,rng.randrange(m,full+1),full-1,full):
                block,direct = construct(counts,groups,plain,n)
                assert len(direct)<=plain
                assert all(len(xs)<=a for (_,xs),a in zip(block,counts))
                vertices,weights = check(block,direct,n)
                if n==full:
                    assert len(direct)==plain and [len(xs) for _,xs in block]==counts
                for k in (1,2,3,5,7,11):
                    if n%k==0:
                        joint = rng.randrange(k)
                        assert Counter((x+joint)%k for x in vertices)==Counter({i:n//k for i in range(k)})
                        assert Counter((y+2*joint)%k for y in weights)==Counter({i:n//k for i in range(k)})
                        reductions += 1
                cases += 1
            k = full+rng.randrange(1,10)
            block,direct = construct(counts,groups,plain,k)
            check(block,direct,k)
            first,second = [p for p,_ in block], [p for p,_ in block]
            for z,xs in block:
                first.extend(xs)
                second.extend(z+v for v in xs)
            first.extend(direct[:plain])
            second.extend(direct[:plain])
            for d in direct[plain:]:
                original = block[0][1][0]
                V,W=first.copy(),second.copy()
                V[V.index(original)] = W[W.index(original)] = d
                assert len({x%k for x in V})==len({x%k for x in W})==full
                assert d%k in {x%k for x in W}
                short += 1
    print(f"{cases} interval prefixes, {reductions} divisor checks, {short} padded deficit restrictions.")


if __name__=='__main__':
    main()

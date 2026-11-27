"""Compare the attachment test with exhaustive choices, then check actual tree sums."""

from itertools import accumulate, permutations, product
from random import Random

from research.census.chain_stars import chain_stars


def brute(sizes, joins):
    # Assign unrestricted local permutations until all actual joining sums fit.
    def grow(i, previous):
        for p in permutations(range(sizes[i])):
            if i and p[joins[i-1][1]]+previous != sizes[i-1]-1:
                continue
            if i+1 == len(sizes) or grow(i+1,p[joins[i][0]]):
                return True
        return False
    return grow(0,0)


def audit(sizes, joins, exact):
    witness = chain_stars(sizes,joins)
    if exact:
        assert bool(witness) == brute(sizes,joins)
    if all(a <= b for a,b in zip(sizes,sizes[1:])):
        assert witness
    if witness is None:
        return False
    labels,reported = witness
    starts = [0,*accumulate(a+1 for a in sizes)]
    edges = {(s,s+j+1) for a,s in zip(sizes,starts) for j in range(a)}
    edges.update((starts[i]+x+1,starts[i+1]+y+1) for i,(x,y) in enumerate(joins))
    assert edges == set(reported) and len(edges) == starts[-1]-1
    assert sorted(labels) == list(range(starts[-1]))
    A = sum(sizes[::2])+len(sizes)//2
    assert all((labels[v]<A) != (labels[u]<A) for u,v in edges)
    assert sorted(labels[u]+labels[v] for u,v in edges) == list(range(A,A+len(edges)))
    return True


if __name__ == "__main__":
    total = solved = 0
    for q in range(1,7):
        for sizes in product(range(1,4),repeat=q):
            for split in product(*[range(min(a,2)) for a in sizes[1:-1]]):
                joins = [(split[i-1] if i else 0,0) for i in range(q-1)]
                solved += audit(sizes,joins,True)
                total += 1
    print(f"{total} small size/port patterns checked against independent exhaustive permutations, "
          f"{solved} forward block labelings")
    rng = Random(1991)
    for _ in range(320):
        sizes = sorted(rng.randint(1,60) for _ in range(rng.randint(2,75)))
        joins = [(rng.randrange(a),rng.randrange(b)) for a,b in zip(sizes,sizes[1:])]
        assert audit(sizes,joins,False)
    print("320 monotone chains with independently chosen actual attachment leaves checked")

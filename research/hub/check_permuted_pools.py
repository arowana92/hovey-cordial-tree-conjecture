"""Independent finite checks of the quota repair and its use on actual tree edges."""

from collections import Counter
from fractions import Fraction
from itertools import permutations,product
from random import Random

from research.hub.permuted_pools import assign_leaves,round_counts
from research.hub.two_hub_contraction import complete


def coupling_check():
    # Two coordinates suffice for a nontrivial permutation. Check the *joint*
    # four-bit law of a factor, including cross-coordinate independence.
    for g in (Fraction(1,8),Fraction(1,3),Fraction(1,2)):
        catalog = [(0,0,1-2*g),(1,1,g*g),(1,2,g-g*g),
                   (2,1,g-g*g),(2,2,g*g)]
        for perm in ((0,1),(1,0)):
            for factor in (1,2):
                hist = Counter()
                for first,second in product(catalog,repeat=2):
                    rows = (first,second)
                    bits = tuple(int(row[0]==factor) for row in rows)
                    cols = tuple(int(rows[perm[i]][1]==factor) for i in range(2))
                    hist[bits+cols] += first[2]*second[2]
                for vec in product((0,1),repeat=4):
                    assert hist[vec]==g**sum(vec)*(1-g)**(4-sum(vec))


def hall_check():
    # Independently check every zero-sum multiset is represented at these orders.
    checked = 0
    for k in range(2,9):
        realized = {tuple(sorted((y-x)%k for x,y in enumerate(row)))
                    for row in permutations(range(k))}
        def visit(prefix,low,need):
            nonlocal checked
            if need==1:
                last = -sum(prefix)%k
                if last>=low:
                    assert tuple(prefix+[last]) in realized
                    checked += 1
                return
            for i in range(low,k):
                visit(prefix+[i],i,need-1)
        visit([],0,k)
    return checked


def random_checks():
    rng = Random(6527)
    fixes = moves = trials = 0
    for k in (127,256,441,503,840,1009):
        for trial in range(20):
            # A piecewise rotation gives an explicit nontrivial Hall witness.
            # The displacement at a wrap is also included as its own demand.
            pi = []
            left = 0
            for width in (k//7,k//5,k//4,k-k//7-k//5-k//4):
                p = rng.randrange(1,width)
                pi.extend(left+(i+p)%width for i in range(width))
                left += width
            full = Counter((y-i)%k for i,y in enumerate(pi))
            counts = {p:round(w*0.38) for p,w in full.items() if round(w*0.38)}
            rounded = round_counts(counts,k)
            m = sum(counts.values())
            assert sum(rounded.values())==k and all(abs(b*m-counts[p]*k)<=m for p,b in rounded.items())
            sample = {x for x in range(k) if rng.random()<0.57}
            fixed_v = set(rng.sample(range(k),max(3,k//64)))
            fixed_c = set(rng.sample(range(k),max(3,k//64)))
            moment = rng.randrange(k)
            legs,A,C,s,(f,r) = assign_leaves(k,pi,counts,sample,fixed_v,fixed_c,moment,trial%k)
            assert {p:len(xs) for p,xs in legs.items() if xs}==counts
            slots = [x for xs in legs.values() for x in xs]
            edge = [(x+p)%k for p,xs in legs.items() for x in xs]
            assert sorted(slots+list(A))==sorted(edge+list(C))==list(range(k))
            assert fixed_v<=A and fixed_c<=C and s in C-fixed_c
            shift = sum(p*len(xs) for p,xs in legs.items())
            assert (sum(C)-sum(A)+shift)%k==0
            assert (2*sum(A)-moment-sum(C)+s)%k==0
            fixes += f
            moves += r
            trials += 1
    assert fixes and moves
    return trials,fixes,moves


def actual_edges():
    # Each fixture is built from an integer interval certificate. Its extra
    # leaves at the two hubs are stripped before the core equations are audited.
    count = 0
    for d in (7,12,19,30):
        tree = [-1]+list(range(d))
        labels,interval,_ = complete(tree,0,d)
        old = [(p,i) for i,p in enumerate(tree) if i]
        extra = [(p,x) for p,a,b in interval.blocks for x in range(a,b)]
        for m0,m1 in ((8,17),(31,12),(3,29)):
            leaves = extra+[(0,x) for x in range(interval.hi+1,interval.hi+m0+1)]
            leaves += [(1,x) for x in range(interval.lo-m1,interval.lo)]
            k = len(tree)+len(leaves)
            X = [v%k for v in labels]
            core_weights = [(X[u]+X[v])%k for u,v in old]
            all_v = X+[x%k for _,x in leaves]
            all_e = core_weights+[(p+x)%k for p,x in leaves]
            assert sorted(all_v)==list(range(k)) and len(set(all_e))==k-1
            gap, = set(range(k))-set(all_e)
            C = set(core_weights)|{gap}
            shift = sum(p for p,_ in leaves)
            assert (sum(C)-sum(X)+shift)%k==0
            # Split the path into two vertex chains, retaining the edge between
            # the chains. The endpoints of each chain are counted with multiplicity.
            cut = len(X)//2
            fixed_weight = (X[cut-1]+X[cut])%k
            ends = X[0]+X[cut-1]+X[cut]+X[-1]
            # Each chain's weights sum to twice its vertex sum minus its endpoints.
            assert (sum(C)-gap-fixed_weight-2*sum(X)+ends)%k==0
            assert gap==(ends-fixed_weight-sum(X)-shift)%k
            count += 1
    return count


if __name__=='__main__':
    coupling_check()
    print(f"{hall_check():,} zero-sum displacement multisets at moduli 2–8.")
    t,f,r = random_checks()
    print(f"{t} prime/composite pool replays, {f:,} deficit arcs and {r} omitted-weight repairs.")
    print(f"{actual_edges()} labeled trees checked on their actual edges; both permuted two-coordinate laws verified.")

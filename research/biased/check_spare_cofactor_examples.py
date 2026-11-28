"""Exact coefficient checks and whole-tree replays for the leaf list results."""
from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations
from random import Random



def circulants():
    checked = 0
    for q in (2,3,4,5,7,8,9):
        coefficients = Counter()
        for perm in permutations(range(q)):
            monomial = tuple(sorted((x-i)%q for i,x in enumerate(perm)))
            inversions = sum(x>y for x,y in combinations(perm,2))
            coefficients[monomial] += (-1)**inversions
        expected = {a for a in combinations_with_replacement(range(q),q) if sum(a)%q==0}
        assert expected == {a for a,c in coefficients.items() if c}
        checked += len(expected)
    return checked


def integer_cofactor(shifts, multiplicities, omitted):
    # Coefficients of 1,z,...,z^26 before imposing the cyclotomic relation.
    zero = (0,)*len(shifts)
    counts = {zero:[1]+[0]*26}
    for j in range(sum(multiplicities)+1):
        if j==omitted:
            continue
        new = {}
        for exps, histogram in counts.items():
            for i,s in enumerate(shifts):
                if exps[i]==multiplicities[i]:
                    continue
                nxt = exps[:i]+(exps[i]+1,)+exps[i+1:]
                dest = new.setdefault(nxt,[0]*27)
                delta = j*s % 27
                for h,v in enumerate(histogram):
                    dest[(h+delta)%27] += v
        counts = new
    return counts[multiplicities]


def exact_examples():
    # A size-17 case that vanishes in characteristic 487 for all deleted columns.
    shifts = [0,3,6,9,12,18]
    profile = (3,4,4,3,1,2)
    nonzero = 0
    for j in range(18):
        a = integer_cofactor(shifts,profile,j)
        assert sum(n*pow(19,i,487) for i,n in enumerate(a))%487==0
        if any(a[t]!=a[t+9] or a[t]!=a[t+18] for t in range(9)):
            nonzero += 1
    assert nonzero
    return nonzero


def leaf_example(shifts,lists,rng):
    # This samples positive witnesses; the polynomial proof covers all inputs.
    for _ in range(2000):
        sources, destinations = set(), set()
        choices = {}
        remaining = set(range(len(lists)))
        while remaining:
            def options(i):
                return [x for x in lists[i] if x not in sources and (x+shifts[i])%27 not in destinations]
            candidates, row = min(((options(i),i) for i in remaining),
                                  key=lambda pair:(len(pair[0]),pair[1]))
            if not candidates:
                break
            x = rng.choice(candidates)
            choices[row] = x
            sources.add(x)
            destinations.add((x+shifts[row])%27)
            remaining.remove(row)
        if not remaining:
            return [choices[i] for i in range(len(lists))]
    raise AssertionError("whole-tree example lacks a witness")


def trees():
    rng = Random(27)
    joined = Counter()
    for h in range(2,7):
        n = 27+h
        path = [(i//2+((n+1)//2 if i%2 else 0))%27 for i in range(n)]
        old_edges = list(zip(range(n-1),range(1,n)))
        weights = Counter((path[i]+path[j])%27 for i,j in old_edges)
        high_e = {w for w in weights if weights[w]==2}
        high_v = {v for v in path if path.count(v)==2}
        assert len(high_v)==h and len(high_e)==h-1
        r = 27-2*h
        for size in range(1,8):
            for _ in range(8):
                parents = rng.sample(range(27),size)
                shifts = parents+[rng.choice(parents) for _ in range(r-size)]
                rng.shuffle(shifts)
                lists = []
                for s in shifts:
                    allowed = [x for x in range(27) if x not in high_v and (s+x)%27 not in high_e]
                    lists.append(rng.sample(allowed,r+1))
                leaves = leaf_example(shifts,lists,rng)
                assert all(x in a for x,a in zip(leaves,lists))
                labels = path+list(leaves)
                edges = old_edges+[(path.index(s),n+i) for i,s in enumerate(shifts)]
                for hist in (Counter(labels),Counter((labels[x]+labels[y])%27 for x,y in edges)):
                    assert max(hist[x] for x in range(27))-min(hist[x] for x in range(27))<=1
                joined[len(labels)] += 1
    return dict(sorted(joined.items()))


if __name__ == '__main__':
    print('nonzero circulant monomials',circulants())
    print('nonzero exact cofactors in the size-17 example',exact_examples())
    print('whole trees by order',trees())

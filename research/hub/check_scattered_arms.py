"""Integer incompatibility certificates and a direct search for pinned two-edge arms."""

from itertools import permutations
from math import gcd
from functools import reduce


def equations(parents,s,t,matching):
    n = 2*len(parents)
    rows = []
    for j,v in enumerate(matching):
        row = [0]*(n+1)
        rhs = s if v == n else 0
        if j < n:
            row[2*(j//2)] = 1
            if j % 2:
                row[j] = 1
            else:
                rhs -= parents[j//2]
        elif j == n:
            rhs -= t
        else:
            row[n] = 1
        if v < n:
            row[v] -= 1
        rows.append((row,rhs))
    return rows


def annihilators(rows):
    """Carry integer multipliers throughout elimination, including every normalization."""
    columns = len(rows[0][0])
    pivots = {}
    for j,(source,_) in enumerate(rows):
        row = source+[int(i == j) for i in range(len(rows))]
        for i in range(columns):
            if not row[i]:
                continue
            if i not in pivots:
                pivots[i] = row
                break
            pivot = pivots[i]
            a,b = pivot[i],row[i]
            row = [a*x-b*y for x,y in zip(row,pivot)]
            common = reduce(gcd,row,0)
            if common > 1:
                row = [x//common for x in row]
        else:
            yield row[columns:]


def uniform_check(parents,s,t):
    n = 2*len(parents)
    bound = matchings = 0
    for sigma in permutations(range(n+2)):
        rows = equations(parents,s,t,sigma)
        for lam in annihilators(rows):
            value = sum(a*c for a,(_,c) in zip(lam,rows))
            if value:
                # Recheck the claimed integer relation against the original matrix.
                assert all(sum(a*r[i] for a,(r,_) in zip(lam,rows)) == 0 for i in range(n+1))
                bound = max(bound,abs(value))
                break
        else:
            raise ValueError(f"matching {sigma} has no integer incompatibility")
        matchings += 1
    return matchings,bound


def direct(k,parents,s,t):
    """Try every injection on the arms. At order k all remaining root leaves are forced as a set."""
    a = (t-s) % k
    core = {0,*parents,a,s}
    base_weights = [*parents,a,t]
    assert len(core) == len(parents)+3 and len(set(base_weights)) == len(base_weights)
    rest = set(range(k))-core
    tried = 0
    for labels in permutations(rest,2*len(parents)):
        tried += 1
        weights = list(base_weights)
        for i,p in enumerate(parents):
            x,y = labels[2*i:2*i+2]
            weights.extend(((p+x) % k,(x+y) % k))
        weights.extend(rest-set(labels))
        assert len(weights) == k-1
        if len(set(weights)) == k-1:
            return tried,labels
    return tried,None


def main():
    total = 0
    for parents,s,t,expected in (((1,),7,19,39),((1,7),24,61,259),
                                  ((1,11,127),1601,19013,152635)):
        count,bound = uniform_check(parents,s,t)
        assert bound == expected and max(*parents,s,t) <= bound
        total += count
        noun = "arm" if len(parents) == 1 else "arms"
        print(f"{len(parents)} {noun}, {count:,} matchings, obstruction for all k > {bound:,}.")
    tried = 0
    for k,parents,s,t in ((8,(1,),2,5),(13,(1,2),6,3),(13,(1,2,3),4,10)):
        n,solution = direct(k,parents,s,t)
        assert solution is None
        tried += n
    for k,parents,s,t in ((8,(1,),2,7),(13,(1,2),3,7),(13,(1,2,3),4,9)):
        assert direct(k,parents,s,t)[1] is not None
    print(f"{total:,} integer certificates, {tried:,} injections rejected on three small "
          "prefixes, and a cordial completion for the same three trees with other prefixes.")


if __name__ == '__main__':
    main()

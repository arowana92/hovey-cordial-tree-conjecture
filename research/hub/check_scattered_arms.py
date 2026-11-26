"""Integer incompatibility certificates and a direct search for pinned two-edge arms."""

from itertools import permutations
from math import gcd
from functools import reduce


def branch_edges(parents,arities):
    edges = []
    for p,m in zip(parents,arities):
        root = len(edges)
        edges.append((None,p))
        edges.extend((root,0) for _ in range(m))
    return edges


def equations(edges,s,t,matching):
    n = len(edges)
    rows = []
    for j,v in enumerate(matching):
        row = [0]*(n+1)
        rhs = s if v == n else 0
        if j < n:
            parent,fixed = edges[j]
            row[j] = 1
            if parent is None:
                rhs -= fixed
            else:
                row[parent] += 1
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


def uniform_check(parents,s,t,arities=None):
    edges = branch_edges(parents,arities or [1]*len(parents))
    n = len(edges)
    bound = matchings = 0
    for sigma in permutations(range(n+2)):
        rows = equations(edges,s,t,sigma)
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


def direct(k,parents,s,t,arities=None):
    """Try every injection on the arms. At order k all remaining root leaves are forced as a set."""
    a = (t-s) % k
    core = {0,*parents,a,s}
    base_weights = [*parents,a,t]
    assert len(core) == len(parents)+3 and len(set(base_weights)) == len(base_weights)
    rest = set(range(k))-core
    tried = 0
    edges = branch_edges(parents,arities or [1]*len(parents))
    for labels in permutations(rest,len(edges)):
        tried += 1
        weights = list(base_weights)
        weights.extend((x+(labels[u] if u is not None else fixed)) % k
                       for x,(u,fixed) in zip(labels,edges))
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
    for parents,arities,s,t,expected in (((1,),(4,),7,19,96),
                                         ((1,11),(1,2),127,1601,9629),
                                         ((1,11),(2,2),127,1601,14443)):
        count,bound = uniform_check(parents,s,t,arities)
        assert bound == expected and max(*parents,s,t) <= bound
        total += count
        print(f"Star arities {arities}, {count:,} matchings, obstruction for all k > {bound:,}.")
    tried = 0
    for arities,s,t in (((1,2),4,7),((2,2),5,12)):
        n,solution = direct(13,(1,2),s,t,arities)
        assert solution is None and direct(13,(1,2),3,7,arities)[1] is not None
        tried += n
    for k,parents,s,t in ((8,(1,),2,5),(13,(1,2),6,3),(13,(1,2,3),4,10)):
        n,solution = direct(k,parents,s,t)
        assert solution is None
        tried += n
    for k,parents,s,t in ((8,(1,),2,7),(13,(1,2),3,7),(13,(1,2,3),4,9)):
        assert direct(k,parents,s,t)[1] is not None
    print(f"{total:,} integer certificates, {tried:,} injections rejected on five small "
          "prefixes, and a cordial completion for the same five trees with other prefixes.")


if __name__ == '__main__':
    main()

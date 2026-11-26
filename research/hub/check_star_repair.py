"""Check the original two-level branches and all actual sums of the constructed trees."""

from collections import Counter
from math import gcd
from random import Random

from research.hub.check_odd_branch_groups import append_branch
from research.hub.star_repair import construct, five_roots, repair


def nine_edge_checks():
    cases = 0
    for k in range(1,42):
        for p in range(k):
            for d in range(k):
                roots,children = five_roots(p,d)
                labels = Counter(v % k for v in roots+children)
                sums = [(p+v) % k for v in roots]+[(v+w) % k for v,w in zip(roots[1:],children)]
                assert Counter(sums) == labels
                cases += 1
    return cases


def repair_checks():
    cases = cycles = shared = 0
    rng = Random(263)
    for k in (65520,65521,65536):
        for m in (1,2,3,4,5,6,9):
            for p in (0,1,3,9):
                for s,t in ((3,41),(9,127),(137,137)):
                    gap = 0 if t == 41 else 89
                    blocked = {0,p,s,t,gap,16,255}
                    parents,labels,next_gap,n = repair(p,m,s,t,gap,k,set(blocked),rng)
                    assert len(labels) == len(set(labels)) and next_gap in labels and gap != next_gap
                    assert set(labels).isdisjoint(blocked-{t})
                    assert len(labels) == (25 if p else 5)*(m+1)
                    expected = [u for j in range(0,len(labels),m+1) for u in [-1]+[j]*m]
                    assert parents == expected
                    edges = Counter((x+(p if u < 0 else labels[u])) % k for x,u in zip(labels,parents))
                    assert edges+Counter([t,next_gap]) == Counter(labels)+Counter([s,gap])
                    cycles += n
                    shared += gcd(m,k) > 1
                    cases += 1
    return cases,cycles,shared


def main():
    equations = nine_edge_checks()
    transfers,cycles,shared = repair_checks()
    count = edges = shifts = 0
    for k in (65520,65521,65536):
        for anchor in (0,1):
            for m in (1,2,3,6):
                for distant in (False,True):
                    core = [-1,0,1]
                    if distant:
                        append_branch(core,1,[-1]+list(range(19)))
                        mark = len(core)-1
                    else:
                        mark = 2
                    for _ in range(6):
                        append_branch(core,1,[-1,0,0])
                    number = 25*((32 if distant else 18) if anchor else (7 if distant else 4))
                    counts = {1:25,mark:12}
                    counts[0] = k-len(core)-number*(m+1)-sum(counts.values())
                    parents,labels,gap,stats = construct(core,counts,anchor,m,number,k,range(k))
                    expected = list(core)
                    for _ in range(number):
                        expected.extend([anchor]+[len(expected)]*m)
                    assert parents[:len(expected)] == expected
                    assert Counter(parents[len(expected):]) == Counter(counts)
                    assert len(parents) == len(labels) == k and set(labels) == set(range(k))
                    sums = {(labels[v]+labels[parents[v]]) % k for v in range(1,k)}
                    assert set(range(k))-sums == {gap}
                    count += 1
                    edges += k-1
                    shifts += stats['repairs']
    # Large populations at both sites, with all extra branches at the zero site.
    k = 65521
    core = [-1,0]
    number = 500
    m = 1
    counts = {1: (k-len(core)-number*2)*47//100}
    counts[0] = k-len(core)-number*2-counts[1]
    rng = Random(1)
    bins = [rng.random() < .55 for _ in range(150)]
    palette = [x for x in range(k) if bins[(300*min(x,k-x)//k) % 150]]
    parents,labels,gap,stats = construct(core,counts,0,m,number,k,palette)
    expected = core+[u for j in range(len(core),len(core)+number*2,2) for u in (0,j)]
    assert parents[:len(expected)] == expected and Counter(parents[len(expected):]) == Counter(counts)
    assert len(parents) == len(labels) == k and set(labels) == set(range(k))
    assert {(labels[v]+labels[parents[v]]) % k for v in range(1,k)} == set(range(k))-{gap}
    count += 1
    edges += k-1
    shifts += stats['repairs']
    assert cycles and shared and shifts
    print(f"{equations:,} nine-edge identities, {transfers} isolated repairs with {cycles} "
          f"erased cycles, including {shared} noncoprime cases.")
    print(f"{count} expanded trees, {edges:,} actual edge sums and {shifts:,} surplus repairs.")


if __name__ == '__main__':
    main()

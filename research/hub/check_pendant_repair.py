"""Rebuild all actual sums and check the repaired trees, including the replaced edges."""

from collections import Counter, defaultdict
from itertools import product
from random import Random

from research.hub.check_odd_branch_groups import append_branch
from research.hub.pendant_repair import bridge, construct, neutral_arm


def check_bridges():
    modular = separated = 0
    rng = Random(101)
    for k in range(2,10):
        for p,q,w,z in product(range(k),repeat=4):
            d = w-neutral_arm(p,0,3)[-1]-neutral_arm(q,0,4)[-1]
            left = neutral_arm(p,-3*d+14*z,3)
            right = neutral_arm(q,2*d-9*z,4)
            row = [x % k for x in left+right[::-1]]
            weights = [(a+b) % k for a,b in zip([p]+row,row+[q])]
            assert Counter(weights) == Counter(row)+Counter([w])
            modular += 1
    for k in (509,512,525,1009):
        for p,q in ((0,0),(0,7),(11,0),(7,7),(49,117),(k-1,1)):
            for w in (0,1,p,q,(p+q) % k,k-1):
                avoid = {p,q,18,19}
                row = bridge(p,q,w,k,avoid,rng)
                weights = [(a+b) % k for a,b in zip([p]+row,row+[q])]
                assert len(row) == len(set(row)) == 21 and avoid.isdisjoint(row)
                assert Counter(weights) == Counter(row)+Counter([w])
                separated += 1
    return modular,separated


def verify(core,anchor,length,subdivide,counts,k,palette):
    parents,labels,stats = construct(core,counts,anchor,length,k,palette,subdivide=subdivide)
    expected = list(core)+[anchor]+list(range(len(core),len(core)+length-1))
    if subdivide is not None:
        assert core[subdivide] == anchor
        expected[subdivide] = len(expected)-1
    assert expected == parents[:len(expected)]
    assert Counter(parents[len(expected):]) == Counter(counts)
    assert len(labels) == len(parents) == k and set(labels) == set(range(k))
    sums = Counter((labels[v]+labels[p]) % k for v,p in enumerate(parents) if v)
    assert set(sums) == set(range(1,k)) and all(n == 1 for n in sums.values())
    return stats


def main():
    modular,separated = check_bridges()
    counts_checked = edges = internal = 0
    total = defaultdict(int)
    for k in (32749,32768,36060):
        for case in range(4):
            core = [-1,0,1]
            sites = [0,1,2]
            if case >= 2:
                start = len(core)
                append_branch(core,2,[-1]+list(range(29)))
                sites.append(len(core)-1)
                if case == 3:
                    append_branch(core,start+12,[-1]+list(range(10)))
                    sites.append(len(core)-1)
                    append_branch(core,start+12,[-1,0,1,2])
                    # The extra branching vertex has bounded degree and is a mark.
            anchor = len(core)
            append_branch(core,1,[-1]+list(range(20)))
            for v in sites[:3]:
                for _ in range(8):
                    append_branch(core,v,[-1,0,0])
            palette = [x for x in range(k) if k//12 < min(x,k-x) < 5*k//12]
            for edge in (False,True):
                base = 31 if edge else 10
                length = base+14*(230 if case == 3 else 100)
                counts = {v:22+case for v in sites[1:]}
                counts[0] = k-len(core)-length-sum(counts.values())
                attach = (0 if case == 0 else 1) if edge else anchor
                child = (1 if case == 0 else 2) if edge else None
                stats = verify(core,attach,length,child,counts,k,palette)
                for key,n in stats.items():
                    total[key] += n
                internal += edge
                counts_checked += 1
                edges += k-1

    for k in (65521,65520):
        core = [-1,0]
        for _ in range(6):
            append_branch(core,1,[-1,0,0])
        rng = Random(1)
        selected = [rng.random() < .55 for _ in range(150)]
        palette = [x for x in range(k) if selected[(300*min(x,k-x)//k) % 150]]
        for edge in (False,True):
            length = (31 if edge else 10)+14*115
            m = (49*(k-len(core)-length))//100
            counts = {0:k-len(core)-length-m,1:m}
            stats = verify(core,0 if edge else 1,length,1 if edge else None,counts,k,palette)
            for key,n in stats.items():
                total[key] += n
            counts_checked += 1
            internal += edge
            edges += k-1

    repaired = sum(total[key] for key in ('leaf errors','fixed errors','packet errors','single errors'))
    assert all(total[key] > 0 for key in ('leaf errors','fixed errors','packet errors','single errors','batches'))
    print(f"{modular:,} modular bridge identities and {separated} injective prescribed-weight bridges.")
    print(f"{counts_checked} whole trees including {internal} internal subdivisions; {edges:,} actual "
          f"edges, {repaired:,} fourteen-vertex repairs, {total['packets']} packets and {total['batches']} batches.")


if __name__ == '__main__':
    main()

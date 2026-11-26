"""Independent cyclic reconstruction, interval quotas, and pinned-tree label checks."""

from collections import Counter
from fractions import Fraction
from itertools import product
from math import isqrt
from random import Random

from research.check_large_order_subdivision import children, compress, peel, restore
from research.large_order_degree import balanced, counts
from research.large_order_primitive import squared_terms
from research.large_order_subdivision import expand, round_groups
from research.large_order_switches import run


def reconstruct(data):
    k = len(data)
    totals = [0]*k
    tables = squared_terms(data)
    for stride, row in tables.items():
        assert stride > 0 and stride & (stride-1) == 0
        for x, weight in enumerate(row):
            totals[x] += weight
            totals[(x+stride)%k] -= 2*weight
            totals[(x+2*stride)%k] += weight
    assert list(data) == totals
    return tables


def norm_check(f):
    # Bound any interval of f by M sqrt(length) directly from all endpoint pairs.
    k = len(f)
    m = 0
    for start in range(k):
        total = 0
        for end in range(start,k):
            total += f[end]
            m = max(m, (abs(total)+isqrt(end-start+1)-1)//isqrt(end-start+1))
    for s, row in reconstruct(f).items():
        assert max(map(abs,row)) <= 48*(2+m/max(1,isqrt(min(k,s))))


def interval_columns(k, observations):
    widths = [2**j for j in range((k-1).bit_length()+1)]
    rows = [(w,i) for w in widths for i in range(0,k,w)]
    return [Fraction(sum(i<=x<i+w for x in observations),2**((w.bit_length()-1)//2))
            for w,i in rows]


def test_interval_rounding(k, rng):
    groups = []
    entries = []
    for _ in range(23):
        offsets = [rng.randrange(k) for _ in range(3)]
        options = [[(x+d)%k for d in offsets] for x in range(k)]
        entries.append(options)
        groups.append([interval_columns(k,points) for points in options])
    chosen = round_groups(groups,len(groups[0][0]))
    hist = Counter(v for group,j in zip(entries,chosen) for v in group[j])
    for i in range(k):
        for end in range(i+1,k+1):
            t = end-i
            assert abs(k*sum(hist[x] for x in range(i,end))-69*t) <= 200*k*isqrt(t)


def pin_tree(tree,k,pins,stats,outer=True):
    # Shorter peels and a smaller stopping threshold exercise more recursive calls.
    n = len(tree)
    if n <= 2*len(pins)+1:
        return [0]*n
    kids = children(tree)
    live,undo = peel(tree,kids,k,None if outer else 4,pins)
    ids,small,paths = compress(tree,kids,live,pins)
    index = {u:i for i,u in enumerate(ids)}
    if not outer and len(ids)==n:
        # Only the protected skeleton remains when a short peel has no effect.
        assert not undo and n <= 40*len(pins)+1
        return [0]*n
    core = pin_tree(small,k,{index[u] for u in pins},stats,False)
    labels = [None]*n
    for i,val in zip(ids,core):
        labels[i] = val
    requests = [(labels[p[0]],labels[p[-1]],(len(p)-2)//12) for p in paths]
    for p,walk in zip(paths,expand(requests,k)):
        for i,x in zip(p,walk):
            labels[i] = x
    stats[0] += len(undo)
    stats[1] += sum(q for _,_,q in requests)
    return restore(tree,labels,undo,k)


def verify_pins(rng):
    stats = [0,0]
    cases = 0
    for k in (3,4,5,6):
        for n in (37,91,157):
            for parents in ([-1]+list(range(n-1)),[-1]+[rng.randrange(v) for v in range(1,n)]):
                for r in (2,5):
                    pins = {0,*rng.sample(range(1,n),r-1)}
                    labels = pin_tree(parents,k,pins,stats)
                    assert all(labels[v]==0 for v in pins)
                    vertices,edges = counts(parents,labels,k)
                    delta = [v-e for v,e in zip(vertices,edges)]
                    assert sorted(delta)==[0]*(k-1)+[1]
                    gap = delta.index(1)
                    additions = [x for x in range(k)
                                 for _ in range(max(vertices)+(x==gap)-vertices[x])]
                    enlarged = list(parents)+[rng.choice(sorted(pins)) for _ in additions]
                    assert all(balanced(row) for row in counts(enlarged,labels+additions,k))
                    cases += 1
    return cases,stats


if __name__=='__main__':
    rng = Random(841337)
    trials = 0
    for k in range(2,11):
        for f in product((-1,0,1),repeat=k):
            if not sum(f) and not sum(i*x for i,x in enumerate(f))%k:
                reconstruct(f)
                trials += 1
    for k in range(2,145):
        f = [0]*k
        for _ in range(2*k):
            x,a,b = (rng.randrange(k) for _ in range(3))
            f[x] += 1
            f[(x+a+b)%k] += 1
            f[(x+a)%k] -= 1
            f[(x+b)%k] -= 1
        norm_check(f)
    for k in (1024,8191,16384):
        a = [((i//37)%11)-5 for i in range(k)]
        reconstruct([a[i]-2*a[(i-91)%k]+a[(i-182)%k] for i in range(k)])
    for k in (3,5,8,9):
        test_interval_rounding(k,rng)
    cases,stats = verify_pins(rng)
    full = [run(k,leaf,64,True,squared_terms) for k in (5,6,8,9,10,13) for leaf in (False,True)]
    print(f"{trials} exhaustive and 146 larger reconstructions, four interval-quota checks.")
    print(f"{cases} pinned trees, {stats[0]} restored batches and {stats[1]} twelve-site blocks.")
    print(f"{len(full)} whole trees through order {max(n for n,_ in full)}, "
          f"{sum(u for _,u in full)} ordinary switches verified.")

"""Test fixed-core recoloring by independently scalable unit offsets."""
from collections import Counter, defaultdict
from itertools import combinations, product
from math import gcd
from random import Random

from .check_period_chains import factors, make_piece


def destinations(k,p,weights,selected):
    """Specify new weights on selected edges, or return None if this is impossible."""
    if not selected:
        return {}
    counts = Counter(weights)
    minimum = len(weights)//k
    groups = defaultdict(list)
    for i in selected:
        groups[weights[i]%p].append(i)
    major = max(groups,key=lambda c:len(groups[c]))
    inside = groups[major][:]
    outside = [i for i in selected if weights[i]%p!=major]
    excess = len(inside)-len(outside)
    result = {}
    if excess>0:
        high = {weights[i]:i for i in inside if counts[weights[i]]>minimum}
        low = [z for z in range(k) if counts[z]==minimum and z%p!=major]
        if len(high)<excess or len(low)<excess:
            return None
        for i,z in list(zip(high.values(),low))[:excess]:
            result[i] = z
        inside = [i for i in inside if i not in result]
        for i,j in zip(inside,outside):
            result[i],result[j] = weights[j],weights[i]
    else:
        # In cyclic order each class occupies at most the largest block length.
        order = [i for group in groups.values() for i in group]
        for j,i in enumerate(order):
            result[i] = weights[order[(j+len(inside))%len(order)]]
    return result


def feasible(k,weights,selected,*,any_nonzero=False):
    # Each destination bin has mandatory and optional slots. Dummy edges may fill
    # only optional slots, so a perfect matching enforces both histogram bounds.
    q,r = divmod(len(weights),k)
    marked = set(selected)
    kept = Counter(w for i,w in enumerate(weights) if i not in marked)
    slots = [(z,i<q-kept[z]) for z in range(k) for i in range(q+bool(r)-kept[z])]
    candidates = [[j for j,(z,_) in enumerate(slots) if (z!=weights[i] if any_nonzero else gcd(z-weights[i],k)==1)]
                  for i in selected]
    candidates.extend([[j for j,(_,must) in enumerate(slots) if not must]]
                      *(len(slots)-len(selected)))
    matching = {}
    def insert(i,seen):
        for j in candidates[i]:
            if j in seen:
                continue
            seen.add(j)
            if j not in matching or insert(matching[j],seen):
                matching[j] = i
                return True
        return False
    return all(insert(i,set()) for i in range(len(candidates)))


def test(k,p,weights,selected):
    out = destinations(k,p,weights,selected)
    assert (out is not None)==feasible(k,weights,selected)
    if out is None:
        return False
    assert set(out)==set(selected)
    assert all(gcd(z-weights[i],k)==1 for i,z in out.items())
    sums = Counter(out.get(i,w) for i,w in enumerate(weights))
    bins = [sums[z] for z in range(k)]
    assert max(bins)-min(bins)<=1
    return True


def profiles():
    cases = rejected = 0
    for k in (2,3,4,5):
        p, = (p for p,_ in factors(k))
        for q in (0,1):
            for r in range(k):
                for high in combinations(range(k),r):
                    counts = [q+int(z in high) for z in range(k)]
                    weights = [z for z,c in enumerate(counts) for _ in range(c)]
                    for marks in product(*(range(c+1) for c in counts)):
                        selected = [i for z,m in enumerate(marks)
                                    for i in range(sum(counts[:z]),sum(counts[:z])+m)]
                        rejected += not test(k,p,weights,selected)
                        cases += 1
    rng = Random(271953)
    for k in (7,8,9,11,16,25,27,32):
        p = factors(k)[0][0]
        for _ in range(350):
            n = rng.randrange(1,4*k)
            weights = [i%k for i in range(n-1)]
            selected = rng.sample(range(n-1),rng.randrange(n))
            rejected += not test(k,p,weights,selected)
            cases += 1
    print('histogram and marking cases',cases,'infeasible',rejected)


def expansions():
    rng = Random(5327)
    totals = Counter()
    for k in (3,4,5,7,8,9,16,25,27,29):
        p = factors(k)[0][0]
        for trial in range(45):
            order = rng.randrange(2,3*k+1)
            labels = [i%k for i in range(order)]
            weights = labels[1:]  # ordinary star at vertex 0
            selected = rng.sample(range(order-1),rng.randrange(1,order))
            targets = destinations(k,p,weights,selected)
            if targets is None:
                continue
            edges = []
            for i,w in enumerate(weights):
                if i not in targets:
                    edges.append((0,i+1))
                    continue
                c = rng.choice([j for j in range(1,k) if gcd(j,k)==1])
                q = 1+trial%2
                block,internal,h,a,b = make_piece(k,rng,c,q)
                u = (targets[i]-w)*pow(c,-1,k)%k
                d = labels[0]+u*(block[a]-h)
                start = len(labels)
                labels.extend((u*x+d)%k for x in block)
                edges.extend((start+v,start+z) for v,z in internal)
                edges.extend(((0,start+a),(i+1,start+b)))
                totals['pieces'] += 1
            assert len(edges)==len(labels)-1
            hist = Counter((labels[v]+labels[z])%k for v,z in edges)
            for counts in (Counter(labels),hist):
                full = [counts[j] for j in range(k)]
                assert max(full)-min(full)<=1
            totals['ordinary trees'] += 1
    print('expansions',dict(totals))


def packing_threshold():
    rng=Random(271992)
    joins=rejected=0
    for k in (2,3,4,5,6,8,9,10,25,27,29):
        for q in range(5):
            for r in sorted({1,k-1}):
                # Give a star a balanced complete labeling on its original vertices.
                labels=[i%k for i in range(q*k+r+1)]
                weights=labels[1:]
                m=2*(q+1)-1
                for _ in range(5):
                    selected=rng.sample(range(len(weights)),m)
                    targets=destinations(k,k,weights,selected)
                    assert targets is not None and feasible(k,weights,selected,any_nonzero=True)
                    f=labels[:]
                    edges=[]
                    for i,w in enumerate(weights):
                        if i not in targets:
                            edges.append((0,i+1))
                            continue
                        diff=(targets[i]-w)%k
                        assert diff
                        start=len(f)
                        f.extend(range(k))
                        edges.extend((start,start+j) for j in range(1,k))
                        edges.extend(((0,start),(start+diff,i+1)))
                    assert len(edges)==len(f)-1
                    for hist in (Counter(f),Counter((f[u]+f[v])%k for u,v in edges)):
                        bins=[hist[x] for x in range(k)]
                        assert max(bins)-min(bins)<=1
                    joins+=1
            if q:
                weights=[i%k for i in range(1,q*k+2)]
                inside=[i for i,w in enumerate(weights) if w==1]
                outside=[i for i,w in enumerate(weights) if w!=1]
                selected=inside+outside[:q-1]
                assert len(selected)==2*q
                assert not feasible(k,weights,selected,any_nonzero=True)
                rejected+=1
    print('threshold expansions',joins,'sharp fixed-core examples',rejected)


if __name__=='__main__':
    profiles()
    expansions()
    packing_threshold()

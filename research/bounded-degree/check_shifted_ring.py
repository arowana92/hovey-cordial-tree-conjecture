"""Audit the edge transfers and exhaust small shifted cycles with attachments."""
from collections import Counter
from functools import reduce
from itertools import permutations
from math import gcd
from random import Random

from check import adjacency
from shifted_ring import construct


def graphs(k):
    def cycle(c):
        return [(v,(v+1)%c) for v in range(c)]
    yield cycle(k)
    for length in (1,2,3,8):
        c = k-length
        if c>=3:
            yield cycle(c)+[(0,c)]+[(v-1,v) for v in range(c+1,k)]
    for leaves in (2,3,7,12):
        c = k-leaves
        if c>=3:
            yield cycle(c)+[(v%min(3,c),c+v) for v in range(leaves)]
    if k>40:
        # Many leaves, with coefficient gcd two or three when the division is exact.
        for period in (2,3):
            c = (k+period-1)//period
            yield cycle(c)+[(i%c,c+i) for i in range(k-c)]
        # An abundant odd degree and a rare even degree give distinct gcds.
        c = k//2
        yield cycle(c)+[(max(0,i-1)%c,c+i) for i in range(k-c)]
        # Short cycle, long corridor, two adjacent vertices of large degree.
        c = 3
        spine = k-16
        yield cycle(c)+[(0,c)]+[(v-1,v) for v in range(c+1,spine)]+[(c+v%2,v) for v in range(spine,k)]


def possible(edges,bias):
    k=len(edges)
    graph=adjacency(k,edges)
    ends=[v for v,ns in enumerate(graph) if len(ns)==1]
    moment=(k*(k-1)//2+sum(bias.values()))%k
    if not ends: return moment==0
    if len(ends)>1: return sum(bias.values())%reduce(gcd,(len(ns)-1 for ns in graph),k)==0
    if not moment: return False
    y=ends[0]
    h=next(v for v,ns in enumerate(graph) if len(ns)==3)
    w=next(iter(graph[y]))
    if w not in graph[h]: return True
    return (moment+bias.get(frozenset((y,w)),0)-bias.get(frozenset((h,w)),0))%k!=0


def verify(edges,bias,result):
    k=len(edges)
    kept,closing,missing,pins,labels=result
    old=set(map(frozenset,edges))
    new=set(map(frozenset,kept))
    graph=adjacency(k,kept)
    done,queue={0},[0]
    for v in queue:
        for w in graph[v]-done:
            done.add(w)
            queue.append(w)
    assert len(done)==k and len(kept)==k-1 and max(map(len,graph))<=6
    assert all(e<=pins.keys() for e in (old^new)|bias.keys())
    assert all(labels[v]==x for v,x in pins.items()) and len(labels)==len(set(labels.values()))
    assert sum(labels.values())%k==sum(range(k))%k
    assert (sum(len(graph[v])*x for v,x in labels.items())+missing-sum(range(k)))%k==0
    for d,count in Counter(map(len,graph)).items():
        inside=sum(len(graph[v])==d for v in labels)
        assert inside==count or min(inside,count-inside)>=6
    assert (sum(pins[v] for v in closing)+bias.get(frozenset(closing),0))%k==missing
    for point in (pins,labels):
        previous=Counter((sum(point[v] for v in e)+bias.get(e,0))%k for e in old if e<=point.keys())
        after=Counter(sum(point[v] for v in e)%k for e in new if e<=point.keys())
        assert missing not in after
        after[missing]+=1
        assert previous==after and max(previous.values())==1


def cores():
    rng=Random(270127)
    counts=Counter()
    for k in (503,625,810,1024):
        for edges in graphs(k):
            for mode in range(5):
                perm=list(range(k))
                rng.shuffle(perm)
                es=[(perm[a],perm[b]) for a,b in edges]
                # Include offset sets of total -S and sums with no such restriction.
                bias={i:rng.randrange(1,k) for i in rng.sample(range(k),8)} if mode else {}
                if mode in (1,2):
                    bias[0]=(-k*(k-1)//2-sum(x for i,x in bias.items() if i))%k
                values={es[i]:x for i,x in bias.items() if x}
                rng.shuffle(es)
                canonical={frozenset(e):x for e,x in values.items()}
                result=construct(es,values,rng,cap=4)
                assert (result is not None)==possible(es,canonical)
                if result is not None:
                    verify(es,canonical,result)
                counts[result is not None]+=1
    return counts


def insertions(es,bs,x):
    k=len(es)
    graph=adjacency(k,es)
    # Test cycle membership by disconnecting the graph at the proposed opening.
    tested=0
    for j,(u,v) in enumerate(es):
        seen,queue={u},[u]
        for a in queue:
            for b in graph[a]-seen:
                if {a,b}=={u,v}:
                    continue
                seen.add(b)
                queue.append(b)
        if v not in seen:
            continue
        left,right,old=2%k,(k-1-j)%k,(j+1)%k
        alpha=(j+3)%k
        gamma=bs.get(frozenset((u,v)),0)
        beta=(gamma+old-alpha)%k
        shift=(left+old-beta-x[v])%k
        new=[(a+shift)%k for a in x]
        weights=[(new[a]+new[b]+bs.get(frozenset((a,b)),0))%k
                 for i,(a,b) in enumerate(es) if i!=j]
        weights.extend(((left+new[u]+alpha)%k,(new[v]+right+beta)%k))
        net=Counter(weights)
        net[(left+right+old)%k]-=1
        assert all(net[a]==1 for a in range(k)) and sorted(new)==list(range(k))
        tested+=1
    return tested


def literal():
    found=forced=small=opened=0
    for k in range(3,9):
        for es in graphs(k):
            for i in range(k):
                for d in range(k) if i==0 else range(1,k):
                    bs={frozenset(es[i]):d}
                    expected=possible(es,bs)
                    success=False
                    # A common translation fixes the first label at zero.
                    for tail in permutations(range(1,k)):
                        x=(0,)+tail
                        if len({(x[a]+x[b]+(d if j==i else 0))%k
                                for j,(a,b) in enumerate(es)})==k:
                            success=True
                            break
                    assert not success or expected
                    if success:
                        found+=1
                        opened+=insertions(es,bs,x)
                    elif expected: small+=1
                    else: forced+=1
    return found,forced,small,opened


if __name__=='__main__':
    c=cores()
    print(f"degree cores={c[True]} rejected moments or collisions={c[False]}",flush=True)
    yes,no,small,opened=literal()
    print(f"small actual bijections={yes} forced failures={no} other small failures={small} verified insertions={opened}")

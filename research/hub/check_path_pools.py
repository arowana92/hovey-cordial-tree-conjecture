"""Audit the modular path blocks, the two-pool coupling and the gluing moments."""

from collections import Counter
from fractions import Fraction
from itertools import product
from random import Random
from research.hub.universal_hub import construct
from research.large_order_subdivision import POSITIONS, evaluate


def coupling(g,t):
    row = [[1-2*g,0,0],[0,g*g,g-g*g],[0,g-g*g,g*g]]
    assert all(sum(r)==s for r,s in zip(row,(1-2*g,g,g)))
    vparts=[Fraction(1,t+1),Fraction(t-1,t+1),Fraction(1,t+1)]
    cparts=[Fraction(t,t+1),Fraction(1,t+1)]
    for i in (1,2):
        for c in cparts:
            for v in vparts:
                assert row[i][i]*v*c == (g*v)*(g*c)
            assert sum(row[j][i]*c for j in (0,1,2) if j!=i)==(1-g)*(g*c)


def path_rows(k):
    for p,q in product(range(k),repeat=2):
        if p*q==0 or (p+q)%k==0:
            continue
        for i,row in enumerate(POSITIONS):
            for previous in POSITIONS[:i]:
                if row[2:]==previous[2:]:
                    assert evaluate(row,p,q,0,0,k)!=evaluate(previous,p,q,0,0,k)


def make_fixture(k,blocks,rng):
    # All base edges selected for elongation have distinct nonzero endpoint sum.
    tree=[-1,0,1,2,0,4,5,0,7]
    x,missing,_=construct(tree)
    labels=[a%k for a in x]
    edges=[]
    for v,p in enumerate(tree):
        if v:
            edges.append((p,v))
    occupied=set(labels)
    assert len(occupied)==len(x)
    good=[edge for edge in edges if all(labels[v]!=0 for v in edge)
          and sum(labels[v] for v in edge)%k]
    for i,(a,b) in enumerate(good[:3]):
        edges.remove((a,b))
        left=[a]; tails=[]; prev=(labels[a],labels[b])
        for _ in range(blocks+i):
            for _ in range(10000):
                u,v=rng.randrange(k),rng.randrange(k)
                extra=[evaluate(row,*prev,u,v,k) for row in POSITIONS]
                if len(set(extra))==12 and not occupied.intersection(extra):
                    break
            else: raise ValueError("fixture parameter search exhausted")
            ids=list(range(len(labels),len(labels)+12))
            labels+=extra;occupied.update(extra)
            left.append(ids[0]);tails.append(ids[1:]);prev=u,v
        path=left+[v for tail in reversed(tails) for v in tail]+[b]
        edges.extend(zip(path,path[1:]))
    weights=[(labels[a]+labels[b])%k for a,b in edges]
    assert sorted(weights+[missing%k])==sorted(labels)
    return labels,edges,missing%k


def roles(labels,edges,gap,k,t):
    adj=[[] for _ in labels]
    for u,v in edges:
        adj[u].append(v);adj[v].append(u)
    marks={v for v,group in enumerate(adj) if len(group)!=2}|{0}
    chains=[[],[]]
    seen=set()
    for root in marks:
        for child in adj[root]:
            if frozenset((root,child)) in seen:
                continue
            u,v=root,child;interior=[]
            while v not in marks:
                interior.append(v)
                seen.add(frozenset((u,v)))
                u,v=v,next(w for w in adj[v] if w!=u)
            seen.add(frozenset((u,v)))
            width=len(interior)//(2*(t+1))*(t+1)
            if width:
                chains[0].append(interior[:width])
                chains[1].append(interior[width:2*width])
    assert len(seen)==len(edges)
    pools=[];outside=set(range(len(labels)));old_edges=set(seen)
    endpoint_sum=0
    for group in chains:
        starts=set();ends=set();middle=set();colors=set();link={}
        first=set();last=set()
        for chain in group:
            assert len(chain)%(t+1)==0
            outside.difference_update(chain)
            first.add(labels[chain[0]]);last.add(labels[chain[-1]])
            for j,node in enumerate(chain):
                residue=labels[node]
                pos=j%(t+1)
                (starts if pos==0 else ends if pos==t else middle).add(residue)
                if not j:continue
                old_edges.remove(frozenset((chain[j-1],node)))
                before=labels[chain[j-1]]
                if pos==0:link[before]=residue
                else:colors.add((before+residue)%k)
        connector={(a+b)%k for a,b in link.items()}
        assert set(link)==ends-last and set(link.values())==starts-first
        assert len(starts)==len(ends)==len(middle)//(t-1)==len(colors)//t
        assert (sum(starts)+sum(ends)+2*sum(middle)-sum(colors))%k==0
        assert (sum(starts-first)+sum(ends-last)-sum(connector))%k==0
        # Reorder the connector edges. The required path bijection still joins
        # exactly the prescribed firsts, lengths and lasts of all the chains.
        entries=iter(sorted(link.items(),reverse=True)); match={}; visits=[]
        for chain in group:
            src=labels[chain[0]]; begin=src
            for _ in range(len(chain)//(t+1)-1):
                end,next_start=next(entries);match[src]=end;src=next_start
            match[src]=labels[chain[-1]]
            visits.append((begin,len(chain)//(t+1),labels[chain[-1]]))
        assert set(match)==starts and set(match.values())==ends
        for first_vertex,size,last_vertex in visits:
            at=first_vertex
            for j in range(size):
                at=match[at]
                if j+1<size:at=link[at]
            assert at==last_vertex
        endpoint_sum+=sum(first)+sum(last)
        pools.extend([colors,connector])
    w0={sum(labels[v] for v in edge)%k for edge in old_edges}
    assert set.union(w0,*pools)==set(labels)-{gap}
    v0=sum(labels[v] for v in outside)
    assert (2*v0+endpoint_sum-sum(w0)-sum(labels))%k==gap
    return sum(map(len,chains))


def exchange(buckets, targets, k):
    for i, want in enumerate(targets[:-1]):
        step=(want-sum(buckets[i]))%k
        if not step:continue
        x=next(x for x in buckets[i] if (x+step)%k in buckets[-1])
        y=(x+step)%k
        buckets[i].remove(x);buckets[i].add(y)
        buckets[-1].remove(y);buckets[-1].add(x)
    assert [sum(b)%k for b in buckets]==targets


if __name__=='__main__':
    rng=Random(423918)
    for g,t in product((Fraction(1,50),Fraction(1,5),Fraction(2,5),Fraction(1,2)),(2,3,7,24)):
        coupling(g,t)
    for k in range(2,41):path_rows(k)
    nzone=0
    for k in (2000,2003,2016):
        for b in (2,3,5,8):
            x,edges,s=make_fixture(k,b,rng)
            for t in (2,3,5):
                nzone+=roles(x,edges,s,k,t)
    for k in (809,1000,1009,1200):
        for _ in range(15):
            items=list(range(k));rng.shuffle(items)
            buckets=[set(items[i*k//4:(i+1)*k//4]) for i in range(4)]
            first=[rng.randrange(k) for _ in range(3)]
            exchange(buckets,first+[(sum(items)-sum(first))%k],k)
    print(f"Exact role marginals, collision tests at 39 moduli, {nzone} chains "
          "reassembled on twelve labeled trees, and 60 modular sum repairs.")

"""Exact connector offsets for a subdivided double star on one period."""
from itertools import combinations
from math import gcd

from research.rainbow.surplus_prime_powers import grow


def witnesses(k,t):
    """Map each attainable offset to (far hub label, connector label, hub neighbors)."""
    choices={}
    for b in range(1,k):
        h=k//gcd(b,k)
        q,j=divmod(t,h)
        if j==h-1:
            continue
        arc={-i*b%k for i in range(1,j+1)}
        step=k//h
        for delta in set(range(k))-choices.keys():
            for a in ((b-delta)%k,(-t*b-delta)%k):
                if a not in arc and not (q and a%step):
                    continue
                cosets=list(range(1,step))
                if a%step:
                    cosets.remove(a%step)
                    cosets.insert(0,a%step)
                neighbors=arc|{(r+i*b)%k for r in cosets[:q] for i in range(h)}
                choices[delta]=(b,a,neighbors)
                break
        if len(choices)==k:
            break
    return choices


def direct(k,t):
    # Choose the actual far-hub neighbors as a subset, including the connector.
    possible=set()
    for b in range(1,k):
        for sample in combinations(set(range(1,k))-{b},t):
            x=set(sample)
            leaf_labels=set(range(1,k))-x-{b}
            weights=leaf_labels|{(b+i)%k for i in x}
            if len(weights)==k-2:
                possible.update((w-a)%k for a in x for w in set(range(k))-weights)
    return possible


def check():
    residues=small=whole=0
    for k in range(4,101):
        prime_power=not any(k%d==0 and gcd(d,k//d)==1 for d in range(2,k))
        twice_prime=k%2==0 and k>=10 and all((k//2)%p for p in range(2,int((k//2)**0.5)+1))
        for t in range(1,k-1):
            options=witnesses(k,t)
            if k<=14:
                assert set(options)==direct(k,t)
                small+=k
            if t>=2 and prime_power:
                assert len(options)==k
            if t>=2 and twice_prime:
                missing={k//2} if t<=k//2-2 else set()
                assert set(range(k))-options.keys()==missing
            if t in (2,3) and k%2==0:
                assert (k//2 in options)==(k%3==0 or k%(4 if t==2 else 8)==0)
            for delta,(b,a,neighbors) in options.items():
                leaves=set(range(1,k))-neighbors-{b}
                labels=[0,a,b,*(neighbors-{a}),*leaves]
                values=[(a+delta)%k,(a+b)%k,*((b+x)%k for x in neighbors-{a}),*leaves]
                assert len(set(labels))==len(labels)==k and len(set(values))==len(values)==k-1
                whole+=1
            residues+=k
    print('literal offset inputs',residues,'independent subset comparisons',small,'full labeled trees',whole)


def two_connectors():
    joins=prefixes=0
    for k in (4,5,8,9,16,25,27,32):
        biases=range(k) if k<=9 else (0,1,2,3,k//2,k-1)
        for s,t in ((2,2),(2,k-2),(k-2,2),(k+1,k-1),(2*k,2*k+1)):
            for a in biases:
                for b in biases:
                    labels=[0]
                    hubs={}
                    edges=[]
                    vertex,weight=[1]+[0]*(k-1),[0]*k
                    for side,x in grow(k,s,t,a,b):
                        parent=hubs.get(side,0)
                        offset=0 if parent else (a,b)[side]
                        v=len(labels)
                        weight[(labels[parent]+x+offset)%k]+=1
                        vertex[x]+=1
                        assert max(vertex)-min(vertex)<=1 and max(weight)-min(weight)<=1
                        if parent:
                            edges.append((parent,v))
                        else:
                            hubs[side]=v
                        labels.append(x)
                    assert len(labels)==s+t+1
                    prefixes+=len(labels)
                    # Restore each connector as an ordinary k-vertex star with
                    # entering vertex zero, leaving from its prescribed residue.
                    for side,d in enumerate((a,b)):
                        start=len(labels)
                        labels.extend(range(k))
                        edges.extend((start,start+i) for i in range(1,k))
                        edges.extend(((0,start),(start+d,hubs[side])))
                    vcounts,ecounts=[0]*k,[0]*k
                    for x in labels:
                        vcounts[x]+=1
                    for u,v in edges:
                        ecounts[(labels[u]+labels[v])%k]+=1
                    assert len(edges)==len(labels)-1 and max(vcounts)-min(vcounts)<=1
                    assert max(ecounts)-min(ecounts)<=1
                    joins+=1
    print('two independent connector expansions',joins,'adjusted prefixes',prefixes)


if __name__=='__main__':
    check()
    two_connectors()

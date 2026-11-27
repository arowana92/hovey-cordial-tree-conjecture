"""Replay both embedding moments, induced edges, and the degree-class condition."""
from random import Random
from unicyclic_core import core


def inspect(k,edges,cut,labels):
    u,v = edges[cut]
    assert len(set(labels.values()))==len(labels) and all(0<=a<k for a in labels.values())
    gap = (labels[u]+labels[v])%k
    degree = [0]*k
    weights = []
    for i,(a,b) in enumerate(edges):
        if i!=cut:
            degree[a] += 1
            degree[b] += 1
            if a in labels and b in labels:
                weights.append((labels[a]+labels[b])%k)
    assert gap not in weights and len(set(weights))==len(weights)
    total = k*(k-1)//2%k
    assert sum(labels.values())%k==total
    assert sum(degree[i]*v for i,v in labels.items())%k==(total-gap)%k
    for d in set(degree):
        count = sum(degree[i]==d for i in labels)
        outside = degree.count(d)-count
        assert outside==0 or min(count,outside)>=6


def constrained(k,c,rng):
    cycle = [(i,(i+1)%c) for i in range(c)]
    edges = cycle[:]
    available = list(range(c))
    degree = [2]*c
    cap = rng.randrange(3,9)
    for v in range(c,k):
        i = rng.randrange(len(available))
        a = available[i]
        degree[a] += 1
        if degree[a]==cap:
            available[i] = available[-1]
            available.pop()
        available.append(v)
        degree.append(1)
        edges.append((a,v))
    return edges


def main():
    rng = Random(19912509)
    tested = largest = 0
    for k in (311,480,729,892,1024,1875):
        for c in (3,4,k//3,k//2,k-2):
            cycle = [(i,(i+1)%c) for i in range(c)]
            examples = [constrained(k,c,rng) for _ in range(3)]
            # Two long tails, at the same joint or at two neighboring joints.
            for b in (0,1):
                split = (k+c)//2
                examples.append(cycle+[(0,c),(b,split)]+
                                [(i-1,i) for i in range(c+1,split)]+
                                [(i-1,i) for i in range(split+1,k)])
            for edges in examples:
                for cut in {0,c-1,rng.randrange(c)}:
                    labels = core(k,edges,cut)
                    inspect(k,edges,cut,labels)
                    tested += 1
                    largest = max(largest,len(labels))
        if k%2==0:
            # All vertices have degree one or three. No degree-two buffers exist.
            c = k//2
            edges = [(i,(i+1)%c) for i in range(c)]+[(i,c+i) for i in range(c)]
            for cut in (0,c//2,c-1):
                labels = core(k,edges,cut)
                inspect(k,edges,cut,labels)
                tested += 1
    print('checked unicyclic embedding cores',tested,'largest core',largest)


if __name__=='__main__':
    main()

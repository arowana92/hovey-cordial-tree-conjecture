"""Check the degree-core certificates, cut-edge multisets and square-root obstruction."""
from collections import Counter
from functools import reduce
from math import gcd
from random import Random

from check import adjacency
from excess_pins import build, obstruction


def verify(edges,pins,gap,result,cap):
    tree,labels = result
    k = len(edges)+1
    graph = adjacency(k,tree)
    seen,queue = {0},[0]
    for v in queue:
        for w in graph[v]-seen:
            seen.add(w)
            queue.append(w)
    assert len(tree)==k-1 and len(seen)==k and max(map(len,graph))<=cap+1
    assert all(labels[v]==x for v,x in pins.items())
    assert set(labels.values())<=set(range(k)) and len(set(labels.values()))==len(labels)
    assert (sum(labels.values()) - sum(range(k)))%k==0
    for es in [edges,tree]:
        weights = [(labels[a]+labels[b])%k for a,b in es if a in labels and b in labels]
        assert gap not in weights and len(weights)==len(set(weights))
        degree = Counter(v for edge in es for v in edge)
        assert (sum(degree[v]*x for v,x in labels.items())+gap-sum(range(k)))%k==0
    for d,count in Counter(map(len,graph)).items():
        inside = sum(len(graph[v])==d for v in labels)
        assert inside==count or min(inside,count-inside)>=6
    old = set(map(frozenset,edges))
    new = set(map(frozenset,tree))
    def weights(changed):
        return Counter(sum(labels[v] for v in edge)%k for edge in changed)
    assert weights(old-new)==weights(new-old)
    return len(old-new)


def random_pins(edges,sites,k,rng):
    pins,weights = {},set()
    graph = adjacency(k,edges)
    for v in sites:
        occupied = set(pins.values())
        choices = [x for x in range(k) if x not in occupied and
                   all((x+pins[y])%k not in weights for y in graph[v] if y in pins)]
        x = rng.choice(choices)
        weights.update((x+pins[y])%k for y in graph[v] if y in pins)
        pins[v] = x
    return pins,weights


def fixtures():
    rng = Random(19910827)
    yes = no = moved = pinned_cuts = largest = 0
    for k in (480,729,960,1200,1536):
        spine = k-39
        decorated = [(i-1,i) for i in range(1,spine)]
        decorated += [(2+i%3,spine+i) for i in range(k-spine)]
        tests = [(decorated,[2,3,*range(spine,spine+14),spine//2],3),
                 (decorated,[*range(spine,spine+24),spine//2,spine//2+1],3)]
        if k%2==0:
            # A cubic caterpillar with eight extra leaves at one hub keeps all degrees odd.
            h = (k-2-8)//2
            edges = [(i-1,i) for i in range(1,h)]
            nxt = h
            for i in range(h):
                children = 1 + int(i in (0,h-1)) + 8*int(i==3)
                edges += [(i,v) for v in range(nxt,nxt+children)]
                nxt += children
            assert nxt==k
            tests.append((edges,[3,1,h//2,*range(h,h+8)],3))
        for edges,sites,cap in tests:
            degrees = Counter(v for e in edges for v in e)
            largest = max(largest,max(degrees.values()))
            pins,weights = random_pins(edges,sites,k,rng)
            divisor = reduce(gcd,(degrees[v]-1 for v in range(k) if v not in pins),k)
            pinned_moment = sum((degrees[v]-1)*x for v,x in pins.items())
            for gap in rng.sample(sorted(set(range(k))-weights),9):
                result = build(edges,pins,gap,cap,rng)
                if (gap+pinned_moment)%divisor:
                    assert result is None
                    no += 1
                else:
                    moved += verify(edges,pins,gap,result,cap+1)
                    old = set(map(frozenset,edges))-set(map(frozenset,result[0]))
                    pinned_cuts += sum(all(v in pins for v in e) for e in old)
                    yes += 1
            if weights:
                assert build(edges,pins,next(iter(weights)),cap,rng) is None
    assert no and pinned_cuts
    return yes,no,moved,pinned_cuts,largest


def obstructions():
    cases = 0
    for k in range(64,401):
        edges,pins,gap = obstruction(k)
        graph = adjacency(k,edges)
        assert len(edges)==k-1 and len(set(pins.values()))==len(pins)
        weights = [(pins[a]+pins[b])%k for a,b in edges if a in pins and b in pins]
        assert gap not in weights and len(set(weights))==len(weights)
        assert sum(v not in pins and len(row)==1 for v,row in enumerate(graph))>=2
        assert reduce(gcd,(len(row)-1 for v,row in enumerate(graph) if v not in pins),k)==1
        neighbors = [pins[v] for v in graph[0] if v in pins]
        assert all(any((x+a)%k in weights for a in neighbors) for x in range(k))
        # Removing all leaves yields a path.
        nonleaves = {v for v,row in enumerate(graph) if len(row)>1}
        assert max(len(graph[v]&nonleaves) for v in nonleaves)<=2
        cases += 1
    return cases


if __name__ == "__main__":
    print("feasible, gcd obstructions, moved edges, doubly pinned cuts, maximum degree:",fixtures())
    print(obstructions(),"locally valid caterpillar prescriptions blocked at every hub label")

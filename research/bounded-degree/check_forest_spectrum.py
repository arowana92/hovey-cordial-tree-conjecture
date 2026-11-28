"""Reconstruct cut-edge histograms and both embedding moments on the actual forest."""
from collections import Counter
from random import Random

from check import adjacency
from forest_spectrum import build


def verify(parents,boundary,pins,gap,result,cap):
    first,final,labels = result
    n,k = len(parents),len(parents)+1
    assert labels[n]==0 and len(set(labels.values()))==len(labels)
    assert all(labels[v]==x for v,x in pins.items())
    assert sum(labels.values())%k==sum(range(k))%k
    original = [(u,v) for v,u in enumerate(parents) if u>=0]
    weights = Counter((labels[u]+labels[v])%k for u,v in original if u in labels and v in labels)
    weights.update((labels[r]+b)%k for r,b in boundary.items())
    assert gap not in weights and max(weights.values())==1
    # Count the incidence moment on the original forest, including its entries.
    counts = Counter(parents)
    assert (sum(counts[v]*x for v,x in labels.items() if v<n)+sum(boundary.values())+gap)%k==0
    for edges in (first,final):
        graph = adjacency(k,edges)
        seen,queue = {0},[0]
        for v in queue:
            for w in graph[v]-seen:
                seen.add(w)
                queue.append(w)
        assert len(seen)==k and len(edges)==k-1
        actual = Counter((labels[u]+labels[v])%k for u,v in edges if u in labels and v in labels)
        assert weights==actual
        assert (sum(len(graph[v])*x for v,x in labels.items())+gap-sum(range(k)))%k==0
    assert max(map(len,graph))<=cap+4
    for d,total in Counter(map(len,graph)).items():
        inside = sum(len(graph[v])==d for v in labels)
        assert total==inside or min(inside,total-inside)>=6


def run():
    rng = Random(199108)
    yes = no = local = paired = 0
    for k in (690,729,1024,1305):
        n = k-1
        for m in (2,3,8):
            spine = n-36
            parents = [-1]*m+[i-m for i in range(m,spine)]+[0,1,2]*12
            boundary = {i:rng.randrange(k) for i in range(m)}
            pins = {0:13,spine:14,spine+1:17}
            # Change boundaries when a coincidental conflict occurs at a
            # fixed edge. Use a known interior neighbor to force a local test.
            boundary[0]=1
            boundary[1]=3
            for gap in (0,1,10,rng.randrange(k),13+boundary[0]+1):
                if gap==27: continue
                result = build(parents,boundary,pins,gap,4,rng)
                assert result is not None
                verify(parents,boundary,pins,gap,result,4)
                yes += 1
            # The input at component root 1 and its edge to its pinned child
            # would have exactly the same symbolic weight.
            bad = dict(pins)
            bad[1+m] = boundary[1]
            assert build(parents,boundary,bad,0,4,rng) is None
            local += 1
        # A forest of full binary components, hence a genuine gcd-two test.
        if k%2==0:
            parents = [-1,-1,-1]
            for i in range((n-3)//2):
                parents.extend([i,i])
            boundary = {0:2,1:5,2:2}
            for w in range(8):
                result = build(parents,boundary,{},w,3,rng)
                if w%2==0:
                    assert result is None
                    no+=1
                else:
                    verify(parents,boundary,{},w,result,3)
                    yes+=1
            # At one root switch to an alternate input; the same row now
            # replaces its old entering weight with the prescribed gap.
            x = 9
            for c in range(10,14):
                gap = (x+c)%k
                result = build(parents,boundary,{1:x},gap,3,rng)
                if (gap+sum(boundary.values())+2*x)%2:
                    assert result is None
                    no+=1
                else:
                    verify(parents,boundary,{1:x},gap,result,3)
                    final = result[2]
                    weights = {(final[u]+final[v])%k for v,u in enumerate(parents)
                               if u>=0 and u in final and v in final}
                    weights.update((final[r]+(c if r==1 else b))%k for r,b in boundary.items())
                    assert (x+5)%k not in weights
                    paired+=1
    return yes,no,local,paired


if __name__ == "__main__":
    print("prescribed gaps, arithmetic exclusions, local exclusions, shared rows:",run())

"""Check the equal-histogram modular certificate on actual parent edges."""

from collections import Counter
from random import Random

from research.hub.linear_hub_batches import construct
from research.rainbow.verify import rooted_shapes


def audit(tree,k):
    labels,gap,stats = construct(tree,k)
    assert labels[0]==0 and len(set(labels))==len(tree)
    vertices = Counter(labels)
    weights = Counter((labels[v]+labels[p])%k for v,p in enumerate(tree[1:],1))
    assert vertices==weights+Counter([gap])
    return stats


def main():
    small = 0
    for n in range(1,11):
        for raw in rooted_shapes(n).values():
            audit(list(raw),65536)
            small += 1
    rng = Random(19741)
    cases = rounds = pairs = cycles = largest = 0
    for n in (555,2800,8400):
        hosts = [[-1]+list(range(n-1)),[-1]+[(i-1)//2 for i in range(1,n)]]
        for _ in range(3):
            tree = [-1]
            available = [0]
            counts = Counter()
            for i in range(1,n):
                j = rng.randrange(len(available))
                p = available[j]
                tree.append(p)
                counts[p] += 1
                if counts[p]==3:
                    available[j] = available[-1]
                    available.pop()
                available.append(i)
            hosts.append(tree)
        # Bounded nonroot degree with many repeated small branches of distinct shapes.
        mixed = [-1]+list(range(130))
        for j in range(n//7):
            p = len(mixed)
            mixed.extend([0,p,p+1,p+(j%2),p+3,p+3])
        hosts.append(mixed)
        for tree in hosts:
            for k in (2**28,1000000007):
                r,w,c,f,twins = audit(tree,k)
                rounds += r
                pairs += twins
                cycles += c
                largest = max(largest,len(tree))
                cases += 1
    # Verify all prefixes of the periodic extension from a small modulus certificate.
    tree = [-1]+list(range(80))
    k = 401
    labels,missing,_ = construct(tree,k)
    A = set(labels)
    period = sorted(set(range(k))-A)+[missing]+sorted(A-{missing})
    V = Counter(labels)
    E = Counter((labels[v]+labels[p])%k for v,p in enumerate(tree) if v)
    for x in period*2:
        V[x] += 1
        E[x] += 1
        for hist in (V,E):
            counts = [hist[y] for y in range(k)]
            assert max(counts)-min(counts)<=1
    print(f"{small:,} rooted shapes through order 10; {cases} larger modular certificates through order {largest:,}.")
    print(f"{rounds:,} neutral batches, {cycles:,} erased cycles, {pairs:,} reflected pairs of branches; "
          f"all {2*k} leaf prefixes checked at modulus {k}.")


if __name__=='__main__':
    main()

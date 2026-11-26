"""Independent histograms for modular star blocks and composites of whole trees."""

from collections import Counter
from random import Random

from research.hub.linear_hub_batches import construct
from research.hub.neutral_star_blocks import star_block


def audit(k, p, d, rows, blocked):
    labels, weights = [], []
    assert len(rows) == 4*d
    for root, leaves in rows:
        assert len(leaves) == d
        labels.extend([root, *leaves])
        weights.append((root+p) % k)
        weights.extend((root+x) % k for x in leaves)
    assert len(labels) == len(set(labels)) and set(labels).isdisjoint(blocked)
    assert Counter(labels) == Counter(weights)
    return set(labels)


def local():
    rng = Random(82191)
    trials = sizes = 0
    for k in (211,360,401,484,512,777):
        for p in range(k):
            for d in (1,2):
                blocked = set(rng.sample(range(k), 5)) | {p}
                rows = star_block(k,p,d,blocked)
                sizes += len(audit(k,p,d,rows,blocked))
                trials += 1
    k = 30030
    for d in range(1,15):
        for p in (0,1,2,17,k//2,k//3,k//5,k//7):
            blocked = set(rng.sample(range(k),40)) | {p}
            sizes += len(audit(k,p,d,star_block(k,p,d,blocked),blocked))
            trials += 1
    return trials,sizes


def whole():
    rng = Random(17911)
    count = 0
    for k in (1009,1512,2048,3003):
        for rep in range(6):
            tree = [-1,0,0,1,1,2,2,4,7,7,3,6,6,9]
            labels,gap,_ = construct(tree,k,seed=rep)
            used = set(labels)
            for v in rng.sample(range(len(tree)),7):
                d = 1+rng.randrange(3)
                rows = star_block(k,labels[v],d,used)
                used.update(audit(k,labels[v],d,rows,used))
                for root,leaves in rows:
                    parent = len(tree)
                    tree.extend([v]+[parent]*len(leaves))
                    labels.extend([root,*leaves])
            weights = Counter((labels[p]+labels[v])%k for v,p in enumerate(tree) if v)
            vertices = Counter(labels)
            assert weights == vertices - Counter([gap]) and len(vertices)==len(tree)
            period = list(sorted(set(range(k))-used))+[gap]+list(sorted(used-{gap}))
            for pos in range(2*k+1):
                if pos % 103 == 0 or pos in (k-len(used),k-len(used)+1,2*k):
                    for hist in (vertices,weights):
                        freqs = [hist[x] for x in range(k)]
                        assert max(freqs)-min(freqs)<=1
                if pos < 2*k:
                    x = period[pos%k]
                    vertices[x] += 1
                    weights[(labels[0]+x)%k] += 1
            count += 1
    return count


if __name__ == '__main__':
    n,v = local()
    print(f"{n:,} prescribed-parent blocks and {v:,} actual incoming edges verified.")
    print(f"{whole()} complete multi-site trees checked, including two periods of root leaves.")

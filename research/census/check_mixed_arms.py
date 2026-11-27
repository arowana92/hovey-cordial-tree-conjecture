"""Audit prescribed holes and recount fixed-core attachments on actual trees."""

from collections import Counter
from random import Random

from .mixed_arms import extend, mixed


def packet(k, y, leaves, arms, singles):
    assert len(singles) == leaves and 2*len(arms)+leaves == k-1
    labels = [v % k for a,z in arms for v in (a,z)] + [v % k for v in singles]
    weights = [v % k for a,z in arms for v in (a,a+z)] + [v % k for v in singles]
    assert sorted(labels) == [v for v in range(k) if v != y % k]
    assert len(set(weights)) == k-1


def whole(k, b, ell, trial, rng):
    # Rotating a labeled star makes every requested parent/surplus difference
    # available. A labeled path tests an independently shaped core.
    n = 1+k*(1+trial%3)
    if trial % 2:
        parents = [-1]+list(range(n-1))
        old = [(i//2 + (i%2)*((n+1)//2)) % k for i in range(n)]
    else:
        parents = [-1]+[0]*(n-1)
        old = [i % k for i in range(n)]
    shift = rng.randrange(k)
    labels = [(x+shift)%k for x in old]
    fixed = tuple(labels)
    joint = rng.randrange(n)
    pairs,singles = extend(k,labels[joint],shift,b,ell)
    assert len(pairs) == b and len(singles) == ell
    for a,z in pairs:
        parents.extend([joint,len(labels)])
        labels.extend([a,z])
    parents.extend([joint]*ell)
    labels.extend(singles)
    assert tuple(labels[:n]) == fixed and all(0 <= x < k for x in labels)
    weights = [(labels[p]+labels[i])%k for i,p in enumerate(parents) if i]
    for vals in (labels,weights):
        counts = Counter(vals)
        hist = [counts[x] for x in range(k)]
        assert max(hist)-min(hist) <= 1, (k,b,ell,trial)



def main():
    rng = Random(198303)
    packets = trees = four = 0
    for k in range(1,101):
        for y in range(k):
            for ell in range((k-1)%2,k,2):
                packet(k,y,ell,*mixed(k,y,ell))
                packets += 1
        for t in range(3*k+1):
            whole(k,rng.randrange(3*k),rng.randrange(3*k),t,rng)
            trees += 1
    # Exhaust the only exceptional period reduction at modulus four.
    for y in range(4):
        for b in range(4):
            for ell in range(4):
                arms,singles = extend(4,0,y,b,ell)
                vertices = [y,*singles]+[u for pair in arms for u in pair]
                weights = singles+[w for a,z in arms for w in (a,(a+z)%4)]
                for vals in (vertices,weights):
                    counts = [vals.count(i) for i in range(4)]
                    assert max(counts)-min(counts)<=1
                four += 1
    for k in (127,128,165,194,225,255,256,312,1001,4032,65535,65536):
        for y in {0,1,2,3,k//6,k//4,k//3,k//2,k-1}:
            for e in {(k-1)%2,(k-1)%2+2,k-1-2*(k//6),k-1}:
                packet(k,y,e,*mixed(k,y,e))
                packets += 1
    print("prescribed packets",packets,"whole trees",trees,"four-label tails",four)


if __name__ == "__main__":
    main()

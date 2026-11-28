"""Verify the prescribed-center Hall argument and rebuild ordinary star attachments."""
from collections import Counter, defaultdict
from itertools import permutations
from math import gcd
from random import Random

from .check_short_stars import replay
from .star_period import pinned_sources


def test_permutations():
    strict = cycles = 0
    for k in range(2, 7):
        for targets in permutations(range(k)):
            shifts = [(w-v) % k for v, w in enumerate(targets)]
            for mask in range(1, (1 << k)-1):
                spare = {b for v,b in enumerate(shifts) if mask & (1 << v)}
                required = {b for v,b in enumerate(shifts) if not mask & (1 << v)}
                unsafe = {v for v,b in enumerate(shifts) if b not in spare}
                for a in required:
                    centers = [v for v,b in enumerate(shifts) if b == a]
                    for x in range(1,k):
                        if len(centers) > len(unsafe):
                            strict += 1
                        elif required-spare == {a} and len(centers) % (k//gcd(k,x)):
                            cycles += 1
                        else:
                            continue
                        assert any((s-x) % k not in unsafe for s in centers)
    return strict, cycles


def label(k, shifts, x, reserve):
    padding = list(reserve) + [0]*(k-1-len(shifts)-len(reserve))
    assert len(shifts)+len(padding) == k-1
    padding.append(-sum(shifts+padding) % k)
    full = shifts+padding
    sources = pinned_sources(full,0,0)
    spare = set(padding)
    at = {v:b for v,b in zip(sources,full)}
    s = next(v for v,b in at.items() if b == shifts[0] and at[(v-x)%k] in spare)
    available = defaultdict(list)
    for v,b in at.items():
        y = (v-s+x) % k
        if v != s and y:
            available[b].append(y)
    return [x] + [available[b].pop() for b in shifts[1:]]


def test_attachments():
    rng = Random(271128)
    checked = varied = orbit = 0
    for k in range(4,61):
        for t in range(2,k):
            d = k-t
            for _ in range(5):
                x = rng.randrange(1,k)
                a = rng.randrange(k)
                pool = rng.sample(range(k),min(t-1,d))
                effective = [rng.choice(pool) for _ in range(t-1)]
                # Make the entering shift one of the noncenter shifts.
                a_cycle = effective[0]
                if (effective.count(a_cycle)+1) % (k//gcd(k,x)):
                    reserve = sorted(set(effective)-{a_cycle})
                    labels = label(k,[a_cycle]+effective,x,reserve)
                    assert labels[0] == x
                    replay(k,labels,len(effective),a_cycle,[],[(b-x)%k for b in effective])
                    orbit += 1
                if d < 3:
                    continue
                # Ordinary edges. Include the old neighbor among the protected parents.
                protected = {a,*rng.sample(range(k),rng.randrange(min(k,d-1)))}
                x = next((b for b in sorted(protected) if b),1)
                protected.add(x)
                r = rng.randrange(t)
                outside = rng.randrange(min(r+1,t-1-r)+1)
                children = rng.randrange(t-r-outside)
                singles = [a]*r + [rng.randrange(k) for _ in range(outside)]
                singles += [rng.choice(sorted(protected)) for _ in range(t-1-len(singles)-children)]
                shifts = [a]+[x]*children+singles
                labels = label(k,shifts,x,sorted(protected))
                assert labels[0] == x
                replay(k,labels,children,a,singles,[0]*children)
                checked += 1
                varied += len(set(shifts[1:])) > d-1
    return checked, varied, orbit


if __name__ == '__main__':
    print('permutation cases, cardinality and orbit', *test_permutations(), flush=True)
    print('ordinary trees, beyond distinct-shift bound, orbit attachments', *test_attachments())

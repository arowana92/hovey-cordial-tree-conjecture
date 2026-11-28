"""Verify the prescribed-center Hall argument and rebuild ordinary star attachments."""
from collections import Counter, defaultdict
from itertools import permutations, product
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
                        assert any((s+x) % k not in unsafe for s in centers)
    return strict, cycles


def label(k, shifts, x, reserve, move=False):
    pin, forbidden = (0,x) if move else (x,0)
    shifts = [(shifts[0]+x-pin) % k]+shifts[1:]
    padding = list(reserve) + [0]*(k-1-len(shifts)-len(reserve))
    assert len(shifts)+len(padding) == k-1
    padding.append(-sum(shifts+padding) % k)
    full = shifts+padding
    sources = pinned_sources(full,0,0)
    spare = set(padding)
    at = {v:b for v,b in zip(sources,full)}
    s = next(v for v,b in at.items() if b == shifts[0] and at[(v+forbidden-pin)%k] in spare)
    available = defaultdict(list)
    for v,b in at.items():
        y = (v-s+pin) % k
        if v != s and y != forbidden:
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


def test_independent_parent():
    # Four children, seven and three singles at the chosen parents, eight elsewhere.
    # Try all colors of the entering parent and both independently chosen parents.
    checked = moved = 0
    for entering, busiest, second in product(range(27), repeat=3):
        move = busiest != entering
        x = (busiest-entering)%27 if move else (busiest or second or 1)
        reserve = sorted({busiest, second, x})
        singles = [busiest]*7+[second]*3+[(entering+i)%27 for i in range(8)]
        shifts = [entering]+[x]*4+singles
        labels = label(27,shifts,x,reserve,move)
        assert labels[0] == x
        replay(27,labels,4,entering,singles,[0]*4)
        checked += 1
        moved += move
    return checked, moved


def test_unreserved_children():
    checked = Counter()
    for t, counts, children in ((23,[6,5,4],3), (24,[8,6],3), (25,[12],4)):
        for entering, *colors in product(range(27), repeat=1+min(2,len(counts))):
            if len(counts) == 3:
                colors.append((entering+colors[0]-colors[1])%27)
            b = colors[0]
            moved = entering != b
            x = (b-entering)%27 if moved else 1
            singles = [v for v,n in zip(colors,counts) for _ in range(n)]
            singles.extend((entering+i)%27 for i in range(t-1-len(singles)-children))
            shifts = [entering]+[x]*children+singles
            reserve = sorted(set(colors))
            reserve += [b]*(27-t-1-len(reserve))
            labels = label(27,shifts,x,reserve,moved)
            replay(27,labels,children,entering,singles,[0]*children)
            checked[28+t] += 1
    return dict(checked)


if __name__ == '__main__':
    print('permutation cases, cardinality and orbit', *test_permutations(), flush=True)
    print('ordinary trees, beyond distinct-shift bound, orbit attachments', *test_attachments())
    print('order-51 independent-parent attachments, moved centers', *test_independent_parent())
    print('without reserving the child shift, by tree order',test_unreserved_children())

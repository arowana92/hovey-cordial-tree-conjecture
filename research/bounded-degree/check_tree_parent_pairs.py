"""Test two-parent incidence, the auxiliary leaf, and exact star and cover formulas."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from math import gcd
from random import Random


def rooted(n):
    shapes = {}
    for parents in product(*(range(i) for i in range(1,n))):
        children = [[] for _ in range(n)]
        for i in range(n-1,0,-1):
            children[parents[i-1]].append(tuple(sorted(children[i])))
        shapes[tuple(sorted(children[0]))] = parents
    return shapes.values()


def small(k):
    group = set(range(k))
    counts = Counter()
    for parents in rooted(k-1):
        deg = [parents.count(i) + int(i != 0) for i in range(k-1)]
        if deg[0] == 1 and max(deg) <= 2:
            continue
        h = gcd(k, *(d-1 for d in deg[1:]))
        actual = set()
        for row in permutations(range(1,k)):
            weights = {(row[i]+row[p]) % k for i,p in enumerate(parents,1)}
            if len(weights) == k-2:
                b,c = sorted((w-row[0]) % k for w in group-weights)
                actual.add((row[0],b,c))
        allowed = {(x,b,c) for x in range(1,k) for b,c in combinations(range(k),2)
                   if ((deg[0]+1)*x+b+c) % h == 0}
        if actual-allowed:
            raise ValueError("incidence criterion excludes a witness")
        pairs = {(b,c) for _,b,c in actual}
        counts.update(shapes=1, witnesses=len(actual), extra=len(allowed-actual),
                      absent_pairs=k*(k-1)//2-len(pairs))
    return counts


def stars():
    tested = 0
    for k in range(3,46):
        group = set(range(k))
        center_pairs, tip_pairs = set(), set()
        for y in range(1,k):
            holes = group - {(y+v) % k for v in group-{0,y}}
            for x in range(1,k):
                pair = tuple(sorted((w-x) % k for w in holes))
                (center_pairs if x == y else tip_pairs).add(pair)
                tested += 1
        forbidden = set()
        if k%2 == 0:
            forbidden.add((0,k//2))
        if k%3 == 0:
            forbidden.add((k//3,2*k//3))
        assert center_pairs == {(0,y) for y in range(1,k)}
        assert set(combinations(range(k),2))-tip_pairs == forbidden
    return tested


def matching(k,h,t):
    @lru_cache(None)
    def best(remaining):
        if len(remaining) <= 1:
            return 0
        x, *others = remaining
        largest = best(tuple(others))
        for j,y in enumerate(others):
            if (x+y-t) % h == 0:
                largest = max(largest, 1+best(tuple(others[:j]+others[j+1:])))
        return largest
    return best(tuple(range(k)))


def auxiliary():
    rng = Random(199126)
    tested = 0
    for k in (97,100,126,157,232):
        n = k-1
        for _ in range(20):
            parents, degrees = [], [0] * n
            for i in range(1,n):
                p = rng.choice([j for j in range(i) if degrees[j] < 4])
                parents.append(p)
                degrees[i] += 1
                degrees[p] += 1
            r = rng.randrange(n)
            h = gcd(k,*(d-1 for i,d in enumerate(degrees) if i!=r))
            adj = [{p,v} for v,p in enumerate(parents,1)]
            sites = [j for j,d in enumerate(degrees)
                     if j != r and d >= 2 and degrees.count(d) >= 3 and {j,r} not in adj]
            assert sites and (degrees[r]+2) % h == 0
            for _ in range(60):
                x = rng.randrange(1,k)
                b,c = rng.sample(range(k),2)
                if (x+b) % k == 0:
                    b,c = c,b
                y, w = (x+b)%k, (x+c)%k
                t = rng.choice(sites) if b else r
                deg = degrees[:] + [1]
                deg[t] += 1
                pins = {r:x,t:y,n:0}
                assert len(set(pins.values())) == len(pins)
                assert [pins[t]+pins[n]] == [y] and y!=w
                hu = gcd(k,*(d-1 for i,d in enumerate(deg) if i not in pins))
                pinned = sum((deg[i]-1)*z for i,z in pins.items())
                assert hu == h and (w+pinned-((degrees[r]+1)*x+b+c)) % h == 0
                tested += 1
    return tested


if __name__ == "__main__":
    for k in range(5,9):
        print(k,dict(small(k)))
    checked = 0
    for k in range(4,16):
        for h in range(1,k):
            if k%h: continue
            for t in range(h):
                f = sum((2*r-t)%h==0 for r in range(h))
                assert 2*(k-matching(k,h,t)) == k + f*((k//h)%2)
                checked += 1
    print(stars(),"star label choices,",checked,"matching sizes,",auxiliary(),"auxiliary attachments")

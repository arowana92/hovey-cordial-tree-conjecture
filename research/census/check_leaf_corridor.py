"""Test balanced fourteen-leaf corridors at 27 with the published profiles."""
import argparse
from collections import Counter, defaultdict
from pathlib import Path
from random import Random

from research.census.check_leaf_profile_manifests import read_rows
from research.census.leaf_profile_geometry import cut_test, numerical_branches
from research.rainbow.spine_counts import partitions
from research.rainbow.verify import rooted_shapes


def endpoint_cases(t):
    for hs in partitions(7):
        if len(hs) < 2:
            continue

        def assign(i, current):
            if i == len(hs):
                yield tuple(sorted(current))
                return
            h = hs[i]
            low = max(h+(h>1), current[-1][0] if i and hs[i-1] == h else 1)
            for s in range(low, t):
                next_parts = current+((s,h),)
                sizes = [a for a,_ in next_parts]
                if sum(sizes)-min(sizes) >= t:
                    break
                yield from assign(i+1,next_parts)
        yield from assign(0, ())


def bounds(t, proved):
    cases = set(endpoint_cases(t))
    independent = {p for s in range(7,2*t-1) for p in numerical_branches(s,7,6,t)}
    assert cases == independent
    cuts = cut_test(t, proved)
    by_mass = defaultdict(Counter)
    for p in cases:
        S = sum(s for s,h in p)
        if S >= t and cuts(p):
            continue
        # Along the corridor h internal vertices are available. The first
        # feasible ring removes this endpoint from consideration at h or more.
        first = min((26-S+s for s,j in p if 7-j >= 2 and 26-S+s >= 2), default=27)
        by_mass[S][first] += 1

    def pairs(n):
        count = 0
        for a, left in by_mass.items():
            for b, right in by_mass.items():
                if b < a:
                    continue
                h = n-a-b-2
                if not 0 <= h < 27:
                    continue
                if any(j%27 in (0,n%27) for j in range(a+1,a+h+2)):
                    continue
                # For the vanishing test it is harmless to count ordered pairs
                # when the two endpoint masses agree.
                count += sum(v for d,v in left.items() if d>h)*sum(v for d,v in right.items() if d>h)
        return count

    return len(cases), sum(sum(c.values()) for c in by_mass.values()), pairs(55+t), pairs(82+t)


def inspect_tree(parents):
    n = len(parents)
    neighbors = [set() for _ in parents]
    for v in range(1,n):
        neighbors[v].add(parents[v])
        neighbors[parents[v]].add(v)
    L = sum(len(c)==1 for c in neighbors)
    if L < 6 or L%2:
        return None
    q = (L-2)//2

    def side(v,blocked):
        vertices = [v]
        earlier = {v, blocked}
        for u in vertices:
            for y in neighbors[u]-earlier:
                earlier.add(y)
                vertices.append(y)
        return sum(len(neighbors[u]) == 1 for u in vertices)

    half = {(v,parents[v]) for v in range(1,n) if side(v,parents[v])==q+1}
    if not half:
        v = next(u for u in range(n) if all(side(y,u)<=q for y in neighbors[u]))
        counts = [side(y,v) for y in neighbors[v]]
        while True:
            counts.sort()
            if len(counts)<2 or counts[0]+counts[1]>q:
                break
            counts = [counts[0]+counts[1]]+counts[2:]
        assert len(counts)<=4
        if len(counts)==4:
            assert q%2 and set(counts)=={(q+1)//2}
        return False
    deg = Counter(v for e in half for v in e)
    ends = [v for v,d in deg.items() if d==1]
    assert len(ends)==2 and all(len(neighbors[v])==2 for v,d in deg.items() if d>1)
    assert len(half)==len(deg)-1
    for v in ends:
        light = [side(y,v) for y in neighbors[v] if y not in deg]
        assert sum(light)==q+1 and max(light)<=q
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifests", type=Path, default=Path(__file__).with_name("leaf-profile-audits"))
    parser.add_argument("--through", type=int, choices=range(49,55), default=52)
    args=parser.parse_args()
    rng = Random(1427)
    fixtures = list(rooted_shapes(11).values())
    fixtures += [tuple([-1]+[rng.randrange(v) for v in range(1,n)]) for n in range(25,65) for _ in range(10)]
    kinds=Counter(inspect_tree(p) for p in fixtures)
    assert kinds[True] and kinds[False]
    print(f"shape checks with a balanced path={kinds[True]} without={kinds[False]}")
    for t in range(22,27):
        count, unresolved, near, far = bounds(t,{})
        assert far==0
        print(f"t={t} numerical endpoints={count} six-tip survivors={unresolved} far pairs={far}")
        if t+28 <= args.through:
            profiles = {}
            for leaves in (12,13):
                profiles.update(read_rows(args.manifests/f"{leaves}-{t+28}.txt",t))
            _, unresolved, near, far = bounds(t,profiles)
            assert near==far==0
            print(f"  with profiles: surviving endpoints={unresolved} near pairs={near} far pairs={far}")


if __name__=='__main__':
    main()

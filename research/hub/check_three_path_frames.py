"""Check every seed and reconstruct both path orientations on actual trees."""

from collections import Counter, defaultdict
import json
from pathlib import Path

from research.hub.all_radius_two import minimal_shell


def check_tree(edges, expected, direct=(0,0)):
    adjacency = defaultdict(set)
    for x,y in edges:
        assert x != y and y not in adjacency[x]
        adjacency[x].add(y)
        adjacency[y].add(x)
    lower, upper = min(adjacency), max(adjacency)
    assert sorted(adjacency) == list(range(lower, upper+1))
    assert sorted(x+y for x,y in edges) == list(range(lower+1, upper+1))
    assert 1 in adjacency[0]
    used = {0,1}
    for c in (0,1):
        lengths = Counter()
        for first in adjacency[c]-{1-c}:
            prev, current, length = c, first, 0
            while True:
                assert current not in used
                used.add(current)
                length += 1
                following = adjacency[current]-{prev}
                if not following:
                    break
                assert len(following) == 1
                prev, current = current, next(iter(following))
            lengths[length] += 1
        assert set(lengths) <= {1,3} and lengths[1] == direct[c] and lengths[3] == expected[c]
    assert used == set(adjacency)


def expand(edges, d, second):
    # minimal_shell returns a permutation tau for which tau(u)-u permutes S.
    tau = minimal_shell(d)
    shell = sorted(tau)
    amount = 3*(len(shell)//2)

    def move(x):
        row = x//3
        return x+amount*(int(row >= d)-int(row <= -d))

    result = [(move(x),move(y)) for x,y in edges]
    for i,u in enumerate(shell):
        v = -tau[u]
        left, middle, right = 3*u+1, 3*v+2, 3*u
        result.extend(((left,middle), (middle,right)))
        result.append((1,right) if i in second else (0,left))
    lo = min(min(edge) for edge in result)
    hi = max(max(edge) for edge in result)
    return result+[(0,hi+1), (1,lo-1), (1,lo-2)]


def main():
    rows = [json.loads(s) for s in Path(__file__).with_name("three-path-seeds.jsonl").read_text().splitlines()]
    bases, frames = set(), {}
    materialized = 0
    for a,b,d,lower,paths in rows:
        assert 0 <= b <= a and (a,b) not in bases
        bases.add((a,b))
        upper = lower+3*(a+b)+1
        edges = [(0,1)]+[edge for path in paths for edge in zip(path,path[1:])]
        assert (min(min(e) for e in edges), max(max(e) for e in edges)) == (lower,upper)
        check_tree(edges, (a,b))
        if not d:
            continue
        assert d in (1,2)
        frames[a,b] = d
        for origin,lo in ((0,lower),(1,lower+1)):
            assert lo <= 3*(1-d)+origin and upper >= 3*(d-1)+origin+2
        def speed(x, origin):
            row = (x-origin)//3
            return int(row >= d)-int(row <= -d)
        assert all(speed(x,0)+speed(y,0) == speed(x+y,1) for x,y in edges)
        count = 6*(2*d-1)
        # All possible split sizes, and individually reversing each path.
        choices = {frozenset(range(j)) for j in range(count+1)} | {frozenset([i]) for i in range(count)}
        for second in choices:
            check_tree(expand(edges, d, second), (a+count-len(second), b+len(second)), (1,2))
            materialized += 1
    assert frames == {(2,0):1, (1,1):1, **{(a,0):2 for a in range(6,12)}}
    for n in range(2,24):
        for b in range(n//2+1):
            a = n-b
            assert (a,b) in bases or any(a >= x and b >= y and (n-x-y)%6 == 0 and
                                        n-x-y >= 6*(2*d-1) for (x,y),d in frames.items())
    print(f"Verified {len(rows)} seeds including {len(frames)} frames and {materialized} expanded trees.")


if __name__ == "__main__":
    main()

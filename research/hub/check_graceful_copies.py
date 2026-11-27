"""Verify both copies, their individual leaf populations and the complete integer labeling."""

from itertools import permutations
from random import Random

from research.hub.graceful_copies import expand
from research.rainbow.verify import rooted_shapes


def graceful_fixture(parents):
    n = len(parents)
    for f in permutations(range(n)):
        if {abs(f[i]-f[p]) for i, p in enumerate(parents) if i} == set(range(1, n)):
            return f
    raise AssertionError("no graceful fixture")


def main():
    rng = Random(1991)
    total = 0
    for n in range(1, 9):
        for parents in rooted_shapes(n).values():
            f = graceful_fixture(parents)
            for join in range(n):
                profiles = [sorted((rng.randrange(9) for _ in f), reverse=True) for _ in range(2)]
                if join % 3 == 0:
                    profiles[0] = [17] + [0]*(n-1)
                edges, labels = expand(parents, f, join, *profiles)
                assert len(edges) == len(labels)-1
                base = {(c*n+p, c*n+i) for c in (0, 1) for i, p in enumerate(parents) if i}
                base.add((join, join+n))
                populations = [0]*(2*n)
                tips = set()
                for u, v in edges:
                    if max(u, v) < 2*n:
                        base.remove(tuple(sorted((u, v))))
                    else:
                        assert 0 <= u < 2*n <= v < len(labels) and v not in tips
                        tips.add(v)
                        populations[u] += 1
                assert not base and len(tips) == len(labels)-2*n
                for i, g in enumerate(f):
                    assert {labels[i], labels[n+i]} == {-g, 1+g}
                    for v in (i, n+i):
                        assert populations[v] == profiles[labels[v] % 2][g]
                lo, hi = min(labels), max(labels)
                assert sorted(labels) == list(range(lo, hi+1))
                assert sorted(labels[u]+labels[v] for u, v in edges) == list(range(lo+1, hi+1))
                total += 1
    print(f"Verified {total} decorated pairs of graceful trees.")


if __name__ == "__main__":
    main()

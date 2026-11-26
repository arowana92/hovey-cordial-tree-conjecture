"""Check the one-hub construction from the original edges and residue counts."""

from collections import Counter
from random import Random

from research.hub.universal_hub import construct
from research.rainbow.verify import rooted_shapes


def check(tree):
    x, gap, kind = construct(tree)
    h = len(tree)
    e = sum(p > 0 for p in tree)
    if x[0] or len(set(x)) != h or max(x)-min(x) > (2*h+4)*h*2**e:
        raise ValueError("root, injectivity or span failure")
    sums = [x[i]+x[p] for i, p in enumerate(tree) if i]
    target = Counter(x)
    target.subtract([gap])
    if Counter(sums) != +target:
        raise ValueError(f"ordinary endpoint sums failed: {tree}, {x}")
    return kind


def period(tree):
    x, s, _ = construct(tree)
    span = max(x)-min(x)
    for k in (span+1, span+2):
        core = {a % k for a in x}
        gap = s % k
        vertices = [0]*k
        edges = [0]*k
        for a in x:
            vertices[a % k] += 1
        for i, p in enumerate(tree[1:], 1):
            edges[(x[i]+x[p]) % k] += 1
        order = sorted(set(range(k))-core)+[gap]+sorted(core-{gap})
        for v in order*2:
            vertices[v] += 1
            edges[v] += 1
            if max(vertices)-min(vertices)>1 or max(edges)-min(edges)>1:
                raise ValueError("unbalanced modular extension")


def fringe(path, counts):
    # Force the path configuration with an additional short branch at the fork;
    # in the two-arm case use two two-support arms. Counts are extra leaf counts.
    if path:
        tree = [-1, 0, 1, 2, 3, 4, 1, 6]
        sites = [2, 3, 4]
    else:
        tree = [-1, 0, 1, 2, 3, 1, 5, 6]
        sites = [2, 3, 5, 6]
    for p, n in zip(sites, counts):
        tree += [p]*n
    return tree


if __name__ == "__main__":
    from itertools import product
    proofs = Counter()
    for n in range(1, 13):
        for tree in rooted_shapes(n).values():
            proofs[check(tree)] += 1
    cases = 0
    for path in (True, False):
        for counts in product(range(5), repeat=3 if path else 4):
            if check(fringe(path, counts)) != ("path" if path else "two arms"):
                raise ValueError("intended fringe was not used")
            cases += 1
    rng = Random(716053)
    for n in range(20, 201):
        for _ in range(10):
            tree = [-1]+[rng.randrange(i) for i in range(1, n)]
            check(tree)
    for tree in ([-1], [-1, 0, 1, 2], fringe(True, (2, 0, 3)),
                 fringe(True, (0, 4, 0)), fringe(False, (0, 2, 0, 2)),
                 fringe(False, (4, 2, 0, 1))):
        period(tree)
    print(f"All {sum(proofs.values())} rooted shapes through order twelve: {dict(proofs)}.")
    print(f"{cases} fringe profiles, 1810 larger trees, and two full leaf periods "
          "at each of two consecutive moduli on six trees.")

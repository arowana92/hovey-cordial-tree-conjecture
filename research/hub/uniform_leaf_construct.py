"""Construct leaf extensions from a normalized seed and exact parent populations."""

import json
from collections import Counter
from math import lcm
from random import Random

from .many_leaf_parents import Block, verify
from .radius_threshold import split, weighted_tiles
from .two_hubs import Completion
from .uniform_leaf_verify import CERTIFICATE, CORES


def rational_blocks(counts):
    for side, allocation in enumerate(split(counts)):
        for a, b, coefficient in weighted_tiles(allocation, side):
            parents = (side,) if a == 0 else (side+a,) * b + (side-b,) * a
            yield side, parents, coefficient


def dilate(counts):
    tiles = list(rational_blocks(counts))
    factor = lcm(*(c.denominator for _, _, c in tiles))
    return factor, [Block(side, shifts, int(c*factor)) for side, shifts, c in tiles]


def zero_sum_cycles(counts, side):
    # Remove each closed subwalk as soon as its last position repeats.
    path, index = [0], {0: 0}
    for p, copies in counts.items():
        for _ in range(copies):
            target = path[-1] + p - side
            if target not in index:
                index[target] = len(path)
                path.append(target)
                continue
            begin = index[target]
            cycle = path[begin:]
            lo, hi = min(cycle), max(cycle)
            parents = [side] * (hi - lo + 1)
            for u, v in zip(cycle, cycle[1:] + cycle[:1]):
                parents[u-lo] = side + v-u
            yield Block(side, tuple(parents))
            for u in path[begin+1:]:
                del index[u]
            del path[begin+1:]
    assert path == [0]


def exact_blocks(counts):
    """The keys are the core labels. Unused attachment sites may be omitted."""
    if any(n < 0 for n in counts.values()):
        raise ValueError("negative population")
    if not counts or not sum(counts.values()):
        return []
    d = 1 + max(max(counts), 1) - min(min(counts), 0)
    reserve = (2*len(counts) + 2) * d**2
    remaining = Counter(counts)
    total = sum(remaining.values())
    moment = sum(p*n for p, n in remaining.items())
    if not 0 <= moment <= total:
        raise ValueError("parent sum excludes an extension")
    if min(remaining[0], remaining[1]) < reserve:
        raise ValueError("the sufficient two-parent bound does not apply")

    working = remaining.copy()
    working[0] -= min(reserve, total-moment)
    working[1] -= min(reserve, moment)
    blocks = []

    def use(block):
        if block.copies:
            blocks.append(block)
            for p, n in Counter(block.parents).items():
                remaining[p] -= n * block.copies

    residual = working.copy()
    for side, parents, coefficient in rational_blocks(working):
        whole = int(coefficient)
        use(Block(side, parents, whole))
        for p, n in Counter(parents).items():
            residual[p] -= whole*n

    if moment < reserve or total-moment < reserve:
        side = int(total-moment < reserve)
        for block in zero_sum_cycles(residual, side):
            use(block)
    else:
        for p, n in residual.items():
            if p > 1:
                use(Block(1, (p,) + (0,)*(p-1), n))
            elif p < 0:
                use(Block(0, (1,)*(-p) + (p,), n))
    assert all(n >= 0 for n in remaining.values())
    use(Block(0, (0,), remaining[0]))
    use(Block(1, (1,), remaining[1]))
    assert not any(remaining.values())
    return blocks


def check_blocks(counts, blocks):
    actual = Counter()
    below = 0
    for block in blocks:
        n = len(block.parents)
        assert block.copies > 0 and block.offset in [0, 1]
        assert sorted(i + p - block.offset for i, p in enumerate(block.parents)) == list(range(n))
        for p, amount in Counter(block.parents).items():
            actual[p] += amount * block.copies
        below += block.offset * n * block.copies
    assert all(actual[p] == counts.get(p, 0) for p in set(actual) | set(counts))
    assert below == sum(p*n for p, n in counts.items())


def test_blocks():
    rng = Random(1729)
    trials = 0
    for _ in range(500):
        counts = {p: rng.randrange(1, 45) for p in range(-5, 7) if p not in (0, 1)}
        # Adjust the population at 1 to give zero moment. A large negative
        # population makes this adjustment possible without signed counts.
        counts[-5] += 2000
        counts[1] = -sum(p*n for p, n in counts.items())
        counts[0] = 10_000
        for shift in (0, 1, 300, 10_000):
            example = dict(counts)
            example[1] += shift
            for reflected in (example, {1-p: n for p, n in example.items()}):
                check_blocks(reflected, exact_blocks(reflected))
                trials += 1
        small = {p: rng.randrange(4) for p in range(-3, 5)}
        if 0 <= sum(p*n for p, n in small.items()) <= sum(small.values()):
            factor, blocks = dilate(small)
            check_blocks({p: n*factor for p, n in small.items()}, blocks)
            trials += 1
    return trials


def test_trees():
    records = json.loads(CERTIFICATE.read_text())
    rng = Random(314159)
    trials = 0
    for edges, record in zip(CORES, records):
        parents = [-1] + [u for u, v in edges]
        for i in range(40):
            counts = [5000 + rng.randrange(500) for _ in parents]
            if i:
                counts[i % 5] += 10**(3+i)
                counts[(i+1) % 5] += 10**(3+i//2)
            for f, (lo, hi, filler_parents) in record["seeds"]:
                missing = sorted(set(range(lo, hi+1)) - set(f))
                remaining = Counter(dict(zip(f, counts)))
                remaining.subtract(filler_parents)
                try:
                    blocks = exact_blocks(remaining)
                except ValueError:
                    continue
                a, b = edges[0]
                seed = Completion([f[a], f[b]], leaves=zip(filler_parents, missing),
                                  twig_edges=[(f[u], f[v]) for u, v in edges[1:]])
                verify(parents, counts, seed, dict(enumerate(f)), blocks, expand=(i == 0))
                trials += 1
                break
            else:
                raise AssertionError("no accepted seed")
    return trials


if __name__ == "__main__":
    print(f"{test_blocks()} block constructions, {test_trees()} full tree profiles verified.")

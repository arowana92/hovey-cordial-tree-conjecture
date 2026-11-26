"""Linear-range integral vertex labels and endpoint sums, matched up to sign."""

from collections import Counter
from fractions import Fraction
from itertools import chain
from math import ceil, floor
from random import Random

from research.hub.branches import children_of
from research.rainbow.verify import rooted_shapes

# Local parents (-1 = previously labeled attachment), (t,p) coefficients,
# and a rational choice of t/p for which every output has magnitude <= |p|/2.
BLOCKS = {
    "siblings": ((-1, -1), ((-1, -1), (1, 0)), Fraction(-1, 2)),
    "mixed": ((-1, -1, 1), ((2, -1), (-2, 0), (1, 0)), Fraction(1, 4)),
    "three_arms": ((-1, 0, -1, 2, -1, 4),
                   ((2, 0), (2, 1), (6, 1), (-4, -1), (-6, -2), (3, 1)),
                   Fraction(-1, 4)),
    "path": ((-1, 0, 1), ((1, 0), (1, 1), (-2, -1)), Fraction(-1, 2)),
    "fork": ((-1, 0, 1, 0, 3), ((4, 0), (4, 1), (-8, -1), (-2, 0), (1, 0)),
             Fraction(-1, 8)),
}


def decomposition(children, root):
    stack = [root]
    order = []
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(children[v])
    stems = {}
    blocks = []
    for v in reversed(order):
        short, long = [], []
        for child in children[v]:
            stem = stems.pop(child)
            if stem:
                (short if len(stem) == 1 else long).append(stem)
        while len(short) >= 2:
            blocks.append(("siblings", short.pop() + short.pop()))
        while len(long) >= 3:
            blocks.append(("three_arms", long.pop() + long.pop() + long.pop()))
        if short and long:
            blocks.append(("mixed", short.pop() + long.pop()))
        tail = tuple(chain.from_iterable(short + long))
        if v == root:
            return [v, *tail], list(reversed(blocks))
        if long:
            blocks.append(("path" if len(long) == 1 else "fork", (v,) + tail))
            stems[v] = ()
        else:
            stems[v] = (v,) + tail


def construct(parents, zero_root=False, extreme_root=False):
    """With a zero root, treat each of its branches independently."""
    children = children_of(parents)
    n = len(parents)
    if extreme_root and zero_root:
        raise ValueError("an extreme root must be nonzero")
    bound = (84 if extreme_root else 81)*n
    labels = [None]*n
    used = {0}
    if zero_root:
        labels[0] = 0
    for root in children[0] if zero_root else [0]:
        initial, blocks = decomposition(children, root)
        seeds = {1: (12,), 2: (12, -6), 3: (12, -4, 8),
                 5: (12, -2, 1, -10, 5)}[len(initial)]
        scales = [7*n] if extreme_root else range(1, 5*n+2)
        for scale in scales:
            if all(abs(x)*scale not in used for x in seeds):
                break
        else:
            raise ValueError("no initial scale")
        for v, x in zip(initial, seeds):
            labels[v] = scale*x
            used.add(abs(labels[v]))
        for kind, nodes in blocks:
            shape, coefficients, center = BLOCKS[kind]
            p = labels[parents[nodes[0]]]
            if not p:
                raise ValueError("unlabeled or zero attachment")
            for v, local in zip(nodes, shape):
                if parents[v] != (parents[nodes[0]] if local < 0 else nodes[local]):
                    raise ValueError("incorrect block partition")
            a = max(abs(c) for c, _ in coefficients)
            radius = Fraction(bound, 2*a)
            for t in range(ceil(center*p-radius), floor(center*p+radius)+1):
                values = [c*t+d*p for c, d in coefficients]
                magnitudes = set(map(abs, values))
                if len(magnitudes) == len(nodes) and used.isdisjoint(magnitudes):
                    break
            else:
                raise ValueError("no free parameter")
            for v, x in zip(nodes, values):
                labels[v] = x
            used.update(magnitudes)
    return labels


def check(parents, labels):
    n = len(parents)
    if len({abs(x) for x in labels}) != n or max(map(abs, labels)) > 81*n:
        raise ValueError("vertex magnitude collision or bound exceeded")
    sums = [abs(labels[v]+labels[p]) for v, p in enumerate(parents) if v]
    if Counter(sums) != Counter(map(abs, labels[1:])):
        raise ValueError("endpoint sums do not match the nonroot magnitudes")


def check_reflections(parents, labels, join):
    m = len(parents)
    edges = [(v, p) for v, p in enumerate(parents) if v]
    both = edges + [(v+m, p+m) for v, p in edges]
    values = labels + [-x for x in labels] + [0]
    for links, missing in (([(0, 2*m), (m, 2*m)], 0),
                           ([(join, join+m), (0, 2*m)], -labels[0])):
        sums = [values[u]+values[v] for u, v in both+links]
        target = Counter(values)
        target.subtract([missing])
        if len(set(values)) != 2*m+1 or Counter(sums) != +target:
            raise ValueError("reflected endpoint sums or vertex labels failed")


def check_interval(parents):
    n = len(parents)
    x = construct(parents, extreme_root=True)
    p = x[0]
    labels = x + [-v for v in x] + [0]
    edges = [(i, j) for i, j in enumerate(parents) if i]
    join = n-1
    sums = [labels[i]+labels[j] for i, j in edges]
    sums += [labels[n+i]+labels[n+j] for i, j in edges]
    sums += [labels[join]+labels[n+join], labels[0]+labels[2*n]]
    added = sorted(set(range(-p, p+1))-set(labels))
    if (p != 84*n or len(added) != 166*n or
            sorted(sums+added) != list(range(1-p, p+1)) or
            sorted(labels+added) != list(range(-p, p+1))):
        raise ValueError("reflected interval completion failed")


if __name__ == "__main__":
    checked = 0
    for n in range(1, 10):
        for tree in rooted_shapes(n).values():
            for zero in (True, False):
                labels = construct(tree, zero)
                check(tree, labels)
            check_reflections(tree, labels, checked % n)
            check_interval(tree)
            checked += 1
    rng = Random(761)
    large = [tuple([-1]+[rng.randrange(i) for i in range(1, n)])
             for n in (80, 127, 256, 400)]
    large += [tuple([-1]+list(range(399))), tuple([-1]+[0]*399),
              tuple([-1]+[(i-1)//2 for i in range(1, 400)])]
    for tree in large:
        for zero in (True, False):
            labels = construct(tree, zero)
            check(tree, labels)
        check_reflections(tree, labels, len(tree)//2)
        check_interval(tree)
    print(f"Both root conventions on {checked} rooted shapes through order nine "
          f"and {len(large)} larger trees; both reflected edge sets and interval completions checked.")

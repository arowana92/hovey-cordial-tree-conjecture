"""Integer witnesses from an anchor at the hub or a coprime branch order."""

import argparse
from itertools import count
from math import gcd
from random import Random

from research.rainbow.verify import rooted_shapes


def children_of(parents):
    children = [[] for _ in parents]
    for i in range(1, len(parents)):
        children[parents[i]].append(i)
    return children


def anchor_labels(parents):
    """Use one hub neighbor with children, at most one of them nonterminal."""
    children = children_of(parents)
    roots = children[0]
    for anchor in roots:
        nonterminal = [i for i in children[anchor] if children[i]]
        if children[anchor] and len(nonterminal) <= 1:
            tip = nonterminal[0] if nonterminal else children[anchor][0]
            break
    else:
        return None

    labels = [None] * len(parents)
    labels[0] = 0
    for value, i in enumerate((i for i in roots if i != anchor), 1):
        labels[i] = value
    seed = len(roots)
    labels[tip] = -seed
    negative = seed
    positive = 0
    for i, p in enumerate(parents[1:], 1):
        if p == 0 or p == anchor:
            continue
        if labels[p] > 0:
            negative += labels[p]
            labels[i] = -negative
        else:
            positive -= labels[p]
            labels[i] = positive
    labels[anchor] = positive + seed
    for i in children[anchor]:
        if i != tip:
            negative += labels[anchor]
            labels[i] = -negative
    return labels


def coefficients(parents, order):
    """Assign the running pair to a vertex, then add the pair of its parent."""
    pairs = [None] * len(parents)
    pairs[0] = (1, 0)
    a, b = 0, 1
    for i in order:
        pairs[i] = (a, b)
        u, v = pairs[parents[i]]
        a, b = a + u, b + v
    return pairs, (a, b)


def attach_branch(branch, order, old_labels, missing, modulus=None):
    """Return new labels and the resulting missing weight at a zero-labeled hub."""
    pairs, (a, b) = coefficients(branch, order)
    if not order or gcd(a, b) != 1:
        raise ValueError("expected a nontrivial branch with a coprime order")
    x = missing * pow(a, -1, b)
    y = (missing - a * x) // b
    for t in count() if modulus is None else range(modulus):
        labels = [u * (x + b * t) + v * (y - a * t) for u, v in pairs]
        if modulus is not None:
            labels = [label % modulus for label in labels]
        if len(set(labels)) == len(branch) and set(labels).isdisjoint(old_labels):
            return labels, labels[order[0]]
    raise ValueError("no collision-free parameter at this modulus")


def schedules(parents, rng):
    children = children_of(parents)

    def depth_first(i, reverse):
        for child in reversed(children[i]) if reverse else children[i]:
            yield child
            yield from depth_first(child, reverse)

    for reverse in (False, True):
        yield list(depth_first(0, reverse))
    yield list(range(1, len(parents)))
    for _ in range(60):
        ready = list(children[0])
        order = []
        while ready:
            i = ready.pop(rng.randrange(len(ready)))
            order.append(i)
            ready.extend(children[i])
        yield order


def check_labels(parents, labels, modulus=None):
    weights = [labels[i] + labels[parents[i]] for i in range(1, len(labels))]
    if modulus is not None:
        weights = [w % modulus for w in weights]
    if (labels[0] != 0 or len(set(labels)) != len(parents)
            or len(set(weights)) != len(weights) or not set(weights) <= set(labels)):
        raise ValueError(f"invalid integer witness: {parents}, {labels}")
    return (set(labels) - set(weights)).pop()


def check_mixed_branches():
    branches = [(-1, 0), (-1, 0, 0, 1, 2), (-1, 0, 1, 2),
                (-1, 0, 0, 1, 1, 2, 2)]
    for modulus in (None, 1009, 1024, 1155):
        parents, labels, missing = [-1], [0], 0
        for branch in branches:
            for order in schedules(branch, Random(5)):
                if gcd(*coefficients(branch, order)[1]) == 1:
                    break
            added, missing = attach_branch(branch, order, labels, missing, modulus)
            offset = len(parents)
            parents.extend(p + offset if p >= 0 else 0 for p in branch)
            labels.extend(added)
            if check_labels(parents, labels, modulus) != missing:
                raise ValueError("wrong missing weight after gluing branches")


def check(up_to):
    rng = Random(5)
    maximum = 1
    for n in range(2, up_to + 1):
        shapes = rooted_shapes(n)
        anchors = 0
        for parents in shapes.values():
            labels = anchor_labels(parents)
            if labels is not None:
                if check_labels(parents, labels) != min(labels):
                    raise ValueError("wrong missing anchor weight")
                anchors += 1

            for order in schedules(parents, rng):
                pairs, (a, b) = coefficients(parents, order)
                if gcd(a, b) == 1:
                    break
            else:
                raise ValueError(f"no coprime order found for {parents}")
            slopes = [u * b - v * a for u, v in pairs]
            extended = (-1,) + tuple(p + 1 for p in parents)
            if check_labels(extended, [0] + slopes) != slopes[order[0]]:
                raise ValueError("wrong missing branch weight")
            maximum = max(maximum, max(0, *slopes) - min(0, *slopes))
        print(f"order {n}: {len(shapes)} coprime branches, {anchors} anchored cores, "
              f"maximum slope span so far {maximum}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("order", type=int, nargs="?", default=16)
    check_mixed_branches()
    check(parser.parse_args().order)

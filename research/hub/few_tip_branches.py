"""Check short, unary-suppressed branches with up to four terminal vertices."""

from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import comb, gcd
from random import Random

from research.hub.branches import coefficients, schedules


def partitions(n, least=1):
    if n == 0:
        yield ()
    for first in range(least, n+1):
        for tail in partitions(n-first, first):
            yield (first,) + tail


@lru_cache(None)
def forks(leaves):
    """An arm is (length, subtree). At every fork the arm tuple is sorted."""
    if leaves == 1:
        return ((),)
    result = []
    for parts in partitions(leaves):
        if len(parts) < 2:
            continue
        groups = []
        for size, copies in Counter(parts).items():
            arms = [(length, subtree) for length in range(1, 8)
                    for subtree in forks(size)]
            groups.append(combinations_with_replacement(arms, copies))
        for selections in product(*groups):
            result.append(tuple(sorted(arm for group in selections for arm in group)))
    return tuple(result)


def expand(tree):
    parents = [-1]

    def visit(v, children):
        for length, subtree in children:
            p = v
            for _ in range(length):
                parents.append(p)
                p = len(parents)-1
            visit(p, subtree)

    visit(0, tree)
    return parents


def counts(limit):
    # Formal series for multisets of child arms, by number of terminal vertices.
    numbers = [0, 1]
    for leaves in range(2, limit+1):
        counts_by_size = [1] + [0]*leaves
        for size in range(1, leaves):
            choices = 7*numbers[size]
            nxt = [0]*(leaves+1)
            for old, ways in enumerate(counts_by_size):
                for take in range((leaves-old)//size+1):
                    nxt[old+take*size] += ways*comb(choices+take-1, take)
            counts_by_size = nxt
        numbers.append(counts_by_size[leaves])
    return numbers


def verify_order(parents, order):
    # Set the root label provisionally to one and the initial running label to
    # zero and then vice versa. The linear combination closes the terminal at zero.
    def run(root, first):
        labels = [None]*len(parents)
        labels[0] = root
        current = first
        for v in order:
            if labels[v] is not None or labels[parents[v]] is None:
                raise ValueError("invalid parent-before-child order")
            labels[v] = current
            current += labels[parents[v]]
        return current

    a, b = run(1, 0), run(0, 1)
    labels = [None]*len(parents)
    labels[0] = b
    current = -a
    for v in order:
        labels[v] = current
        current += labels[parents[v]]
    weights = [labels[v]+labels[p] for v, p in enumerate(parents) if v]
    weights.append(labels[0])  # edge from the zero hub
    if (current != 0 or gcd(a, b) != 1 or 0 in labels or
            len(set(labels)) != len(labels) or
            Counter(weights) != Counter([0] + [x for x in labels if x != -a])):
        raise ValueError("failed integer labeling")


def check(limit=4):
    expected = counts(limit)
    for tips in range(2, limit+1):
        trees = forks(tips)
        if len(set(trees)) != expected[tips] or len(trees) != expected[tips]:
            raise ValueError("incomplete fork enumeration")
        attempts = 0
        for tree in trees:
            parents = expand(tree)
            rng = Random(17)
            for i, order in enumerate(schedules(parents, rng), 1):
                if gcd(*coefficients(parents, order)[1]) == 1:
                    break
            else:
                raise ValueError(f"no coprime order for {tree}")
            verify_order(parents, order)
            attempts = max(attempts, i)
        print(f"{tips} tips: {len(trees)} branches, at most {attempts} orders tried.",
              flush=True)


if __name__ == "__main__":
    check()

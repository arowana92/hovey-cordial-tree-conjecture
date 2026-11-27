"""Independent direct integer checks and exhaustive tests of the fixed-pair criterion."""

from itertools import product
from random import Random

from research.hub.matched_arms import arm_tree, interval_lift
from research.rainbow.generate import rainbow
from research.rainbow.verify import rooted_shapes


def consecutive(edges, labels):
    m = len(labels) // 2
    return (sorted(labels) == list(range(2*m))
            and sorted(labels[u]+labels[v] for u, v in edges) == list(range(m, 3*m-1)))


def feasible_by_enumeration(edges, indices):
    m = len(indices)
    for choices in product((0, 1), repeat=m):
        labels = [x + m * (choice ^ port)
                  for x, choice in zip(indices, choices) for port in (0, 1)]
        if consecutive(edges, labels):
            return True
    return False


def main():
    families = successes = failures = 0
    for h in range(161):
        for a in range(h//2, 2*h - h//2 + 1):
            edges, labels = arm_tree(a, 2*h-a)
            assert consecutive(edges, labels)
            assert edges[0] == (0, 1)
            assert sum(u == 0 for u, _ in edges[1:]) == a
            assert sum(u == 1 for u, _ in edges[1:]) == 2*h-a
            for i in range(1, 2*h + 1):
                assert edges[2*i-1][1] == 2*i and edges[2*i] == (2*i, 2*i+1)
            families += 1
    rng = Random(1991)
    for m in (3, 5, 7):
        for parents in rooted_shapes(m).values():
            f = [0] + rainbow(tuple(j-1 for j in parents[1:]), m)
            used = {(f[p]+f[i]) % m for i, p in enumerate(parents) if i}
            missing, = set(range(m)) - used
            shift = (-1-missing)*pow(2, -1, m)
            indices = [(x+shift) % m for x in f]
            if m <= 5:
                all_joins = product(tuple(product((0, 1), repeat=2)), repeat=m-1)
            else:
                all_joins = [[(rng.randrange(2), rng.randrange(2)) for _ in parents[1:]]
                             for _ in range(15)]
            for joins in all_joins:
                edges = [(2*i, 2*i+1) for i in range(m)]
                edges.extend((2*p+left, 2*i+right)
                             for i, (p, (left, right)) in enumerate(zip(parents[1:], joins), 1))
                actual = interval_lift(parents, indices, joins)
                expected = feasible_by_enumeration(edges, indices)
                assert (actual is not None) == expected
                if expected:
                    assert consecutive(edges, actual)
                    successes += 1
                else:
                    failures += 1
    print(f"Verified {families} two-center labelings.")
    print(f"Fixed pair allocations: {successes} feasible and {failures} infeasible.")


if __name__ == "__main__":
    main()

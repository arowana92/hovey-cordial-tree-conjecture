"""Construct sparse branch forms and verify ordinary vertex and edge histograms."""

from collections import Counter
from itertools import product

from research.hub.branches import coefficients
from research.rainbow.verify import rooted_shapes


def build(branches):
    r = len(branches)
    if r < 2 or any(len(branch) < 2 for branch in branches):
        raise ValueError("expected at least two nonsingleton branches")
    data = [coefficients(branch, range(1, len(branch))) for branch in branches]
    parents = [-1]
    forms = [(0,) * r]
    for i, (branch, (vectors, (a, b))) in enumerate(zip(branches, data)):
        offset = len(parents)
        j = (i + 1) % r
        before, after = data[i-1][1][0], data[j][1][0]
        for p, (u, v) in zip(branch, vectors):
            row = [0] * r
            row[i] = (a*v - b*u) * before
            row[j] = u * after
            forms.append(tuple(row))
            parents.append(0 if p < 0 else offset + p)
    return parents, forms


def specialize(forms, modulus):
    r = len(forms[0])
    conditions = [[] for _ in range(r)]
    for i, row in enumerate(forms):
        for old in forms[:i]:
            diff = tuple(x-y for x, y in zip(row, old))
            last = max(j for j, x in enumerate(diff) if x)
            conditions[last].append(diff)
    values = []
    for j, tests in enumerate(conditions):
        restrictions = [(w[j], sum(x*t for x, t in zip(w, values))) for w in tests]
        for t in range(modulus):
            if all((d*t + c) % modulus for d, c in restrictions):
                values.append(t)
                break
        else:
            raise ValueError("all parameter values excluded")
    return [sum(x*t for x, t in zip(row, values)) % modulus for row in forms]


def check_identity(branches):
    parents, forms = build(branches)
    edges = [tuple(x+y for x, y in zip(forms[i], forms[p]))
             for i, p in enumerate(parents) if i]
    assert len(set(forms)) == len(parents)
    assert Counter(edges) == Counter(forms[1:])
    return parents, forms


def check_modular(branches, k):
    parents, forms = check_identity(branches)
    labels = specialize(forms, k)
    edge_values = [(labels[i]+labels[p]) % k for i, p in enumerate(parents) if i]
    assert len(set(labels)) == len(labels)
    assert Counter(edge_values) == Counter(labels[1:])
    vertex_counts = Counter(labels)
    edge_counts = Counter(edge_values)
    cycle = sorted(set(range(k)) - set(labels)) + [0] + sorted(labels[1:])
    for leaf in cycle * 2:
        vertex_counts[leaf] += 1
        edge_counts[leaf] += 1
        for counts in (vertex_counts, edge_counts):
            low = sum(counts.values()) // k
            assert low <= min(counts.values()) and max(counts.values()) <= low + 1
            assert len(counts) == k or low == 0


if __name__ == "__main__":
    shapes = [t for n in range(2, 7) for t in rooted_shapes(n).values()]
    tested = 0
    # The middle branch ranges over every rooted shape through order nine.
    for n in range(2, 10):
        for i, branch in enumerate(rooted_shapes(n).values()):
            for left, right in ((shapes[0], shapes[-1]),
                                (shapes[i % len(shapes)], shapes[-1-i % len(shapes)])):
                check_identity([left, branch, right])
                tested += 1
    for branches in product(shapes[:3], repeat=4):
        check_identity(branches)
        tested += 1
    for k in (97, 256, 315):
        check_modular([shapes[2], shapes[8], shapes[12], shapes[25]], k)
    # With only two branches, equal stars share their midpoint form.
    _, two = build([(-1, 0, 0)] * 2)
    assert len(set(two)) < len(two)
    print(f"{tested} multivariate identities; integer specializations modulo 97, 256, 315; "
          "two full periods of extra leaves at each modulus.")

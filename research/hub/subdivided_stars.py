"""Cordial labels for partially subdivided stars and paired stars at a hub."""

from itertools import combinations_with_replacement, cycle, islice

from research.repeated_branches import branch_labels


def folded_block(m, start):
    """Map each signed difference in ±1,...,±m to a tip in one interval."""
    if not m:
        return {}
    zigzag = [i // 2 if i % 2 == 0 else m - 1 - i // 2 for i in range(m)]
    walk = zigzag + [m + a for a in reversed(zigzag)]
    return {walk[(i + 1) % len(walk)] - a: start + a for i, a in enumerate(walk)}


def odd_core(pair_sizes):
    """One special two-edge leg and pairs of stars with given child counts."""
    m = len(pair_sizes)
    sizes = sorted(pair_sizes, reverse=True)
    start = m + 2
    branches = {c: [] for c in range(-m, m + 1) if c}
    branches[m + 1] = [-m - 1]
    for j in range(1, max(sizes, default=0) + 1):
        active = sum(n >= j for n in sizes)
        for center, tip in folded_block(active, start).items():
            branches[center].append(tip)
        start += 2 * active
    return branches


def paired_templates(pair_sizes):
    """Construct both integer templates when the smallest pair has one child."""
    sizes = sorted(pair_sizes, reverse=True)
    m = len(sizes)
    first = {i: [] for i in range(-m, m + 1) if i}
    start = m + 1
    for j in range(1, max(sizes) + 1):
        active = sum(n >= j for n in sizes)
        for center, tip in folded_block(active, start).items():
            first[center].append(tip)
        start += 2 * active
    if sizes[-1] != 1:
        raise ValueError("the second template uses a pair of one-child neighbors")
    second = odd_core(sizes[:-1])
    second[-m - 1] = [1]
    return first, second


def legs_at_modulus(d, k):
    """Return (center, tip) labels for d two-edge legs at a hub labeled zero."""
    blocks, residual = divmod(d, k)
    if residual == 0:
        legs = []
    elif residual % 2:
        branches = odd_core([1] * (residual // 2))
        legs = [(c, tips[0]) for c, tips in branches.items()]
    else:
        m = residual // 2
        if 3 * m < k <= 4 * m:
            branches = odd_core([1] * (m - 1))
            legs = [(c, tips[0]) for c, tips in branches.items()]
            legs.append((-m - 1, 1))
        else:
            legs = list(folded_block(m, m + 1).items())
    if blocks:
        legs.extend(branch_labels((-1, 0), k) * blocks)
    return [(c % k, t % k) for c, t in legs]


def histograms(legs, k):
    vertices, weights = [0] * k, [0] * k
    vertices[0] = 1
    for c, t in legs:
        vertices[c] += 1
        vertices[t] += 1
        weights[c] += 1
        weights[(c + t) % k] += 1
    return vertices, weights


def leaf_period(vertices, weights):
    """List one period that can be appended at the hub in any prefix length."""
    s, = [i for i, (v, e) in enumerate(zip(vertices, weights)) if v == e + 1]
    if max(vertices) == min(vertices):
        return [s] + [i for i in range(len(vertices)) if i != s]
    low = min(vertices)
    return ([i for i, v in enumerate(vertices) if v == low] + [s]
            + [i for i, v in enumerate(vertices) if v != low and i != s])


def check():
    integer_cases = 0
    for m in range(7):
        for sizes in combinations_with_replacement(range(1, 7), m):
            branches = odd_core(sizes)
            degrees = sorted(len(tips) for tips in branches.values())
            if degrees != sorted([1, *sizes, *sizes]):
                raise ValueError("wrong multiset of child counts")
            labels = sorted([0, *branches] + [a for tips in branches.values() for a in tips])
            sums = sorted(list(branches) + [c + a for c, ts in branches.items() for a in ts])
            if labels != list(range(-m - 1, -m - 1 + len(labels))) or sums != labels[1:]:
                raise ValueError(("integer intervals", sizes))
            integer_cases += 1
            if m and sizes[0] == 1:
                first, second = paired_templates(sizes)
                for index, template in enumerate((first, second)):
                    if sorted(map(len, template.values())) != sorted([*sizes, *sizes]):
                        raise ValueError("wrong shape for paired template")
                    labels = [0, *template] + [v for ts in template.values() for v in ts]
                    weights = list(template) + [c + v for c, ts in template.items() for v in ts]
                    if index == 0:
                        expected = list(range(-m, -m + len(labels)))
                        if sorted(labels) != expected or sorted(weights + [0]) != expected:
                            raise ValueError("first paired template")
                    else:
                        expected = list(range(-m - 1, -m - 1 + len(weights)))
                        if sorted(weights) != expected or sorted(expected + [1]) != sorted(labels):
                            raise ValueError("second paired template")
    modular_cases = 0
    for k in range(1, 97):
        for d in range(2 * k + 1):
            legs = legs_at_modulus(d, k)
            if len(legs) != d:
                raise ValueError("wrong number of two-edge legs")
            vertices, weights = histograms(legs, k)
            period = leaf_period(vertices, weights)
            if sorted(period) != list(range(k)):
                raise ValueError("invalid period")
            for leaf in islice(cycle(period), 2 * k + 1):
                if max(vertices) - min(vertices) > 1 or max(weights) - min(weights) > 1:
                    raise ValueError(("cordial counts", k, d))
                vertices[leaf] += 1
                weights[leaf] += 1
            modular_cases += 1
    print(f"Verified {integer_cases} paired-star cores and {modular_cases} modulus/leg pairs.")


if __name__ == "__main__":
    check()

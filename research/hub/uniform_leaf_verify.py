"""Independently verify five-vertex seeds and a covering of their population simplex."""

import json
from fractions import Fraction
from itertools import permutations
from pathlib import Path

CERTIFICATE = Path(__file__).with_name("five-vertex-leaf-seeds.json")
CORES = [
    [(0, 1), (1, 2), (2, 3), (3, 4)],
    [(0, 1), (0, 2), (0, 3), (0, 4)],
    [(0, 1), (0, 2), (0, 3), (1, 4)],
]


def check_seed(edges, seed):
    labels, (lo, hi, parents) = seed
    assert len(labels) == len(set(labels)) == 5
    assert {0, 1} <= set(labels) <= set(range(lo, hi + 1))
    missing = sorted(set(range(lo, hi + 1)) - set(labels))
    assert len(missing) == len(parents) and set(parents) <= set(labels)
    weights = [labels[u] + labels[v] for u, v in edges]
    weights.extend(x + p for x, p in zip(missing, parents))
    assert sorted(weights) == list(range(lo + 1, hi + 1))


def midpoint(a, b):
    return tuple((x + y) / 2 for x, y in zip(a, b))


def verify_cover(seeds, node, apex, start, stop, facet):
    if isinstance(node, int):
        assert 0 <= node < len(seeds)
        labels = seeds[node][0]
        # Bound both slacks below by eta times the mass off the largest vertex.
        margin = Fraction(1)
        for t in (start, stop):
            for z in facet:
                x = [t * value for value in z]
                x[apex] += 1 - t
                value = sum(a * b for a, b in zip(labels, x))
                if t == 0:
                    assert 0 <= value <= 1
                else:
                    assert 0 < value < 1 and x[apex] < 1
                    margin = min(margin, value / (1 - x[apex]),
                                 (1 - value) / (1 - x[apex]))
        return 1, margin
    if node[0] == "t":
        _, left, right = node
        middle = (start + stop) / 2
        a = verify_cover(seeds, left, apex, start, middle, facet)
        b = verify_cover(seeds, right, apex, middle, stop, facet)
    else:
        i, j, left, right = node
        assert 0 <= i < j < 4
        middle = midpoint(facet[i], facet[j])
        first, second = facet.copy(), facet.copy()
        first[i], second[j] = middle, middle
        a = verify_cover(seeds, left, apex, start, stop, first)
        b = verify_cover(seeds, right, apex, start, stop, second)
    return a[0] + b[0], min(a[1], b[1])


def main():
    records = json.loads(CERTIFICATE.read_text())
    assert len(records) == len(CORES)
    for edges, record in zip(CORES, records):
        seeds = record["seeds"]
        for seed in seeds:
            check_seed(edges, seed)
        chambers = list(permutations(range(5)))
        assert len(record["cover"]) == len(chambers)
        margin, cells = Fraction(1), 0
        for order, cert in zip(chambers, record["cover"]):
            facet = [tuple(Fraction(int(i in order[:r]), r) for i in range(5))
                     for r in range(2, 6)]
            count, eta = verify_cover(seeds, cert, order[0],
                                      Fraction(0), Fraction(1), facet)
            cells += count
            margin = min(margin, eta)
        d = max(max(f) - min(f) + 1 for f, _ in seeds)
        fillers = max(len(parents) for _, (_, _, parents) in seeds)
        reserve = 12 * d**2
        required = (reserve + fillers*d) / (4 * margin)
        bound = max(reserve + fillers, -(-required.numerator // required.denominator))
        print(f"{len(seeds)} seeds, {cells} cells, eta={margin}, "
              f"D={d}, F={fillers}, sufficient minimum={bound}")


if __name__ == "__main__":
    main()

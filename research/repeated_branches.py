"""Construct k balanced copies of a rooted branch, and audit both histograms."""

import argparse
from collections import Counter

from research.rainbow.verify import rooted_shapes


def branch_labels(parents, k, hub=0):
    """Return the free vertex labels, one tuple per copy, in parent-vector order."""
    n = len(parents)
    if k < 1 or not parents or parents[0] != -1 or any(
        not 0 <= parents[v] < v for v in range(1, n)
    ):
        raise ValueError("expected positive modulus and a parent-first rooted tree")

    if k % 2:
        return [((hub + i) % k,) * n for i in range(k)]

    if n % 2:
        offsets = [0]
        for v in range(1, n):
            offsets.append((v % 2) - offsets[parents[v]])
        return [tuple((hub + i + c) % k for c in offsets) for i in range(k)]

    degrees = [int(v != 0) for v in range(n)]
    for parent in parents[1:]:
        degrees[parent] += 1
    special = next(v for v in range(1, n) if (degrees[v] - degrees[0]) % 2 == 0)
    odd_left = (n - degrees[0] - degrees[special]) // 2
    parity = [0] * n
    for v in range(1, n):
        parent = parents[v]
        if v == special:
            parity[v] = 1
        elif parent not in (0, special):
            chosen = odd_left > 0
            parity[v] = parity[parent] ^ chosen
            odd_left -= chosen
    layouts = [parity, [b if v in (0, special) else 1 - b for v, b in enumerate(parity)]]

    offsets = [[0] * n for _ in layouts]
    parity_counts = [0, 0]
    for bits, labels in zip(layouts, offsets):
        for v in range(1, n):
            parent = parents[v]
            edge_parity = bits[parent] ^ bits[v]
            weight = edge_parity + 2 * (parity_counts[edge_parity] % 2)
            parity_counts[edge_parity] += 1
            labels[v] = weight - labels[parent]
    return [tuple((hub + 2 * i + c) % k for c in profile)
            for profile in offsets for i in range(k // 2)]


def verify(max_order, max_modulus):
    shapes = cases = 0
    for n in range(1, max_order + 1):
        for parents in rooted_shapes(n).values():
            shapes += 1
            for k in range(1, max_modulus + 1):
                for hub in {0, k // 2, k - 1}:
                    copies = branch_labels(parents, k, hub)
                    vertices, edges = Counter(), Counter()
                    if len(copies) != k:
                        raise ValueError("wrong number of copies")
                    for labels in copies:
                        if len(labels) != n or any(not 0 <= a < k for a in labels):
                            raise ValueError("invalid label vector")
                        vertices.update(labels)
                        edges.update((a + (hub if b < 0 else labels[b])) % k
                                     for a, b in zip(labels, parents))
                    target = Counter({a: n for a in range(k)})
                    if vertices != target or edges != target:
                        raise ValueError((k, hub, parents, vertices, edges))
                    cases += 1
    print(f"Verified both histograms in {cases} cases on {shapes} rooted trees.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--order", type=int, default=9)
    parser.add_argument("--modulus", type=int, default=24)
    args = parser.parse_args()
    if min(args.order, args.modulus) < 1:
        parser.error("positive bounds required")
    verify(args.order, args.modulus)

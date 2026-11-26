"""Validate the affine identities and range constants without selecting a parameter."""

from collections import Counter

from research.hub.signed_tree import BLOCKS


def unsigned_form(row):
    return min(row, tuple(-x for x in row))


for name, (parents, values, center) in BLOCKS.items():
    old = (0, 1)
    target = Counter(map(unsigned_form, values))
    weights = []
    for v, parent in enumerate(parents):
        first = old if parent < 0 else values[parent]
        weights.append(tuple(a+b for a, b in zip(first, values[v])))
    if Counter(map(unsigned_form, weights)) != target or len(target) != len(parents):
        raise ValueError(f"{name}: affine identity or signed distinctness")
    if any(a == 0 or abs(a*center+b)*2 > 1 for a, b in values):
        raise ValueError(f"{name}: constant form or range error")
    if 2*len(values)*max(abs(a) for a, _ in values) >= 81:
        raise ValueError(f"{name}: insufficient parameter interval")
print("All five affine identities, distinctness conditions and range constants verified.")

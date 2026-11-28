"""Find a minimum set of witness permutations for each eight-label ordered cut."""

from collections import Counter
from functools import lru_cache
from itertools import permutations, product
from pathlib import Path
import struct
import sys


def shapes():
    # Add an auxiliary root 0 to seven free vertices. Every rooted tree has
    # a numbering in which each parent precedes its children.
    words = set()
    for parents in product(*(range(i) for i in range(1, 8))):
        children = [[] for _ in range(8)]
        for i in range(7, 0, -1):
            word = "1" + "".join(sorted(children[i], key=lambda s: (len(s), s))) + "0"
            children[parents[i - 1]].append(word)
        words.add("".join(sorted(children[0], key=lambda s: (len(s), s))))
    return sorted(words)


def decode(word):
    parents, roots, stack = [], [], []
    for bit in word:
        if bit == "0":
            stack.pop()
            continue
        i = len(parents)
        if not stack:
            roots.append(i)
        parents.append(stack[-1] if stack else -1)
        stack.append(i)
    sizes = [end - start for start, end in zip(roots, roots[1:] + [7])]
    return parents, roots, sizes


def boundary_orbits(sizes, tips):
    count = len(sizes)
    if tips > 4:
        return {(0,) * count: 0}
    profiles = {(a,) * count for a in range(8)}
    for i in range(1, count):
        if sizes[i] > sum(sizes[:i]):
            profiles.update((a,) * i + (b,) * (count - i)
                            for a, b in product(range(8), repeat=2))
    # Three actual runs need at least eight vertices. All units preserve zero.
    keys = {p: min(tuple(u * a % 8 for a in p) for u in (1, 3, 5, 7)) for p in profiles}
    index = {key: i for i, key in enumerate(sorted(set(keys.values())))}
    return {p: index[key] for p, key in keys.items()}


def covers(word):
    parents, roots, sizes = decode(word)
    orbits = boundary_orbits(sizes, word.count("10"))
    full = (1 << (1 + max(orbits.values()))) - 1
    masks = {}
    for row in permutations(range(1, 8)):
        if next(x for x in row if x % 2) != 1:
            continue
        used = {(row[i] + row[p]) % 8 for i, p in enumerate(parents) if p >= 0}
        if len(used) != 7 - len(roots):
            continue
        mask = 0
        for colors, orbit in orbits.items():
            edges = used.union((row[r] + a) % 8 for r, a in zip(roots, colors))
            if len(edges) == 7:
                mask |= 1 << orbit
        if mask:
            masks.setdefault(mask, row)
    maximal = {}
    for mask in sorted(masks, key=lambda m: bin(m).count("1"), reverse=True):
        if all(mask & other != mask for other in maximal):
            maximal[mask] = masks[mask]
    return maximal, full


def minimum(masks, full):
    options = [[m for m in masks if m & (1 << i)] for i in range(full.bit_length())]
    weight = lambda m: bin(m).count("1")
    largest = max(map(weight, masks))

    @lru_cache(None)
    def solve(need, budget):
        if not need:
            return ()
        if budget == 0 or weight(need) > budget * largest:
            return None
        choices = min((opts for i, opts in enumerate(options) if need & (1 << i)), key=len)
        # A larger intersection always does at least as well on the remaining
        # inputs. Keep a corresponding original mask for certificate output.
        next_masks = {m & need: m for m in choices}
        visited = []
        for hit in sorted(next_masks, key=weight, reverse=True):
            if weight(need) - weight(hit) > (budget - 1) * largest:
                break
            if any(hit & other == hit for other in visited):
                continue
            visited.append(hit)
            tail = solve(need & ~hit, budget - 1)
            if tail is not None:
                return (next_masks[hit],) + tail
        return None

    for budget in range(1, full.bit_length() + 1):
        result = solve(full, budget)
        if result is not None:
            return result
    raise ValueError("some boundary has no witness")


def main(output):
    histogram = Counter()
    data = bytearray(b"SPN2\x08")
    worst = []
    for word in shapes():
        masks, full = covers(word)
        chosen = minimum(masks, full)
        histogram[len(chosen)] += 1
        worst.append((len(chosen), word))
        data.extend(struct.pack("<QI", int(word, 2), len(chosen)))
        for mask in chosen:
            data.extend(masks[mask])
    if output is not None:
        output.write_bytes(data)
    print(f"minimum rows by forest: {sorted(histogram.items())}")
    print(f"{sum(histogram.values())} shapes, {sum(n*c for n,c in histogram.items())} rows, "
          f"{len(data)} bytes")
    print("worst shapes:", [w for n, w in worst if n == max(histogram)])


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)

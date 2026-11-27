"""Replay the leaf-to-matching reduction on explicitly labeled trees."""

from random import Random

from .check_spare_lists import verify_choice


def counts(values, k):
    histogram = [0] * k
    for value in values:
        histogram[value % k] += 1
    return histogram


def check_tree(k, leaves, periods, s, rng):
    h = periods * k + s - leaves
    split = (h + 1) // 2
    labels = [(i // 2 + (i % 2) * split) % k for i in range(h)]
    edges = [(i - 1, i, 0) for i in range(1, h)]
    vertex_counts = counts(labels, k)
    weight_counts = counts((labels[i] + labels[j] for i, j, _ in edges), k)
    assert max(vertex_counts) == max(weight_counts) == periods + 1
    assert min(vertex_counts) == min(weight_counts) == periods

    # Keep both path ends as parents so the added vertices are exactly its leaves.
    parents = [0, h - 1] + [rng.randrange(h) for _ in range(leaves - 2)]
    if periods == 0:
        offsets = [0] * leaves
    elif periods == 1:
        # All colors then contain parallel copies of precisely the same edges.
        offsets = [(-labels[parent]) % k for parent in parents]
    else:
        offsets = [rng.randrange(k) for _ in parents]
    shifts = [(labels[parent] + offset) % k for parent, offset in zip(parents, offsets)]
    lists = []
    for shift in shifts:
        allowed = [x for x in range(k)
                   if vertex_counts[x] == periods and weight_counts[(x + shift) % k] == periods]
        assert len(allowed) >= k - 2 * (s - leaves) + 1
        rng.shuffle(allowed)
        lists.append(allowed)
    labels.extend(verify_choice(k, shifts, lists))
    edges.extend((parent, h + i, offsets[i]) for i, parent in enumerate(parents))
    for bins in (counts(labels, k), counts((labels[i] + labels[j] + b for i, j, b in edges), k)):
        assert max(bins) - min(bins) <= 1


def main():
    rng = Random(1991)
    cases = 0
    for k in range(7, 75):
        for leaves in range(2, k):
            # Largest t at the sufficient threshold with the parity of k.
            t = leaves // 2
            t -= (k - t) % 2
            s = (k + t) // 2
            if s - leaves < 2:
                continue
            assert 2 * leaves - t + 1 >= (3 * leaves + 1) // 2 + 1
            for periods in range(3):
                check_tree(k, leaves, periods, s, rng)
                cases += 1
    print(f"{cases} whole-tree matching extensions checked through modulus 74")


if __name__ == "__main__":
    main()

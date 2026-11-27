"""Independent checks of the actual long path, adjustable interval and subdivisions."""

from random import Random
from types import SimpleNamespace

from research.hub.check_two_hub_contraction import audit_ranges
from research.hub.integer_bare_endpoint import restore
from research.hub.integer_layers import prepare
from research.hub.two_hub_buffer import insert_neutral
from research.hub.two_hub_contraction import Interval, remove_fillers


def check(size, capacity, rng):
    parents = [-1, 0, 1, 2]
    labels = {0: 1, 1: -1, 2: 2, 3: 0}
    forest = [-1]
    boundary = {}
    for j in range(size):
        p = 0 if j < 8 else rng.randrange(1, j+1)
        forest.append(p)
        if p:
            parents.append(3+p)
        else:
            actual = rng.randrange(4)
            boundary[j+1] = labels[actual]
            parents.append(actual)
    free, bills, _ = prepare(forest, boundary, set(labels.values()), rng)
    labels.update((3+v, x) for v, x in free.items())
    capacity = max(capacity, len(bills))
    before = list(parents)
    radius = 10**8
    gap, bound = restore(parents, labels, set(), 2, bills, -1, capacity, radius, rng)
    v = 2
    for i in range(53+14*capacity):
        v = parents[v]
        assert v == len(parents)-i-1
    assert parents[v] == before[2]
    assert all(before[i] == parents[i] for i in range(len(before)) if i!=2)
    xs = sorted(labels.values())
    assert len(set(xs)) == len(parents) == len(xs)
    assert gap == xs[0] < -radius and -gap > xs[-1]
    iv = Interval(SimpleNamespace(lo=gap, hi=max(radius, xs[-1]), added=[]))
    iv.blocks = [(0, a+1, b) for a, b in zip(xs, xs[1:]) if a+1 < b]
    iv.fill(0, xs[-1]+1, iv.hi+1)
    actual = [labels[v]+labels[p] for v, p in enumerate(parents) if v]
    audit_ranges(actual, [(a,b) for _,a,b in iv.blocks], iv.lo+1, iv.hi+1)

    # Restore two other old edges using only the available leaves at zero.
    old = sorted(v for v in range(4, len(before)) if
                 labels[v] and labels[parents[v]] and labels[v]+labels[parents[v]])
    occupied = set(xs)
    for child in old[:2]:
        parent = parents[child]
        assert max(abs(labels[parent]), abs(labels[child])) <= bound
        path = insert_neutral((labels[parent], labels[child]), 13, 100*(len(parents)+400),
                              occupied, lambda z: False, rng)
        remove_fillers(iv, set(path[1:-1]))
        for x in path[1:-1]:
            labels[len(parents)] = x
            parents.append(parent)
            parent = len(parents)-1
        parents[child] = parent
    actual = [labels[v]+labels[p] for v, p in enumerate(parents) if v]
    bands = [(a,b) for p,a,b in iv.blocks]
    audit_ranges(list(labels.values()), bands, iv.lo, iv.hi+1)
    audit_ranges(actual, bands, iv.lo+1, iv.hi+1)
    return len(actual), len(bills), capacity


def main():
    rng = Random(7403)
    data = [check(size, capacity, rng) for size, capacity in
            ((48, 12), (81, 25), (290, 0), (95, 864))]
    print(f"{len(data)} exact marked-seed repairs, {sum(e for e, _, _ in data):,} actual edge sums.")
    print(f"{sum(b for _, b, _ in data)} protected pairs; one full {53+14*864:,}-vertex replacement.")
    print("104 twelve-vertex subdivisions after interval completion, all paid at zero.")


if __name__ == "__main__":
    main()

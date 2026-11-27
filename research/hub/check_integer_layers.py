"""Check ordinary integer sums from the original forest and its actual boundary."""

from collections import Counter
from random import Random

from research.hub.integer_layers import centers, prepare
from research.rainbow.verify import rooted_shapes


def audit(tree, boundary, fixed, rng):
    labels, jobs, stats = prepare(tree, boundary, fixed, rng)
    h = len(tree)-1
    assert set(labels) == set(range(1, len(tree)))
    vertices = set(labels.values())
    assert len(vertices) == h and vertices.isdisjoint(fixed)
    occupied = vertices | set(fixed)
    actual = Counter(x+(labels[tree[v]] if tree[v] else boundary[v]) for v, x in labels.items())
    expected = Counter(labels.values())
    targets = set()
    assert len(jobs) <= 2*stats[-1] and stats[-1] <= 432
    for b, t in jobs:
        actual[b] += 1
        expected[t] += 1
        assert b in vertices and b+2*t and t and targets.isdisjoint((t, -t))
        targets.update((t, -t))
        assert all(t != 2*p and -b not in (p, 2*p, 3*p) for p in occupied)
    assert actual == expected and targets.isdisjoint(occupied)
    return stats, len(jobs)


def split_checks(rng):
    cases = 0
    seen = set()
    for n in range(2, 51):
        for family in range(5):
            jumps = {v: rng.randrange(-10000, 10001) for v in range(n)}
            degrees = {v: (1 if family == 0 else rng.randrange(1, 10)) for v in jumps}
            if family == 2:
                degrees[0] = sum(degrees.values())
            if family == 3:
                degrees = {v: 0 for v in jumps}
            if family == 4:
                jumps = {v: (7 if v%2 else -7) for v in jumps}
            fixed = set(jumps.values()) | set(range(-2*n, 3*n))
            groups = centers(jumps, degrees, fixed, fixed, rng)
            row = {v: x for part, _, _, _ in groups for v, x in part.items()}
            assert len(set(row.values())) == len(row) == n
            assert fixed.isdisjoint(row.values())
            forward = Counter(x+jumps[v] for v, x in row.items())
            expected = Counter(row.values())
            for _, _, _, pairs in groups:
                for b, t in pairs:
                    forward[b] += 1
                    expected[t] += 1
            assert forward == expected
            m = sum(degrees.values())
            total = sum(degrees[v]*x for v, x in row.items())
            assert abs(total) <= (m+1)*120*(len(fixed)+n+20)
            seen.add('terminal' if not m else 'heavy' if 3*max(degrees.values()) >= m else 'balanced')
            cases += 1
    assert seen == {'heavy', 'balanced', 'terminal'}
    return cases


def main():
    rng = Random(11406)
    shapes = cases = edges = 0
    splits = split_checks(Random(6071))
    for h in range(1, 13):
        for tree in rooted_shapes(h).values():
            boundary = {v: 0 for v in range(1, h) if tree[v] == 0}
            audit(tree, boundary, {0}, rng)
            shapes += 1
    seed_hits = [0, 0]
    max_jobs = 0
    for size in (24, 97, 515, 790):
        for length in (0, 1, size):
            tree = [-1]
            boundary = {}
            for p in (7, -10, 0, 5, -10, 1):
                v = 0
                for j in range(length+1):
                    tree.append(v)
                    v = len(tree)-1
                    if j == 0:
                        boundary[v] = p
                    if j % 13 == 2:
                        tree.extend([v]*3)
            for _ in range(size):
                tree.append(rng.randrange(1, len(tree)))
            fixed = set(range(-10, 13))
            stats, jobs = audit(tree, boundary, fixed, rng)
            seed_hits[0] += stats[0]
            seed_hits[1] += stats[1]
            max_jobs = max(max_jobs, jobs)
            edges += len(tree)-1
            cases += 1
    assert min(seed_hits) > 0 and max_jobs > 100
    print(f"{splits} two-group, heavy-child and terminal level checks.")
    print(f"{shapes:,} rooted shapes through order 12; {cases} forests, {edges:,} entering edges.")
    print(f"Repeated, signed and zero boundaries; {seed_hits[0]} seed transfers, "
          f"{seed_hits[1]} seed subdivisions, up to {max_jobs} guarded discrepancies.")


if __name__ == "__main__":
    main()

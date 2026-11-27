"""Replay the small certificates independently, then test assembled witnesses."""

from itertools import combinations_with_replacement, permutations, product
import json
from pathlib import Path

from . import four_leaves as build


def spider_edges(lengths):
    edges = []
    start = 1
    for length in lengths:
        edges.append((0, start))
        edges.extend((v, v + 1) for v in range(start, start + length - 1))
        start += length
    return edges


def double_edges(a, b, g, c, d):
    edges = spider_edges((a, b, g))
    center = a + b + g
    edges.extend((center + i, center + i + 1) for i in range(c))
    edges.append((center, center + c + 1))
    edges.extend((center + c + i, center + c + i + 1) for i in range(1, d))
    return edges


def verify_rank(edges, row):
    n = len(edges) + 1
    sides = [0] * n
    for u, v in edges:
        sides[v] = 1 - sides[u]
    assert len(row) == n
    for side in (0, 1):
        values = [x for x, c in zip(row, sides) if c == side]
        assert sorted(values) == list(range(len(values)))
    assert sorted(row[u] + row[v] for u, v in edges) == list(range(n - 1))


def verify_interval(edges, row):
    assert sorted(row) == list(range(len(edges) + 1))
    sums = sorted(row[u] + row[v] for u, v in edges)
    assert sums == list(range(sums[0], sums[0] + len(edges)))


def numbers(text):
    return tuple(map(int, text.split(",")))


def has_depth(n, i, depth):
    for even in permutations(range((n + 1) // 2)):
        for odd in permutations(range(n // 2)):
            row = [0] * n
            row[::2], row[1::2] = even, odd
            if row[i] == depth and len({x+y for x, y in zip(row, row[1:])}) == n-1:
                return True
    return False


def certificates():
    data = json.loads(Path(__file__).with_name("four-leaf-certificates.json").read_text())
    no_one = {(1, 1), (1, 4), (4, 4)}
    expected_one = {(a, b) for a in range(1, 9) for b in range(a, a + 8)} - no_one
    assert set(map(numbers, data["rank_one"])) == expected_one
    zeros = {(2,5), (3,5), (4,4), (4,9), (5,9), (6,6), (6,13), (7,13),
             (8,8), (9,17), (10,10), (12,12)}
    assert set(map(numbers, data["rank_zero"])) == zeros
    for group, depth in (("rank_zero", 0), ("rank_one", 1)):
        for case, row in data[group].items():
            a, b = numbers(case)
            verify_rank([(i, i+1) for i in range(a+b)], row)
            assert row[a] == depth
    for a, b in no_one:
        assert not has_depth(a + b + 1, a, 1)
    assert not has_depth(5, 2, 0)
    expected_kernels = {(2,2,1,5,1), (2,2,3,7,1), (2,2,5,9,1), (2,2,4,7,0),
                        (2,2,5,7,0), (1,1,1,3,1), (1,4,1,6,1), (4,4,1,9,1),
                        (2,2,2,5,11,2)}
    assert set(map(numbers, data["kernels"])) == expected_kernels
    for case, row in data["kernels"].items():
        *legs, pin, depth = numbers(case)
        verify_rank(spider_edges(legs), row)
        assert row[pin] == depth
    residuals = {(3,3), (3,4), (3,9), (4,4), (4,9), (5,5), (9,9)}
    doubles = {(a,b,g) for a,b in no_one for g in (1,4)} | {(a,b,3) for a,b in residuals}
    spiders = {(2,2,2,t) for t in (1,2,3,4,6,7,8,9,14)} | {(2,2,2)}
    for case, row in data["intervals"].items():
        kind, shape = case.split(":")
        args = numbers(shape)
        if kind == "s":
            spiders.remove(args)
            edges = spider_edges(args)
        else:
            assert kind == "d"
            doubles.remove(args)
            c, d, g = args
            edges = double_edges(2, 2, g, c, d)
        verify_interval(edges, row)
    assert not spiders and not doubles
    print("105 finite witnesses, all required keys, and four excluded marked ranks checked")


def constructions():
    count = 0
    for n in range(1, 161):
        edges = [(i, i+1) for i in range(n-1)]
        for depth in range((n+1)//2):
            if n == 4*depth+1 and depth:
                continue
            row = build.endpoint(n, depth)
            verify_rank(edges, row)
            assert row[0] == (n-1)//2-row[-1] == depth
            count += 1
    print(f"{count} endpoint constructions checked")
    count = 0
    for a in range(1, 46):
        for b in range(a, 90):
            edges = [(i, i+1) for i in range(a+b)]
            for h in range(7):
                if h == 0 and (a,b) == (2,2) or h == 1 and (a,b) in {(1,1),(1,4),(4,4)}:
                    continue
                if h >= 2 and a < 4*h+5 and b < a+4*h+4:
                    continue
                row = build.marked(a, b, h)
                verify_rank(edges, row)
                assert row[a] == h
                count += 1
    print(f"{count} internally marked paths checked")
    count = 0
    for length in (3,4):
        shapes = list(product(range(1,7), repeat=length))
        shapes += [(2,2,2,t) for t in range(7,41)] if length == 4 else [(17,18,21)]
        for shape in shapes:
            _, row = build.spider(shape)
            verify_interval(spider_edges(shape), row)
            count += 1
    arms = list(combinations_with_replacement(range(1,8),2)) + [(4,9),(9,9),(8,17),(19,32)]
    for (a,b),(c,d) in product(arms, repeat=2):
        for g in (1,2,3,4,5,6,7,8,9,17):
            _, row = build.double_fork(a,b,g,c,d)
            verify_interval(double_edges(a,b,g,c,d), row)
            count += 1
    for args in ((2,2,3,27,2),(17,3,1,2,2),(2,17,29,18,1),(2,2,503,202,202)):
        _, row = build.double_fork(*args)
        verify_interval(double_edges(*args), row)
        count += 1
    print(f"{count} assembled trees checked using independent edge lists")


if __name__ == "__main__":
    certificates()
    constructions()

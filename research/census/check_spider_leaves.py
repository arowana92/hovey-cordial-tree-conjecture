"""Check interval labels on independently reconstructed spiders and connectors."""

from itertools import combinations_with_replacement, product

from .check_four_leaves import double_edges, spider_edges, verify_interval, verify_rank
from .spider_leaves import CENTER_ZERO, UPPER, decorated_connector, spider


def check_spider(arms, leaves):
    _, row = spider(arms, leaves)
    edges = spider_edges(arms)
    start = len(edges) + 1
    edges += [(0, v) for v in range(start, start+leaves)]
    if edges:
        verify_interval(edges, row)
    else:
        assert row == [0]


def main():
    for t, row in CENTER_ZERO.items():
        verify_rank(spider_edges((2,2,t)), row)
        assert row[0] == 0
    assert set(CENTER_ZERO) == set(range(7,12))
    for t, row in UPPER.items():
        edges = spider_edges((2,2,2,t))
        verify_interval(edges, row)
        assert min(row[u]+row[v] for u,v in edges) == row[0]+1
    assert set(UPPER) == {2,3,4,6}
    count = 0
    for length in range(5):
        for arms in combinations_with_replacement(range(2,11), length):
            for leaves in (0,1,2,9,80):
                check_spider(arms, leaves)
                count += 1
    for t in range(2,65):
        check_spider((2,t,2,2), 37)
        count += 1
    check_spider((2,2,2,1003), 1100)
    count += 1
    count_spine = 0
    for a,b,c,d in product(range(1,6),repeat=4):
        if (a,b) == (2,2) or (c,d) == (2,2):
            continue
        for counts in ((0,0), (9,7), (1,3,0,5,8), (15,0,1,2,17,0,35,1,7,3)):
            g = len(counts)-1
            edges = double_edges(a,b,g,c,d)
            start = len(edges)+1
            for u,m in zip([0]+list(range(a+b+1,a+b+g+1)), counts):
                edges.extend((u,i) for i in range(start,start+m))
                start += m
            _, row = decorated_connector(a,b,c,d,counts)
            verify_interval(edges, row)
            count_spine += 1
    print(f"Nine extra certificate rows, {count} spiders and {count_spine} decorated connectors checked")


if __name__ == "__main__":
    main()

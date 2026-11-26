"""Audit the four-site completion at a fixed nonzero boundary, including short order."""

from collections import Counter
from itertools import combinations_with_replacement
from random import Random

from research.check_large_order_subdivision import children
from research.hub.check_odd_branch_groups import append_branch
from research.hub.modular_injection import finish
from research.hub.odd_branch_groups import construct
from research.hub.polynomial_hub import bottom_fringe
from research.rainbow.verify import rooted_shapes


def audit(tree,values,gap,k):
    assert len(values) == len(set(values)) == len(tree)
    weights = Counter((values[v]+values[p]) % k for v,p in enumerate(tree) if v)
    assert weights+Counter([gap]) == Counter(values)
    assert 0 in weights and gap != 0


def main():
    rng = Random(91027)
    shapes = [row for n in range(2,7) for row in rooted_shapes(n).values()]
    cases = Counter()
    cycles = repeated = 0
    for left,right in combinations_with_replacement(shapes,2):
        for order in (3,5,8):
            q = 100003
            k = q*order
            tree = [-1,0]
            append_branch(tree,1,left)
            append_branch(tree,1,right)
            append_branch(tree,0,[-1,0,0,1])
            tree.extend([1]*rng.randrange(order+2))
            kids = children(tree)
            fringe = bottom_fringe(tree,kids,1,height=0)
            values,gap,_,_ = finish(tree,kids,{0:0,1:q},fringe,k,rng)
            audit(tree,values,gap,k)
            kind,boundary,nodes,_,_,other = fringe
            if boundary == 1 and kind == 'arms':
                weak = sum(tree[v] == nodes[2] for v in other)
                cycles += weak//order
            cases[(kind,boundary == 1)] += 1

    for d in (3,5,9):
        q = 200003
        tree = [-1,0]
        for _ in range(4*d):
            append_branch(tree,1,[-1]+[0]*(2*d+3))
        for m in (0,1,d-1,d,3*d+2):
            values,gap,(_,groups,_) = construct(tree,d,q,m)
            audit(tree+[1]*m,values,gap,d*q)
            assert values[:2] == [0,q] and groups > 0
            repeated += 1
    assert cycles and all(cases[(kind,True)] for kind in ('arms','path-b','path-c'))
    assert any(n for (_,fixed),n in cases.items() if not fixed)
    print(f"{sum(cases.values()):,} four-site completions with actual edge counts, "
          f"{sum(n for (_,fixed),n in cases.items() if fixed):,} at a fixed boundary.")
    print(f"{cycles} complete cycles at a constant leaf parent; {repeated} whole trees "
          "with many short branches and a protected pair.")


if __name__ == '__main__':
    main()

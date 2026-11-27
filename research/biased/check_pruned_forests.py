"""Certify a ten-row extension after choosing which two vertices to restore."""

from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from math import gcd

from research.eight.generate import forests
from research.rainbow.generate import tree_size
from research.rainbow.verify import rooted_shapes
from .pruned_forests import choose_fringe
from .check_nine_row_lists import catalog, table


def large_factors(n):
    for p in (2,3,5,7,11,13,17,19,23):
        while n and n % p == 0:
            n //= p
    return abs(n)


def restore(forest):
    """Return one component root to the connected core."""
    for i, tree in enumerate(forest):
        if i and tree == forest[i-1]:
            continue
        yield tuple(sorted(forest[:i] + tree + forest[i+1:]))


def prune(previous, size):
    current = {}
    for forest in forests(size):
        value = 0
        for smaller in restore(forest):
            value = gcd(value, previous[smaller])
            if value == 1:
                break
        current[forest] = value
    return current


def check_cuts():
    checked = 0
    for n in range(4,12):
        for parents in rooted_shapes(n).values():
            adjacency = [set() for _ in parents]
            for v,p in enumerate(parents[1:],1):
                adjacency[v].add(p)
                adjacency[p].add(v)
            for q in range(2,n-1):
                for target in range(1,q//2+1):
                    cut = choose_fringe(parents,q,target)
                    assert len(cut) == q
                    for group in (cut,set(range(n))-cut):
                        remaining = group.copy()
                        parts = []
                        while remaining:
                            active = [remaining.pop()]
                            count = 0
                            while active:
                                v = active.pop()
                                count += 1
                                more = remaining & adjacency[v]
                                remaining -= more
                                active.extend(more)
                            parts.append(count)
                        if group is cut:
                            assert len(parts) >= 3 or sorted(parts) == [target,q-target]
                        else:
                            assert parts == [n-q]
                    checked += 1
    print(f"{checked} connected cuts independently checked",flush=True)


def verify_pruning(previous, prime=None):
    expected = {17:3,19:3,23:1}

    for size in (11,12):
        previous = prune(previous, size)
        assert len(previous) == {11:4766,12:12486}[size]
        bad = [f for f,d in previous.items() if d != 1 and len(f) >= 2]
        print(f"{prime or 'rational'}, {size} vertices: {len(bad)} forests with two or more components survive", flush=True)
        if size == 11 and prime is None:
            assert len(bad) == 26
    sizes = Counter(tuple(sorted(map(tree_size,f))) for f in bad)
    assert sizes == ({(1,11):15, (6,6):1} if prime is None else {(1,11):expected[prime]})
    # Move one boundary of the core toward the larger component, returning
    # its root and taking in the smaller component's adjacent core vertex.
    for forest in bad:
        a,b = sorted(forest,key=tree_size)
        exchanged = tuple(sorted(((a,),) + b))
        assert previous[exchanged] == 1
    print(f"All {len(bad)} boundary exchanges give a certified ten-vertex forest.", flush=True)


def main(independent=True, field=None):
    check_cuts()
    cases, grown = catalog(10)
    assert len(cases) == 1842
    if field in (None,"rational"):
        values = table(cases, grown, Fraction(-11,2), None, independent)
        assert all(values)
        verify_pruning({forest:large_factors(x.numerator) for (forest,_,_),x in zip(cases,values)})
    if field == "rational":
        return
    for p in ((17,19,23) if field is None else (int(field),)):
        values = table(cases, grown, (p-11)//2, p, independent)
        verify_pruning({forest:int(x != 0) for (forest,_,_),x in zip(cases,values)},p)



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--single-expansion", action="store_true",
                        help="skip the independent forward coefficient expansion")
    parser.add_argument("--field",choices=("rational","17","19","23"),help="replay one coefficient table")
    args = parser.parse_args()
    main(not args.single_expansion,args.field)

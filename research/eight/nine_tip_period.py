"""Verify all twenty-four-vertex cuts left by the nine-tip parity obstruction."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path

from .generate import forests, parent_vector
from .period_blocks import flags, safe_block


@lru_cache(None)
def full_binary(size):
    if size == 1:
        return ((),)
    return tuple((a,b) for left in range(1,size-1,2)
                 for a in full_binary(left) for b in full_binary(size-1-left) if a <= b)


def binary_pairs():
    return {tuple(sorted((a,b))) for size in range(1,16,2)
            for a in full_binary(size) for b in full_binary(16-size)}


def by_new_parents(pairs):
    shapes = set(pairs)
    for _ in range(8):
        following = set()
        for roots in shapes:
            for n in range(1,len(roots)+1):
                for chosen in combinations(range(len(roots)),n):
                    children = tuple(roots[i] for i in chosen)
                    others = [tree for i,tree in enumerate(roots) if i not in chosen]
                    following.add(tuple(sorted(others+[children])))
        shapes = following
    return shapes


def uncolored(parents):
    children = [[] for _ in parents]
    roots = []
    for i in reversed(range(len(parents))):
        (roots if parents[i]<0 else children[parents[i]]).append(tuple(sorted(children[i])))
    return tuple(sorted(roots))


def by_grafting(pairs):
    shapes = set()
    for prefix in forests(8):
        p = parent_vector(prefix,range(len(prefix)))
        tips = set(range(8))-set(p)
        if len(tips)>2:
            continue
        for a,b in product(range(-1,8), repeat=2):
            if not tips <= {a,b}:
                continue
            for pair in pairs:
                parents = p.copy()
                for root,site in zip(pair,(a,b)):
                    base = len(parents)
                    for ancestor in parent_vector((root,),(0,)):
                        parents.append(site if ancestor<0 else base+ancestor)
                shapes.add(uncolored(parents))
    return shapes


def find_cut(parents, bad, common):
    vertices = set(range(24))
    children = Counter(parents)

    def visit(i, prefix):
        if len(prefix) == 8:
            if not safe_block(parents,prefix,bad,common):
                return None
            rest = vertices.difference(prefix)
            sites = [parents[v] for v in rest if parents[v] not in rest]
            if len(sites)==2 and sites[0]!=sites[1] and all(children[v] in (0,2) for v in rest):
                return None
            return prefix
        if 24-i < 8-len(prefix):
            return None
        if parents[i]<0 or parents[i] in prefix:
            found = visit(i+1,prefix+(i,))
            if found is not None:
                return found
        return visit(i+1,prefix)
    return visit(0,())


def check():
    catalog = Path(__file__).with_name('period-pins.jsonl.gz')
    _, bad, common = flags(catalog)
    pairs = binary_pairs()
    candidates = by_new_parents(pairs)
    assert candidates == by_grafting(pairs)
    by_components = Counter()
    for shape in candidates:
        p = parent_vector(shape,range(len(shape)))
        assert len(p) == 24 and len(set(range(24))-set(p)) == 9
        first = find_cut(p,bad,common)
        assert first is not None and len(first)==len(set(first))==8
        assert all(p[i]<0 or p[i] in first for i in first)
        assert safe_block(p,first,bad,common)
        rest = [i for i in range(24) if i not in first]
        indices = {v:i for i,v in enumerate(rest)}
        remaining = uncolored([indices.get(p[v],-1) for v in rest])
        if remaining in pairs:
            assert len({p[v] for v in rest if p[v] not in indices}) == 1
        by_components[len(shape)] += 1
    print('full binary pairs',len(pairs),'reconstructed forests',len(candidates),
          'verified cuts by component count',sorted(by_components.items()))


if __name__ == '__main__':
    check()

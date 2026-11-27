"""Generate cycles of matched pairs with further pairs attached at arbitrary vertices."""

from argparse import ArgumentParser
from functools import lru_cache
from itertools import product
from pathlib import Path


def canonical(sites):
    return min(seq[i:]+seq[:i] for seq in (sites,sites[::-1]) for i in range(len(seq)))


@lru_cache(None)
def children(root):
    depth = start = 0
    forest = []
    for i,c in enumerate(root[1:-1]):
        depth += 1 if c == '(' else -1
        if depth == 0:
            forest.append(root[start+1:i+2])
            start = i+1
    return tuple(forest)


def node(forest):
    return '(' + ''.join(sorted(forest)) + ')'


@lru_cache(None)
def extend(root):
    forest = children(root)
    result = {node(forest+('(())',))}
    for i,subtree in enumerate(forest):
        for larger in extend(subtree):
            result.add(node(forest[:i]+(larger,)+forest[i+1:]))
    return result


def necklaces(pairs,extra):
    rings = set()
    for traversed in product((False,True),repeat=pairs-extra):
        sites = tuple(site for t in traversed for site in (('()','()') if t else ('(())',)))
        rings.add(canonical(sites))
    for _ in range(extra):
        rings = {canonical(r[:i]+(larger,)+r[i+1:]) for r in rings
                 for i,site in enumerate(r) for larger in extend(site)}
    return rings


if __name__ == '__main__':
    options = ArgumentParser()
    options.add_argument('pairs',type=int)
    options.add_argument('extra',type=int)
    options.add_argument('output',type=Path)
    args = options.parse_args()
    rings = necklaces(args.pairs,args.extra)
    args.output.write_text(''.join('.'.join(r)+'\n' for r in sorted(rings)))
    print(f'{len(rings)} unicyclic graphs with {args.extra} off-path pairs')

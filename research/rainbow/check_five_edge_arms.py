"""Enumerate the independent six-tip tests needed when every terminal arm has length five or more."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from random import Random
import re
import sys

from research.census.leaf_profile_geometry import suffix_shapes
from research.eight.verify import components
from research.rainbow.check_prescribed_forest_order import catalog
from research.rainbow.verify import rooted_shapes
from research.rainbow.check_terminal_arm_order import arm_tree, preorder
from research.rainbow.check_two_rooted_trees import replay
from research.rainbow.prescribed_forest_order import extend
from research.rainbow.two_rooted_trees import padded_search


def reduced_profiles():
    profiles = set()
    for parts in suffix_shapes(10, 6):
        if sum(h for s,h in parts) != 6:
            continue
        for chosen in product(*(range(h+1) for s,h in parts)):
            if sum(chosen) == 4:
                profiles.add(tuple(sorted((s+4*c,h) for (s,h),c in zip(parts,chosen))))
    return profiles


def enlarged_forests():
    # Independently add four vertices at each of four distinct tips of a
    # ten-vertex forest. A dummy root enumerates forests through rooted trees.
    forests = {}
    for tree in rooted_shapes(11).values():
        parents = [p-1 for p in tree[1:]]
        tips = sorted(set(range(10))-set(parents))
        if len(tips) != 6:
            continue
        for chosen in combinations(tips,4):
            expanded = parents.copy()
            for v in chosen:
                for _ in range(4):
                    expanded.append(v)
                    v = len(expanded)-1
            key = tuple(sorted(code for _,code in components(expanded)))
            forests[key] = tuple(sorted((len(code)//2,code.count('()')) for code in key))
    return forests


def check(path):
    profiles = reduced_profiles()
    forests = enlarged_forests()
    assert profiles == set(forests.values())
    remaining = {p:n for p,n in catalog(6).items() if p in profiles}
    totals = Counter()
    row_totals = Counter()
    literal = Counter()
    cases = Counter(len(p) for p in forests.values() if p in remaining)
    print('candidate forests', len(forests), 'by component count',
          sorted(Counter(len(p) for p in forests.values()).items()))
    print('supplementary candidate forests', sorted(cases.items()))
    for line in path.read_text().splitlines():
        match = re.fullmatch(r'[0-9a-f]{64}  forests=(\d+) rows=(\d+) assignments=(\d+)  (.+)',line)
        assert match
        n,rows,assignments = map(int,match.groups()[:3])
        parts = tuple(tuple(map(int,x.split(','))) for x in match[4].split())
        r = len(parts)
        assert remaining.pop(parts) == n and n <= rows <= assignments == n*27**r
        totals[r] += n
        row_totals[r] += rows
        literal[r] += assignments
    assert not remaining
    for r in sorted(totals):
        print('components, certified forests, rows, literal inputs', r,totals[r],row_totals[r],literal[r])


def growth(library):
    rng = Random(270505)
    solve = padded_search(library,27)
    base = [-1,0,0,0,3,3,0,0]
    example = arm_tree(base,[28,5,5,5,5,12])
    cases = [(example,0,None)]
    for _ in range(40):
        base = [-1]+[rng.randrange(i) for i in range(1,rng.randrange(12,40))]
        leaves = sum(base.count(v)+int(v!=0)==1 for v in range(len(base)))
        tree = arm_tree(base,[rng.randint(5,9) for _ in range(leaves)])
        cases.append((tree,rng.randrange(len(tree)),rng))
    prefixes = six = 0
    for tree,root,shuffle in cases:
        parents = preorder(tree,root,shuffle)
        order = list(range(1,len(parents)))
        for start in range(1,len(parents),27):
            group = set(order[start-1:start+25])
            tips = len(group-set(parents[v] for v in group))
            assert tips <= 6
            if tips == 6 and sum(parents[v] not in group for v in group) == 5:
                six += 1
        labels = extend(parents,[0],order,27,solve)
        prefixes += replay(parents,[0],labels,order,{})
    assert six
    print('DFS orders',len(cases),'cordial growth steps',prefixes,'five-component fork batches',six)


if __name__ == '__main__':
    check(Path(sys.argv[1]))
    if len(sys.argv) == 3:
        growth(sys.argv[2])

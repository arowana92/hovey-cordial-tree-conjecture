"""Check the seventh-tip certificate manifests by exact rooted-tree counts."""
from argparse import ArgumentParser
from gzip import open as open_gz
from pathlib import Path
import re

from research.rainbow.seven_tip_profiles import count, single_trees
from research.rainbow.spine_counts import rooted
from research.census.leaf_profile_geometry import suffix_shapes
from research.census.check_leaf_profile_manifests import read_rows


def verify(path):
    expected = set(single_trees(26,7))
    seen = set()
    totals = [0,0,0]
    with open_gz(path,"rt") as file:
        for line in file:
            match = re.fullmatch(r"[0-9a-f]{64}  forests=(\d+) rows=(\d+) assignments=(\d+)  stem=(\d+) (.+)\n",line)
            assert match
            shapes,rows,inputs,stem = map(int,match.groups()[:4])
            parts = tuple(tuple(map(int,t.split(","))) for t in match[5].split())
            key = (stem,parts)
            assert key not in seen and key in expected
            seen.add(key)
            assert shapes==count(parts) and inputs==27*shapes and shapes<=rows<=inputs
            for i,n in enumerate((shapes,rows,inputs)):
                totals[i]+=n
    assert seen == expected and totals[0] == rooted(26)[7]
    print(f"profiles={len(seen)} forests={totals[0]} rows={totals[1]} assignments={totals[2]}")
    return totals


def check_multiple(paths, singles):
    expected = {parts for parts in suffix_shapes(26,7) if len(parts)>1 and sum(h for _,h in parts)==7}
    seen = {}
    for path in paths:
        records = read_rows(path,26)
        for parts,values in records.items():
            if len(parts)>1 and sum(h for _,h in parts)==7:
                assert parts not in seen
                seen[parts] = values
    assert set(seen)==expected, f"missing {len(expected-seen.keys())} profiles"
    totals = tuple(map(sum,zip(*seen.values())))
    assert totals[0]+singles[0]==rooted(27)[7]
    combined = [a+b for a,b in zip(singles,totals)]
    print(f"multiple profiles={len(seen)} forests={totals[0]} rows={totals[1]} assignments={totals[2]}")
    print(f"seven-tip forests={combined[0]} rows={combined[1]} assignments={combined[2]}")


if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("manifest",type=Path)
    parser.add_argument("--multiple", nargs="+", type=Path)
    args=parser.parse_args()
    single_totals=verify(args.manifest)
    if args.multiple:
        check_multiple(args.multiple,single_totals)

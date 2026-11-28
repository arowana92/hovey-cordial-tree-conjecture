"""Check the seventh-tip certificate manifests by exact rooted-tree counts."""
from argparse import ArgumentParser
from gzip import open as open_gz
from pathlib import Path
import re

from research.rainbow.seven_tip_profiles import count, single_trees
from research.rainbow.spine_counts import rooted


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


if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("manifest",type=Path)
    verify(parser.parse_args().manifest)

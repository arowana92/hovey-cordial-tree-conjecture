"""Cross-check forest totals and sharp boundary counts in the 27-label manifests."""
import argparse
from collections import Counter
from math import comb, prod
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory

from research.census.leaf_profile_geometry import check_geometry
from research.rainbow.spine_counts import boundaries, rooted


def read_rows(path, mass):
    rows = {}
    for line in path.read_text().splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  forests=(\d+) rows=(\d+) assignments=(\d+)  (.+)", line)
        assert match, f"invalid manifest row in {path}"
        digest, forests, witnesses, inputs, parts = match.groups()
        shape = tuple(tuple(map(int, x.split(","))) for x in parts.split())
        assert shape == tuple(sorted(shape)) and shape not in rows
        sizes = tuple(s for s, h in shape)
        assert sum(sizes) == mass and 6 < sum(h for s, h in shape) <= 16
        count = prod(comb(rooted(s)[h] + c - 1, c) for (s, h), c in Counter(shape).items())
        assert int(forests) == count > 0 and int(inputs) == count * boundaries(sizes, 27)
        assert count <= int(witnesses) <= int(inputs)
        rows[shape] = (count, int(witnesses), int(inputs))
    assert rows
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("order", type=int, choices=range(50, 55))
    parser.add_argument("leaves", type=int, choices=(12, 13))
    parser.add_argument("geometry", type=Path)
    parser.add_argument("manifests", nargs="+", type=Path)
    args = parser.parse_args()
    rows = {}
    for path in args.manifests:
        more = read_rows(path, args.order - 28)
        assert not rows.keys() & more.keys()
        rows.update(more)
    with TemporaryDirectory() as temp:
        listing = Path(temp, "profiles")
        listing.write_text("".join(" ".join(f"{s},{h}" for s, h in key) + "\n" for key in rows))
        subprocess.run([args.geometry.resolve(), str(args.order), str(args.leaves), listing], check=True)
    cases = subprocess.check_output([args.geometry.resolve(), str(args.order), str(args.leaves),
                                     "--candidates"], text=True)
    native = {tuple(sorted(tuple(map(int, p.split(","))) for p in line.split())) for line in cases.splitlines()}
    assert check_geometry(args.order, args.leaves, rows) == native
    forests, witnesses, inputs = map(sum, zip(*rows.values()))
    print(f"profiles={len(rows)} forests={forests} rows={witnesses} assignments={inputs}")


if __name__ == "__main__":
    main()

"""Compare tip-limited streams with full small catalogs and an independent partition count."""

import argparse
from pathlib import Path
import struct
import subprocess
from tempfile import TemporaryDirectory

from .check_spine_samples import parse
from .spine_counts import boundaries, forest_leaves, partitions


def totals(k, limit):
    shapes = colorings = 0
    for sizes in partitions(k-1):
        if len(sizes) <= limit:
            n = sum(count for tips, count in forest_leaves(sizes).items() if tips <= limit)
            shapes += n
            colorings += n * boundaries(sizes, k)
    return shapes, colorings


def records(path):
    raw = path.read_bytes()
    assert raw[:4] == b'SPN2'
    k = raw[4]
    rows = {}
    at = 5
    while at < len(raw):
        word, count = struct.unpack_from('<QI', raw, at)
        end = at+12+count*(k-1)
        assert count and end <= len(raw) and word not in rows
        parents, _, _, _ = parse(k, word)
        tips = k-1-len(set(parents)-{-1})
        rows[word] = (tips, raw[at:end])
        at = end
    return rows


def replay(generate, verify):
    with TemporaryDirectory() as tmp:
        folder = Path(tmp)
        catalog, subset, damaged = (folder/name for name in ('all', 'subset', 'damaged'))
        for k in range(5, 12):
            subprocess.run([generate,str(k),'0','1',catalog,'--ranked-cover'],
                           check=True,stdout=subprocess.DEVNULL)
            full = records(catalog)
            for limit in range(1, 2*(k-2)//3+1):
                subprocess.run([generate,str(k),'0','1',subset,'--tips',str(limit)],
                               check=True,stdout=subprocess.DEVNULL)
                rows = records(subset)
                assert rows == {w: v for w,v in full.items() if v[0] <= limit}
                shapes, colorings = totals(k, limit)
                cmd = [verify,str(k),'--tips',str(limit)]
                report = subprocess.check_output(cmd+[subset],text=True)
                assert f"forests={shapes} " in report and f"boundary assignments={colorings}\n" in report
                if k == 9 and limit == 2:
                    data = subset.read_bytes()
                    first = next(iter(rows.values()))[1]
                    bad = [data[:5]+data[5+len(first):], data+first,
                           data+next(v[1] for v in full.values() if v[0] > limit)]
                    for content in bad:
                        damaged.write_bytes(content)
                        result = subprocess.run(cmd+[damaged],capture_output=True)
                        assert result.returncode != 0
        print("Tip-limited records match every selected full-catalog record at orders 5 through 11.")
        print("The verifier rejected an omitted, repeated, and out-of-family record.")


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--binaries', nargs=2, type=Path, metavar=('GENERATOR','VERIFIER'))
    cli.add_argument('--tips', type=int, default=4)
    options = cli.parse_args()
    if options.binaries:
        replay(*(path.resolve() for path in options.binaries))
    for modulus in range(26, 31):
        shapes, colorings = totals(modulus, options.tips)
        print(f"k={modulus} tip limit={options.tips} forests={shapes} boundary assignments={colorings}")

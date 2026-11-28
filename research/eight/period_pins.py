"""Classify uniform eight-vertex attachments and all allowed labels at one new vertex."""
import argparse
from collections import Counter
import gzip
from itertools import groupby
import json
from math import gcd
from pathlib import Path

from .generate import boundary_labels, forests, parent_vector
from .surplus import assignment_filter


def color_orbit(forest, colors):
    groups = [tuple(c for _,c in group) for _,group in groupby(zip(forest,colors),key=lambda p:p[0])]
    return {tuple(x for group in groups for x in sorted((u*y+d) % 8 for y in group))
            for u in (1,3,5,7) for d in range(8)}


class Period:
    def __init__(self):
        self.rows, self.valid = assignment_filter(8,8,range(8))
        digits = [[bytearray(len(self.rows)//8) for _ in range(8)] for _ in range(8)]
        for i,row in enumerate(self.rows):
            for v,x in enumerate(row):
                digits[v][x][i//8] |= 1 << (i%8)
        self.digits = [[int.from_bytes(b,'little') for b in part] for part in digits]

    def masks(self, good):
        return [sum(1 << x for x in range(8) if good & positions[x]) for positions in self.digits]


def classify(output):
    period = Period()
    counts, common, extra = Counter(), Counter(), Counter()
    records = 0
    for forest in forests(8):
        consumed = set()
        for colors in boundary_labels(forest,8):
            if colors in consumed:
                continue
            orbit = color_orbit(forest,colors)
            assert not consumed.intersection(orbit)
            consumed.update(orbit)
            parents = parent_vector(forest,colors)
            good = period.valid(parents)
            divisor = gcd(8,*(parents.count(i) for i in range(8)))
            moment = sum(colors) % divisor == 0
            assert not good or moment
            kind = 'feasible' if good else 'extra' if moment else 'moment'
            counts[kind] += len(orbit)
            if kind == 'extra':
                extra[len(forest)] += 1
            if not any(colors):
                common[kind] += 1
            record = [parents,bin(good).count('1'),period.masks(good)]
            output.write((json.dumps(record,separators=(',',':'))+'\n').encode())
            records += 1
    print('affine representatives',records,'colored forests',dict(counts))
    print('common-parent rooted forests',dict(common),'extra orbits by component count',dict(extra))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--catalog',type=Path)
    group.add_argument('--parents',nargs=8,type=int,metavar='P')
    parser.add_argument('--pin',nargs=2,type=int,metavar=('VERTEX','RESIDUE'))
    args = parser.parse_args()
    if args.catalog:
        if args.pin:
            parser.error('--pin requires --parents')
        with args.catalog.open('wb') as raw, gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as out:
            classify(out)
        return
    if any(not -8 <= p < i for i,p in enumerate(args.parents)):
        parser.error('each parent must be an earlier index or -1 minus an old label')
    period = Period()
    good = period.valid(args.parents)
    if args.pin:
        v,x = args.pin
        if not (0 <= v < 8 and 0 <= x < 8):
            parser.error('the pin index and residue must be between zero and seven')
        good &= period.digits[v][x]
    if good:
        print('witness',*period.rows[(good & -good).bit_length()-1])
    else:
        print('no uniform extension')


if __name__ == '__main__':
    main()

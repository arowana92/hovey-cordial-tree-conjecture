"""Count the typed single-branch certificate and check the interval tests."""
from argparse import ArgumentParser
from math import gcd
from functools import lru_cache
from pathlib import Path
import re

from .spine_counts import rooted


def check_manifest(path):
    counts = rooted(22)
    totals = [0,0,0]
    seen = set()
    for line in path.read_text().splitlines():
        match = re.fullmatch(r"[a-f0-9]{64}  forests=(\d+) rows=(\d+) assignments=(\d+)  22,(\d+)",line)
        assert match
        shapes, rows, inputs, tips = map(int,match.groups())
        assert 8 <= tips <= 21 and tips not in seen
        seen.add(tips)
        assert shapes == counts[tips] and shapes <= rows <= inputs == 27*shapes
        for i,value in enumerate((shapes,rows,inputs)):
            totals[i] += value
    assert seen == set(counts)-set(range(1,8))
    print('certified at eight or more tips',*totals,'all rooted shapes',sum(counts.values()))


def largest_gap(values, k):
    points = sorted(values)
    return max(b-a for a,b in zip(points,points[1:]+[points[0]+k]))


def interval_checks(k):
    palette = set(range(k))
    units = [u for u in palette if gcd(u,k)==1]
    orbits = [{u*b % k for u in units} for b in range(1,k) if k%b==0]
    limits = []
    for orbit in orbits:
        single = common = 0
        for m in range(1,k):
            V = set(range(m))
            hv = palette-V
            # Normalize W-r to an interval starting at a variable origin c.
            # Enumerate every pair of missing vertex and edge labels literally.
            hw = palette-set(range(m-1))
            origins = {(b+z-w)%k for b in orbit for z in hv for w in hw}
            works = origins == palette
            assert works == (2*(k-m) >= largest_gap(orbit,k))
            if works:
                single = m
            absent = palette-set(range(m+1))
            works = all(any((r-b)%k in absent for b in orbit) for r in range(m+1))
            assert works == (m < k-largest_gap(orbit|{0},k))
            if works:
                common = m
        limits.append((min(orbit),single,common))
    return limits


def sharp_common_bound(limit):
    @lru_cache(None)
    def unit_gap(t):
        return largest_gap({0}|{x for x in range(1,t) if gcd(x,t)==1}, t)
    for k in range(2,limit+1):
        divisors = [t for t in range(2,k+1) if k%t==0]
        actual = max(k//t*unit_gap(t) for t in divisors)
        expected = 2*k//3 if k%6==0 else k//divisors[0]
        assert actual==expected
        # At the claimed threshold exhibit a failing marked interval, realized
        # by the ordinary star labeling with center 0 and leaf labels 1..m.
        m=k-actual
        order=6 if k%6==0 else divisors[0]
        mark=k//6 if order==6 else 0
        shifts=[k//order*u for u in range(1,order) if gcd(u,order)==1]
        assert all((mark-b)%k<=m for b in shifts)
    print('sharp common-parent width through modulus',limit)


if __name__ == '__main__':
    cli = ArgumentParser(description=__doc__)
    cli.add_argument('--manifest',type=Path)
    cli.add_argument('--intervals',action='store_true')
    args = cli.parse_args()
    if args.manifest:
        check_manifest(args.manifest)
    if args.intervals:
        sharp_common_bound(1024)
        for k in range(2,42):
            table = interval_checks(k)
            if k==27:
                assert table == [(1,26,24),(3,24,20),(9,18,17)]
                print('27-label orbit representative, branch limit, common-parent forest limit',table)

"""Replay small short-forest proofs by leaf insertion and direct endpoint sums."""

import argparse
from math import gcd
from pathlib import Path
from struct import unpack_from
import subprocess
from tempfile import TemporaryDirectory

from research.eight.verify import components
from .check_spine_samples import parse
from .check_tip_forests import totals
from .verify import rooted_shapes


def colorings(k, sizes):
    def extend(colors, mass, runs):
        i = len(colors)
        if i == len(sizes):
            yield colors
            return
        for c in range(k):
            change = not colors or colors[-1] != c
            if change and sizes[i] < mass+runs:
                continue
            yield from extend(colors+(c,),mass+sizes[i],runs+int(change))
    return extend((),0,0)


def direct(path,k,mass,limit):
    raw = path.read_bytes()
    assert raw[:6] == b'SPN3'+bytes((k,mass))
    expected = {word for word,p in rooted_shapes(mass+1).items()
                if mass+1-len(set(p)-{-1}) <= limit}
    seen = set()
    offset = 6
    inputs = 0
    units = [u for u in range(1,k) if gcd(u,k)==1]
    while offset < len(raw):
        word,count = unpack_from('<QI',raw,offset)
        parents,roots,sizes,_ = parse(k,word,mass)
        key = components([-1]+[p+1 for p in parents])[0][1]
        assert key in expected and key not in seen
        seen.add(key)
        offset += 12
        images = []
        for _ in range(count):
            row = raw[offset:offset+mass]
            offset += mass
            assert len(row)==len(set(row))==mass and all(0<x<k for x in row)
            images.extend(tuple(u*x%k for x in row) for u in units)
        for colors in colorings(k,sizes):
            boundary = dict(zip(roots,colors))
            assert any(len({(x+(boundary[i] if p<0 else row[p]))%k
                            for i,(x,p) in enumerate(zip(row,parents))})==mass for row in images)
            inputs += 1
    assert seen == expected and offset == len(raw)
    assert (len(seen),inputs) == totals(k,limit,mass)
    return inputs


def small(generate,verify):
    tested = 0
    with TemporaryDirectory() as tmp:
        path = Path(tmp)/'proof'
        bad = Path(tmp)/'bad'
        for k,mass in [(8,3),(9,7),(10,8),(26,7),(32,4),(33,4),(40,3)]:
            for limit in range(1,min(4,mass)+1):
                cmd = [verify,str(k),'--short',str(mass),str(limit)]
                subprocess.run([generate,str(k),'0','1',path,'--short',str(mass),str(limit)],
                               check=True,capture_output=True)
                subprocess.run(cmd+[path],check=True,capture_output=True)
                tested += direct(path,k,mass,limit)
                if (k,mass,limit)==(9,7,3):
                    raw = path.read_bytes()
                    count = unpack_from('<I',raw,14)[0]
                    end = 18+mass*count
                    for data in (raw[:6]+raw[end:],raw+raw[6:end],raw[:5]+bytes((mass-1,))+raw[6:],
                                 raw[:18]+bytes((0,))+raw[19:]):
                        bad.write_bytes(data)
                        assert subprocess.run(cmd+[bad],capture_output=True).returncode
    print(f'{tested} small boundary inputs checked by direct endpoint addition.')


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binaries',nargs=2,type=Path,metavar=('GENERATOR','VERIFIER'))
    args = parser.parse_args()
    if args.binaries:
        small(*(path.resolve() for path in args.binaries))
    for k,mass,limit in [(26,18,6),(26,19,12),(27,19,12),(28,19,12),
                         (30,19,12),(32,19,10),(33,19,8)]:
        shapes,colors = totals(k,limit,mass)
        print(f'k={k} free vertices={mass} tips<={limit} forests={shapes} inputs={colors}')

"""Independently count the equal halves, expand sample rows, and replay actual growth."""
import argparse
from itertools import permutations
from math import gcd
from pathlib import Path
from random import Random
import re
import subprocess
from tempfile import TemporaryDirectory

from research.census.check_typed_leaf_streams import records
from research.rainbow.spine_counts import rooted
from research.rainbow.two_rooted_trees import grow, padded_search


def manifest(path):
    counts = rooted(13)
    expected = {(a,b) for a in counts for b in counts if a <= b and a+b <= 7}
    totals = [0,0,0]
    for line in path.read_text().splitlines():
        found = re.fullmatch(r"[0-9a-f]{64}  forests=(\d+) rows=(\d+) assignments=(\d+)  13,(\d+) 13,(\d+)",line)
        assert found
        shapes, rows, inputs, a, b = map(int,found.groups())
        expected.remove((a,b))
        assert shapes == (counts[a]*counts[b] if a!=b else counts[a]*(counts[a]+1)//2)
        assert shapes <= rows <= inputs == 729*shapes
        for i,v in enumerate((shapes,rows,inputs)):
            totals[i] += v
    assert not expected
    print('equal-half forests, witness rows, literal inputs',*totals)


def replay(parents, old, labels, order, offsets):
    prefix = set(range(len(old)))
    assert labels[:len(old)]==old and len(labels)==len(parents)
    assert all(0<=x<27 for x in labels)
    for v in order:
        assert v not in prefix and parents[v] in prefix
        prefix.add(v)
        vertices, weights = [0]*27,[0]*27
        for w in prefix:
            vertices[labels[w]] += 1
            if w:
                weights[(labels[w]+labels[parents[w]]+offsets.get(w,0))%27] += 1
        assert max(vertices)-min(vertices)<=1 and max(weights)-min(weights)<=1
    assert len(prefix)==len(parents)
    return len(order)


def literal(parents, roots, payload):
    # Derive each pair of actual colors from two different unused edge weights.
    lookup = {}
    for start in range(0,len(payload),26):
        raw = payload[start:start+26]
        for u in range(1,27):
            if gcd(u,27)>1:
                continue
            row = [u*x%27 for x in raw]
            assert set(row)==set(range(1,27))
            used = {(row[i]+row[p])%27 for i,p in enumerate(parents) if p>=0}
            assert len(used)==24
            for x,y in permutations(set(range(27))-used,2):
                lookup.setdefault(((x-row[roots[0]])%27,(y-row[roots[1]])%27),row)
    assert len(lookup)==27**2
    surplus = 17
    old = [surplus]+list(range(27))
    for (a,b),row in lookup.items():
        attach = dict(zip(roots,((a+surplus)%27,(b+surplus)%27)))
        tree = [-1]+[0]*27+[1+attach[i] if p<0 else 28+p for i,p in enumerate(parents)]
        replay(tree,old,old+[(x+surplus)%27 for x in row],list(range(28,54)),{})
    return len(lookup)


def samples(generator, verifier):
    inputs = 0
    with TemporaryDirectory() as tmp:
        file = Path(tmp)/'sample'
        for a,b in [(1,1),(1,2),(2,2)]:
            profile = [f'13,{a}',f'13,{b}']
            make = [generator,'27','0','1',file]
            check = [verifier,'27','--two-roots',file,*profile]
            subprocess.run(make+['--two-roots',*profile],check=True,capture_output=True)
            subprocess.run(check,check=True,capture_output=True)
            rows = list(records(file))
            _,_,body,(p,r,_,_) = rows[len(rows)//2]
            inputs += literal(p,r,body)
            if (a,b)==(1,1):
                subprocess.run(make+['--typed',*profile],check=True,capture_output=True)
                assert subprocess.run(check,capture_output=True).returncode != 0
    print('literal two-color joins',inputs,'cordial prefixes',26*inputs)


def branch(rng, size, tips, first, site):
    if not size:
        return []
    parents = [-1] if tips==1 else [-1]+[0]*tips
    while len(parents)<size:
        v = rng.randrange(len(parents))
        # Subdivide the edge above v, including the entering edge, or grow at a tip.
        if v not in parents and rng.randrange(2):
            parents.append(v)
        else:
            parents.append(parents[v])
            parents[v] = len(parents)-1
    queue = [parents.index(-1)]
    for v in queue:
        queue.extend(w for w,p in enumerate(parents) if p==v)
    ids = {v:first+i for i,v in enumerate(queue)}
    return [site if parents[v]<0 else ids[parents[v]] for v in queue]


def growth(library):
    witness = padded_search(library,27)
    rng = Random(199127)
    trees = prefixes = 0
    cases = [(0,0),(1,0),(26,0),(27,0),(28,0),(0,56),(1,1),(12,12),(13,13),
             (12,14),(1,25),(13,14),(1,26),(14,14),(26,27),(52,53),(150,173)]
    for core in (1,27,28,54,55):
        tree = [-1]+list(range(core-1))
        unit = rng.choice([u for u in range(27) if gcd(u,27)==1])
        shift = rng.randrange(27)
        old = [(unit*v+shift)%27 for v in range(core)]
        for sizes in cases:
            for forked in (False,True):
                p = list(tree)
                roots, offsets = [],{}
                for i,s in enumerate(sizes):
                    if s:
                        roots.append(len(p))
                        offsets[len(p)] = rng.randrange(27)
                        h = min(max(1,s-1),(3,4)[i]) if forked else 1
                        p.extend(branch(rng,s,h,len(p),rng.randrange(core)))
                for first in roots or [None]:
                    order, labels = grow(p,old,first,offsets,witness)
                    if roots:
                        assert order[0]==first
                    prefixes += replay(p,old,labels,order,offsets)
                    trees += 1
    print('fixed-core growth orders',trees,'cordial prefixes',prefixes)


if __name__=='__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('manifest',type=Path)
    cli.add_argument('--samples',nargs=2,metavar=('GENERATOR','VERIFIER'))
    cli.add_argument('--growth',metavar='LIBRARY')
    args = cli.parse_args()
    manifest(args.manifest)
    if args.samples:
        samples(*args.samples)
    if args.growth:
        growth(args.growth)

"""Verify eight-tip uniform attachments at sixteen vertices."""
import argparse
from collections import Counter, defaultdict
import gzip
from itertools import product
from math import gcd
import json
from pathlib import Path

from .verify import components
from research.rainbow.spine_counts import rooted


def canonical(parents):
    children = [[] for _ in parents]
    roots = []
    for i in reversed(range(len(parents))):
        word = '1'+''.join(sorted(children[i],key=lambda w:(len(w),w)))+'0'
        p = parents[i]
        (roots if p < 0 else children[p]).append(word)
    return int(''.join(sorted(roots,key=lambda w:(len(w),w))),2)


def decode(code):
    stack, parents = [], []
    for digit in format(code,'b'):
        if digit == '1':
            i = len(parents)
            parents.append(stack[-1] if stack else -i-1)
            stack.append(i)
        else:
            stack.pop()
    assert not stack and len(parents) == 16 and canonical(parents) == code
    return parents


def flags(catalog):
    words, failures, same = {}, set(), set()
    with gzip.open(catalog,'rt') as stream:
        for line in stream:
            parents,count,_ = json.loads(line)
            if count:
                continue
            word = canonical(parents)
            shape = tuple(sorted(tree for _,tree in components(parents)))
            failures.add(shape)
            words[word] = words.get(word,0) | 1
            if len({p for p in parents if p < 0}) == 1:
                same.add(shape)
                words[word] |= 2
    return words, failures, same


def safe_block(parents, vertices, failures, same):
    indices = {v:i for i,v in enumerate(vertices)}
    sites = {parents[v] for v in vertices if parents[v] not in indices}
    induced = [indices.get(parents[v],-1) for v in vertices]
    shape = tuple(sorted(tree for _,tree in components(induced)))
    return shape not in (same if len(sites)==1 else failures)


def direct_witness(parents, colors):
    source = iter(colors)
    ps = [p if p >= 0 else -1-next(source) for p in parents]
    labels, vertices, weights = [0]*16, [0]*8, [0]*8

    def visit(i):
        if i == 16:
            return True
        p = ps[i]
        b = labels[p] if p >= 0 else -1-p
        for x in range(8):
            w = (b+x) % 8
            if vertices[x] == 2 or weights[w] == 2:
                continue
            labels[i] = x
            vertices[x] += 1
            weights[w] += 1
            if visit(i+1):
                return True
            vertices[x] -= 1
            weights[w] -= 1
        return False

    assert visit(0)
    return labels


def check(cuts, catalog, direct, generate, nine=False):
    _, failures, same = flags(catalog)
    rows = defaultdict(dict)
    if not generate:
        with gzip.open(direct,'rt') as stream:
            for line in stream:
                code,*values = map(int,line.split())
                colors,labels = tuple(values[:-16]),values[-16:]
                assert colors not in rows[code]
                rows[code][colors] = labels
    seen = set()
    counts, hard = Counter(), Counter()
    literal = moment = 0
    allowed = {9} if nine else set(range(1,9))
    with cuts.open() as stream:
        for line in stream:
            code,cut = map(int,line.split())
            assert code not in seen
            seen.add(code)
            ps = decode(code)
            tips = sum(i not in ps for i in range(16))
            assert tips in allowed
            counts[tips] += 1
            if cut:
                assert 0 < cut < (1 << 16)
                first = [i for i in range(16) if cut >> i & 1]
                last = [i for i in range(16) if i not in first]
                assert len(first) == 8 and all(ps[i] < 0 or ps[i] in first for i in first)
                assert safe_block(ps,first,failures,same) and safe_block(ps,last,failures,same)
                continue
            hard[tips] += 1
            roots = [i for i,p in enumerate(ps) if p < 0]
            divisor = gcd(8,*(ps.count(i) for i in range(16)))
            for tail in product(range(8),repeat=len(roots)-1):
                colors = (0,)+tail
                if sum(colors) % divisor:
                    assert nine and len(roots) == divisor == 2
                    assert all(ps.count(i) in (0,2) for i in range(16))
                    moment += 1
                    continue
                if generate:
                    print(code,*colors,*direct_witness(ps,colors))
                else:
                    labels = rows[code].pop(colors)
                    old = dict(zip(roots,colors))
                    weights = [(x+(old[i] if p < 0 else labels[p])) % 8
                               for i,(p,x) in enumerate(zip(ps,labels))]
                    assert Counter(labels) == Counter(weights) == {x:2 for x in range(8)}
                literal += 1
            if not generate:
                assert not rows.pop(code)
    assert counts == {j:c for j,c in rooted(17).items() if j in allowed} and not rows
    if not generate:
        print('forests',sum(counts.values()),'direct shapes',sum(hard.values()),'direct inputs',literal)
        print('direct shapes by tip count',sorted(hard.items()))
        if nine:
            print('normalized inputs excluded by the moment',moment)


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--catalog',type=Path,default=here/'period-pins.jsonl.gz')
    cli.add_argument('--direct',type=Path)
    cli.add_argument('--nine-tips',action='store_true')
    action = cli.add_mutually_exclusive_group(required=True)
    action.add_argument('--flags',action='store_true')
    action.add_argument('--cuts',type=Path)
    cli.add_argument('--generate-direct',action='store_true')
    args = cli.parse_args()
    if args.flags:
        for word,flag in sorted(flags(args.catalog)[0].items()):
            print(word,flag)
    else:
        direct = args.direct or here / ('period-16-nine.txt.gz' if args.nine_tips else 'period-16-direct.txt.gz')
        check(args.cuts,args.catalog,direct,args.generate_direct,args.nine_tips)

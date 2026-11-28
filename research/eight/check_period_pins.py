"""Check every published pin spectrum by assigning vertices along actual edges."""
import argparse
from collections import Counter
import gzip
import json
from math import gcd
from pathlib import Path

from .verify import components, key


def colored_forests():
    level = {(): ()}
    for n in range(8):
        following = {}
        for parents in level.values():
            for p in range(-8,n):
                more = parents+(p,)
                following.setdefault(key(components(more),0,8),more)
        level = following
    return set(level)


def literal(parents):
    labels = [0]*8
    masks = [0]*8

    def assign(i, used, weights):
        if i == 8:
            for v,x in enumerate(labels):
                masks[v] |= 1 << x
            return 1
        p = parents[i]
        parent = labels[p] if p >= 0 else -1-p
        count = 0
        for x in range(8):
            if used & (1 << x):
                continue
            w = (parent+x) % 8
            if weights & (1 << w):
                continue
            labels[i] = x
            count += assign(i+1, used | (1 << x), weights | (1 << w))
        return count

    return assign(0,0,0), masks


def check(path):
    remaining = colored_forests()
    stats = Counter()
    exceptional_shapes = Counter()
    common = []
    pins = 0
    with gzip.open(path,'rt') as stream:
        for line in stream:
            parents, count, masks = json.loads(line)
            assert len(parents) == 8 and all(-8 <= p < i for i,p in enumerate(parents))
            assert literal(parents) == (count,masks)
            parts = components(parents)
            orbit = {key([(u*c % 8,tree) for c,tree in parts],d,8)
                     for u in (1,3,5,7) for d in range(8)}
            assert orbit <= remaining
            remaining.difference_update(orbit)
            g = gcd(8,*(parents.count(i) for i in range(8)))
            moment = sum(c for c,_ in parts) % g == 0
            assert not count or moment
            kind = 'yes' if count else 'extra' if moment else 'moment'
            stats[len(parts),kind] += len(orbit)
            if kind == 'extra':
                exceptional_shapes[tuple(sorted(tree for _,tree in parts))] += len(orbit)
            if len({c for c,_ in parts}) == 1:
                if not count:
                    common.append(tuple(parents))
                pins += sum(bool(mask & (1 << parts[0][0])) for mask in masks)
    assert not remaining
    assert sum(value for (_,kind),value in stats.items() if kind == 'extra') == 420
    assert all(not stats[c,kind] for c in (1,3,5,7) for kind in ('extra','moment'))
    print('components, feasible, failed congruence, further failures')
    for c in range(1,9):
        print(c,stats[c,'yes'],stats[c,'moment'],stats[c,'extra'])
    print('exceptional uncolored shapes')
    for shape,n in sorted(exceptional_shapes.items(),key=lambda r:(len(r[0]),r[0])):
        print(n,*shape)
    print('common-parent failures',common)
    print('rooted-index pairs permitting a shared surplus',pins)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('catalog',type=Path,default=Path(__file__).with_name('period-pins.jsonl.gz'),nargs='?')
    check(parser.parse_args().catalog)

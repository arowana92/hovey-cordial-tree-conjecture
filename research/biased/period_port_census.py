"""Enumerate doubly marked order-27 trees by their branches at the unique centroid."""
import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement, groupby, product
from math import comb
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryFile

from research.census.few_leaf_rings import trees
from research.rainbow.spine_counts import partitions, rooted


def word(children):
    value = 1
    for branch in sorted(children):
        value = (value<<branch.bit_length()) | branch
    return value<<1


@lru_cache(None)
def branches(size,tips):
    shapes = []
    for text in trees(size,tips):
        stack = []
        for symbol in text:
            if symbol=='(':
                stack.append([])
            else:
                code = word(stack.pop())
                if stack:
                    stack[-1].append(code)
        shapes.append(code)
    return tuple(sorted(shapes))


def tip_assignments(sizes,remaining,previous=0,least=1):
    if not sizes:
        if remaining==0:
            yield ()
        return
    size = sizes[0]
    lower = least if previous==size else 1
    upper = min(remaining-len(sizes)+1,max(1,size-1))
    for h in range(lower,upper+1):
        for tail in tip_assignments(sizes[1:],remaining-h,size,h):
            yield ((size,h),)+tail


def centered_words(leaves):
    codes = []
    for sizes in partitions(26):
        if sizes[-1]>13 or len(sizes)>leaves:
            continue
        for profile in tip_assignments(sizes,leaves):
            choices = [combinations_with_replacement(branches(s,h),len(list(group)))
                       for (s,h),group in groupby(profile)]
            for parts in product(*choices):
                codes.append(word(branch for part in parts for branch in part))
    return sorted(codes)


def independent_counts():
    # Multiply the multiset factors for all rooted branch types, truncating at mass 26.
    states = {(0,0):1}
    for size in range(1,14):
        for tips,multiplicity in rooted(size).items():
            new = defaultdict(int)
            for (mass,leaves),ways in states.items():
                for q in range((26-mass)//size+1):
                    new[mass+q*size,leaves+q*tips] += ways*comb(multiplicity+q-1,q)
            states = new
    return {h:n for (mass,h),n in states.items() if mass==26}


def check(lines,leaves):
    counts = independent_counts()
    totals = defaultdict(lambda:[0,0])
    last = {}
    for line in lines:
        match = re.fullmatch(r'(\d+) (\d+) (\d+) (\d+) (\d+) ([0-9a-f]{64})\n',line)
        assert match
        h,n,rows,first,end = map(int,match.groups()[:5])
        assert h in leaves and 1<=n<=rows and last.get(h,0)<first<=end
        totals[h][0] += n
        totals[h][1] += rows
        last[h] = end
    for h in leaves:
        assert totals[h][0]==counts[h]
    return dict(sorted(totals.items()))


def generate(leaves,make,verify,directory,workers):
    directory.mkdir(exist_ok=True)
    lines = []
    for h in leaves:
        codes = centered_words(h)
        assert len(codes)==independent_counts()[h]
        def shard(start):
            name = directory/f'{h}-{start}.checked'
            if name.exists():
                return name.read_text()
            data = ''.join(f'{x}\n' for x in codes[start:start+4096]).encode()
            with TemporaryFile(dir=directory) as stream:
                subprocess.run([make,'--ports'],input=data,stdout=stream,check=True)
                stream.seek(0)
                result = subprocess.run([verify,'--ports',str(h)],stdin=stream,
                                        capture_output=True,text=True,check=True)
                stream.seek(0)
                digest = sha256()
                for block in iter(lambda:stream.read(1<<20),b''):
                    digest.update(block)
            line = f'{h} {result.stdout.strip()} {digest.hexdigest()}\n'
            tmp = name.with_suffix('.pending')
            tmp.write_text(line)
            tmp.replace(name)
            return line
        with ThreadPoolExecutor(max_workers=workers) as pool:
            lines.extend(pool.map(shard,range(0,len(codes),4096)))
    print(check(lines,leaves))
    (directory/'manifest.txt').write_text(''.join(lines))


if __name__=='__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('leaves',nargs='+',type=int)
    mode = cli.add_mutually_exclusive_group(required=True)
    mode.add_argument('--run',type=Path)
    mode.add_argument('--manifest',type=Path)
    mode.add_argument('--sample',type=int,help='print this many evenly spaced words per leaf count')
    cli.add_argument('--generator',type=Path)
    cli.add_argument('--verifier',type=Path)
    cli.add_argument('--workers',type=int,default=2)
    args = cli.parse_args()
    if args.run:
        generate(args.leaves,args.generator.resolve(),args.verifier.resolve(),args.run,args.workers)
    elif args.manifest:
        print(check(args.manifest.read_text().splitlines(True),args.leaves))
    else:
        for h in args.leaves:
            words = centered_words(h)
            for i in range(min(args.sample,len(words))):
                print(words[i*(len(words)-1)//max(1,min(args.sample,len(words))-1)])

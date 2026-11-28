"""Generate, independently verify and count marked-tree color certificates modulo 27."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryFile

from research.biased.verify import free_count


def summary(lines,n,edge=False):
    total = free_count(n)
    shards = len(lines)
    trees = rows = 0
    for j,line in enumerate(lines):
        match = re.fullmatch(rf"{j}/{shards} [0-9a-f]{{64}} (\d+) (\d+)\n",line)
        assert match
        shapes, witnesses = map(int,match.groups())
        assert shapes == len(range(j,total,shards)) and witnesses >= shapes
        trees += shapes
        rows += witnesses
    assert trees == total
    print('order',n,'unrooted trees',trees,'rows',rows,'marked inputs',trees*(n-int(edge))*27)


def run(n,shards,workers,make,check,output,edge):
    if min(shards,workers)<1:
        raise ValueError('positive shard and worker counts required')
    output.mkdir()
    def worker(j):
        args = [str(n),str(j),str(shards)]+(['--edge'] if edge else [])
        with TemporaryFile(dir=output) as stream:
            subprocess.run([make,*args],stdout=stream,check=True)
            stream.seek(0)
            report = subprocess.run([check,*args],stdin=stream,stdout=subprocess.PIPE,
                                    check=True,text=True).stdout
            stream.seek(0)
            digest = hashlib.sha256()
            for block in iter(lambda:stream.read(1<<20),b''):
                digest.update(block)
        row = f'{j}/{shards} {digest.hexdigest()} '+report
        (output/f'{j}.checked').write_text(row)
        return row
    with ThreadPoolExecutor(max_workers=workers) as pool:
        lines = list(pool.map(worker,range(shards)))
    summary(lines,n,edge)
    (output/'manifest.txt').write_text(''.join(lines))


def samples(stream,n,limit):
    with stream.open('rb') as f:
        for _ in range(limit):
            raw = f.read(8)
            if not raw:
                break
            assert len(raw)==8
            word = int.from_bytes(raw,'little')
            adj = [[] for _ in range(n)]
            stack = []
            i = 0
            for bit in format(word,'b'):
                if bit=='0':
                    stack.pop()
                else:
                    if stack:
                        adj[i].append(stack[-1])
                        adj[stack[-1]].append(i)
                    stack.append(i)
                    i += 1
            assert i==n and not stack
            rows = []
            while True:
                lead = f.read(1)
                if lead==b'\xff':
                    break
                assert lead
                row = lead+f.read(n-1)
                assert len(row)==len(set(row))==n and max(row)<27
                rows.append(row)
            yield adj,rows


def replay(stream,n,limit):
    # Actual joins onto a 28-vertex star. Its center is zero, and its leaves
    # contain each residue once. Every boundary color is present on a leaf.
    units = [u for u in range(1,27) if u%3]
    prefixes = trees = 0
    for adj,rows in samples(stream,n,limit):
        for root in range(n):
            # Each available witness is chosen by transforming the literal
            # labels. A different marked vertex gives a different old joint.
            options = {}
            for row in rows:
                for u in units:
                    for hole in set(range(27)).difference(row)|{row[root]}:
                        b = u*(row[root]-hole)%27
                        if b not in options:
                            options[b] = [u*(x-hole)%27 for x in row]
                if len(options)==27:
                    break
            assert len(options)==27
            order = [(root,-1)]
            for v,p in order:
                order.extend((w,v) for w in adj[v] if w!=p)
            for b,labels in options.items():
                vertex,edge = [2]+[1]*26,[1]*27
                assert labels[root]==b
                for v,p in order[1:]:
                    vertex[labels[v]] += 1
                    edge[(labels[v]+labels[p])%27] += 1
                    assert max(vertex)-min(vertex)<=1 and max(edge)-min(edge)<=1
                    prefixes += 1
                trees += 1
    print('whole-tree joins',trees,'cordial prefixes',prefixes)


def replay_edges(stream,n,limit):
    from collections import Counter
    units=[u for u in range(1,27) if u%3]
    path=[i//2+14*(i%2) for i in range(27)]
    [hole]=set(range(27))-{(a+b)%27 for a,b in zip(path,path[1:])}
    expansions=0
    for adj,rows in samples(stream,n,limit):
        edges=[(v,w) for v,neighbors in enumerate(adj) for w in neighbors if v<w]
        for mark,(a,b) in enumerate(edges):
            options={}
            for row in rows:
                for u in units:
                    labels=[u*x%27 for x in row]
                    sums=[(labels[x]+labels[y])%27 for x,y in edges]
                    other=set(sums[:mark]+sums[mark+1:])
                    assert len(other)==n-2
                    for offset in range(27):
                        if offset not in options and (sums[mark]+offset)%27 not in other:
                            options[offset]=labels
                if len(options)==27:
                    break
            assert len(options)==27
            for offset,labels in options.items():
                # Expand the marked edge to a 27-vertex path. Its entering port
                # has label zero, and its outgoing port realizes this offset.
                end=path.index((offset+hole)%27)
                shift=(labels[a]-hole)%27
                full=labels+[(x+shift)%27 for x in path]
                actual=edges[:mark]+edges[mark+1:]+[(a,n),(b,n+end)]
                actual.extend((n+i,n+i+1) for i in range(26))
                old=[(labels[x]+labels[y]+(offset if j==mark else 0))%27
                     for j,(x,y) in enumerate(edges)]
                assert len(set(old))==n-1
                period=Counter(range(27))
                assert Counter(full)==Counter(labels)+period
                assert Counter((full[x]+full[y])%27 for x,y in actual)==Counter(old)+period
                expansions+=1
    print('one-offset joins expanded on whole trees',expansions)


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('order',type=int)
    mode = cli.add_mutually_exclusive_group(required=True)
    mode.add_argument('--manifest',type=Path)
    mode.add_argument('--replay',type=Path)
    mode.add_argument('--run',type=Path,metavar='OUTPUT')
    cli.add_argument('--generator',type=Path)
    cli.add_argument('--verifier',type=Path)
    cli.add_argument('--shards',type=int,default=128)
    cli.add_argument('--workers',type=int,default=1)
    cli.add_argument('--sample',type=int,default=4)
    cli.add_argument('--edge',action='store_true')
    args = cli.parse_args()
    if args.manifest:
        summary(args.manifest.read_text().splitlines(True),args.order,args.edge)
    elif args.replay:
        (replay_edges if args.edge else replay)(args.replay,args.order,args.sample)
    else:
        if not args.generator or not args.verifier:
            cli.error('--run requires --generator and --verifier')
        run(args.order,args.shards,args.workers,args.generator.resolve(),args.verifier.resolve(),args.run,args.edge)

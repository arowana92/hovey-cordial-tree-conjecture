"""Independent centroid counts, small full-catalog comparisons and direct sample checks."""

import argparse
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from research.rainbow.spine_counts import forest_leaves, partitions


def centroid_count(n, limit):
    def count(sizes):
        if len(sizes) > limit:
            return 0
        return sum(v for t,v in forest_leaves(sizes).items() if t <= limit)
    one = sum(count(sizes) for sizes in partitions(n-1) if 2*sizes[-1] < n)
    two = 0 if n%2 else count((n//2,n//2))
    return one, two


def check_row(data, n, modular):
    word = int.from_bytes(data[:8],'little')
    labels = list(data[8:])
    assert sorted(labels) == list(range(n))
    stack, edges = [], []
    index = 0
    for bit in bin(word)[2:]:
        if bit == '1':
            if stack:
                edges.append((stack[-1],index))
            stack.append(index)
            index += 1
        else:
            stack.pop()
    assert not stack and index == n and len(edges) == n-1
    degree = [0]*n
    sums = []
    for u,v in edges:
        degree[u] += 1
        degree[v] += 1
        sums.append(labels[u]+labels[v])
    if modular:
        assert len({s%n for s in sums}) == n-1
    else:
        assert sorted(sums) == list(range(min(sums),min(sums)+n-1))
    return degree.count(1)


def rows(path,n):
    data = path.read_bytes()
    assert len(data)%(n+8) == 0
    return [data[i:i+n+8] for i in range(0,len(data),n+8)]


def small(integer, modular, verify):
    with TemporaryDirectory() as tmp:
        whole, limited, bases, bad = (Path(tmp)/s for s in ('whole','limited','bases','bad'))
        for n in range(2,15):
            subprocess.run([integer,str(n),'0','1',whole],check=True,stderr=subprocess.DEVNULL)
            all_rows = [(r,check_row(r,n,False)) for r in rows(whole,n)]
            for limit in range(2,min(8,n)+1):
                selected = [r for r,t in all_rows if t <= limit]
                assert len(selected) == sum(centroid_count(n,limit))
                subprocess.run([integer,str(n),'0','1',limited,'--leaves',str(limit)],
                               check=True,stderr=subprocess.DEVNULL)
                assert rows(limited,n) == selected
                subprocess.run([verify,str(n),'--leaves',str(limit),limited],check=True,stdout=subprocess.DEVNULL)
                if n < 5:
                    continue
                subprocess.run([modular,str(n),str(limit),'0','1',bases],check=True,stdout=subprocess.DEVNULL)
                observed = rows(bases,n)
                assert [r[:8] for r in observed] == [r[:8] for r in selected]
                assert all(check_row(r,n,True) <= limit for r in observed)
                cmd = [verify,str(n),'--modular-leaves',str(limit)]
                subprocess.run(cmd+[bases],check=True,stdout=subprocess.DEVNULL)
                if n == 10 and limit == 4:
                    data = bases.read_bytes()
                    duplicate_label = bytearray(data)
                    duplicate_label[9] = duplicate_label[8]
                    for damaged in (data[n+8:], bytes(duplicate_label), data[:n+8]+data):
                        bad.write_bytes(damaged)
                        assert subprocess.run(cmd+[bad],capture_output=True).returncode != 0
    print("Centroid words and integer rows match the unrestricted small catalogs.")


def sample(path,n,count,limit,modular):
    assert path.stat().st_size == count*(n+8)
    with path.open('rb') as stream:
        for j in range(257):
            index = j*(count-1)//256
            stream.seek(index*(n+8))
            assert check_row(stream.read(n+8),n,modular) <= limit


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--binaries',nargs=3,type=Path,metavar=('INTEGER','MODULAR','VERIFIER'))
    cli.add_argument('--files',type=Path)
    args = cli.parse_args()
    if args.binaries:
        small(*(p.resolve() for p in args.binaries))
    for n in (28,29,30):
        for limit, kind in ((6,'int'),(8,'mod')):
            one,two = centroid_count(n,limit)
            print(f"order={n} leaves<={limit} one centroid={one} two centroids={two} total={one+two}")
            if args.files:
                sample(args.files/f'{kind}{n}-l{limit}.bin',n,one+two,limit,kind=='mod')

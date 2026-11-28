"""Assemble path witnesses on actual cores and recount every prefix."""

from functools import lru_cache
from math import gcd
from pathlib import Path
from random import Random
import sys

from .check_cut_growth import replay


class Catalog:
    def __init__(self, directory, k, paths=5):
        self.k = k
        self.positions = {}
        for j in range(1, paths+1):
            path = directory / f"multipath-{k}-{j}"
            with path.open("rb") as stream:
                while True:
                    start = stream.tell()
                    line = stream.readline()
                    if not line:
                        break
                    fields = line.split(None, 2+j)
                    assert list(map(int, fields[:2])) == [k,j]
                    self.positions[tuple(map(int, fields[2:2+j]))] = path, start

    @lru_cache(32)
    def words(self, lengths):
        path, offset = self.positions[lengths]
        with path.open("rb") as stream:
            stream.seek(offset)
            return stream.readline().split()[2+len(lengths):]

    def batch(self, parents, segments, surplus):
        k = self.k
        lengths = [len(segment) for segment in segments]
        # Pad one segment after its actual tip. Sort after padding to find the row.
        padded = lengths[:]
        padded[-1] += k-1-sum(padded)
        order = sorted(range(len(padded)), key=padded.__getitem__)
        shape = tuple(padded[j] for j in order)
        first = [sum(shape[:j]) for j in range(len(shape))]
        internal = sorted(set(range(k-1))-set(first))
        choices = []
        for u in range(1,k):
            if gcd(k,u) == 1:
                inv = pow(u,-1,k)
                choices.append((u, [(parents[j]-surplus)*inv % k for j in order]))
        for word in self.words(shape):
            x = [v-33 for v in word]
            weights = {(x[v]+x[v-1]) % k for v in internal}
            assert len(weights) == len(internal)
            for u, boundary in choices:
                entering = {(x[i]+b) % k for i,b in zip(first,boundary)}
                if len(entering) != len(shape) or not weights.isdisjoint(entering):
                    continue
                return {v: (surplus+u*x[start+i]) % k for j,start in zip(order,first)
                        for i,v in enumerate(segments[j])}
        raise ValueError((shape, parents, surplus))


def check(directory, k, paths=5):
    catalog = Catalog(directory, k, paths)
    rng = Random(1991+k)
    total = 0
    for core in (k,k+1):
        for arms in range(1,paths+1):
            for common in (False,True):
                shift = rng.randrange(k)
                labels = [(v+shift)%k for v in range(core)]
                parent = [-1]+[0]*(core-1)
                tips = [rng.randrange(core) for _ in range(arms)]
                if common:
                    tips = [tips[0]]*arms
                order = list(range(arms)) + [rng.randrange(arms) for _ in range(2*k+7)]
                rng.shuffle(order)
                for arm in order:
                    parent.append(tips[arm])
                    tips[arm] = len(parent)-1
                while len(labels)<len(parent):
                    n = len(labels)
                    if n%k == 0:
                        counts = [0]*k
                        for v in range(1,n):
                            counts[(labels[v]+labels[parent[v]])%k] += 1
                        deficit = counts.index(min(counts))
                        labels.append((deficit-labels[parent[n]])%k)
                        continue
                    assert n%k == 1
                    counts = [labels.count(x) for x in range(k)]
                    surplus = counts.index(max(counts))
                    end = min(n+k-1,len(parent))
                    by_arm = {}
                    for v in range(n,end):
                        by_arm.setdefault(order[v-core],[]).append(v)
                    segments = list(by_arm.values())
                    boundary = [labels[parent[seg[0]]] for seg in segments]
                    placed = catalog.batch(boundary,segments,surplus)
                    labels.extend(placed[v] for v in range(n,end))
                total += replay(parent,labels,k,range(core,len(parent)),range(core))
    print(k, "actual tree prefixes", total)


if __name__ == "__main__":
    if len(sys.argv)==4:
        check(Path(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
    else:
        for modulus in (26,27):
            check(Path(sys.argv[1]),modulus)

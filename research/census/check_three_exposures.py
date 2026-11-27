"""Check the arm certificates, degree-three mass profiles and padded forest construction."""

from argparse import ArgumentParser
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
from random import Random

from .check_paired_joins import arms, decode, holes, possible_fake, ring, ORBITS, UNITS
from ..paired_forest import extend
from ..check_near_matching import maximum


def neutral(path):
    total = 0
    with path.open() as data:
        for split,pattern in product(range(7),range(4096)):
            s,m,*rows = next(data).split()
            assert (int(s),int(m)) == (split,pattern)
            edges,roots = arms(split,pattern)
            served = set()
            for row in rows:
                labels = decode(row)
                left,right = [labels[v] for v in roots]
                u,v = holes(labels,edges)
                for x,y in [(u,v),(v,u)]:
                    served.update(ORBITS[(x-y-left+right)%26])
            expected = set(range(26)) if pattern else set(range(0,26,2))
            assert served==expected
            total += len(rows)
        assert not data.read()
    return total


def transfers(path):
    trials = 0
    with path.open() as data:
        for split in range(7):
            s,pattern,*rows = next(data).split()
            assert int(s)==split and int(pattern)==0
            edges,roots = arms(split,0)
            for q in (1,13):
                adj = {v:set() for v in range(26)}
                for row in rows:
                    f = decode(row)
                    holes(f,edges)
                    for unit in UNITS:
                        for t in range(26):
                            g = [(unit*x+t)%26 for x in f]
                            counts = [0]*26
                            for i,j in edges:
                                counts[(g[i]+g[j])%26] += 1
                            counts[g[roots[0]]] += 1
                            counts[(q+g[roots[1]])%26] += 1
                            if counts.count(1)==24 and 2 in counts:
                                adj[counts.index(2)].add(counts.index(0))
                            trials += 1
                for start in adj:
                    seen = {start}
                    queue = [start]
                    for v in queue:
                        new = adj[v]-seen
                        queue.extend(new)
                        seen.update(new)
                    assert len(seen)==26
        assert not data.read()
    return trials


def check_profiles():
    total = branched = shared = 0
    for s in range(6):
        for h in combinations_with_replacement(range(1,12-s),3):
            if sum(h)+s!=23:
                continue
            for placed in combinations_with_replacement(range(24-s),s):
                # Index zero is the median. The three arms run from their tips inward.
                counts = Counter(placed)
                offset = 1
                prefixes = []
                for length in h:
                    end = {0:0}
                    mass = 0
                    for i in range(length):
                        mass += 1+counts[offset+i]
                        end[mass]=i+1
                    prefixes.append(end)
                    offset += length
                for i,j in combinations(range(3),2):
                    pairs = [(x,12-x) for x in prefixes[i] if 12-x in prefixes[j]]
                    assert pairs
                    for x,y in pairs:
                        side = 12-prefixes[i][x]-prefixes[j][y]
                        same_pair = (x==max(prefixes[i]) and y==max(prefixes[j]))
                        assert 0<=side<=5 and (not same_pair or side==0)
                        branched += side>0
                        shared += same_pair
                total += 1
    return total,branched,shared


def padded_forests():
    rng = Random(260351)
    total = 0
    for m in (3,5,7,11,13):
        k = 2*m
        for _ in range(180):
            multiple = rng.choice([1,1,1,2,3])
            count = rng.randint(1,m) if multiple==1 else m*multiple
            dummy = {rng.randrange(count)} if multiple>1 else {
                i for i in range(count) if rng.randrange(2)}
            boundary = [rng.randrange(k) for _ in range(5)]
            links = []
            for i in range(count):
                p = rng.randrange(-5,i)
                # Port one is reserved for deletion in each padded pair.
                links.append((p,0 if p in dummy else rng.randrange(2),
                              0 if i in dummy else rng.randrange(2),rng.randrange(k)))
            deficit = rng.randrange(k)
            f = extend(m,boundary,links,deficit)
            vx,ex = [1]*k,[1]*k
            ex[deficit] -= 1
            for i,(p,a,b,off) in enumerate(links):
                par = f[p][a] if p>=0 else boundary[-1-p]
                ex[(par+f[i][b]+off)%k] += 1
                vx[f[i][0]] += 1
                if i not in dummy:
                    vx[f[i][1]] += 1
                    ex[sum(f[i])%k] += 1
            assert max(vx)-min(vx)<=1 and max(ex)-min(ex)<=1
            total += 1
    return total


def check_51(edges, roots, records, core_ports):
    # A 25-vertex path with 24 consecutive edge weights. The boundary
    # sites may coincide. Try affine changes and count the actual 51 vertices.
    base = [v//2 + 13*(v%2) for v in range(25)]
    full_edges = [(v-1,v) for v in range(1,25)]+[(25+a,25+b) for a,b in edges]
    full_edges += [(u,25+v) for u,v in zip(core_ports,roots)]
    adj = [[] for _ in range(51)]
    for u,v in full_edges:
        adj[u].append(v)
        adj[v].append(u)
    queue = [0]
    seen = {0:0}
    parents = [-1]
    for u in queue:
        for v in adj[u]:
            if v not in seen:
                seen[v] = len(queue)
                queue.append(v)
                parents.append(seen[u])
    assert len(queue)==51 and len(full_edges)==50
    deficiency = 51-2*maximum(parents)
    assert deficiency in (1,3)
    for row in records:
        f = decode(row)
        for unit in UNITS:
            scaled = [unit*x for x in f]
            for t in range(26):
                labels = base+[(x+t)%26 for x in scaled]
                counts = [0]*26
                for u,v in full_edges:
                    counts[(labels[u]+labels[v])%26] += 1
                if max(counts)-min(counts)<=1:
                    assert sorted(labels.count(v) for v in range(26))==[1]+[2]*25
                    return deficiency
    raise AssertionError("no whole-tree labeling")


def sample_trees(out,rings):
    rng = Random(5126)
    cases = Counter()
    for path in (out/'neutral-arms.txt',out/'transfer-arms.txt'):
        for i,line in enumerate(path.open()):
            if i>=7 and i%617: continue
            s,pattern,*rows = line.split()
            e,roots = arms(int(s),int(pattern))
            p,q = rng.randrange(25),rng.randrange(25)
            if int(pattern)==0 and 'neutral' in path.name: q=p
            cases[check_51(e,roots,rows,(p,q))] += 1
    if rings:
        for b in range(1,6):
            with (rings/f'socket{b}.txt').open() as data:
                for i,line in enumerate(data):
                    if i>=8 and i%131071: continue
                    key,*rows=line.split()
                    c,es=ring(key)
                    fake=rng.choice([i for i in range(c) if possible_fake(es,es[i])])
                    close=rng.choice([j for j in range(c) if j!=fake])
                    e=[edge for j,edge in enumerate(es) if j not in (fake,close)]
                    p=rng.randrange(25)
                    q=rng.choice([v for v in range(25) if v//2!=p//2])
                    cases[check_51(e,es[close],rows,(p,q))] += 1
    return dict(sorted(cases.items()))


if __name__ == '__main__':
    args = ArgumentParser()
    args.add_argument('directory',type=Path)
    args.add_argument('--ring-directory',type=Path)
    options = args.parse_args()
    out = options.directory
    print('neutral arm bijections',neutral(out/'neutral-arms.txt'))
    print('literal transfer histograms',transfers(out/'transfer-arms.txt'))
    print('tripod profiles, branched splits, shared-site-pair splits',*check_profiles())
    print('padded forest extensions',padded_forests())
    print('literal 51-vertex trees by matching deficiency',sample_trees(out,options.ring_directory))

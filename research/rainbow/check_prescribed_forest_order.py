"""Count the independent boundary tests and replay prescribed orders on complete trees."""
import argparse
from collections import Counter
from itertools import combinations_with_replacement, permutations, product
from math import comb, gcd
from pathlib import Path
from random import Random
import re
import subprocess
from tempfile import TemporaryDirectory

from research.check_matching_expansion import check as check_histograms
from research.check_near_matching import maximum
from research.near_matching import label as match_and_lift
from research.census.check_typed_leaf_streams import records
from research.rainbow.check_two_rooted_trees import branch, replay
from research.rainbow.prescribed_forest_order import extend
from research.rainbow.spine_counts import forest_leaves, partitions, rooted
from research.rainbow.two_rooted_trees import padded_search


def catalog(tips):
    wanted = {}
    for sizes in partitions(26):
        if not 3<=len(sizes)<tips:
            continue
        # Every assignment, including one with a different color at every root,
        # is ordered exactly when all component positions can begin a new run.
        if all(s>=sum(sizes[:i])+i for i,s in enumerate(sizes)):
            continue
        groups = sorted(Counter(sizes).items())
        options = [list(combinations_with_replacement(range(1,min(s,tips)+1),n)) for s,n in groups]
        for terms in product(*options):
            if sum(map(sum,terms))!=tips:
                continue
            profile,ways = [],1
            for (s,n),hs in zip(groups,terms):
                for h,c in Counter(hs).items():
                    ways *= comb(rooted(s).get(h,0)+c-1,c)
                profile.extend((s,h) for h in hs)
            if ways:
                wanted[tuple(profile)] = ways
    return wanted


def manifest(path,tips):
    needed = catalog(tips)
    totals = [0]*3
    for line in path.read_text().splitlines():
        m = re.fullmatch(r'[0-9a-f]{64}  forests=(\d+) rows=(\d+) assignments=(\d+)  (.+)',line)
        assert m
        numbers = list(map(int,m.groups()[:3]))
        profile = tuple(tuple(map(int,x.split(','))) for x in m[4].split())
        assert numbers[0]==needed.pop(profile)
        assert numbers[0]<=numbers[1]<=numbers[2]==numbers[0]*27**len(profile)
        totals = [a+b for a,b in zip(totals,numbers)]
    assert not needed
    print('tips, supplementary forests, rows, assignments',tips,*totals)
    shapes = inputs = 0
    for sizes in partitions(26):
        if len(sizes)<=tips:
            n = sum(c for h,c in forest_leaves(sizes).items() if h<=tips)
            shapes += n
            inputs += n*27**len(sizes)
    print('all forests and literal assignments through',tips,'tips',shapes,inputs)


def literal(parents,roots,payload):
    k = 27
    r = len(roots)
    rng = Random(27+r)
    selected = {tuple(rng.randrange(k) for _ in roots) for _ in range(64)}
    selected.update({(0,)*r,(9,)*r,tuple(range(r))})
    targets = {sum(x*k**i for i,x in enumerate(c)):c for c in selected}
    seen = bytearray(k**r)
    old = [8]+list(range(k))
    joined = 0
    for pos in range(0,len(payload),26):
        row = payload[pos:pos+26]
        assert set(row)==set(range(1,k))
        used = {(row[i]+row[p])%k for i,p in enumerate(parents) if p>=0}
        assert len(used)==26-r
        spare = sorted(set(range(k))-used)
        perms = list(permutations(spare,r))
        for u in range(1,k):
            if gcd(u,k)>1:
                continue
            byroot = [{w:(u*(w-row[v])%k)*k**i for w in spare} for i,v in enumerate(roots)]
            for ws in perms:
                code = sum(table[w] for table,w in zip(byroot,ws))
                seen[code] = 1
                if code in targets:
                    c = targets.pop(code)
                    site = dict(zip(roots,c))
                    p = [-1]+[0]*27+[1+(8+site[i])%k if w<0 else 28+w for i,w in enumerate(parents)]
                    labels = old+[(8+u*x)%k for x in row]
                    replay(p,old,labels,list(range(28,54)),{})
                    joined += 1
    assert all(seen) and not targets
    return len(seen),joined


def samples(generator,verifier):
    inputs = joined = 0
    with TemporaryDirectory() as tmp:
        path = Path(tmp)/'stream'
        for profile in [('3,2','10,1','13,1'),('3,2','3,2','20,1'),('3,2','5,1','9,1','9,1')]:
            make = [generator,'27','0','1',path]
            check = [verifier,'27','--independent-roots',path,*profile]
            subprocess.run(make+['--independent-roots',*profile],check=True,capture_output=True)
            subprocess.run(check,check=True,capture_output=True)
            _,_,payload,(p,roots,_,_) = next(records(path))
            i,j = literal(p,roots,payload)
            inputs += i
            joined += j
            subprocess.run(make+['--typed',*profile],check=True,capture_output=True)
            assert subprocess.run(check,capture_output=True).returncode
    print('literal boundary inputs',inputs,'whole trees',joined,'prefixes',26*joined)


def six_tip_samples(generator,verifier):
    rng = Random(276)
    profiles = [('5,1','5,4','16,1'), ('3,2','3,2','10,1','10,1'),
                ('1,1','3,2','4,1','9,1','9,1')]
    joined = 0
    with TemporaryDirectory() as tmp:
        path = Path(tmp)/'stream'
        for profile in profiles:
            subprocess.run([generator,'27','0','1',path,'--independent-roots',*profile],
                           check=True,capture_output=True)
            subprocess.run([verifier,'27','--independent-roots',path,*profile],
                           check=True,capture_output=True)
            _,_,payload,(p,roots,_,_) = next(records(path))
            targets = {tuple(rng.randrange(27) for _ in roots) for _ in range(80)}
            targets.update(tuple(x for _ in roots) for x in (0,1,9,18))
            targets.add(tuple(range(len(roots))))
            old = [8]+list(range(27))
            for pos in range(0,len(payload),26):
                row = payload[pos:pos+26]
                assert set(row)==set(range(1,27))
                spare = set(range(27))-{(row[v]+row[u])%27 for v,u in enumerate(p) if u>=0}
                assert len(spare)==len(roots)+1
                for unit in range(1,27):
                    if unit%3==0:
                        continue
                    inverse = pow(unit,-1,27)
                    for colors in targets.copy():
                        entering = {(row[v]+b*inverse)%27 for v,b in zip(roots,colors)}
                        if len(entering)!=len(roots) or not entering<=spare:
                            continue
                        site = dict(zip(roots,colors))
                        parent = [-1]+[0]*27+[1+(8+site[i])%27 if u<0 else 28+u
                                               for i,u in enumerate(p)]
                        labels = old+[(8+unit*x)%27 for x in row]
                        replay(parent,old,labels,list(range(28,54)),{})
                        targets.remove(colors)
                        joined += 1
                if not targets:
                    break
            assert not targets
    print('six-tip whole-tree joins',joined,'prefixes',26*joined)


def growth(library,tip_bound=5):
    rng = Random(272611)
    search = padded_search(library,27)
    prefixes = runs = 0
    patterns = ((5,), (2,3), (1,2,2), (1,1,1,2), (1,1,1,1,1))
    if tip_bound==6:
        patterns = ((6,), (3,3), (2,2,2), (1,1,2,2), (1,1,1,1,2), (1,1,1,1,1,1))
    for core in (1,27,28,54,55):
        backbone = [-1]+list(range(core-1))
        old = [(5*i+7)%27 for i in range(core)]
        for tips in patterns:
            for extra in (0,1,23,26,27,54,108):
                p = list(backbone)
                for h in tips:
                    size = (1 if h==1 else h+1)+rng.randint(0,extra//len(tips))
                    p.extend(branch(rng,size,h,len(p),rng.randrange(core)))
                for _ in range(3):
                    pool = [i for i in range(core,len(p)) if p[i]<core]
                    order = []
                    while pool:
                        v = pool.pop(rng.randrange(len(pool)))
                        order.append(v)
                        pool.extend(i for i in range(core,len(p)) if p[i]==v)
                    offsets = {}
                    pos = 0
                    while pos<len(order):
                        n = 1 if (core+pos)%27==0 else 26
                        batch = set(order[pos:pos+n])
                        offsets.update((v,rng.randrange(27)) for v in batch if p[v] not in batch)
                        pos += n
                    labels = extend(p,old,order,27,search,offsets)
                    prefixes += replay(p,old,labels,order,offsets)
                    runs += 1
    print('prescribed orders',runs,'cordial prefixes',prefixes)

    def quotient(qp,k):
        order = list(range(1,len(qp)))
        assert len(set(order)-set(qp))<=tip_bound
        return extend(qp,[0],order,k,search)
    lifted = Counter()
    # Subdivide random skeleton edges, preserving the leaves. Vary the
    # parities to exercise distinct matching deficiencies at doubled modulus.
    for leaves in range(2,tip_bound+2):
        for n in range(42,125):
            p = [-1]+[0]*leaves
            while len(p)<n:
                v = rng.randrange(1,len(p))
                p.append(p[v])
                p[v] = len(p)-1
            queue = [0]
            for v in queue:
                queue.extend(w for w,u in enumerate(p) if u==v)
            index = {v:i for i,v in enumerate(queue)}
            tree = [-1]+[index[p[v]] for v in queue[1:]]
            d = n-2*maximum(tree)
            r = ((n+d)//2-1)%27+1
            if d<=r:
                row = match_and_lift(tree,27,ordered_quotient=quotient)
                check_histograms(row,list(enumerate(tree))[1:],54)
                lifted[d] += 1
    if tip_bound==6:
        # Seven odd arms force deficiency six. Their 64 vertices give r=8.
        tree = [-1]
        for arm in range(7):
            start = len(tree)
            tree.extend([0,*range(start,start+8)])
        assert len(tree)==64 and len(tree)-2*maximum(tree)==6
        row = match_and_lift(tree,27,ordered_quotient=quotient)
        check_histograms(row,list(enumerate(tree))[1:],54)
        lifted[6] += 1
    assert set(lifted)==set(range(tip_bound+1))
    print('54-label lifts by deficiency',sorted(lifted.items()))


if __name__=='__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('manifests',type=Path,nargs='*',help='successive manifests starting at four tips')
    cli.add_argument('--samples',nargs=2,metavar=('GENERATOR','VERIFIER'))
    cli.add_argument('--growth',metavar='LIBRARY')
    cli.add_argument('--tips',type=int,choices=(5,6),default=5,help='tip bound for sample replays')
    args = cli.parse_args()
    for h,path in enumerate(args.manifests,4):
        manifest(path,h)
    if args.samples:
        if args.tips==6:
            six_tip_samples(*args.samples)
        else:
            samples(*args.samples)
    if args.growth:
        growth(args.growth,args.tips)

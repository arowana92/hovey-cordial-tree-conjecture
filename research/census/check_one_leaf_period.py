"""Check explicit labels, all opening edges and all relevant initial histograms."""
from collections import Counter
from math import gcd
from pathlib import Path
import sys


def graph(k,c):
    cycle = [(i,(i+1)%c) for i in range(c)]
    return cycle+[(0,c)]+[(v,v+1) for v in range(c,k-1)]


def connected(k,arcs):
    def visit(edges):
        seen = {0}
        while True:
            added = {b for a,b in edges if a in seen}-seen
            if not added:
                return len(seen)==k
            seen.update(added)
    return visit(arcs) and visit([(b,a) for a,b in arcs])


def verify(k,c,rows,units):
    edges = graph(k,c)
    arcs = [set() for _ in range(c)]
    colors = [set() for _ in range(c)]
    palette = set(range(k))
    zeros = set()
    records = []
    neutral = False
    boundary = set()
    for kind,x in rows:
        if kind==-4:
            cut,d,*x = x
        assert len(x)==k and set(x)<=palette
        weights = [(x[a]+x[b])%k for a,b in edges]
        counts = Counter(weights)
        if kind==-4:
            assert (k,c)==(6,3) and 0<=cut<c and 0<=d<k and set(x)==palette
            a,b = edges[cut]
            actual = weights[:cut]+weights[cut+1:]+[x[a],(d+x[b])%k]
            assert sorted(actual)==sorted([*range(k),d])
            boundary.add((cut,d))
            records.append((kind,x,(cut,d)))
        elif kind==-3:
            assert not k%2 and set(x)==palette and len(counts)==k
            neutral = True
            records.append((kind,x,None))
        elif kind==-2:
            assert k%2 and set(x)==palette and len(counts)==k-1
            dup, = (w for w in counts if counts[w]==2)
            gap, = palette-set(counts)
            for v in range(c):
                arcs[v].add(((dup-2*x[v])%k,(gap-2*x[v])%k))
            records.append((kind,x,(dup,gap)))
        else:
            assert k%2 and set(x)==palette-{0}
            if kind==-1:
                assert len(counts)==k
                for v in range(c):
                    colors[v].update(u*x[v]%k for u in units)
            else:
                assert 0<=kind<c
                a,b = edges[kind]
                actual = weights[:kind]+weights[kind+1:]+[x[a],x[b]]
                assert sorted(actual)==[0]+list(range(k))
                zeros.add(kind)
            records.append((kind,x,None))
    if k%2:
        assert zeros==set(range(c)) and all(row==palette-{0} for row in colors)
        # Expand on the actual residues. The generator works on gcd classes.
        strong = [connected(k,{(a*u%k,b*u%k) for a,b in row for u in units}) for row in arcs]
        assert all(strong[i] or strong[(i+1)%c] for i in range(c))
    else:
        assert neutral or len(boundary)==k*c
    return records


def old_tree(k,n,cut):
    if k%2 and n%k==1 and cut%3==1:
        x = [v%k for v in range(n)]
        edges = [(i,i+1) for i in range(n-1)]
        return x,edges,(cut*7+1)%(n-1)
    a = (n+cut)%k
    x = [a]+[(a+i)%k for i in range(1,n)]
    return x,[(0,i) for i in range(1,n)], k-1 if n%k==1 and cut%3==0 else cut%(n-1)


def find_labels(k,records,units,cut,opposite,old_bins,surplus):
    for kind,x,pair in records:
        if kind==-4:
            a,b = opposite[1][1],opposite[0][1]
            if pair==(cut,(b-a)%k):
                return [(z+a)%k for z in x]
            continue
        if kind>=0:
            if kind==cut and all(a==surplus for _,a in opposite):
                return [(z+surplus)%k for z in x]
            continue
        for v,a in opposite:
            if kind==-3:
                return [(z+a-x[v])%k for z in x]
            if kind==-1 and surplus is not None:
                for u in units:
                    if (u*x[v]+surplus)%k==a:
                        return [(u*z+surplus)%k for z in x]
            if kind==-2 and surplus is None:
                dup,gap = pair
                for u in units:
                    offset = a-u*x[v]
                    d,g = (dup*u+2*offset)%k,(gap*u+2*offset)%k
                    if old_bins[d]<old_bins[g]:
                        return [(u*z+offset)%k for z in x]
    raise AssertionError('no opening in replay')


def balanced(k,values):
    counts = Counter(values)
    return max(counts.get(v,0) for v in range(k))-min(counts.get(v,0) for v in range(k))<=1


def replay(k,c,records,units,cut,n):
    x,edges,old_edge = old_tree(k,n,cut)
    a,b = edges.pop(old_edge)
    weights = [(x[i]+x[j])%k for i,j in edges]+[(x[a]+x[b])%k]
    assert balanced(k,x) and balanced(k,weights)
    state = Counter(weights)
    surplus = Counter(x).most_common(1)[0][0] if n%k==1 else None
    piece = graph(k,c)
    left,right = piece.pop(cut)
    labels = find_labels(k,records,units,cut,[(left,x[b]),(right,x[a])],state,surplus)
    edges.extend((n+i,n+j) for i,j in piece)
    edges.extend([(a,n+left),(b,n+right)])
    x.extend(labels)
    assert len(edges)==len(x)-1
    assert balanced(k,x) and balanced(k,((x[i]+x[j])%k for i,j in edges))


def check(k,path):
    groups = {c:[] for c in range(3,k)}
    for line in path.read_text().splitlines():
        n,c,kind,*x = map(int,line.split())
        assert n==k
        groups[c].append((kind,x))
    units = [u for u in range(1,k) if gcd(k,u)==1]
    examples = openings = 0
    for c,rows in groups.items():
        records = verify(k,c,rows,units)
        for cut in range(c):
            replay(k,c,records,units,cut,k+1)
            replay(k,c,records,units,cut,k+((cut+c)%(k-1)+2))
            examples += 2
        openings += c
    print(k,len(groups),openings,sum(map(len,groups.values())),examples,flush=True)


if __name__=='__main__':
    for arg in sys.argv[1:]:
        path = Path(arg)
        with path.open() as source:
            k = int(source.readline().split()[0])
        check(k,path)

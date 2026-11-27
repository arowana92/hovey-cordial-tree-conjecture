"""Check the actual path order, vertex sets, endpoint sums and final core histograms."""

from collections import Counter
from itertools import product
from random import Random

from research.hub.prescribed_paths import bridge, integer_subdivision, modular_attachment


def check_path(p,q,w,L,F,k=None):
    path = bridge(p,q,w,L,F,modulus=k)
    sums = [a+b for a,b in zip([p,*path],[*path,q])]
    if k:
        sums = [s%k for s in sums]
        F = {v%k for v in F}
        w %= k
    assert len(path)==len(set(path))==L and not set(path) & F
    assert Counter(sums)==Counter([*path,w])


def check_subdivision(order, coarse, internal, final):
    # Trace each old edge through its private degree-two vertices.
    nodes = order
    expected = []
    for (u,v),length in zip(coarse,internal):
        path = [u,*range(nodes,nodes+length),v]
        expected.extend(zip(path,path[1:]))
        nodes += length
    assert expected == final
    return nodes


def integer_graph(order,E,internal,site):
    f,actual = integer_subdivision(order,E,internal,site)
    n = check_subdivision(order,E,internal,actual)
    assert f[site]==0 and len(f)==len(set(f))==n
    W = sorted(f[a]+f[b] for a,b in actual)
    tree = len(E)==order-1
    assert W==sorted(f)[int(tree):]
    lo,hi = min(f),max(f)
    assert hi-lo<=828*n
    # Fill each missing integer at the actual labeled site.
    slots = set(f)
    for v in range(lo,hi+1):
        if v not in slots:
            actual.append((site,len(f)))
            f.append(v)
    assert sorted(f)==list(range(lo,hi+1))
    assert sorted(f[a]+f[b] for a,b in actual)==list(range(lo+int(tree),hi+1))


def main():
    rng = Random(8119)
    count = trees = modular = 0
    for length in range(76,115):
        for p,q in product((0,1,-1),(0,2)):
            F = set(range(-12,13))
            check_path(p,q,0,length,F)
            count += 1
    for k in (72072,99991,131072):
        for p,q in ((0,0),(0,k//2),(k//2,k//2),(k//3,k//4),(1,k-1)):
            for w in (0,k//2,rng.randrange(k)):
                F = {rng.randrange(k) for _ in range(120)} | {p,q,w}
                check_path(p,q,w,rng.randrange(76,155),F,k)
                count += 1
    for order in range(2,8):
        edges = [(rng.randrange(i),i) for i in range(1,order)]
        for site in (0,order-1):
            for extra in ([],[(site,site)], [edges[0]]):
                E = edges+extra
                integer_graph(order,E,[rng.randrange(76,97) for _ in E],site)
                trees += 1
    E = [(0,1),(0,2)]
    internal = [76,79]
    base = 2+sum(internal)
    k = 65536
    for old,joint,site in [([17,91,17],0,1),([17,0,1],1,1),([31,7,44],2,0)]:
        for leaves,deficit in [(0,0),(6,k//2),(k-base,41),(k-base,None),(k-base+2,14)]:
            f,actual = modular_attachment(old,E,internal,joint,site,leaves,k,deficit)
            assert f[:3] == old
            check_subdivision(3,E,internal,actual[:sum(internal)+2])
            assert actual[base:] == [(site,i) for i in range(base+1,len(f))]
            V = Counter(x for i,x in enumerate(f) if i!=joint)
            W = Counter((f[a]+f[b])%k for a,b in actual)
            if deficit is None:
                assert V==W==Counter(range(k))
            else:
                W[deficit] -= 1
                assert max(V[i] for i in range(k))-min(V[i] for i in range(k))<=1
                assert max(W[i] for i in range(k))-min(W[i] for i in range(k))<=1
            modular += 1
    print(f"{count} two-ended paths, {trees} completed integer graphs, "
          f"{modular} whole modular attachments.")


if __name__=='__main__':
    main()

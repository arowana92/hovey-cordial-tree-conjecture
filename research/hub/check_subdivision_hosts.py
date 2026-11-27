"""Check incidence, integer sums, completion and interval bounds independently."""

from random import Random

from research.hub.subdivision_hosts import anchored_tree, graph_host, high_bridge


def check(order,E,lengths,f,actual,site,high=None,charge=None,M=None):
    n = order
    edges = []
    for (u,v),L in zip(E,lengths):
        path = [u,*range(n,n+L),v]
        n += L
        edges.extend(zip(path,path[1:]))
    assert edges==actual and len(f)==len(set(f))==n and f[site]==0
    expanded = [0]*len(edges) if charge is None else [
        x for L,b in zip(lengths,charge) for x in ([0]*(L+1) if L else [b])]
    weights = sorted(f[u]+f[v]+b for (u,v),b in zip(edges,expanded))
    assert len(set(weights))==len(weights)
    if high is None:
        assert weights==sorted(f)[1:]
        high = max(f)
        assert high-min(f)<=23*(36*n if M is None else M)
        first = min(f)+1
        excess = 0
    else:
        excess = len(E)-order
        assert weights==sorted(f)+list(range(high+1,high+1+excess))
        assert max(f)<=high and high-min(f)<=12312*n
        first = min(f)
    # Every hole is filled at the actual site. Verify closing both intervals
    # without materializing millions of separate padding edges.
    missing = set(range(min(f),high+1))-set(f)
    assert all(f[site]+x==x for x in missing)
    assert set(weights) | missing == set(range(first,high+1+excess))
    assert not set(weights) & missing


def main():
    rng = Random(1991)
    count = dense = 0
    for h in range(2,13):
        edges = [(rng.randrange(i),i) for i in range(1,h)]
        for site in (0,h-1):
            j = rng.randrange(h-1)
            lengths = [0]*(h-1)
            lengths[j] = 77*h-1
            f,actual = anchored_tree(h,edges,lengths,site)
            check(h,edges,lengths,f,actual,site)
            count += 1
            lengths = [153 if i%2 else 230 for i in range(h-1)]
            f,actual = anchored_tree(h,edges,lengths,site)
            check(h,edges,lengths,f,actual,site)
            count += 1
    charged = 0
    E = [(0,1),(0,2),(1,3),(3,4)]
    L = [0,384,0,0]
    for b in (-100000,0,100000):
        charge = [b,0,b-3,-7]
        for initial in (None,[-8,1,3,0,24]):
            f,actual = anchored_tree(5,E,L,3,charge,initial)
            M = max(36*len(f), *(abs(x) for x in f[:5]),
                    *(abs(f[u]+f[v]+c) for (u,v),l,c in zip(E,L,charge) if l==0))
            check(5,E,L,f,actual,3,charge=charge,M=M)
            if initial is not None:
                assert f[:5]==initial
            charged += 1
    for L in range(92,110):
        M = 36*(L+4)
        for p,q in ((0,0),(0,2),(2,0),(1,2)):
            w = 160*M+(L%9)+1
            rows = high_bridge(p,q,w,L,{0,1,2},M)
            path = [p,*rows,q]
            assert sorted(a+b for a,b in zip(path,path[1:]))==sorted(rows+[w])
            assert len(set(rows))==len(rows)==L and not set(rows)&{0,1,2}
            assert -182*M<=min(rows)<=max(rows)<160*M
    for h in range(1,6):
        E = [(rng.randrange(i),i) for i in range(1,h)]
        E += [(0,0),(0,0),(rng.randrange(h),rng.randrange(h))]
        # Interior sizes at both the representability threshold and later residues.
        L = [rng.randrange(92,116) for _ in E]
        f,actual,high = graph_host(h,E,L,h-1)
        check(h,E,L,f,actual,h-1,high)
        dense += 1
    print(f"{count} partially subdivided trees, {charged} prescribed-offset trees, 72 exterior target bridges, {dense} multigraphs.")


if __name__=='__main__':
    main()

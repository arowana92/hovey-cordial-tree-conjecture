"""Check actual induced subtrees, integer labelings and each transition bound."""

from collections import Counter
from random import Random

from research.census.level_hosts import host, original
from research.rainbow.verify import rooted_shapes


def verify(children,extra=True):
    n = len(children)
    given = {(u,v) for u,row in enumerate(children) for v in row}
    levels = [[0]]
    while row := [v for u in levels[-1] for v in children[u]]:
        levels.append(row)
    h = len(levels)-1
    cutoff = n
    for i in range(1,h):
        p = [j for j,u in enumerate(levels[i-1]) if children[u]]
        q = [j for j,u in enumerate(levels[i]) if children[u]]
        cut = len(levels[i])-1-(len(levels[i-1])-1-max(p))-min(q)
        cutoff += max(cut,0)
    restricted = original(children)
    labels = restricted.labels()
    weight = [labels[u]+labels[v] for u,v in given]
    assert len(set(x%cutoff for x in labels))==n
    assert len(set(x%cutoff for x in weight))==n-1
    assert max(labels)+1==cutoff
    sizes = []
    for compress in (False,True):
        tree = host(children,compress)
        N = len(tree.side)
        assert len(tree.edges)==N-1 and tree.rank[0]==0
        assert set((u,v) for u,v in tree.edges if u<n and v<n)==given
        adj = [[] for _ in range(N)]
        for u,v in tree.edges:
            adj[u].append(v)
            adj[v].append(u)
        reached = {0}
        queue = [0]
        for u in queue:
            for v in adj[u]:
                if v not in reached:
                    queue.append(v)
                    reached.add(v)
        assert len(reached)==N
        assert all(tree.side[u]!=tree.side[v] for u,v in tree.edges)
        assert sorted(tree.labels())==list(range(N))
        sums = [tree.rank[v]+tree.rank[u] for u,v in tree.edges]
        assert sorted(sums)==list(range(N-1))
        if extra:
            for k in (2,8,16,25,N+3):
                x = tree.labels()
                for values in (x,[x[u]+x[v] for u,v in tree.edges]):
                    counts = Counter(v%k for v in values)
                    assert max(counts[i] for i in range(k))-min(counts[i] for i in range(k))<=1
        sizes.append(N)
    assert sizes[1]<=sizes[0]
    if h:
        last_children = len(children[levels[-2][-1]])
        assert sizes[0]<=2*n-h-last_children
    return cutoff,sizes[0],sizes[1]


def spine_children(par, route, rng):
    adj = [[] for _ in par]
    for v,u in enumerate(par[1:],1):
        adj[u].append(v)
        adj[v].append(u)
    order = [route[0]]
    parent = {route[0]:-1}
    succ = dict(zip(route,route[1:]))
    kids = []
    for v in order:
        row = [u for u in adj[v] if u!=parent[v]]
        rng.shuffle(row)
        if v in succ:
            row.sort(key=lambda u: 1 if u==succ[v] else 0 if len(adj[u])==1 else 2)
        kids.append(row)
        order.extend(row)
        parent.update((u,v) for u in row)
    index = {v:j for j,v in enumerate(order)}
    return [[index[u] for u in row] for row in kids]


def main():
    rng = Random(1991)
    total = improved = spine = 0
    for n in range(2,12):
        for par in rooted_shapes(n).values():
            children = [[] for _ in par]
            for v,u in enumerate(par[1:],1):
                children[u].append(v)
            for row in children:
                rng.shuffle(row)
            cutoff,plain,short = verify(children)
            total += 1
            improved += short<plain
            tips = [v for v,row in enumerate(children) if not row]
            if len(children[0])==1:
                tips.append(0)
            a,b = rng.sample(tips,2)
            def ancestors(v):
                trace = []
                while v>=0:
                    trace.append(v)
                    v=par[v]
                return trace
            first,second = ancestors(a),ancestors(b)
            common = next(v for v in first if v in second)
            path = first[:first.index(common)+1]+list(reversed(second[:second.index(common)]))
            support = set(path)
            for leaf in tips:
                if leaf not in support and (par[leaf] in path or leaf==0 and children[0][0] in path):
                    support.add(leaf)
            oriented = spine_children(par,path,rng)
            k,_,_ = verify(oriented,False)
            assert k<=2*n-len(support)
            spine += 1
    print(f"rooted trees={total}, smaller compressed hosts={improved}, prescribed spines={spine}")


if __name__ == "__main__":
    main()

"""Compare the symbolic prefix catalog with separately compressed ordinary prefixes."""

from collections import Counter
from random import Random
from research.hub.branches import children_of
from research.hub.prefix_moduli import collision_product, prefix_catalog
from research.hub.universal_hub import construct
from research.rainbow.verify import rooted_shapes


def code(tree):
    kids = children_of(tree)
    enc = ['']*len(tree)
    for i in reversed(range(len(tree))):
        enc[i] = '('+''.join(sorted(enc[v] for v in kids[i]))+')'
    return enc[0]


def replay(tree):
    kids = children_of(tree)
    marks = {0,*[i for i in range(len(tree)) if len(kids[i])!=1]}
    order = []
    stack = [0]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(reversed(kids[v]))
    result = set()
    living = set()
    for v in order:
        living.add(v)
        retained = {0}
        for top in (marks & living):
            for u in kids[top]:
                if u not in living:
                    continue
                chain = [u]
                while u not in marks and kids[u][0] in living:
                    u, = kids[u]
                    chain.append(u)
                while len(chain)>14:
                    del chain[1:13]
                retained.update(chain)
        ids = sorted(retained)
        index = {v:i for i,v in enumerate(ids)}
        small = [-1]
        for u in ids[1:]:
            p = tree[u]
            while p not in retained:
                p = tree[p]
            small.append(index[p])
        result.add(code(small))
    return result


def check(tree,compare=True):
    catalog = list(prefix_catalog(tree))
    kids = children_of(tree)
    tips = sum(not group for group in kids[1:])
    assert len(catalog)<=28*tips+1
    if compare:
        assert {code(c) for c in catalog} == replay(tree)
    for core in catalog:
        x,gap,_ = construct(core)
        depth = [0]*len(core)
        for i,p in enumerate(core[1:],1):
            depth[i] = 1+depth[p]
        assert max(x)-min(x)<=8*(1+len(core))**(max(depth)+4)
        assert len(core)<=28*tips+1 and len(set(x))==len(core) and x[0]==0
        assert Counter(x)==Counter([gap]+[x[i]+x[p] for i,p in enumerate(core) if i])
    return len(catalog)


if __name__=='__main__':
    shapes = catalogs = prime_checks = 0
    for n in range(1,10):
        for tree in rooted_shapes(n).values():
            catalogs += check(tree)
            shapes += 1
            if n<=7:
                value = collision_product(tree)
                for k in range(2,72):
                    if value%k:
                        for core in prefix_catalog(tree):
                            x,_,_=construct(core)
                            assert len({u%k for u in x})==len(x)
                        prime_checks += 1
    rng = Random(508882)
    for _ in range(64):
        tree = [-1]
        for j in range(rng.randrange(1,7)):
            p = rng.randrange(len(tree))
            for _ in range(rng.randrange(5,53)):
                tree.append(p)
                p = len(tree)-1
        catalogs += check(tree)
    print(f"{shapes} rooted shapes and 64 subdivided trees; {catalogs} compressed prefixes, "
          f"{prime_checks} sufficient modular divisibility checks.")

"""Exhaust actual trees and labelings, recording every compatible cover prescription."""
from itertools import combinations, product
from .cover_pins import complete
from .few_leaf_rings import trees


def check(k,n,parent):
    edges = list(enumerate(parent[1:],1))
    degree = [0]*n
    for u,v in edges:
        degree[u] += 1
        degree[v] += 1
    cases = 0
    def balanced(xs):
        bins = [xs.count(i) for i in range(k)]
        return max(bins)-min(bins)<=1
    rows = []
    for row in product(range(k),repeat=n):
        weights = [(row[u]+row[v])%k for u,v in edges]
        if not (balanced(row) and balanced(weights)): continue
        zero = {v for v in range(n) if row[v]==0}
        outside = len([1 for u,v in edges if u not in zero and v not in zero])
        inverse = len([1 for u,v in edges if u not in zero and v not in zero and (row[u]+row[v])%k==0])
        assert sum(degree[v]-1 for v in range(n) if v not in zero)<=outside+inverse
        rows.append(row)
    for mask in range(1,1<<n):
        cover = {i for i in range(n) if mask>>i&1}
        if any(u not in cover and v not in cover for u,v in edges): continue
        available = [row for row in rows if all(row[v]==0 for v in cover)]
        subsets = [()]+[(i,) for i in range(n)]
        subsets += list(combinations((v for v in range(n) if v not in cover),2))
        for places in subsets:
            allowed = {tuple(row[i] for i in places) for row in available}
            for xs in product(range(k),repeat=len(places)):
                pins = dict(zip(places,xs))
                row = complete(k,n,edges,cover,0,pins)
                assert (row is not None)==(xs in allowed)
                if row is not None:
                    assert all(row[v]==0 for v in cover) and all(row[v]==x for v,x in pins.items())
                    assert balanced(row) and balanced([(row[u]+row[v])%k for u,v in edges])
                cases += 1
    return cases


if __name__ == '__main__':
    total = 0
    for n in range(1,7):
        for tips in range(1,n+1):
            for word in trees(n,tips):
                stack,parent = [],[]
                for c in word:
                    if c=='(':
                        parent.append(stack[-1] if stack else -1)
                        stack.append(len(parent)-1)
                    else: stack.pop()
                for k in (2,3,4):
                    total += check(k,n,parent)
    print(total,"partial labelings on marked covers")

"""Build actual odd-modulus tree joins, including transfers from padded leaves."""
from collections import Counter


def staircase(k, low):
    x,y = 0,low
    edges = [(x,y)]
    for _ in range(low-1):
        x += 1
        edges.append((x,y))
    for _ in range(k-low-1):
        y += 1
        edges.append((x,y))
    assert {x+y for x,y in edges} == set(range(low,low+k-1))
    return edges


def replay(k, edges, root, singles, padding, b):
    # The old star, labeled by its vertex IDs, has edge deficit zero.
    designated = singles[0]
    removed = set(singles[-padding:]) if padding else set()
    for unit in (1,-1):
        colors = [((x-root)*unit+b)%k for x in range(k)]
        hits = [(x,y) for x,y in edges if (colors[x]+colors[y])%k==0]
        if 2*b%k==0 or hits:
            break
    moved = False
    if 2*b%k==0:
        colors[designated] = b
    else:
        (x,y), = hits
        if x in removed or y in removed:
            spare = x if x in removed else y
            colors[spare],colors[designated] = colors[designated],colors[spare]
            moved = True
    vertex = list(range(k))
    ids = {root:b}
    joins = [(0,i) for i in range(1,k)]
    for x in range(k):
        if x!=root and x not in removed:
            ids[x] = len(vertex)
            vertex.append(colors[x])
    joins.extend((ids[x],ids[y]) for x,y in edges if x not in removed and y not in removed)
    assert len(vertex)==2*k-1-padding and len(joins)==len(vertex)-1
    for hist in (Counter(vertex),Counter((vertex[x]+vertex[y])%k for x,y in joins)):
        counts = [hist[z] for z in range(k)]
        assert max(counts)-min(counts)<=1
    return moved


if __name__ == '__main__':
    checked = transfers = equal = 0
    for k in range(3,36,2):
        for low in {1,k//2,k-1}:
            edges = staircase(k,low)
            degrees = Counter(v for link in edges for v in link)
            for root in range(k):
                singles = [v for edge in edges if root in edge for v in edge
                           if v!=root and degrees[v]==1]
                for padding in range(len(singles)):
                    for b in range(k):
                        transfers += replay(k,edges,root,singles,padding,b)
                        equal += b==0
                        checked += 1
    assert transfers and equal
    print('whole-tree joins',checked,'equal-deficit cases',equal,'padded-leaf transfers',transfers)

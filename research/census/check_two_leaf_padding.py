"""Recount cycles, all normalized small inputs and actual subdivided trees."""
from collections import Counter,defaultdict
from itertools import combinations_with_replacement,permutations
from math import gcd
from pathlib import Path
from random import Random

from .two_leaf_padding import padded_tree,two_leaves


def local(k,a,b,p,q,x,y,row):
    assert sorted([x,y]+row)==list(range(k))
    chain = [a]+row+[b]
    weights = Counter((u+v)%k for u,v in zip(chain,chain[1:]))
    weights[(x+p)%k] += 1
    weights[(y+q)%k] += 1
    weights[(a+b)%k] -= 1
    return all(weights[i]==1 for i in range(k))


def certificate():
    pairs = defaultdict(list)
    for line in Path(__file__).with_name("two-leaf-cycles.txt").read_text().splitlines():
        k,h,x,y,*row = map(int,line.split())
        assert sorted([x,y]+row)==list(range(k))
        weights = [x,(y+h)%k]+[(u+v)%k for u,v in zip(row,row[1:]+row[:1])]
        assert sorted(weights)==list(range(k))
        pairs[k,h].append({x,y})
    expected = {(k,gcd(k,h)%k) for k in range(10,65,2) for h in range(k)}
    assert pairs.keys()==expected
    assert all(len(rows)==2 and rows[0].isdisjoint(rows[1]) for rows in pairs.values())
    return 2*len(pairs)


def small(k):
    bad = set()
    for h in range(k):
        for a,b in combinations_with_replacement(range(k),2):
            # The leaf residue sum follows by subtracting the two first moments.
            for x in range(k):
                y = (h+k*(k-1)//2-x)%k
                if x==y:
                    continue
                rest = set(range(k))-{x,y}
                if any(local(k,a,b,0,h,x,y,list(row)) for row in permutations(rest)):
                    break
            else:
                bad.add((h,a,b))
    return bad


def tree(k,edges,chosen,extra):
    f,row = padded_tree(k,edges,chosen,extra)
    assert len(row)==extra
    a,b = edges[chosen]
    chain = [f[a]]+row+[f[b]]
    weights = [(f[u]+f[v])%k for i,(u,v) in enumerate(edges) if i!=chosen]
    weights += [(u+v)%k for u,v in zip(chain,chain[1:])]
    for values in (f+row,weights):
        freq = Counter(values)
        bins = [freq[x] for x in range(k)]
        assert max(bins)-min(bins)<=1


def main():
    rng = Random(28112612)
    cert = certificate()
    assert not small(5)
    assert small(6)=={(0,2,2),(0,4,4)}
    assert small(8)=={(4,0,4),(4,1,3),(4,2,2),(4,5,7),(4,6,6)}
    assignments = trees = 0
    for k in list(range(5,65))+[65,75,81,105,125,143,169,243,315]:
        if k in (6,8):
            continue
        # Sweep the difference and one anchor; random translations also test
        # the other endpoint and both actual parent labels.
        for h in range(k):
            for anchor in (range(k) if k<=65 else range(0,k,max(1,k//12))):
                p,b = rng.randrange(k),rng.randrange(k)
                q = (p+h)%k
                a = (p+anchor)%k
                assert local(k,a,b,p,q,*two_leaves(k,a,b,p,q))
                assignments += 1
        for _ in range(10):
            n = rng.randrange(2,37)
            edges = [(j,rng.randrange(j)) for j in range(1,n)]
            tree(k,edges,rng.randrange(n-1),(k-2)*((n-2)//2)+rng.randrange(4))
            trees += 1
    print('cycle witnesses',cert,'packet assignments',assignments,'whole trees',trees,
          'normalized exceptions at six and eight',2,5)


if __name__=='__main__':
    main()

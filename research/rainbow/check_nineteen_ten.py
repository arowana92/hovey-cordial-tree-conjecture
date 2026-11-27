"""Check every two-tip prefix that can leave a failed double-star suffix."""
from functools import lru_cache
from itertools import permutations,product

from .generate import forests,leaf_count,parent_vector
from research.eight.verify import components


def weight(x,p,f):
    return (x+(f[p] if p>=0 else -1-p))%10


def prefixes(ps):
    f = [0]*9
    def visit(i,free,used):
        if i==9:
            missing = (1023^used).bit_length()-1
            yield tuple(f),missing
            return
        p = ps[i]
        choices = free
        while choices:
            bit = choices & -choices
            choices -= bit
            a = bit.bit_length()-1
            w = 1<<weight(a,p,f)
            if not w&used:
                f[i] = a
                yield from visit(i+1,free-bit,used|w)
    yield from visit(0,1022,0)


@lru_cache(None)
def tail_labels(left,right,deficit):
    for a,b,z in permutations(range(10),3):
        tips = [x for x in range(10) if x not in (a,b,z)]
        add = [(a+left)%10]+[(a+x)%10 for x in tips]+[(b+right)%10,(b+z)%10]
        bins = [add.count(i)+int(i!=deficit) for i in range(10)]
        if max(bins)-min(bins)<=1:
            return [a]+tips+[b,z]
    return None


def check_join(f,g,p,r,ps):
    # Realize every boundary color at a leaf of an actual 11-vertex star.
    labels = [0]+list(range(10))+list(f)+g
    new_parents = ps+[p]+[9]*7+[r,17]
    parents = [0]*10+[11+j if j>=0 else -j for j in new_parents]
    vertices = [0]*10
    edges = [0]*10
    for i,x in enumerate(labels):
        vertices[x] += 1
        if i:
            edges[(x+labels[parents[i-1]])%10] += 1
    assert vertices==[3]*10 and sorted(edges)==[2]+[3]*9


def check():
    shapes = cases = lifts = joins = 0
    catalog = set()
    for forest in forests(9):
        if sum(leaf_count(t) for t in forest)>2:
            continue
        shapes += 1
        for colors in product(range(10),repeat=len(forest)):
            ps = parent_vector(forest,colors)
            signature = tuple(sorted(components(ps)))
            assert signature not in catalog
            catalog.add(signature)
            cases += 1
            choices = prefixes(ps)
            f,missing = next(choices)
            assert sorted(f)==list(range(1,10))
            assert {weight(x,p,f) for x,p in zip(f,ps)}==set(range(10))-{missing}
            pending = []
            for p,r in product(range(-10,9),repeat=2):
                left = f[p] if p>=0 else -1-p
                right = f[r] if r>=0 else -1-r
                tail = tail_labels(left,right,missing)
                if tail is None:
                    assert 2*left%10==missing and right==(left+5)%10
                    pending.append((p,r))
                else:
                    check_join(f,tail,p,r,ps)
                    joins += 1
            lifts += len(pending)
            for g,d in choices:
                if not pending:
                    break
                for p,r in pending.copy():
                    left = g[p] if p>=0 else -1-p
                    right = g[r] if r>=0 else -1-r
                    tail = tail_labels(left,right,d)
                    if tail is not None:
                        check_join(g,tail,p,r,ps)
                        pending.remove((p,r))
                        joins += 1
            assert not pending
    # One chain, forks with positive trunk and unordered positive arms,
    # and two chains of unequal positive lengths summing to nine.
    forks = sum((9-trunk)//2 for trunk in range(1,8))
    assert shapes==1+forks+4 and cases==10*(1+forks)+400
    assert joins==cases*19**2 and lifts==2544
    print('two-tip shapes',shapes,'boundary cases',cases,'whole trees',joins,
          'alternate prefix witnesses',lifts)


if __name__=='__main__':
    check()

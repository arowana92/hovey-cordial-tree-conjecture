"""Construct short star attachments and recount their actual endpoint weights."""
from itertools import product
from random import Random

from .star_period import pinned_sources


def equal_singletons(k, children, singles, entering, common):
    """The surplus is zero. All child edges are ordinary."""
    if common:
        center = common
        blocked = {0, center, entering}
        leaves = [x for x in range(k) if x not in blocked][:children+singles]
        return [center]+leaves
    center = 1
    child = {k-i for i in range(1,children+1)}
    if entering in child:
        child.remove(entering)
        child.add(k-children-1)
        spare = entering
    else:
        spare = (entering+1)%k
    available = sorted(set(range(k))-child-{0,center,spare})
    return [center]+sorted(child)+available[:singles]


def reserve(k, effective, center):
    """Pin the center in row zero and move zero to a dummy of the same shift."""
    shifts = sorted(set(effective[1:]))
    assert center and len(effective)+len(shifts)<k
    padded = effective+shifts+[0]*(k-1-len(effective)-len(shifts))
    padded.append(-sum(padded)%k)
    labels = pinned_sources(padded,0,center)
    at = labels.index(0)
    if at < len(effective):
        dummy = len(effective)+shifts.index(effective[at])
        labels[at],labels[dummy] = labels[dummy],labels[at]
    return labels[:len(effective)]


def replay(k,labels,j,entering,singleton_colors,offsets):
    # The old star has surplus zero and represents each prescribed parent color.
    old = [0]+list(range(k))
    vertices = old+labels
    edges = [(0,i,0) for i in range(1,k+1)]
    start = len(old)
    edges.append((1+entering,start,0))
    edges.extend((start,start+1+i,offset) for i,offset in enumerate(offsets))
    edges.extend((1+b,start+1+j+i,0) for i,b in enumerate(singleton_colors))
    assert len(edges)+1==len(vertices)
    assert len(labels)==1+j+len(singleton_colors)
    bins = [0]*k
    weights = [0]*k
    for x in vertices:
        bins[x] += 1
    for u,v,b in edges:
        weights[(vertices[u]+vertices[v]+b)%k] += 1
    assert max(bins)-min(bins)<=1 and max(weights)-min(weights)<=1


def main():
    common = many = 0
    for k in range(3,23):
        for j in range(k-2):
            single = k-3-j
            for a,b in product(range(k),repeat=2):
                labels = equal_singletons(k,j,single,a,b)
                replay(k,labels,j,a,[b]*single,[0]*j)
                common += 1
    rng = Random(271123)
    for k in range(4,61):
        for n in range(1,k-1):
            d = k-n
            for j in {0,n//2,n-1}:
                x = rng.randrange(1,k)
                pool = rng.sample(range(k),min(n,d-1))
                actual = [rng.choice(pool) for _ in range(n-1)]
                entering = rng.randrange(k)
                effective = [entering]+actual
                labels = reserve(k,effective,x)
                replay(k,labels,j,entering,actual[j:],[(b-x)%k for b in actual[:j]])
                many += 1
    print('equal-parent whole trees',common,'varied effective shifts',many)


if __name__=='__main__':
    main()

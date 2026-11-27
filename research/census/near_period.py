"""Reduce a prescribed forest and a complementary subdivision to a dense rainbow path."""
from itertools import product
from random import Random


def forest_edges(k,parents,shifts,f):
    return [(f[i]+b+(f[p] if p>=0 else 0))%k for i,(p,b) in enumerate(zip(parents,shifts))]


def choose_forest(k,parents,shifts,a,b,old_weight):
    """Return admissible labels, or None in the algebraically impossible cases.

    External shifts include their parent label. Internal shifts are edge offsets.
    The replacement path uses ordinary sums. The proof applies for large k and
    h+2 <= sqrt(k); the enumeration fallback also permits small experimental cases.
    """
    h = len(parents)
    if len(shifts)!=h or any(p>=i for i,p in enumerate(parents)):
        raise ValueError("need parent-before-child rows")
    target = (k*(k-1)//2+a+b-old_weight+sum(shifts))%k
    if not h:
        return [] if target==0 else None
    coefficient = [1]*h
    for p in parents:
        if p>=0:
            coefficient[p] -= 1
    pivot = next(i for i in range(h) if i not in parents)
    free = [i for i in range(h) if i!=pivot]
    if h==2 and parents[1]==0 and (target+shifts[1]-shifts[0])%k==0:
        root = (old_weight-shifts[0])%k
        return [root,target] if root!=target else None

    def candidate(word):
        f = [0]*h
        for i,x in zip(free,word):
            f[i] = x
        f[pivot] = (target-sum(c*x for c,x in zip(coefficient,f)))%k
        if len(set(f))==h and len(set(forest_edges(k,parents,shifts,f)))==h:
            return f
        return None

    rng = Random(97631)
    for _ in range(100):
        f = candidate([rng.randrange(k) for _ in free])
        if f is not None:
            return f
    return next((f for word in product(range(k),repeat=h-1)
                 if (f:=candidate(word)) is not None),None)


def path_request(k,vertices,counts,a,b):
    """Reserve the endpoint edges and a repeated weight, then return a simple path request."""
    repeated = [x for x,n in enumerate(counts) if n==2]
    if min(counts)<0 or max(counts)>2 or len(repeated)>1 or sum(counts)!=len(vertices)+1:
        raise ValueError("incompatible weight multiplicities")
    for u in sorted(vertices):
        first = (a+u)%k
        if counts[first]!=1:
            continue
        prefix = [u]
        if repeated:
            v = (repeated[0]-u)%k
            if v==u or v not in vertices:
                continue
            prefix.append(v)
        else:
            v = u
        for w in sorted(vertices-set(prefix)):
            last = (w+b)%k
            if counts[last]!=1 or last==first:
                continue
            internals = vertices-set(prefix)-{w}
            colors = {i for i,z in enumerate(counts) if z}-{first,last}
            assert len(colors)==len(internals)+1
            assert sum(colors)%k==(v+w+2*sum(internals))%k
            return prefix[:-1],v,w,internals,colors
    raise ValueError("insufficient room for endpoint edges")


def prepare(k,parents,shifts,a,b,old_weight):
    f = choose_forest(k,parents,shifts,a,b,old_weight)
    if f is None:
        return None
    counts = [1+int(i==old_weight) for i in range(k)]
    for w in forest_edges(k,parents,shifts,f):
        counts[w] -= 1
    return f,path_request(k,set(range(k))-set(f),counts,a,b)


def pendant_request(k,vertex_high,edge_high,parent,tip):
    """Complete an early-residue core up to divisible order with a chosen path tip."""
    r = len(vertex_high)
    if not (0<r<k and len(edge_high)==r-1):
        raise ValueError("need compatible old high sets")
    all_sites = set(range(k))
    available = all_sites-vertex_high
    colors = all_sites-edge_high
    missing = (tip+sum(colors)-parent-2*sum(available))%k
    if tip not in available or missing not in colors:
        return None
    colors.remove(missing)
    for first in sorted(available-{tip}):
        w = (parent+first)%k
        if w in colors:
            inside = available-{first,tip}
            remaining = colors-{w}
            assert len(remaining)==len(inside)+1
            assert sum(remaining)%k==(first+tip+2*sum(inside))%k
            return first,tip,inside,remaining,missing
    raise ValueError("no initial edge for the dense request")

"""Verify the partial embeddings and exhaust small exceptional fibers independently."""
from collections import Counter
from itertools import product
from random import Random

from check import adjacency
from partial_gap import build,forced_collision,valid
from check_excess import expression
from sparse_ports import particular


def fibers():
    # Enumerate actual fibers of the primitive moment, independently of the
    # affine forms used for testing conflicts at equal labels or weights.
    trials = 0
    rng = Random(7021991)
    for k in (12,15,16,21):
        for coeff in ((-1,),(2,1),(2,3),(-1,1,1),(-1,2,3),(1,2,3)):
            r = len(coeff)
            terms = dict(enumerate(coeff))
            strata = [[] for _ in range(k)]
            for xs in product(range(k),repeat=r):
                strata[sum(c*x for c,x in zip(coeff,xs))%k].append(xs)
            for y,region in enumerate(strata):
                sol = particular(k,terms,y)
                c = coeff[0]
                forms = {i:expression((i,c),constant=sol[i]) for i in range(1,r)}
                forms[0] = expression(*[(i,-coeff[i]) for i in range(1,r)],constant=sol[0])
                for _ in range(8):
                    # Compare two linear sums on distinct endpoints, allowing
                    # old labels to supply constant offsets.
                    a = sorted(rng.sample(range(r),rng.randrange(min(2,r)+1)))
                    b = sorted(rng.sample(range(r),rng.randrange(min(2,r)+1)))
                    shift = rng.randrange(k)
                    left = expression(*[(v,n) for i in a for v,n in forms[i].items()])
                    right = expression(*[(v,n) for i in b for v,n in forms[i].items()],constant=shift)
                    forced = all((sum(xs[i] for i in a)-sum(xs[i] for i in b)-shift)%k==0 for xs in region)
                    assert forced==forced_collision([left,right],k)
                    trials += 1
    return trials


def main():
    rng = Random(4491991)
    good = no = bad_local = 0
    for k in (504,625,729,1024,1440):
        path = [(v-1,v) for v in range(1,k)]
        binary = [((v-1)//2,v) for v in range(1,k)]
        trees = [path,binary,path[:-8]+[(3+i//2,k-8+i) for i in range(8)]]
        for edges in trees:
            adj = adjacency(k,edges)
            leaves = [v for v,row in enumerate(adj) if len(row)==1]
            if len(leaves)>k//4:
                sets = [rng.sample(range(k),i) for i in (1,8,17)]
            else:
                hubs = [v for v,row in enumerate(adj) if len(row)>2]
                sets = [leaves[:-i] if i else leaves[:] for i in (0,1,2)]
                sets += [leaves+hubs[:-i] if i else leaves+hubs for i in (0,1,2)]
            for selected in sets:
                selected = sorted(set(selected)|{k//2})
                pins = dict(zip(selected,rng.sample(range(k),len(selected))))
                for gap in {0,rng.randrange(k),(-sum(range(k))-sum((len(adj[v])-2)*x for v,x in pins.items()))%k}:
                    result = build(edges,pins,gap,rng)
                    if result is None:
                        if not valid(pins,edges,k,gap): bad_local += 1
                        else: no += 1
                        continue
                    assert all(result[v]==x for v,x in pins.items())
                    assert len(result)==len(set(result.values())) and valid(result,edges,k,gap)
                    assert (sum(result.values())-sum(range(k)))%k==0
                    assert (sum(len(adj[v])*x for v,x in result.items())-sum(range(k))+gap)%k==0
                    for d,n in Counter(map(len,adj)).items():
                        seen = sum(len(adj[v])==d for v in result)
                        assert seen==n or min(seen,n-seen)>=6
                    good += 1
    print('partial embedding targets',good,'arithmetic or forced obstructions',no,
          'invalid initial pins',bad_local,'literal affine-fiber comparisons',fibers())


if __name__=='__main__':
    main()

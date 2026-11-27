"""Recount all labels and actual edge sums in the two-ended leaf construction."""

from random import Random

from research.census.leaf_intervals import extend,tree_labels
from research.rainbow.verify import rooted_shapes


def audit(labels,weights,bound):
    for values in (labels,weights):
        assert len(set(values))==len(values)
        assert max(values,default=0)-min(values,default=0)<bound
        for k in range(bound,bound+5):
            assert len({x%k for x in values})==len(values)


def tree(n,edges):
    f = tree_labels(n,edges)
    assert len(f)==n
    degree = [0]*n
    for v,w in edges:
        degree[v] += 1
        degree[w] += 1
    h = sum(d>1 for d in degree)
    bound = max(1,n,n+h-1)
    audit(f,[f[v]+f[w] for v,w in edges],bound)


def main():
    small = large = prescribed = 0
    rng = Random(67423)
    tree(0,[])
    for n in range(1,13):
        for parents in rooted_shapes(n).values():
            edges = [(v,p) for v,p in enumerate(parents) if p>=0]
            tree(n,edges)
            small += 1
    for h in (1,2,5,15,70,150):
        for leaves in (1,3,11,60,500,2000):
            for distribution in range(3):
                edges = [(i,rng.randrange(i)) for i in range(1,h)]
                if distribution==0:
                    sites = [0]
                elif distribution==1:
                    sites = [0,h-1]
                else:
                    sites = list(range(h))
                edges.extend((h+i,rng.choice(sites)) for i in range(leaves))
                rename = list(range(h+leaves))
                rng.shuffle(rename)
                edges = [(rename[u],rename[v]) for u,v in edges]
                rng.shuffle(edges)
                tree(h+leaves,edges)
                large += 1
    for h in range(1,16):
        for _ in range(150):
            f = [0,*rng.sample(range(1,3*h+1),h-1)]
            # Force independently chosen, distinct old weights by actual edge offsets.
            core = [(u,rng.randrange(u)) for u in range(1,h)]
            old = rng.sample(range(-4*h,4*h+1),h-1)
            bias = [w-f[u]-f[v] for w,(u,v) in zip(old,core)]
            parents = rng.choices(range(h),k=rng.randrange(1,45))
            offsets = [rng.randrange(-4*h,4*h+1) for _ in parents]
            new,bound = extend(f,old,parents,offsets)
            weights = [f[u]+f[v]+b for (u,v),b in zip(core,bias)]
            weights.extend(x+f[p]+b for x,p,b in zip(new,parents,offsets))
            audit(f+new,weights,bound)
            prescribed += 1
    print(f"{small} rooted trees, {large} relabeled trees with growing leaf counts, "
          f"{prescribed} cores with independently prescribed edge weights and leaf offsets")


if __name__=="__main__":
    main()

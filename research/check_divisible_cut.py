"""Check actual edge cuts and prescribed-offset gluing on independently built trees."""

from random import Random

from research.rainbow.verify import rooted_shapes


def parameters(parents):
    n = len(parents)
    size = [1]*n
    degree = [0]*n
    for v in reversed(range(1,n)):
        u = parents[v]
        size[u] += size[v]
        degree[v] += 1
        degree[u] += 1
    return degree.count(1), [(a,n-a) for a in size[1:]]


def check_shapes():
    count = irreducible = 0
    for n in range(2,13):
        for parents in rooted_shapes(n).values():
            leaves,cuts = parameters(parents)
            for k in range(2,n+2):
                count += 1
                if all(a%k and b%k for a,b in cuts):
                    assert (n-1)//k <= leaves-2
                    irreducible += 1
    return count,irreducible


def sharp():
    count = 0
    for k in range(3,41):
        for leaves in range(2,k+2):
            deficits = [1]*leaves
            left = k+1-leaves
            for j in range(leaves):
                extra = min(left,k-2)
                deficits[j] += extra
                left -= extra
            assert not left
            parents = [-1]
            for d in deficits:
                parent = 0
                for _ in range(k-d):
                    parents.append(parent)
                    parent = len(parents)-1
            l,cuts = parameters(parents)
            assert l == leaves and len(parents) == k*(leaves-1)
            assert all(a%k and b%k for a,b in cuts)
            count += 1
    return count


def check_bridges():
    rng = Random(19521991)
    def labeled(n,k):
        labels = [i%k for i in range(n)]
        rng.shuffle(labels)
        weights = [i%k for i in range(n-1)]
        rng.shuffle(weights)
        edges = []
        for v,w in enumerate(weights,1):
            u = rng.randrange(v)
            edges.append((u,v,(w-labels[u]-labels[v])%k))
        return labels,edges
    def bins(values,k):
        counts = [0]*k
        for v in values:
            counts[v] += 1
        return counts
    def edge_bins(labels,edges,k):
        return bins(((labels[u]+labels[v]+b)%k for u,v,b in edges),k)
    for _ in range(2500):
        k = rng.randrange(2,75)
        q = rng.randrange(1,5)
        x,old = labeled(rng.randrange(1,3*k+1),k)
        y,new = labeled(k*q,k)
        original = list(x)
        n = len(x)
        i,j = rng.randrange(n),rng.randrange(len(y))
        bridge = rng.randrange(k)
        weights = edge_bins(y,new,k)
        deficit, = [v for v,h in enumerate(weights) if h==q-1]
        d = (x[i]+y[j]+bridge-deficit)%k
        edges = old+[(n+u,n+v,b) for u,v,b in new]+[(i,n+j,bridge)]
        labels = x+[(a+d)%k for a in y]
        assert labels[:n] == original
        assert bins(labels,k) == [q+h for h in bins(x,k)]
        assert edge_bins(labels,edges,k) == [q+h for h in edge_bins(x,old,k)]
    return 2500


if __name__=='__main__':
    total,irreducible = check_shapes()
    print(f'{total} tree/modulus checks with {irreducible} cut-irreducible instances')
    print(f'{sharp()} equality examples with every edge cut inspected')
    print(f'{check_bridges()} offset bridges checked by both histograms')

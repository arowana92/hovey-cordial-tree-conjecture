"""Recount the path construction at each residue and on explicitly labeled trees."""

from random import Random

from .surplus_path import core_path, divisible_path, full_path, rank_window


def histogram(values, k):
    bins = [0]*k
    for x in values:
        bins[x%k] += 1
    return bins


def check_ranks():
    cases = 0
    for n in range(5, 151):
        for h in range(1, (n+(1 if n%2 else -2))//6+1):
            for at in range((n+1)//2):
                ranks = rank_window(at,n-1-at,h)
                assert ranks[at] in (h-1,h)
                assert sorted(ranks[::2]) == list(range((n+1)//2))
                assert sorted(ranks[1::2]) == list(range(n//2))
                assert sorted(x+y for x,y in zip(ranks,ranks[1:])) == list(range(n-1))
                cases += 1
    return cases


def check_full():
    cases = 0
    for k in range(2, 74):
        for mark in range(k-1):
            for parent in range(k):
                labels = full_path(k,mark,parent)
                weights = [(x+y)%k for x,y in zip(labels,labels[1:])]
                weights.append((parent+labels[mark])%k)
                assert sorted(labels) == list(range(1,k))
                assert len(set(weights)) == k-1
                cases += 1
    return cases


def check_trees():
    rng = Random(199108)
    for _ in range(2600):
        k = rng.randint(1,150)
        a = rng.randrange(4*k)
        b = rng.randrange(4*k)
        if rng.randrange(2):
            a,b = b,a
        # A path core with consecutive vertex labels and consecutive edge sums.
        shift = rng.randrange(k)
        order = k+rng.randrange(2)
        labels = [(shift+i//2+(i%2)*((order+1)//2))%k for i in range(order)]
        edges = [(i-1,i) for i in range(1,order)]
        site = rng.randrange(order)
        core = tuple(labels)
        if order == k:
            used = {(labels[i]+labels[j])%k for i,j in edges}
            deficit, = set(range(k))-used
            added = divisible_path(k,a,b,labels[site],deficit)
        else:
            added = core_path(k,a,b,labels[site],shift)
        assert len(added) == a+b+1
        labels.extend(added)
        edges.append((site,order+a))
        edges.extend((v-1,v) for v in range(order+1,len(labels)))
        assert tuple(labels[:order]) == core
        for bins in (histogram(labels,k),histogram((labels[u]+labels[v] for u,v in edges),k)):
            assert max(bins)-min(bins) <= 1
    return 2600


if __name__ == '__main__':
    print(f"{check_ranks()} marked-rank witnesses checked")
    print(f"{check_full()} prescribed full blocks checked")
    print(f"{check_trees()} whole-tree extensions checked")

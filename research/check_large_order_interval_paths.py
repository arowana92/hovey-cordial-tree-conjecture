"""Audit short-jump budgets and actual edges before and after the final leaf extension."""

from collections import Counter
from random import Random

from research.large_order_gap_paths import leaf_batch
from research.large_order_interval_paths import interval_walks, seed


def counts(tree, x, k):
    v, e = [0]*k,[0]*k
    for i,z in enumerate(x):
        assert 0 <= z < k
        v[z] += 1
        if i:
            p = tree[i]
            assert 0 <= p < i
            e[(z+x[p]) % k] += 1
    return v,e


def check_walks(demands, r, rng, exact=False):
    width = r//2
    all_steps = sum(abs(a//width-b//width)+2 for a,b in demands)
    internal, jumps = Counter(),Counter()
    for (x,y),walk in zip(demands,interval_walks(demands,r,rng.randrange(10000),exact)):
        assert (walk[0],walk[-1])==(x,y)
        internal.update(walk[1:-1])
        mids = [v//width for v in walk[1:-1]]
        assert len(mids)==len(set(mids))==abs(y//width-x//width)+1
        change = Counter()
        for a,b in zip(walk,walk[1:]):
            assert abs(b-a)<r
            change[a] -= 1
            change[b] += 1
            jumps[b-a] += 1
        change[y] -= 1
        change[x] += 1
        assert not any(change.values())
    assert sum(jumps.values())==all_steps
    assert max(internal.values(),default=0)*width <= 2*len(demands)+12*width
    assert max(jumps.values(),default=0)*width <= 2*all_steps+12*width
    return all_steps


def full(k, tree, sites, bands, aux, depth, rng):
    tr,x,holders,(blocks,nroute) = seed(tree,k,bands,sites,aux,depth,rng.randrange(1<<25))
    v,e = counts(tr,x,k)
    assert len(set(e))==1 and v.count(e[0]+1)==1 and v.count(e[0])==k-1
    assert tr[:len(tree)]==tree and set(tr[len(tree):]) <= set(holders.values())
    used = Counter(tr[len(tree):])
    # The listed prefix of each rank in fact has at least the specified population.
    available = {v:0 for v in sites}
    for rank,r,pop in bands:
        for site in sites[:rank]:
            available[site] = max(available[site],pop)
        assert all(x[holders[d]]==d%k for d in range(1-r,r))
    available[sites[-1]] += 3
    available[len(tree)-1] = available.get(len(tree)-1,0)+2
    rest = []
    for p,n in available.items():
        assert n >= used[p]
        q, extra = divmod(n-used[p],k)
        tr.extend([p]*(q*k))
        x.extend(list(range(k))*q)
        rest.extend([p]*extra)
    gap = v.index(e[0]+1)
    for i in range(0,len(rest),k):
        group=rest[i:i+k]
        extra,gap=leaf_batch([x[p] for p in group],gap,k)
        tr.extend(group)
        x.extend(extra)
    v,e = counts(tr,x,k)
    assert max(v)-min(v)<=1 and max(e)-min(e)<=1
    assert Counter(tr[len(tree):])==+Counter(available)
    return len(tr),blocks,nroute


def check_auxiliary_moduli():
    """Use the modulus, rank and auxiliary-size relations in the theorem itself."""
    results = []
    for k, rank, denominator in [(256, 16, 2), (729, 64, 3)]:
        # B = k^(1/(4*denominator)). Determine ceil(rank*B) in integer arithmetic.
        power = 4*denominator
        auxiliary = rank
        while auxiliary**power < k * rank**power:
            auxiliary += 1
        assert auxiliary <= k and rank**denominator <= k**(denominator-1)
        tree = [-1] + list(range(2*rank-2))
        sites = list(range(0,len(tree),2))
        ranks = []
        r = 16
        while r <= rank:
            ranks.append((r,r//8,(8192*k+r-1)//r))
            r *= 2
        tr,x,holders,(blocks,routed) = seed(tree,k,ranks,sites,auxiliary)
        assert not blocks and routed > 0
        vertices,weights = counts(tr,x,k)
        assert len(set(weights)) == 1
        assert vertices.count(weights[0]+1) == 1 and vertices.count(weights[0]) == k-1
        uses = Counter(tr[len(tree):])
        assert all(uses[holder] <= next(pop for _,radius,pop in ranks if abs(d)<radius)
                   for d,holder in holders.items())
        results.append((k,auxiliary,routed))
    return results


def check_capacity_estimates(rng):
    """Check the thinning and integer interval budgets without constructing huge trees."""
    cases = 0
    threshold_cases = set()
    for profile in range(160):
        exponent = rng.randrange(24, 121)
        k = (1 << exponent) + rng.randrange(1024)
        limit = rng.randrange(12, 200)
        cutoff = 128 * limit
        ranks = [1 << j for j in range(4, exponent - 2)]
        pops = sorted((rng.randrange(cutoff, 8*k // r + cutoff) for r in ranks), reverse=True)
        if profile % 2:
            pops = [1024*pop for pop in pops]
        by_band = {}
        for r, pop in zip(ranks, pops):
            by_band[pop.bit_length()] = (r, pop)
        bands = sorted(by_band.values())
        total = sum(r*pop for r,pop in bands)
        assert sum(r*pop for r,pop in zip(ranks,pops)) <= 4*total
        start = load = 0
        cumulative = 0
        blocks = []
        for r,pop in bands:
            cumulative += r*pop
            end = k*cumulative//total
            width = r//8
            blocks.append((end-start+width-1)//width)
            start = end
        assert start == k
        threshold_cases.add(total >= 256*limit*k)
        later_pop = later_count = 0
        for (r,pop),count in reversed(list(zip(bands,blocks))):
            load += limit * count
            later_pop += pop
            later_count += 1
            assert later_pop <= 4*pop and later_count*cutoff <= 4*pop
            assert load*total*cutoff <= 64*limit*k*pop*cutoff + 8*limit*pop*total
            if total >= 256*limit*k:
                assert 2*load <= pop
        cases += 1
    assert threshold_cases == {False, True}
    return cases


def main():
    rng = Random(20261127)
    hops = cases = 0
    for r in (2,3,4,7,12,25,64):
        for size in (1,6,31,79):
            demands = [(rng.randrange(-3*r,5*r),rng.randrange(-5*r,3*r)) for _ in range(size)]
            hops += check_walks(demands,r,rng)
            cases += 1
    for r in (4,6):
        hops += check_walks([(0,r+1),(r+2,-1),(r,r)],r,rng,exact=True)
        cases += 1
    auxiliary = check_auxiliary_moduli()
    budgets = check_capacity_estimates(Random(20261127))
    results = []
    for k in (5,7,8,11):
        tree = [-1]
        sites = [0]
        for _ in range(32):
            parent = len(tree)
            tree += [0,parent]
            sites.append(parent+1)
        bands = [(16,2,700),(32,3,370)]
        results.append(full(k,tree,sites,bands,13,840,rng))
        # A large set of terminal paths; the specified sites remain in the other branches.
        for j in range(6):
            end = 0
            for _ in range(840+j+2):
                tree.append(end)
                end=len(tree)-1
                if j%2==0 and _ in (14,51):
                    tree.append(end)
        results.append(full(k,tree,sites,bands,13,840,rng))
    for k in (19,31):
        tree = [-1]
        sites = [0]
        for j in range(65):
            p = len(tree)
            tree.extend([0 if j < 3 else sites[j//2],p])
            sites.append(p+1)
        rng.shuffle(sites)
        results.append(full(k,tree,sites,[(16,2,500),(32,4,227),(64,8,100)],43,840,rng))
    assert any(b for _,b,_ in results) and any(l for _,_,l in results)
    print(f"Auxiliary-modulus seeds (k, M, repair leaves): {auxiliary}.")
    print(f"{budgets} multiscale population budgets checked with integer arithmetic.")
    print(f"{cases} integer route lists and {hops:,} site charges verified.")
    print(f"{len(results)} complete trees through order {max(n for n,_,_ in results):,}, "
          f"{sum(b for _,b,_ in results)} double paths, {sum(m for _,_,m in results)} short-jump leaves.")
    print("All populations restored and all vertex and actual edge bins recounted.")


if __name__=='__main__':
    main()

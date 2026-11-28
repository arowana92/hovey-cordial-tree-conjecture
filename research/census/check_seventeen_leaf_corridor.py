"""Bound a least 27-label failure within seventeen leaves by auditing its central path."""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations_with_replacement

from .check_order_fifty_one import short_arms
from .check_order_fifty_two import catalog_and_totals
from .check_sixteen_leaf_corridor import cross_cut
from .leaf_profile_geometry import cut_test, numerical_branches
from research.rainbow.spine_counts import partitions


def edge_allowed(t, size):
    first = {22:22,23:21,24:22}.get(t,t+1)
    return size%27 not in (0,(t+1)%27) and not first<=size<=27


def union_allowed(t, parts):
    forbidden = {22:(22,),23:(21,22),24:(22,)}.get(t,())
    reachable = 1
    for s,_ in parts:
        reachable |= reachable << s
    return all(not reachable & (1<<s) for s in forbidden)


def central_tip_types():
    failed = []
    for part in partitions(17):
        if max(part)>7:
            continue
        states = {(0,0,0)}
        for h in part:
            states = {tuple(sorted(state[:i]+(a+h,)+state[i+1:]))
                      for state in states for i,a in enumerate(state) if a+h<=7}
        if not states:
            failed.append(part)
    assert set(failed)=={(4,4,4,5),(1,4,4,4,4)}


def hubs(t, cuts):
    count = 0
    n = 55+t
    for four_count,more in ((3,5),(4,1)):
        for sizes in combinations_with_replacement(range(5,t),four_count):
            s = n-1-sum(sizes)
            if not more+(more>1)<=s<t:
                continue
            if more==1 and s+max(sizes)>=t:
                continue
            parts = tuple(sorted([(a,4) for a in sizes]+[(s,more)]))
            if union_allowed(t,parts) and all(edge_allowed(t,a) and edge_allowed(t,n-a) for a,_ in parts):
                assert cuts(parts), (n,parts)
                count += 1
    return count


def by_tip_partition(t, tips):
    """Build branch sizes after partitioning tips, tracking maximum attainable mass."""
    for counts in partitions(tips):
        if max(counts)>7:
            continue
        def assign(i, parts, maxima):
            if i==len(counts):
                yield tuple(sorted(parts))
                return
            h = counts[i]
            lo = max(h+(h>1),parts[-1][0] if i and counts[i-1]==h else 1)
            for s in range(lo,t-maxima[7-h]):
                new = maxima[:h]+tuple(max(maxima[j],s+maxima[j-h]) for j in range(h,8))
                yield from assign(i+1,parts+((s,h),),new)
        yield from assign(0,(),(0,)*8)


def endpoints(t, tips, cuts):
    cases = set(by_tip_partition(t,tips))
    independent = {p for mass in range(tips,2*t-1)
                   for p in numerical_branches(mass,tips,7,t,7)}
    assert cases==independent
    groups = defaultdict(list)
    for p in cases:
        if not all(edge_allowed(t,s) for s,_ in p) or not union_allowed(t,p) or not short_arms(p,t):
            continue
        mass = sum(s for s,_ in p)
        if sum(s for s,h in p if h==1)>=t or (mass>=t and cuts(p)):
            continue
        ring = min((26-mass+s for s,j in p if 1<=tips-j<=6 and 26-mass+s>=2),default=27)
        longest = max([1]+[s for s,j in p if j==1])
        groups[mass].append((ring,longest,p))
    return groups,len(cases)


def checks(t, catalog):
    cuts = cut_test(t,catalog,7)
    central = hubs(t,cuts)
    eight, count8 = endpoints(t,8,cuts)
    nine, count9 = endpoints(t,9,cuts)

    @lru_cache(None)
    def interval(n,a,e):
        return all(edge_allowed(t,j) and edge_allowed(t,n-j) for j in range(a+1,a+e+2))

    plain = Counter()
    for n in range(55+t,4*t+19,27):
        if n in (80,81):
            continue
        for a,left in eight.items():
            for b,right in nine.items():
                e = n-a-b-2
                if 0<=e<=20 and interval(n,a,e):
                    plain[n] += sum(r>e for r,_,_ in left)*sum(r>e for r,_,_ in right)
        assert not plain[n], (t,n,plain[n])

    @lru_cache(None)
    def remaining(a,e,d):
        counts = Counter()
        for ring,longest,p in eight[a]:
            if ring<=e or any(cross_cut(t,(d,1),v) or cross_cut(t,v,(d,1)) for v in p):
                continue
            # A terminal tail stays outside an order-27 piece using up to e corridor vertices.
            fits = max(1,a-26)<=longest and max(0,27-a)<=e
            counts[fits] += 1
        return counts

    compressed = Counter()
    for n in range(55+t,5*t+34,27):
        if n in (80,81):
            continue
        for a in eight:
            for b in eight:
                if b<a:
                    continue
                for e in range(21):
                    if not interval(n,a,e):
                        continue
                    for f in range(21):
                        d = n-a-b-3-e-f
                        if not 1<=d<=t-6 or not interval(n,b,f):
                            continue
                        if 1+d+e+f>=27 and 27-d>=3:
                            continue
                        u,v = remaining(a,e,d),remaining(b,f,d)
                        total = sum(u.values())*sum(v.values())
                        assert total == u[True]*v[True], (t,n,a,b,e,f,d,u,v)
                        compressed[n] += total
    print('t',t,'central',central,'endpoint inventories',count8,count9,
          'two-piece joins',dict((n,c) for n,c in compressed.items() if c))


if __name__=='__main__':
    central_tip_types()
    catalog,_ = catalog_and_totals()
    for t in range(22,27):
        checks(t,catalog)

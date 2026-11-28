"""Verify the two small orders at 16 leaves, using independently audited profiles."""
from itertools import combinations
from pathlib import Path

from .check_leaf_corridor import endpoint_cases
from .check_leaf_profile_manifests import read_rows
from .check_sixteen_leaf_corridor import ProfileCatalog
from .leaf_profile_geometry import cut_test, numerical_branches
from research.rainbow.spine_counts import partitions


def by_tip_partition(mass, tips, t):
    for hs in partitions(tips):
        if hs[-1]>7:
            continue
        lower=[h+int(h>1) for h in hs]

        def assign(i,left,max_mass,parts):
            if i==len(hs):
                if left==0:
                    yield tuple(sorted(parts))
                return
            h=hs[i]
            low=max(lower[i],parts[-1][0] if i and hs[i-1]==h else 0)
            high=min(t-1-max_mass[7-h],left-sum(lower[i+1:]))
            for s in range(low,high+1):
                best=max_mass[:h]+tuple(max(max_mass[a],s+max_mass[a-h]) for a in range(h,8))
                yield from assign(i+1,left-s,best,parts+[(s,h)])
        yield from assign(0,mass,(0,)*8,[])


def verify(n):
    t=n-28
    directory=Path(__file__).with_name('leaf-profile-audits')
    catalog=ProfileCatalog()
    for m in range(22,27):
        for leaves in range(12,16):
            path=directory/f'{leaves}-{28+m}.txt'
            if path.exists():
                catalog.known[m].update(read_rows(path,m))
    rows=read_rows(directory/f'16-{n}.txt',t)
    assert not catalog.known[t].intersection(rows)
    catalog.known[t].update(rows)
    cut=cut_test(t,catalog,7)
    def accepts(parts):
        if sum(s for s,h in parts if h==1)>=t:
            return True
        if t<=22 and any(sum(sizes)==t for j in range(len(parts)+1)
                         for sizes in combinations([s for s,_ in parts],j)):
            return True
        return cut(parts)
    central=set(numerical_branches(n-1,16,7,t,7))
    assert central==set(by_tip_partition(n-1,16,t))
    endpoints={p for p in endpoint_cases(t,8) if 27<=sum(s for s,h in p)<=min(t+18,2*(t-1))}
    independent={p for a in range(27,min(t+18,2*(t-1))+1) for p in numerical_branches(a,8,7,t,7)}
    assert endpoints==independent
    for p in central|endpoints:
        assert accepts(p), (n,p)
    totals=tuple(map(sum,zip(*rows.values())))
    print('order',n,'central profiles',len(central),'heavy endpoints',len(endpoints),
          'added profiles',len(rows),'forests, witness rows, boundary assignments',totals)


if __name__=='__main__':
    for order in (50,51):
        verify(order)

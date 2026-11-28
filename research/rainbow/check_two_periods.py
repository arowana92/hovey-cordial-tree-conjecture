"""Complete two-component uniform-period tests through modulus ten."""
from itertools import permutations
from math import gcd

from research.eight.generate import forests,parent_vector
from research.rainbow.spine_counts import rooted


def failure_search(parents,k,delta):
    """Assign actual labels at parents zero and delta; the first root is free."""
    roots=[i for i,p in enumerate(parents) if p<0]
    labels=[0]*k
    def extend(i,vertices,weights):
        if i==k:
            return True
        parent=parents[i]
        a=labels[parent] if parent>=0 else (0 if i==roots[0] else delta)
        for x in range(k):
            source=1<<x
            target=1<<((a+x)%k)
            if vertices&source or weights&target: continue
            labels[i]=x
            if extend(i+1,vertices|source,weights|target):
                return True
        return False
    return extend(0,0,0)


def check(k):
    summary=[0,0,0,0]
    failures=[]
    for shape in forests(k):
        if len(shape)!=2: continue
        parents=parent_vector(shape,(0,0))
        last=parents.index(-1,1)
        g=gcd(k,*(parents.count(i) for i in range(k)))
        wanted=set(range(0,k,g))
        covered=set()
        inside=[(u,v) for v,u in enumerate(parents) if u>=0]
        for tail in permutations(range(1,k)):
            row=(0,)+tail
            weights={(row[u]+row[v])%k for u,v in inside}
            if len(weights)!=k-2: continue
            a,b=set(range(k))-weights
            for first,second in [(a,b),(b,a)]:
                delta=(second-first-row[last])%k
                if delta in covered: continue
                # Reconstruct a literal witness with prescribed parents 0,delta.
                actual=[(x-first)%k for x in row]
                entering=[(x+(actual[p] if p>=0 else (0 if i==0 else delta)))%k
                          for i,(x,p) in enumerate(zip(actual,parents))]
                assert set(entering)==set(range(k))==set(actual)
                covered.add(delta)
            if covered==wanted: break
        assert covered<=wanted
        extra=sorted(wanted-covered)
        for delta in extra:
            assert not failure_search(parents,k,delta)
        if extra:
            failures.append((tuple(parents),extra))
        for i,count in enumerate((1,len(covered),k-len(wanted),len(extra))):
            summary[i]+=count
    types={s:sum(rooted(s).values()) for s in range(1,k)}
    expected=sum(types[s]*types[k-s] for s in range(1,(k+1)//2))
    if k%2==0:
        half=types[k//2]
        expected+=half*(half+1)//2
    assert summary[0]==expected
    if k==8:
        for parents,delta in failures: print(parents,delta)
    return summary


if __name__=="__main__":
    for k in range(3,11):
        print(k,*check(k),flush=True)

"""Check local repairs on decorated trees by recounting every original edge."""

from itertools import combinations
from math import gcd
from random import Random

from research.biased.large_order import coarse_labels, finish_two_shifts
from research.check_large_order_hall_pools import assign
from research.large_order_check import balanced_target, moment
from research.large_order_hall_pools import edge_split


def hist(par, lab, bias, k):
    vertices, edges = [0]*k, [0]*k
    for v,r in enumerate(lab):
        vertices[r] += 1
        if v:
            edges[(r+lab[par[v]]+bias[v])%k] += 1
    return vertices, edges


def two_groups(k, d, rng, shared):
    n = rng.randrange(2,70)
    par = [-1]+[rng.randrange(i) for i in range(1,n)]
    bias = [rng.randrange(k) for _ in par]
    span = gcd(k,d)
    low = coarse_labels(par,bias,span)
    lab = [v+span*rng.randrange(k//span) for v in low]
    V,E = hist(par,lab,bias,k)
    spare,a,b,surplus = finish_two_shifts(k,d,V,E)
    ports = (0,0 if shared else rng.randrange(1,n))
    for shift,p,amounts in ((0,ports[0],a),(d,ports[1],b)):
        for x,amount in enumerate(amounts):
            for _ in range(amount):
                par.append(p)
                bias.append((shift-lab[p])%k)
                lab.append(x)
    for x in spare:
        p = ports[0]
        par.append(p)
        bias.append(-lab[p]%k)
        lab.append(x)
    v,e = hist(par,lab,bias,k)
    assert len(set(e)) == 1 and v == [e[0]+int(x==surplus) for x in range(k)]


def path_sites(k,rng):
    layers = 160
    par,lab,bias = [-1],[rng.randrange(k)],[0]
    end = 0
    def add(parent):
        par.append(parent)
        lab.append(rng.randrange(k))
        bias.append(rng.randrange(k))
        return len(par)-1
    def site():
        nonlocal end
        left = add(add(end))
        center = add(left)
        end = add(add(center))
        return center
    pools = []
    for d in (0,0,1):
        counts = [[0]*k for _ in range(3)]
        groups = [[] for _ in range(k)]
        for _ in range((layers+6)*k):
            v = site()
            def observations(p):
                return p,(p-bias[v])%k,(p+d-bias[v+1])%k
            p = min(range(k),key=lambda s: sum(c[x] for c,x in zip(counts,observations(s))))
            _,lab[v-1],lab[v+1] = observations(p)
            for c,x in zip(counts,observations(p)):
                c[x] += 1
            groups[p].append((v,p))
        assert min(counts[0]) >= layers
        pool = [item for group in groups for item in group[:layers]]
        pools.append(pool)
        assign(pool,lab,[layers]*k,'edges')
    special = []
    for center,right in ((1,0),(0,1)):
        v = site()
        lab[v-1],lab[v],lab[v+1] = -bias[v]%k,center,(right-bias[v+1])%k
        special.append(v)
    spare = add(end)
    tail = add(spare)
    v,e = hist(par,lab,bias,k)
    vt,et = balanced_target(len(lab),k),balanced_target(len(lab)-1,k)
    a,b = moment(vt)-moment(v),moment(et)-moment(e)
    lab[spare] = (lab[spare]+b-a)%k
    lab[tail] = (lab[tail]+2*a-b)%k
    v,e = hist(par,lab,bias,k)
    dv = [i-j for i,j in zip(vt,v)]
    toggle,h,g = edge_split([i-j for i,j in zip(et,e)])
    if toggle:
        x,y = special
        lab[x],lab[y] = lab[y],lab[x]
    for pool,delta,kind in zip(pools,(dv,h,g),('vertices','edges','edges')):
        assert layers+min(delta) >= 0
        assign(pool,lab,[layers+x for x in delta],kind)
    assert hist(par,lab,bias,k) == (vt,et)
    return len(lab)


if __name__ == "__main__":
    rng = Random(41355)
    tests = 0
    for k in range(2,42):
        for d in range(1,k):
            for shared in (False,True):
                two_groups(k,d,rng,shared)
                tests += 1
    print(f"{tests} decorated tree completions with two effective shifts")
    cases = vertices = 0
    for k in range(2,10):
        for _ in range(2):
            vertices += path_sites(k,rng)
            cases += 1
    print(f"{cases} decorated path repairs on {vertices} total vertices")
    checked = 0
    for k in range(2,16):
        for t in range(2,k+1):
            for points in combinations(range(k),t):
                gaps = [(points[(i+1)%t]-v)%k for i,v in enumerate(points)]
                assert k//gcd(k,min(gaps)) >= t
                checked += 1
    print(f"{checked} circle-spacing checks for distinct leaf offsets")

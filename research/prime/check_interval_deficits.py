"""Verify affine interval-deficit attachments on actual summed edges."""

from functools import lru_cache
from math import gcd
from random import Random

from .check_deficit_cut import realize


@lru_cache(None)
def units(k):
    return tuple(v for v in range(1,k) if gcd(v,k) == 1)


def factor_powers(k):
    p = 2
    while p*p <= k:
        if k % p == 0:
            q = 1
            while k % p == 0:
                k //= p
                q *= p
            yield p,q
        p += 1
    if k > 1:
        yield k,k


def totient(n):
    result = n
    for p, _ in factor_powers(n):
        result -= result//p
    return result


def reasons(k,step,h,a):
    E = h*(2*a+1)
    F = a*(2*h+1)
    D = max(E,F)
    global_test = totient(k//gcd(k,step)) > 3*h*E*E*F
    local_test = False
    for p,q in factor_powers(k):
        factor = 1
        while factor*p <= 3*h:
            factor *= p
        local_test |= totient(q//gcd(q,step)) > factor*D
    return global_test,local_test


def place(k,core_low_v,core_low_e,V,W,b):
    # The old port is zero. Test each of the two anchors and a fixed low
    # bridge by directly inspecting the transformed sets.
    z = min(core_low_e)
    for u in units(k):
        for shift in (u*(b-W[0]), u*(b-W[-1]), z-u*b):
            transformed = {(u*v+shift) % k for v in V}
            if transformed & core_low_v:
                continue
            edges = {(u*w+2*shift) % k for w in W}
            bridge = (shift+u*b) % k
            if bridge in edges:
                if not (edges-{bridge}) & core_low_e:
                    return u,shift
            elif bridge in core_low_e and not edges & core_low_e:
                return u,shift
    return None


def build(k,h,step,rng):
    v0, w0, b = (rng.randrange(k) for _ in range(3))
    V = [(v0+i*step)%k for i in range(h)]
    W = [(w0+i*step)%k for i in range(h+1)]
    labels, parents, sites = realize(k,[2-int(v in V) for v in range(k)],
                                    [2-int(w in W) for w in range(k)],rng)
    return V,W,b,labels,parents,sites


def actual():
    rng = Random(80261991)
    count = [0,0,0]
    cases = [(720,1,1,1),(3024,1,2,1),(4725,2,1,1),(512,1,1,1)]
    for _ in range(650):
        k = rng.choice((64,81,128,169,243,256,343,392,512,625,729,1155,5005))
        h = rng.randint(1,5)
        a = rng.randint(1,8)
        step = rng.choice((1,2,3,4,5,7,8))
        cases.append((k,h,a,step))
    for k,h,a,step in cases:
        g,l = reasons(k,step,h,a)
        if not (g or l):
            continue
        V,W,b,part,pp,sites = build(k,h,step,rng)
        assert len(set(W)) == h+1
        low_v = set(rng.sample(range(k),a))
        low_e = set(rng.sample(range(k),a+1))
        core,cp,old = realize(k,[2-int(x in low_v) for x in range(k)],
                              [2-int(x in low_e) for x in range(k)],rng)
        u,t = place(k,low_v,low_e,V,W,b)
        row = [(u*x+t)%k for x in part]
        vertices,edges = [0]*k,[0]*k
        for vals,parents in ((core,cp),(row,pp)):
            for i,x in enumerate(vals):
                vertices[x] += 1
                if i:
                    edges[(x+vals[parents[i]])%k] += 1
        edges[(core[old[0][-1]]+row[sites[b][0]])%k] += 1
        assert max(vertices)-min(vertices) <= 1 and max(edges)-min(edges) <= 1
        count[int(g)+2*int(l)-1] += 1
    assert all(count)
    return count


def trees_of_pieces():
    rng = Random(82691)
    count = pieces = 0
    for _ in range(64):
        k = rng.choice((256,343,512,625,1009))
        h = rng.randint(1,3)
        _,_,_,labels,parents,_ = build(k,h,1,rng)
        edges = [(parents[i],i,0) for i in range(1,len(labels))]
        a = h
        for _ in range(8):
            vc, ec = [0]*k, [0]*k
            for x in labels:
                vc[x] += 1
            for left,right,bias in edges:
                ec[(labels[left]+labels[right]+bias)%k] += 1
            assert max(vc)-min(vc) <= 1 and max(ec)-min(ec) <= 1
            assert vc.count(min(vc)) == a and ec.count(min(ec)) == a+1
            h = rng.randint(1,3)
            if not any(reasons(k,1,h,a)):
                break
            V,W,b,row,pp,sites = build(k,h,1,rng)
            left = rng.randrange(len(labels))
            bias = rng.randrange(k)
            c = (labels[left]+bias)%k
            low_v = {(x-c)%k for x in range(k) if vc[x] == min(vc)}
            low_e = {(w-2*c)%k for w in range(k) if ec[w] == min(ec)}
            u,t = place(k,low_v,low_e,V,W,b)
            start = len(labels)
            labels.extend((c+u*x+t)%k for x in row)
            edges.extend((start+pp[i],start+i,0) for i in range(1,len(row)))
            edges.append((left,start+sites[b][0],bias))
            a += h
            pieces += 1
        vc,ec = [0]*k,[0]*k
        for x in labels:
            vc[x] += 1
        for left,right,bias in edges:
            ec[(labels[left]+labels[right]+bias)%k] += 1
        assert max(vc)-min(vc) <= 1 and max(ec)-min(ec) <= 1
        count += 1
    return count,pieces


def forced_collisions():
    rng = Random(41391)
    count = 0
    for k in (5,6,7,8,9,10,13,15,18,22,26,29):
        for a in range(2,5):
            for h in range(2,5):
                if a+h+1 > k:
                    continue
                def fixture(j):
                    vlow = set(range(j+1))-{1}
                    return realize(k,[2-int(x in vlow) for x in range(k)],
                                   [2-int(w<=j) for w in range(k)],rng)
                old,cp,cs = fixture(a)
                part,pp,sites = fixture(h)
                old_v,old_e = [0]*k,[0]*k
                for i,x in enumerate(old):
                    old_v[x] += 1
                    if i:
                        old_e[(x+old[cp[i]])%k] += 1
                for u in units(k):
                    for t in range(k):
                        row = [(u*x+t)%k for x in part]
                        vc,ec = old_v.copy(),old_e.copy()
                        for i,x in enumerate(row):
                            vc[x] += 1
                            if i:
                                ec[(x+row[pp[i]])%k] += 1
                        ec[(old[cs[0][0]]+row[sites[0][0]])%k] += 1
                        assert max(vc)-min(vc)>1 or max(ec)-min(ec)>1
                count += 1
    return count


def positions():
    # Directly count surviving placements in quotients with step of any
    # order, including when tau or sigma lies outside the generated subgroup.
    count = 0
    for k in range(3,40):
        for step in range(1,k):
            m = k//gcd(k,step)
            for h in range(1,min(7,(m-1)//3)+1):
                def window(u,l,r):
                    return {(u+j*step)%k for j in range(l,r+1)}
                first_x, first_y = window(0,1-h,0),window(0,-h,-1)
                last_x, last_y = window(0,1,h),window(0,h+1,2*h)
                low_y,low_diff = window(0,0,h),window(0,0,h-1)
                for x in range(k):
                    for y in range(k):
                        assert not ((x in first_x or y in first_y)
                                    and (x in last_x or y in last_y)
                                    and (y in low_y or (y-x)%k in low_diff))
                        count += 1
    return count


if __name__ == '__main__':
    print('Quotient interval configurations:', positions(), flush=True)
    print('Actual joins, global only / local only / both:', actual(), flush=True)
    print('Trees of pieces and verified attachments:', trees_of_pieces(), flush=True)
    print('Fixed tree pairs rejecting every affine image:', forced_collisions(), flush=True)

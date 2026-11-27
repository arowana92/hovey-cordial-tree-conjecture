"""Check the small packets left after a maximum-size surplus-forest census."""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from math import gcd
from pathlib import Path
import json
import sys

from research.eight.verify import components
from .check_surplus_spectrum import orbit
from .generate import rainbow


def direct(ps,k,d):
    """Return a witness keeping the surplus (d=None) or divisible core fixed."""
    v = [int(i==0) if d is None else 1 for i in range(k)]
    w = [0 if d is None else int(i!=d) for i in range(k)]
    n = sum(v)+len(ps)
    lo_v,lo_w = n//k,(n-1)//k
    hi_v,hi_w = (n+k-1)//k,(n+k-2)//k
    internals = set(p for p in ps if p>=0)
    order = sorted(internals)
    f = [None]*len(ps)

    def parent(i):
        p = ps[i]
        return -1-p if p<0 else f[p]

    def solve(pos,leaves):
        if pos==len(order) and not leaves:
            pending = [i for i in range(len(ps)) if i not in internals]
            groups = Counter(parent(i) for i in pending)
            pending.sort(key=lambda i:(-groups[parent(i)],parent(i),i))
            order.extend(pending)
            ans = solve(pos,True)
            del order[pos:]
            return ans
        if pos==len(order):
            return min(v)>=lo_v and min(w)>=lo_w
        i = order[pos]
        a = parent(i)
        same = leaves and pos>len(internals) and parent(order[pos-1])==a
        first = f[order[pos-1]] if same else 0
        for x in range(first,k):
            y = (a+x)%k
            if v[x]>=hi_v or w[y]>=hi_w:
                continue
            v[x] += 1
            w[y] += 1
            f[i] = x
            left = len(ps)-pos-1
            if (sum(max(0,lo_v-z) for z in v)<=left and
                    sum(max(0,lo_w-z) for z in w)<=left and solve(pos+1,leaves)):
                return True
            f[i] = None
            v[x] -= 1
            w[y] -= 1
        return False

    return f if solve(0,False) else None


def balanced(ps,k,d,f):
    assert f is not None and len(f)==len(ps) and all(0<=x<k for x in f)
    v = Counter(f)
    e = Counter((f[i]+(f[p] if p>=0 else -1-p))%k for i,p in enumerate(ps))
    if d is None:
        v[0] += 1
    else:
        e[d] -= 1
    return all(max(hist[i] for i in range(k))-min(hist[i] for i in range(k))<=1
               for hist in (v,e))


def affine(ps,k,d):
    # Keep the same unit on the boundary colors and the old deficit.
    roots = components(ps)
    return {(tuple(sorted(((u*x+s)%k,t) for x,t in roots)),(u*d+2*s)%k)
            for u in range(1,k) if gcd(u,k)==1 for s in range(k)}


def negative(ps,k,d):
    """Enumerate label multisets within sibling leaves, keeping all internal labels."""
    size = len(ps)
    internal = {p for p in ps if p>=0}
    groups = [[i] for i in sorted(internal)]
    leaves = {}
    for i,p in enumerate(ps):
        if i not in internal:
            leaves.setdefault(p,[]).append(i)
    groups += list(leaves.values())
    f = [0]*size
    total = 0
    def candidates(i,remaining):
        nonlocal total
        if i==len(groups):
            total += 1
            if balanced(ps,k,d,f):
                raise ValueError("a declared obstruction has a witness")
            return
        sites = groups[i]
        for chosen in set(combinations(remaining,len(sites))):
            rest = list(remaining)
            for v,x in zip(sites,chosen):
                f[v] = x
                rest.remove(x)
            candidates(i+1,rest)

    assert size==k
    candidates(0,list(range(k)))
    if d is None:
        # A moved surplus replaces the zero by a second copy of the new high.
        for x in range(1,k):
            candidates(0,sorted([x]+list(range(1,k))))

    return total


def first_root_lifts(failed,k,key):
    lifts = set()
    direct_cases = []
    for ps in failed.values():
        zeroes = [i for i,p in enumerate(ps) if p==-1]
        for mask in range(1<<len(zeroes)):
            attach = {i for j,i in enumerate(zeroes) if mask>>j&1}
            tail = tuple(0 if j in attach else p+(p>=0) for j,p in enumerate(ps))
            for d in range(k):
                q = (-1-d,)+tail
                for i,p in enumerate(q):
                    if p>=0:
                        continue
                    x = (d+1+p)%k
                    rest = tuple(-1 if t==i else -1-((-1-t-x)%k) if t<0 else t-int(t>i)
                                 for j,t in enumerate(q) if j!=i)
                    if key(rest) not in failed:
                        break
                else:
                    direct_cases.append((q,d))
                lifts.add((q,d))
    return len(lifts),set(direct_cases)


def check(k,bad):
    @lru_cache(None)
    def key(ps):
        return min(orbit(ps,k))

    def cut(ps,i):
        return tuple(p-int(p>i) for j,p in enumerate(ps) if j!=i)

    maximum = {key(tuple(ps)):tuple(ps) for ps in bad}
    shorter = set()
    divisible_bad = {}
    surplus_bad = {}
    bad_ten = {}
    negative_rows = 0
    for ps in maximum.values():
        for i in range(k-1):
            if i not in ps:
                q = cut(ps,i)
                if key(q) not in shorter:
                    word = rainbow(q,k)
                    assert len(set(word))==len(q) and 0 not in word
                    assert len({(word[j]+(word[p] if p>=0 else -1-p))%k
                                for j,p in enumerate(q)})==len(q)
                    shorter.add(key(q))
    lifts,hard = first_root_lifts(maximum,k,key)
    for q,d in hard:
        labels = direct(q,k,d)
        if labels is None:
            images = affine(q,k,d)
            rep = min(images)
            if rep not in divisible_bad:
                negative_rows += negative(q,k,d)
                divisible_bad[rep] = len(images)
        else:
            assert balanced(q,k,d,labels)

    previous = maximum
    frontier = []
    while previous:
        n = len(next(iter(previous.values())))
        frontier.append(len(previous))
        following = {}
        for ps in previous.values():
            for p in range(-k,n):
                q = ps+(p,)
                rep = key(q)
                if rep in following:
                    continue
                if all(key(cut(q,i)) in previous for i in range(n+1) if i not in q):
                    labels = direct(q,k,None)
                    if labels is None:
                        negative_rows += negative(q,k,None)
                        surplus_bad[rep] = len(orbit(q,k))
                        bad_ten[rep] = q
                    else:
                        assert balanced(q,k,None,labels)
                    following[rep] = q
        previous = following
    lifts11,hard11 = first_root_lifts(bad_ten,k,key)
    for q,d in hard11:
        assert balanced(q,k,d,direct(q,k,d))
    assert (lifts11,len(hard11))==(480,20)
    print('eleven-vertex divisible lifts',lifts11,'direct cases',len(hard11))
    assert len(maximum)==16 and len(shorter)==26
    assert sorted(divisible_bad.values())==[10] and sorted(surplus_bad.values())==[4,4]
    assert (lifts,len(hard),negative_rows,frontier)==(4760,140,18612,[16,6,3])
    print('divisible failures',divisible_bad,'surplus failures at larger sizes',surplus_bad,
          'negative rows',negative_rows)
    print('shorter orbits',len(shorter),'divisible lifts',lifts,
          'direct divisible cases',len(hard),'successive exceptional ideal orbits',frontier)


if __name__=='__main__':
    check(10,json.loads(Path(sys.argv[1]).read_text()))

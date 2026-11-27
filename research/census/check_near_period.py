"""Search the reduced Hamilton paths and replay the two histograms on actual trees."""
from itertools import permutations
from random import Random
from math import isqrt

from .near_period import pendant_request,prepare


def find_path(k,start,end,inside,colors,rng):
    # Reversing a segment changes only its two boundary edges. Try to remove
    # duplicate or unwanted colors before the endpoint-by-endpoint search.
    if k>=36:
        for _ in range(12):
            middle = sorted(inside)
            rng.shuffle(middle)
            path = [start]+middle+[end]
            color = [(a+b)%k for a,b in zip(path,path[1:])]
            hist = [color.count(i) for i in range(k)]
            for step in range(3000):
                bad = [i for i,x in enumerate(color) if x not in colors or hist[x]>1]
                if not bad:
                    return path
                i = rng.choice(bad)
                choices = []
                best = -3
                for j in range(len(color)):
                    if abs(i-j)<2:
                        continue
                    left,right = sorted((i,j))
                    x,y = color[left],color[right]
                    u = (path[left]+path[right])%k
                    v = (path[left+1]+path[right+1])%k
                    changed = {x,y,u,v}&colors
                    gain = sum(int(hist[z]-(z==x)-(z==y)+(z==u)+(z==v)>0)-int(hist[z]>0)
                               for z in changed)
                    if gain>best:
                        choices = []
                        best = gain
                    if gain==best:
                        choices.append((left,right,u,v))
                if best<0 and rng.randrange(10):
                    continue
                left,right,u,v = rng.choice(choices)
                hist[color[left]] -= 1
                hist[color[right]] -= 1
                hist[u] += 1
                hist[v] += 1
                path[left+1:right+1] = reversed(path[left+1:right+1])
                color[left+1:right] = reversed(color[left+1:right])
                color[left],color[right] = u,v
    mask = (1<<k)-1
    def neighbors(weights,label):
        return (weights>>label)|((weights<<(k-label))&mask)

    def visit(left,right,sites,weights):
        nonlocal budget
        budget -= 1
        if not sites:
            return [left,right] if weights==1<<((left+right)%k) else None
        choices = sites&neighbors(weights,left)
        back = sites&neighbors(weights,right)
        if not choices or not back:
            return None
        flip = bin(back).count("1")<bin(choices).count("1")
        if flip:
            choices = back
        port = right if flip else left
        while choices and budget>0:
            # Randomizing the first available bit reduces repeated dead tails.
            shift = rng.randrange(k)
            rotated = (choices>>shift)|((choices<<(k-shift))&mask)
            x = ((rotated&-rotated).bit_length()-1+shift)%k
            bit = 1<<x
            choices ^= bit
            rest = sites^bit
            colors = weights^(1<<((x+port)%k))
            if flip:
                path = visit(left,x,rest,colors)
                if path is not None:
                    return path+[right]
            else:
                path = visit(x,right,rest,colors)
                if path is not None:
                    return [left]+path
        return None

    for _ in range(200):
        budget = 6000
        result = visit(start,end,sum(1<<x for x in inside),sum(1<<x for x in colors))
        if result is not None:
            return result
    raise AssertionError("sample path search exhausted")


def run(k,ps,shifts,a,b,w,rng):
    result = prepare(k,ps,shifts,a,b,w)
    if result is None:
        return False
    f,(prefix,v,z,inside,colors) = result
    try:
        row = prefix+find_path(k,v,z,inside,colors,Random(k*1000003+sum(1<<x for x in inside)+v))
    except AssertionError as exc:
        raise AssertionError((k,ps,shifts,a,b,w,f,len(inside))) from exc
    # Old tree consists of the edge and a distinct old parent for each external
    # vertex; choose independent actual parent labels and split the shifts.
    ext = [rng.randrange(k) for p in ps if p<0]
    labels = [a,b]+ext
    edges = [(0,1,(w-a-b)%k)]+[(0,2+i,rng.randrange(k)) for i in range(len(ext))]
    def bins(labels,edges):
        counts = [[0]*k for _ in range(2)]
        for x in labels:
            counts[0][x] += 1
        for u,v,c in edges:
            counts[1][(labels[u]+labels[v]+c)%k] += 1
        return counts
    old = bins(labels,edges)
    edges = edges[1:]
    base = len(labels)
    ext_idx = 2
    for i,p in enumerate(ps):
        if p<0:
            edges.append((ext_idx,base+i,(shifts[i]-labels[ext_idx])%k))
            ext_idx += 1
        else:
            edges.append((base+p,base+i,shifts[i]))
    labels.extend(f)
    first = len(labels)
    labels.extend(row)
    chain = [0]+list(range(first,len(labels)))+[1]
    edges.extend((u,v,0) for u,v in zip(chain,chain[1:]))
    new = bins(labels,edges)
    assert all(y==x+1 for h,g in zip(old,new) for x,y in zip(h,g))
    return True


def main():
    rng = Random(28112613)
    yes = no = 0
    for k in (13,16,19,22,25,26,27,29,31,36,49,64,81):
        for h in range(isqrt(k)-1):
            for t in range(8):
                a,b = rng.randrange(k),rng.randrange(k)
                ps = [i-1 if t%3==0 else -1 if t%3==1 else rng.randrange(-1,i)
                      for i in range(h)]
                shifts = [rng.randrange(k) for _ in ps]
                w = (a+b)%k if t%2 else rng.randrange(k)
                if h==2 and ps[1]==0 and t%2:
                    # Enforce equality of the two forest weights explicitly.
                    w = (a+b+k*(k-1)//2+2*shifts[1])%k
                T = (k*(k-1)//2+a+b-w+sum(shifts))%k
                impossible = ((h==0 and T!=0) or
                              (h==2 and ps[1]==0 and (T+shifts[1]-shifts[0])%k==0
                               and (w-shifts[0])%k==T))
                ok = run(k,ps,shifts,a,b,w,rng)
                assert ok!=impossible
                yes += ok
                no += not ok
    # On the two-vertex obstruction inspect every possible pair of distinct
    # forest labels. The path can only contribute nonnegative weight counts.
    negative = 0
    for k in range(5,56,2):
        for p in range(k):
            old_weight = 2*p%k
            for x,y in permutations(range(k),2):
                if (2*(x+y)-(p+x)-(x+y)-k*(k-1)//2)%k:
                    continue
                assert (p+x)%k==(x+y)%k!=old_weight
                negative += 1
    paths = prefixes = 0
    for k in (13,17,22,26,27,35,49,64):
        for r in range(1,isqrt(k)):
            for _ in range(5):
                vs = set(rng.sample(range(k),r))
                es = set(rng.sample(range(k),r-1))
                parent = rng.randrange(k)
                options = [pendant_request(k,vs,es,parent,t) for t in range(k)]
                assert sum(row is not None for row in options)>=k-2*r+1
                first,tip,inside,colors,gap = rng.choice([row for row in options if row])
                path = find_path(k,first,tip,inside,colors,rng)
                v = [1+int(i in vs) for i in range(k)]
                e = [1+int(i in es) for i in range(k)]
                for x in path:
                    v[x] += 1
                    e[(x+parent)%k] += 1
                    parent = x
                    assert max(v)-min(v)<=1 and max(e)-min(e)<=1
                    prefixes += 1
                assert v==[2]*k and e==[2-int(i==gap) for i in range(k)]
                paths += 1
    print('pendant completions',paths,'cordial intermediate prefixes',prefixes)
    print('complete grafts',yes,'moment or duplicate obstructions',no,
          'moment-compatible negative assignments',negative)


if __name__=='__main__':
    main()

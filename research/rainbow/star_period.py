"""Compressed counts for a star and equal-parent singleton leaves over whole periods."""
from math import gcd

from research.large_order_hall_pools import hall_pair, zero_block


def cyclic(k,q,c,p,b,a):
    """Return child and singleton count vectors, or None, for a prescribed center."""
    if k<1 or q<1 or not 0<=c<q*k:
        raise ValueError("the center and children must fit")
    a,b,p = a%k,b%k,p%k
    d = (a-b)%k
    surplus = (b-p-c*d)%k
    rhs = [0]*k
    for i,z in ((0,1),(a,1),(surplus,-1),((p+d)%k,-1)):
        rhs[i] += z
    children = [0]*k
    cosets = []
    g = gcd(d,k)
    h = k//g
    for root in range(g):
        sites = [(root+j*d)%k for j in range(h)]
        base = 0
        for i in sites:
            base -= rhs[i]
            children[i] = base
        if base:
            return None
        lower = -min(children[i] for i in sites)
        upper = min(q-int(i==p)-children[i] for i in sites)
        if upper<lower:
            return None
        for i in sites:
            children[i] += lower
        cosets.append((sites,upper-lower))
    layers,remainder = divmod(c-sum(children),h)
    if remainder or layers<0 or layers>sum(cap for _,cap in cosets):
        return None
    for sites,cap in cosets:
        take = min(layers,cap)
        for i in sites:
            children[i] += take
        layers -= take
    singletons = [q-int(i==(p+d)%k)-children[(i-d)%k] for i in range(k)]
    return children,singletons,surplus


def arbitrary(k,shifts,center,children):
    """Use either congruence with arbitrary edge offsets and singleton-parent colors.

    The input shifts include the old parent plus offset for externally attached
    rows, and just the edge offset for center children. The old surplus is zero.
    """
    n = len(shifts)
    if n%k or not n or center in children:
        raise ValueError("need whole periods and an external center")
    c = len(children)
    total = sum(shifts)
    for move in (False,True):
        for a in range(k):
            if ((c+int(move))*a+total)%k:
                continue
            delta = [(b+(a if i in children else 0))%k for i,b in enumerate(shifts)]
            if move:
                delta[center] = (delta[center]+a)%k
            # Each zero-sum Hall layer can be translated, so the distinguished
            # row can receive its prescribed source even when it occurs once.
            pending = {}
            for i,x in enumerate(delta):
                pending.setdefault(x,[]).append(i)
            left = n
            f = [None]*n
            while left:
                counts = [len(pending.get(x,[])) for x in range(k)]
                if left==k:
                    block = [x for x,amount in enumerate(counts) for _ in range(amount)]
                else:
                    block = zero_block(counts)
                sites = [pending[x].pop() for x in block]
                pair = hall_pair(block)
                sources = [-x%k for x,_ in pair]
                shift = 0
                if center in sites:
                    shift = ((0 if move else a)-sources[sites.index(center)])%k
                for i,x in zip(sites,sources):
                    f[i] = (x+shift)%k
                left -= k
            f[center] = a
            return f
    return None


def pinned_sources(shifts,site,value):
    """Realize one zero-sum period with a chosen source at site."""
    k = len(shifts)
    sources = [-x%k for x,_ in hall_pair(shifts)]
    change = value-sources[site]
    return [(x+change)%k for x in sources]


def independent(k,shifts,surplus):
    """Add arbitrarily many independent rows to a core with one high vertex bin."""
    answer = []
    pos = 0
    while pos<len(shifts):
        batch = list(shifts[pos:pos+k-1])
        r = len(batch)
        padded = batch+[0]*(k-1-r)+[-sum(batch)%k]
        labels = pinned_sources(padded,k-1,surplus)[:r]
        answer.extend(labels)
        pos += r
        if pos<len(shifts):
            weights = {(x+b)%k for x,b in zip(labels,batch)}
            gap, = set(range(k))-weights
            surplus = (gap-shifts[pos])%k
            answer.append(surplus)
            pos += 1
    return answer


def one_center(k,shifts,center,children):
    """Extend a zero-surplus core for all n>k and at n=k by either congruence."""
    n = len(shifts)
    if k<1 or n<k or not 0<=center<n or center in children or any(not 0<=i<n for i in children):
        raise ValueError("need a center and at least one period")
    if k==1:
        return [0]*n
    kids = sorted(children)
    singles = [i for i in range(n) if i!=center and i not in children]
    if n==k:
        return arbitrary(k,shifts,center,children)
    # The selected first period contains j children and k-1-j singletons.
    low = max(0,k-1-len(singles))
    high = min(k-1,len(kids))
    j = next((x for x in range(low,high+1) if gcd(x,k)==1 or gcd(x+1,k)==1),None)
    answer = [None]*n
    if j is not None:
        batch = [center]+kids[:j]+singles[:k-1-j]
        rest = kids[j:]+singles[k-1-j:]
        row = arbitrary(k,[shifts[i] for i in batch],0,set(range(1,j+1)))
        for i,x in zip(batch,row):
            answer[i] = x
        high_bin, = [x for x in range(k) if row.count(x)+int(x==0)==2]
        extra = [(shifts[i]+(row[0] if i in children else 0))%k for i in rest]
        for i,x in zip(rest,independent(k,extra,high_bin)):
            answer[i] = x
        return answer

    # One virtual source is supplied by the last leaf; the other extra rows
    # may all translate together while avoiding two sources and one weight.
    leaves = kids+singles
    batch = [center]+leaves[:k-1]
    rest = leaves[k-1:]
    assert rest and 3*(len(rest)-1)<k
    a = 1
    effective = [(b+(a if i in children else 0))%k for i,b in enumerate(shifts)]
    requests = [effective[i] for i in batch]
    correction = sum(requests)%k
    w = (a+correction)%k
    requests[0] = (requests[0]-correction)%k
    for i,x in zip(batch,pinned_sources(requests,0,w)):
        answer[i] = x
    answer[center] = a
    last = rest.pop()
    answer[last] = w
    used_weight = (w+effective[last])%k
    shifts_left = [effective[i] for i in rest]
    padded = shifts_left+[0]*(k-1-len(rest))+[-sum(shifts_left)%k]
    free = pinned_sources(padded,k-1,0)[:len(rest)]
    for change in range(k):
        if all((x+change)%k not in (0,a) and (x+change+effective[i])%k!=used_weight
               for i,x in zip(rest,free)):
            for i,x in zip(rest,free):
                answer[i] = (x+change)%k
            return answer
    raise AssertionError("the forbidden translations exhaust the group")

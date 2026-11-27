"""Preserve prescribed edge endpoints when inserting a path in a cordial tree."""


def interval_cycle(n, even_repeat=False):
    """Mosahab's interval cycle, or the modified even-repeat cycle of order 4m."""
    r = n//2
    if n%2:
        return [j//2 if j%2 == 0 else r+1+j//2 for j in range(n)]
    if n == 4 and not even_repeat:
        return [0,1,3,2]
    if n == 8:
        return [0,1,4,2,6,5,3,7] if even_repeat else [0,3,1,7,2,4,6,5]
    if n < 6 or (even_repeat and r%2):
        raise ValueError("unsupported interval cycle")
    if even_repeat:
        seeds = {6:[7,9,4,11,3,8,10], 8:[10,12,5,13,11,4,15,6,14]}
    else:
        seeds = {3:[1,5,3,4], 5:[2,9,3,7,6,8], 6:[7,9,8,4,11,3,10],
                 8:[10,12,11,5,15,6,13,4,14]}
    base = next(i for i in seeds if (r-i)%4 == 0)
    steps = (r-base)//4
    low = [2*r-2]+[(i-1)//2 if i%2 else r-2+i//2 for i in range(1,r+1)]
    # From h to h+4, old entries below h gain two and the others gain six.
    high = [x+steps*(2 if x<base else 6) for x in seeds[base]]
    for h in range(base,r,4):
        rest = (r-h-4)//4
        high.extend((h+2+2*rest,2*h+7+6*rest,h+1+2*rest,2*h+6+6*rest))
    return low+high[1:-1]


def after(cycle, x):
    i = cycle.index(x)+1
    return cycle[i:]+cycle[:i]


def half_weights(k, repeated):
    """A Hamilton cycle repeating the specified sum, omitting its antipode."""
    if k%2 or k < 6:
        raise ValueError("requires even modulus at least six")
    if repeated%2:
        p = [j//2 if j%2 == 0 else k//2+j//2 for j in range(k)]
        old = k-1
    else:
        p = interval_cycle(k,even_repeat=k%4 == 0)
        old = (0 if k == 8 else k//2) if k%4 == 0 else k//2-1
    shift = (repeated-old)//2
    return [(x+shift)%k for x in p]


def short(k, a, b, surplus, t):
    """Insert t vertices, 2 <= t < k, at any edge of an order-one core, k>=5."""
    if k < 5 or not 2 <= t < k:
        raise ValueError("requires modulus at least five and 2 <= length < k")
    a,b = (a-surplus)%k,(b-surplus)%k
    if t == 2:
        for x in range(1,k):
            z = (a+b-x)%k
            if z and x != z and (a+x)%k != (b+z)%k:
                return [(x+surplus)%k,(z+surplus)%k]
        # Only the five- and six-label boundary checks can reach this fallback.
        for x in range(1,k):
            for z in range(1,k):
                weights = [(a+x)%k,(x+z)%k,(z+b)%k]
                if x != z and (a+b)%k in weights:
                    weights.remove((a+b)%k)
                    if weights[0] != weights[1]:
                        return [(x+surplus)%k,(z+surplus)%k]
        raise AssertionError("no two-vertex insertion")
    if a or b:
        endpoint = a or b
        left = max(1,endpoint-t+1)
        row = after([x+left for x in interval_cycle(t)],endpoint)
        if not a:
            row.reverse()
    else:
        if t+1 == k and k%2 == 0:
            p = half_weights(k,0)
        else:
            p = interval_cycle(t+1)
            s = next(x+y for x,y in zip(p,p[1:]+p[:1]) if (x+y)%2 == 0)
            p = [(x-s//2)%k for x in p]
        row = after(p,0)[:-1]
    return [(x+surplus)%k for x in row]


def pendant(k, joint, surplus, count):
    """Grow a path from an order-one core, with no bound on its new length."""
    if k < 1 or count < 0:
        raise ValueError("invalid path parameters")
    periods,t = divmod(count,k)
    a = (joint-surplus)%k
    if t < 3:
        row = [] if not t else [1]
        if t == 2:
            z = next(x for x in range(1,k) if x != a)
            row = [next(x for x in range(1,k) if x != z),z]
    elif a:
        left = max(1,a-t+1)
        row = after([x+left for x in interval_cycle(t)],a)
    else:
        row = [j//2 if j%2 == 0 else (t+2)//2+j//2 for j in range(1,t+1)]
    row = [(x+surplus)%k for x in row]
    for _ in range(periods):
        last = row[-1] if row else joint
        row.extend((last+j//2+(k//2+1)*(j%2))%k for j in range(1,k+1))
    return row


def divisible_period(k, endpoint, deficit):
    """One period of inserted vertices. Return the row and the new deficit."""
    if k%2:
        return [(endpoint+i)%k for i in range(1,k+1)],deficit
    return after(half_weights(k,deficit),endpoint),(deficit+k//2)%k


def finish_divisible(k, chain, deficit, t):
    """Insert a final t<k vertices along a chain containing all but at most one bin."""
    if t == 0:
        return chain
    if t == 1:
        i = next(i for i,x in enumerate(chain) if 2*x%k == deficit)
        return chain[:i+1]+[chain[i]]+chain[i+1:]
    if t == 2:
        for i,(u,v) in enumerate(zip(chain,chain[1:])):
            if (2*(u-v))%k == 0:
                continue
            x = (deficit-u)%k
            z = (u+v-x)%k
            if x == z:
                z = (deficit-v)%k
                x = (u+v-z)%k
            return chain[:i+1]+[x,z]+chain[i+1:]
        raise AssertionError("three consecutive distinct labels force a usable edge")
    p = interval_cycle(t)
    w = next(x+y for x,y in zip(p,p[1:]+p[:1]) if k%2 or (x+y-deficit)%2 == 0)
    shift = ((deficit-w)*pow(2,-1,k))%k if k%2 else (deficit-w)//2
    p = [(x+shift)%k for x in p]
    slots = set(p)
    i = next(i for i,x in enumerate(chain) if x in slots)
    return chain[:i+1]+after(p,chain[i])+chain[i+1:]


def insert(k, a, b, surplus, count):
    """Insert count vertices on a prescribed edge of an order-one-residue core."""
    if k < 5 or count < 0:
        raise ValueError("requires modulus at least five and nonnegative length")
    a,b,surplus = a%k,b%k,surplus%k
    if count == 1:
        if a == b == surplus:
            raise ValueError("both endpoints carry the forbidden surplus")
        return [a if a != surplus else b]
    if count%k == 0:
        periods = count//k
        if k%2:
            return [(a+i)%k for i in range(1,k+1)]*periods
        if periods%2:
            if k%4 == 2:
                raise ValueError("the surplus shift cannot double to an odd residue")
            first = short(k,a,b,surplus,k-1)
            # The edge deficit is now 2*surplus-k/2. Both its half-residues
            # occur on the chain since neither is the previously omitted surplus.
            chain = finish_divisible(k,[a,*first,b],(2*surplus-k//2)%k,1)
            return chain[1:-1]+insert(k,chain[-2],b,surplus,count-k)
        row = [(a+i//2 if i%2 == 0 else b+i//2)%k for i in range(1,2*k+1)]
        return row*(periods//2)
    if count < k:
        return short(k,a,b,surplus,count)
    row = short(k,a,b,surplus,k-1)
    chain = [a,*row,b]
    weights = [(u+v)%k for u,v in zip(chain,chain[1:])]
    weights.remove((a+b)%k)
    deficit, = set(range(k))-set(weights)
    periods,tail = divmod(count-(k-1),k)
    for _ in range(periods):
        block,deficit = divisible_period(k,row[-1],deficit)
        row.extend(block)
    chain = finish_divisible(k,[a,*row,b],deficit,tail)
    return chain[1:-1]


def long_divisible(k, a, b, deficit, count):
    """Subdivide one edge of a prescribed divisible core by at least one period."""
    if k < 5 or count < k:
        raise ValueError("requires modulus at least five and at least one period")
    a,b,deficit = a%k,b%k,deficit%k
    periods,tail = divmod(count,k)
    row = []
    for _ in range(periods):
        period,deficit = divisible_period(k,a,deficit)
        row.extend(period)
    if tail == 1 and k%2 == 0 and deficit%2:
        raise ValueError("no vertex label doubles to the required deficit")
    return finish_divisible(k,[a,*row,b],deficit,tail)[1:-1]

"""Restore prescribed histograms between two fixed labeled trees using path blocks."""
from .prescribed_path_surplus import prescribe


def moment(counts):
    return sum(x*n for x,n in enumerate(counts))


def subset_sum(k, size, target):
    """A proper nonempty subset of prescribed size and residue sum."""
    if not 0 < size < k:
        raise ValueError("The subset must be nonempty and proper")
    values = list(range(size))
    extra = (target-sum(values))%k
    for i in reversed(range(size)):
        step = min(k-size,extra)
        values[i] += step
        extra -= step
    assert extra == 0
    return values


def blocks_needed(vertices,weights,t):
    k = len(vertices)
    threshold = max(1, k*max(vertices)-sum(vertices), k*max(weights)-sum(weights)-1)
    return threshold+(t-threshold)%k


def realize(a,b,t,vertices,weights,final_v,final_e,s):
    """Return the internal labels for feasible target counts and a block count s."""
    k = len(vertices)
    q0 = 2 if k%4 == 0 else 1
    if s < 1 or (t-s)%k or t < s*(q0*k+1):
        raise ValueError("Insufficient path length for these blocks")
    periods = (t-s)//k
    extras = [f-v-periods for f,v in zip(final_v,vertices)]
    joins = [f-w-periods for f,w in zip(final_e,weights)]
    if min(extras+joins) < 0 or sum(extras) != s or sum(joins) != s+1:
        raise ValueError("Incompatible target sizes")
    if (moment(joins)-2*moment(extras)-a-b-periods*sum(range(k)))%k:
        raise ValueError("Incompatible endpoint moment")
    x = [i for i,count in enumerate(extras) for _ in range(count)]
    w = [i for i,count in enumerate(joins) for _ in range(count)]
    row = []
    last = a
    for j,surplus in enumerate(x):
        q = periods-(s-1)*q0 if j == 0 else q0
        part = prescribe(k,0,q*k,surplus,(w[j]-last)%k)
        row.extend(part)
        last = part[-1]
    assert (last+b)%k == w[-1]
    return row


def bridge(a,b,t,vertices,weights):
    """Balance both histograms. None signifies the necessary parity obstruction."""
    k = len(vertices)
    if k == 1:
        return [0]*t
    if len(weights)!=k or sum(vertices)-sum(weights)!=2:
        raise ValueError("Expected the combined histograms of two trees")
    s = blocks_needed(vertices,weights,t)
    q0 = 2 if k%4 == 0 else 1
    if t < s*(q0*k+1):
        raise ValueError("Outside the sufficient length bound")
    n = sum(vertices)+t
    q,r = divmod(n,k)
    qe,re = divmod(n-1,k)
    total = sum(range(k))
    invariant = moment(weights)-2*moment(vertices)+a+b
    if re:
        high_v = list(range(r))
        target = invariant+2*(q*total+sum(high_v))-qe*total
        high_e = subset_sum(k,re,target)
    else:
        target = (-q*total-invariant)%k
        surplus = next((x for x in range(k) if 2*x%k == target),None)
        if surplus is None:
            return None
        high_v,high_e = [surplus],[]
    final_v = [q+(x in high_v) for x in range(k)]
    final_e = [qe+(x in high_e) for x in range(k)]
    return realize(a,b,t,vertices,weights,final_v,final_e,s)


def pinned_path(k,n,pins):
    """Label a path of order n with the stipulated separation between its pins."""
    if k < 1 or n < 0 or any(not 0 <= i < n or not 0 <= x < k for i,x in pins.items()):
        raise ValueError("Invalid modulus, order or pin")
    if k == 1:
        return [0]*n
    if len(pins) <= 1:
        row = [(i//2 + (i%2)*((n+1)//2))%k for i in range(n)]
        if pins:
            pos,x = next(iter(pins.items()))
            shift = x-row[pos]
            row = [(a+shift)%k for a in row]
        return row
    if k%2==0 and n%k==1:
        if 0 in pins and n-1 in pins:
            if (pins[0]+pins[n-1]-(n//k)*sum(range(k)))%2:
                return None
        else:
            reverse = n-1 in pins
            positions = {(n-1-i if reverse else i):x for i,x in pins.items()}
            row = pinned_path(k,n-1,positions)
            counts = [0]*k
            for x,y in zip(row,row[1:]):
                counts[(x+y)%k] += 1
            row.append((counts.index(min(counts))-row[-1])%k)
            return row[::-1] if reverse else row
    positions = sorted(pins)
    mid = len(positions)//2
    left_end = (positions[mid-1]//k+1)*k
    q0 = 2 if k%4==0 else 1
    t = k*(q0*k+1) + n%k
    right_start = left_end+t
    if right_start > positions[mid]:
        raise ValueError("Pins too close for the long-bridge construction")
    first = pinned_path(k,left_end,{i:pins[i] for i in positions[:mid]})
    second = pinned_path(k,n-right_start,{i-right_start:pins[i] for i in positions[mid:]})
    vertices = [0]*k
    weights = [0]*k
    for part in (first,second):
        for x in part:
            vertices[x] += 1
        for x,y in zip(part,part[1:]):
            weights[(x+y)%k] += 1
    middle = bridge(first[-1],second[0],t,vertices,weights)
    if middle is None:
        raise ArithmeticError("A compatible endpoint parity failed to glue")
    return first+middle+second

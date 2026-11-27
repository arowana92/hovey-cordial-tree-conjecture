"""Extend a prescribed cordial core of order one modulo k over a path."""

from math import gcd

from .four_leaves import available, endpoint, marked, staircase


def join(left, right):
    n = len(left)
    return left + [x + (n+1-(n+i)%2)//2 for i,x in enumerate(right)]


def rank_window(a, b, h):
    """Attain h or h-1 on a sufficiently long marked path of either parity."""
    if a > b:
        return rank_window(b,a,h)[::-1]
    n = a+b+1
    if h < 1 or n < 6*h + (-1 if n%2 else 2):
        raise ValueError((a,b,h))
    if (a,b,h) == (4,4,1):
        return marked(a,b,0)
    for x in (h, h-1):
        for near, far in ((a,b), (b,a)):
            y = near//2-x
            if available(near+1,x) and available(far,y):
                row = join(endpoint(near+1,x)[::-1],endpoint(far,y))
                return row if near == a else row[::-1]
        z = x-a//2
        if available(a,z) and available(b+1,z):
            return join(endpoint(a,z),endpoint(b+1,z))
        for length in (a+2*x+1, a+2*x+2):
            y = (length-1)//2
            if length <= n and available(n-length,y):
                return join(staircase(length)[::-1],endpoint(n-length,y))
    raise AssertionError("path rank window")


def two_blocks(left, right, low_left, low_right):
    """Give the two paths consecutive ranks within each common class."""
    low = (len(left)+1-low_left)//2
    high = len(left)-low
    total_low = low+(len(right)+1-low_right)//2
    first = [1+x+(0 if i%2==low_left else total_low) for i,x in enumerate(left)]
    second = [1+x+(low if i%2==low_right else total_low+high) for i,x in enumerate(right)]
    return first+second


def half_turn(k, at):
    n = k-1
    other = n-1-at
    if at%2 == 0:
        ranks = marked(at,other,0)
        return [1+x+(k//2 if i%2 else 0) for i,x in enumerate(ranks)]
    if other >= 3 and other != 5:
        left = endpoint(at+1,0)[::-1]
        right = endpoint(other,(other-3)//2)
        return two_blocks(left,right,1,0)
    if at >= 3 and at != 5:
        return half_turn(k,other)[::-1]
    if at > other:
        return half_turn(k,other)[::-1]
    return list({(1,1):(1,2,3), (1,5):(1,2,6,7,3,4,5),
                 (5,5):(1,2,3,4,8,10,11,9,5,6,7)}[at,other])


def quarter_turn(k, at):
    """Normalize the parent to k/4 and use the gap between two path blocks."""
    n, d = k-1, k//4
    if at > n-1-at:
        return quarter_turn(k,n-1-at)[::-1]
    if at == 2*d-1:
        # The mark has rank d-1 in the upper class. Negate the solution at -d.
        return [(-1-x-(2*d if i%2 else 0))%k for i,x in enumerate(staircase(n))]
    m = d+at//2
    s = n-m
    low_left = 1-at%2
    end_high = (m-1)%2 != low_left
    diff = (s+1)//2-(m+1)//2
    ranks = (diff,diff+1 if end_high else diff-1)
    x = next(y for y in ranks if available(s,y))
    return two_blocks(staircase(m),endpoint(s,x),low_left,int(end_high))


def full_path(k, at, parent):
    """Label k-1 vertices with all nonzero residues and distinct incoming/internal sums."""
    n = k-1
    parent %= k
    if at == n-1 and at:
        return full_path(k,0,parent)[::-1]
    if (k,at) == (6,2):
        return list(((1,2,4,3,5), (1,2,4,3,5), (1,3,5,4,2), (2,5,3,1,4),
                     (1,3,2,5,4), (1,3,2,4,5))[parent])
    if at == 0:
        size = (n+1)//2
        for rank in range(size):
            if not available(n,rank):
                continue
            lower = parent in ((size-1-rank)%k,(size-rank)%k)
            if lower or parent in ((-1-rank)%k,(-rank)%k):
                row = endpoint(n,rank)
                break
        else:
            raise AssertionError("endpoint rank coverage")
        unit = 1
    elif parent == 0:
        row = marked(at,n-1-at,0)
        lower, unit = False, 1
    else:
        d = gcd(k,parent)
        order = k//d
        if order == 2:
            return half_turn(k,at)
        if order == 4:
            row = quarter_turn(k,at)
            return row if parent == d else [(-v)%k for v in row]
        lower = order%2 == 1
        target = (k-d)//2 if lower else -d
        own = (n+1-at%2)//2
        rank = own-target if lower else d
        row = rank_window(at,n-1-at,rank) if rank else marked(at,n-1-at,0)
        unit = next(c for c in range(1,k) if gcd(c,k)==1 and c*target%k==parent)
    low_side = at%2 if lower else 1-at%2
    low_size = (n+1-low_side)//2
    return [unit*(1+x+(0 if i%2==low_side else low_size))%k for i,x in enumerate(row)]


def partial(k, n, at, parent, surplus):
    """Pad at the far end, retaining the marked position and the supplied surplus."""
    if at == n-1:
        return [(v+surplus)%k for v in full_path(k,0,parent-surplus)[:n]][::-1]
    return [(v+surplus)%k for v in full_path(k,at,parent-surplus)[:n]]


def restore_periods(k, a, b, row):
    def grow(start, length):
        tail = []
        for _ in range(length//k):
            chunk = [(start+i//2+(k//2+1)*(i%2))%k for i in range(1,k+1)]
            tail.extend(chunk)
            start = chunk[-1]
        return tail
    return grow(row[0],a)[::-1]+row+grow(row[-1],b)


def core_path(k, a, b, parent, surplus):
    """The two distances from the vertex adjacent to the old parent are a and b."""
    if min(a,b) < 0 or k < 1:
        raise ValueError((k,a,b))
    if k == 1:
        return [0]*(a+b+1)
    if a > b:
        return core_path(k,b,a,parent,surplus)[::-1]
    left, right = a%k, b%k
    n = left+right+1
    if n <= k-1:
        row = partial(k,n,left,parent,surplus)
    else:
        # Reserve the leftmost vertex if the left side alone fills k-1 positions.
        skip = int(left == k-1)
        row = partial(k,k-1,left-skip,parent,surplus)
        weights = {(x+y)%k for x,y in zip(row,row[1:])}
        weights.add((parent+row[left-skip])%k)
        missing, = set(range(k))-weights
        fill = (missing-(row[0] if skip else row[-1]))%k
        row = [fill]+row if skip else row+[fill]
        if n > k:
            row.extend(partial(k,n-k,0,row[-1],fill))

    return restore_periods(k,a,b,row)


def divisible_path(k, a, b, parent, deficit):
    """Attach a path to a core of order zero modulo k with the given missing weight."""
    if min(a,b) < 0 or k < 1:
        raise ValueError((k,a,b))
    base = [i//2+(i%2)*((k+1)//2) for i in range(k)]
    left = a%k
    n = left+b%k+1
    shift = deficit-parent-base[left]
    row = [(v+shift)%k for v in base[:n]]
    if n > k:
        internal = {(x+y)%k for x,y in zip(row,row[1:])}
        missing, = set(range(k))-internal
        shift = missing-row[-1]
        row.extend((v+shift)%k for v in base[:n-k])
    return restore_periods(k,a,b,row)

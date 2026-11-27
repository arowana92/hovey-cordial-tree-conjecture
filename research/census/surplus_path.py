"""Extend a prescribed cordial core of order one modulo k over a path."""

from math import gcd

from .four_leaves import available, endpoint, marked, staircase


def join(left, right):
    n = len(left)
    return left + [x + (n+1-(n+i)%2)//2 for i,x in enumerate(right)]


def rank_window(a, b, h):
    """On an even path of order at least 6h+2 attain h or h-1 at position a."""
    if a > b:
        return rank_window(b,a,h)[::-1]
    n = a+b+1
    if h < 1 or n%2 or n < 6*h+2:
        raise ValueError((a,b,h))
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
    raise AssertionError("even-path rank window")


def full_path(k, at, parent):
    """Label k-1 vertices with all nonzero residues and distinct incoming/internal sums."""
    n = k-1
    parent %= k
    if at == n-1 and at:
        return full_path(k,0,parent)[::-1]
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
    elif k%2 and parent == 0:
        row = marked(at,n-1-at,0)
        lower, unit = False, 1
    elif k%2:
        d = gcd(k,parent)
        rank = (d-1)//2
        row = rank_window(at,n-1-at,rank) if rank else marked(at,n-1-at,0)
        target = (k-d)//2
        unit = next(c for c in range(1,k) if gcd(c,k)==1 and c*target%k==parent)
        lower = True
    else:
        raise ValueError("interior attachment requires an odd modulus")
    low_side = at%2 if lower else 1-at%2
    low_size = (n+1-low_side)//2
    return [unit*(1+x+(0 if i%2==low_side else low_size))%k for i,x in enumerate(row)]


def partial(k, n, at, parent, surplus):
    """Pad at the far end, retaining the marked position and the supplied surplus."""
    if at == n-1:
        return [(v+surplus)%k for v in full_path(k,0,parent-surplus)[:n]][::-1]
    return [(v+surplus)%k for v in full_path(k,at,parent-surplus)[:n]]


def core_path(k, a, b, parent, surplus):
    """The two distances from the vertex adjacent to the old parent are a and b."""
    if min(a,b) < 0 or k < 1 or (k%2 == 0 and min(a,b) != 0):
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

    def periods(start, length):
        tail = []
        for _ in range(length//k):
            chunk = [(start+i//2+(k//2+1)*(i%2))%k for i in range(1,k+1)]
            tail.extend(chunk)
            start = chunk[-1]
        return tail

    return periods(row[0],a)[::-1]+row+periods(row[-1],b)

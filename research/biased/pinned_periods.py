"""Cordial extensions with specified labels at all parents in a rooted tree."""

from collections import Counter, defaultdict, deque

from research.large_order_hall_pools import hall_pair, zero_block


def marked_periods(k, shifts, pins):
    """Realize balanced input/output periods, translating one marked row per block.

    Raises ValueError if this zero-sum partition cannot separate the pins.
    The frequency inequalities in the theorem guarantee success.
    """
    if k < 1:
        raise ValueError("expected a positive modulus")
    shifts = [s%k for s in shifts]
    if not shifts or len(shifts)%k or sum(shifts)%k or any(not 0<=v<len(shifts) for v in pins):
        raise ValueError("expected complete zero-sum periods and valid pin indices")
    frequencies = Counter(shifts)
    counts = [frequencies[a] for a in range(k)]
    blocks = []
    while sum(counts):
        repeated = next((a for a,c in enumerate(counts) if c>=k),None)
        block = (repeated,)*k if repeated is not None else zero_block(counts)
        blocks.append(block)
        for a in block:
            counts[a] -= 1

    by_shift = defaultdict(list)
    for j,block in enumerate(blocks):
        for s in set(block):
            by_shift[s].append(j)
    # Match each pin to a separate block containing its displacement.
    owner = {}
    for pin in pins:
        parents = {pin:None}
        visited = set()
        queue = deque([pin])
        free = None
        while queue and free is None:
            p = queue.popleft()
            for j in by_shift[shifts[p]]:
                if j in visited:
                    continue
                visited.add(j)
                if j not in owner:
                    free = j
                    break
                nxt = owner[j]
                if nxt not in parents:
                    parents[nxt] = (p,j)
                    queue.append(nxt)
        if free is None:
            raise ValueError("this partition cannot separate the pinned rows")
        owner[free] = p
        while parents[p] is not None:
            p,j = parents[p]
            owner[j] = p

    available = defaultdict(list)
    for i,s in enumerate(shifts):
        if i not in pins:
            available[s].append(i)
    labels = [None]*len(shifts)
    for j,block in enumerate(blocks):
        sources = [-x%k for x,_ in hall_pair(block)]
        pin = owner.get(j)
        pos = block.index(shifts[pin]) if pin is not None else None
        offset = pins[pin]-sources[pos] if pin is not None else 0
        for i,(s,x) in enumerate(zip(block,sources)):
            v = pin if i==pos else available[s].pop()
            labels[v] = (x+offset)%k
    return labels


def extend(k, parents, offsets, fixed):
    """Label a tree in parent order under the shift-frequency theorem."""
    n = len(parents)
    if k<1 or not n or len(offsets)!=n or parents[0]!=-1 or any(not 0<=p<i for i,p in enumerate(parents[1:],1)):
        raise ValueError("invalid rooted tree or modulus")
    if set(fixed) != (set(parents[1:]) | {0}):
        raise ValueError("prescribe exactly the root and all parents")
    r = n%k
    if n<k*len(fixed):
        raise ValueError("insufficient order for the prescribed-core theorem")
    shifts = [0]+[(fixed[p]+b)%k for p,b in zip(parents[1:],offsets[1:])]
    total = Counter(shifts[1:])
    marked = Counter(shifts[v] for v in fixed if v)
    if any(total[s]<k*m for s,m in marked.items()):
        raise ValueError("shift-frequency condition fails")
    excess = {s:c-k*marked[s] for s,c in total.items()}
    removed = []
    kept = [0]
    for v in range(1,n):
        s = shifts[v]
        if v not in fixed and len(removed)<r and excess[s]:
            removed.append(v)
            excess[s] -= 1
        else:
            kept.append(v)
    assert len(removed)==r
    shifts[0] = -sum(shifts[v] for v in kept[1:])%k
    tags = {i:fixed[v] for i,v in enumerate(kept) if v in fixed}
    core = marked_periods(k,[shifts[v] for v in kept],tags)
    f = [None]*n
    for v,x in zip(kept,core):
        f[v] = x
    if removed:
        first,*rest = removed
        missing = (f[0]+shifts[0])%k
        f[first] = (missing-shifts[first])%k
        if rest:
            requests = [shifts[v] for v in rest]+[0]*(k-1-len(rest))
            requests.append(-sum(requests)%k)
            source = [-a%k for a,_ in hall_pair(requests)]
            move = f[first]-source[-1]
            for v,x in zip(rest,source):
                f[v] = (x+move)%k
    return f


def uniform_star(k, offsets, children):
    """Uniformly label a full-period attachment, with its only free parent at row 0.

    At externally attached rows the offset includes the fixed external parent.
    At children of row zero it is the additive edge offset alone.
    Return None exactly when the degree congruence is insoluble.
    """
    children = set(children)
    if k<1 or not offsets or len(offsets)%k or any(not 1<=v<len(offsets) for v in children):
        raise ValueError("expected full periods and children of row zero")
    total = sum(offsets)
    x = next((a for a in range(k) if (len(children)*a+total)%k==0),None)
    if x is None:
        return None
    shifts = [(s+(x if i in children else 0))%k for i,s in enumerate(offsets)]
    return marked_periods(k,shifts,{0:x})

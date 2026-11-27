"""Realize prescribed vertex and weight counts along one subdivided edge."""
from collections import Counter, deque
from research.large_order_hall_pools import hall_pair, pairs_for, zero_block
from research.large_order_subdivision import round_groups


def subset_sum(k, count, target):
    """A count-element subset with prescribed sum modulo k, 0 < count < k."""
    if not 0 < count < k:
        raise ValueError("the subset must be nonempty and proper")
    extra = (target-count*(count-1)//2)%k
    values = list(range(count))
    for i in reversed(range(count)):
        step = min(extra,k-count)
        values[i] += step
        extra -= step
    assert extra == 0
    return values


def moment(hist):
    return sum(i*v for i,v in enumerate(hist))


def target_increments(vertex, edge, t):
    """Choose balanced final bins subject to the one subdivision invariant."""
    k = len(vertex)
    n = sum(vertex)
    qv,rv = divmod(n+t,k)
    qe,re = divmod(n+t-1,k)
    inv = (2*moment(vertex)-moment(edge))%k
    s = k*(k-1)//2
    if re:
        high = sorted(range(k), key=vertex.__getitem__, reverse=True)[:rv]
        wanted = 2*(qv*s+sum(high))-inv-qe*s
        weights = subset_sum(k,re,wanted)
    elif k == 1:
        high,weights = [],[]
    else:
        rhs = (inv-qv*s)%k
        if k%2 == 0 and rhs%2:
            raise ValueError("no balanced target has the required parity")
        high = [(rhs*pow(2,-1,k))%k if k%2 else rhs//2]
        weights = []
    vh,eh = set(high),set(weights)
    return ([qv+(i in vh)-vertex[i] for i in range(k)],
            [qe+(i in eh)-edge[i] for i in range(k)])


def circuit(vertex, edge, start):
    """Return heads of an Euler circuit with the specified transition margins."""
    k = len(vertex)
    if k == 0 or len(edge) != k or sum(vertex) != sum(edge) or min(vertex) < 1:
        raise ValueError("incompatible transition counts")
    if (2*moment(vertex)-moment(edge))%k:
        raise ValueError("incompatible weight sum")
    c = min(vertex)
    arcs = [[] for _ in range(k)]
    left = list(edge)
    # One spanning directed cycle and the surplus visits at each residue.
    for x in range(k):
        successor = (x+1)%k
        arcs[x].append(successor)
        left[(x+successor)%k] -= 1
        extra = vertex[x]-c
        arcs[x].extend([x]*extra)
        left[2*x%k] -= extra
    if min(left) < 0:
        raise ValueError("insufficient weights for the spanning cycle and extra loops")
    # Two uniform layers can be stripped without zero-sum subset search.
    layers = min(left)//2
    if layers:
        for x in range(k):
            arcs[x].extend([x,(x+1)%k]*layers)
            left[x] -= 2*layers
    for x,y in pairs_for(left):
        arcs[x].append(y)
    walk = []
    stack = [start%k]
    while stack:
        x = stack[-1]
        if arcs[x]:
            stack.append(arcs[x].pop())
        else:
            walk.append(stack.pop())
    walk.reverse()
    assert walk[0] == walk[-1] == start%k and len(walk) == 1+sum(vertex)
    return walk[1:]


def extend(vertex, edge, t, endpoint):
    v,w = target_increments(vertex,edge,t)
    return circuit(v,w,endpoint)


def bfs_padding(k, parents, chosen, t):
    """Construct a cordial labeling after t>=n+3k-3 subdivisions of any one edge.

    Vertices must be in breadth-first order with siblings consecutive. The edge
    leads to vertex chosen. Return its original vertex labels and inserted row.
    """
    n = len(parents)
    if not 1 <= chosen < n or parents[0] != -1 or parents[1:] != sorted(parents[1:]):
        raise ValueError("need an edge of a breadth-first parent array")
    if k < 1 or t < n+3*k-3:
        raise ValueError("outside the sufficient padding range")
    if n == 2:
        size = 2+t
        path = [(i//2+(i%2)*((size+1)//2))%k for i in range(size)]
        return [path[0],path[-1]],path[1:-1]
    # At final residue one, set aside an original leaf off the chosen edge.
    skip = None
    if (n+t)%k == 1:
        internal = set(parents[1:])
        skip = next(i for i in range(n) if (i not in internal or
                    (i==0 and parents.count(0)==1)) and i not in (chosen,parents[chosen]))
    # Compact the breadth-first indices across a skipped leaf. This also works
    # if the skipped vertex is the original root of degree one.
    f = [(i-int(skip is not None and skip < i))%k for i in range(n)]
    v = Counter(x for i,x in enumerate(f) if i != skip)
    w = Counter((f[i]+f[p])%k for i,p in enumerate(parents) if i and i != skip and p != skip)
    raw_v,raw_w = [v[i] for i in range(k)],[w[i] for i in range(k)]
    row = extend(raw_v,raw_w,t,f[parents[chosen]])
    if skip is not None:
        chain = [f[parents[chosen]],*row,f[chosen]]
        w.subtract([(chain[0]+chain[-1])%k])
        w.update((a+b)%k for a,b in zip(chain,chain[1:]))
        d = min(range(k),key=w.__getitem__)
        neighbor = parents[skip] if skip else parents.index(0)
        f[skip] = (d-f[neighbor])%k
    return f,row


def one_neighbor(k, parents):
    """Choose labels at sites with one fixed neighbor, keeping both spreads <=2."""
    sites = [deque() for _ in range(k)]
    for i,p in enumerate(parents):
        sites[p].append(i)
    labels = [None]*len(parents)

    def place(block):
        padded = list(block)
        if len(padded) < k:
            padded.extend([0]*(k-len(padded)-1))
            padded.append(-sum(block)%k)
        for p,(x,_) in zip(block,hall_pair(padded)):
            labels[sites[p].popleft()] = -x%k

    left = len(parents)
    while left >= 2*k-1:
        place(zero_block([len(row) for row in sites]))
        left -= k
    rest = [p for p,row in enumerate(sites) for _ in row]
    if rest:
        place(rest[:k-1])
        if len(rest) >= k:
            place(rest[k-1:])
    return labels


def skeleton(parents,mark=None):
    """Return neighbors, breadth-first pins, and maximal open degree-two runs."""
    neighbors = [[] for _ in parents]
    for i,p in enumerate(parents[1:],1):
        neighbors[i].append(p)
        neighbors[p].append(i)
    pins = {i for i,row in enumerate(neighbors) if len(row) != 2}
    if mark is not None:
        pins.add(mark)
    root = min(pins) if mark is None else mark
    queue = deque([root])
    assigned = {root}
    order,runs = [],[]
    while queue:
        pin = queue.popleft()
        order.append(pin)
        for nxt in neighbors[pin]:
            previous,current = pin,nxt
            inside = []
            while current not in pins:
                inside.append(current)
                a,b = neighbors[current]
                previous,current = current,b if a==previous else a
            if current in assigned:
                continue
            assigned.add(current)
            queue.append(current)
            runs.append(inside)
    return neighbors,order,runs


def fill_gaps(k,neighbors,labels,gaps):
    """Label all open paths between fixed endpoints with bounded discrepancy."""
    first,second = [],[]
    for inside in gaps:
        first.extend(inside[1::2])
        second.extend(inside[::2])

    def fixed(i):
        return [labels[j] for j in neighbors[i] if labels[j] is not None]

    near = [i for i in first if fixed(i)]
    free = [i for i in first if not fixed(i)]
    partial = one_neighbor(k,[fixed(i)[0] for i in near])
    uses = Counter(partial)
    for i,x in zip(near,partial):
        labels[i] = x
    for i in free:
        x = min(range(k),key=uses.__getitem__)
        labels[i] = x
        uses[x] += 1
    # Full batches of identical neighbor pairs have an exact uniform choice.
    by_pair = {}
    for i in second:
        pair = tuple(sorted(fixed(i)))
        by_pair.setdefault(pair,[]).append(i)
    remainder = []
    for batch in by_pair.values():
        cut = len(batch)-len(batch)%k
        for j,i in enumerate(batch[:cut]):
            labels[i] = j%k
        remainder.extend(batch[cut:])
    groups = []
    for i in remainder:
        a,b = fixed(i)
        choices = []
        for x in range(k):
            column = [0]*(2*k)
            column[x] = 2
            column[k+(x+a)%k] += 1
            column[k+(x+b)%k] += 1
            choices.append(column)
        groups.append(choices)
    for i,x in zip(remainder,round_groups(groups,2*k)):
        labels[i] = x
    return labels


def approximate_tree(k,parents):
    """Color a tree with h skeleton vertices for the uniform bare-path bound."""
    neighbors,pins,runs = skeleton(parents)
    labels = [None]*len(parents)
    for j,pin in enumerate(pins):
        labels[pin] = j%k
    return fill_gaps(k,neighbors,labels,runs)

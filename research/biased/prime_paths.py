"""Find biased prime path blocks and join them with prescribed boundary data."""

from research.prime.verify_templates import primes_through


def block(p, offsets):
    """One full permutation along a path, with root zero and distinct edge weights."""
    if p not in primes_through(p) or len(offsets)!=p-1:
        raise ValueError("expected a prime and p-1 offsets")
    values = [0]
    all_bits = (1<<p)-1

    def visit(vertices, weights):
        if len(values)==p:
            return (all_bits ^ weights).bit_length()-1
        shift = (values[-1]+offsets[len(values)-1])%p
        free = all_bits^weights
        choices = (all_bits^vertices)&((free>>shift)|(free<<(p-shift)))
        while choices:
            bit = choices & -choices
            choices -= bit
            x = bit.bit_length()-1
            w = (x+shift)%p
            values.append(x)
            missing = visit(vertices|bit,weights|(1<<w))
            if missing is not None:
                return missing
            values.pop()
        return None

    missing = visit(1,0)
    if missing is None:
        raise AssertionError("no full prime path block")
    return values,missing


def pendant(p, parent, offsets):
    """A path adding p vertices and p edges uniformly at the given parent."""
    if len(offsets)!=p:
        raise ValueError("expected p new edges")
    f,missing = block(p,offsets[1:])
    # Parent+offset[0]+f[0]+s has to be missing+2s after translation.
    s = parent+offsets[0]+f[0]-missing
    return [(x+s)%p for x in f]


def path(p, offsets):
    n = len(offsets)+1
    first = (n-1)%p+1
    initial,_ = block(p,[*offsets[:first-1],*([0]*(p-first))])
    f = initial[:first]
    while len(f)<n:
        i = len(f)-1
        f.extend(pendant(p,f[-1],offsets[i:i+p]))
    return f


def two_paths(p, labels, arms, deficit):
    """Extend a divisible-order core by at most p edges on one or two paths.

    An arm is (old parent, [(free vertex, edge offset), ...]). Write all new labels.
    """
    arms = [(v,list(steps)) for v,steps in arms if steps]
    if not 1<=len(arms)<=2 or sum(len(steps) for _,steps in arms)>p:
        raise ValueError("expected one or two nonempty arms of total length at most p")
    parent,steps = arms[0]
    first,b = steps.pop(0)
    x = (deficit-labels[parent]-b)%p
    labels[first] = x
    arms[0] = (first,steps)
    adjusted = []
    for parent,steps in arms:
        if steps:
            vertices,offsets = map(list,zip(*steps))
            offsets[0] += labels[parent]-x
            adjusted.append((vertices,offsets))
        else:
            adjusted.append(([],[]))
    if len(adjusted)==1:
        adjusted.append(([],[]))
    (left,lb),(right,rb) = adjusted
    order = [*reversed(left),None,*right]
    bias = [*reversed(lb),*rb,*([0]*(p-len(order)))]
    f,_ = block(p,bias)
    shift = x-f[len(left)]
    for v,y in zip(order,f):
        if v is not None:
            labels[v] = (y+shift)%p


def subdivision(p, order, edges, biases):
    """Parents precede children in edges. Each edge carries its path's list of offsets."""
    if len(edges)!=order-1 or len(biases)!=len(edges):
        raise ValueError("expected a rooted coarse tree")
    routes = []
    next_id = order
    for (parent,child),offsets in zip(edges,biases):
        L = len(offsets)
        if L<p-1:
            raise ValueError("every path must have length at least p-1")
        ids = [*range(next_id,next_id+L-1),child]
        next_id += L-1
        routes.append((parent,list(zip(ids,offsets))))
    if not routes:
        return [0]
    labels = [None]*next_id
    pending = []
    remaining = p-1
    first = True
    deficit = None
    for parent,steps in routes:
        start = 0
        while start<len(steps):
            part = steps[start:start+remaining]
            pending.append((parent,part))
            start += len(part)
            parent = part[-1][0]
            remaining -= len(part)
            if remaining==0:
                if first:
                    (root,initial), = pending
                    f,deficit = block(p,[b for _,b in initial])
                    labels[root] = f[0]
                    for (v,_),y in zip(initial,f[1:]):
                        labels[v] = y
                    first = False
                else:
                    arms = merge_paths(pending)
                    two_paths(p,labels,arms,deficit)
                    # The relative old weight counts are -1 at deficit and zero elsewhere.
                    frequencies = [0]*p
                    frequencies[deficit] = -1
                    for u,segment in arms:
                        for v,b in segment:
                            frequencies[(labels[u]+labels[v]+b)%p] += 1
                            u = v
                    deficit = frequencies.index(0)
                remaining,pending = p,[]
    if pending:
        two_paths(p,labels,merge_paths(pending),deficit)
    return labels


def merge_paths(parts):
    if len(parts)==2 and parts[0][1][-1][0]==parts[1][0]:
        return [(parts[0][0],parts[0][1]+parts[1][1])]
    return parts

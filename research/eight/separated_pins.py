"""Construct the separated precoloring theorem at eight and nine labels."""
from collections import deque

from .bridge_pins import bridge


def traversal(graph, roots):
    parent = dict.fromkeys(roots)
    order = list(parent)
    for v in order:
        for u in graph[v]:
            if u not in parent:
                parent[u] = v
                order.append(u)
    return order, parent


def grow(k, graph, labels):
    """Keep a divisible core and search one actual forest of at most k at a time."""
    order,parent = traversal(graph, labels)
    counts = [0]*k
    for v in labels:
        for u in graph[v]:
            if u in labels and u < v:
                counts[(labels[v]+labels[u])%k] += 1
    for i in range(len(labels),len(order),k):
        batch = order[i:i+k]
        ceil = min(counts) + (1 if len(batch)==1 else 2)

        def fill(j, used):
            if j == len(batch):
                return max(counts)-min(counts) <= 1
            u = batch[j]
            for x in range(k):
                w = (labels[parent[u]] + x) % k
                if used >> x & 1 or counts[w] == ceil:
                    continue
                labels[u] = x
                counts[w] += 1
                if fill(j+1, used | (1 << x)):
                    return True
                counts[w] -= 1
                del labels[u]
            return False

        if not fill(0,0):
            raise ArithmeticError("A divisible-core attachment had no witness")
    return labels


def one_pin(k, graph, root, fixed):
    order,parent = traversal(graph,[root])
    base = order[:k]
    labels = {root:fixed}

    def visit(i, vertices, weights):
        if i == len(base):
            return True
        u = base[i]
        for x in range(k):
            w = (x + labels[parent[u]]) % k
            if vertices >> x & 1 or weights >> w & 1:
                continue
            labels[u] = x
            if visit(i+1, vertices | (1 << x), weights | (1 << w)):
                return True
            del labels[u]
        return False

    if not visit(1,1<<fixed,0):
        raise ArithmeticError("No labeling of the ordinary base")
    return grow(k,graph,labels)


def induced(graph, vertices):
    return {v:graph[v] & vertices for v in vertices}


def split(k, core, pins):
    root = next(iter(pins))
    order,parent = traversal(core,[root])
    mass, marks = {}, {}
    residue = len(core)%k
    t = residue if residue >= 3 else k+residue
    for v in reversed(order):
        children = [u for u in core[v] if u != parent[v]]
        mass[v] = 1 + sum(mass[u] for u in children)
        marks[v] = int(v in pins) + sum(marks[u] for u in children)
        if v == root or (len(core)-mass[v])%k or not 0 < marks[v] < len(pins):
            continue
        prev,u = parent[v],v
        chain = []
        while len(chain) < t and u not in pins and len(core[u]) == 2:
            chain.append(u)
            prev,u = u,next(iter(core[u]-{prev}))
        if len(chain) == t:
            right = {u}
            todo = [u]
            for w in todo:
                for z in core[w]:
                    if parent[z] == w:
                        right.add(z)
                        todo.append(z)
            left = set(core)-right-set(chain)
            return left, right, chain, parent[v], u
    raise ValueError("No aligned unmarked corridor in this core")


def label(k, graph, pins):
    """Return actual labels on an integer-indexed tree under the theorem's hypotheses."""
    if not graph and not pins:
        return {}
    if len(pins) <= 1:
        root = next(iter(pins),next(iter(graph)))
        return one_pin(k,graph,root,pins.get(root,0))

    # Remove unmarked tips to obtain the subtree spanned by all pins.
    degree = {v:len(adj) for v,adj in graph.items()}
    tips = deque(v for v in graph if degree[v]==1 and v not in pins)
    hull = set(graph)
    while tips:
        v = tips.popleft()
        hull.remove(v)
        for u in graph[v] & hull:
            degree[u] -= 1
            if degree[u]==1 and u not in pins:
                tips.append(u)
    order,_ = traversal(graph,hull)
    take = len(hull) + (-len(hull))%k
    core = induced(graph,set(order[:take]))
    left,right,chain,a,b = split(k,core,pins)
    labels = {}
    gaps = []
    for side in (left,right):
        piece = induced(core,side)
        part = label(k,piece,{v:pins[v] for v in side & pins.keys()})
        counts = [0]*k
        for v in side:
            for u in piece[v]:
                if v < u:
                    counts[(part[v]+part[u])%k] += 1
        gaps.append(counts.index(min(counts)))
        labels.update(part)

    row = bridge(k,labels[a],labels[b],*gaps,len(chain))
    if row is None:
        raise ValueError("The fixed bridge profiles fail the parity test")
    labels.update(zip(chain,row))
    return grow(k,graph,labels)

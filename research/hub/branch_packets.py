"""Construct interval seeds and attach six equally shaped branches per packet."""

from collections import deque


def row_function(offsets):
    width = len(offsets)
    residues = {x % width:x for x in offsets}
    if len(residues) != width:
        raise ValueError("column offsets must represent each residue once")
    return lambda x: (x-residues[x % width])//width


def seed(parents, gap, offsets):
    """Nodes 0 and 1 are the ordered adjacent hubs. Parents precede children."""
    if gap <= 0 or parents[:2] != [-1,0] or any(not 0 <= p < i for i,p in enumerate(parents[1:],1)):
        raise ValueError("expected a positive gap and a tree rooted at the first hub")
    labels = [None]*len(parents)
    labels[:2] = [0,gap]
    highest = gap
    for i in range(2,len(parents)):
        if parents[i] == 0:
            highest += 1
            labels[i] = highest
    start = highest+1
    surplus = start
    for i in range(2,len(parents)):
        if parents[i] == 1:
            labels[i] = surplus
            surplus += gap
    for i in range(2,len(parents)):
        if labels[i] is None:
            labels[i] = surplus
            surplus += labels[parents[i]]
    edges = [(labels[p],labels[i]) for i,p in enumerate(parents) if i]
    if surplus > start:
        edges.extend(((0,start-surplus), (start-surplus,surplus)))
        missing = 0
    else:
        missing = start
        edges.extend(((0,-missing), (-missing,missing)))
    return finish_seed(edges, labels, missing, offsets)


def finish_seed(edges, labels, missing, offsets):
    row = row_function(offsets)
    fixed = {x for edge in edges for x in edge} | {x+y for x,y in edges} | {missing}
    d = max(abs(row(x)) for x in fixed)+2
    width = len(offsets)
    bound = max(abs(x) for x in fixed)+max(abs(c) for c in offsets)+width*(d+1)+1
    left, right = -bound, bound+missing
    edges.extend(((0,right), (right,left)))
    used = {x for edge in edges for x in edge}
    leaves = [x for x in range(left,right+1) if x not in used]
    edges.extend((0,x) for x in leaves)
    return edges, labels, leaves, d


def many_site_seed(parents, core_labels, offsets):
    """Use 2h+1 auxiliary paths, where h counts only the fixed labeled core."""
    h = len(core_labels)
    labels = list(core_labels)+[None]*(len(parents)-h)
    edges = [(labels[parents[i]],labels[i]) for i in range(1,h)]
    weights = {x+y for x,y in edges}
    if (len(set(core_labels)) != h or labels[0] != 0 or min(core_labels) < 0
            or len(weights) != h-1):
        raise ValueError("expected nonnegative distinct core labels, root zero and distinct sums")
    highest = max(set(core_labels) | weights)
    for i in range(h,len(parents)):
        if parents[i] == 0:
            highest += 1
            labels[i] = highest
    running = highest+1
    for i in range(h,len(parents)):
        p = labels[parents[i]]
        if labels[i] is None:
            labels[i] = running
            running += p
        edges.append((p,labels[i]))
    weights = {x+y for x,y in edges}
    used = set(labels)
    extra = sorted(weights-used)
    missing_targets = sorted(used-weights-{0})
    assert len(extra) == len(missing_targets) <= h
    forbidden = used | weights
    for w,v in zip(extra,missing_targets):
        middle = max(map(abs,forbidden))+max(w,v)+1
        first,second = middle-w,v-middle
        edges.extend(((0,first),(first,w),(0,second),(second,middle)))
        forbidden.update((middle,first,second))
    missing = 0
    used = {x for edge in edges for x in edge} | {0}
    for _ in range(2*(h-len(extra))):
        tip = 1
        while tip in used or missing-tip in used or tip == missing-tip:
            tip += 1
        parent = missing-tip
        edges.extend(((0,parent),(parent,tip)))
        used.update((parent,tip))
        missing = tip
    return finish_seed(edges, labels, missing, offsets)


def packet_tree(seed_edges, offsets, d, triples, assignments):
    """One (hub label, root offset, internal edges) per opposed pair of triples."""
    width = len(offsets)
    row = row_function(offsets)
    amount = 3*width*len(triples)

    def move(x):
        i = row(x)
        return x+amount*(int(i >= d)-int(i <= -d))

    edges = [(move(a),move(b)) for a,b in seed_edges]
    if len(triples) != len(assignments):
        raise ValueError("one branch type is required for each group of six")
    for triple, (hub, root, internal) in zip(triples,assignments):
        adjacency = {x:[] for x in offsets}
        for x,y in internal:
            adjacency[x].append(y)
            adjacency[y].append(x)
        colors = {root:0}
        todo = deque([root])
        while todo:
            x = todo.popleft()
            for y in adjacency[x]:
                if y not in colors:
                    colors[y] = 1-colors[x]
                    todo.append(y)
        for sign in (-1,1):
            for i in range(3):
                rows = [sign*triple[i], sign*triple[(i+1)%3]]
                values = {c:width*rows[colors[c]]+c for c in offsets}
                edges.append((hub,values[root]))
                edges.extend((values[x],values[y]) for x,y in internal)
    return edges


def star_types(r):
    offsets = list(range(-1,r))
    def branch(hub,root):
        return hub,root,[(root,x) for x in offsets if x != root]
    return offsets, (branch(0,0),branch(r,-1))


def path_types(length):
    m = length//2
    if length%2:
        order = [x for j in range(m) for x in (m-j,-j-1)]+[0]
    else:
        order = [x for j in range(m) for x in (m-1-j,-j-1)]
    internal = list(zip(order,order[1:]))
    return sorted(order), ((0,order[0],internal),(order[0]-order[-1],order[-1],internal))

"""Finite operations for random palettes and boundary cuts in a branching tree."""

from collections import deque


def palette_law(modulus, rows, columns, independent):
    """Return integer cell masses over modulus squared. Row and column zero are outside."""
    total = sum(rows)
    if total != sum(columns) or not 0 < total <= modulus:
        raise ValueError("incompatible palette sizes")
    if any(x < 0 for x in [*rows, *columns]):
        raise ValueError("negative palette size")
    # Fill the surplus mass by a transportation with the indicated cells forbidden.
    flow = [[0 for _ in columns] for _ in rows]
    room = list(columns)
    for source, need in enumerate(rows):
        while need:
            queue = deque([source])
            previous = {source: None}
            end = None
            while queue and end is None:
                i = queue.popleft()
                if i >= 0:
                    for j in range(len(columns)):
                        node = ~j
                        if node in previous or (i,j) in independent:
                            continue
                        previous[node] = i
                        if room[j]:
                            end = node
                            break
                        queue.append(node)
                else:
                    for row in range(len(rows)):
                        if row not in previous and flow[row][~i]:
                            previous[row] = i
                            queue.append(row)
            if end is None:
                raise ValueError("no admissible transport")
            path = [end]
            while path[-1] != source:
                path.append(previous[path[-1]])
            path.reverse()
            amount = min(need,room[~end])
            for old,new in zip(path,path[1:]):
                if old < 0:
                    amount = min(amount,flow[new][~old])
            for old,new in zip(path,path[1:]):
                if old >= 0:
                    flow[old][~new] += amount
                else:
                    flow[new][~old] -= amount
            need -= amount
            room[~end] -= amount
    outside = modulus-total
    return [[modulus*outside]+[0]*len(columns)]+[
        [0]+[a*b+outside*flow[i][j] for j,b in enumerate(columns)]
        for i,a in enumerate(rows)]


def finish_vertex(modulus, neighbors, vertex_pool, color_pool, endpoint_sum):
    """Find an internal label and an unused gap for a terminal matching.

    The pools contain the unspent labels and weights *before* this vertex lands.
    The caller retains the actual, already assigned leaf-parent labels.
    """
    degree = len(neighbors)
    if degree < 2 or len(set(neighbors)) != degree:
        raise ValueError("need distinct labeled neighbors")
    constant = (sum(color_pool)-sum(vertex_pool)-endpoint_sum-sum(neighbors)) % modulus
    for z in sorted(vertex_pool):
        colors = {(z+p)%modulus for p in neighbors}
        gap = (constant-(degree-1)*z)%modulus
        if colors <= color_pool and gap in color_pool-colors:
            return z,gap
    return None


def rooted_order(graph, root):
    parent = {root: None}
    order = [root]
    for v in order:
        for w in graph[v]:
            if w not in parent:
                parent[w] = v
                order.append(w)
    size = {v:1 for v in order}
    for v in reversed(order[1:]):
        size[parent[v]] += size[v]
    return order,parent,size


def two_suffixes(graph, count):
    """Two disjoint descendant-closed suffixes, each of the prescribed order."""
    n = len(graph)
    if not 1 <= count <= (n-1)//4:
        raise ValueError("need a positive suffix of at most a quarter of the tree")
    order,parent,size = rooted_order(graph,0)
    center = next(v for v in order if max([n-size[v]]+
                  [size[w] for w in graph[v] if parent.get(w)==v]) <= n//2)
    _,parent,size = rooted_order(graph,center)
    roots = sorted(graph[center],key=lambda w:(size[w],w),reverse=True)
    # A single branch in [(n-1)/4,n/2] suffices; otherwise accumulate small ones.
    groups = [[],[]]
    first_size = 0
    for v in roots:
        if first_size < count:
            groups[0].append(v)
            first_size += size[v]
        else:
            groups[1].append(v)
    suffixes = []
    for group in groups:
        stack = group.copy()
        preorder = []
        while stack:
            v = stack.pop()
            preorder.append(v)
            stack.extend(sorted((w for w in graph[v] if parent.get(w)==v),
                                key=lambda w:(size[w],w),reverse=True))
        suffixes.append(set(preorder[-count:]))
    return center,suffixes

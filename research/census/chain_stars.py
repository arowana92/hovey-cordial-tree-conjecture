"""An alpha-labeling of a path of stars from feasible attachment ranks."""


def chain_stars(sizes, joins):
    """Return labels and edges, or None when the forward block construction fails.

    Star i has a center followed by its leaves in index order. Pair i gives
    the leaf indices on the join from star i to star i+1.
    """
    if not sizes or min(sizes) < 1 or len(joins) != len(sizes)-1:
        raise ValueError("invalid chain sizes")
    if any(not (0 <= x < sizes[i] and 0 <= y < sizes[i+1]) for i,(x,y) in enumerate(joins)):
        raise ValueError("invalid attachment leaf")

    incoming = [set()]
    for i,(outgoing_leaf,_) in enumerate(joins):
        if i == 0:
            possible = range(sizes[i])
        elif outgoing_leaf == joins[i-1][1]:
            possible = incoming[i]
        elif len(incoming[i]) == 1:
            possible = set(range(sizes[i]))-incoming[i]
        else:
            possible = range(sizes[i])
        choices = {sizes[i]-1-v for v in possible if sizes[i]-1-v < sizes[i+1]}
        if not choices:
            return None
        incoming.append(choices)

    ranks = [{} for _ in sizes]
    if joins:
        next_rank = min(incoming[-1])
        for i in range(len(joins)-1,-1,-1):
            left,right = joins[i]
            ranks[i+1][right] = next_rank
            ranks[i][left] = sizes[i]-1-next_rank
            if i:
                if joins[i-1][1] == left:
                    next_rank = ranks[i][left]
                else:
                    next_rank = min(x for x in incoming[i] if x != ranks[i][left])

    # Number the two whole-tree bipartition classes in consecutive blocks.
    first_size = sum(a if i%2 == 0 else 1 for i,a in enumerate(sizes))
    cursor = [0,first_size]
    starts,labels,edges = [],[],[]
    for i,a in enumerate(sizes):
        starts.append(len(labels))
        leaf_side = i%2
        center = len(labels)
        labels.append(cursor[1-leaf_side])
        cursor[1-leaf_side] += 1
        used = set(ranks[i].values())
        unused = iter(x for x in range(a) if x not in used)
        for j in range(a):
            rank = ranks[i][j] if j in ranks[i] else next(unused)
            edges.append((center,len(labels)))
            labels.append(cursor[leaf_side]+rank)
        cursor[leaf_side] += a
    for i,(x,y) in enumerate(joins):
        edges.append((starts[i]+1+x,starts[i+1]+1+y))
    return labels,edges

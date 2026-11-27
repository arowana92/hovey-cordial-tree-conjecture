"""Expand a labeled two-center seed using a partition into zero-sum triples."""


def seed_tree(record):
    _, _, _, _, arms = record
    return [(0, 1), *((u, v) for c, p, x in arms for u, v in ((c, p), (p, x)))]


def expand(record, triples, second_center):
    """Select whole triples by zero-based index for the center labeled one."""
    _, _, cutoff, _, _ = record
    amount = 3*len(triples)

    def move(x):
        relative = x + x % 2
        return x + amount * (int(relative >= cutoff) - int(relative <= -cutoff))

    edges = [(move(u), move(v)) for u, v in seed_tree(record)]
    for i, triple in enumerate(triples):
        c = int(i in second_center)
        for j, z in enumerate(triple):
            displacement = triple[j-1]
            p = 2*displacement - c
            x = 2*z - 1 + c
            edges.extend(((c, p), (p, x)))
    return edges

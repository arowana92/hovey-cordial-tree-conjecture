"""Finite operations in the permuted random-pool proof."""

from collections import defaultdict


def round_counts(counts, k):
    total = sum(counts.values())
    if total==0:
        raise ValueError("need a nonempty list of leaf demands")
    quotients = {p:divmod(k*w,total) for p,w in counts.items()}
    amounts = {p:q for p,(q,_) in quotients.items()}
    left = k-sum(amounts.values())
    for p in sorted(counts,key=lambda p:(-quotients[p][1],p))[:left]:
        amounts[p] += 1
    return amounts


def assign_leaves(k, permutation, counts, core_sample, pinned_vertices, pinned_weights,
                  moment, forbidden_source=None):
    """Return leaf labels by parent shift, the two core pools and the omitted weight.

    The permutation witnesses Hall's rounded list, apart from one dummy source.
    Existence of sufficient simultaneous choices is proved for the sampled pools.
    """
    all_residues = set(range(k))
    if set(permutation)!=all_residues or len(permutation)!=k:
        raise ValueError("expected a permutation")
    colors = {permutation[v] for v in core_sample}
    picked = defaultdict(list)
    used_vertices, used_colors = set(), set()
    for x,y in enumerate(permutation):
        p = (y-x)%k
        if (x==forbidden_source or x in core_sample or x in pinned_vertices or
                y in pinned_weights or len(picked.get(p,()))>=counts.get(p,0)):
            continue
        picked[p].append(x)
        used_vertices.add(x)
        used_colors.add(y)
    fixes = 0
    for p,needed in counts.items():
        if len(picked[p])==needed:
            continue
        for x in sorted(core_sample-pinned_vertices-used_vertices):
            y = (x+p)%k
            if y in colors and y not in pinned_weights and y not in used_colors:
                picked[p].append(x)
                used_vertices.add(x)
                used_colors.add(y)
                fixes += 1
                if len(picked[p])==needed:
                    break
        if len(picked[p])!=needed:
            raise ValueError("the finite sample has too few unused arcs")

    A,C = all_residues-used_vertices,all_residues-used_colors
    shifts = sum(p*n for p,n in counts.items())
    gap = (moment-sum(A)-shifts)%k
    if gap in C-pinned_weights:
        return dict(picked),A,C,gap,(fixes,0)
    for p,entries in picked.items():
        for i,x in enumerate(entries):
            old = (x+p)%k
            if old==gap:
                continue
            for y in sorted(A-pinned_vertices):
                new = (y+p)%k
                other = (gap+y-x)%k
                if new in C-pinned_weights and other in C-pinned_weights and new!=other:
                    A.remove(y)
                    A.add(x)
                    C.remove(new)
                    C.add(old)
                    entries[i] = y
                    return dict(picked),A,C,other,(fixes,1)
    raise ValueError("the finite sample has no moment repair")

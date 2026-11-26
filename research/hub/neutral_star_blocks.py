"""Disjoint neutral copies of rooted stars below a prescribed cyclic-group label."""


def choose(modulus, occupied, forms, excluded=()):
    """Find a parameter on which a list of affine forms avoids previous residues."""
    excluded = {x % modulus for x in excluded}
    for t in range(modulus):
        if t in excluded:
            continue
        values = [(a*t+b) % modulus for a,b in forms]
        if len(set(values)) == len(forms) and occupied.isdisjoint(values):
            occupied.update(values)
            return t, values
    raise ValueError("no free parameter for this set of occupied residues")


def star_block(modulus, parent, arity, forbidden=()):
    """Return 4*arity rows (root, children). Inputs may include both used labels and weights."""
    if arity < 1 or modulus < 1:
        raise ValueError("positive arity and modulus required")
    p = parent % modulus
    occupied = {x % modulus for x in forbidden} | {0}
    roots, children = [], [[] for _ in range(4*arity)]

    def swaps(i, j):
        x = roots[i]
        assert (x+roots[j]) % modulus == 0
        for _ in range(arity):
            _, (b,c) = choose(modulus, occupied, [(1,0),(1,x)])
            children[i].append(b)
            children[j].append(c)

    if 2*p % modulus == 0:
        for _ in range(arity):
            i = len(roots)
            if p == 0:
                forms = [(1,0),(2,0),(-1,0),(-2,0)]
            else:
                forms = [(1,0),(1,p),(-1,0),(-1,p)]
            _, group = choose(modulus,occupied,forms)
            roots.extend(group)
            swaps(i,i+2)
            swaps(i+1,i+3)
    else:
        # Each progression of two roots generates one unused head two steps above its tail.
        # Two children, attached at a prescribed pair of active roots, return it to the tail.
        def progressions(positive, negative, pos_middle, neg_middle, forbidden_t=()):
            a,b = positive
            c,e = negative
            forms = [(a,b+j*p) for j in range(3)] + [(c,e+j*p) for j in range(3)]
            forms.extend([pos_middle,neg_middle])
            t, (x,x1,h,y,y1,l,m,n) = choose(modulus,occupied,forms,forbidden_t)
            roots.extend((x,x1,y,y1))
            children[0].append(h)
            children[3].append(m)
            children[2].append(l)
            children[1].append(n)
            return t

        a = progressions((1,0),(-1,-3*p),(2,2*p),(-2,-4*p),
                         [0,-p,-2*p,-3*p])
        for _ in range(1,arity):
            i = len(roots)
            progressions((1,0),(-1,-p),(1,2*p+a),(-1,-2*p-a))
            swaps(i,i+3)
            swaps(i+1,i+2)
    assert all(len(row)==arity for row in children)
    return list(zip(roots,children))

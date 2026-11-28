"""Short bridges and the degree-core pins for paths shorter than one period."""


def short(k,a,b,d,e,t):
    """Construct 3 <= t < k when k > 4t-10+2 gcd(2,k)."""
    from math import gcd
    if not 3 <= t < k or k <= 4*t-10+2*gcd(2,k):
        raise ValueError("Outside the elementary counting bound")
    path = [(d-a)%k]
    colors = set()
    while len(path) < t-2:
        x = next(v for v in range(k) if v not in path and (path[-1]+v)%k not in colors)
        colors.add((path[-1]+x)%k)
        path.append(x)
    for y in range(k):
        z = (e-y)%k
        first,last = (path[-1]+y)%k,(b+z)%k
        if (y != z and y not in path and z not in path and first != last
                and first not in colors and last not in colors):
            return path + [y,z]
    raise ArithmeticError("No two final labels")


def auxiliary(k,a,b,d,e,t):
    """Return the order-k auxiliary tree, its fixed labels and its missing sum."""
    if k < 32 or not 8 <= t < k:
        raise ValueError("Expected k >= 32 and 8 <= t < k")
    total = sum(range(k))
    x = (d-a)%k
    y = next(i for i in range(k) if i != x and (b+i)%k != e)
    last = (b+y)%k
    u = next(i for i in range(k) if i not in (x,y) and (e-i)%k not in (i,x,y))
    pair = (e-u)%k
    used = {x,y,u,pair}
    for z in range(k):
        h = (last-z)%k
        if h == z or h in used or z in used:
            continue
        base = x+y+h-z-total
        if k-t == 1 and base%k in (e,last):
            continue
        if k-t == 2 and (base-2*z)%k == 0:
            continue
        break
    else:
        raise ArithmeticError("No label for the branch vertex")
    # Position t is a single spare leaf. Positions after t form a second arm.
    edges = [(i-1,i) for i in range(1,t)] + [(5,t)]
    pins = {0:x, 2:u, 3:pair, 5:z, t-1:y, t:h}
    gap = base%k
    if k-t >= 2:
        edges.append((5,t+1))
        edges.extend((i-1,i) for i in range(t+2,k))
        for v in range(k):
            gap = (base+v-z)%k
            if v in pins.values() or gap in (e,last):
                continue
            if k-t == 2 and (z+v)%k in (e,last,gap):
                continue
            pins[k-1] = v
            break
        else:
            raise ArithmeticError("No label for the spare tip")
    return edges,pins,gap

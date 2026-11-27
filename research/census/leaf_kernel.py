"""Congruence counts for a fixed rooted tree with all further leaves at one vertex."""

from collections import Counter
from itertools import permutations
from math import factorial, gcd, prod


def partitions(size):
    """Restricted-growth words and the partition-lattice Möbius coefficients."""
    def visit(word, blocks):
        if len(word) == size:
            mu = (-1)**(size-blocks)*prod(factorial(word.count(i)-1) for i in range(blocks))
            yield word, blocks, mu
        else:
            for i in range(blocks+1):
                yield from visit(word+(i,), max(blocks, i+1))
    yield from visit((), 0)


def diagonal(matrix, rhs):
    """Unimodular integer row and column operations, also applied to the RHS."""
    A = [row.copy() for row in matrix]
    b = rhs.copy()
    height, width = len(A), len(A[0])
    rank = 0
    for i in range(min(height, width)):
        pivot = next(((r,c) for r in range(i,height) for c in range(i,width) if A[r][c]), None)
        if pivot is None:
            break
        r,c = pivot
        A[i], A[r] = A[r], A[i]
        b[i], b[r] = b[r], b[i]
        for row in A:
            row[i], row[c] = row[c], row[i]
        while True:
            for r in range(i+1,height):
                if A[r][i]:
                    q = A[r][i] // A[i][i]
                    A[r] = [x-q*y for x,y in zip(A[r], A[i])]
                    b[r] -= q*b[i]
                    if A[r][i]:
                        A[r], A[i] = A[i], A[r]
                        b[r], b[i] = b[i], b[r]
                    break
            else:
                c = next((c for c in range(i+1,width) if A[i][c]), None)
                if c is None:
                    break
                q = A[i][c] // A[i][i]
                for row in A:
                    row[c] -= q*row[i]
                if A[i][c]:
                    for row in A:
                        row[c], row[i] = row[i], row[c]
        rank += 1
    factors = []
    for r in range(rank):
        a = abs(A[r][r])
        if a > 1:  # gcd(a,n) must divide b[r]*d. Only gcd(a,b[r]) matters.
            factors.append((a, gcd(a,b[r])))
    return width-rank, tuple(sorted(factors)), gcd(0, *b[rank:])


def spectrum(parent, site, marked=False):
    """Return terms for the neutral count or the count with a marked deficit edge."""
    s = len(parent)-1
    if s < 1 or parent[0] != -1 or not 0 <= site <= s:
        raise ValueError("use a rooted nonempty kernel and a vertex of that kernel")
    if any(not 0 <= p < v for v,p in enumerate(parent[1:], 1)):
        raise ValueError("each parent must precede its child")
    groups = list(partitions(s))
    terms = Counter()
    for pi in permutations(range(1,s+1)):
        for special in (range(1,s+1) if marked else [None]):
            rows = []
            rhs = []
            for v in range(1,s+1):
                row = [0]*s
                row[v-1] += 1
                if parent[v]:
                    row[parent[v]-1] += 1
                if v != special:
                    if site:
                        row[site-1] -= 1
                    row[pi[v-1]-1] -= 1
                rows.append(row)
                rhs.append(int(v==special))
            for word, blocks, mu in groups:
                merged = []
                for row in rows:
                    collapsed = [0]*blocks
                    for col,j in enumerate(word):
                        collapsed[j] += row[col]
                    merged.append(collapsed)
                terms[diagonal(merged, rhs)] += mu
    return {key: n for key,n in terms.items() if n}


def evaluate(terms, n, d=0):
    total = 0
    for (free, factors, zero_rhs), coefficient in terms.items():
        if (zero_rhs*d) % n:
            continue
        lifts = 1
        for a,b in factors:
            g = gcd(a,n)
            if b*d % g:
                break
            lifts *= g
        else:
            total += coefficient * n**free * lifts
    return total


def divisors(n):
    from math import isqrt
    small = [i for i in range(1,isqrt(n)+1) if n % i == 0]
    return small + [n//i for i in reversed(small) if i*i != n]


def positivity_bound(terms, minimum):
    """A sufficient threshold for positivity for all orders of the deficit."""
    from math import comb, lcm
    period = lcm(*(a for _, factors, _ in terms for a,_ in factors))
    small_orders = {h for _,_,b in terms if b for h in divisors(b)}
    ds = divisors(period)

    def polynomial(n, d, order):
        coef = Counter()
        for (power, factors, b), weight in terms.items():
            if b and (order is None or b % order):
                continue
            product = weight
            for a,c in factors:
                g = gcd(n,a)
                if c*d % g:
                    break
                product *= g
            else:
                coef[power] += product
        return tuple(coef[i] for i in range(max((i for i in coef if coef[i]),default=-1)+1))

    # For small h, d may be taken as n/h by unit symmetry. Otherwise every
    # nonzero last-row constraint fails; only gcd(n,L), gcd(d,gcd(n,L)) matter.
    polynomials = {polynomial(g, f, None) for g in ds for f in divisors(g)}
    polynomials.update(polynomial(h*t, t, h) for h in small_orders for t in ds)
    threshold = minimum
    for coefficients in polynomials:
        if not coefficients or coefficients[-1] <= 0:
            return None
        while True:
            shifted = [sum(comb(i,j)*coefficients[i]*threshold**(i-j)
                           for i in range(j,len(coefficients))) for j in range(len(coefficients))]
            if shifted[0] > 0 and min(shifted) >= 0:
                break
            threshold *= 2
    return threshold


def all_deficits(terms, minimum):
    threshold = positivity_bound(terms, minimum)
    if threshold is None:
        return None
    for n in range(minimum,threshold):
        if any(evaluate(terms, n, n//h) <= 0 for h in divisors(n)):
            return None
    return threshold

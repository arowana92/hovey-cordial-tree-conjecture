"""Compare the two-shift formula with all partial matchings on small cyclic groups."""
from functools import lru_cache
from math import gcd


@lru_cache(None)
def ones(mask):
    return bin(mask).count('1')


def cycle_spectrum(k, shift, inputs, outputs):
    size = k//gcd(k,shift)
    mixed = False
    spare = 0
    intact = 0
    for start in range(k//size):
        cycle = sum(1 << ((start+j*shift)%k) for j in range(size))
        h = ones(inputs & cycle)
        e = ones(outputs & cycle)
        mixed |= h>0 and e>0
        if h+e:
            spare += size-h-e
        else:
            intact += 1
    r = k-ones(inputs)-ones(outputs)
    if mixed:
        return (1 << (r+1))-1
    return sum(1 << b for b in range(r+1) if
               any(0 <= b-q*size <= spare for q in range(intact+1)))


def direct(k,shift):
    @lru_cache(None)
    def match(left,right):
        if not left:
            return (1,)
        first = left & -left
        rest = left ^ first
        result = list(match(rest,right)) + [0]
        for target, increment in ((first,0),(1 << ((first.bit_length()-1+shift)%k),1)):
            if target & right:
                for r,bits in enumerate(match(rest,right^target)):
                    result[r+1] |= bits << increment
        return tuple(result)
    return match


def guaranteed(k,d,h,e):
    r = k-h-e
    touched = (h+d-1)//d + (e+d-1)//d
    rest = touched*d-h-e
    return sum(1 << b for b in range(r+1) if touched>=k//d or b%d<=rest)


def check_small(k,shift):
    full = (1 << k)-1
    match = direct(k,shift)
    common = {}
    cases = 0
    for inputs in range(full+1):
        h=ones(inputs)
        for outputs in range(full+1):
            e=ones(outputs)
            r = k-h-e
            if r<0:
                continue
            got = match(full^inputs,full^outputs)[r]
            assert got==cycle_spectrum(k,shift,inputs,outputs)
            key = h,e
            common[key] = common.get(key,(1 << (r+1))-1)&got
            cases += 1
    for (h,e),got in common.items():
        assert got==guaranteed(k,k//gcd(k,shift),h,e)
    match.cache_clear()
    return cases


def boundary(k,s):
    h = k+1-s
    r = k-2*h+1
    return [(d,b) for d in range(2,k+1) if k%d==0 for b in range(r+1)
            if not guaranteed(k,d,h,h-1) & (1 << b)]


def example_27():
    # Actual shifts 0 and 9. Decompose only for the brute-force matching search.
    # Track both the number of edges and the number assigned the second shift.
    forbidden_inputs = {0,9,18}
    forbidden_outputs = {1,10}
    totals = {(0,0)}
    match = direct(3,1)
    for root in range(9):
        sites = [root,root+9,root+18]
        left = sum(1 << i for i,x in enumerate(sites) if x not in forbidden_inputs)
        right = sum(1 << i for i,x in enumerate(sites) if x not in forbidden_outputs)
        choices = [(r,b) for r,bits in enumerate(match(left,right)) for b in range(r+1) if bits & (1 << b)]
        totals = {(n+r,c+b) for n,c in totals for r,b in choices}
    assert {b for n,b in totals if n==22} == {b for b in range(23) if b%3!=2}


if __name__=='__main__':
    cases = sum(check_small(k,t) for k in range(2,9) for t in range(1,k))
    print('literal forbidden-set and shift cases',cases)
    example_27()
    for s in range(23,28):
        failures = boundary(27,s)
        assert failures == ([(3,b) for b in range(2,23,3)] if s==25 else [])
        print('residue',s,'exceptional shift orders and multiplicities',failures)

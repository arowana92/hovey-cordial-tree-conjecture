"""Integer decomposition into squared cyclic differences at dyadic strides."""

from collections import defaultdict


def rounded_moments(numerators, total, moment):
    """Round a vector of quarters to prescribed nearby mass and first moment."""
    prefix = 0
    old = 0
    out = []
    for x in numerators:
        prefix += x
        value = prefix//4
        out.append(value-old)
        old = value
    out[-1] += total-old
    missing = moment-sum(i*x for i,x in enumerate(out))
    sign = 1 if missing >= 0 else -1
    remaining = abs(missing)
    while remaining:
        jump = min(remaining,len(out)-1)
        out[0] -= sign
        out[jump] += sign
        remaining -= jump
    return out


def squared_terms(data):
    k = len(data)
    moment = sum(i*x for i,x in enumerate(data))
    if not k or sum(data) or moment%k:
        raise ValueError("expected zero mass and zero moment modulo the length")
    base,rem = divmod(-moment//k,k)
    tail = [base+(i<rem) for i in range(k)]
    lifted = [x-y for x,y in zip(data,tail)]+tail
    terms = defaultdict(lambda: [0]*k)

    def visit(arr,origin,stride):
        if not any(arr):
            return
        if len(arr)<=4:
            first = second = 0
            for j,x in enumerate(arr):
                first += x
                second += first
                terms[stride][(origin+j*stride)%k] += second
            return
        f = [0]+arr+[0]
        origin -= stride
        nums = [-x for x in arr]
        even = f[::2]
        half,parity = divmod(sum(even),2)
        assert not parity
        moment_even = sum(i*x for i,x in enumerate(even))
        parity = (half-moment_even)%2
        odd_total = parity+2*((sum(nums[1::2])-4*parity+4)//8)
        even_total = odd_total+half
        odd_moment = (sum(i*x for i,x in enumerate(nums[1::2]))+2)//4
        even_moment = odd_moment+(moment_even-even_total+2*odd_total)//2
        h = [0]*len(arr)
        h[::2] = rounded_moments(nums[::2],even_total,even_moment)
        h[1::2] = rounded_moments(nums[1::2],odd_total,odd_moment)
        g = f[:]
        for j,x in enumerate(h):
            terms[stride][(origin+j*stride)%k] += x
            g[j] -= x
            g[j+1] += 2*x
            g[j+2] -= x
        for parity in (0,1):
            child = g[parity::2]
            assert sum(child)==sum(i*x for i,x in enumerate(child))==0
            visit(child,origin+parity*stride,2*stride)
    visit(lifted,0,1)
    return dict(terms)

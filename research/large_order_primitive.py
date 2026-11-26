"""Round the same integer second antiderivative at all dyadic scales."""


def lifted_moment_zero(data):
    k = len(data)
    moment = sum(i*x for i, x in enumerate(data))
    if not k or sum(data) or moment % k:
        raise ValueError("expected zero mass and zero moment modulo the length")
    total = -moment//k
    tail = [((i+1)*total)//k-(i*total)//k for i in range(k)]
    return [x-y for x,y in zip(data,tail)]+tail


def squared_terms(data):
    k = len(data)
    first = second = 0
    primitive = []
    for x in lifted_moment_zero(data):
        first += x
        second += first
        primitive.append(second)
    assert first == second == 0

    terms = {}
    fine = None
    stride = 1
    while True:
        # Project after rounding the finitely supported interval coefficients.
        coarse = [0]*k
        denominator = stride**2
        for i, x in enumerate(primitive):
            coarse[(i-stride+1)%k] += (2*x+denominator)//(2*denominator)
        if fine is not None:
            half = stride//2
            terms[half] = [fine[i]-coarse[i]-2*coarse[(i-half)%k]-coarse[(i-stride)%k]
                           for i in range(k)]
        if stride >= 2*k:
            terms[stride] = coarse
            return terms
        fine = coarse
        stride *= 2

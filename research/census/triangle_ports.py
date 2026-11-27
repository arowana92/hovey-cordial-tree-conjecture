"""Verify the all-difference square and triangle decisions on complete progressions."""

from collections import defaultdict
from itertools import combinations
from math import gcd, lcm, prod

from .square_ports import signatures


def factors(signature, k):
    return prod(gcd(k,d) for d in signature[1])


def terms(table, k):
    """Each linear polynomial contributes on one subgroup of endpoint differences."""
    result = defaultdict(lambda: [0,0])
    for (source,fixed), mult in table.items():
        a,b = factors(source,k), factors(fixed,k)
        if source[0] == fixed[0]:
            assert a % b == 0
            key = ("size", a//b)
        else:
            assert source[0] == fixed[0]+1 and b % a == 0
            key = ("index", b//a)
        assert fixed[0] in (0,1)
        result[key][fixed[0]] += mult*b
    return {key:value for key,value in result.items() if any(value)}


def intersection_size(k, groups):
    index = lcm(*(x for kind,x in groups if kind == "index"))
    assert k % index == 0
    return gcd(k//index, *(x for kind,x in groups if kind == "size"))


def population(k, groups, mask):
    required = [g for j,g in enumerate(groups) if mask & (1<<j)]
    forbidden = [g for j,g in enumerate(groups) if not mask & (1<<j)]
    return sum((-1)**j * intersection_size(k,required+list(extra))
               for j in range(len(forbidden)+1) for extra in combinations(forbidden,j))


def check_all(table, prediction):
    period = lcm(*(d for pair in table for sig in pair for d in sig[1]))
    base = period
    for r in range(1,base+1):
        groups = list(terms(table,r))
        indices = lcm(*(x for kind,x in groups if kind == "index"))
        sizes = lcm(*(x for kind,x in groups if kind == "size"))
        period = lcm(period,indices*sizes)
    # A shared period also fixes the proposed criterion at 2,3,4 and 5.
    period = lcm(period,60)
    for start in range(4,4+period):
        formula = terms(table,start)
        groups = list(formula)
        holds = [True]*3
        for mask in range(1<<len(groups)):
            pop = population(start,groups,mask)
            growth = population(start+period,groups,mask)-pop
            assert pop >= 0 and growth >= 0
            if pop == growth == 0:
                continue
            coeff = [sum(formula[g][i] for j,g in enumerate(groups) if mask & (1<<j))
                     for i in range(2)]
            assert coeff[1]>=0
            for t in range(3):
                if pop+t*growth:
                    value = coeff[0]+coeff[1]*(start+t*period)
                    assert value>=0
                    holds[t] &= value>0
            # For t>=2 an occupied class either has a positive increasing count
            # or a constant count. The strict-positivity verdict is stable.
        assert all(v==prediction(start) for v in holds), (start,holds)
    return period


if __name__ == "__main__":
    graph = [(0,1),(1,2),(2,3),(3,1)]
    closed = signatures(graph,None)
    assert closed == {((0,(4,)),(0,(4,))):1, ((0,(2,)),(0,(2,))):-1}
    near = check_all(signatures(graph,1),lambda k: k%4==0 or k%6==0 or gcd(k,30)==1)
    far = check_all(signatures(graph,2),lambda k: k%4==0)
    print("verified every modulus k >= 4; progression periods",near,far)

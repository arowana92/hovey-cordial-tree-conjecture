"""Count all attainable second-shift multiplicities at each partial matching size."""
from math import gcd

from .check_two_shift_holes import direct


def multiplicities(k,delta,inputs,outputs):
    """Return a bit mask per matching size, after normalizing the first shift to zero."""
    if not 0 < delta < k or inputs < 0 or outputs < 0 or (inputs | outputs) >> k:
        raise ValueError('expected a nonzero shift and two residue masks')
    cycles=gcd(k,delta)
    period=k//cycles
    flexible=intact=0
    forced=[[],[]]
    for root in range(cycles):
        deleted=[]
        for j in range(period):
            v=(root+j*delta)%k
            deleted.extend([bool(outputs & (1<<v)),bool(inputs & (1<<v))])
        if not any(deleted):
            intact+=1
            continue
        first_hole=deleted.index(True)
        run=0
        for i in range(first_hole+1,first_hole+2*period+1):
            if not deleted[i%(2*period)]:
                run+=1
                continue
            if run%2:
                flexible+=run//2
            elif run:
                # Destination-first even paths force flat edges; source-first ones force shifted edges.
                forced[(i-run)%2].append(run//2)
            run=0
    for group in forced:
        group.sort(reverse=True)
    maximum=flexible+intact*period+sum(map(sum,forced))
    result=[]
    for size in range(maximum+1):
        deficit=maximum-size
        low=sum(forced[1][deficit:])
        high=size-sum(forced[0][deficit:])
        if deficit:
            result.append(((1<<(high-low+1))-1)<<low)
        else:
            result.append(sum(1<<j for j in range(size+1) if any(
                0<=j-low-q*period<=flexible for q in range(intact+1))))
    return result


if __name__=='__main__':
    cases=0
    for k in range(2,9):
        full=(1<<k)-1
        for delta in range(1,k):
            enumerate_matchings=direct(k,delta)
            for inputs in range(full+1):
                for outputs in range(full+1):
                    actual=enumerate_matchings(full^inputs,full^outputs)
                    predicted=multiplicities(k,delta,inputs,outputs)
                    assert tuple(predicted)+(0,)*(len(actual)-len(predicted))==actual
                    cases+=len(actual)
            enumerate_matchings.cache_clear()
    print('forbidden sets, shifts and matching sizes checked',cases)

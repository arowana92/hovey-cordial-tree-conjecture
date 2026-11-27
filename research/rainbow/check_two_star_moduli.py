"""Compare the arithmetic criterion with actual endpoint sums and center searches."""
from math import gcd

from .check_two_star_extension import deficits, replay
from .two_star_extension import integral_packet
from .two_star_moduli import (construct, divisors, first_obstruction, obstructing_prime,
                              prime_powers, prime_witness)


def center_search(k,s,q,delta):
    return (integral_packet(k,s,q,delta) is not None or
            integral_packet(k,k-s,(-q)%k,delta) is not None)


def two_prime_rule(p,a,q,b):
    for z in range(1,q):
        for i in range(a):
            residue = pow(p,i,q)*z%q
            if p*min(residue,q-residue)>=q-int(b==1 and i==a-1):
                break
        else:
            return False
    return True


def main():
    direct = splits = individual = positive = prime_inputs = negative = 0
    for k in range(2,12):
        for s in range(1,k):
            universal = True
            for q in range(k):
                possible = deficits(k,s,q)
                universal &= len(possible)==k
                for d in range(k):
                    result = construct(k,s,0,q,d)
                    if result is not None:
                        assert d in possible
                        replay(k,s,k-s,0,q,d,result)
                    if len(possible)<k:
                        assert obstructing_prime(k,s) is not None
                    direct += 1
            assert universal==(obstructing_prime(k,s) is None)

    # A unit can take any discrepancy of order m to k/m. Test every Q in
    # its subgroup and every split outside the elementary constructions.
    for k in range(2,121):
        for s in range(1,k//2+1):
            failed = False
            for m in divisors(k)[1:]:
                delta = k//m
                if s%m or delta%gcd(s,k)==0:
                    continue
                for q in range(delta,k,delta):
                    possible = center_search(k,s,q,delta)
                    result = construct(k,s,0,q,(q+delta)%k)
                    if result is not None:
                        assert possible
                        replay(k,s,k-s,0,q,(q+delta)%k,result)
                        positive += 1
                    if len(divisors(m))==2:
                        assert possible==(prime_witness(k,s,m) is not None)
                        prime_inputs += 1
                    failed |= not possible
                    individual += 1
            assert failed==(obstructing_prime(k,s) is not None)
            splits += 1

    for k in range(2,201):
        for s in range(1,k//2+1):
            p = obstructing_prime(k,s)
            if p is not None:
                delta = k//p
                assert not center_search(k,s,delta,delta)
                # Old star has all residues once and is missing precisely 2*delta.
                weights = {(delta+v)%k for v in range(k) if v!=delta}
                assert set(range(k))-weights=={2*delta%k}
                negative += 1

    mixed = []
    checked_even = two_prime = 0
    for k in range(2,2401):
        factors = prime_powers(k)
        universal = first_obstruction(k) is None
        if k<=500 and len(factors)>1 and universal:
            mixed.append(k)
        if k%2==0:
            assert universal==(k//(k&-k) in (1,3))
            checked_even += 1
        if len(factors)==2:
            (p,pa),(q,qb) = factors
            a = len(divisors(pa))-1
            b = len(divisors(qb))-1
            assert universal==two_prime_rule(p,a,q,b)
            two_prime += 1
    print('literal inputs',direct,'universal split comparisons',splits)
    print('center searches',individual,'recounted singular constructions',positive,
          'prime-order comparisons',prime_inputs,'old-star obstructions',negative)
    print('even moduli',checked_even,'two-prime moduli',two_prime)
    print('universal mixed-prime moduli through 500',mixed)


if __name__=='__main__':
    main()

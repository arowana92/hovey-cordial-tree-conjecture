"""Compare the prime-size obstruction with direct searches on independent lists."""

from itertools import combinations,product
from random import Random

from .check_leaf_lists import choose
from .check_twice_prime_power import verify_coefficient


def coset_obstruction(k, prime, shifts, lists):
    step = k // prime
    origin = shifts[0]
    if any((shift - origin) % step for shift in shifts):
        return False
    input_cosets = {x % step for row in lists for x in row}
    return len(input_cosets) == 1 and sum((shift - origin) // step for shift in shifts) % prime != 0


def check(k, prime, shifts, lists):
    witness = choose(k, shifts, lists)
    obstructed = coset_obstruction(k, prime, shifts, lists)
    assert (witness is None) == obstructed
    if witness is not None:
        outputs = {(x + shift) % k for x, shift in zip(witness, shifts)}
        assert len(set(witness)) == len(shifts) == len(outputs)
        assert all(x in row for x, row in zip(witness, lists))
    return int(obstructed)


def exhaustive():
    sets = list(combinations(range(6),3))
    seen = bad = 0
    # Subtracting the first shift from every output normalizes it to zero.
    for tails in product(range(6),repeat=2):
        shifts = (0,)+tails
        for lists in product(sets,repeat=3):
            bad += check(6,3,shifts,lists)
            seen += 1
    return seen,bad


def sample():
    rng = Random(195226)
    seen = bad = 0
    for p in (5,7):
        k = 2*p
        for j in range(600):
            parity = rng.randrange(2)
            shifts = [2*rng.randrange(p)+parity for _ in range(p)]
            coset = list(range(rng.randrange(2),k,2))
            lists = [list(coset) for _ in shifts]
            if j%4==1:
                lists[0].append(coset[0]^1)
            elif j%4==2:
                shifts[-1] ^= 1
            elif j%4==3:
                lists = [rng.sample(range(k),rng.randrange(p,k+1)) for _ in shifts]
            bad += check(k,p,shifts,lists)
            seen += 1
    return seen,bad


def other_quotients():
    rng = Random(52621)
    seen = failures = 0
    for k, prime in ((9, 3), (15, 5), (20, 5), (21, 7)):
        step = k // prime
        for index in range(200):
            origin = rng.randrange(step)
            shifts = [origin + step * rng.randrange(prime) for _ in range(prime)]
            coset = list(range(rng.randrange(step), k, step))
            lists = [list(coset) for _ in shifts]
            if index % 3 == 1:
                lists[-1].append((coset[0] + 1) % k)
            elif index % 3 == 2:
                lists = [rng.sample(range(k), prime) for _ in shifts]
            failures += check(k, prime, shifts, lists)
            seen += 1
    return seen, failures


def coefficients():
    rng = Random(131991)
    count = 0
    for p in (3,5):
        k = 2*p*p
        for r in range(p, min(2*p,8)+1):
            for v in range(1,r):
                mixed = r%2==0 and v%2==1
                required = max(v,r-v)
                if required > (p if mixed else p-1):
                    continue
                shifts = [2*rng.randrange(k//2)+int(i<v) for i in range(r)]
                verify_coefficient(k,p,shifts,(0,v) if mixed else None)
                count += 1
    return count


if __name__=='__main__':
    print('Exhaustive normalized three-row instances and failures:',exhaustive())
    print('Sampled five- and seven-row instances and failures:',sample())
    print('Other quotient sizes, instances and failures:',other_quotients())
    print('Exact lifted cyclotomic coefficients:',coefficients())

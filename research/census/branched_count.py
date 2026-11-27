"""Count the rings independently with rooted matching types and Burnside's lemma."""

from math import comb, gcd


def rooted_types(limit):
    # free[t]: odd rooted trees of size 2t+1 with their root left over.
    # matched[t]: internally perfectly matched rooted trees of size 2t+2.
    free = [1]
    matched = [1]
    for t in range(1,limit+1):
        coefficients = [1]+[0]*t
        for size,colors in enumerate(matched,1):
            old = coefficients[:]
            for k in range(size,t+1):
                coefficients[k] += sum(comb(colors+j-1,j)*old[k-size*j]
                                       for j in range(1,k//size+1))
        free.append(coefficients[t])
        matched.append(sum(free[i]*free[t-i] for i in range(t+1)))
    return free,matched


def coefficient(orbits, total):
    counts = [1]+[0]*total
    for length,colors in orbits:
        counts = [sum(colors[j]*counts[i-length*j] for j in range(i//length+1))
                  for i in range(total+1)]
    return counts[total]


def bracelets(length, total, colors, fixed):
    count = 0
    for a in range(length):
        g = gcd(a,length)
        count += coefficient([(length//g,colors)]*g,total)
        f = sum((2*j-a)%length == 0 for j in range(length))
        count += coefficient([(1,fixed)]*f+[(2,colors)]*((length-f)//2),total)
    assert count%(2*length) == 0
    return count//(2*length)


def ring_count(pairs, extra):
    sites = pairs-extra
    free,matched = rooted_types(extra)
    same = [free[i//2] if i%2 == 0 else 0 for i in range(extra+1)]
    mixed = bracelets(sites,extra,[2*x for x in matched],
                      [x+y for x,y in zip(matched,same)])
    traversed = bracelets(sites,extra,matched,same)
    undecorated_matching = bracelets(2*sites,extra,free,free)
    return mixed-traversed+undecorated_matching


if __name__ == '__main__':
    for extra in range(1,7):
        print(extra,ring_count(13,extra))

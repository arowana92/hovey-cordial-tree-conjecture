"""Recompute corrected edge counts independently of the packed-interval construction."""

from collections import Counter
from itertools import product
from random import Random

from research.hub.bounded_error import construct, place_packet
from research.hub.check_odd_branch_groups import append_branch
from research.rainbow.verify import rooted_shapes


def packet_checks():
    rng = Random(417)
    checked = 0
    for n in range(1,8):
        for tree in rooted_shapes(n).values():
            for width in (1,3,7,15):
                rows = [list(range(i*n,(i+1)*n)) for i in range(2*width)]
                k = 65521
                labels = place_packet(tree,rows,k,{0,1,2,3},rng)
                vertices = Counter(labels.values())
                for p in (0,1,2,5):
                    weights = Counter((labels[row[v]]+(p if u < 0 else labels[row[u]])) % k
                                      for row in rows for v,u in enumerate(tree))
                    assert len(vertices) == len(labels) and sum((weights-vertices).values()) <= 2*min(width,p)
                    checked += 1
    return checked


def coarse_checks():
    # The buffer in the coarse criterion must protect every point of the fine
    # parameter cell, even with negative slope and a wrap around the circle.
    M,k = 53,1031
    ordinary = set(range(M))-{3,8,29,47}
    trials = 0
    for a,c,i in product((-2,-1,1,2),range(M),range(M)):
        if any((a*i+c+j) % M not in ordinary for j in range(-5,6)):
            continue
        x0,x1 = (i*k+M-1)//M,((i+1)*k+M-1)//M
        b0,b1 = (c*k+M-1)//M,((c+1)*k+M-1)//M
        for x in (x0,x1-1):
            for b in (b0,b1-1):
                for offset in (-k//M,0,k//M):
                    assert ((a*x+b+offset) % k)*M//k in ordinary
                    trials += 1
    return trials


def main():
    packet_count = packet_checks()
    coarse = coarse_checks()
    cases = packets = batches = witnesses = distant = 0
    max_error = 0
    for k in (3019,4096,5010):
        for length in (6,49,138):
            tree = [-1]+list(range(length))
            sites = [0,length//3,length]
            for j,v in enumerate(sites):
                for arity in range(1,4):
                    for _ in range(10+j*3):
                        append_branch(tree,v,[-1]+[0]*arity)
            counts = [k-len(tree)-190,120,70]
            for reserve in (range(k//2,k//2+240),
                            [x for x in range(k) if (x*70//k) % 10 == 3]):
                parents,labels,budget,stats = construct(tree,sites,counts,k,reserve)
                assert parents[:len(tree)] == tree and set(labels) == set(range(k))
                assert Counter(parents[len(tree):]) == Counter(dict(zip(sites,counts)))
                actual = [(labels[v]+labels[p]) % k for v,p in enumerate(parents) if v]
                used = set()
                missing = iter(sorted(set(range(k))-set(actual)))
                corrected = []
                for x in actual:
                    if x in used:
                        corrected.append(next(missing))
                    else:
                        used.add(x)
                        corrected.append(x)
                changes = sum(x != y for x,y in zip(actual,corrected))
                assert len(set(corrected)) == k-1 and changes <= budget
                max_error = max(max_error,changes)
                packets += stats[0]
                batches += stats[1]
                witnesses += changes
                distant += length >= 49
                cases += 1
    assert min(packets,batches,witnesses,distant) > 0
    print(f"{packet_count:,} signed interval packet histograms and {coarse:,} "
          "fine-coordinate endpoint checks under the coarse buffer.")
    print(f"{cases} expanded trees, {packets} packets, {batches} neutral batches; "
          f"{witnesses} explicit corrected weights in total, maximum {max_error} per tree.")


if __name__ == '__main__':
    main()

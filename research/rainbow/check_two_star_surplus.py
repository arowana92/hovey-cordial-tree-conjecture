"""Compare the orbit solver, endpoint search and explicit prime constructions."""
from itertools import combinations, product
from math import isqrt
from random import Random
from subprocess import check_output
import sys

from .check_two_star_extension import core
from .two_star_surplus import antipodal, common, packet, prime_growth, surplus_site


def prime(n):
    return n>=2 and all(n%d for d in range(2,isqrt(n)+1))


def literal(k,s,a,b):
    palette = set(range(1,k))
    for x in palette:
        for y in palette-{x}:
            for leaves in combinations(palette-{x,y},s-1):
                sums = [a+x,b+y]+[x+v for v in leaves]+[y+v for v in palette-{x,y,*leaves}]
                if len({w%k for w in sums})==k-1:
                    return True
    return False


def replay(k,a,b,parts,direct=()):
    # A star core of order k+1 realizes every normalized parent pair and surplus zero.
    labels = [0]+list(range(k))
    edges = [(0,v) for v in range(1,k+1)]
    def append(parent,label):
        edges.append((parent,len(labels)))
        labels.append(label)
    for p,part in zip((a,b),parts):
        center = len(labels)
        append(1+p,part[0])
        for z in part[1:]:
            append(center,z)
    for z in direct:
        append(1+a,z)
    assert all(labels.count(i)==2 for i in range(k))
    weights = [(labels[v]+labels[w])%k for v,w in edges]
    assert sorted(weights.count(i) for i in range(k))==[1]+[2]*(k-1)


def half_prime_failure(k,s,a,b):
    p = k//2
    for order,first,second in ((s,a,b),(k-1-s,b,a)):
        if first==0 and ((order==1 and second%2) or (second==p and order<=p-2)):
            return True
    return False


def growth_checks():
    rng = Random(220311)
    trees = prefixes = 0
    for k in (2,3,5,7,11,13,17,23,29,41,59,97):
        orders = []
        if k<=7:
            for n in range(2,8):
                orders.extend(row for row in product(range(2),repeat=n) if len(set(row))==2)
        for n in (k,k+1,2*k-1,2*k,3*k+8):
            orders.extend(([0]*(n//2)+[1]*(n-n//2),[i%2 for i in range(n)],
                           [0,1]+[rng.randrange(2) for _ in range(n-2)]))
        for order in orders:
            a,b,mark = (rng.randrange(k) for _ in range(3))
            for surplus in (False,True):
                if surplus:
                    labels = [mark]+list(range(k))
                    edges = [(0,j) for j in range(1,k+1)]
                else:
                    labels,edges = core(k,mark)
                sites = [labels.index(a),labels.index(b)]
                centers = {}
                digits = prime_growth(k,order,a,b,mark,surplus=surplus)
                assert len(digits)==len(order)
                vertex,weight = [0]*k,[0]*k
                for v in labels:
                    vertex[v] += 1
                for v,w in edges:
                    weight[(labels[v]+labels[w])%k] += 1
                for side,z in zip(order,digits):
                    parent = centers.get(side,sites[side])
                    centers.setdefault(side,len(labels))
                    labels.append(z)
                    vertex[z] += 1
                    weight[(labels[parent]+z)%k] += 1
                    assert max(vertex)-min(vertex)<=1 and max(weight)-min(weight)<=1
                    prefixes += 1
                trees += 1
    return trees,prefixes


def main(native):
    checks = failed = permutations = singles = antipodes = surplus_inputs = 0
    for k in range(3,64):
        full = k<=30 or k in (34,37,38,46)
        prime_power = any(prime(q) and k in {q**e for e in range(1,7)} for q in range(2,k+1))
        args = [native,str(k)]+([] if full else ['--surplus-site'])
        rows = [list(map(int,line.split())) for line in check_output(args,text=True).splitlines()]
        assert [(a,b) for a,b,_ in rows]==(
            [(a,b) for a in range(k) for b in range(k)] if full else [(0,b) for b in range(k)])
        for a,b,mask in rows:
            for s in range(1,k-1):
                block = packet(k,s,a,b)
                good = bool(mask & (1<<s))
                assert (block is not None)==good,(k,s,a,b)
                if block is not None:
                    assert len(block[0])==s and len(block[1])==k-1-s
                    replay(k,a,b,block)
                else:
                    failed += 1
                if a==b or prime(k):
                    assert good
                if k%2==0 and k//2%2 and prime(k//2):
                    assert good!=half_prime_failure(k,s,a,b)
                if k%2==0 and (a,b)==(0,k//2):
                    assert good==antipodal(k,s)
                    antipodes += 1
                if a==0:
                    assert good==surplus_site(k,s,b)
                    surplus_inputs += 1
                    if prime_power:
                        assert good != (k%2==0 and s==1 and b%2==1)
                if k<=9:
                    assert good==literal(k,s,a,b)
                    permutations += 1
                checks += 1
    for k in range(3,33):
        for s in range(1,k-1):
            for t in range(1,k-s):
                for a in range(k):
                    left,right,direct = common(k,s,t,k-1-s-t,a)
                    assert (len(left),len(right),len(direct))==(s,t,k-1-s-t)
                    replay(k,a,a,(left,right),direct)
                    singles += 1
    print('prescribed orders and intermediate prefixes',*growth_checks())
    print(checks,'full inputs,',failed,'impossible,',permutations,'literal searches,',
          antipodes,'antipodal inputs,',surplus_inputs,'surplus-site inputs,',singles,'common-site packets with direct leaves')


if __name__=='__main__':
    main(sys.argv[1])

"""Check mixed guard orderings, divisibility bounds and actual restored edges."""

from collections import Counter
from itertools import accumulate, permutations, product
from math import gcd
from random import Random

from research.hub.paired_stars import repair as paired_repair
from research.hub.mixed_sparse import construct, guard, guard_split
from research.hub.seven_errors import prepare
from research.rainbow.verify import rooted_shapes


def totals(profiles,j):
    # Calculate the derivative by assigning the actual parents twice and
    # subtracting. The distinguished tip of the guard is still a pending jump.
    def evaluate(z):
        if j is None:
            data = [(z-1,z),(z-4,2*z-1),(-2*z-6,-2*z+1)]
        else:
            data = [(j*z,z),(-2*j*z-z,j*z+z)]
        return sum(l*x+(m-(i!=0))*y for i,((x,y),(l,m)) in enumerate(zip(data,profiles)))
    return evaluate(1)-evaluate(0)


def guard_checks():
    count = 0
    profiles = list(product(range(4),range(1,5)))
    for width in (2,3):
        for shapes in product(profiles,repeat=width):
            roots,j = guard(tuple(range(width)),shapes)
            assert totals([shapes[i] for i in roots],j)>0
            values = [totals(p,j) for p in permutations(shapes)]
            if j is None:
                assert sum(values)==2*sum(m for _,m in shapes)
            else:
                assert sum(values)>=sum(m for _,m in shapes)
            count += 1
    return count


def arithmetic_checks():
    # Count the fibres themselves at small composite moduli.
    fibres = 0
    for k in range(2,29):
        for a,b in product(range(-4,5),repeat=2):
            actual = Counter((a*x+b*y)%k for x in range(k) for y in range(k))
            assert set(actual.values())=={k*gcd(gcd(a,b),k)}
            fibres += 1
    rng = Random(84)
    schedules = 0
    for k in (512,2310,30030,360360,510510,9699690,65521):
        for _ in range(220):
            seq = [[sgn*s for s in ([1]+[2]*rng.randrange(10,100)+[6]*rng.randrange(12,100)
                                     +[-3]*rng.randrange(2,24))] for sgn in (1,-1)]
            p,q = [list(accumulate(row)) for row in seq]
            cut = guard_split(seq[0],k)
            walk = ([(p[0],0),(p[0],q[0])]+[(x,q[0]) for x in p[1:cut]]
                    +[(p[cut-1],y) for y in q[1:]]+[(x,q[-1]) for x in p[cut:]])
            assert all(x and y for x,y in walk[1:])
            assert gcd(p[cut-1],k)<=6 and all(gcd(x,k)>6 for x in p[cut:])
            # In the short final interval at most one distinct abscissa can
            # exceed the square-root gcd cutoff against the terminal ordinate.
            if cut<len(p):
                width = max(p[cut:])-min(p[cut:])
                high = {u for u in p[cut:] if gcd(u,q[-1])**2>abs(q[-1])*width}
                assert len(high)<=1
            cost = sum(gcd(gcd(x,y),k) for x,y in walk)
            assert cost<=12*len(walk)
            schedules += 1
    return fibres,schedules


def mixed_pairs():
    rng = Random(927)
    cases = edges = 0
    for k in (65520,65521,65536):
        for trial in range(8):
            sites = list(range(1,33))
            rng.shuffle(sites)
            parents = [-1]+[0]*32
            labels = {v:v for v in range(33)}
            stars,arities = {},{}
            for v in sites:
                stars[v] = []
                sizes = sorted((rng.randrange(1,12),rng.randrange(1,12)))
                for m in sizes:
                    root = len(parents)
                    parents.extend([v]+[root]*m)
                    stars[v].append(root)
                    arities[root] = m
            roles = []
            for j in range(0,24,4):
                group = sorted(sites[j:j+4],key=lambda v:arities[stars[v][1]])
                h,a,q,c = group
                roles.append((a,q,c,h))
            b,t,g = 1,177+trial,0
            blocked = set(labels.values())|{t,(-t)%k}
            new,_,_ = paired_repair(parents,stars,arities,roles,sites[24:],labels,
                                    blocked,b,t,g,k,rng)
            assert len(set(labels.values()))==len(labels)==len(parents)
            actual = Counter((labels[v]+labels[parents[v]])%k for v in range(33,len(parents)))
            actual.update((t,new))
            target = Counter(labels[v] for v in range(33,len(parents)))
            target.update((b,g))
            assert actual==target
            edges += len(parents)-33
            cases += 1
    return cases,edges


def main():
    pairs,pair_edges = mixed_pairs()
    orders = guard_checks()
    fibres,schedules = arithmetic_checks()
    rng = Random(991)
    shapes = 0
    for n in range(1,13):
        for tree in rooted_shapes(n).values():
            data,bills,_,_ = prepare(tree,32760,rng,guard_multiples=True)
            assert all(y==0 or (2*y%32760 and 3*y%32760) for y in data.values())
            for b,t in bills:
                for y in data.values():
                    assert (2*y-t)%32760 and all((b+i*y)%32760 for i in (1,2,3))
            shapes += 1
    cases = sums = repairs = loops = 0
    for k in (262139,262140,262144):
        for kind in ('zero','common','distinct'):
            number = 8*(10 if kind=='zero' else 15)
            core = [-1]+[0]*number+[1,number+1,number+2,number+3]
            roots = ([0]*number if kind=='zero' else
                     [number+4]*number if kind=='common' else list(range(1,number+1)))
            branches = [(p,rng.randrange(7),1+rng.randrange(8)) for p in roots]
            # Mix large populations with short branches at the same boundaries.
            for i in range(0,number,23):
                p,l,m = branches[i]
                branches[i] = (p,l+24,m) if i%2 else (p,l,m+28)
            parents,labels,gap,e,c = construct(core,branches,k,seed=100+cases)
            expected = list(core)
            for p,l,m in branches:
                r = len(expected)
                expected.extend([p,r]+[r+1]*m+[r]*l)
            assert parents==expected and len(set(labels))==len(labels)==len(expected)
            assert labels[0]==0
            weights = Counter((labels[v]+labels[p])%k for v,p in enumerate(expected) if v)
            weights[gap] += 1
            assert weights==Counter(labels)
            cases += 1
            sums += len(expected)-1
            repairs += e
            loops += c
    assert repairs and loops
    print(f"{orders:,} guard profiles, {shapes:,} guarded preparations, {fibres:,} congruence maps and {schedules:,} schedules.")
    print(f"{pairs} mixed paired-star replacements, {pair_edges:,} actual boundary and internal edges.")
    print(f"{cases} expanded trees, {sums:,} endpoint sums, {repairs} surplus repairs and {loops} translated cycles.")


if __name__=='__main__':
    main()

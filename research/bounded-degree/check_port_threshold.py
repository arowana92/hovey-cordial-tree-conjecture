"""Exercise random independent pins, a moving transfer bin, and obstructions at every order."""
from collections import Counter
from functools import reduce
from math import gcd,isqrt
from random import Random

from check import adjacency
from check_port_parity import piece
from check_two_leaf_repair import inspect
from port_parity import finish,plan


def prescriptions(k,h,target,edge_high,vertex_high):
    moves = plan(k,h,target,edge_high,vertex_high)
    if moves is None: return {}
    base = [[group[0][0],group[1][0]] if group else [None,None] for group in moves]
    j = 0 if moves[0] else 1
    b = 0 if len(moves[j][0])>=len(moves[j][1]) else 1
    result = {}
    for x in moves[j][b]:
        base[j][b] = x
        edge,vertex = base
        E = edge[0]-edge[1] if edge[0] is not None else 0
        V = vertex[0]-vertex[1] if vertex[0] is not None else 0
        m = (target+E-2*V)%k
        assert m%h==0
        result[m] = ([edge[0],vertex[0]],[edge[1],vertex[1]])
    assert 4*len(result)*h>=k
    return result


def construct(k,edges,ports,old,removed,eh,vh,rng):
    graph = adjacency(k,edges)
    counts = Counter(ports)
    delta = [len(row)+counts[v]-2 for v,row in enumerate(graph)]
    assert len(ports)>=5 and delta.count(-1)<=1
    fixed = {v for v,c in enumerate(delta) if c or counts[v]}
    internal = [(a,b) for a,b in edges if a in fixed and b in fixed]
    h = reduce(gcd,delta,k)
    choices = prescriptions(k,h,sum(removed)-sum(old)-sum(range(k)),eh,vh)
    if not choices: return None
    assert len(set(zip(ports,old)))==len(ports)
    for attempt in range(1,5001):
        pins = {v:rng.randrange(k) for v in fixed}
        moment = sum(delta[v]*x for v,x in pins.items())%k
        if moment not in choices or len(set(pins.values()))!=len(pins): continue
        dup,gap = (list(row) for row in choices[moment])
        colors = [(pins[v]+a)%k for v,a in zip(ports,old)]+[(pins[v]+pins[w])%k for v,w in internal]
        if len(set(colors))!=len(colors) or gap[0] in colors or gap[1] in pins.values(): continue
        if gap[0] is None:
            dup[0] = gap[0] = next(x for x in range(k) if x not in colors)
        return attempt,finish(edges,graph,ports,old,removed,dup,gap,pins)
    raise ValueError('random fixture did not produce a target')


def cover(k):
    # Check every translate by sliding one cyclic window, independently
    # counting its intersections with the residue positions in B.
    m = isqrt((k-1)//2)+1
    B = set(range(0,k,m))
    window = sum(i in B for i in range(2*m))
    smallest = window
    for i in range(k):
        window += ((i+2*m)%k in B)-(i in B)
        smallest = min(smallest,window)
    assert smallest>=2
    assert 2*m+len(B)<=isqrt(8*k)+3
    return 2*m+len(B)


def main():
    rng = Random(19611991)
    good = parity = longest = 0
    for k in (800,1024,1449,1600,2025):
        for charges in ([1],[2],[2,2],[4,6],[3,3,3]):
            edges,initial = piece(k,charges,True,())
            for ps in (initial+[1]*6,initial[:-1]+[1]*7,initial+[1,1,2,2,2]):
                old = list(range(len(ps)))
                for e in (set(),{0},set(range(1,k)),set(range(0,k,3))):
                    vh = set(rng.sample(range(k),(len(e)+1)%k))
                    for target in (0,1,3,9):
                        removed = [0]*(len(ps)-2)+[(sum(old)+sum(range(k))+target)%k]
                        result = construct(k,edges,ps,old,removed,e,vh,rng)
                        if result is None:
                            deg = Counter(v for edge in edges for v in edge)
                            deg.update(ps)
                            assert k%2==0 and target%2 and not e and all(c%2==0 for c in deg.values())
                            parity += 1
                        else:
                            steps,(aux,labels,absent,dup,gap,holes) = result
                            inspect(k,edges,ps,old,removed,e,vh,(aux,labels,absent,dup[1],gap[1],holes))
                            good += 1
                            longest = max(longest,steps)
    for k in range(5,2001): cover(k)
    print('random-pin targets',good,'parity obstructions',parity,'maximum draws',longest,
          'all-modulus covers',1996)


if __name__=='__main__':
    main()

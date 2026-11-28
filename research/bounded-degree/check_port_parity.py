"""Compare complete palette enumeration and reconstruct the auxiliary tree targets."""
from collections import Counter
from itertools import combinations
from math import gcd
from random import Random

from check_two_leaf_repair import inspect
from port_parity import build
from multiport import construct
from check_unicyclic_core import inspect as inspect_closed


def all_profiles():
    cases = 0
    for k in range(4,10):
        G = set(range(k))
        layers = [[set(xs) for xs in combinations(range(k),a)] for a in range(k)]
        for h in range(2,k):
            if k%h: continue
            for e in range(k):
                for high_e in layers[e]:
                    edge = {(b-f)%h for b in G-high_e for f in high_e}
                    for high_v in layers[(e+1)%k]:
                        vertex = {2*(f-b)%h for b in G-high_v for f in high_v}
                        # Require at least one genuine transfer even for target zero.
                        totals = edge|vertex|{(x+y)%h for x in edge for y in vertex}
                        for t in range(h):
                            blocked = not high_e and h%2==0 and t%2==1
                            assert ((-t)%h in totals)==(not blocked)
                            cases += 1
    return cases


def piece(k,charges,adjacent,center_ports):
    # Two port tips at the ends of a spine. Grow enough short tip arms at
    # each marked joint to realize its charge, allowing an entering edge there.
    t = sum(charges)+2
    internal_ports = set(center_ports)
    n = k-(t-2-len(internal_ports))
    edges = [(v-1,v) for v in range(1,n)]
    ports = [0,n-1]
    tip = n
    for j,c in enumerate(charges):
        v = (j+1)*(1 if adjacent else 17)
        if j in internal_ports:
            ports.append(v)
        for _ in range(c-(j in internal_ports)):
            edges.append((v,tip))
            ports.append(tip)
            tip += 1
    assert tip==k and len(ports)==t
    return edges,ports


def concrete_star(k,t):
    # Every augmented free degree is even. The actual old star has
    # uniform edge bins, and its retained entering site has either parity.
    edges,ports = piece(k,[t-2],False,())
    degree = Counter(v for edge in edges for v in edge)
    for v in ports: degree[v] += 1
    assert all(d%2==0 for d in degree.values())
    old = [0]+list(range(k))
    removed = list(range(t-1))
    remaining = [old[i+1] for i in range(k) if i not in removed]
    main = next(x for x in remaining if (x-k*(k-1)//2)%2)
    entering = [main]+removed
    assert Counter((old[0]+x)%k for x in old[1:])==Counter(range(k))
    assert max(Counter(old).values())-min(Counter(old).values())==1
    assert (sum(entering)-sum(removed)-sum(range(k)))%2
    # The inserted whole tree has order 2k+1, hence every edge count must be two.


def small_boundaries(rng):
    checked = blocked = 0
    for k in (180,225,256,315):
        path = [(v-1,v) for v in range(1,k)]
        for tree,port in ((path,k//2),([((v-1)//2,v) for v in range(1,k)],k//3)):
            aux,cut,labels,pairs,wires,_ = construct(tree,[port],[13],[],rng)
            inspect_closed(k,aux,cut,labels)
            assert not pairs and set(aux[:cut])==set(tree)
            assert sum(labels[v] for v in wires[0])%k==(labels[port]+13)%k
            checked += 1
        for ports,targets in (([0,k-1],[1,2,k//2,k-1]),([k//3,k-1],[0])):
            for target in targets:
                old = [13,27]
                removed = [(target+sum(old)+sum(range(k)))%k]
                for eh in (set(),{0},set(range(k-1)),set(range(0,k,3))):
                    vh = set(rng.sample(range(k),(len(eh)+1)%k))
                    data = build(path,ports,old,removed,eh,vh,rng)
                    if data is None:
                        assert len(ports)==2 and ports[0]==0 and not eh and k%2==0 and target%2
                        blocked += 1
                    else:
                        aux,labels,absent,dup,gap,holes = data
                        inspect(k,path,ports,old,removed,eh,vh,(aux,labels,absent,dup[1],gap[1],holes))
                        checked += 1
    return checked,blocked


def run():
    rng = Random(10481991)
    outcomes = Counter()
    for k in (504,625,720,1024,1350):
        for charges in ([2],[3],[4],[6],[2,2],[3,3],[4,4],[2,4],[3,6],[2,2,2]):
            h = gcd(k,gcd(*charges)) if len(charges)>1 else gcd(k,charges[0])
            if h==1: continue
            for adjacent,at in ((True,()),(False,(0,)),(True,tuple(range(len(charges))))):
                edges,ports = piece(k,charges,adjacent,at)
                for target in range(h):
                    old = [rng.randrange(k) for _ in ports]
                    removed = [rng.randrange(k) for _ in ports[1:]]
                    removed[-1] = (removed[-1]+target-(sum(removed)-sum(old)-k*(k-1)//2))%k
                    profiles = (set(),{0},set(range(1,k)),set(range(0,k,3)),set(rng.sample(range(k),k//3)))
                    for edge_high in profiles:
                        vh = set(rng.sample(range(k),(len(edge_high)+1)%k))
                        data = build(edges,ports,old,removed,edge_high,vh,rng)
                        if data is None:
                            assert not edge_high and h%2==0 and target%2==1
                            outcomes['parity'] += 1
                            continue
                        aux,labels,absent,dup,gap,holes = data
                        inspect(k,edges,ports,old,removed,edge_high,vh,
                                (aux,labels,absent,dup[1],gap[1],holes))
                        d = labels.copy()
                        if absent is not None: d[absent] = dup[1]
                        original = {frozenset(e) for e in edges}
                        actual = {frozenset(e) for e in aux}
                        diff = Counter((d[u]+d[v])%k for u,v in original-actual)
                        diff.update((d[v]+a)%k for v,a in zip(ports,old))
                        diff.subtract((d[u]+d[v])%k for u,v in actual-original)
                        diff.subtract(removed)
                        expected = Counter(holes+[dup[0]])
                        expected.subtract([gap[0]])
                        assert all(diff[i]==expected[i] for i in range(k))
                        outcomes['both' if absent is not None and dup[0]!=gap[0] else
                                 'vertex' if absent is not None else 'edge'] += 1
    for k in (80,82,128,130):
        for t in (4,6,8):
            concrete_star(k,t)
    print('reconstructed targets and parity obstructions',sorted(outcomes.items()),
          'literal star obstructions',12,'exhaustive histogram pairs and targets',all_profiles(),
          'one- and two-port successes and obstructions',small_boundaries(rng))


if __name__=='__main__':
    run()

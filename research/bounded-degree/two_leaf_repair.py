"""Build a prescribed tree embedding when a uniform multiport insertion fails."""
from collections import Counter
from functools import reduce
from math import gcd

from check import adjacency
from check_excess import expression
from multiport import lift_marks, neighborhood, residue_sums, routing
from unicyclic_core import core


def transfer(k,g,m,edge_high,vertex_high):
    """Return (palette to change, duplicated bin, omitted bin)."""
    for kind,high in (('edge',edge_high),('vertex',vertex_high)):
        for omitted in sorted(high):
            # For edges: m + duplicated - omitted = 0.
            # For vertices: m + omitted - duplicated = 0.
            residue = (omitted+(-m if kind=='edge' else m))%g
            for duplicated in range(residue,k,g):
                if duplicated not in high:
                    return kind,duplicated,omitted
    raise ValueError('incompatible old bin counts')


def build(edges,ports,old,removed,edge_high,vertex_high,rng):
    k = len(edges)+1
    adj = adjacency(k,edges)
    multiplicity = Counter(ports)
    marked_ports = set(ports)
    c = [len(row)-1+multiplicity[v] for v,row in enumerate(adj)]
    m = sum(removed)-sum(old)
    divisor = reduce(gcd,c,k)
    assert m%divisor
    kind,dup,gap = transfer(k,divisor,m,edge_high,vertex_high)
    reps = {weight:v for v,weight in enumerate(c) if weight}
    leaves = [v for v,weight in enumerate(c) if not weight][:2]
    protected = marked_ports|set(reps.values())|set(leaves)
    absent = parent = None
    d = Counter(len(row) for row in adj if len(row)>=2).most_common(1)[0][0]
    g = gcd(k,d-1)
    credits = list(removed)
    if kind=='vertex':
        forbidden = neighborhood(adj,protected,2)
        absent = next(v for v in range(k) if c[v]==0 and v not in forbidden)
        parent, = adj[absent]
        protected.update((parent,absent))
        target = m+gap-dup
    else:
        credits.append(dup)
        target = m+dup-gap
    pairs,kept,anchors,wires = routing(edges,adj,len(ports),protected,d,closed=False)
    variables = set(ports)|set(anchors)|set(reps.values())|{a for a,b in pairs}
    if absent is not None:
        variables.update((parent,pairs[-1][1]))
        kept = [edge for edge in kept if absent not in edge]
    residues = dict.fromkeys(variables,0)
    initial = sum(c[b]*w for (_,b),w in zip(pairs,credits))
    values = residue_sums(g,reps,target-initial)
    residues.update(dict(zip(reps.values(),values)))
    forms = {v:expression((v,1),constant=a) for v,a in residues.items()}
    for (a,b),w in zip(pairs,credits):
        forms[b] = expression((a,-1),constant=w-residues[a])
    sums = []
    for (anchor,site),v,a in zip(wires,ports,old):
        sums.append(expression((v,1),constant=residues[v]+a))
        forms[site] = expression((v,1),(anchor,-1),constant=residues[v]+a-residues[anchor])
    vs = list(forms.values())
    for a,b in kept:
        if a in forms and b in forms:
            sums.append(expression(*forms[a].items(),*forms[b].items()))
    if absent is None:
        sums.append(expression(constant=gap))
    else:
        vs.append(expression(constant=gap))
        a,b = pairs[-1]
        sums.extend((expression(*forms[parent].items(),constant=dup),
                     expression(*forms[a].items(),*forms[b].items())))
    pins = lift_marks(k,g,variables,forms,(vs,sums),rng)
    auxiliary = kept+wires
    holes = [gap] if absent is None else [(dup+pins[parent])%k,
                                         sum(pins[v] for v in pairs[-1])%k]
    labels = core(k,auxiliary,None,pins,leaves,d,absent=absent,
                  forbidden_vertex=gap if absent is not None else None,holes=holes)
    return auxiliary,labels,absent,dup,gap,holes

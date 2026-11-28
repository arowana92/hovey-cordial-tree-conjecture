"""Lift prescribed residue counts and arbitrarily located pins to a rainbow embedding."""
from collections import Counter, defaultdict, deque
from functools import reduce
from math import gcd
from pathlib import Path
import sys

from check import adjacency
from sparse_ports import particular
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from research.census.long_bridge import moment,subset_sum


def reduce_degree(adj,cap,pins):
    n = len(adj)
    groups = defaultdict(list)
    for v,neighbors in enumerate(adj):
        if v not in pins:
            groups[len(neighbors)].append(v)
    common = max((d for d in groups if d<=cap),key=lambda d:len(groups[d]))
    reps = {d:vs[0] for d,vs in groups.items()}
    sites = set(groups[common][1:])
    root = min(sites)
    parent,component = {root:None},{root:root}
    order = [root]
    kept,cuts = [],{}
    for v in order:
        children = sorted(adj[v]-{parent[v]})
        limit = cap-int(v!=root)
        for j,u in enumerate(children):
            order.append(u)
            parent[u] = v
            if j<limit:
                kept.append((v,u))
                component[u] = component[v]
            else:
                cuts[u] = v
                component[u] = u
    supply = defaultdict(list)
    for v in sorted(sites):
        supply[component[v]].append(v)
    ready = deque(supply[root])
    copies = {}
    for u in sorted(cuts,key=lambda u:not bool(supply[u])):
        if not ready:
            raise ValueError("Insufficient fresh sites for reconnection")
        z = ready.popleft()
        kept.append((z,u))
        copies[z] = cuts[u]
        ready.extend(supply[u])
    return common,reps,kept,copies


def cover_classes(aux,kernel):
    groups = defaultdict(list)
    for v,neighbors in enumerate(aux):
        groups[len(neighbors)].append(v)
    for vs in groups.values():
        free = [v for v in vs if v not in kernel]
        needed = max(0,6-(len(vs)-len(free)))
        kernel.update(free if len(free)-needed < 6 else free[:needed])


def lift_pins(k,m,aux,low):
    n = k*m
    labels,seen,sums = {},set(),set()
    for v,r in low.items():
        old = [labels[u] for u in aux[v] if u in labels]
        for value in range(r,n,k):
            weights = [(value+y)%n for y in old]
            if value not in seen and sums.isdisjoint(weights):
                seen.add(value)
                sums.update(weights)
                labels[v] = value
                break
        else:
            raise ValueError("The lift fibers are too small for these pins")
    return labels,sums


def palette(k,m,counts,protected,target):
    n = k*m
    omitted = set()
    for x,count in enumerate(counts):
        needed = m-count-(2 if x==0 else 0)
        if needed<0:
            raise ValueError("Two slots must be available for the moment adjustment")
        for v in range(x,n,k):
            if not needed:
                break
            if v not in protected:
                omitted.add(v)
                needed -= 1
        if needed:
            raise ValueError("Too many required values in a lift fiber")
    remainder = (n*(n-1)//2-target-sum(omitted))%n
    if remainder%k:
        raise ValueError("Incompatible projected moment")
    for v in range(0,n,k):
        w = (remainder-v)%n
        if v!=w and {v,w}.isdisjoint(omitted) and {v,w}.isdisjoint(protected):
            omitted.update((v,w))
            return set(range(n))-omitted
    raise ValueError("No two unused lifts supply the target moment")


def prepare(k,edges,pins,vertices,weights,cap):
    """Return the auxiliary tree and embedding hypotheses, or None for a failed congruence."""
    adj = adjacency(len(edges)+1,edges)
    common,reps,tree,copies = reduce_degree(adj,cap,pins)
    aux = adjacency(len(adj),tree)
    kernel = set(pins)|set(reps.values())|set(copies)|set(copies.values())
    cover_classes(aux,kernel)
    low = dict.fromkeys(sorted(kernel),0)
    low.update(pins)
    vertex_rest = moment(vertices)-sum(pins.values())
    edge_rest = moment(weights)-sum(len(adj[v])*x for v,x in pins.items())
    terms = {v:d-common for d,v in reps.items() if d!=common}
    values = particular(k,terms,edge_rest-common*vertex_rest)
    if values is None:
        return None
    low.update(values)
    for z,v in copies.items():
        low[z] = low[v]
    anchor = reps[common]
    low[anchor] = (moment(vertices)-sum(low.values()))%k
    m = max(max(vertices),max(weights))+2
    labels,sums = lift_pins(k,m,aux,low)
    V = palette(k,m,vertices,set(labels.values()),sum(labels.values()))
    E = palette(k,m,weights,sums,sum(len(aux[v])*x for v,x in labels.items()))
    return k*m,tree,copies,labels,V,E


def cordial_targets(k,edges,pins):
    n = len(edges)+1
    degree = Counter(v for edge in edges for v in edge)
    degrees = {degree[v] for v in range(n) if v not in pins}
    pivot = min(degrees)
    g = reduce(gcd,(d-pivot for d in degrees),k)
    p = sum(pins.values())
    w = sum(degree[v]*x for v,x in pins.items())
    q,r = divmod(n,k)
    b,j = divmod(n-1,k)
    total = sum(range(k))
    if j:
        high_v = list(range(r))
        target = w+pivot*(q*total+sum(high_v)-p)-b*total
        high_e = subset_sum(k,j,target)
    else:
        x = next((x for x in range(k) if (b*total-w-pivot*(q*total+x-p))%g==0),None)
        if x is None:
            return None
        high_v,high_e = [x],[]
    return ([q+int(i in high_v) for i in range(k)],
            [b+int(i in high_e) for i in range(k)])

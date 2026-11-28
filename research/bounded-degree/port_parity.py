"""Prescribed cores for multiport repairs with all leaves among the ports."""
from collections import Counter
from functools import reduce
from math import gcd

from check import adjacency
from check_excess import choose_variables, expression
from multiport import neighborhood
from sparse_ports import particular


def options(k,h,high):
    """For each attainable difference mod h, keep a pair of large residue bins."""
    upper = [[] for _ in range(h)]
    lower = [[] for _ in range(h)]
    for x in range(k):
        (upper if x in high else lower)[x%h].append(x)
    result = {}
    for i,dup in enumerate(lower):
        for j,gap in enumerate(upper):
            if not dup or not gap:
                continue
            r = (i-j)%h
            if r not in result or max(len(dup),len(gap))>max(map(len,result[r])):
                result[r] = dup,gap
    return result


def plan(k,h,target,edge_high,vertex_high):
    edge = options(k,h,edge_high)
    vertex = options(k,h,vertex_high)
    for a in edge:
        if (target+a)%h==0:
            return edge[a],None
    for b in vertex:
        if (target-2*b)%h==0:
            return None,vertex[b]
    for a in edge:
        for b in vertex:
            if (target+a-2*b)%h==0:
                return edge[a],vertex[b]
    return None


def select(k,h,target,positive,ports,old,moves):
    """In the single-joint case vary one histogram bin to free its label."""
    e,v = moves
    chosen = [bins[0][0] if bins else None for bins in (e,v)]
    gaps = [bins[1][0] if bins else None for bins in (e,v)]
    which = 0 if e else 1
    bins = (e,v)[which]
    values = chosen if len(bins[0])>=len(bins[1]) else gaps
    choices = max(bins,key=len)
    joint_sites = [a for v,a in zip(ports,old) if v in positive] if len(positive)==1 else []
    for x in choices:
        values[which] = x
        shift = (chosen[0]-gaps[0] if e else 0)-2*(chosen[1]-gaps[1] if v else 0)
        total = (target+shift)%k
        if len(positive)!=1:
            return chosen,gaps,total,None
        joint,d = next(iter(positive.items()))
        base = (total//h)*pow(d//h,-1,k//h)%(k//h)
        for a in range(base,k,k//h):
            if a not in old and a!=gaps[1] and all((a+b)%k!=gaps[0] for b in joint_sites):
                return chosen,gaps,total,a
    raise ValueError('insufficient choices for a joint label')


def marks(k,adj,ports,old,positive,total,joint_label,vertex_gap,edge_gap,rng,leaf):
    marked = set(ports)|set(positive)
    if leaf is not None:
        marked.add(leaf)
    joint,c = next(iter(positive.items()),(None,None))
    forms = {v:expression((v,1)) for v in marked}
    if leaf is not None:
        forms[leaf] = expression((joint,1),constant=-total)
    elif joint_label is not None:
        forms[joint] = expression(constant=joint_label)
    elif positive:
        values = particular(k,positive,total)
        if len(positive)==2:
            v,w = positive
            if positive[v]==positive[w] and w in adj[v] and (values[v]+values[w])%k==edge_gap:
                values[v] += k//gcd(k,c)
        for v in marked-{joint}:
            forms[v] = expression((v,c),constant=values.get(v,0))
        forms[joint] = expression(*[(v,-b) for v,b in positive.items() if v!=joint],
                                  constant=values[joint])
    vertices = list(forms.values())
    if vertex_gap is not None:
        vertices.append(expression(constant=vertex_gap))
    weights = [expression(constant=edge_gap)]
    weights.extend(expression(*forms[v].items(),constant=a) for v,a in zip(ports,old))
    weights.extend(expression(*forms[v].items(),*forms[w].items())
                   for v in marked for w in adj[v] if w in marked and v<w)
    evaluate = choose_variables(vertices,weights,k,rng)
    return {v:evaluate(f) for v,f in forms.items()}


def windows(adj,protected,count):
    forbidden = neighborhood(adj,protected,2)
    segments = []
    for root in range(len(adj)):
        if root in forbidden or len(adj[root])!=2:
            continue
        left,right = [root],[root]
        for path,start in zip((left,right),sorted(adj[root])):
            path.append(start)
            while len(path)<5 and len(adj[path[-1]])==2:
                path.append(next(v for v in adj[path[-1]] if v!=path[-2]))
        path = left[:0:-1]+right
        if len(path)!=9 or forbidden.intersection(path) or any(len(adj[v])!=2 for v in path):
            continue
        segments.append(path)
        forbidden.update(neighborhood(adj,path,1))
        if len(segments)==count:
            return segments
    raise ValueError('insufficient disjoint path windows')


def build(edges,ports,old,removed,edge_high,vertex_high,rng):
    k = len(edges)+1
    adj = adjacency(k,edges)
    boundary = Counter(ports)
    delta = [len(row)-2+boundary[v] for v,row in enumerate(adj)]
    outside_leaves = [v for v,c in enumerate(delta) if c<0]
    positive = {v:c for v,c in enumerate(delta) if c>0}
    target = sum(removed)-sum(old)-k*(k-1)//2
    leaf = None
    if outside_leaves:
        # Only the uniformly obstructed two-port, one-outside-leaf case.
        leaf, = outside_leaves
        assert len(ports)==2 and target%k==0
        joint_label = None
        if edge_high:
            f = min(edge_high)
            b = next(x for x in range(k) if x not in edge_high)
            dup,gap,total = [b,None],[f,None],b-f
        else:
            f, = vertex_high
            b = next(x for x in range(k) if (2*(x-f))%k)
            dup,gap,total = [None,b],[None,f],2*(f-b)
    else:
        h = reduce(gcd,positive.values(),k)
        assert (h>1 or len(positive)==1) and (positive or target%k)
        moves = plan(k,h,target,edge_high,vertex_high)
        if moves is None:
            return None
        dup,gap,total,joint_label = select(k,h,target,positive,ports,old,moves)
    if gap[0] is None:
        # A cut of the same color as this hole implements zero edge transfer.
        avoid = {(joint_label+a)%k for v,a in zip(ports,old)
                 if joint_label is not None and v in positive}
        gap[0] = dup[0] = next(x for x in range(k) if x not in avoid)
    labels = marks(k,adj,ports,old,positive,total,joint_label,gap[1],gap[0],rng,leaf)
    segments = windows(adj,set(labels),len(ports)+(gap[1] is not None))
    used = set(labels.values())
    if gap[1] is not None:
        used.add(gap[1])

    def pair(a,b,w):
        x = next(i for i in range(k) if i not in used and (w-i)%k not in used and (w-i)%k!=i)
        labels[a],labels[b] = x,(w-x)%k
        used.update((labels[a],labels[b]))

    auxiliary = {tuple(sorted(e)) for e in edges}
    for seg,v,a,w in zip(segments,ports,old,list(removed)+[dup[0]]):
        b,c = seg[3:5]
        auxiliary.remove(tuple(sorted((b,c))))
        auxiliary.add(tuple(sorted((seg[1],seg[6]))))
        pair(b,c,w)
        pair(seg[1],seg[6],labels[v]+a)
    holes = [gap[0]]
    absent = None
    if gap[1] is not None:
        seg = segments[-1]
        b,absent,c = seg[3:6]
        auxiliary.remove(tuple(sorted((b,absent))))
        auxiliary.remove(tuple(sorted((absent,c))))
        weights = {(labels[v]+a)%k for v,a in zip(ports,old)}|set(holes)
        weights.update((labels[i]+labels[j])%k for i,j in auxiliary if i in labels and j in labels)
        fresh = []
        for v in (b,c):
            x = next(i for i in range(k) if i not in used and (dup[1]+i)%k not in weights)
            labels[v] = x
            used.add(x)
            fresh.append((dup[1]+x)%k)
            weights.add(fresh[-1])
        auxiliary.add(tuple(sorted((seg[1],seg[7]))))
        pair(seg[1],seg[7],fresh[0])
        holes.append(fresh[1])
    graph = adjacency(k,auxiliary)
    forbidden = neighborhood(graph,labels,1)
    isolated = []
    for v in range(k):
        if len(graph[v])==2 and v not in forbidden:
            isolated.append(v)
            forbidden.update(graph[v])
            if len(isolated)==6: break
    assert len(isolated)==6
    for v in isolated[:4]:
        labels[v] = next(x for x in range(k) if x not in used)
        used.add(labels[v])
    pair(*isolated[4:],k*(k-1)//2-(gap[1] or 0)-sum(labels.values()))
    return list(auxiliary),labels,absent,dup,gap,holes

"""Neutral one-period attachments, with an explicit prescribed embedding core."""
from collections import Counter
from functools import reduce
from math import gcd

from check import adjacency
from forest_spectrum import build as forest_gap
from rooted_gap import build as rooted_gap


def path_marks(k,path_edges,path,labels,vertex_palette,edge_palette,outside=None):
    """The pinned endpoints already have the required incidence moment."""
    graph = adjacency(k,path_edges)
    avoid = set(labels).union(*(graph[v] for v in labels))
    sites = []
    for v in path:
        if v not in avoid and len(graph[v])==2:
            sites.append(v)
            avoid.update(graph[v])
            if len(sites)==6:
                break
    assert len(sites)==6
    used = set(labels.values())
    for v in sites[:4]:
        a = min(vertex_palette-used)
        labels[v]=a
        used.add(a)
    total = (sum(vertex_palette)-sum(labels.values()))%k
    a = next(a for a in sorted(vertex_palette-used)
             if (total-a)%k in vertex_palette-used and a!=(total-a)%k)
    labels[sites[4]],labels[sites[5]]=a,(total-a)%k
    if outside:
        labels.update(outside)
    return path_edges,vertex_palette,edge_palette,labels,0


def one_path(parents,boundary,root,singles):
    k=len(parents)
    group=set(range(k))
    graph=adjacency(k,[(p,v) for v,p in enumerate(parents) if p>=0])
    path=[root]
    for v in path:
        path.extend(w for w in graph[v] if parents[w]==v)
    fixed,weights={},set()
    for i,r in enumerate(singles):
        for a in sorted(group-set(fixed.values())):
            w=(boundary[r]+a)%k
            if w in weights:
                continue
            if i+1==len(singles):
                end=(sum(group)-sum(fixed.values())-a+sum(boundary.values()))%k
                if end==a or end in fixed.values():
                    continue
            fixed[r]=a
            weights.add(w)
            break
        else:
            raise ValueError("no singleton label")
    end=(sum(group)-sum(fixed.values())+sum(boundary.values()))%k
    vertices=group-set(fixed.values())
    x=next(a for a in sorted(vertices-{end}) if (a+boundary[root])%k not in weights)
    weights.add((x+boundary[root])%k)
    marks={root:x,path[-1]:end}
    return path_marks(k,list(zip(path,path[1:])),path,marks,vertices,group-weights,fixed)


def two_paths(parents,boundary,roots,tips):
    k=len(parents)
    group=set(range(k))
    root,other=roots
    endpoint={}
    for z in tips:
        v=z
        while parents[v]>=0:
            v=parents[v]
        endpoint[v]=z
    a,b=endpoint[root],endpoint[other]
    tree=[(p,v) for v,p in enumerate(parents) if p>=0]+[(a,b)]
    x=(sum(group)+boundary[other])%k
    joint=(x+boundary[root])%k
    y=next(y for y in sorted(group-{x}) if (y+boundary[other])%k!=joint)
    gap=(y+boundary[other])%k
    for z in range(k):
        pins={root:x,other:y,a:z,b:(joint-z)%k}
        if len(set(pins.values()))<4: continue
        weights=[(pins[u]+pins[v])%k for u,v in tree if u in pins and v in pins]
        if len(weights)==len(set(weights)) and gap not in weights:
            return path_marks(k,tree,range(k),pins,group,group-{gap})
    raise ValueError("could not pin the two paths")


def build(parents,boundary,bound,rng):
    k=len(parents)
    group=set(range(k))
    roots=list(boundary)
    children=Counter(p for p in parents if p>=0)
    g=reduce(gcd,(children[v] for v in range(k)),k)
    if sum(boundary.values())%g:
        return None
    tips=[v for v,p in enumerate(parents) if p>=0 and not children[v]]
    singles=[r for r in roots if not children[r]]
    if len(tips)==1:
        root=next(r for r in roots if children[r])
        return one_path(parents,boundary,root,singles)
    if len(tips)==2 and not singles:
        if len(roots)==2:
            return two_paths(parents,boundary,roots,tips)
        root,=roots
        edges=[(p,v) for v,p in enumerate(parents) if p>=0]
        tree,marks=rooted_gap(edges,root,0,bound,rng)
        return tree,group,group-{0},marks,boundary[root]
    if len(tips)<2:
        raise ValueError("the sublinear component bound requires a nontrivial component")
    leaf = singles[0] if singles else tips[0]
    parent = parents[leaf]
    shift = 1 if parent in boundary and boundary[parent]==0 else 0
    beta={r:(b-shift)%k for r,b in boundary.items()}
    keep=[v for v in range(k) if v!=leaf]
    index={v:i for i,v in enumerate(keep)}
    small=[-1 if parents[v]<0 else index[parents[v]] for v in keep]
    incoming={index[r]:b for r,b in beta.items() if r!=leaf}
    if parent<0:
        pins,gap={},beta[leaf]
    else:
        h=reduce(gcd,(children[v] for v in range(k) if v!=parent),k)
        banned={0}
        if parents[parent] in beta:
            banned.add(beta[parents[parent]])
        x=next(x for x in range(1,k) if x not in banned
               and (children[parent]*x+sum(beta.values()))%h==0)
        pins,gap={index[parent]:x},x
    result=forest_gap(small,incoming,pins,gap,bound,rng)
    if result is None:
        raise ValueError("unexpected forest-gap obstruction")
    _,tree,marks=result
    back=keep+[leaf]
    return ([(back[u],back[v]) for u,v in tree],group,group-{gap},
            {back[v]:x for v,x in marks.items()},shift)


def lift_boundary(parents,boundary,k):
    """Lift external residues to the forest order before constructing one period."""
    n=len(parents)
    if k<1 or n%k:
        raise ValueError("forest order must be divisible by the modulus")
    children=Counter(p for p in parents if p>=0)
    h=reduce(gcd,(children[v] for v in range(n)),n)
    g=gcd(h,k)
    total=sum(boundary.values())
    if total%g:
        return None
    modulus=h//g
    digit=0 if modulus==1 else (-total//g)*pow(k//g,-1,modulus)%modulus
    lifted=boundary.copy()
    lifted[min(lifted)]+=k*digit
    return lifted

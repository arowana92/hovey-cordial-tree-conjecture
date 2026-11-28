"""Exact compatibility tests and small embeddings for partially labeled trees."""
from collections import Counter
from functools import reduce
from math import gcd

from check import adjacency
from check_excess import choose_variables,expression
from multiport import lift_marks,neighborhood,residue_sums
from sparse_ports import particular
from unicyclic_core import core


def valid(pins,edges,k,gap):
    weights = [(pins[u]+pins[v])%k for u,v in edges if u in pins and v in pins]
    return (len(set(pins.values()))==len(pins) and all(0<=x<k for x in pins.values()) and
            len(set(weights))==len(weights) and gap not in weights)


def groups(forms,edges,gap):
    weights = [expression(constant=gap)]
    weights.extend(expression(*forms[u].items(),*forms[v].items())
                   for u,v in edges if u in forms and v in forms)
    return list(forms.values()),weights


def dense(k,edges,adj,pins,gap,leaves,rng):
    c = [len(row)-1 for row in adj]
    target = -gap-sum(c[v]*x for v,x in pins.items())
    h = reduce(gcd,(a for v,a in enumerate(c) if v not in pins),k)
    if target%h: return None
    d = Counter(len(row) for row in adj if len(row)>1).most_common(1)[0][0]
    g = gcd(k,d-1)
    reps = {a%g:v for v,a in enumerate(c) if v not in pins and a%g}
    residues = residue_sums(g,reps,target)
    forms = {v:expression(constant=x) for v,x in pins.items()}
    forms.update({v:expression((v,1),constant=x) for v,x in zip(reps.values(),residues)})
    labels = lift_marks(k,g,reps.values(),forms,groups(forms,edges,gap),rng)
    return core(k,edges,None,labels,leaves[:2],d,holes=[gap])


def forced_collision(group,k):
    seen = set()
    for form in group:
        key = tuple(sorted((v,a if v!=-1 else a%k) for v,a in form.items() if v!=-1 or a%k))
        if key in seen: return True
        seen.add(key)
    return False


def sparse(k,edges,adj,pins,gap,rng):
    terms = {v:len(row)-2 for v,row in enumerate(adj) if len(row)!=2 and v not in pins}
    target = (-sum(range(k))-gap-sum((len(adj[v])-2)*x for v,x in pins.items()))%k
    integer_gcd = reduce(gcd,terms.values(),0)
    if integer_gcd==0:
        if target: return None
        labels = pins.copy()
    else:
        h = gcd(k,integer_gcd)
        if target%h: return None
        primitive = {v:c//integer_gcd for v,c in terms.items()}
        j,d = next(iter(primitive.items()))
        first = target//h*pow(integer_gcd//h,-1,k//h)%(k//h)
        for y in range(first,k,k//h):
            sol = particular(k,primitive,y)
            forms = {v:expression(constant=x) for v,x in pins.items()}
            forms.update({v:expression((v,d),constant=sol[v]) for v in primitive if v!=j})
            forms[j] = expression(*[(v,-n) for v,n in primitive.items() if v!=j],constant=sol[j])
            vertices,weights = groups(forms,edges,gap)
            if forced_collision(vertices,k) or forced_collision(weights,k): continue
            evaluate = choose_variables(vertices,weights,k,rng)
            labels = {v:evaluate(form) for v,form in forms.items()}
            break
        else: return None
    blocked = neighborhood(adj,labels,1)
    spare = []
    for v in range(k):
        if len(adj[v])==2 and v not in blocked:
            spare.append(v)
            blocked.update(adj[v])
            if len(spare)==6: break
    assert len(spare)==6
    used = set(labels.values())
    for v in spare[:4]:
        labels[v] = next(x for x in range(k) if x not in used)
        used.add(labels[v])
    total = sum(range(k))-sum(labels.values())
    x = next(x for x in range(k) if x not in used and (total-x)%k not in used and (total-x)%k!=x)
    labels[spare[4]],labels[spare[5]] = x,(total-x)%k
    return labels


def build(edges,pins,gap,rng):
    k = len(edges)+1
    if not valid(pins,edges,k,gap): return None
    adj = adjacency(k,edges)
    leaves = [v for v,row in enumerate(adj) if len(row)==1 and v not in pins]
    return dense(k,edges,adj,pins,gap,leaves,rng) if len(leaves)>=2 else sparse(k,edges,adj,pins,gap,rng)

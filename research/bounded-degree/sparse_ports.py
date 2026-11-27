"""Uniform multiport insertions with at most one unmarked leaf."""
from collections import Counter
from math import gcd

from check import adjacency
from check_excess import choose_variables, difference, expression
from multiport import neighborhood, routing


def particular(k,terms,target):
    """Solve a single linear congruence, retaining witnesses for each coefficient."""
    moduli = [k]
    for c in terms.values():
        moduli.append(gcd(moduli[-1],c))
    if target%moduli[-1]:
        return None
    values = {}
    for (v,c),before,after in reversed(list(zip(terms.items(),moduli,moduli[1:]))):
        period = before//after
        x = target//after*pow(c//after,-1,period)%period
        values[v] = x
        target -= c*x
    return values


def local(k,adj,ports,old,deleted,rng):
    boundary = dict(zip(ports,old))
    delta = {v:len(row)-2+int(v in boundary) for v,row in enumerate(adj)}
    tips = [v for v,c in delta.items() if c<0]
    assert len(tips)<=1
    positive = {v:c for v,c in delta.items() if c>0}
    marks = set(ports)|set(positive)|set(tips)
    S = k*(k-1)//2
    target = (sum(deleted)-sum(old)-S)%k
    forms = {v:expression((v,1)) for v in marks}
    unpaid = list(ports)
    credits = [w%k for w in deleted]
    if tips:
        y, = tips
        if len(ports)==2 and target==0:
            return None
        forms[y] = expression(*positive.items(),constant=-target)
    elif not positive:
        if target:
            return None
    elif len(positive)==1:
        joint,c = next(iter(positive.items()))
        w0 = Counter(credits)
        for h in range(k):
            if (c*h-target)%k:
                continue
            bad = [r for r in ports if r in adj[joint] and boundary[r]%k==h]
            at_joint = (h+boundary[joint])%k if joint in boundary else None
            options = [w for w in w0 if (w-2*h)%k and (w!=at_joint or w0[w]>=2)]
            if len(options)>=len(bad):
                break
        else:
            return None
        forms[joint] = expression(constant=h)
        for r,w in zip(bad,options):
            forms[r] = expression(constant=(w-h)%k)
            unpaid.remove(r)
            credits.remove(w)
            if at_joint==w:
                unpaid.remove(joint)
                credits.remove(w)
    else:
        solution = particular(k,positive,target)
        if solution is None:
            return None
        z,c = next(iter(positive.items()))
        for v in marks-{z}:
            forms[v] = expression((v,c),constant=solution.get(v,0))
        forms[z] = expression(*[(v,-n) for v,n in positive.items() if v!=z],constant=solution[z])
    weights = [expression(*forms[a].items(),*forms[b].items())
               for a in marks for b in adj[a] if b in marks and a<b]
    weights += [expression(*forms[r].items(),constant=boundary[r]) for r in unpaid]
    evaluate = choose_variables(list(forms.values()),weights,k,rng)
    labels = {v:evaluate(f) for v,f in forms.items()}
    return labels,[(r,(labels[r]+boundary[r])%k) for r in unpaid],credits


def construct(edges,ports,old,deleted,rng):
    k = len(edges)+1
    assert len(ports)==len(set(ports))==len(old)==len(deleted)+1
    adj = adjacency(k,edges)
    case = local(k,adj,ports,old,deleted,rng)
    if case is None:
        return None
    fixed,unpaid,credits = case
    pairs,kept,anchors,wires = routing(edges,adj,len(unpaid),set(fixed),2)
    forms = {v:expression(constant=a) for v,a in fixed.items()}
    for (a,b),w in zip(pairs,credits):
        forms[a] = expression((a,1))
        forms[b] = expression((a,-1),constant=w)
    for (r,b),(anchor,site) in zip(unpaid,wires):
        forms[anchor] = expression((anchor,1))
        forms[site] = expression((anchor,-1),constant=b)
    weights = [expression(constant=b) for r,b in unpaid]
    weights += [expression(*forms[a].items(),*forms[b].items())
                for a,b in kept if a in forms and b in forms]
    evaluate = choose_variables(list(forms.values()),weights,k,rng)
    labels = {v:evaluate(f) for v,f in forms.items()}
    auxiliary = kept+wires
    graph = adjacency(k,auxiliary)
    excluded = neighborhood(graph,labels,1)
    extras = []
    for v in range(k):
        if len(graph[v])==2 and v not in excluded:
            extras.append(v)
            excluded.update(graph[v])
            if len(extras)==6:
                break
    assert len(extras)==6
    used = set(labels.values())
    for v in extras[:4]:
        value = next(i for i in range(k) if i not in used)
        labels[v] = value
        used.add(value)
    total = (k*(k-1)//2-sum(labels.values()))%k
    value = next(i for i in range(k) if i not in used and (total-i)%k not in used and (total-i)%k!=i)
    labels[extras[4]],labels[extras[5]] = value,(total-value)%k
    return auxiliary,len(kept),labels,unpaid,credits,pairs,wires

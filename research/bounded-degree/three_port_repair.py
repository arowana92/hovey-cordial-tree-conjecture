"""Pinned spanning-tree targets for repairing the single-joint obstruction."""
from math import gcd

from check import adjacency
from multiport import neighborhood


def target(k,joint,ports,old,deleted,high):
    d = len(ports)-2
    inv = pow(d,-1,k)
    T = sum(deleted)-sum(old)-k*(k-1)//2
    forbidden = set(old)
    at_joint = old[ports.index(joint)] if joint in ports else None
    if high is not None:
        for dup in range(k):
            if dup in high:
                continue
            for gap in sorted(high):
                h = (T+dup-gap)*inv%k
                if h not in forbidden and (at_joint is None or (h+at_joint)%k!=gap):
                    return h,dup,gap
        raise ValueError('could not avoid the finitely many joint labels')
    for repeated in range(1,k):
        h = (T-2*repeated)*inv%k
        if h not in forbidden|{0,repeated}:
            return h,repeated,None
    raise ValueError('could not move the old surplus')


def build(edges,ports,old,deleted,high=None):
    """For uniform old edges, all old data are normalized at the vertex surplus."""
    k = len(edges)+1
    graph = adjacency(k,edges)
    special = [i for i in range(k) if len(graph[i])-2+(i in ports)]
    joint, = special
    assert gcd(k,len(ports)-2)==1
    h,extra,gap = target(k,joint,ports,old,deleted,high)
    labels = {joint:h}
    used = {h}
    weights = set()
    if joint in ports:
        weights.add((old[ports.index(joint)]+h)%k)
    omitted_vertex = 0 if high is None else None
    if high is None:
        used.add(extra)
    else:
        weights.add(gap)
    # All nonjoint ports are tips. Only a length-one arm meets another mark.
    for v,a in zip(ports,old):
        if v==joint:
            continue
        for x in range(k):
            sums = [(a+x)%k]
            if v in graph[joint]:
                sums.append((h+x)%k)
            if x!=omitted_vertex and x not in used and len(set(sums))==len(sums) and weights.isdisjoint(sums):
                break
        else:
            raise ValueError('no port value')
        labels[v] = x
        used.add(x)
        weights.update(sums)
    arms = []
    for v in graph[joint]:
        arm = [joint,v]
        while len(graph[arm[-1]])>1:
            arm.append(next(w for w in graph[arm[-1]] if w!=arm[-2]))
        arms.append(arm)
    arm = max(arms,key=len)
    assert len(arm)>12*len(ports)+12
    if high is None:
        labels[arm[-3]] = extra

    def fresh_pair(a,b,w):
        x = next(x for x in range(k) if x not in used and x!=omitted_vertex and
                 (w-x)%k not in used and (w-x)%k!=omitted_vertex and (w-x)%k!=x)
        labels[a],labels[b] = x,(w-x)%k
        used.update((x,(w-x)%k))

    auxiliary = {tuple(sorted(e)) for e in edges}
    absent = None
    holes = []
    credits = list(deleted)
    if high is not None:
        credits.append(extra)
        holes.append(gap)
    for i,(r,a) in enumerate(zip(ports,old)):
        start = 4+12*i
        left = arm[start]
        if i<len(credits):
            b,c = arm[start+2:start+4]
            right = arm[start+5]
            auxiliary.remove(tuple(sorted((b,c))))
            fresh_pair(b,c,credits[i])
        else:
            b,absent,c = arm[start+2:start+5]
            right = arm[start+6]
            for v in (b,c):
                x = next(x for x in range(1,k) if x not in used and (extra+x)%k not in weights)
                labels[v] = x
                used.add(x)
                holes.append((extra+x)%k)
                weights.add(holes[-1])
            auxiliary.remove(tuple(sorted((b,absent))))
            auxiliary.remove(tuple(sorted((absent,c))))
        auxiliary.add(tuple(sorted((left,right))))
        fresh_pair(left,right,labels[r]+a)
    adj = adjacency(k,auxiliary)
    exclude = neighborhood(adj,labels,1)
    isolated = []
    for v in range(k):
        if len(adj[v])==2 and v not in exclude:
            isolated.append(v)
            exclude.update(adj[v])
            if len(isolated)==6:
                break
    assert len(isolated)==6
    for v in isolated[:4]:
        x = next(x for x in range(k) if x not in used and x!=omitted_vertex)
        labels[v] = x
        used.add(x)
    total = (k*(k-1)//2-sum(labels.values()))%k
    fresh_pair(*isolated[4:],total)
    return sorted(auxiliary),labels,absent,extra,holes

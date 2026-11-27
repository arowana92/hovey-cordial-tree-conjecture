"""Restore leaf- and star-decorated paths inside specified edges of a sparse tree."""

from dataclasses import dataclass
from itertools import chain
from random import Random

from research.hub.modular_injection import candidates
from research.hub.paired_stars import offsets
from research.hub.pendant_repair import bridge, finish_leaves, neutral_arm, prepare
from research.hub.star_repair import close_leaf_walk


SLOPES = (14,14,28,42,-112,70,56,-42,-70,126,-126,72,45,-54,-72,117,-45,-27,-18,-9,-9)


@dataclass
class Window:
    left: int
    right: int
    spine: list
    direct: dict
    stars: dict
    children: dict


def expand_edge(parents, child, profile):
    """Each internal vertex has (number of leaves, tuple of pendant star arities)."""
    left = parents[child]
    spine = list(range(len(parents),len(parents)+len(profile)))
    parents.extend([left]+spine[:-1])
    parents[child] = spine[-1]
    direct,stars,children = {},{},{}
    for v,(leaves,arities) in zip(spine,profile):
        direct[v] = list(range(len(parents),len(parents)+leaves))
        parents.extend([v]*leaves)
        stars[v] = []
        for size in arities:
            r = len(parents)
            stars[v].append(r)
            children[r] = list(range(r+1,r+1+size))
            parents.extend([v]+[r]*size)
    return Window(left,child,spine,direct,stars,children)


def parameters(size,bound,k,rng):
    """Independent trials followed by the exhaustive separating integer line."""
    radix = 2*bound+3
    scales = [pow(radix,i,k) for i in range(size)]
    return chain(([rng.randrange(k) for _ in scales] for _ in range(min(k,256))),
                 ([z*w % k for w in scales] for z in candidates(k,rng)))


def path_values(p,q,w,z,k):
    d = w-neutral_arm(p,0,3)[-1]-neutral_arm(q,0,4)[-1]
    left = neutral_arm(p,-3*d+14*z,3)
    right = neutral_arm(q,2*d-9*z,4)
    values = left+right[::-1]
    return values if k is None else [x % k for x in values]


def starred(windows,parents,labels,blocked,b,t,gap,k,rng):
    """Twelve windows of 43 internal vertices with a star at each midpoint."""
    roots,auxiliary,direct = [],[],[]
    for i,window in enumerate(windows):
        p,q = labels[window.left],labels[window.right]
        middle = window.spine[21]
        if i%2 == 0:
            j = next(x for x in candidates(k,rng) if x != t and (2*x)%k
                     and x not in blocked and (-x)%k not in blocked)
            blocked.update((j,(-j)%k))
        center = j if i%2 == 0 else (-j)%k
        labels[middle] = center
        for ids,a,c,w in ((window.spine[:21],p,center,center),
                          (window.spine[22:],center,q,(p+q)%k)):
            values = bridge(a,c,w,k,blocked,rng)
            labels.update(zip(ids,values))
            blocked.update(values)
        selected = window.stars[middle][0]
        roots.append(selected)
        for v in window.spine:
            direct.extend(window.direct[v])
            auxiliary.extend(r for r in window.stars[v] if r!=selected)
    children = {r:vs for window in windows for r,vs in window.children.items()}
    jumps = {r:labels[parents[r]] for r in auxiliary}
    rel,total,root_cycles = offsets(auxiliary,jumps,k,rng)
    primary = [children[r][0] for r in roots[:8:2]]
    guards = [children[r][0] for r in roots[8::2]]
    tips = [v for vs in children.values() for v in vs]
    backward = guards+[v for v in tips if v not in primary and v not in guards]+direct
    spine_parents = {parents[v]:labels[parents[v]] for v in direct}
    for a,c,f,u,v in parameters(5,8*(len(backward)+10),k,rng):
        shifts = (a,c,f,(b-t-total-a-c-f)%k,u,v)
        row = {r:(t+a+c+x)%k for r,x in rel.items()}
        for i,d in enumerate(shifts):
            r,r2 = roots[2*i:2*i+2]
            row[r],row[r2] = d,(d+labels[parents[r]])%k
        row.update(zip(primary,(t,(t+a)%k,(t+a+c+total)%k,(b-shifts[3])%k)))
        used = set(row.values())
        if len(used)!=len(row) or not blocked.isdisjoint(used-{t}):
            continue
        row.update(spine_parents)
        result = close_leaf_walk(row,backward,parents,gap,k,blocked,rng)
        if result is not None:
            labels.update(row)
            return result[0],root_cycles,result[1]
    raise ValueError("no disjoint specialization of the starred paths")


def guard_order(window,reverse=False):
    ids = window.spine[::-1] if reverse else window.spine
    total = sum(s*len(window.direct[v]) for s,v in zip(SLOPES,ids))
    sign = -1 if total<0 else 1
    tips = [leaf for positive in (True,False) for s,v in zip(SLOPES,ids)
            if (sign*s>0)==positive for leaf in window.direct[v]]
    return total,tips


def leafy_layout(kind,windows,labels,b,gap,k):
    # Each entry gives a left-to-right (possibly reversed) path and a weight.
    # Marks t, X and G acquire their values in the simultaneous specialization.
    segments,marks = [],{}
    def original(w):
        weight = labels[w.left]+labels[w.right]
        return weight if k is None else weight%k
    if kind=='active':
        guards = []
        for w in windows[:2]:
            total,tips = guard_order(w)
            reverse = total==0
            if reverse:
                total,tips = guard_order(w,True)
            if not total:
                raise ValueError("both orientations of this guard have zero total")
            guards.append(tips)
            vertices = [w.left]+w.spine+[w.right]
            if reverse:
                vertices.reverse()
            segments.append((vertices[1:-1],vertices[0],vertices[-1],original(w)))
        for w,mark,weight in zip(windows[2:],('t','G'),(b,gap)):
            mid = w.spine[21]
            marks[mid] = mark
            segments.append((w.spine[:21],w.left,mid,weight))
            segments.append((w.spine[22:],mid,w.right,original(w)))
        other = [v for w in windows[2:] for vs in w.direct.values() for v in vs]
        first,second = guards
        backward = [first[0],second[0]]+first[1:]+second[1:]+other
    elif kind=='uniform':
        w, = windows
        cut = [w.spine[i] for i in (21,43,65)]
        marks.update(zip(cut,('t','X','G')))
        ends = [w.left]+cut+[w.right]
        for i,weight in enumerate((b,'X',gap,original(w))):
            segments.append((w.spine[22*i:22*i+21],ends[i],ends[i+1],weight))
        m = len(w.direct[w.spine[0]])
        if any(len(vs)!=m for vs in w.direct.values()):
            raise ValueError("a uniform repair needs constant leaf counts")
        guards = [[leaf for pos in (True,False) for s,v in zip(SLOPES,seg[0])
                   if (s>0)==pos for leaf in w.direct[v]] for seg in segments[:2]]
        first,second = guards
        other = [leaf for v in (cut[:1]+w.spine[43:]) for leaf in w.direct[v]]
        backward = ([first[0],second[0]]+first[1:-1]+second[1:-1]+other
                    +[first[-1],second[-1]]) if m else []
    else:
        raise ValueError("unknown repair type")
    if any(w.children for w in windows):
        raise ValueError("a leafy repair expects only direct leaves")
    return segments,marks,backward


def leafy(kind,windows,parents,labels,blocked,b,t,gap,k,rng):
    segments,marks,backward = leafy_layout(kind,windows,labels,b,gap,k)
    # Bridge entries have coefficient at most 126 in their own parameter.
    # In moving marks the arm constant is linear with bounded coefficients.
    # Each backward tail contains at most one term per leaf plus its start.
    for coords in parameters(2+len(segments),10000*(len(backward)+2),k,rng):
        x,g,*zs = coords
        substitution = {'t':t,'X':x,'G':g}
        row = {v:substitution[name] for v,name in marks.items()}
        if 0 in row.values() or len(set(row.values()))!=len(row):
            continue
        for (ids,left,right,weight),z in zip(segments,zs):
            p = row[left] if left in row else labels[left]
            q = row[right] if right in row else labels[right]
            wgt = x if weight=='X' else weight
            row.update(zip(ids,path_values(p,q,wgt,z,k)))
        used = set(row.values())
        if len(used)!=len(row) or not blocked.isdisjoint(used-{t}):
            continue
        if not backward:
            labels.update(row)
            blocked.update(used)
            return g,0,0
        result = close_leaf_walk(row,backward,parents,g,k,blocked,rng)
        if result is not None:
            labels.update(row)
            return result[0],0,result[1]
    raise ValueError("no disjoint specialization of the leaf-decorated paths")


def construct(core,counts,jobs,k,palette,seed=5841):
    """Each job is (kind, [(core edge child, ordered internal profile), ...])."""
    rng = Random(seed)
    parents = list(core)
    labels,bills,blocked,leaves,stats = prepare(core,counts,k,palette,rng)
    if len(jobs)<len(bills) or counts[0]!=max(counts.values()):
        raise ValueError("insufficient windows or wrong root")
    selected = set()
    gap = 0
    for i,(kind,edges) in enumerate(jobs):
        lengths = {'starred':[43]*12,'active':[21,21,43,43],'uniform':[87]}[kind]
        if [len(profile) for _,profile in edges]!=lengths:
            raise ValueError("incorrect window lengths")
        windows = []
        for child,profile in edges:
            if child in selected or not 0<child<len(core):
                raise ValueError("expected distinct compressed edges")
            selected.add(child)
            windows.append(expand_edge(parents,child,profile))
        if i<len(bills):
            b,t = bills[i]
            stats['repairs'] += 1
        else:
            b = t = next(x for x in candidates(k,rng) if x not in blocked)
            stats['neutral'] += 1
        blocked.add(t)
        if kind=='starred':
            gap,r,l = starred(windows,parents,labels,blocked,b,t,gap,k,rng)
        else:
            gap,r,l = leafy(kind,windows,parents,labels,blocked,b,t,gap,k,rng)
        stats['root cycles'] += r
        stats['leaf cycles'] += l
    parents,values = finish_leaves(parents,labels,leaves,counts,k)
    return parents,values,gap,dict(stats)

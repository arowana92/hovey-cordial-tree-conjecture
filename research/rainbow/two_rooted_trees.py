"""Grow a fixed 27-cordial core across two rooted trees with seven tips in total."""
from collections import Counter

from research.marked_leaf import restore_batches
from research.rainbow.generate import native_search


def padded_search(library, k):
    search = native_search(library,k)
    def solve(parents, modulus):
        links = list(parents)
        roots = []
        for v,p in enumerate(links):
            roots.append(v if p < 0 else roots[p])
        largest = Counter(roots).most_common(1)[0][0]
        end = max(v for v,r in enumerate(roots) if r == largest)
        while len(links) < k-1:
            links.append(end)
            end = len(links)-1
        return search(links,modulus)[:len(parents)]
    return solve


def blocks(parent, core, first, k):
    free = set(range(core,len(parent)))
    steps = []
    def record(batch, forced=False):
        chosen = set(batch)
        incoming = [(v,parent[v]) for v in batch if parent[v] not in chosen]
        internal = [(v,parent[v]) for v in batch if parent[v] in chosen]
        steps.append((incoming+internal,len(incoming),forced))
        free.difference_update(chosen)
    while free:
        roots = []
        children = {v:[] for v in free}
        sizes = dict.fromkeys(free,1)
        for v in sorted(free,reverse=True):
            p = parent[v]
            if p in free:
                sizes[p] += sizes[v]
                children[p].append(v)
            else:
                roots.append(v)
        if len(free) <= (k-1 if core%k else k):
            tail = sorted(free-{first})
            if core%k:
                record([first]+tail)
            else:
                if tail:
                    record(tail)
                record([first],True)
            break
        t = (core+len(free)-1)%k
        if not t:
            record([next(v for v in sorted(free) if v != first and not children[v])],True)
            continue
        root = max(roots,key=sizes.get)
        assert sizes[root] > t
        walk, stack = [],[root]
        while stack:
            v = stack.pop()
            walk.append(v)
            stack.extend(sorted(children[v],key=sizes.get,reverse=True))
        record(walk[-t:])
    return reversed(steps)


def grow(parent, old, first, offsets, witness):
    """Each key in offsets is the new endpoint of a bridge. Return order and labels."""
    k = 27
    core = len(old)
    if not 0 < core <= len(parent) or core%k not in (0,1):
        raise ValueError("expected a nonempty core of order zero or one modulo 27")
    if parent[0] != -1 or any(not 0 <= p < v for v,p in enumerate(parent[1:],1)):
        raise ValueError("expected a parent-first tree")
    if any(not 0 <= x < k for x in old):
        raise ValueError("old labels must be residues")
    roots = [v for v in range(core,len(parent)) if parent[v] < core]
    if len(roots)>2 or set(offsets)-set(roots) or (roots and first not in roots):
        raise ValueError("expected up to two bridges and a choice of first root")
    if len(set(range(core,len(parent)))-set(parent)) > 7:
        raise ValueError("the attached trees have more than seven tips")
    vertices = Counter(old)
    weights = Counter((old[v]+old[parent[v]])%k for v in range(1,core))
    for bins in (vertices,weights):
        if max(bins[r] for r in range(k))-min(bins[r] for r in range(k))>1:
            raise ValueError("the initial labeling must be cordial")
    if not roots:
        return [],list(old)

    # Replace the core by a star with the same surplus or the same edge deficit.
    # Every effective bridge color then has an actual old parent of that color.
    if core%k:
        center = max(range(k),key=vertices.__getitem__)
        star = [center]+list(range(k))
    else:
        hole = min(range(k),key=weights.__getitem__)
        center = (14*hole)%k
        star = [center]+[x for x in range(k) if x!=center]
    shift = len(star)-core
    surrogate = [-1]+[0]*(len(star)-1)
    for v in range(core,len(parent)):
        p = parent[v]
        surrogate.append(star.index((old[p]+offsets.get(v,0))%k) if p<core else p+shift)
    labels = dict(enumerate(star))
    counts = Counter((center+x)%k for x in star[1:])
    restore_batches(k,labels,counts,blocks(surrogate,len(star),first+shift,k),witness)
    order = [v-shift for v in list(labels)[len(star):]]
    return order,list(old)+[labels[v+shift] for v in range(core,len(parent))]

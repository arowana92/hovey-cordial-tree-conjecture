"""Extend a fixed cordial labeling by a rooted forest attached at one old vertex."""
from collections import Counter

from ..marked_leaf import restore_batches
from .generate import rainbow


def grow(parent, core_labels, k, *, witness=rainbow):
    """The initial core is a prefix of the parent array. Return additions and all labels."""
    core = len(core_labels)
    if k < 1:
        raise ValueError("the modulus must be positive")
    if not core or core%k not in (0,1):
        raise ValueError("the core must be nonempty and have order zero or one modulo k")
    if core > len(parent) or parent[0] != -1 or any(
            not 0 <= p < v for v,p in enumerate(parent[1:],1)):
        raise ValueError("expected a parent-first tree")
    free = set(range(core,len(parent)))
    sites = {parent[v] for v in free if parent[v] < core}
    if len(sites) > 1:
        raise ValueError("the forest must attach at a single old vertex")
    weights = Counter((core_labels[v]+core_labels[parent[v]])%k for v in range(1,core))
    f = dict(enumerate(core_labels))
    for histogram in (Counter(core_labels),weights):
        bins = [histogram[r] for r in range(k)]
        if max(bins)-min(bins) > 1:
            raise ValueError("the core labeling must be cordial")
    if any(not 0 <= x < k for x in core_labels):
        raise ValueError("core labels must be residues")
    steps = []
    while free:
        children = {v:[] for v in free}
        roots = []
        size = dict.fromkeys(free,1)
        for v in sorted(free,reverse=True):
            p = parent[v]
            if p in free:
                children[p].append(v)
                size[p] += size[v]
            else:
                roots.append(v)
        walk = []
        stack = sorted(roots,key=size.get,reverse=True)
        while stack:
            v = stack.pop()
            walk.append(v)
            stack.extend(sorted(children[v],key=size.get,reverse=True))
        t = (core+len(free)-1)%k
        batch = walk[-(t or 1):]
        selected = set(batch)
        incoming = [(v,parent[v]) for v in batch if parent[v] not in selected]
        internal = [(v,parent[v]) for v in batch if parent[v] in selected]
        steps.append((incoming+internal,len(incoming),t==0))
        free.difference_update(selected)
    restore_batches(k,f,weights,reversed(steps),witness)
    return list(f)[core:], [f[v] for v in range(len(parent))]

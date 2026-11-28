"""Replace high-degree edges by a bounded-degree tree with pinned equal sums."""
from check import adjacency


def reduce_degree(edges,marked,*,root=None,degree_bound=3,reserved=(),site_degree=2,
                  paired_buffers=False):
    k = len(edges)+1
    graph = adjacency(k,edges)
    if root is None:
        root = next(v for v in range(k) if len(graph[v])==1)
    reserved = set(reserved)
    parent = {root:None}
    order = [root]
    cut = []
    for v in order:
        children = sorted((w for w in graph[v] if w!=parent[v]),key=lambda w:(w not in reserved,w))
        for w in children:
            parent[w] = v
            order.append(w)
        cut.extend((v,w) for w in children[degree_bound-1:])
    cut_set = {frozenset(e) for e in cut}
    retained = [e for e in edges if frozenset(e) not in cut_set]
    blocked = {v for e in cut for v in e}|{root}|set(marked)|reserved
    extra = []
    extra_count = len(cut) if paired_buffers else 5
    for a,b in retained if extra_count else ():
        low = not paired_buffers or max(len(graph[a]),len(graph[b])) < degree_bound
        if low and a not in blocked and b not in blocked:
            extra.append((a,b) if parent[b]==a else (b,a))
            blocked.update((a,b))
            if len(extra)==extra_count: break
    assert len(extra)==extra_count
    original_cuts = cut[:]
    cut.extend(extra)
    cut_set.update(frozenset(e) for e in extra)
    kept = [e for e in retained if frozenset(e) not in cut_set]
    forest = adjacency(k,kept)
    roots = {w for _,w in cut}|{root}
    fixed = set(marked)|roots|{v for v,_ in cut}
    protect = fixed|reserved
    blocked = protect.union(*(forest[v] for v in protect))
    pools = {r:[] for r in roots}
    component = {}
    for v in order:
        r = v if v in roots else component[parent[v]]
        component[v] = r
        if v not in blocked and len(graph[v])==site_degree:
            pools[r].append(v)
            blocked.update(forest[v])
    priority = sorted(roots,key=lambda v:(-len(pools[v]),v))
    matched = {}

    def place(r,visited):
        for i,e in enumerate(cut):
            if i in visited or r in e: continue
            visited.add(i)
            if i not in matched or place(matched[i],visited):
                matched[i] = r
                return True
        return False

    if paired_buffers:
        prescribed = {}
        for old,fresh in zip(original_cuts,extra):
            prescribed[old[1]] = fresh
            prescribed[fresh[1]] = old
        if priority[0] != root:
            prescribed[root] = prescribed.pop(priority[0])
    else:
        assert all(place(r,set()) for r in priority[1:])
        prescribed = {r:cut[i] for i,r in matched.items()}
    sites = {}
    available = pools[priority[0]][:]
    for r in priority[1:]:
        s = available.pop()
        sites[s] = (*prescribed[r],r)
        kept.append((s,r))
        available.extend(pools[r])
    return kept,fixed,sites

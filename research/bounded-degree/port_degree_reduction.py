"""Replace high-degree edges by a bounded-degree tree with pinned equal sums."""
from check import adjacency


def reduce_degree(edges,marked):
    k = len(edges)+1
    graph = adjacency(k,edges)
    root = next(v for v in range(k) if len(graph[v])==1)
    parent = {root:None}
    order = [root]
    cut = []
    for v in order:
        children = sorted(w for w in graph[v] if w!=parent[v])
        for w in children:
            parent[w] = v
            order.append(w)
        cut.extend((v,w) for w in children[2:])
    cut_set = {frozenset(e) for e in cut}
    retained = [e for e in edges if frozenset(e) not in cut_set]
    blocked = {v for e in cut for v in e}|{root}|set(marked)
    extra = []
    for a,b in retained:
        if a not in blocked and b not in blocked:
            extra.append((a,b) if parent[b]==a else (b,a))
            blocked.update((a,b))
            if len(extra)==5: break
    assert len(extra)==5
    cut.extend(extra)
    cut_set.update(frozenset(e) for e in extra)
    kept = [e for e in retained if frozenset(e) not in cut_set]
    forest = adjacency(k,kept)
    roots = {w for _,w in cut}|{root}
    fixed = set(marked)|roots|{v for v,_ in cut}
    blocked = fixed.union(*(forest[v] for v in fixed))
    pools = {r:[] for r in roots}
    component = {}
    for v in order:
        r = v if v in roots else component[parent[v]]
        component[v] = r
        if v not in blocked and len(graph[v])==2:
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

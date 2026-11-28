"""Complete fixed labels when a vertex cover has a common prescribed residue."""
from collections import Counter


def complete(k,n,edges,cover,color,pins):
    if not cover:
        raise ValueError("Expected a nonempty prescribed cover")
    if any(u not in cover and v not in cover for u,v in edges):
        raise ValueError("The specified set is not a vertex cover")
    degrees = Counter(v for edge in edges for v in edge)
    forced = {v:color for v in range(n) if v in cover or degrees[v]>1}
    if any(v in forced and forced[v]!=x for v,x in pins.items()):
        return None
    forced.update(pins)
    q,r = divmod(n,k)
    used = Counter(forced.values())
    high = {x for x in range(k) if used[x]>q}
    if r:
        high.add(color)
    if len(high)>r or any(c>q+1 for c in used.values()):
        return None
    high.update([x for x in range(k) if x not in high][:r-len(high)])
    remaining = iter(x for x in range(k) for _ in range(q+(x in high)-used[x]))
    return [forced[v] if v in forced else next(remaining) for v in range(n)]

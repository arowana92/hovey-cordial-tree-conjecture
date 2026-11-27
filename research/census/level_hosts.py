"""Complete an ordered rooted tree to an alpha tree in two lists of class ranks."""

from dataclasses import dataclass


@dataclass
class Labeling:
    edges: list
    side: list
    rank: list

    def labels(self):
        width = max(r for s,r in zip(self.side,self.rank) if s == 0)+1
        return [r+s*width for s,r in zip(self.side,self.rank)]


def layout(children):
    levels = [[0]]
    while next_level := [v for u in levels[-1] for v in children[u]]:
        levels.append(next_level)
    counts = [[len(children[u]) for u in level] for level in levels]
    leading = [next((j for j,c in enumerate(row) if c),len(row)) for row in counts]
    trailing = [next((j for j,c in enumerate(reversed(row)) if c),len(row)) for row in counts]
    return levels, counts, leading, trailing


def original(children):
    """The least level spacings separating the spans of successive edge lists."""
    levels,_,left,right = layout(children)
    start = [0,0]
    for i in range(len(levels)-2):
        gap = max(0,len(levels[i+1])-1-right[i]-left[i+1])
        start.append(start[i]+len(levels[i])+gap)
    side = [0]*len(children)
    rank = side.copy()
    for i,level in enumerate(levels):
        for j,u in enumerate(level):
            side[u],rank[u] = i%2,start[i]+j
    edges = [(u,v) for u,branch in enumerate(children) for v in branch]
    return Labeling(edges, side, rank)


def host(children, compress=True):
    levels,counts,leading,_ = layout(children)
    h = len(levels)-1
    if not h:
        return Labeling([], [0], [0])
    skip = leading if compress else [0]*len(levels)
    start = [0,0]
    for i in range(h-1):
        start.append(start[i]+len(levels[i])+len(levels[i+1])-1-skip[i+1])
    n = len(children)
    side,rank = [0]*n,[0]*n
    registry = [{},{}]
    def register(s,r):
        v = len(side)
        side.append(s)
        rank.append(r)
        registry[s][r] = v
        return v

    for i,level in enumerate(levels):
        for j,v in enumerate(level):
            side[v],rank[v] = i%2,start[i]+j
            registry[i%2][rank[v]] = v
    last = [max(row) for row in registry]
    targets = []
    for i in range(1,h):
        prefix = 0
        t = len(levels[i])
        for j,c in enumerate(counts[i]):
            if j>skip[i]:
                v = register(1-i%2,start[i+1]-t+j)
                targets.append((v,i%2,start[i]+t-1+prefix))
            prefix += c
    high = last[:]
    for _,s,r in targets:
        high[s] = max(high[s],r)
    edges = [(u,v) for u,branch in enumerate(children) for v in branch]
    # Complete the upper intervals in this order. Their sums immediately
    # follow all the transition intervals, even when both tails are nonempty.
    for s in range(2):
        neighbor = registry[1-s][last[1] if s==0 else high[0]]
        for r in range(last[s]+1,high[s]+1):
            edges.append((register(s,r),neighbor))
    edges.extend((v,registry[s][r]) for v,s,r in targets)
    return Labeling(edges,side,rank)

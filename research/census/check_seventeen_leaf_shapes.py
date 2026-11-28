"""Check the heavy-edge geometry and the two terminal-tail cuts on actual trees."""
from collections import Counter
from random import Random


def inspect(graph):
    leaves = {v for v,adj in graph.items() if len(adj)==1}
    assert len(leaves)==17
    def side(first, blocked):
        seen = {first,blocked}
        queue = [first]
        for u in queue:
            for v in graph[u]-seen:
                queue.append(v)
                seen.add(v)
        return set(queue)
    heavy = {tuple(sorted((u,v))) for u,adj in graph.items() for v in adj if u<v
             and len(side(v,u)&leaves) in (8,9)}
    if not heavy:
        assert any(all(len(side(v,u)&leaves)<=7 for v in adj) for u,adj in graph.items())
        return 'central',0
    ends = Counter(v for edge in heavy for v in edge)
    path = [v for v,count in ends.items() if count==1]
    assert len(path)==2 and max(ends.values())<=2
    start,end = path
    ordered = [start]
    used = {start}
    while ordered[-1]!=end:
        v = ordered[-1]
        w, = (u for u in graph[v]-used if tuple(sorted((u,v))) in heavy)
        ordered.append(w)
        used.add(w)
    assert len(ordered)==len(heavy)+1
    left,right = side(start,ordered[1]),side(end,ordered[-2])
    spurs = [(i,graph[v]-used) for i,v in enumerate(ordered[1:-1],1) if graph[v]-used]
    if not spurs:
        assert sorted([len(left&leaves),len(right&leaves)])==[8,9]
        return '8/9',0
    (i,external), = spurs
    root, = external
    arm = side(root,ordered[i])
    assert len(arm&leaves)==1 and all(len(graph[v])<=2 for v in arm)
    assert len(left&leaves)==len(right&leaves)==8

    pieces = []
    for outer,corridor in ((left,ordered[:i]),(right,ordered[:i:-1])):
        a = len(outer)-1
        length = max(1,a-26)
        use = max(0,27-a)
        if use>len(corridor)-1:
            return '8/8 with arm',0
        for leaf in outer&leaves:
            tail = [leaf]
            while len(tail)<length:
                nxt = graph[tail[-1]]-set(tail)
                v, = nxt
                if v==corridor[0] or len(graph[v])!=2:
                    break
                tail.append(v)
            if len(tail)==length:
                piece = (outer-set(tail)) | set(corridor[1:use+1])
                assert len(piece)==27
                pieces.append(piece)
                break
        else:
            return '8/8 with arm',0
    assert pieces[0].isdisjoint(pieces[1])
    small = {v:adj.copy() for v,adj in graph.items()}
    for piece in pieces:
        start = next(iter(piece))
        queue = [start]
        seen = {start}
        for u in queue:
            for v in (small[u]&piece)-seen:
                seen.add(v)
                queue.append(v)
        assert seen==piece
        ports = [v for x in piece for v in small[x]-piece]
        u,v = ports
        assert u!=v and v not in small[u]
        for x in piece:
            del small[x]
        small[u].difference_update(piece)
        small[v].difference_update(piece)
        small[u].add(v)
        small[v].add(u)
    assert len(small)==len(graph)-54 and sum(len(s)==1 for s in small.values())==3
    return '8/8 with arm',1


def fixtures():
    rng = Random(170027)
    for trial in range(900):
        graph = {0:set()}
        def child(p):
            v = len(graph)
            graph[v] = {p}
            graph[p].add(v)
            return v
        def arm(p,n):
            for _ in range(n):
                p = child(p)
            return p
        if trial%3==0:
            for _ in range(17):
                arm(0,rng.randint(1,4))
        elif trial%3==1:
            for _ in range(8):
                arm(0,rng.randint(2,5))
            middle = arm(0,rng.randint(1,10))
            other = arm(middle,rng.randint(1,10))
            arm(middle,rng.randint(1,10))
            for _ in range(8):
                arm(other,rng.randint(2,5))
        else:
            for _ in range(3):
                child(0)
            for _ in range(14):
                v = rng.choice([u for u in graph if len(graph[u])==1])
                child(v)
                arm(v,rng.randint(1,7))
        yield graph


if __name__=='__main__':
    counts = Counter()
    compressions = 0
    for graph in fixtures():
        shape,done = inspect(graph)
        counts[shape] += 1
        compressions += done
    assert len(counts)==3 and compressions
    print('shape checks',dict(counts),'two connected pieces compressed',compressions)

"""Replay entire labeled trees and independently enumerate the rooted pin projections."""
from itertools import combinations
from random import Random

from research.census.few_leaf_rings import trees as rooted_trees
from .check_bridge_pins import cordial, short_distances
from .separated_pins import label


def rooted_projections(k):
    projections = [set(range(1,k)) for _ in range(k)]
    triples = set(combinations(range(1,k),2))
    count = 0
    for tips in range(1,k):
        for word in rooted_trees(k,tips):
            parent,depth,stack = [],[],[]
            for c in word:
                if c == '(':
                    parent.append(stack[-1] if stack else -1)
                    depth.append(len(stack))
                    stack.append(len(parent)-1)
                else:
                    stack.pop()
            assert len(parent) == k
            children = [i for i in range(1,k) if parent[i] == 0]
            neighbors = list(combinations(children,2))
            available = [set() for _ in range(k)]
            pairs = [set() for _ in neighbors]
            row = [0]*k

            def visit(v,vertices,sums):
                if v == k:
                    for i in range(1,k):
                        available[i].add(row[i])
                    for seen,(u,w) in zip(pairs,neighbors):
                        seen.add((row[u],row[w]))
                    return
                for x in range(1,k):
                    s = (x+row[parent[v]])%k
                    if x not in vertices and s not in sums:
                        row[v] = x
                        visit(v+1,vertices|{x},sums|{s})

            visit(1,{0},set())
            for i in range(1,k):
                projections[depth[i]] &= available[i]
            for seen in pairs:
                triples = {(a,b) for a,b in triples if (a,b) in seen and (b,a) in seen}
            count += 1
    assert projections[1:] == short_distances(k) and not triples
    assert count == {8:115, 9:286}[k]
    return count


def arm(graph, start, length):
    v = start
    for _ in range(length):
        u = len(graph)
        graph[v].add(u)
        graph[u] = {v}
        v = u
    return v


def whole_trees(k):
    rng = Random(7819+k)
    total = vertices = rejected = 0

    def check(graph,pins,possible=True):
        nonlocal total,vertices,rejected
        try:
            labels = label(k,graph,pins)
        except ValueError as exc:
            assert not possible and 'parity' in str(exc), (k,len(graph),pins,exc)
            rejected += 1
            return
        assert possible and labels.keys() == graph.keys()
        assert all(labels[v] == x for v,x in pins.items())
        edges = [(v,u) for v in graph for u in graph[v] if v < u]
        assert len(edges) == len(graph)-1
        assert cordial(k,[labels[v] for v in range(len(graph))],edges), (k,len(graph),pins)
        total += 1
        vertices += len(graph)

    limit = 2*k*k-k+1
    for d in range(limit,limit+k):
        for extra in (0,1,k-2,k-1,k+4):
            graph = {0:set()}
            end = arm(graph,0,d)
            for _ in range(extra):
                arm(graph,rng.randrange(len(graph)),1)
            x,y = rng.randrange(k),rng.randrange(k)
            allowed = not (k==8 and not extra and (d%8)==0 and (x-y)%2)
            check(graph,{0:x,end:y},allowed)

    # Pin a branching vertex as well as every leaf, including a uniform-edge order.
    for limbs in (3,4,6,9):
        for change in (0,1,2):
            graph = {0:set()}
            lengths = [2*limit-1+rng.randrange(k) for _ in range(limbs)]
            lengths[-1] += (-sum(lengths))%k
            ends = [arm(graph,0,w) for w in lengths]
            pins = {v:rng.randrange(k) for v in [0]+ends}
            odd_sum = sum(pins[v] for v in pins if len(graph[v])%2)
            if change:
                arm(graph,0,change)  # Leaves at small distances can stay unpinned.
            check(graph,pins,k==9 or change or odd_sum%2 == 0)

    # Short segments between adjacent joints can coexist with remote pinned leaves.
    for count in (3,7,12):
        graph = {0:set()}
        joints = [0]
        for j in range(1,count):
            joints.append(arm(graph,joints[rng.randrange(j)],1))
        ends = [arm(graph,v,limit+2) for v in joints for _ in range(2)]
        arm(graph,joints[0],3)
        check(graph,{v:rng.randrange(k) for v in ends})
    return total,vertices,rejected


if __name__ == '__main__':
    for k in (8,9):
        print(f"{rooted_projections(k)} rooted bases at {k}",flush=True)
        accepted,vertices,rejected = whole_trees(k)
        print(f"{accepted} complete trees, {vertices} vertices, {rejected} parity obstructions",flush=True)

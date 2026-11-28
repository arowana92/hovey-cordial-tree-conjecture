"""Check the terminal-arm bound on DFS intervals, and recount 27-cordial prefixes."""
from collections import Counter
from itertools import accumulate
from random import Random
import sys

from research.rainbow.check_two_rooted_trees import replay
from research.rainbow.prescribed_forest_order import extend
from research.rainbow.two_rooted_trees import padded_search


def arm_tree(base, lengths):
    adj = [[] for _ in base]
    for v,p in enumerate(base[1:],1):
        adj[p].append(v)
        adj[v].append(p)
    leaves = [i for i,row in enumerate(adj) if len(row)==1]
    for v,length in zip(leaves,lengths):
        # Make the last length vertices a pendant path.
        for _ in range(length-1):
            adj.append([v])
            w = len(adj)-1
            adj[v].append(w)
            v = w
    return adj


def preorder(adj,start,rng):
    # Return the tree numbered in the chosen preorder.
    stack,ids,parents = [(start,-1)],{},[]
    while stack:
        v,p = stack.pop()
        ids[v] = len(parents)
        parents.append(-1 if p<0 else ids[p])
        children = [w for w in adj[v] if w!=p]
        if rng is not None:
            rng.shuffle(children)
        stack.extend((w,v) for w in reversed(children))
    return parents


def check_intervals(parents):
    intervals = extreme = 0
    for i in range(1,len(parents)):
        kids = Counter()
        for j in range(i,min(i+26,len(parents))):
            if parents[j]>=i:
                kids[parents[j]] += 1
            tips = j-i+1-len(kids)
            if tips>5:
                assert tips==6 and j-i+1==26 and max(kids.values())==1
                extreme += 1
            intervals += 1
    return intervals,extreme


def plane_orders(n):
    # In preorder, the depth of each nonroot vertex ranges from one to
    # one more than the preceding depth. Its parent is fixed by its depth.
    def visit(parents, ancestors):
        if len(parents) == n:
            yield parents
            return
        for depth, parent in enumerate(ancestors, 1):
            yield from visit(parents+[parent], ancestors[:depth]+[len(parents)])
    yield from visit([-1], [0])


def original_arms(parents):
    adj = [[] for _ in parents]
    for v,p in enumerate(parents[1:], 1):
        adj[v].append(p)
        adj[p].append(v)
    if all(len(row) < 3 for row in adj):
        return {}
    arms = {}
    for leaf,row in enumerate(adj):
        if len(row) != 1:
            continue
        path = [leaf]
        v, = row
        while len(adj[v]) == 2:
            w = next(w for w in adj[v] if w != path[-1])
            path.append(v)
            v = w
        arms[leaf] = set(path)
    return arms


def exhaustive_geometry():
    orders = checked = equality = 0
    for n in range(1, 11):
        for parents in plane_orders(n):
            orders += 1
            arms = original_arms(parents)
            if not arms:
                continue
            shortest = [0, *accumulate(sorted(map(len, arms.values())))]
            for i in range(1, n):
                for j in range(i+1, n):
                    batch = set(range(i,j+1))
                    tips = sorted(batch-set(parents[i:j+1]))
                    if len(tips) < 2:
                        continue
                    checked += 1
                    roots = sum(parents[v] not in batch for v in batch)
                    children = Counter(parents[v] for v in batch if parents[v] in batch)
                    assert roots+sum(max(0,d-1) for d in children.values()) == len(tips)
                    for v in tips[1:-1]:
                        assert arms[v] <= batch-{tips[0],tips[-1]}
                    bound = 2+shortest[len(tips)-2]
                    assert len(batch) >= bound
                    if len(batch) == bound:
                        # In equality each tip is in its own path component.
                        assert roots == len(tips)
                        equality += 1
    print('plane rooted orders', orders, 'intervals with multiple tips', checked,
          'exact bounds attained', equality)


def main(library):
    exhaustive_geometry()
    rng = Random(271991)
    witness = padded_search(library,27)
    examples = [(arm_tree([-1]+[0]*6,[28,6,6,6,6,12]),0,None)]
    for trial in range(40):
        base = [-1]+[rng.randrange(i) for i in range(1,rng.randrange(18,45))]
        leaves = [v for v in range(len(base)) if base.count(v)+int(v!=0)==1]
        values = sorted(rng.randint(6,12) for _ in leaves)
        if len(values)>=4 and trial%2:
            values[0] = 1
            values[1:] = [max(8,x) for x in values[1:]]
        rng.shuffle(values)
        adj = arm_tree(base,values)
        tip = next(v for v,row in enumerate(adj) if len(row)==1)
        for start in (tip,adj[tip][0],rng.randrange(len(adj))):
            examples.append((adj,start,rng))
    intervals = extreme = prefixes = 0
    offset_rng = Random(271992)
    offset_runs = offset_prefixes = 0
    for trial,(adj,start,shuffle) in enumerate(examples):
        parents = preorder(adj,start,shuffle)
        n,critical = check_intervals(parents)
        intervals += n
        extreme += critical
        order = list(range(1,len(parents)))
        labels = extend(parents,[11],order,27,witness)
        prefixes += replay(parents,[11],labels,order,{})
        if trial%3 == 0:
            offsets = {}
            pos = 1
            while pos < len(parents):
                stop = min(len(parents),pos+(1 if pos%27 == 0 else 26))
                for v in range(pos,stop):
                    if parents[v] < pos:
                        offsets[v] = offset_rng.randrange(27)
                pos = stop
            adjusted = extend(parents,[11],order,27,witness,offsets)
            offset_prefixes += replay(parents,[11],adjusted,order,offsets)
            offset_runs += 1
    assert extreme
    print('DFS orders',len(examples),'intervals',intervals,
          'six-tip equality cases',extreme,'cordial prefixes',prefixes)
    print('offset orders',offset_runs,'adjusted cordial prefixes',offset_prefixes)


if __name__=='__main__':
    main(sys.argv[1])

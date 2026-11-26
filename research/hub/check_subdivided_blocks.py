"""Check consecutive blocks, cuts below exceptional vertices, and actual boundary weights."""

from collections import Counter
from itertools import permutations
from random import Random

from research.hub.check_common_boundary import witness
from research.rainbow.verify import rooted_shapes


def traversal(tree, d):
    sizes = [1] * len(tree)
    children = [[] for _ in tree]
    for v in range(len(tree)-1, 0, -1):
        sizes[tree[v]] += sizes[v]
        children[tree[v]].append(v)
    high = {v for v,row in enumerate(children) if len(row) + int(v != 0) > d}
    neighborhood = high.copy()
    for _ in range(2):
        neighborhood |= {tree[v] for v in neighborhood if v} | {
            w for v in neighborhood for w in children[v]}
    near = {v for v in neighborhood if len(children[v]) + int(v != 0) == 1}
    stack, order = [0], []
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(sorted(children[v], key=lambda w: (sizes[w],w), reverse=True))
    return order, high, near


def check_block(tree, order, high, near, start, b, k, d):
    seq = order[start:start+b]
    assert len(seq) == b and start > 0
    part = set(seq)
    external = {tree[v] for v in part if tree[v] not in part}
    assert len(external) <= 2 or (1 << (len(external)-2)) <= k+1
    boundary = {v for v in seq if tree[v] not in part or tree[v] in high}
    owners, groups = {}, {}
    for v in seq:
        root = v if v in boundary else owners[tree[v]]
        owners[v] = root
        groups.setdefault(root, []).append(v)
    deep = {(tree[v],v) for v in seq if v not in boundary and tree[v] not in boundary}
    bad = 0
    pos = {v:i for i,v in enumerate(seq)}
    charged = set()
    for root,group in groups.items():
        internal = sum((tree[v],v) in deep for v in group)
        if tree[root] not in high or pos[root]+2 >= b:
            bad += 1
        else:
            a = pos[root]
            first = root if root in high or root in near else seq[a+1]
            if first in high or first in near:
                assert first in group and first not in charged
                charged.add(first)
                bad += 1
            else:
                x,y = seq[a+1:a+3]
                assert tree[x] == root and tree[y] == x and (x,y) in deep
                assert internal * (d+1) >= len(group)
        assert internal >= len(group)-d
    assert bad <= len(high & part) + len(near & part) + 2 + d * len(external)
    assert (len(deep) + bad*d) * (d+1) >= b
    # Append the terminal path to the last visited vertex, an actual terminal of the block.
    parents = {v:tree[v] for v in seq}
    assert seq[-1] not in parents.values()
    p = seq[-1]
    for v in range(len(tree), len(tree) + k-1-b):
        parents[v] = p
        p = v
    roots = {v for v,p in parents.items() if p not in parents or p in high}
    padded = sum(v not in roots and p not in roots for v,p in parents.items())
    assert len(parents) == k-1 and padded >= len(deep) + k-1-b-2
    return len(external), len(groups), len(deep), len(charged)


def pendant_subdivision(tree, length, rng):
    leaves = set(range(1,len(tree))) - set(tree[1:])
    if tree[1:].count(0) == 1:
        leaves.add(0)
    out, endpoint = [-1], {0:0}
    for v in range(1,len(tree)):
        p = endpoint[tree[v]]
        for _ in range(length + rng.randrange(3) if v in leaves or tree[v] in leaves else 0):
            out.append(p)
            p = len(out)-1
        out.append(p)
        endpoint[v] = len(out)-1
    return out


def blocks():
    nchecks = multihigh = highcuts = max_boundary = max_components = 0
    charges = Counter()
    d = 3
    rng = Random(65714)
    for n in range(4,10):
        for tree in rooted_shapes(n).values():
            state = traversal(tree, d)
            for start in range(1,n):
                for b in range(1,n-start+1):
                    a,c,_,bad = check_block(tree,*state,start,b,b+1+start%3,d)
                    max_boundary = max(max_boundary,a)
                    max_components = max(max_components,c)
                    charges['charged'] += bad
                    nchecks += 1
    # Adjacent high vertices, ternary branching, long paths, and random recursive trees.
    for size in (51,253,1500):
        for mode in range(4):
            tree = [-1]+[([max(0,v//31-1),(v-1)//3,v-1,rng.randrange(v)][mode])
                         for v in range(1,size)]
            for length in (-1,2,7):
                actual = tree if length < 0 else pendant_subdivision(tree,length,rng)
                state = traversal(actual,d)
                if length >= 2 and len(actual) > 1:
                    assert not state[2]
                for k in (11,63,127,263):
                    for start in range(1,len(actual),k):
                        b = min(k-1,len(actual)-start)
                        a,c,_,bad = check_block(actual,*state,start,b,k,d)
                        nchecks += 1
                        local_high = state[1].intersection(state[0][start:start+b])
                        multihigh += len(local_high) >= 2
                        highcuts += sum(actual[v] in local_high for v in state[0][start:start+b])
                        charges['charged'] += bad
                        max_boundary = max(max_boundary,a)
                        max_components = max(max_components,c)
    assert multihigh and highcuts and charges['charged'] and max_boundary >= 3
    return nchecks,multihigh,highcuts,max_boundary,max_components


def forest_examples():
    checked = multi = composite = 0
    for k in range(11,17):
        tree = [-1,0,0,1,1,2,5,3,7,-1] + [-1]*(k-11)
        cut = {0,1}
        for left,right in ((0,3),(2,5),(3,1)):
            boundary = [0]*len(tree)
            boundary[0],boundary[9] = left,right
            for u in (0,1,k//2):
                pool = set(range(k)) - {u,0,left,right}
                solutions = (witness(tree,boundary,k,u,{0:a,1:b})
                             for a,b in permutations(sorted(pool),2))
                labels = next((row for row in solutions if row is not None),None)
                assert labels is not None, (k,left,right,u)
                roots = {v for v,p in enumerate(tree) if p < 0 or p in cut}
                ext = {v:boundary[v] if tree[v] < 0 else labels[tree[v]] for v in roots}
                direct = [(x + (boundary[v] if p < 0 else labels[p])) % k
                          for v,(x,p) in enumerate(zip(labels,tree))]
                rebuilt = [((ext[v] if v in roots else labels[tree[v]]) + x) % k
                           for v,x in enumerate(labels)]
                assert set(labels) == set(range(k))-{u}
                assert direct == rebuilt and len(set(rebuilt)) == k-1
                assert sum(p not in roots and v not in roots for v,p in enumerate(tree)) >= 2
                assert len(set(ext.values())) >= 4
                # Quota slots belong to a particular shift even with internal children.
                assigned = {p:{labels[v] for v in roots if ext[v] == p}
                            for p in set(ext.values())}
                used = {((x+p) % k) for p,xs in assigned.items() for x in xs}
                assert len(used) == len(roots) and used == {direct[v] for v in roots}
                multi += len([v for v in roots if v in tree]) >= 3
                composite += any(k%i==0 for i in range(2,int(k**0.5)+1))
                checked += 1
    return checked,multi,composite


if __name__ == '__main__':
    n,m,c,b,r = blocks()
    print(f"{n:,} blocks checked, {m:,} with multiple high vertices and {c:,} child edges "
          f"at high vertices; maxima {b} boundary parents and {r} cut components.")
    n,m,c = forest_examples()
    print(f"{n} exact multi-shift forest searches, {m} with at least three nonterminal roots, "
          f"{c} over composite moduli; all cut weights reconstructed.")

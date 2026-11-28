"""Classify prescribed connected orders of fewer than three periods at eight and nine."""
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement, permutations, product

from research.eight.surplus import mask_solver
from research.eight.verify import components
from research.rainbow.check_terminal_arm_order import plane_orders
from research.rainbow.verify import rooted_shapes
from research.eight.check_two_period_depth_first import example
from research.eight.check_dfs_obstructions import cordial


def exceptions(k):
    # The published packet classification excludes forests with two internal
    # vertices and all-singleton forests. Recompute every one-center case.
    solve = mask_solver(k-1,k)
    bad = set()
    for h in range(1,k-1):
        for s in combinations_with_replacement(range(k),k-2-h):
            for a in range(k):
                parents = [-1-a]+[0]*h+[-1-x for x in s]
                if solve(parents) is None:
                    bad.add((h,s,a))
    return bad


def inverse(colors,bad):
    k = len(colors)-1
    sites = [[i for i,x in enumerate(colors) if x==c] for c in range(k)]
    return {(h,tuple(sorted(s)),a) for h,cs,c in bad
            for s in product(*(sites[x] for x in cs)) for a in sites[c]}


def identify(parents,root,placement):
    # An isomorphism may permute equal child branches. The forced step and all
    # final attachment sites must be preserved, including multiplicities.
    k = len(parents)
    h,s,a = placement
    singles = Counter(s)
    adj = [[] for _ in parents]
    for v,p in enumerate(parents[1:],1):
        adj[v].append(p)
        adj[p].append(v)
    def visit(v,p):
        return (v==a,singles[v],tuple(sorted(visit(w,v) for w in adj[v] if w!=p)))
    return h,a==k,singles[k],visit(root,-1)


def catalog(k):
    bad = exceptions(k)
    shapes = rooted_shapes(k)
    assert shapes.keys() == {components(ps)[0][1] for ps in plane_orders(k)}
    all_colors = set(range(k))
    result = set()
    bad_bases = raw = rows = 0
    for ps in shapes.values():
        survivors = None
        for suffix in permutations(range(1,k)):
            word = (0,)+suffix
            weights = {(word[i]+word[ps[i]])%k for i in range(1,k)}
            if len(weights) != k-1:
                continue
            gap, = all_colors-weights
            # The forced vertex is attached at the distinguished old root zero.
            colors = [(x-gap)%k for x in word]+[0]
            if survivors is None:
                survivors = inverse(colors,bad)
            else:
                survivors = {(h,s,a) for h,s,a in survivors
                             if (h,tuple(sorted(colors[v] for v in s)),colors[a]) in bad}
            rows += 1
            if not survivors:
                break
        assert survivors is not None
        if survivors:
            bad_bases += 1
            raw += len(survivors)
            result.update(identify(ps,0,placement) for placement in survivors)
    print('modulus, packet exceptions, rooted bases, bases with failures, raw placements, types, rows',
          k,len(bad),len(shapes),bad_bases,raw,len(result),rows)
    return result


def obstructed(k,parents,table):
    """Input vertices must already be numbered in the prescribed growth order."""
    if k not in (8,9) or not 1 <= len(parents) < 3*k:
        raise ValueError('expected a nonempty order shorter than three periods at eight or nine')
    if parents[0]!=-1 or any(not 0<=p<v for v,p in enumerate(parents[1:],1)):
        raise ValueError('expected an ordered tree with parent-first indices')
    if len(parents)<2*k:
        return False
    new = range(k+1,2*k)
    internal = Counter(parents[v] for v in new if parents[v]>k)
    if len(internal)!=1:
        return False
    (center,h), = internal.items()
    s = tuple(sorted(parents[v] for v in new if v!=center and parents[v]<=k))
    return identify(parents[:k],parents[k],(h,s,parents[center])) in table


def materialize(key):
    h,center_new,extra,marked = key
    parents,singles = [],[]
    center_site = None
    def visit(tree,p):
        nonlocal center_site
        is_center,count,children = tree
        v = len(parents)
        parents.append(p)
        singles.extend([v]*count)
        if is_center:
            center_site = v
        for child in children:
            visit(child,v)
    visit(marked,-1)
    k = len(parents)
    parents.append(0)
    center = len(parents)
    site = k if center_new else center_site
    parents.extend([site]+[center]*h+singles+[k]*extra)
    assert site is not None and len(parents)==2*k
    return parents


def replay_catalog(k,table):
    solve = mask_solver(k-1,k)
    @lru_cache(None)
    def base(parents):
        out = []
        for tail in permutations(range(1,k)):
            word = (0,)+tail
            weights = {(word[i]+word[p])%k for i,p in enumerate(parents) if i}
            if len(weights) == k-1:
                gap, = set(range(k))-weights
                out.append(word+((gap-word[0])%k,))
        return out

    def literal(parents):
        # In these materialized examples the forced vertex attaches to old zero.
        assert parents[k] == 0
        for old in base(tuple(parents[:k])):
            x = old[-1]
            links = tuple(p-k-1 if p>k else -1-(old[p]-x)%k for p in parents[k+1:])
            row = solve(links)
            if row is not None:
                labels = list(old)+[(v+x)%k for v in row]
                assert all(cordial(k,parents,labels[:j]) for j in range(1,2*k+1))
                return True
        return False

    for key in table:
        parents = materialize(key)
        assert obstructed(k,parents,table) and not literal(parents)
        # Move one singleton below a child of the star to produce a second
        # internal vertex. Each accepted labeling is replayed on the new tree.
        parents[-1] = k+2
        assert not obstructed(k,parents,table) and literal(parents)
    print('complete failed orders and adjacent successful examples replayed',k,len(table),len(table))


if __name__ == '__main__':
    for k,p in [(8,2),(9,3)]:
        table = catalog(k)
        tree,_,_ = example(k,p,k//p)
        assert obstructed(k,tree,table)
        assert not obstructed(k,tree[:-1],table)
        assert obstructed(k,tree+[0]*(k-1),table)
        assert not obstructed(k,[-1]+list(range(3*k-2)),table)
        replay_catalog(k,table)

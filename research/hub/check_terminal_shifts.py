"""Finite tests for shift quotas, nested reservoirs and terminal matchings."""

from collections import Counter
from fractions import Fraction
from itertools import permutations
from random import Random

from research.hub.check_subdivided_blocks import traversal
from research.hub.neutral_star_blocks import star_block
from research.rainbow.verify import rooted_shapes


def nested_laws():
    checks = 0
    for k in (199,512,1021):
        for r in (1,2,3):
            v = Fraction(1,2)
            p = Fraction(r,k)
            for common in (True,False):
                roles = dict.fromkeys(('X0','X1','Y0','Y1','Z0','Z1'),p)
                if not common:
                    roles['W'] = 2*p
                    roles['J'] = Fraction(1,30)
                outcomes = Counter()
                for a in (False,True):
                    for c in (False,True):
                        mass = (v if a else 1-v)*(v if c else 1-v)
                        if a and c:
                            outcomes.update({(a,c,i):q for i,q in roles.items()})
                            mass -= sum(roles.values())
                        outcomes[a,c,None] += mass
                assert min(outcomes.values()) >= 0 and sum(outcomes.values()) == 1
                ypr = zpr = 0
                for (a,c,i),q in outcomes.items():
                    x = i in ('X0','X1')
                    y = i in ('Y0','Y1')
                    z = i in ('Z0','Z1')
                    w = x if common else i == 'W'
                    if a and not x and not y:
                        ypr += q
                    if c and not w and not z:
                        zpr += q
                assert ypr == zpr == v-4*p
                checks += 1
    return checks


def distinct_fallback(sources, choices):
    owner = {}

    def augment(x, seen):
        for y in choices[x]:
            if y in seen:
                continue
            seen.add(y)
            if y not in owner or augment(owner[y],seen):
                owner[y] = x
                return True
        return False

    for x in sorted(sources,key=lambda u:len(choices[u])):
        assert augment(x,set())
    return {x:y for y,x in owner.items()}


def allocations(rng):
    total = fallback = checked_triples = 0
    for k in (1021,1536,2503,4096):
        for _ in range(10):
            all_values = list(range(k))
            rng.shuffle(all_values)
            s = k//10
            xset = set(all_values[:s])
            wanted = set(all_values[s:2*s])
            spare = set(all_values[2*s:2*s+k//2])
            shifts = rng.sample(range(1,k),max(40,k//30))
            quota = {p:s//len(shifts)+(i<s%len(shifts)) for i,p in enumerate(shifts)}
            arcs = []
            pairs = [set(),set(),set()]
            for x in xset:
                for p in shifts:
                    y = (x+p)%k
                    if y in wanted:
                        clone = (p,rng.randrange(quota[p]))
                        triple = (x,y,clone)
                        for i,key in enumerate(((x,y),(x,clone),(y,clone))):
                            assert key not in pairs[i]
                            pairs[i].add(key)
                        arcs.append(triple)
            checked_triples += len(arcs)
            rng.shuffle(arcs)
            landing,used,clones = {},set(),set()
            for x,y,c in arcs:
                if x not in landing and y not in used and c not in clones:
                    landing[x] = y
                    used.add(y)
                    clones.add(c)
            assert set(landing.values())<=wanted
            count = Counter((y-x)%k for x,y in landing.items())
            assert all(count[p]<=quota[p] for p in shifts)
            missed = xset-landing.keys()
            missing_targets = wanted-used
            assert len(missed) == len(missing_targets)
            groups = [shifts[j::max(1,len(shifts)//20)] for j in range(max(1,len(shifts)//20))]
            choices = {}
            group_users = Counter()
            for x in xset:
                g = rng.randrange(len(groups))
                group_users[g] += 1
                choices[x] = [(x+p)%k for p in groups[g] if (x+p)%k in spare]
            extra = distinct_fallback(missed,choices)
            landing.update(extra)
            assert set(landing) == xset and len(set(landing.values())) == s
            final = Counter((y-x)%k for x,y in landing.items())
            for i,group in enumerate(groups):
                for p in group:
                    assert final[p] <= quota[p]+group_users[i]
            assert sum(abs(final[p]-quota[p]) for p in shifts) <= 2*len(missed)
            assert len(set(landing.values()) ^ wanted) == 2*len(missed)
            total += 1
            fallback += len(extra)
    return total,fallback,checked_triples


def complete_layer(k, parents, labels, colors):
    for assigned in permutations(labels):
        if {(x+y)%k for x,y in zip(parents,assigned)} == colors:
            return assigned
    raise AssertionError("no terminal matching")


def actual_forests(rng):
    count = stages = 0
    for k in (127,256,341,503):
        for rep in range(10):
            u = rng.randrange(k)
            occupied = {u}
            forest = []
            for shift,d in ((1,1),(3+rep,2),(k//2,1)):
                for root,leaves in star_block(k,shift,d,occupied):
                    forest.append((shift,root,leaves))
                    occupied.update([root,*leaves])
            forest.extend((0,x,[]) for x in range(k) if x not in occupied)
            labels = [x for _,a,row in forest for x in [a,*row]]
            edges = [w for b,a,row in forest for w in [(b+a)%k,*[(a+x)%k for x in row]]]
            assert set(labels) == set(range(k))-{u} and len(labels)==k-1==len(set(edges))
            orig_gap, = set(range(k))-set(edges)
            ids = [i for i,(_,_,row) in enumerate(forest) if row]
            rng.shuffle(ids)
            marked = ids[:10]
            b,z,adj = forest[ids[-1]]
            neighbors = [b,*adj]
            assert len(set(neighbors)) == len(neighbors)
            X = [forest[i][1] for i in marked]
            Y = [forest[i][2][0] for i in marked]
            Z = [(x+y)%k for x,y in zip(X,Y)]
            V = set(Y)|{z}
            C = set(Z)|{orig_gap}|{(z+a)%k for a in neighbors}
            gap = (sum(C)-sum(V)-sum(X)-sum(neighbors)-(len(neighbors)-1)*z)%k
            assert gap == orig_gap
            open_v, open_c = set(Y),set(Z)
            start = 0
            for size in (5,3,2):
                stop = start+size
                xs = X[start:stop]
                ys = sorted(Y[start:stop],reverse=True)
                cs = set(Z[start:stop])
                actual = complete_layer(k,xs,ys,cs)
                assert cs <= open_c and set(actual) <= open_v
                for j,label in enumerate(actual,start):
                    forest[marked[j]][2][0] = label
                open_c -= cs
                open_v -= set(actual)
                assert (sum(open_c)-sum(open_v)-sum(X[stop:]))%k == 0
                start = stop
                stages += 1
            edges2 = [w for b,a,row in forest for w in [(b+a)%k,*[(a+x)%k for x in row]]]
            labels2 = [x for _,a,row in forest for x in [a,*row]]
            assert sorted(edges2) == sorted(edges) and sorted(labels2) == sorted(labels)
            count += 1
    return count,stages


def strip_pendant_edges_once(tree):
    degree = Counter(tree[1:]) + Counter(range(1,len(tree)))
    out = [-1]
    endpoint = {0:0}
    for v in range(1,len(tree)):
        p = endpoint[tree[v]]
        if min(degree[v],degree[tree[v]]) == 1:
            out.append(p)
            p = len(out)-1
        out.append(p)
        endpoint[v] = len(out)-1
    return out


def block_checks():
    count = only_shallow = 0
    def run(tree, full):
        nonlocal count,only_shallow
        d = 3
        order,high,_ = traversal(tree,d)
        degree = Counter(tree[1:]) + Counter(range(1,len(tree)))
        direct = {v for v,p in enumerate(tree) if v and degree[v] == 1 and p in high}
        if degree[0] == 1 and any(tree[v] == 0 for v in high):
            direct.add(0)
        sizes = range(2,len(tree)+1) if full else (17,64,155,511)
        for k in sizes:
            starts = range(1,len(tree)) if full else range(1,len(tree),k)
            for j in starts:
                seq = order[j:j+k-1]
                take = set(seq)
                ext = {tree[v] for v in seq if tree[v] not in take}
                roots = {v for v in seq if tree[v] in high or tree[v] not in take}
                parents = {tree[v] for v in seq if v not in roots}
                singleton = roots-parents
                assert all(v in high or v in direct or tree[v] in ext-high or v == seq[-1]
                           for v in singleton)
                assert len(singleton) <= len(high & take)+len(direct & take)+d*len(ext)+1
                internal = len(take)-len(roots)
                assert 2*internal >= len(take)-len(singleton)
                deep = sum(v not in roots and tree[v] not in roots for v in seq)
                if internal >= (len(take)+1)//2 and deep == 0 and len(take)>=8:
                    only_shallow += 1
                count += 1
    for n in range(3,9):
        for tree in rooted_shapes(n).values():
            run(tree,True)
    for size in (137,1048,2281):
        for mode in range(3):
            tree = [-1]+[([0,(v-1)//19,max(0,(v-1)//2-4)][mode]) for v in range(1,size)]
            run(tree,False)
            run(strip_pendant_edges_once(tree),False)
    assert only_shallow > 0
    return count,only_shallow


if __name__ == '__main__':
    rng = Random(918033)
    print(f"{nested_laws()} exact nested categorical laws.")
    n,f,t = allocations(rng)
    print(f"{n} cloned-quota packings, {t:,} linear triples checked, {f:,} fallback assignments.")
    n,m = actual_forests(rng)
    print(f"{n} full prescribed forests, {m} exact matching stages with actual weights and gap.")
    n,z = block_checks()
    print(f"{n:,} preorder blocks, {z} with at least half internal edges and no deep edge.")

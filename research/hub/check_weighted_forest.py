"""Audit the exact vector split, weighted forest and delayed actual terminal edges."""

from collections import Counter
from random import Random

from research.hub.check_endpoint_windows import audit
from research.hub.decorated_spine import expand_edge
from research.hub.endpoint_hub import support_first
from research.hub.integer_layers import offsets_for_level, first_choice, guard_points
from research.hub.integer_windows import restore
from research.hub.weighted_forest import partition, prepare


def vectors(rng):
    cases = 0
    for n in (1, 3, 9, 27):
        for r in range(1, 5):
            for mode in range(6):
                rows = [[rng.randrange(9) for _ in range(r)] for _ in range(n)]
                if mode == 0:
                    rows = [[0]*r for _ in rows]
                elif mode == 1:
                    rows = [[a[0]*i for i in range(1, r+1)] for a in rows]
                elif mode == 2:
                    rows = [[a[0]*10**12+i for i in range(r)] for a in rows]
                plan = partition(list(range(n)), rows)
                idx = [v for _, _, part in plan.parts for v in part]
                assert sorted(idx) == list(range(n))
                for g in range(len(plan.signatures)):
                    parts = [(s, vs) for j, s, vs in plan.parts if j == g]
                    assert all(len(vs)==1 or abs(s)==1 for s, vs in parts)
                    assert sum(abs(s)<1 for s, vs in parts) <= len(plan.dual)
                    for i in range(r):
                        assert sum(s*rows[v][i] for s, vs in parts for v in vs)==0
                offsets = [rng.randrange(-40, 41) for _ in rows]
                a = [sum(x*w for x,w in zip(offsets, col)) for col in zip(*plan.cols)]
                cs = [sum(x*y for x,y in zip(dual, a)) for dual in plan.dual]
                assert all(abs(c)<=max(map(abs, offsets)) for c in cs)
                for col in zip(*rows):
                    lifted = sum(sum(x*y for x,y in zip(cs,plan.signatures[g]))*col[v]
                                 for g, _, vs in plan.parts for v in vs)
                    assert lifted == sum(x*y for x,y in zip(offsets, col))
                cases += 1
    return cases


def direct(tree, labels, boundary, fixed, jobs):
    vertices = Counter(labels.values())
    edges = Counter(x+(labels[tree[v]] if tree[v] else boundary[v]) for v,x in labels.items())
    assert len(labels) == len(vertices) == len(tree)-1 and set(vertices).isdisjoint(fixed)
    old = set(vertices) | set(fixed)
    reserved = []
    for b,t in jobs:
        vertices[t] += 1
        edges[b] += 1
        assert b in old and b+2*t and all(t!=2*p and -b not in (p, 2*p, 3*p) for p in old)
        reserved.extend((t,-t))
    assert len(set(reserved)) == len(reserved) and old.isdisjoint(reserved)
    assert vertices == edges


def actual_tree(kind, rng, arity):
    core = [-1]+[0]*4+[rng.randrange(1, v) for v in range(5, 36)]
    boundary = {v:0 for v in range(1,5)}
    counts = {v: ((v*7)%13 if v%5 else arity) for v in range(1,len(core))}
    labels, jobs, plans = prepare(core, boundary, {0}, counts, rng)
    direct(core, labels, boundary, {0}, jobs)
    labels[0] = 0
    blocked = set(labels.values())
    for b,t in jobs:
        blocked.update({t,-t} | guard_points(b,t))
    parents = list(core)
    external = []
    for v,m in counts.items():
        external.extend(range(len(parents), len(parents)+m))
        parents.extend([v]*m)
    if kind == 'empty':
        jumps = {v:labels[parents[v]] for v in external}
        placement = first_choice(offsets_for_level(jumps), 0, set(labels.values()), blocked)
        row, values, reserve, extra = placement
        labels.update(row)
        blocked.update(values | reserve)
        jobs.extend(extra)
        external = []
    pairs = list(jobs)
    routes = []
    def edge():
        v = len(parents)
        parents.append(0)
        x = v+1
        while x in blocked or any(x in guard_points(b,t) for b,t in pairs):
            x += 1
        blocked.add(x)
        labels[v] = x
        return v
    for j,(b,t) in enumerate(pairs):
        windows = []
        for i, length in enumerate((21,21,43,43) if kind=='active' else (87,)):
            if kind == 'empty':
                ms = [0]*length
            elif kind == 'active':
                ms = [0]*length
                ms[3] = 1+j%2
            else:
                ms = [1+j%3]*length
            windows.append(expand_edge(parents, edge(), [(m,()) for m in ms]))
        routes.append(('active' if kind=='active' else 'uniform',windows,b,t))
    extras = []
    if kind == 'active':
        for j in range(4):
            ms = [0]*21
            ms[9 if j%2 else 10] = 10
            extras.append(expand_edge(parents, edge(), [(m,()) for m in ms]))
    g = restore(parents, labels, blocked, routes, 0, rng, endpoint_windows=extras,
                external_leaves=external)
    return audit(parents, labels, g), len(pairs), sum(counts.values())


def bounded_supports(rng):
    cases = 0
    for size in range(1, 10):
        for leaves in (0, 1, 27, 571):
            tree = [-1]+[rng.randrange(i) for i in range(1, size)]
            tree.extend([0]*leaves)
            for p in range(1, size):
                tree.extend([p]*(2+(p%3)*leaves))
            labels, gap = support_first(tree)
            assert gap == min(labels) and labels[0] == 0
            assert len(set(labels)) == len(labels) == len(tree)
            actual = Counter(labels[v]+labels[p] for v,p in enumerate(tree) if v)
            actual[gap] += 1
            assert actual == Counter(labels)
            assert max(labels)-min(labels) <= 100*(size+1)*2**size*(len(tree)+1)**2
            cases += 1
    return cases


def main():
    rng = Random(4577)
    print(f"{vectors(rng)} rational vector partitions with zero, dependent and nearly parallel weights.")
    trees = edges = 0
    for n in range(1, 44):
        for mode in range(3):
            tree = [-1]+[rng.randrange(v) for v in range(1,n)]
            boundary = {v:(-12,0,7)[v%3] for v in range(1,n) if not tree[v]}
            counts = {v:(rng.randrange(15) if mode else int(v==n-1)*10**12)
                      for v in range(1,n)}
            fixed = set(range(-12,9))
            labels, jobs, plans = prepare(tree,boundary,fixed,counts,rng)
            direct(tree,labels,boundary,fixed,jobs)
            # The weighted terminal sum on a nonseed level is a sum of rounding
            # errors and transverse displacements, one per unit of mass.
            for plan in plans:
                mass = sum(counts[v] for v in plan.nodes)
                actual = sum(counts[v]*labels[v] for v in plan.nodes)
                bound = 100*(len(plan.parts)+1)**2*(10*(n+len(fixed))+1)
                assert abs(actual) <= (bound+1)*mass
            trees += 1
            edges += n-1
    deep = [-1]
    boundary = {}
    for j, p in enumerate((0, -12, 7)):
        v = 0
        for _ in range(480+17*j):
            deep.append(v)
            if not v:
                boundary[len(deep)-1] = p
            v = len(deep)-1
    core_labels, pairs, _ = prepare(deep, boundary, set(range(-12, 9)),
                                    {v:v%31 for v in range(1, len(deep))}, rng)
    direct(deep, core_labels, boundary, set(range(-12,9)), pairs)
    print(f"Deep neutral-seed forest with {len(deep)-1:,} entering edges.")
    print(f"{bounded_supports(Random(813))} support-first endpoint certificates.")
    data = [actual_tree(kind,rng,m) for kind in ('uniform','active','empty') for m in (17,72)]
    print(f"{trees} forests, {edges:,} actual entering edges and terminal moment checks.")
    print(f"{len(data)} whole trees, {sum(x[0] for x in data):,} edges, "
          f"{sum(x[1] for x in data)} repairs, {sum(x[2] for x in data):,} ordinary terminal leaves.")


if __name__=='__main__':
    main()

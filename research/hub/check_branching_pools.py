"""Check the palette coupling, modular gap calculation, and two disjoint weighted cuts."""

from collections import Counter
from itertools import permutations, product
from random import Random

from research.hub.branching_pools import finish_vertex, palette_law, two_suffixes
from research.hub.two_hub_contraction import complete
from research.rainbow.verify import rooted_shapes


def palette_checks(rng):
    checked = joint = 0
    for k in (53,96,121,256):
        for trial in range(24):
            # Each bulk batch has a terminal and an ordinary vertex role.
            h = rng.randrange(k//2,k+1)
            final = rng.randrange(1,h//12+1)
            blocks = [(h-final)//4+int(i<(h-final)%4) for i in range(4)]
            terminal = [0]*4
            for _ in range(final):
                i = rng.choice([i for i in range(4) if terminal[i]<blocks[i]])
                terminal[i] += 1
            a = [v for i,n in enumerate(blocks) for v in (terminal[i],n-terminal[i])]+[final]
            b = blocks+[final]
            rules = {(i,i//2) for i in range(8)}|{(i,4) for i in (0,2,4,6,8)}
            cells = palette_law(k,a,b,rules)
            assert list(map(sum,cells))==[k*(k-h)]+[k*x for x in a]
            assert list(map(sum,zip(*cells)))==[k*(k-h)]+[k*x for x in b]
            assert all(x>=0 for row in cells for x in row)
            assert not any(cells[0][1:]) and not any(row[0] for row in cells[1:])
            for i,j in rules:
                assert cells[i+1][j+1]==a[i]*b[j]
            if trial==0:
                # Swap two underlying color coordinates. Test the full role law, including
                # the distinctions between all selected vertex roles and their complement.
                for rows,col in [({0,1},0),({0,2,4,6,8},4)]:
                    one = Counter()
                    for i,row in enumerate(cells):
                        for j,mass in enumerate(row):
                            one[(i if i-1 in rows else 0,int(j==1+col))] += mass
                    counts = Counter()
                    for (x,c),(y,d) in product(one,repeat=2):
                        counts[(x,y,d,c)] += one[x,c]*one[y,d]
                    vertex = {i+1:a[i] for i in rows}
                    vertex[0] = k-sum(vertex.values())
                    for (x,y,c,d),mass in counts.items():
                        z = b[col]
                        assert mass==vertex[x]*vertex[y]*(z if c else k-z)*(z if d else k-z)
                        joint += 1
            checked += 1
    return checked,joint


def graph_of(tree):
    graph = [[] for _ in tree]
    for v,p in enumerate(tree[1:],1):
        graph[p].append(v)
        graph[v].append(p)
    return graph


def check_cut(graph,count,rng):
    n = len(graph)
    center,sets = two_suffixes(graph,count)
    assert sets[0].isdisjoint(sets[1])
    populations = [rng.randrange(22) for v in graph]
    if n%2:
        populations[rng.randrange(n)] += 10**5
    assert min(sum(populations[v] for v in side) for side in sets)*2 <= sum(populations)
    excess = sum(max(0,len(nb)-3) for nb in graph)
    for side in sets:
        assert len(side)==count and center not in side
        reachable = {center}
        queue = [center]
        for v in queue:
            for w in graph[v]:
                if w not in side and w not in reachable:
                    queue.append(w)
                    reachable.add(w)
        assert len(reachable)==n-count
        parents = [p for p in reachable for w in graph[p] if w in side]
        assert len(set(parents)) <= 3+count.bit_length()
        assert len(parents)<=3*(3+count.bit_length())+excess


def cuts(rng):
    total = 0
    for n in range(5,12):
        for tree in rooted_shapes(n).values():
            for count in range(1,(n-1)//4+1):
                check_cut(graph_of(tree),count,rng)
                total += 1
    for n in (97,256,2025,5000):
        for mode in range(5):
            tree = [-1]+[([v-1,0,(v-1)//2,rng.randrange(v),v//3][mode]) for v in range(1,n)]
            for count in (1,n//10,(n-1)//4):
                check_cut(graph_of(tree),count,rng)
                total += 1
    return total


def matching_moments(rng):
    successes = full = composite = degrees = 0
    for _ in range(140):
        # Decorate an actual branching tree. Reduction of its two complete integer
        # intervals gives the full bijection, independent of the matching routine.
        tree = [-1,0,0,1,1,2,2,3,4,5,6,3,4,5,6,7,9,11,12,13,14]
        a,b = rng.sample(range(10),2)
        witness = complete(tree,a,b)
        assert witness is not None
        labels,iv,_ = witness
        extras = [(p,x) for p,lo,hi in iv.blocks for x in range(lo,hi)]
        extras += [(0,iv.hi+1+i) for i in range(rng.randrange(2,20))]
        k = len(tree)+len(extras)
        root_label = labels[0]%k
        labels = [x%k for x in labels]
        weights = {v:(labels[tree[v]]+labels[v])%k for v in range(1,len(tree))}
        leaves = [v for v in range(1,len(tree)) if v not in tree[1:]]
        rng.shuffle(leaves)
        chosen = []
        parents = set()
        for v in leaves:
            if tree[v] not in parents:
                parents.add(tree[v])
                chosen.append(v)
            if len(chosen)==4:
                break
        graph = graph_of(tree)
        z = rng.choice([v for v in range(1,len(tree)) if v not in chosen and
                        v not in parents and v not in (a,b) and len(graph[v])>=2])
        neighbors = [labels[w] for w in graph[z]]
        used = set(weights.values())|{(p+x)%k for p,x in extras}
        gap, = set(range(k))-used
        C = {gap}|{(labels[z]+p)%k for p in neighbors}|{weights[v] for v in chosen}
        V = {labels[z]}|{labels[v] for v in chosen}
        X = [labels[tree[v]] for v in chosen]
        assert root_label not in V
        result = finish_vertex(k,neighbors,V,C,sum(X))
        assert result is not None
        trial,newgap = result
        open_weights = C-{(trial+p)%k for p in neighbors}
        new_vertices = V-{trial}
        assert newgap in open_weights
        assert (sum(open_weights)-newgap-sum(new_vertices)-sum(X))%k==0
        # Exhaust the actual labeled boundary edges for this finite completion.
        for row in permutations(new_vertices):
            if {(p+x)%k for p,x in zip(X,row)}==open_weights-{newgap}:
                full += 1
                break
        true = set(C)-{(labels[z]+p)%k for p in neighbors}
        assert (sum(true)-gap-sum(V-{labels[z]})-sum(X))%k==0
        composite += any(k%i==0 for i in range(2,int(k**0.5)+1))
        degrees = max(degrees,len(neighbors))
        successes += 1
    return successes,full,composite,degrees


if __name__=='__main__':
    rng = Random(500933)
    a,b = palette_checks(rng)
    print(f"{a} exact transportation laws; {b:,} probabilities checked after a nontrivial permutation.")
    print(f"{cuts(rng):,} pairs of disjoint weighted suffixes checked on the input trees.")
    n,f,c,d = matching_moments(rng)
    print(f"{n} internal-label and omitted-weight checks (degree through {d}, {c} composite moduli); "
          f"{f} exact terminal matchings for the first admissible internal label.")

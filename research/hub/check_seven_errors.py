"""Direct histograms for the seven-error bound and its exact bare-path repair."""

from collections import Counter
from random import Random

from research.hub.seven_errors import prepare, restore
from research.rainbow.verify import rooted_shapes


def compare(tree,labels,bills,k):
    assert labels[0]==0 and len(set(labels))==len(labels)==len(tree)
    weights = Counter((labels[v]+labels[p])%k for v,p in enumerate(tree) if v)
    vertices = Counter(labels)
    weights[0] += 1
    reserved = set()
    for b,t in bills:
        weights[b] += 1
        vertices[t] += 1
        assert b in labels and len({t,(-t)%k})==2 and (b+2*t)%k
        assert reserved.isdisjoint((t,(-t)%k))
        reserved.update((t,(-t)%k))
    assert reserved.isdisjoint(labels) and weights==vertices and len(bills)<=7


def main():
    shapes = cases = total = 0
    rng = Random(801)
    for n in range(1,13):
        for tree in rooted_shapes(n).values():
            data,bills,_,_ = prepare(tree,65536,rng)
            compare(tree,[data[v] for v in range(n)],bills,65536)
            shapes += 1
    maximum = restored = attached_sums = 0
    modes = set()
    for k in (65520,65521,65536):
        for n in (38,86,194,320):
            trees = [[-1]+list(range(n-1)),[-1]+[rng.randrange(v) for v in range(1,n)],
                     [-1]+[0]*8+[1+(v-9)%(8+(v-9)//3) for v in range(9,n)]]
            # Shallow, highly branching subtree with exactly seven nonroot levels.
            wide = [-1,0]
            layer = [1]
            for j in range(7):
                top = len(wide)
                wide.extend(p for p in layer for _ in range(2 if j<5 else 1))
                layer = list(range(top,len(wide)))
            trees.append(wide)
            for tree in trees:
                child = rng.randrange(1,len(tree))
                parents,labels,stats,count = restore(tree,child,k)
                compare(parents,labels,[],k)
                assert len(parents)==len(tree)+129
                old = parents[:len(tree)]
                vertex = child
                for j in range(129):
                    vertex = parents[vertex]
                    assert vertex==len(tree)+128-j
                old[child] = parents[vertex]
                assert old==list(tree)
                if tree is wide and n==320:
                    used = set(labels)
                    period = [v for v in range(k) if v not in used]+[0]+sorted(used-{0})
                    for order in (k-17,k,k+1,k+243,2*k+17):
                        leaves = [period[i%k] for i in range(order-len(tree)-129)]
                        vertices = Counter(labels+leaves)
                        weights = Counter((labels[v]+labels[p])%k for v,p in enumerate(parents) if v)
                        weights.update((labels[0]+x)%k for x in leaves)
                        assert all(max(c.values())-min(c[x] for x in range(k))<=1
                                   for c in (vertices,weights))
                        restored += 1
                        attached_sums += order-1
                maximum = max(maximum,count)
                modes.add(bool(stats[0]))
                cases += 1
                total += len(tree)+128
    assert maximum==7 and modes=={True,False}
    print(f"{shapes:,} rooted shapes. {cases} exact repairs, {total:,} actual endpoint sums, "
          f"with up to {maximum} protected errors.")
    print(f"{restored} hub extensions with {attached_sums:,} actual endpoint sums.")


if __name__=='__main__':
    main()

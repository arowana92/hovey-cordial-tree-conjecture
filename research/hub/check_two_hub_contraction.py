"""Audit range certificates without materializing any filler leaf."""

from collections import Counter
from random import Random

from research.hub.modular_injection import construct as modular_certificate
from research.hub.two_hub_contraction import bound, compact_complete, complete
from research.rainbow.verify import rooted_shapes


def audit_ranges(singletons, bands, start, stop):
    change = Counter()
    for x in singletons:
        change[x] += 1
        change[x+1] -= 1
    for a,b in bands:
        assert a<b
        change[a] += 1
        change[b] -= 1
    expected = Counter({start:1,stop:-1})
    assert {x:c for x,c in change.items() if c}==dict(expected)


def audit(tree,a,b,extra=(0,0),compressed=False):
    witness = (compact_complete if compressed else complete)(tree,a,b)
    if witness is None:
        parents = tree+[a,b]
        degrees = Counter(parents[1:])+Counter(range(1,len(parents)))
        spine_degrees = Counter()
        for v,p in enumerate(parents[1:],1):
            if min(degrees[v],degrees[p])>1:
                spine_degrees[v] += 1
                spine_degrees[p] += 1
        assert max(spine_degrees.values(),default=0)<=2
        return None

    labels,interval,rounds = witness
    lo,hi = interval.lo,interval.hi
    assert labels[a]==0 and labels[b]==1
    if compressed:
        order,jobs,_,_ = rounds
        degree = Counter(tree[1:])+Counter(range(1,len(tree)))
        leaves = sum(x==1 for x in degree.values())
        assert order<=12*leaves+1 and jobs<=2*leaves
        assert hi-lo+1<=100*(bound(order)+1)*(len(tree)+1)**2*(leaves+1)
    else:
        assert hi-lo+1<=bound(len(tree))
        assert sum(rounds)<=7*(2*len(tree)-1).bit_length()
    blocks = interval.blocks.copy()
    if extra[0]:
        blocks.append((0,hi+1,hi+1+extra[0]))
        hi += extra[0]
    if extra[1]:
        blocks.append((1,lo-extra[1],lo))
        lo -= extra[1]
    assert all(hub in (0,1) for hub,_,_ in blocks)
    weights = [labels[i]+labels[p] for i,p in enumerate(tree) if i]
    audit_ranges(labels,[(x,y) for _,x,y in blocks],lo,hi+1)
    audit_ranges(weights,[(x+p,y+p) for p,x,y in blocks],lo+1,hi+1)
    return rounds,hi-lo+1


def main():
    small = residual = 0
    for n in range(2,11):
        for tup in rooted_shapes(n).values():
            tree = list(tup)
            for b in range(1,n):
                result = audit(tree,0,b,(2,3))
                small += 1
                residual += result is None

    rng = Random(52129)
    tall = cells = path_rounds = tree_rounds = 0
    for n in (100,511,2001,8193):
        for case in range(8):
            if case<2:
                tree = [-1]+list(range(n-1))
                a,b = (0,n-1) if case==0 else (0,1)
            elif case<4:
                tree = [-1]+[(v-1)//2 for v in range(1,n)]
                a,b = (0,1) if case==2 else (rng.randrange(n//2),n-1)
            else:
                tree = [-1]+list(range(n//2))
                while len(tree)<n:
                    tree.append(rng.randrange(len(tree)))
                a,b = rng.sample(range(n),2)
            result = audit(tree,a,b,(101,207))
            assert result is not None
            stages,size = result
            tall = max(tall,n)
            cells = max(cells,size)
            path_rounds = max(path_rounds,stages[0])
            tree_rounds = max(tree_rounds,stages[1])

    long_tests = 0
    max_group = max_original = 0
    for branches in (2,3,6,14,34):
        for parity in range(4):
            tree = [-1]
            tips = []
            for j in range(branches):
                parent = 0 if j<3 else rng.choice(tips[:-1])
                for _ in range(71+2*j+((j+parity)%2)):
                    tree.append(parent)
                    parent = len(tree)-1
                tips.append(parent)
            a,b = (0,tips[-1]) if parity%2 else (tips[0],tips[-1])
            stages,_ = audit(tree,a,b,(20,31),compressed=True)
            max_group = max(max_group,stages[1])
            max_original = max(max_original,len(tree))
            long_tests += 1
    for n in range(3,9):
        for tup in rooted_shapes(n).values():
            for b in range(1,n):
                audit(list(tup),0,b,compressed=True)
                long_tests += 1
    # If the secondary population is small, absorb it into a new rooted core.
    # Recompute its actual sums before and after a few more leaves at the zero hub.
    tree = [-1,0,0,1,1,2,4,5,3,4,8,10]
    extensions = 0
    for second in range(9):
        core = tree+[4]*second
        k = 101*(len(core)+1)**14
        labels,gap,_ = modular_certificate(core,k)
        verts = set(labels)
        edges = {(labels[i]+labels[p])%k for i,p in enumerate(core) if i}
        assert len(verts)==len(core) and edges==verts-{gap}
        first_leaves = [x for x in range(len(core)+20) if x not in verts][:10]
        assert len(first_leaves)==10
        for count in range(11):
            x = labels+first_leaves[:count]
            parents = core+[0]*count
            assert len(set(x))==len(x)
            assert len({(x[i]+x[p])%k for i,p in enumerate(parents) if i})==len(x)-1
            extensions += 1
    print(f"{small:,} marked cores through order 10, including {residual:,} residual caterpillars.")
    print(f"32 interval sweeps through order {tall:,}; largest verified interval has {cells:,} integers.")
    print(f"Up to {path_rounds} hub-path stage and {tree_rounds} exterior stages; {extensions} one-site absorptions and extensions.")
    print(f"{long_tests:,} compressed-core replays, up to {max_group} simultaneously elongated segments and {max_original:,} original vertices.")


if __name__=='__main__':
    main()

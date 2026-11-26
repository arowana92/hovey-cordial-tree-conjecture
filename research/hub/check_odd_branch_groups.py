"""Check actual boundary edges of signed lifts and both two-site completions."""

from collections import Counter

from research.hub.odd_branch_groups import construct
from research.hub.signed_tree import construct as signed
from research.rainbow.verify import rooted_shapes


def append_branch(tree,site,branch):
    offset = len(tree)
    tree.extend([site]+[offset+p for p in branch[1:]])


def main():
    packets = packet_edges = 0
    for n in range(1,8):
        for branch in rooted_shapes(n).values():
            template = signed(branch)
            for d,q in ((3,512),(5,729),(9,1024)):
                k = d*q
                for parent in range(0,k,q):
                    vertices = []
                    weights = []
                    for sign in (1,-1):
                        for j in range(d):
                            row = [(sign*x+j*q) % k for x in template]
                            vertices.extend(row)
                            weights.extend((row[v]+(parent if v == 0 else row[p])) % k
                                           for v,p in enumerate(branch))
                    assert len(set(vertices)) == len(vertices)
                    assert Counter(vertices) == Counter(weights)
                    packets += 1
                    packet_edges += len(weights)

    cases = groups = rounds = max_order = no_leaves = restricted = 0
    modes = set()
    for d,q in ((3,524288),(5,531441),(9,524287)):
        for side in (0,1):
            for depth in (2,4,5,9,16,68):
                tree = [-1,0]
                path = [-1]+list(range(depth-1))
                # Include both a protected repeated deepest shape and other shapes.
                for _ in range(2*d if depth < 10 else 2):
                    append_branch(tree,side,path)
                for v in (0,1):
                    for branch in ([-1,0],[-1,0,0],[-1,0,1,1]):
                        for _ in range((18 if depth == 68 else 2)*d):
                            append_branch(tree,v,branch)
                for second in ((0,1,d-1,8*d+2) if depth >= 5 else (32*d,32*d+1)):
                    values,gap,(height,g,batches) = construct(tree,d,q,second)
                    k = d*q
                    parents = tree+[1]*second
                    weights = Counter((values[v]+values[p]) % k for v,p in enumerate(parents) if v)
                    assert values[:2] == [0,q] and len(set(values)) == len(parents)
                    assert Counter(values) == weights+Counter([gap])
                    # Use actual extra leaves at zero just before and after all
                    # previously empty residues have been filled.
                    old = set(values)
                    prefix = [gap]+sorted(old-{gap})
                    for j in (0,1,len(values)-1):
                        added = set(prefix[:j])
                        # Each residue outside old appears once in both histograms.
                        for hist in (Counter(values),weights):
                            counts = [hist[x]+(x in added) for x in old]+[1]
                            assert max(counts)-min(counts) <= 1
                    assert height == depth or depth < 3 and height == 3
                    modes.add(depth >= 5)
                    no_leaves += second == 0
                    restricted += second < sum(p == 1 for p in tree[2:])
                    max_order = max(max_order,len(parents))
                    groups += g
                    rounds += batches
                    cases += 1
    assert modes == {True,False} and min(no_leaves,restricted,rounds,groups) > 0
    print(f"{packets:,} neutral packets at all subgroup parents, {packet_edges:,} actual weights.")
    print(f"{cases:,} two-site trees through order {max_order:,}, {groups:,} restored groups and "
          f"{rounds:,} ten-vertex batches; {no_leaves} cases with no second-site leaves.")


if __name__ == '__main__':
    main()

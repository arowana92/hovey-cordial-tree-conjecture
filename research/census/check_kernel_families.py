"""Prove prescribed extensions at all orders for kernels with up to six edges."""

from argparse import ArgumentParser
from collections import Counter
from itertools import permutations

from research.census.check_leaf_kernel import brute
from research.census.leaf_kernel import all_deficits, evaluate, spectrum
from research.rainbow.spine_counts import rooted
from research.rainbow.verify import rooted_shapes


def marked_shapes(s):
    for parent in rooted_shapes(s+1).values():
        seen = set()
        for site in range(s+1):
            code = [""]*(s+1)
            for v in reversed(range(s+1)):
                children = sorted(code[w] for w in range(v+1,s+1) if parent[w]==v)
                left,right = ("[","]") if v == site else ("(",")")
                code[v] = left + "".join(children) + right
            if code[0] not in seen:
                seen.add(code[0])
                yield parent,site


def consecutive_kernel(parent, site):
    """A common interval of s distinct entries injects at every modulus >= s."""
    s = len(parent)-1
    for low in range(1-s,1):
        target = set(range(low,low+s))
        for free in permutations(target):
            label = (0,*free)
            w = {label[v]+label[parent[v]]-label[site] for v in range(1,s+1)}
            if w == target:
                return True
    return False


def small_extension(parent, k, d):
    """Search the actual rooted tree with a normalized joint and old edge deficit d."""
    n = len(parent)-1
    label = [0]*(n+1)
    vertex = [0]*k
    edge = [0]*k
    vlow, vhigh = n//k, (n+k-1)//k
    low = [(n-1)//k + (i==d) for i in range(k)]
    high = [(n+k-2)//k + (i==d) for i in range(k)]

    def visit(i):
        if i == n+1:
            return min(vertex)>=vlow and all(x>=a for x,a in zip(edge,low))
        for x in range(k):
            w = (x+label[parent[i]]) % k
            if vertex[x] == vhigh or edge[w] == high[w]:
                continue
            label[i] = x
            vertex[x] += 1
            edge[w] += 1
            if visit(i+1):
                return True
            vertex[x] -= 1
            edge[w] -= 1
        return False

    assert visit(1), (parent,k,d)
    vcount = Counter(label[1:])
    wcount = Counter((label[v]+label[parent[v]]) % k for v in range(1,n+1))
    ve = [vcount[i] for i in range(k)]
    ed = [wcount[i] - int(i==d) for i in range(k)]
    assert max(ve)-min(ve)<=1 and max(ed)-min(ed)<=1


def check_order(s):
    consecutive = neutral = marked = maximum = small = 0
    for parent,site in marked_shapes(s):
        for k in range(1,s):
            for residual in range(k):
                tree = parent + (site,)*residual
                for d in range(k):
                    small_extension(tree,k,d)
                    small += 1
        if consecutive_kernel(parent,site):
            consecutive += 1
            continue
        neutral_terms = spectrum(parent,site)
        combined = Counter(neutral_terms)
        threshold = all_deficits(combined,s)
        if threshold is None:
            marked_terms = spectrum(parent,site,marked=True)
            for n in (s,s+1):
                actual, by_deficit = brute(parent,site,n)
                assert actual == evaluate(neutral_terms,n)
                assert by_deficit == [evaluate(marked_terms,n,d) for d in range(n)]
            combined.update(marked_terms)
            threshold = all_deficits(combined,s)
            assert threshold is not None, (parent,site)
            marked += 1
        else:
            neutral += 1
        maximum = max(maximum,threshold)
    # A path between two ordered marks is a nonempty sequence of rooted trees.
    expected = [1]
    for n in range(1,s+2):
        expected.append(sum(sum(rooted(j).values())*expected[n-j] for j in range(1,n+1)))
    assert consecutive + neutral + marked == expected[-1]
    print(s, consecutive, neutral, marked, maximum, small, flush=True)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--edges", type=int, choices=range(1,7))
    args = parser.parse_args()
    print("edges interval neutral-count marked-count largest-threshold small-deficits")
    for size in ([args.edges] if args.edges else range(1,7)):
        check_order(size)

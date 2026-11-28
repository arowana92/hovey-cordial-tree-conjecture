"""Verify DFS obstruction trees, ordinary labelings, and sharp fixed-core examples."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations

from research.rainbow.check_terminal_arm_order import original_arms


def cordial(k, parents, labels):
    vertices = [0]*k
    weights = [0]*k
    for v,x in enumerate(labels):
        assert 0 <= x < k
        vertices[x] += 1
        if v:
            weights[(x+labels[parents[v]])%k] += 1
    return max(vertices)-min(vertices) <= 1 and max(weights)-min(weights) <= 1


def is_preorder(parents):
    stack = []
    for v,p in enumerate(parents):
        if v:
            while stack and stack[-1] != p:
                stack.pop()
            if not stack:
                return False
        stack.append(v)
    return True


def add_star(parents,site,size):
    center = len(parents)
    parents.extend([site]+[center]*(size-1))
    return range(center,center+size)


def composite_tree(k,p):
    g = k//p
    parents = [-1]+list(range(k-1))
    sites = [k-1-i for i in range(p)]+[0]
    first_site = sites[0]
    small,large = [],[]
    for site in sites:
        small.append(add_star(parents,first_site,g))
        large.append(add_star(parents,site,k-g))
        first_site = large[-1].start
    assert is_preorder(parents) and len(parents) == k*(p+2)
    return parents,sites,small,large


def caterpillar(k,order,edges):
    bipart = {edges[0][0]:0}
    lists = [[],[]]
    seen = set()
    for u,v in edges:
        bipart[v] = 1-bipart[u]
        for w in (u,v):
            if w not in seen:
                seen.add(w)
                lists[bipart[w]].append(w)
    labels = [-1]*order
    for i,v in enumerate(lists[0]+lists[1]):
        labels[v] = i%k
    return labels


def ordinary(k,parents,sites,small,large):
    # The unpaired stars extend the two ends of the original path.
    left,right = large[-1],small[0]
    spine = [left.start]+list(range(k))+[right.start]
    edges = [(left.start,v) for v in left[1:]]
    edges.extend(zip(spine,spine[1:]))
    edges.extend((right.start,v) for v in right[1:])
    labels = caterpillar(k,len(parents),edges)
    assert sum(x>=0 for x in labels) == 2*k
    for j,site in enumerate(sites[:-1]):
        # Normalize the old parent to zero, then translate the entire piece.
        outer,inner = large[j],small[j+1]
        g = len(inner)
        block = [(outer.start,g-1),(inner.start,g)]
        block.extend(zip(inner[1:],range(g-1)))
        block.extend(zip(outer[1:],range(g+1,k)))
        assert len(block) == k and len({x for _,x in block}) == k
        for v,x in block:
            labels[v] = (x+labels[site])%k
        assert len({(labels[v]+labels[parents[v]])%k for v,_ in block}) == k
    assert cordial(k,parents,labels)


def exhaust_order(k,p):
    parents,sites,small,large = composite_tree(k,p)
    labels = set(range(k))
    g = len(small[0])

    @lru_cache(None)
    def next_states(a,b,gap):
        x = (gap-a)%k
        states = set()
        for y in labels-{x}:
            rest = labels-{x,y}
            for choose in combinations(sorted(rest),g-1):
                first = set(choose)
                # The forced edge has just made the edge bins uniform.
                weights = {(x+v)%k for v in first}
                weights.update((y+v)%k for v in rest-first)
                weights.add((b+y)%k)
                if len(weights) == k-1:
                    missing, = labels-weights
                    states.add((y,missing))
        return states

    initial_count = 0
    for suffix in permutations(range(1,k)):
        word = (0,)+suffix
        weights = {(word[v]+word[parents[v]])%k for v in range(1,k)}
        if len(weights) != k-1:
            continue
        initial_count += 1
        gap, = labels-weights
        states = {(word[sites[0]],gap)}
        for site in sites:
            states = {new for a,d in states for new in next_states(a,word[site],d)}
        assert not states
    return initial_count


def short_caterpillar(k,g):
    parents = [-1]+list(range(k))
    end_leaves = range(len(parents),len(parents)+k-1-g)
    parents.extend([k]*len(end_leaves))
    star = add_star(parents,0,g)
    assert len(parents) == 2*k and is_preorder(parents)
    edges = [(k,v) for v in end_leaves]
    spine = list(reversed(range(k+1)))+[star.start]
    edges.extend(zip(spine,spine[1:]))
    edges.extend((star.start,v) for v in star[1:])
    labels = caterpillar(k,len(parents),edges)
    assert cordial(k,parents,labels)
    assert (k*(k-1)//2)%g != 0
    return len(parents)


def check_small_core(k):
    # Two periods of a path cordial at every prefix, with equal labels at
    # its two ends and label one at the attachment position two.
    path = [i//2 + ((k+1)//2 if i%2 else 0) for i in range(k)]
    S = sum(range(k))%k
    old = path+[(x-S)%k for x in path]+[0]
    parents = [-1]+list(range(2*k))
    assert all(cordial(k,parents,old[:i]) for i in range(1,len(old)+1))
    parents.append(2*k)
    add_star(parents,2,k-6)
    parents.extend([0]*4)
    parents.append(len(parents)-1)
    assert is_preorder(parents) and len(parents) == 3*k+1
    arms = original_arms(parents)
    assert sum(len(path)==1 for path in arms.values()) == (3 if k==8 else 5)
    attempts = 0
    for row in permutations(range(1,k)):
        attempts += 1
        assert not cordial(k,parents,old+list(row))
    return attempts


def main():
    n = total = short = 0
    for k in range(4,201):
        p = next((a for a in range(2,k) if k%a==0),None)
        if p is None:
            continue
        parents,sites,small,large = composite_tree(k,p)
        # Forget all the other earlier labels. Each congruence class contains
        # exactly p of the k distinct labels demanded by the first prefix.
        assert max(Counter(x%(k//p) for x in range(k)).values()) < len(set(sites))
        ordinary(k,parents,sites,small,large)
        n += 1
        total += len(parents)
        two_part = k & -k
        if 1 < two_part < k:
            short += short_caterpillar(k,two_part)

    print('composite moduli',n,'vertices in ordinary cordial trees',total)
    print('vertices in two-period caterpillars',short)
    for k,p in [(4,2),(6,2),(8,2),(9,3)]:
        print('exhausted DFS order',k,'normalized initial path labelings',exhaust_order(k,p))
    print('failed full-batch permutations at eight and nine',check_small_core(8),check_small_core(9))


if __name__ == '__main__':
    main()

# Every tree with at most five nonleaf vertices is super edge-magic

**Theorem.** If at most five vertices of a finite tree have degree at least two, the tree has a bijective integer labeling by an interval $[L,U]$ whose edge sums are exactly $[L+1,U]$. In particular it is $k$-cordial for every positive integer $k$. The number of leaves and the order of the tree are unrestricted. This includes every tree with matching number at most three.

Delete all leaves once to form the nonleaf core $H$. An empty or single-vertex core is immediate. If $H$ is a path, the original tree is a caterpillar, and if $H$ is a star its diameter is at most four. The interval labelings for these families apply. Indeed any consecutive-sums labeling of a tree can be translated so the first edge sum is one more than the first vertex label, with the singleton handled directly. The remaining possible $H$ on at most five vertices has degree sequence $3,2,1,1,1$. We call this tree the fork. The proof below supplies the interval labeling for every possible leaf distribution on it. [Caterpillar and diameter-four constructions](all-radius-two.md) · [Youssef, Theorem 4 on reduction to cordiality](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

For the matching assertion, a forest of matching number $d$ has a vertex cover of size $d$. One proof takes a leaf edge in a maximum matching, exchanging the neighbor's matching edge if necessary. Put the neighbor in the cover, delete both vertices and proceed inductively on the remaining forest. Isolated vertices cost nothing. If a nontrivial tree has a cover of size $d$, all nonleaf vertices outside the cover have at least two neighbors in it. If there are $t$ such vertices, the forest induced by them and the cover has at least $2t$ and at most $d+t-1$ edges. Hence $t\le d-1$ and there are at most $2d-1$ nonleaf vertices.

## Ranking the excess leaf counts

Each terminal vertex of $H$ has at least one leaf neighbor in the original tree. Reserve one such leaf there. Sort the five core vertices by their numbers of remaining leaves, breaking ties arbitrarily, and index them $0$ through $4$. Write $e_r$ for the number of layers comprising one additional leaf at each of the first $r$ vertices, $1\le r\le5$. Equivalently $e_r$ is the difference between the $r$th and next largest excess counts, using zero after the fifth. Each ranked fork edge set and each vector $e\in\mathbb N^5$ therefore specifies a tree, and every tree in this case occurs. There are 60 different edge sets after ranking.

A cell in the certificate has five base coordinates $b_r$ and five steps $d_r\in\{0,1,2\}$. It covers all $e_r=b_r+d_r t_r$ with $t_r\in\mathbb N$. In a coordinate of step zero only the indicated base value is allowed. The seed has the three reserved leaves, the base layers, and fixed labels $f_0,\ldots,f_4$ on the ranked fork. The remaining seed data are its lower endpoint $L$ and the parent index of each unused vertex position in order. The verifier reconstructs the seed, verifies every parent's exact count, and checks both intervals by addition.

For every $d_r>0$ the record includes two lists of parent labels. The lower list $p_i$, $0\le i<l$, and the upper list $q_i$, $0\le i<u$, satisfy
$$
\{i+p_i-1:0\le i<l\}=[0,l-1],\qquad
\{i+q_i:0\le i<u\}=[0,u-1].
$$
Their combined multiset consists of $d_r$ copies of each of $f_0,\ldots,f_{r-1}$. Give the lower children labels $L-l+i$ and the upper children labels $U+1+i$. Their edge sums cover exactly the new positions in the required edge interval. The result retains the core labels and the interval alignment. Repeating these extensions $t_r$ times at each rank labels the entire cell, regardless of the sizes of its coordinates.

Double layers enlarge the available choices of core labels. For example two copies of the parent set $\{-1,0,2\}$ use the lower list $(2,0)$ and upper list $(2,-1,-1,0)$. Their displacements satisfy the two tests above. The rank-three cells using this rule can include profiles with independently varying layers at other ranks.

## Checking coverage of infinitely many profiles

The independent verifier enumerates all four-edge subsets on five labeled vertices and selects the connected graphs of the required degree sequence. For each graph and each coordinate take $A=1+\max b_r$ over its cells, and let $P$ be the least common multiple of its positive steps there, taking one if none occur. For $e_r\ge A$ replacing that coordinate by $A+((e_r-A)\bmod P)$ preserves membership in every cell, including those of step zero. Consequently it suffices to check the box $0\le e_r<A+P$ with the coordinate-specific $A,P$.

Across all 60 graphs this requires 26,544 representatives. Every representative belongs to exactly one of the 2,619 certified cells. Of those cells, 154 use a double layer at some rank. The largest seed has 46 vertices. The finite check verifies the whole unbounded assertion by the interval extension argument. [Independent verifier](ranked_core_verify.py) · [Compressed seed and layer certificate](five-nonleaf.jsonl.gz)

## Reproduction

Run the standard-library verifier from the repository root. For each record it also restores several full layers, constructs the actual edge list and recounts the specified leaf populations and every endpoint sum.

~~~sh
python3 -B -m research.hub.ranked_core_verify
~~~

The generator searches candidate core labels supporting the required layers. If the seed has $m_i$ leaves at vertex $i$, the difference between the total of its vertex labels and the total of its edge sums forces
$$
L=\sum_i(1-\deg_H(i)-m_i)f_i .
$$
It checks that interval and matches every remaining vertex slot to a weight slot using exactly the requested counts at each parent. A limit on search nodes for one assignment has no bearing on the proof. The stored witnesses and coverage check suffice. [Generator](ranked_core_generate.py) · [Native search](ranked_core_search.cpp)

~~~sh
out=$(mktemp -d)
c++ -O3 -std=c++17 -shared -fPIC research/hub/ranked_core_search.cpp -o "$out/search.so"
python3 -B -m research.hub.ranked_core_generate "$out/search.so" > "$out/seeds.jsonl"
gzip -dc research/hub/five-nonleaf.jsonl.gz | cmp - "$out/seeds.jsonl"
~~~

The decompressed certificate has SHA-256 digest `c7b62f5048062ac5a562b5c8028d51d69f0331a7d4761108c40984ce4398ff3e`.

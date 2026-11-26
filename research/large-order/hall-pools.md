# A linear order test at every modulus

**Theorem.** Fix any $k$. If every tree of order below $2^{26}k$ is $k$-cordial, then every finite tree is $k$-cordial. More precisely, every tree of order $n\ge 2^{26}k$ with fewer than $n/32$ leaves is $k$-cordial, and a smallest counterexample has fewer than $k$ leaves. The linear test concerns a smallest counterexample. The [unconditional bound for every counterexample](primitive.md) is $O(k\log(2k))$.

The construction uses three collections of degree-two vertices. Instead of correcting one bin at a time, we realize an entire prescribed multiset of weights or labels on each collection.

## Permutations for a prescribed multiset

Suppose a multiset $A$ in $\mathbb Z/k$ has $\lambda k$ entries and sum zero modulo $k$. There are two lists $P,T$, each using every residue $\lambda$ times, such that their pointwise sums have multiset $A$. While at least $2k$ entries remain, apply the Erdős–Ginzburg–Ziv theorem to find $k$ of sum zero. The final $k$ entries also have sum zero. On each block Hall's abelian permutation theorem realizes the prescribed differences of two permutations. Negate the subtracted permutation to get sums, and concatenate. Thus at sites with a prescribed uniform list of first values we can freely choose the second values with the required two marginals. [Erdős, Ginzburg and Ziv (1961), original theorem](https://nonagon.org/ExLibris/sites/default/files/pdf/Erdos-Ginzburg-Ziv-Theorem-1961.pdf) · [Hall (1952)](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

If $\lambda$ is even, $\lambda$ copies of every residue have sum zero even at even $k$. Every correction used below has zero mass and zero first moment modulo $k$, so adding it to this uniform multiset preserves both conditions.

## Correcting the two weights at a degree-two vertex

Let $z$ denote shift by one residue. Every integer $f$ of zero mass and first moment zero modulo $k$, with $\|f\|_\infty\le D$, can be written
$$
 f=\epsilon(1-z)^2\mathbf e_0+2h+(1+z)g.
$$
Here $\epsilon\in\{0,1\}$, both $h,g$ have zero mass and moment modulo $k$, $\|g\|_\infty\le6$ and $\|h\|_\infty\le3(D+5)$. We take $k\ge2$ throughout; $k=1$ is immediate.

Use the length-$2k$ ordinary moment-zero lift $F$ from the [primitive construction](primitive.md#one-primitive-and-decaying-corrections). Its entries have magnitude at most $2D+1$, since $|\sum i f_i/k|\le kD$ and the tail entries differ by at most one. Let $r_i\in\{0,1\}$ be the parity of the prefix through $i$. On the integer line $F=(1+z)r$ modulo two. Its ordinary first moment implies that $r$ has even mass. Subtracting $(1-z)^2\mathbf e_0$ toggles exactly $r_0,r_1$, hence changes the parity of the first moment of $r$. Choose $\epsilon$ to make that moment even, and use $F'$ for the adjusted vector.

Pair consecutive nonzero entries of the adjusted $r$ from left to right and give each pair signs $+1,-1$. This integer lift has zero mass and even ordinary moment $-m$. The sum $m$ of the disjoint pair distances is between zero and $2k-1$. Move two units from coordinate zero to $m/2$; this gives an integer vector $G$ of zero mass and ordinary moment, bounded by three. Its last entry vanishes since the last prefix is even and $m/2<2k-1$. Thus $H=(F'-(1+z)G)/2$ is integer, supported in the length-$2k$ interval, with both ordinary mass and moment zero. Projecting $G,H$ to residues proves the claimed bounds and decomposition.

## Three collections on paths

An available site consists of five consecutive degree-two vertices. The middle three have labels $(p,t,p+d)$ in path order. The outer two are ordinary free vertices. Reserve three disjoint collections of $\lambda k$ sites, with $\lambda$ even. Within each collection prescribe each $p$ exactly $\lambda$ times; $d$ is constant on the collection. Initially set the centers so that their labels and the weights $p+t$ are both uniform, using the permutation result. The neighbors and both internal weights are then also uniform in each collection.

- In the first collection put $d=0$. The multiset of centers may be changed to any nonnegative $\lambda\mathbf 1+v$ of mass $\lambda k$ and moment zero while preserving a uniform list of $p+t$. Indeed realize the required centers as sums $(-p)+(p+t)$ of uniform lists. Both incident weight lists remain uniform.
- In the second collection put $d=0$ and keep the centers uniform. Realize $p+t$ with multiplicities $\lambda\mathbf 1+h$. The two weight lists together change by $2h$.
- In the third collection put $d=1$ and again keep the centers uniform. Realize $p+t$ with multiplicities $\lambda\mathbf 1+g$. The two weight lists together change by $(1+z)g$.

For the exceptional unit square reserve two additional sites. Give their middles labels $(0,1,0)$ and $(0,0,1)$. Swapping the centers changes the four incident weights from $1,1,0,1$ to $0,0,1,2$. This adds $(1-z)^2\mathbf e_0$ and keeps the vertex histogram fixed, with all residues interpreted modulo $k$.

## A discrepancy estimate in terms of n/k

The remaining free vertices form a forest. Mark one further disjoint site for a free degree-two vertex and keep a leaf free. In the forest repeatedly remove an independent set of vertices of current degree at most eight, stopping when at most $k$ vertices remain. At least half have degree at most eight and a greedy independent subset retains at least one ninth of them. Hence at most $1+18\log(n/k)$ layers have been removed when $n\ge k$; logs here are natural. Within the remaining forest continue the same removals to order its vertices, then assign labels in reverse removal order, first in this small remainder and then in the earlier layers.

Attribute each free vertex observation to its label, each edge between free vertices to the later endpoint, and every edge from a fixed site neighbor to its free buffer to that buffer. At a free variable at most twelve observations arise: one vertex, at most eight edges to earlier free neighbors, and at most one edge to a planted site on the five-vertex construction. Each observation is a translate of the chosen label in its histogram.

For the first at most $k$ choices avoid every row already containing at least 300 observations. At most $12k/300$ rows are saturated in the two histograms together, and at most $12(12k/300)<k$ residues are forbidden at a choice. Thus no bin receives more than 312 observations in this part. Its discrepancy from its own average is at most 312. For each subsequent independent layer, apply [group rounding](flexible-path.md#subdividing-edges-with-controlled-multiplicities) to uniform choices, with column mass at most twelve. Each bin deviates from its mean by at most 24 in a layer. The three reserved collections had uniform initial contributions from their fixed vertices and internal edges, and the exceptional sites contribute at most six vertices and four edges. This proves an initial discrepancy of at most $312+24(1+18\log(n/k))+6$ per histogram bin.

Choose any two balanced targets of the required sizes. If their required moment changes are $a,b$ for vertices and edges, change the spare degree-two label by $b-a$ and the leaf label by $2a-b$. Their degrees give exactly the two required moment changes. At most two vertex and three edge observations move. Thus each remaining correction has magnitude bounded by
$$
D=\lceil2000(1+\log(2+n/k))\rceil .
$$
The target and all choices have the correct total masses.

## How many vertices suffice?

A tree with $L$ leaves has at least $n-2L$ degree-two vertices in at most $2L$ runs. Splitting each run into five-vertex sites gives at least $(n-10L)/5$ sites. If $L<n/32$ this exceeds $n/8$. Take $\lambda$ to be the smallest even integer at least $4(D+10)$. For $x=n/k\ge2^{26}$ we have
$$
3\lambda+3\le 25000(1+\log(2+x)) < x/8.
$$
The second inequality holds at $2^{26}$ using $\log(2+2^{26})<19$, and the difference is increasing thereafter. We therefore have room for $3\lambda k$ ordinary sites, the two exceptional sites and the spare. The estimates above are uniform in how the collections were placed.

Use the first collection to make the vertex correction $v$. Split the independent edge correction $f$ as above, swap the exceptional centers if needed, and use the other two collections for $h,g$. Every required multiset is nonnegative by the choice of $\lambda$. None of the repairs alters a free vertex or an edge to a buffer. The result has both prescribed balanced histograms.

Finally, a [minimum-order counterexample](../counterexample-bound.md#removing-leaves) has fewer than $k$ leaves. Otherwise deleting and restoring one leaf or the residue-sized batch at the last multiple of $k$ gives a labeling from a smaller tree. At $n\ge2^{26}k$ such a tree has fewer than $n/32$ leaves, which we just proved sufficient. This establishes the linear test.

## Bounds for every counterexample

Every possible counterexample has **fewer than $2^{28}k$ nonleaf vertices**. Also, no counterexample contains a path on $2^{26}k$ vertices. The path conclusion holds more generally for any connected subtree $S$ of order $s\ge2^{26}k$ with at most $s/64$ leaves. Apply the [protected leaf deletion](high-degree.md#preserving-a-connected-subtree-while-removing-leaves), which leaves a core $C$ containing $S$ with fewer than $k$ leaves outside $S$ and whose labelings extend to the original tree. Every leaf in $S$ that is terminal in $C$ is also a leaf of $S$. Thus $C$ has fewer than $s/64+k<|C|/32$ leaves, and the path-site theorem labels it.

Here is a second sufficient condition. A tree of order $n\ge k$ with at least $30000k(1+\log(2+n/k))$ **distinct parents of leaves** is cordial. Label the nonleaves first, using the same small-forest greedy step and independent layers as above. For each parent of one or more leaves include a further unit observation in a separate histogram of the labels of the distinct parents. The column bound remains twelve. The frequency of every residue in this histogram differs from the mean by at most $312+24(1+18\log(n/k))$. Thus at least $2\lambda+1$ distinct parents of each residue are available, with $D,\lambda$ as above.

Choose two disjoint pools of leaves, each with exactly $\lambda$ leaves at parents of each residue, using one leaf per selected parent. Give each pool uniform initial lists of labels and weights. Label all other leaves in one further rounding phase with column mass two, changing each bin by at most four from its mean; leave the chosen labels in place except for the moment adjustment. Choose balanced vertex and edge targets so that their required moment changes coincide. At least one of $n,n-1$ has nonzero remainder modulo $k$. Sums of subsets of any such size attain all residues, as seen by moving the largest elements of the initial interval to the right successively; the resulting consecutive range has length at least $k$. Adjust an unplanted leaf by the common change. The remaining corrections have zero moment and size at most $D$. Use the first leaf pool with prescribed vertex counts and uniform weights, and the second with uniform labels and prescribed weights. Both applications are exactly the two-permutation result, and they attain the two targets.

To bound the nonleaves, let $H$ be the tree induced by them, of order $h\ge2^{28}k$. If $H$ has at most $h/64$ leaves, the protected subtree result applies. Otherwise protect $H$ together with one exterior leaf at each leaf of $H$. Every exterior vertex is a leaf of the original tree, so after protected deletion the resulting core has order $n'\le 2h+k$ and retains more than $h/64$ distinct parents of leaves. At $h/k\ge2^{28}$ we have $h/64>30000k(1+\log(3+2h/k))$, by evaluating at the lower endpoint and differentiating. The second sufficient condition labels this core. The protected deletions can now be reversed, proving the nonleaf bound.

## Checking the construction

The independent checker reconstructs the two vectors and the parity correction for 1,475 exhaustive small inputs and 503 larger ones, including 859 cases needing the exceptional swap. It checks both permutations and the actual sums of 288 zero-sum layers. On twelve ordinary trees it assigns the centers by their parent labels, changes the two moments, performs the repairs and recounts every endpoint sum. Twenty-four further trees exercise the two leaf pools. The order test uses the estimates and the two primary permutation theorems above. [Construction](../large_order_hall_pools.py) · [Checker](../check_large_order_hall_pools.py) · [Lean moment and parity identities](HallPools.lean)

~~~sh
python3 -B -m research.check_large_order_hall_pools
lean research/large-order/HallPools.lean
~~~

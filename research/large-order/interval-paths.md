# A square-root logarithm in the unrestricted order bound

**Theorem.** At every positive modulus $k$, every counterexample has order $O(k\sqrt{\log(2k)})$. For each fixed $0<\delta<1$, if at most $k^{1-\delta}$ vertices have leaf neighbors, the order bound is $O_\delta(k)$, with arbitrary leaf populations at those vertices.

The previous [leaf concentration estimate](leaf-routing.md) left the largest $k^\varepsilon$ leaf populations unrestricted. The argument here includes those populations. It uses two features of a tree. A sufficiently large downward fringe supplies [paths that transfer a missing weight](gap-path.md). When that fringe is too small, the compressed problem can instead be labeled in a short integer interval. Only the widest available set of jumps is needed for its repairs.

## Nested intervals of parent labels

Let $H$ be the tree of nonleaves, with order $h\le Ak$. For possible counterexamples we may take $A=2^{28}$ by the [nonleaf bound](hall-pools.md#bounds-for-every-counterexample). Orders one and two are immediate. Sort the leaf populations $p_1\ge p_2\ge\cdots$ in **one** bipartition class of $H$. We will prove, uniformly for $0<\delta\le1/2$ with $k^\delta$ sufficiently large in terms of $A$, that
$$
\sum_{r} r p_r=O_A(k/\delta) \tag{1}
$$
in a counterexample. The sum is over existing dyadic ranks $16\le r\le k^{1-\delta}$.

Write $B=k^{\delta/4}$. We will use $L=C_A(1+1/\delta)$ with a sufficiently large constant, bounding each histogram bin before the final filling step. The estimates establishing $L$ below are independent of the sizes of the retained populations. Discard ranks with $p_r<P_0=\max(B^2,128L)$. Their contribution is at most $2k^{1-\delta}P_0=O_A(k/\delta)$. Among ranks in the same dyadic population band $[2^j,2^{j+1})$, keep only the largest rank. List the remaining pairs $(r_i,p_i)$ in increasing rank order, now using $p_i$ for the population at $r_i$. The sum before the band selection is at most $4S$, where $S=\sum_i r_ip_i$. Also $\sum_{j\ge i}p_j\le4p_i$ and the number of these later indices, including $i$, is at most $4p_i/P_0$. These follow by summing geometric series separately in rank and population. An empty list already proves (1).

Put $R_i=\lfloor r_i/8\rfloor\ge2$. At stage $i$ we need parents with each signed label in $[1-R_i,R_i-1]$. Keep the same vertex every time a label recurs. Give newly requested labels distinct unused parents among the first $r_i$ sites. This is possible because the intervals are nested and the total number of holders needed so far is $2R_i-1<r_i$. Every holder first chosen at stage $i$ has at least $p_i$ leaves. The widest interval has radius $R_*$ at the largest retained rank $r_*$. Every holder has at least $p_*$ leaves. Root $H$ at the holder of zero, and protect the holders.

## Labeling a compressed tree

Peel 840 synchronous layers of unprotected nonroot terminals, stopping early if there are none. In the remaining $C$ let $u$ count the unprotected terminals and let $v$ count all holders. Preserve the holders, root and degree changes while compressing segments to lengths in $[1,12]$ congruent to their former lengths modulo twelve. The number of segments is at most $2(u+v)+v$, by first marking the natural branching points and ends, then adding the protected sites. Thus $C_0$, the compressed tree, has at most $12(2u+3v)$ edges. Compression removes an even number of edges from each segment, so the holders stay in a single bipartition. Every unprotected terminal of $C$ supplies a disjoint path of 840 edges below it. Its descendants that were removed contain no protected vertex, and its last surviving child was removed in round 840. Following the preceding rounds gives the full path.

We use [sparse pinning](leaf-routing.md#prescribing-distinct-labels-at-sparse-sites) in two ambient groups. Here is the quantitative dependence we need. If $v$ distinct labels in one bipartition are prescribed in a cyclic group of size $M\le k$, $|C_0|=O_A(M)$, and $v/M\le k^{-\delta/4}$, then both histograms can be bounded by $O_A(1+1/\delta)$. In the proof of that lemma each of the three types of random counts has mean at most $2v/M$. At $k^\delta$ sufficiently large, $(2v/M)^{\lceil24/\delta\rceil}\le k^{-3}$. The union bound over $3M$ bins and the greedy completion with at most two old neighbors per site give the assertion. The bound depends on the ratio $v/M$ even when $M$ is much smaller than $k$.

**Many unprotected terminals.** If $u\ge v$, there are at most $60u$ compressed edges. Pin the signed labels in the actual group of order $k$. We have $v\le r_*\le k^{1-\delta}$ and $|C_0|\le h$. Label $C_0$ by sparse pinning, then restore the suppressed paths using simultaneous [neutral subdivisions](flexible-path.md#subdividing-edges-with-controlled-multiplicities). As in the [degree theorem](gap-path.md#finding-enough-paths-in-a-tree), cancel the discrepancy of every compressed parent edge with a fourteen-site block. Each fringe path supplies 60 such blocks. The forced sites have labels equal up to sign to the old edge weights and contribute $O_A(1+1/\delta)$ per bin. The varying sites contribute $O_A(1)$, since there are at most $h\le Ak$ repairs. The subdivisions contribute at most $A+96$ per bin. We now have a single gap. No leaf at a holder has yet been spent.

**Few unprotected terminals.** If $u<v$, then $C_0$ has at most $60v=O(r_*)$ edges. Use the auxiliary cyclic group of order $M=\lceil r_* B\rceil$. For $k^\delta$ sufficiently large, $M\le k$, $v/M\le1/B$ and the signed holder labels are distinct modulo $M$. Sparse pinning applies. Choose the required signed representatives for holders and representatives in $[0,M)$ elsewhere. In ordinary integers all labels are in $[-M,M]$, all weights are in $[-2M,2M]$, and every **integer** label or weight multiplicity is bounded by its bin count modulo $M$. Reducing to the actual modulus $k$ also gives bounded multiplicities, since a residue has at most five representatives in this range. Keep these actual labels on $C_0$ and restore the neutral subdivisions in the group of order $k$.

For each compressed edge with child label $x$ and parent label $y$ take one integer demand from $x+y$ to $x$, using the representatives just chosen. Realizing these walks by leaves cancels the edge contributions exactly as a fourteen-site path would. Both endpoint lists have per-integer multiplicity $O_A(1+1/\delta)$ and there are $m_0=O(r_*)$ demands. The following construction uses only the holders with jumps of magnitude less than $R_*$.

## Short jumps for the small compressed tree

Write $w=\lfloor R_*/2\rfloor$, so $w\ge c r_*$ for an absolute $c>0$ over the ranks under consideration. Partition the integers into blocks $[aw,(a+1)w)$. For each demand visit every block from its source block to its target block, in order, choosing one independent uniform intermediate point in each visited block. Include the source and target as separate fixed endpoints, even if both are in the same block. Each jump has absolute value at most $2w-1<R_*$. There are
$$
T=O\big(m_0(1+M/w)\big)=O(r_* B)
$$
jumps in total. Each demand visits any one block at most once.

Choose intermediate points in two phases, even positions on each itinerary first and then odd positions. Attribute each intermediate tail count to its own point. Charge each jump to its last chosen endpoint. Every jump has at least one free endpoint, and points chosen in the same phase are nonadjacent. Conditional on earlier choices, each group's columns record one tail and at most two jumps. The expected count at any one integer tail in a phase is at most $m_0/w$. For any signed jump its expected count in a phase is at most $T/w$, since one uniform point gives any specified difference with probability at most $1/w$. Use [group rounding](flexible-path.md#subdividing-edges-with-controlled-multiplicities) in each phase with column mass at most three.

Thus each integer intermediate location occurs at most $2m_0/w+12=O(1)$ times, and each signed jump is used at most $2T/w+12=O(B)$ times. All tails stay in $[-2M-w,2M+w]$, which has bounded multiplicity on reduction modulo $k$. The fixed source tails contribute $O_A(1+1/\delta)$ per residue. Realize a jump $d$ from integer $a$ by one leaf of label $a\bmod k$ at the actual holder for $d$. The walk telescopes. Since $p_*\ge B^2$, at $k^\delta$ sufficiently large these repairs use at most one quarter of the population at any holder.

## Filling the original tree

In either case restore the 840 layers in reverse order, excluding any already-used path vertices. Split a layer into batches of size at most $k$. There are at most $840+h/k$ nonempty batches in total, since the layers are disjoint. The [single-gap Hall operation](gap-path.md#completing-all-peeled-layers) keeps a single gap $g$ and costs at most two vertex observations per bin per batch. All of $H$ is now present, together with the short-jump leaves if used. Its histograms have $E=V-\mathbf e_g$ and $\max V_x+1\le L$ for a sufficiently large $C_A$ as announced.

Set $N=\max V_x$ and $W=N\mathbf1+\mathbf e_g-V$. Filling $W$ on both sides produces uniform edges and a single surplus vertex. Partition $[0,k)$ consecutively using floors of the cumulative lengths $k r_ip_i/S$. In interval $i$ divide into blocks of at most $R_i$ residues. In each block pair the sorted list with $W_x$ copies of $x$ with its reverse. For each pair $x,y$ use a leaf of label $x$ at the holder labeled $y-x$. This gives exactly $W$ in both histograms. Any specific ordinary difference occurs at most $L$ times per block by monotonicity in the [reversal argument](leaf-routing.md#moving-a-unit-with-leaves).

At a holder first used in stage $i$ the filling costs at most
$$
\sum_{j\ge i} L\left(\frac{k r_jp_j}{S R_j}+2\right)
\le 64L k p_i/S + 8L p_i/P_0,
$$
using $r_j/R_j\le16$. If $S\ge256Lk$ this is at most half the population. Together with the short-jump costs it fits. All unused leaves at every site extend the result by Hall batches starting at order $1\bmod k$. Consequently a counterexample has $S<256Lk$, proving (1).

## Summing the populations

Ranks below 16 in each class contribute $O(k)$ leaves by the [linear maximum-degree bound](gap-path.md). Each dyadic rank $r$ bounds all populations in $[r,2r)$ by $r p_r$ in total. Hence (1) bounds the number of leaves up to rank $k^{1-\delta}$ in both classes. When there are at most $k^{1-\delta}$ leaf parents in the whole tree, we have the claimed linear order bound for fixed $\delta$ (one may decrease $\delta$ to $1/2$).

In general, for ranks $k^{1-\delta}<j\le k$, the [single-size bound](leaf-routing.md#a-sufficient-condition-at-one-population-size) with fixed exponent $1/2$ gives $p_j=O_A(k/j)$. Summation gives $O_A(k(1+\delta\log k))$ leaves. Ranks above $k$ each contribute at most $p_k=O_A(1)$ when they exist, and there are at most $h$ sites. Take $\delta=1/\sqrt{\log k}$ for sufficiently large $k$. Then $k^\delta\to\infty$, and the low and high rank bounds together are $O_A(k\sqrt{\log k})$. Add the $h$ nonleaves and use the absolute $A=2^{28}$. Finitely many smaller moduli are covered by the [former order bound](primitive.md).

There is also a linear bound for all leaf distributions if $H$ has bounded degree apart from a bounded number of vertices. Apply (1) with $\delta=1/2$ for the low ranks. Above rank $\sqrt{k}$, the [degree-based pinning and shared-list proof](leaf-routing.md#a-linear-bound-with-a-degree-condition-on-the-nonleaves) bounds all remaining leaves by $O(k)$, taking any fixed exponent below $1/2$ in that result. Adding the bounds removes the former restriction on the largest leaf population.

The bound applies to every counterexample. The separate [linear test](hall-pools.md) for the smallest one and the unresolved order-$k$ and order-$(k+1)$ questions remain.

## Reproduction

The construction implements the two-phase rounding on integer walks, placement of holders, both compressed-tree repairs and reverse-order filling. The checker reconstructs every integer jump, recomputes the original tree's edge sums, and charges the actual selected parents. Two additional core repairs at $k=256$ and $729$ use the prescribed auxiliary orders $32$ and $111$, including their integer lifts and holder budgets. It independently checks 160 multiscale population budgets with integer arithmetic. The replay checks 30 lists of integer demands with 7,261 jumps and ten complete trees through order 22,263. The tree constructions use 140 fourteen-vertex paths and 490 short-jump leaves. The general estimates follow from the proof above. [Constructor](../large_order_interval_paths.py) · [Checks](../check_large_order_interval_paths.py)

~~~sh
python3 -B -m research.check_large_order_interval_paths
~~~

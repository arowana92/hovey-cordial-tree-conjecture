# Concentration of the leaves of a counterexample

**Theorem.** Fix $0<\varepsilon<1$. In any $k$-counterexample, all but $O_\varepsilon(k\sqrt{\log(2k)})$ leaves are adjacent to the $\lceil k^\varepsilon\rceil$ vertices with the largest numbers of leaf neighbors. In particular, if no vertex has more than $k^{1-\varepsilon}$ leaf neighbors, every counterexample has order $O_\varepsilon(k\sqrt{\log(2k)})$. If in addition at most $k^{1-\delta}$ vertices have leaf neighbors, the order is $O_{\varepsilon,\delta}(k)$ for each fixed $0<\delta<1$. The same linear conclusion holds for arbitrarily many leaf parents if the tree induced by the nonleaves has bounded maximum degree apart from a bounded number of vertices.

The [later interval and path argument](interval-paths.md) gives an unrestricted order bound of $O(k\sqrt{\log(2k)})$, including trees whose leaves are concentrated at one vertex. The construction below uses the [bound of $2^{28}k$ on the number of nonleaves](hall-pools.md#bounds-for-every-counterexample). Write $H$ for the tree induced by the nonleaves and $h$ for its order. In fact all the leaf constructions apply to an arbitrary tree $H$ with $h\le Ak$, with additional leaves attached at its vertices. Trees on one or two vertices are immediate.

## Moving a unit with leaves

A new leaf of label $x$ at a parent labeled $p$ contributes $\mathbf e_{x+p}-\mathbf e_x$ to the edge histogram minus the vertex histogram. A walk from $u$ to $v$ in the residue group therefore contributes $\mathbf e_v-\mathbf e_u$ if we put one leaf at the parent for each jump and give it the label of the corresponding tail. The leaves can be at unrelated places in the tree.

For core histograms $V,E$, put $f=V-E-\mathbf e_0$. Its mass is zero. Pair its negative units to its positive units arbitrarily and route these pairs. The resulting tree has $V'-E'=\mathbf e_0$. Choose an integer $N\ge\max_x V'_x$. It remains to add the same histogram $W=N\mathbf1+\mathbf e_0-V'$ on both sides.

To do so on an interval of at most $R$ consecutive residues, sort $W_x$ copies of each integer representative $x$ and pair the resulting list with its reverse. For a paired $x,y$, put a leaf of label $x$ at a parent labeled $y-x$. Both lists have exactly the requested multiplicities. Any one ordinary difference occurs at most $\max W_x$ times on the interval. Indeed, the first coordinates are nondecreasing, the second nonincreasing, and equality of differences at two positions forces equality of both coordinates throughout the intervening positions. All jumps have absolute value less than $R$.

The resulting tree has uniform edges and a single surplus vertex at order $1\bmod k$. Every remaining leaf can now be added at its actual parent. Restore batches of $k$ until fewer remain, followed by the last partial batch. The leaf-extension lemma assigns distinct vertex labels avoiding the surplus and distinct weights for up to $k-1$ leaves. In a complete batch the last leaf supplies the missing weight. All parents are in $H$. [Leaf-extension proof](../counterexample-bound.md#removing-leaves) · [Marshall Hall's abelian permutation theorem](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

## A set of jumps of size proportional to the radix

Fix integers $2\le R<k$. Take the smallest $d$ with $R^d\ge k$. Put $Q=R^{d-1}$, $a=\lceil k/Q\rceil$ and $w=\lceil R/a\rceil$. Use the grid of integers $[0,aQ)$ with $d-1$ base-$R$ digits and one top digit of size $a$. It contains $[0,k)$ and has size less than $2k$. There are separate entries in the following list even when their residues coincide.

- For each lower digit $i=0,\ldots,d-2$, include $tR^i$ for $|t|<R$.
- Include $mQ+v$ for $0\le m<a$, $0\le v<w$.
- Include $lQ-v$ for $2-2a\le l<a$, $0\le v<w$.

The list has at most $(2d+6)R$ entries, since $aw<2R$. Each residue occurs at most $s_d=2d+12$ times. In each lower digit the integers are distinct and lie strictly between $-k$ and $k$. Each of the last two lists has distinct integers because $w\le R\le Q$. The first lies in $[0,2k)$ and the second in $(-4k,2k)$.

From a source to a target first travel to a uniform random grid point, then travel from it to the target. On each leg change the lower digits one at a time, then the top digit. For a top-digit displacement $jQ$, use two hops
$$
mQ+v,\qquad (j-m)Q-v,
$$
with $m,v$ independent uniform in their displayed ranges, drawn afresh on each leg. The number of hops per route is $2(d+1)$. All observations are reduced modulo $k$.

Suppose the endpoint lists have at most $b$ occurrences of any residue each, and contain $m_0\le bk$ paired units. The expected number of tails at a residue over all routes is at most $4b(d+1)$. At any digit boundary on the outward leg, some digits are uniform and the others retained from the source. Starting from at most $b$ copies per grid point, averaging over the replaced digits preserves that upper bound. The return leg has the same bound by using the target as the fixed endpoint. The intermediate tail of the two-hop top step is an independent translate of the preceding tail. Reduction modulo $k$ adds at most two grid positions, also after a fixed translate. For an individual demand a specified lower entry has probability at most $1/R$ per leg, since one digit in its difference is uniform. A specified top entry has probability at most $1/(aw)\le1/R$, even conditional on the actual displacement. Thus each entry has total expected use at most $2m_0/R$.

For each demand, make a group of histogram columns recording both its tail counts and its uses of the entries. Each column has mass $4(d+1)$. The [group rounding lemma](flexible-path.md#subdividing-edges-with-controlled-multiplicities) selects one route per demand with additive error at most $8(d+1)$ in every row. It applies to arbitrary finite probability weights and to rows shared by different groups. [Beck and Fiala, *Integer-making theorems*](https://doi.org/10.1016/0166-218X(81)90022-6)

## A sufficient condition at one population size

Let $A=\max(1,\lceil h/k\rceil)$. Give each list entry a distinct parent, all with the same lower bound on their leaf populations. We can arrange these prescribed labels so the two old histograms and $|f_x|$ are bounded by
$$
b=4(2A+2)s_d+2.
$$
Root $H$ arbitrarily and list it breadth first, keeping each parent's children together. Sort the prescribed residues in $[0,k)$ and assign them in that order to the selected sites. At all other sites use their successive ranks starting from zero, reduced modulo $k$. Use the unreduced ranks to count multiplicities. In the child list the parents occur in nondecreasing breadth-first order. For each of the four choices of marked or ordinary parent and child, both ordinary label sequences are nondecreasing. Equal sums force equal child labels, which occur at most $s_d$ times. The sums lie in $[0,2Ak]$. Grouping by residues proves the bound for edges, and the vertex bound follows directly.

The routing bound gives $V'_x\le N=b+4b(d+1)+8(d+1)$. Use the reversal on successive intervals of length $R$, with the final interval possibly shorter. A sufficient leaf population at **each** selected parent is
$$
\left\lceil 2bk/R\right\rceil+8(d+1)+(N+1)\lceil k/R\rceil. \tag{1}
$$
Here the reversal uses the digit-zero entry indexed by its ordinary signed difference. The other leaves and their parents are arbitrary.

Consequently for every fixed $A,\eta>0$ there is a constant $C_{A,\eta}$ such that $r$ parents with at least $C_{A,\eta}k/r$ leaves each suffice whenever $k^\eta\le r\le k$ and $h\le Ak$. To see this, fix an integer $D>2/\eta+2$, set $K=8(2D+6)$, and use $R=\lfloor r/K\rfloor$. For sufficiently large $k$, $R\ge r/(2K)\ge k^{\eta/2}$, so $d\le D$ and all entries fit. Formula (1) is $O_{A,\eta}(k/r)$. Increasing the constant covers the finitely many smaller moduli, by the earlier unrestricted order bound.

## Prescribing distinct labels at sparse sites

Let at most $k^{1-\delta}$ sites in one bipartition class receive arbitrary **distinct** labels. Assume $0<\delta<1$ and $k^\delta\ge4$. The other core labels can be chosen so the two histograms and $|f_x|$ are at most
$$
b=8(A+1)+2\lceil6/\delta\rceil+8. \tag{2}
$$

Take the smallest subtree containing the sites. Along with the sites, mark all its vertices of degree at least three. There are at most as many additional marks as sites. Label these additional marks independently and uniformly. Edges between two additional marks have independent uniform sums, since fixing one root label per component and all edge sums uniquely determines the labels of that forest. At one additional mark the edges to originally prescribed neighbors have distinct sums. For a fixed residue their contribution is a Bernoulli variable, independent between additional marks. There are no edges between originally prescribed sites.

Consider a fixed bin separately for the random vertex counts and for the two types of edge counts. In each list it is a sum of independent indicators with mean at most $2k^{-\delta}$, since the marked forest has at most $2k^{1-\delta}$ vertices and edges. For $m=\lceil6/\delta\rceil$, the probability of at least $m$ successes is bounded by the sum of the products over $m$ distinct trials, at most $(2k^{-\delta})^m\le k^{-3}$. A union bound over $3k$ lists gives a choice with all counts below $m$ in each list. The prescribed sites contribute at most one per vertex bin.

Each remaining vertex in the joining subtree has degree at most two there. Label those vertices first, then grow each hanging branch outwards. Each choice controls its own label and at most two edges to already labeled neighbors. Avoid rows holding at least $\max(8A,2m+2)$ observations. Less than $2h$ observations have been made, so at most $k/4$ rows are full and at most $3k/4$ labels are forbidden. A chosen row grows by at most two. This proves (2).

## Sharing the leaves at different population sizes

In one bipartition of $H$ sort the leaf populations $p_1\ge p_2\ge\cdots$. For fixed $0<\eta<1$, fix $D>2/\eta+2$ and $K=8(2D+6)$ as above. Consider the dyadic ranks $r$ with
$$
k^\eta\le r\le k^{1-\delta}
$$
that exist in the list. Constants in the following estimate are uniform in $\delta$ whenever $k^\delta\ge4$ and $k$ is sufficiently large in terms of $\eta$:
$$
\sum_r r p_r=O_{A,\eta}(k/\delta)\quad\text{in every counterexample}. \tag{3}
$$

Use $b$ from (2), $e=8(D+1)$, $L=b+4b(D+1)+e+1$, and $s=2D+12$. Discard ranks with $p_r<P_0=64L+4e$. Their sum of $rp_r$ is at most $2hP_0$. In each remaining population band $[2^l,2^{l+1})$ keep its largest dyadic rank. Write the retained pairs as $(r_j,p_j)$ in increasing **rank** order, with $p_j$ now denoting the population at that rank. Put $S=\sum_j r_jp_j$. The sum before this last thinning is at most $4S$, since the ranks grow geometrically within each band. Also $\sum_{j\ge i}p_j\le4p_i$ by summing the decreasing population bands. We prove that
$$
S\ge 64K(sb+L)k \tag{4}
$$
would give a labeling.

For each retained rank take a list with $R_j=\lfloor r_j/K\rfloor$. These radices satisfy $R_j\ge r_j/(2K)$ and $d_j\le D$. Give each **distinct residue** required anywhere a single actual parent. When a residue first appears at stage $j$, choose an unused parent among the first $r_j$. The list sizes through stage $j$ sum to at most $\sum_{i\le j}r_i/8\le r_j/4$. Thus a residue first assigned at stage $i$ has at least $p_i$ leaves. There are at most $k^{1-\delta}$ chosen parents, all in the same bipartition. Apply (2).

For each paired demand, randomly choose list $j$ with probability $\alpha_j=r_jp_j/S$, then route in that list. Use one rounding row per residue for the actual parent uses, even if several entries or lists use it. The expected tail bound is still $4b(D+1)$, by linearity. Each particular entry of list $j$ has expected use at most $2bk\alpha_j/R_j$. A residue first assigned at stage $i$ occurs at most $s$ times per list, so its expected use is at most
$$
2sbk\sum_{j\ge i}\alpha_j/R_j\le 16sbKk p_i/S.
$$
Rounding changes each pooled row by at most $e$. Set $N=L-1$ for the reversal step.

Partition $[0,k)$ into consecutive intervals of lengths at most $k\alpha_j+1$, using floors of the cumulative lengths. In interval $j$ apply reversal in blocks of at most $R_j$. Any parent residue can represent at most two signed ordinary differences in the digit-zero entries of that list. Its further use is therefore at most
$$
\sum_{j\ge i}2L(k\alpha_j/R_j+2)
\le 16LKk p_i/S+16L p_i/P_0.
$$
Only the lists actually containing the residue can use it, and every listed population is at least $P_0$. Together with the rounded routes, the load is at most
$$
16K(sb+L)k p_i/S+16L p_i/P_0+e\le p_i
$$
by (4) and the cutoff. Every selected leaf exists. The two histogram identities and the Hall extension finish the tree. This proves (3), since $P_0$ and the coefficient of $k$ in (4) are $O_{A,\eta}(1/\delta)$.

## From ranks to tree order

For ranks in $[r,2r)$ the sum of populations is at most $rp_r$. Apply (3) separately to both bipartitions, starting at $k^{\varepsilon/2}$. For large $k$ this covers every rank after $\lfloor k^\varepsilon/2\rfloor$ in each class up to $k^{1-\delta}$, including truncated dyadic intervals. For $k^{1-\delta}<j\le k$, once $\delta\le1/2$, the single-size theorem with $\eta=1/2$ gives $p_j=O_A(k/j)$ in any counterexample. Summing gives $O_A(k(1+\delta\log k))$. For $j>k$ use $p_j\le p_k=O_A(1)$ and $h\le Ak$. With $\delta=1/\sqrt{\log k}$ the two estimates total $O_{A,\varepsilon}(k\sqrt{\log k})$. The two exempt sets together have size at most $\lceil k^\varepsilon\rceil$; removing the globally largest populations only decreases the remainder. The existing nonleaf bound supplies an absolute $A$. The finitely many small moduli are covered by the unrestricted order bound.

If the largest population is $k^{1-\varepsilon}$ or less, the exempt parents add only $O(k)$ leaves. If at most $k^{1-\delta}$ sites have leaves for fixed $\delta>0$, use (3) with that $\delta$ directly. There is no upper-rank tail to sum. This gives the asserted linear order bound under both hypotheses.

## A linear bound with a degree condition on the nonleaves

Suppose at most $u$ vertices of $H$ have degree greater than $D_0$ in $H$. The number of leaves outside the top $\lceil k^\varepsilon\rceil$ parents of any counterexample is $O_{A,\varepsilon,D_0,u}(k)$. This allows the final tree to have large degree at arbitrarily many sites. With maximum leaf population $k^{1-\varepsilon}$ the same linear bound holds for the entire order.

To prove this, replace (2) by a deterministic pinning bound independent of the number of pins. For arbitrary injectively labeled pins in one bipartition, also fix the at most $u$ remaining vertices of degree greater than $D_0$, giving them label zero. Every edge between fixed vertices meets one of those additional vertices. The edges from any one of them to pins have distinct sums, and the additional vertices induce at most $u$ edges among themselves. Thus the vertex and edge counts are at most $2u+1$ per bin. Each subsequent choice controls at most $D_0+1$ observations. At threshold $4A(D_0+1)+2u+2$, fewer than $k/(D_0+1)$ rows are full. Their translates cannot forbid every choice, and at most $D_0+1$ observations are added to any row at one step. This bounds the two histograms and $|f_x|$ by a constant depending only on $A,D_0,u$.

Now use the sharing proof for all dyadic ranks from $k^{\varepsilon/2}$ up to $k$, with this constant in place of (2). The sites are still all distinct, in one bipartition, and carry distinct residues after pooling. The thresholds in (4) and the discarded sum are both $O_{A,\varepsilon,D_0,u}(k)$. Ranks above $k$ contribute $O_A(k)$ as before. This proves the assertion.

## Reproduction and scope

The checker enumerates 1,322,826 directed legs. It follows the actual jumps modulo $k$ and recomputes the rational occupancy and entry-use bounds by counting equally weighted choices. It tests 6,561 reversal histograms and 60 population profiles. Nine additional weighted profiles independently charge all 17,547 parent capacities, including residues shared across several lists. On 40 single-list and 28 pooled trees, it counts every actual endpoint sum, including 67,320 routing leaves and 300 additional leaves restored in Hall batches. The largest of these tests has 67,604 vertices. Fifteen further complete trees exercise the deterministic degree-based pinning bound. Lean verifies the per-bin telescoping and reversal identities. The sparse pinning, rounding and rank estimates have the proofs above. [Construction](../large_order_leaf_routing.py) · [Independent counting checks](../check_large_order_leaf_routing.py) · [Lean identities](LeafRoutes.lean)

~~~sh
python3 -B -m research.check_large_order_leaf_routing
lean research/large-order/LeafRoutes.lean
~~~

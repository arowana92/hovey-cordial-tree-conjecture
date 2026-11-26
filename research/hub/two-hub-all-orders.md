# Two attachment sites with unrestricted branch lengths and tree order

**Theorem.** At all sufficiently large $k$, let $H$ be any tree with at most $2^{\sqrt{\log_2 k}/40}$ leaves. At any two specified vertices add arbitrary numbers of leaves. The result is $k$-cordial. There is no restriction on the order of $H$, the lengths of its branches, the distance between the sites, or either population.

Equivalently the same large-$k$ conclusion holds when all but at most $2^{\sqrt{\log_2 k}/40}$ leaves of a tree are adjacent to two vertices. Removing direct leaves other than the two sites may create at most two additional core leaves; the estimates below allow this additive constant. For a fixed bound on the number of exceptional leaves, only finitely many tree–modulus pairs can fail, by the [linear order bound](../large-order/linear.md) at the remaining finitely many moduli.

There is also an integer result. At a fixed core leaf bound $l$, one can complete an $h$-vertex core to consecutive vertex labels and consecutive edge sums with $O_l(h)$ leaves at one chosen site and $O_l(\log(2h))$ at the other, except in the residual caterpillar cases which already work for all populations. Further leaves can be added at either site independently. The two bounds below keep their dependence on $l$ explicit.

## Creating an interval with few leaves at the second site

Mark the two hubs and all vertices of core degree different from two. There are at most $2l$ marks. Shorten each segment of length above twenty to its congruent length in $[9,20]$ modulo twelve. All remaining lengths are unchanged. The short tree has order $b\le40l+1$. Apply the [two-hub interval construction](two-hub-contraction.md) with the designated first site labeled zero and the second one. Its integer intervals are $[L,U]$ for vertices and $[L+1,U]$ for edge sums. Write $W=U-L+1\le N(b)$ for its width, with $N$ as in the cited construction. In the residual caterpillar case no segment was shortened, since a residual hub path has length at most four and all exterior branches are single leaves.

Put
$$
J=100+6\lceil\log_2(3+h+W)\rceil,\qquad D=100\bigl(h+(J+8)(W+1)+1\bigr),\qquad R=16D+4W.
$$
If no segment needs at least $2J$ new vertices, the [simultaneous odd subdivision](two-hub-contraction.md#arbitrary-odd-subdivisions-in-one-stage) on distinct crossing edges gives width at most $100(W+1)(J+1)^2(2l+1)$. Every retained segment requiring expansion contains a crossing edge, as shown there.

Otherwise on a sufficiently long segment choose an edge with $p>0>q$. There is such an edge: outside the short seed the edges cross the partition $(-\infty,0],[1,\infty)$, and at most two edges of the segment can touch zero. On a long hub path at most one seed edge fails to cross; in the short path-and-twig cases an exterior segment meets at most two exceptional twig edges. Each shortened segment has at least nine retained edges.

Subdivide at the chosen edge using the [two-vertex rule](two-hub-contraction.md#keeping-track-of-intervals). This inserts
$$
x=\min(L-p,p+2q-U-1),\qquad y=p+q-x
$$
in path order from $p$ to $q$, completing the vertex interval to $[x,y]$. Repeat on the new edge $y,q$ with the **same negative endpoint** $q$ each time. Stop when the interval contains $[-R,R]$, rounding the number of moves up to a multiple of six.

Only the first move may need padding below $L-p$ at hub one. It costs at most $4W+1$ such leaves. In every move the upper band contains exactly $-q\le W$ leaves at one. Indeed after the first move the new positive endpoint $p$ is larger than the preceding positive endpoint and larger than $-q$. The old sum $L+U$ equals the preceding positive endpoint plus $q$. Hence $L+U+1\le2p+2q$, and the next move has $x=L-p$. Also the first $x\le 2q-1$, since the original $U\ge p$. Every subsequent upper endpoint $2p+q-L$ exceeds $2p$, and the magnitude of the new lower endpoint is at least $p$. Thus at most $\lceil\log_2 R\rceil+8\le J$ moves suffice, including rounding. The inequality follows directly from the displayed definition of $J$ (equivalently $R<2^{J-8}$). The chosen segment supplies all required vertices.

After each move the magnitudes of the new endpoints are within a factor two of each other, since $-x\ge p$ and $y>-q$. Except for the first move, the larger magnitude grows by at most a factor three per move. Before the last group of six moves either the smaller magnitude was below $R$ or the original interval had width $W$. The final width is therefore $O(R+W)$ with an absolute constant. The total population used at one, including the short seed, is at most $(J+8)(W+1)$.

## Turning leaves at zero into internal vertices

The remaining increments on every segment are multiples of twelve. On each segment to be lengthened choose a retained edge different from the one used to create the wide interval. Its endpoint labels $p',q'$ and their sum must be nonzero. Such an edge exists: at most two retained edges on a segment meet the zero vertex, at most one has sum zero since the short seed has distinct edge sums, and at most one was used for the preceding subdivisions. The chosen endpoints are original short-core labels of magnitude at most $W$.

The [neutral twelve-vertex path](../large-order/FlexiblePath.lean) adds exactly the same multiset to the vertex and edge histograms. Use its two parameters $u,4u$ for $1\le u\le D$. In the twelve affine rows all slopes in $u$ are nonzero. Rows of equal slope have intercept differences among $\pm p',\pm q',\pm(p'+q')$, which are nonzero. Forbid every current actual core label and every label of a filler at one. There are at most $h+(J+8)(W+1)$ forbidden values. At most twelve parameter choices per value and 66 additional pairwise equalities are excluded. Some $u$ therefore gives twelve distinct available labels. Each has magnitude below $R$: inspection of the rows bounds the parameter contribution by $5D$ and the endpoint contribution by $2W$ initially, or $5D$ on later insertions inside the edge $u,4u$. These inner endpoints and their sum are always nonzero.

All twelve sites are thus occupied by leaves at zero. Remove those leaves and insert the path. The edge multiset stays unchanged since the removed weights were precisely those labels. Repeat until the original core is reconstructed. We have proved the following sufficient numbers of added leaves in the long-segment case:
$$
O\bigl(h+(J+8)(W+1)\bigr)\text{ at zero},\qquad
(J+8)(W+1)\text{ at one}. \tag{2}
$$
The implicit constant is absolute. The two interval endpoint operations permit every larger pair of populations. For fixed $l$, $W$ is bounded and $J=O_l(\log(2h))$. In the short-segment alternative $h=O_l(1+J)$, so $h$ itself is bounded in terms of $l$. This proves the asymmetric integer result.

## Up to modulus order

It suffices first to label total order $k$, with $h\le k$. Put the larger leaf population at site zero. Under the theorem's leaf bound, $W\le N(40l+1)\le k^{8/1600+o(1)}$, uniformly, and $J=O(\log k)$. In the short-segment case the whole width is $o(k^{1/15})$. In the long case the site-one threshold in (2) is $o(k^{1/15})$, while the threshold at zero is $Ch+o(k)$ for an absolute $C$.

Choose a fixed $\delta>0$ with $C\delta<(1-\delta)/3$. For $h<\delta k$ the larger population is at least $(k-h)/2$ and meets the site-zero threshold. If the smaller population also meets its threshold the interval labeling works. Otherwise the number of leaves away from the larger site is at most $l+o(k^{1/15})\le k^{1/15}$, so the [one-site all-orders theorem](modular-injection.md) applies. For $\delta k\le h\le k$, the [positive-density theorem with several sites](permuted-pools.md) applies, for instance with $\epsilon=1/2$. This proves the order-$k$ assertion. Its extension to all populations while $h\le k$ follows by restriction and Hall's distinct-leaf lemma as in that theorem.

## A prescribed forest at larger core orders

We need the following variant of the positive-density construction. There are $k-1$ free vertices in a rooted forest, each with one incoming edge, including each component root's edge to an arbitrary given external residue. Avoid any one residue $u$ among the free labels. Designate a set of terminal vertices as added leaves, with at most $k^{1-\epsilon}$ different attachment sites in the ordinary forest or prescribed external labels. The ordinary forest has at least $\delta k$ vertices and the number of its components plus its number of terminals is at most $k^{1-\epsilon}$. Then the free labels and the $k-1$ weights can each be made distinct, for sufficiently large $k$.

To verify this variant include the unused vertex $u$ as an isolated dummy in the fixed vertex set $V_0$. Mark the ordinary roots, sites and vertices of degree different from two in their components. The count of segments remains $O(k^{1-\epsilon})$. Prescribe each component root's external edge when assigning that root's label; a parent-before-child greedy order still has only one incoming edge per vertex. The external labels may repeat and may coincide with free labels. Only the free vertex labels are required to be distinct and avoid $u$. The same leaf jump counts now include shifts from external as well as free parents. There are $k$ vertex positions counting the dummy and $k-1$ weights. Consequently the identity $|W_0|=|V_0|+2c-1$, the incidence count on the chains, and the omitted-weight equation (1) of the [permuted-pools proof](permuted-pools.md) all hold unchanged. Its permutation, repairs and four random embedding applications therefore give the assertion. If there are at most one designated leaf, the [prescribed forest lemma](../bounded-degree/excess.md#forest-lemma) applies directly with a smaller exponent, since the component count and degree excess are bounded by the stated counts plus two.

Use strong induction on total order $n$ for the remaining $h>k$. At $n=1\bmod k$ remove a leaf and restore it at the deficient weight. One can remove an added leaf if present; otherwise deleting an original leaf does not increase the core leaf count. Write $t=(n-1)\bmod k$ in all other cases, $1\le t\le k-1$. If there are at least $t$ added leaves, remove $t$ of them and use the [Hall leaf lemma](../counterexample-bound.md#removing-leaves) after induction.

If the total added population is less than $t$, root $H$ at the larger site. Write $m_1$ for the smaller population. Remove all its leaves and a suffix of $t-m_1$ original vertices in parent-before-child order. The larger site survives since $h>k$. Induction labels the remaining connected tree of order $1\bmod k$. Each suffix component attaches along one edge to a known parent, and its ordinary terminals were terminals of $H$, since an entire descendant subtree accompanies a removed vertex. Both the component count and terminal count are at most $l$. The smaller site's own parent label for its leaves is either already fixed or is a free vertex label inside the suffix. Extend an ordinary terminal by a dummy path of $k-1-t$ vertices. The number of ordinary free vertices is now $k-1-m_1\ge(k-1)/2$, since $m_1\le(m_0+m_1)/2<t/2$. Apply the forest variant with fixed density $1/3$, avoiding the one surplus vertex residue. Restrict to the real suffix. Its distinct added labels and weights preserve both balance conditions. This completes the induction.

## Reproduction

The constructor stores filler leaves as integer ranges and removes the actual labels converted to path vertices. The checker reconstructs every original edge and verifies both entire intervals by taking differences at range boundaries. It also checks the suffix decomposition and the moment with a forbidden vertex and external edges. [Constructor](two_hub_buffer.py) · [Independent checks](check_two_hub_buffer.py)

~~~sh
python3 -B -m research.hub.check_two_hub_buffer
python3 -B -m research.hub.check_two_hub_contraction
python3 -B -m research.hub.check_permuted_pools
~~~

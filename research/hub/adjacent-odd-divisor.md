# Two adjacent vertices of unrestricted degree

**Theorem.** Fix $D\ge3$ and an odd integer $d\ge3$. At every sufficiently large multiple $k$ of $d$, every finite tree with two adjacent specified vertices and degree at most $D$ everywhere else is $k$-cordial. There is no condition on the leaf populations, diameter or order.

Write $k=dq$. The [odd-divisor branch theorem](odd-branch-groups.md) covered exterior height at least five, and also two sufficiently large direct leaf populations. The remaining construction uses the exceptional vertex itself as the common boundary of two arms. Its prescribed residue $q$ has order $d$.

## A four-site construction with a fixed boundary

Let the adjacent sites $a,b$ carry $0,p$, where $p=q$. Their edge uses $p$, leaving the vertex label zero as the sole omitted weight. For the moment the rooted exterior forest has bounded order. Suppose at least two exterior children of $b$ themselves have children. In the subtree on the $b$ side choose a deepest vertex with at least two children that have children. Such a vertex exists, possibly $b$. Below it each chain of vertices with children continues through at most one such child. If a chain has at least three vertices with children, take its last three followed by a leaf. Otherwise take two arms, using a child and its unique child with children if present, or one leaf child. This is exactly the path or two-arm configuration of the [four-site construction](universal-hub.md#finding-the-part-to-label-last). The boundary $w$ can now be $b$. Every other descendant of the four sites is one of the additional terminal leaves in that construction.

Withhold the four sites and their additional leaves. Assign all other exterior vertices by the [first-layer walk and increasing-slope procedure](modular-injection.md#stopping-with-at-most-twelve-levels), starting with the two given site labels. In that procedure the label forms are $jX+c$ over $\mathbb Z_k$, with integer slope $j$. The first-layer jumps are the actual external parent labels. The walk decomposes into a simple path and translated cycles, allowing repeated parents of either label. At this point all ordinary forms have positive slope. The outstanding histogram difference, edges minus vertices, is
$$
-[0]-[X]+[L].
$$
Write $s$ for the slope of $L$. It is positive and at least every previously assigned slope. The terminal $L$ is distinct as a form from the assigned labels, even if the last walk has no further layer. If $w$ is an exterior vertex, use the previous positive-slope four-site proof directly.

If $w=b$, use the same three rows with boundary value $p$, now a constant. Their new vertex forms in path or arm order are

| Configuration | Forms |
| --- | --- |
| Forward path | $-p-L,\ L,\ -L,\ -p$ |
| Reverse path | $-p-L,\ -L,\ L,\ -p-2L$ |
| Two arms | $-p-L,\ L,\ -p,\ -L$ |

Direct addition on each actual edge replaces $L$ by zero in the multiset of these four forms. The additional constant $-p$ when present differs from both seed labels because $p\ne0$ and $2p\ne0$. At slope $-s$ the two forms $-L$ and $-p-L$ differ by $p$. There were no earlier negative slopes. Thus the histogram now has just the omitted label $X$.

Pair leaves of the $+L$ parent with leaves of the $-L$ parent as in the original rule. Order the arms so that the $+L$ end has fewer leaves, breaking ties by giving its intermediate vertex at least as many leaf children as the other intermediate vertex. On a path place $+L$ at the less populated of the two middle sites. For an unpaired leaf, give it the current gap minus its parent's label, so its weight fills that gap and its label becomes the new one. Process negative-slope parents first. If there is any unpaired leaf, one such parent has slope at most $-s$. In the two-arm tie case this follows from the ordering of the intermediate vertices whenever there are leaves at $-p$. Unequal end counts leave a leaf at $-L$. In the path tie case remaining leaves lie at $-p-L$. The first new gap consequently has slope greater than $s$, and later negative-slope parents strictly increase it.

The only remaining unpaired leaves can have the constant parent $-p$. If there are $t$ of them, put $r=t\bmod d$. Starting from the latest gap $G$, use $G+p,\ldots,G+rp$ on the first $r$ leaves. They are distinct from $G$ and from each other by the order of $p$. The form $G$ was the sole previously used form of its slope, which exceeds $s$. Handle each full group of $d$ other leaves by a fresh slope $j$ above all earlier slopes and the values $jX+ip$, $0\le i<d$. The edge sums permute each whole group. Finally each reserved pair receives $T,T+L$ at the parents $+L,-L$ with the slope of $T$ above the current maximum. Their weights exchange those labels. This proves the histogram identity as an identity of affine forms.

All forms are distinct, and equal-slope comparisons have already been separated modulo $k$. At bounded residual order the slopes are bounded. Each unequal-slope comparison excludes at most its absolute slope difference choices of $X$, also for composite $k$. Specializing outside these choices produces an injection with exactly one omitted vertex label among its edge sums.

## Reduction to the bounded residual

Remove the direct leaves at $a,b$, writing $h$ for the ordinary order. The [concentration theorem](concentrated-leaves.md) settles $h\ge\delta k$ for any fixed $\delta>0$. At order $k$ in the complementary range name the site with more direct leaves $a$, and write $m_b$ for the smaller population. The existing odd-divisor theorem settles exterior height at least five or $m_b\ge C(D,d)$. Thus every remaining branch has height at most four and $m_b<C(D,d)$.

If $b$ has fewer than two nontrivial exterior branches, its original degree is at most $C(D,d)+2$. In this case the [one-exceptional-degree theorem](one-exceptional-degree.md) applies with a larger fixed degree bound. Otherwise protect two nontrivial branches at $b$. Group the other branches by their attachment site and rooted shape, setting aside groups of $2d$ identical copies. There are boundedly many rooted shapes of height at most four and bounded nonroot degree, so the residual core has bounded order. Include $m_b\bmod d$ of the direct leaves at $b$ in that core.

The preceding four-site proof applies to the residual core. Restore the set-aside groups using the [signed odd-fiber construction](odd-branch-groups.md#a-neutral-group-of-arbitrary-identical-branches), and restore the remaining direct leaves at $b$ in whole fibers. Each operation adds the same fresh set to both histograms. Uniformly these choices are available if $k>K_{D,d}(h+m_b+1)$, which holds for large $k$ upon choosing $\delta$ small enough. The periodic extension at label zero now permits every leaf population at $a$. This settles order $k$.

For $h<\delta k$ and total order below $k$, pad at a site to order $k$ and restrict. Above order $k$ remove one direct leaf if the order is $1\bmod k$ and otherwise remove $(n-1)\bmod k$ direct leaves. There are enough since the surviving order is at least $k>h$. Induct with the two sites fixed and restore the leaf or leaves at their actual parent shifts. This proves the theorem for all orders. [Leaf extension](../counterexample-bound.md#removing-leaves)

## Verification

The independent checker recomputes every vertex and actual edge count. It tests both boundary types, all three four-site rows, complete cycles and partial cycles at the constant parent, and whole trees with many repeated branches. The fixed-boundary identity also works at even parent orders greater than two. The separate repeated-branch step in this theorem uses odd $d$. [Four-site constructor](modular_injection.py) · [Whole-tree constructor](odd_branch_groups.py) · [Independent checker](check_fixed_boundary.py)

~~~sh
python3 -B -m research.hub.check_fixed_boundary
python3 -B -m research.hub.check_odd_branch_groups
python3 -B -m research.hub.check_modular_injection
~~~

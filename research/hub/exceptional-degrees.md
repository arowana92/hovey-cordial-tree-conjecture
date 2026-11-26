# Finitely many counterexamples with a bounded number of exceptional degrees

**Theorem.** For every fixed pair of integers $D,s\ge 0$, there is a $K(D,s)$ such that every finite tree having at most $s$ vertices of degree greater than $D$ is $k$-cordial for every $k\ge K(D,s)$. The exceptional degrees, distances between their vertices, and tree order are unrestricted.

Consequently only finitely many counterexample pairs $(T,k)$ up to isomorphism can occur in each such class. Indeed, at each of the finitely many smaller moduli the [general order bound](../large-order/linear.md) leaves finitely many trees. Along any infinite sequence of distinct counterexample pairs, for **every** fixed $r$ the $r$-th largest degree must tend to infinity, counting absent degrees as zero. This strengthens the [single exceptional vertex result](one-exceptional-degree.md). The threshold here depends on both fixed bounds. The case in which the number of high-degree vertices grows without a prescribed bound remains open.

**Forbidden induced forests.** For each fixed disjoint union $F$ of stars, including isolated vertices, only finitely many counterexample pairs have an $F$-free tree. Write $r$ for the number of stars and $d$ for their largest number of leaves. Among $2r$ vertices of degree at least $d+r$ in a tree, one bipartition class gives $r$ pairwise nonadjacent centers. At each chosen center exclude the first neighbor on the paths to the other centers, at most $r-1$ directions. Choose the desired leaves in the remaining directions. Every such branch attaches to the subtree joining the centers only at its own center, so the chosen vertices induce $F$. The case $r=1$ follows by choosing any $d$ neighbors. Thus an $F$-free tree has boundedly many vertices above a fixed degree threshold and the theorem applies.

## Reduction to disjoint paths

Increase $D$ to at least three. With no high vertices use the [bounded-degree theorem](../bounded-degree/README.md), which uses the embedding lemma of Müyesser and Pokrovskiy. Suppose towards contradiction that counterexamples exist for an unbounded sequence of moduli in our class. The [order reduction and concentration theorem](concentrated-leaves.md) gives counterexamples of **order exactly $k$** in the same class. To see that the fixed count $s$ is preserved, the reduction only varies the leaves at the original high sites when the tree left by deleting those leaves has order less than $k/2$. The other cases are settled by positive ordinary density. Thus only these original sites can exceed $D$ under padding or deletion. Denote the surviving order by $h$. Along the order-$k$ counterexample sequence, $h=o(k)$.

Root each tree at an original high site with the largest direct leaf population. Let $J$ consist of vertices of descendant height at least two. Its number of tips is bounded in terms of $D,s$ by the [depth-three theorem](depth-three-repair.md). Every child of a vertex of $J$ outside $J$ is a leaf or the root of a pendant star with one or more leaf children. The number of such star roots at any single vertex is bounded in a counterexample by the [single-site repair](pendant-stars.md), counting at most $s$ roots with excessive degree separately. If $|J|$ stayed bounded on a subsequence, the number of nonleaf vertices there would stay bounded too. This contradicts [finiteness at bounded nonleaf count](universal-hub.md#cordiality-and-finite-exceptions). So $|J|\to\infty$.

The number of branch vertices and the maximum degree of $J$ are bounded by its tip count (allow one extra neighbor for the parent). Mark its root, tips, branch vertices, original high sites in $J$, and the attachment of each pendant star having a high root. Also mark the vertices having at least two pendant stars, bounded in number by the [distinct-supplier theorem](paired-stars.md). Deleting the marks leaves boundedly many paths. Every remaining position has only its spine neighbors, direct leaves, and at most one pendant star. The degrees of the position and of its possible star root are at most $D$. We take all windows strictly inside these paths.

A window consists of consecutive internal spine positions with all their side decorations. Its two exterior neighbors remain. Compress it to the edge between these neighbors. We choose windows with disjoint interiors and exterior neighbors and compress them all before assigning labels. This operation preserves the original sites, their direct leaf populations and the degree bounds of the remaining vertices.

Pass to a subsequence. If the number of positions with a star is unbounded, choose arbitrarily many disjoint windows with 43 internal vertices and a star at the middle position. Only boundedly many positions are near marked vertices and each chosen window excludes boundedly many further centers. Otherwise remove the boundedly many star positions. An arbitrarily long path with only direct leaves remains. Partition it into separated blocks of 87 internal vertices, allowing two spare vertices between blocks for endpoints. If arbitrarily many blocks have constant leaf count, use those blocks. Otherwise arbitrarily many blocks have nonconstant count. Each of the latter contains a nonconstant subblock of 40 consecutive counts. Below we show how each of these three alternatives supplies a bounded-size repair.

## What a repair must do

In the compressed ordinary tree use the original high sites and apply the [sparse preparation](bare-path-repair.md#keeping-the-surplus-weights-available). Include the leaves at nonzero sites, and count the virtual edges created by compression. It gives an injection with vertex histogram $V$ and actual edge histogram $E$ satisfying
$$
 E-V=-[0]+\sum_{i=1}^e([t_i]-[b_i]),\qquad e\le C.
$$
Here $[x]$ denotes a unit at $x$. Each $t_i$ is nonzero and reserved as an unused vertex label, and $b_i$ is occupied. The root has label zero. For each discrepancy $(b,t)$, restore a bounded group of windows, cancel $[t]-[b]$ and move the omission from $g$ to $g'$. Start at $g=0$. Set aside exactly $C+1$ groups before preparation and use $b=t$ fresh and nonzero for unused groups. Each restored group then changes $E-V$ by
$$
 [b]-[t]+[g]-[g'].
$$

The following placement details apply to all three repairs. A [21-vertex bridge](bare-path-repair.md#a-bridge-giving-a-prescribed-edge-weight) between prescribed endpoints has edge multiset equal to its new vertex multiset plus one prescribed weight. Each of its labels is affine with nonzero slope in its own control parameter. Equal slopes within a bridge have distinct intercepts for fixed endpoints. All chosen endpoints can be required nonzero, including free marks. The zero-endpoint formula works for a fixed zero as well.

In a single simultaneous placement, coefficients and list sizes are bounded solely in terms of $D$. Combine the variables along $(z,Rz,\ldots,R^{d-1}z)$ with integer radix $R$ greater than twice the maximum absolute coordinate difference plus two. Distinct coefficient vectors give distinct integer slopes. The [common palette lemma](bounded-error.md#a-common-set-of-intervals-for-the-direct-leaves) keeps every moving form away from the dense intervals of nonzero-site leaf labels on at least $ck$ parameters. An unwanted equality with nonzero slope costs at most its absolute slope in choices, also for composite $k$. All comparisons against sparse occupied or reserved values therefore cost $O_{D,s}(h+1)$, plus an additive constant depending on the preparation. Choose the common palette for the bounded individual placements first, then its error bound $C$, and finally take $k$ sufficiently large on the subsequence with $h=o(k)$. None of the individual lists or radii used to choose the palette depends on $C$.

For leaves with known parent labels, walking from $x$ to $x+p$ places a leaf at $x$ under parent $p$, contributing $[x+p]-[x]$. We often specify a walk **backwards** by giving its end and subtracting successive parent labels. If its tails repeat, erase simple cycles and translate each cycle to avoid all labels already used, including the residual simple path. This leaves the same histogram difference. A bounded cycle translates with coefficient one, so the same palette and comparison bound apply. We always arrange that the residual tails avoid previously used labels and the new nonleaf labels. [Cycle erasure and placement](pendant-stars.md#one-repair-with-a-moving-omitted-weight)

## Windows centered at stars

One repair uses six pairs of the 43-position windows. In pair $i$, place opposite labels $J_i,-J_i$ on the two middle vertices. Place one pair at a time, keeping both labels fresh, distinct from each other, and $J_1\ne t$. Complete each spine by two 21-vertex bridges. In the left bridge prescribe its middle vertex's label as the extra weight and in the right bridge prescribe the old virtual weight. The two bridges exactly restore the compressed edge and all spine marks in the histogram difference. All spine labels are now fixed.

At the chosen stars under $J_i,-J_i$, place root labels $d_i,d_i+J_i$. The two incoming sums are $d_i+J_i,d_i$. Call the remaining star roots auxiliary and let $P$ be the sum of their spine parent labels. Form an auxiliary walk of these parent jumps from zero to $P$. Erase its cycles and translate them so that all root offsets are distinct and avoid $P$. The residual path is simple and its terminal is excluded from its tails. These offsets are chosen before assigning the common translation below.

Use five independent parameters $A,B,F,U,V$ and take
$$
 (d_1,\ldots,d_6)=(A,B,F,b-t-P-A-B-F,U,V).
$$
In each of the first four pairs distinguish one leaf at the root $d_i$ and give these four leaves the labels $t,t+A,t+A+B+P,b-d_4$. Translate every auxiliary root offset by $t+A+B$. The four leaves and the auxiliary roots form a walk from $t$ to $b$ up to translated cycles. They contribute exactly $[b]-[t]$.

Finish all other leaves backwards from $g$. First use one leaf at $d_5=U$ and one at $d_6=V$, then use every remaining leaf at either selected or auxiliary stars and every direct leaf on the spines. Every subsequent backward tail, including $g'$, has strictly negative coefficients in both $U,V$. Only the roots of pair 5 involve $U$ and only pair 6 involves $V$ among all assigned parents. Each such occurrence has coefficient $+1$. The first tail $g-U$ has a slope different from every assigned label. Thus all tails can avoid all assigned labels before erasure. The two roots of each selected pair are separated by $J_i\ne0$. Among the moving primary leaves only $t+A$ can coincide identically with a selected root, excluded by $t\ne0$ and $J_1\ne t$. The auxiliary offsets avoid the third primary leaf at offset $P$. All other equalities among assigned labels have different slopes or were already excluded. Common sampling and cycle erasure complete the injection.

## Leaf counts that vary along the path

In spine order, the vector of coefficients of a bridge in its own parameter is
$$
 v=(14,14,28,42,-112,70,56,-42,-70,126,-126,72,45,-54,-72,117,-45,-27,-18,-9,-9).
$$
These are the two [arm slope lists](bare-path-repair.md#a-bridge-giving-a-prescribed-edge-weight) multiplied by $14,-9$, with the second reversed. If the 21 leaf counts form a vector $a$, their total parent jump has coefficient $v\cdot a$. Reversing the bridge gives $v^{\rm rev}\cdot a$.

**Forty-position lemma.** Any nonconstant list of 40 integer counts has a consecutive sublist of length 21 and an orientation with nonzero integer coefficient. Form a $40$ by $40$ integer matrix by shifting $v$ and $v^{\rm rev}$ by $j$ positions for $j=0,\ldots,19$, with zeros outside. Order rows first by $j$, then forward before reverse. All rows sum to zero. Delete the first row and last column. This minor has determinant $2\bmod 5$, by the short fraction-free calculation in the [checker](check_decorated_spine.py). Therefore the full matrix has rank 39 over the rationals and its kernel consists precisely of constant vectors. The [Lean proof](DecoratedWindow.lean) independently computes integer linear combinations of the minor's rows, verifies their product with the original matrix, and proves the constant-vector conclusion for arbitrary integer inputs. This test over the integers applies at every sufficiently large modulus, since $D$ bounds all the individual counts and coefficients.

Take four nonconstant 87-position blocks per repair. Two supply oriented 21-position windows with nonzero total coefficient; the other two supply arbitrary 43-position windows. Compress only the selected windows. Restore each of the two 21-position windows with one bridge prescribing its old virtual weight. Use independent parameters $Z_1,Z_2$ there. In the first 43-position window place $t$ in the middle and prescribe $b,w_1$ on its left and right bridges. In the second put a free mark $G$ in the middle and prescribe $g,w_2$, where $w_1,w_2$ are the respective virtual weights. The bare spines have contributed $[b]-[t]+[g]-[G]$ relative to the compressed tree.

Complete all direct leaves backwards from $G$. In each of the first two windows list jumps whose coefficients have the sign of its nonzero total before the opposite-sign jumps. Every nonempty prefix has the sign of that total, since it first increases in that direction and then returns only as far as the nonzero total. Use the first jump from each list, then finish both lists in order, and finish all other leaves. From the second step onwards every tail has nonzero coefficients in both $Z_1,Z_2$. No assigned label has both. The first tail involves $G$ and $Z_1$ together, which also occurs in no assigned spine label. Distinct bridges have their own parameters. The simultaneous placement of the marks, bridges and residual walk thus meets all the avoidance conditions. The leaf contribution $[G]-[g']$ yields the required repair.

## Constant leaf counts

One 87-position window suffices for each repair. Let $m$ be its common direct leaf count. At internal positions 22, 44 and 66 place $t,X,G$ respectively, numbering from one. The four gaps are 21-vertex bridges. Prescribe weights $b,X,g,w$ in order, with $w$ the virtual weight. The bare replacement again contributes $[b]-[t]+[g]-[G]$. If $m=0$, finish with $g'=G$.

For $m>0$ process the leaves backwards from $G$. The first and second bridges use independent parameters $Z_1,Z_2$ and are independent of $G$. Their total coefficients in the leaf jumps are both zero because $\sum v_j=0$. In each bridge, sort its jumps with positive coefficients first. Both signs occur. Every **proper nonempty** prefix then has strictly positive total coefficient. Take one jump from each bridge, do all remaining jumps from them except the last of each, do every leaf from the other bridges and all three middle marks, then take the two held-out jumps in order.

All tails from the second step through the step preceding the two held-out jumps have both guard coefficients nonzero. The first tail involves $Z_1$ and $G$. For the final two tails, the sum of the internal spine labels is
$$
 L=b-t+g-G\pmod k.
$$
Indeed the sum of all bare path weights is twice the sum of its internal labels plus its endpoints, which add to $w$. Take the first moment of the bare replacement histogram. The total of all leaf jumps is $mL$. The new gap is therefore
$$
 g'=G-mL=(m+1)G-m(b-t+g).
$$
Its nonzero $G$-coefficient differs from that of the mark $G$, since $m>0$. It has no bridge parameter and differs in slope from all other spine labels. The penultimate tail is $g'$ plus the last held-out jump from the second bridge. It involves both $G$ and $Z_2$, which again no assigned label does. This proves the avoidance conditions throughout. The same simultaneous placement and cycle erasure give the required histogram.

After all repairs the tree labeled so far satisfies $E=V-[g']$. Give the remaining leaves at zero the complement of the used vertex labels. Each adds its own label as an edge weight. At order $k$ every vertex label occurs once and every edge weight occurs once except $g'$. This contradicts the supposed counterexample sequence and proves the theorem.

## Reproduction

The whole-tree checker independently recovers the spine and every side branch from the expanded parent relation and reads the label on each actual edge. It checks nine order-$k$ trees at $k=262139,262140,262144$, with 2,359,260 endpoint sums, 18 surplus repairs, nine neutral repairs and 245 translated cycles. Cases include zero leaf counts, unequal star arities, and a window where only the reversed guard coefficient is nonzero. The size-independent conclusions use the arguments above. [Constructor](decorated_spine.py) · [Verifier](check_decorated_spine.py)

~~~sh
python3 -B -m research.hub.check_decorated_spine
lean research/hub/DecoratedWindow.lean
~~~

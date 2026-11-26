# Every counterexample has near-linear order

**Theorem.** For every modulus $k\ge2$, every possible counterexample has maximum degree $O(k\log(2k))$ and order $O(k\log^5(2k))$. The constants are absolute. Both bounds apply to **every** counterexample, including at prime moduli.

The [squared-difference refinement](diagonal.md) improves the order bound to $O(k\log^2(2k))$.

The underlying labeling estimate is independent of tree order. Put
$$
D_k=100+288\lceil\log_2(24k+1)\rceil .
$$
Every finite rooted tree $B$ on $b$ vertices admits labels modulo $k$ with root zero and histograms $V,E$ satisfying, for some residue $s$,
$$
E=V-\mathbf e_s,\qquad |V_a-b/k|\le D_k\quad\text{for every residue }a.
$$
In particular, adding **any** $m\ge kD_k$ leaves at **any** one prescribed vertex of **any** tree gives a $k$-cordial tree. The estimate on $B$ allows logarithmic error. Hovey's conjecture asks for pairwise count differences at most one.

## Subdividing edges with controlled multiplicities

Given old endpoint labels $p,q$, insert the following twelve vertices in path order, with two free parameters $u,v$:
$$
u,\ v,\ -u-v,\ p+u,\ -p-q-u-v,\ q+v,
p-v,\ -p-u,\ -q-v,\ q+u+v,\ -u,\ u+v .
$$
Index these entries from 1 to 12 and index the old edge weight $p+q$ by 13. In order along the path the thirteen sums have indices
$$
4,12,11,7,9,8,13,3,5,1,6,2,10.
$$
Thus the changes in the two histograms are identical, for arbitrary endpoints and parameters, including coincidences. These are integer identities. [Lean verification](FlexiblePath.lean)

**Simultaneous subdivision lemma.** Replace any collection of edges by paths, inserting an independently specified multiple of twelve vertices on each. All original labels can be preserved. If the total number of inserted vertices is $N$, their histogram $W$ is exactly the net gain in edge weights, and the choices can achieve
$$
|W_a-N/k|\le96\qquad(a\in\mathbb Z/k).
$$

For a long replacement, insert the next block on the edge between the first two new sites of the preceding block. These are precisely its independent parameters $u,v$. Number the blocks along each chain starting at zero. A site's label depends only on the pair of its own block and possibly on the preceding pair. Every site has a coefficient $+1$ or $-1$ on at least one of its own parameters. Whenever its dependence on a preceding pair is nonconstant, at least one of those coefficients is also $+1$ or $-1$. Both facts follow directly from the list. A uniform pair on either active side therefore gives a uniform residue when the other side is fixed, for composite moduli as well.

First select the pairs at all even indices, then those at all odd indices. Assign each site to the last pair on which it depends in this order. An edge joins consecutive indices, so the order within either step never matters. Any one pair controls at most 24 assigned sites, from its own and the next block. For each pair at a given step the $k^2$ choices give nonnegative histogram columns of mass at most 24. Their mean gives that group's number of sites divided by $k$ in every bin, including after all earlier choices have been fixed. The rounding lemma below selects one column per group with error at most 48 per bin. Apply it at both steps, then telescope the edge identities.

**Rounding lemma.** Suppose each of finitely many groups has finitely many nonnegative columns of $\ell_1$ norm at most $d$, with a convex combination in each group. The sum of the combinations can be rounded to a sum of one column per group, changing each coordinate by at most $2d$.

Keep the group-sum equations on the fractional coefficients. With $f>0$ fractional coefficients there are at most $f/2$ active groups. In addition retain every coordinate equation in which the sum of the entries of the fractional columns exceeds $2d$. There are strictly fewer than $f/2$ such rows since the sum of all entries is at most $fd$ (the case $d=0$ is immediate). There is a nonzero direction preserving all these equations. Move along it until another coefficient becomes zero or one. The fractional support only shrinks. When a coordinate first stops being retained, its remaining coefficients can change it by at most the sum of its remaining entries, at most $2d$. Before that point its value had been preserved. This proves the bound by finite iteration. This is the floating-variable argument with exact group totals. [Beck and Fiala, *Integer-making theorems* (1981)](https://doi.org/10.1016/0166-218X(81)90022-6)

## A recursive histogram bound

First assume $B$ has at most $k$ nonroot terminals. For $b=|B|$ we prove the histogram assertion with bound
$$
3+288\lceil\log_2 b\rceil.
$$
For $b\le3$ use all zeros. For $b\ge4$, peel all nonroot terminals simultaneously for 96 rounds, stopping if just the root remains. Each removed set has size at most $k$, because a newly terminal parent can be charged to a different removed child. In the remaining tree there are at most $b/97$ nonroot terminals. Each such vertex had a descendant path of 96 edges before peeling, and the original descendant subtrees of different remaining terminals are disjoint.

Mark its root and every vertex of undirected degree other than two. For $t$ nonroot terminals there are at most $2t$ segments between marks. Indeed, every other nonroot mark with children has at least two, and the rooted tree has at most $t-1$ branching vertices when $t>0$. Shorten each segment to its unique length in $\{1,\ldots,12\}$ congruent to its original length modulo twelve. The new rooted tree has at most $1+24b/97\le b/2$ vertices and at most $k$ nonroot terminals. If only the root remains the same size bound holds. Apply induction, then restore all segment lengths using the subdivision lemma. This preserves $E=V-\mathbf e_s$ and increases the maximum absolute deviation of a vertex bin from its average by at most 96.

To restore the peeled sets, fill first with temporary leaves at the zero root to reach order $kM+1$, where $M=\max_a V_a$. Choose the target vertex vector $M\mathbf 1+\mathbf e_s$. Every required addition is nonnegative and the edge vector becomes uniform. Restore each peeled set in reverse, padding it with temporary hub leaves to a batch of $k$. At order $1\bmod k$ with uniform edges, Hall's leaf-extension lemma labels the first $k-1$ of the batch with distinct vertices avoiding the surplus residue and distinct edge weights. The last leaf supplies the unique deficient edge residue. Uniform edges and a single surplus vertex are restored after each batch. All actual parents survive their own batch. [Hall's permutation theorem](https://doi.org/10.1090/S0002-9939-1952-0050579-7) · [Leaf-extension proof](../counterexample-bound.md#removing-leaves)

Remove every temporary hub leaf. Each removes the same residue from the two histograms, so they still differ by one unit. In a restored batch of $j$ actual leaves each residue occurs between zero and two times among the actual vertex labels. Its difference from $j/k$ is at most two. The final vertex deviation has therefore grown by at most $96+2\cdot96=288$ since the recursive call. This gives the claimed logarithmic bound.

We can replace dependence on $b$ by dependence on $k$. **Before** the first peeling, shorten every segment as above. The shortened order is at most $24k+1$ because there are at most $k$ nonroot terminals. Use the bound just proved and expand these segments with one more error of at most 96.

Finally allow arbitrarily many terminals. Delete any $k$ simultaneous nonroot terminals repeatedly until fewer than $k$ remain. Label that surviving core as above and pad it temporarily to order $1\bmod k$ with uniform edges. Restore all the deleted batches, now without adding any further temporary leaves. After $j$ restorations the vertex histogram differs from the one before them by $j\mathbf1$ and the difference of two unit vectors. Thus removing the original temporary leaves increases the vertex discrepancy by at most one in total, even if there were many batches. This proves the displayed value of $D_k$ and the exact histogram relation.

## Cordiality and sizes of possible failures

If $m\ge kD_k$, the floor of $(b+m)/k$ is at least every existing vertex count. Fill with $m$ leaves at the zero root to reach balanced vertex counts, choosing $s$ among the high residues when there are any. The edge vector is the same target minus $\mathbf e_s$ and is also balanced.

At a vertex of degree $\Delta$, [protect its star](high-degree.md#preserving-a-connected-subtree-while-removing-leaves) and delete batches outside it. Every labeling of the reduced core extends to the entire tree. At most $k-1$ branches still extend beyond the star, since each such branch has an exterior terminal. At least $\Delta-k+1$ neighbors are now leaves. The preceding result labels the reduced core whenever $\Delta\ge kD_k+k-1$. This proves the maximum-degree bound without any hypothesis on the tree order.

Put $J=\lceil\log_2(2k)\rceil+2$. The [dyadic correction theorem](dyadic.md) already gives cordiality if $n\ge CkJ^5$ and $\Delta\le n/(CJ^2)$. Every counterexample satisfies $\Delta=O(kJ)$ by the new bound. For sufficiently large $n/(kJ^5)$ both sufficient conditions hold. Hence every counterexample has $n=O(kJ^5)$. This contains the order-$k$ regime and leaves the full conjecture open.

## Reproduction

The symbolic audit recomputes the multiset of four-variable coefficient vectors on the actual path. The exact rational rounding program assembles arbitrary nested replacements. An independent check counts the real path edge sums across all endpoint pairs at moduli 2 through 7 and on longer chains. It also reconstructs 48 entire trees, with 616 restored batches and 156 path blocks, including orders where several levels of the construction were exercised using a shorter first peeling cutoff. Lean verifies the integer path identities and the dimension and shrinking inequalities. The group rounding and the recursive theorem have the mathematical proofs above. [Path and rounding code](../large_order_subdivision.py) · [Independent checks](../check_large_order_subdivision.py)

~~~sh
python3 -B -m research.check_large_order_subdivision
lean research/large-order/FlexiblePath.lean
~~~

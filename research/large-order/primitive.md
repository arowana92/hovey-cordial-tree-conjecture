# Every possible counterexample has order at most a constant times k log(2k)

**Theorem.** There is an absolute constant $C$ such that every tree with at least $Ck\log(2k)$ vertices is $k$-cordial. This holds for every positive modulus and arbitrary degrees. The order range still includes the order-$k$ and order-$(k+1)$ instances of the conjecture.

A [later bound](interval-paths.md) replaces the logarithmic factor by its square root.

We use the [squared-switch construction](diagonal.md). Two refinements reduce its total supply requirement. Fine-scale rounding controls the number of labels in every interval. A single integer antiderivative, rounded independently at different scales, turns these estimates into smaller corrections at long strides. We also show how to pool leaves at several high-degree vertices.

## The same label at several prescribed vertices

Let $B$ be a tree and $P$ a nonempty set of $r$ vertices. There is a labeling modulo $k$ that assigns zero to every member of $P$, has $E=V-\mathbf e_g$ for some gap $g$, and satisfies
$$
\max_x |V_x-|B|/k|=O(r+\log(2k)).
$$
Consequently, adjoining a total of $C_0 k(r+\log(2k))$ or more leaves at the vertices of $P$ gives a cordial tree, for any distribution of those leaves. Each added leaf has the same label as its edge weight. Choose balanced target vertex counts at least as large as all old counts, with $g$ high if there is a high bin; these additions realize the target.

Root at a member of $P$ and protect every member. Delete batches of $k$ simultaneous unprotected terminals until fewer than $k$ remain. As in the [single-root proof](flexible-path.md#a-recursive-histogram-bound), expanding these complete batches after padding temporarily at the zero root changes the final discrepancy by at most one in total. Compress each unmarked degree-two path to its congruent length from 1 through 12, marking all pins as well as the root and every vertex of degree different from two. There are at most $k+r$ rooted terminals and at most $2(k+r)+r$ segments. The first compressed tree has order $O(k+r)$, and restoring its paths later costs at most 96 discrepancy.

On the compressed tree peel all unprotected terminals for 96 rounds, or until none remain. Each round contains at most $k$ vertices, since the number of unprotected terminals cannot increase. In the tree that remains, each unprotected terminal had a descendant path of length 96 before peeling: no protected descendant could have disappeared. Their original subtrees were disjoint. At original order $b$ there are therefore at most $b/97+r$ remaining terminals, including the protected ones. Shorten the segments again. The resulting order is at most $1+24b/97+36r$, at most $b/2$ whenever $b>200(r+1)$. Stop at or below that threshold and assign all labels zero. This has the exact gap identity and costs $O(r)$ in discrepancy.

On unwinding, the simultaneous subdivision lemma preserves the pinned vertices. Padded Hall batches restore the peeled leaves with at most two discrepancy per batch and preserve a single gap after removal of all temporary zero-root leaves. Each recursive level thus costs at most 288. There are $O(\log(2k+r))$ levels, giving the assertion for all $r,k$.

## Rounding counts on intervals

Write $J=1+\lceil\log_2(2k)\rceil$. A possible counterexample already has $n=O(kJ^2)$ by the [previous theorem](diagonal.md), so the number of independent low-degree graph layers in that proof is $O(J)$.

Within a single rounding phase, add a row for each aligned interval $[i2^j,(i+1)2^j)$ of residues, for each histogram. Number the residues from 0 to $k-1$, allowing the last interval at each scale to be truncated. An observation in the interval contributes weight $2^{-\lfloor j/2\rfloor}$ to its row. Its total column mass across all scales is at most four. Include the location quota rows of the leaf construction at unit weight. Column mass is still absolutely bounded. The [group rounding lemma](flexible-path.md#subdividing-edges-with-controlled-multiplicities) therefore gives error $O(\sqrt{2^j})$ in the unweighted count on each aligned interval in a phase. Decompose an arbitrary interval of length $t$ into at most two full dyadic intervals of each size up to $t$, using the ordinary partition of the integer line. Summing the geometric series gives error $O(\sqrt t)$.

A uniformly distributed group contributes its number of observations times $t/k$ to the mean. This remains true for translated observations after all earlier layers have been fixed. The planted path triples are exactly uniform in aggregate, separately for each stride and its supply size. The last phase for leaf pairs rounds their histogram and location rows together; an absolute surplus in the requested size of each location quota absorbs its rounding error. Thus the two whole histograms have discrepancy $O(J\sqrt t)$ on every interval. The bounded number of moment changes in the switch proof costs $O(1)$ more. Subtracting from any balanced target costs at most $t$ compared with its constant average. Each correction vector $f$ has zero mass, zero first moment modulo $k$, and satisfies
$$
\left|\sum_{i\in I} f_i\right|\le C_1(t+J\sqrt t)\qquad (|I|=t).
\tag{1}
$$

## One primitive and decaying corrections

Use $D_s=z^s-1$ in the Laurent polynomials, with an exponent denoting a position. Lift $f$ to an integer interval of length $2k$ as in the earlier proof. Specifically, $q=\sum i f_i/k$ is integral. Summation by parts and (1) at prefix lengths at most $k$ give $|q|=O(k+J\sqrt{k})=O(k)$. Write $-q$ as the sum of $k$ integers $u_i$ given by successive differences of $\lfloor-iq/k\rfloor$. They are absolutely bounded. Put $f_i-u_i$ at $i$ and $u_i$ at $i+k$. The resulting $F$ projects to $f$, has ordinary mass and moment zero, and satisfies (1) up to an absolute factor on every interval, with zero extension outside its support.

There is a finitely supported integer polynomial $P$ with $F=D_1^2P$, obtained by summing prefixes twice. For each dyadic $s$ let
$$
U_s^*=z^{1-s}P/s^2,\qquad U_s=\operatorname{round}(U_s^*)
$$
coefficientwise. Let $S$ be the least dyadic stride at least $2k$. For $s<S$ put $w_s=U_s-(1+z^s)^2U_{2s}$ and put $w_S=U_S$. Because $U_1=P$ and $D_{2s}^2=D_s^2(1+z^s)^2$, telescoping gives $F=\sum_s D_s^2 w_s$ exactly over the integers.

Before rounding the difference defining $w_s$ equals $-z^{-s}D_s^2 U_s^*/4$. The coefficients of $D_s^2 U_s^*$ are obtained by convolving $F$ with the centered kernel
$$
z^{1-s}(1+z+\cdots+z^{s-1})^2/s^2 .
$$
This is an average of $s$ interval sums of length $s$, divided by $s$. Bound (1) gives $O(1+J/\sqrt s)$ for its coefficients. Independent rounding changes a coefficient of $w_s$ by at most $5/2$. At the top scale, the twice-summed prefix bound gives $\|P\|_\infty=O(k^2+Jk^{3/2})$, so $\|U_S\|_\infty=O(1+J/\sqrt S)$. Each table is supported in an interval of length $O(k)$ since $S<4k$, and projection to residues adds only a bounded number of entries per bin per scale. We have proved the integer decomposition
$$
f=\sum_s D_s^2 w_s,\qquad \|w_s\|_\infty\le C_2(1+J/\sqrt s).
\tag{2}
$$
In particular the **sum** over strides of the required maximum coefficients is $O(J)$. The proof also shows, without (1), that arbitrary zero-mass, zero-moment data with $\|f\|_\infty\le D$ have all coefficients $O(D+1)$, uniformly in $k$.

## Paying for the switches

Assume a counterexample has $n\ge CkJ$ with $C$ sufficiently large. Use the same path and leaf switches, signs, and moment choices as in the [squared-difference proof](diagonal.md#enough-switches-at-every-required-location). For each dyadic $s$ reserve $R_s=\lceil C_3(1+J/\sqrt{s})\rceil$ switches of each kind and sign at each residue. All constants in (1) and (2) are independent of these supply sizes: the number of graph layers, column masses and moment edits are bounded independently of the numbers planted. The total cost is $O(k\sum_s R_s)=O(kJ)$, including the paired offsets needed for even moduli. When fewer than $n/32$ vertices are leaves, the degree-two sites occupy a positive fraction of the tree, so the path construction fits these supplies.

Otherwise write $L\ge n/32$ for the number of leaves. There are $b=4(1+\log_2 S)$ combinations of stride, sign and histogram. Mark the $b+2$ leaf parents with largest leaf populations, or all if fewer exist. Write $H$ for the total population at these marked parents. If $H\ge L/8$, remove all their leaves, apply the pinned-vertex result to the remainder and add them back. Since $r\le b+2=O(J)$ and $H\ge n/256$, this already gives a cordial labeling for sufficiently large $C$. Orders one and two are immediate, and otherwise none of these parents is itself a leaf.

Suppose $H<L/8$. In each bipartition class, pair leaf parents in order of nonincreasing population and take the smaller population as each pair's capacity. The total paired capacity is at least $(L-H)/2$, since $H$ covers the sum of the two largest class representatives. Assign successive unused parent pairs to each combination until its exact requested number of leaf pairs has been reached, counting the absolute quota surplus in that request. Discard any excess capacity of the last parent pair of each combination. These at most $b$ pairs are disjoint, so the sum of discarded capacities is at most $H$, the total of the largest $b+2$ individual populations. The remaining capacity exceeds $L/4$, whereas the demand is $O(kJ)$. Choosing $C$ large leaves room for all supplies and an unplanted leaf.

Interval rounding now gives (1), the moment adjustments give the hypotheses of (2), and the actual switches in (2) attain both balanced targets. This contradicts a counterexample of order $n\ge CkJ$ and proves the theorem.

## Independent checks

The checker expands each squared difference directly into its three cyclic terms. It covers 1,475 exhaustive vectors and 146 larger ones, up to modulus 16,384, and checks interval group rounding with rational weights. It reconstructs 48 trees with several prescribed zero vertices, including 683 restored batches and 145 twelve-site blocks, and verifies cordiality after distributing the filler leaves among the pins. Twelve whole-tree switch checks use the new coefficients and recount the original edges and vertices at orders up to 69,920. The finite checks exercise the identities; the estimates above prove the unrestricted order theorem. [Primitive construction](../large_order_primitive.py) · [Independent checker](../check_large_order_primitive.py) · [Lean telescoping identity](Primitive.lean)

~~~sh
python3 -B -m research.check_large_order_primitive
lean research/large-order/Primitive.lean
~~~

# Dyadic corrections for every modulus

Write $J=\lceil\log_2(2k)\rceil+2$. All constants in this note are absolute. For every $k\ge2$:

1. Every tree with $n\ge CkJ^5$ vertices and maximum degree $\Delta\le n/(CJ^2)$ is $k$-cordial.
2. A **minimum-order** counterexample has fewer than $CkJ^5$ vertices.
3. **Every** counterexample, even if smaller ones exist, has maximum degree at most $Ck^{3/2}J^{5/2}$ and order at most $Ck^{3/2}J^{9/2}$.

Enlarging the same constant $C$ if needed gives all three conclusions. The argument uses integer differences, independent random labels, and Hall's leaf extension. It gives asymptotic refinements of the [explicit quadratic bounds](quadratic.md). The powers of the logarithm below come from the number of independent displacement pairs that we prepare.

## An integer decomposition with bounded coefficients

Let $D_s=\tau^s-I$ on cyclic integer vectors of length $k$, where $\tau e_x=e_{x+1}$. Let $f$ have zero mass and $\|f\|_\infty\le D$. Then
$$
f=\sum_s D_s h_s,\qquad \|h_s\|_\infty=O(D+J),
$$
where $s$ ranges over the first $J$ powers of two, starting at 1. If also $\sum_x x f_x=0\pmod k$, we can insist that every $h_s$ has zero mass. Applying the unrestricted conclusion once more then gives
$$
f=\sum_{s,t}D_sD_t w_{s,t},\qquad \|w_{s,t}\|_\infty=O(D+J).
$$
All coefficients are integers. The indexing steps can repeat as residues at small moduli.

**Lifting the moment.** For the constrained version put $q=\sum x f_x/k$. Choose integers $u_x$ of sum $-q$ differing by at most one. Since $|q|\le kD$, each has magnitude at most $D+1$. On the integer interval $[0,2k-1]$ put $f_x-u_x$ at $x$ and $u_x$ at $x+k$. Both ordinary mass and ordinary first moment vanish, and projection modulo $k$ recovers $f$. For the unrestricted version use the original interval $[0,k-1]$.

**One splitting step.** In local coordinates let the current vector $v$ have length $m\ge3$ and mass zero. Use zero outside its interval. We will take out $D_1 h$ so the residual $g_i=v_i+h_i-h_{i-1}$, on $[0,m]$, splits into two shorter zero-mass vectors $g_{2j},g_{2j+1}$. Start with the real choice $h_i^*=-v_i/2$. In each parity separately round its successive prefix sums down to integers, and use their differences as $h_i$. Every prefix rounding error has magnitude less than one. The two parity totals of $h$ are $\lfloor-F/2\rfloor,\lfloor F/2\rfloor$ where $F$ is the even total of $v$. Their difference gives zero mass in each residual parity. The rounding changes $g_i^*=(v_i+v_{i-1})/2$ by at most two.

When the ordinary first moment of $v$ vanishes, $F$ is even and $\sum h=0$. We also require zero ordinary first moment in each of the two smaller vectors. Before rounding, the local moment of the even residual is
$$
\sum_j j(v_{2j}+v_{2j-1})/2=\tfrac14\sum_j v_{2j+1}.
$$
Rounding changes it by at most $2(m+1)$: every even-residual prefix error is the difference of two parity prefix errors, its total is zero, and summation by parts applies. Thus the integer moment to cancel has magnitude $O(m(1+\|v\|_\infty))$.

On the $u=\lceil m/2\rceil$ even positions of $h$, in their local coordinates, add a zero-mass integer adjustment of the required moment $z$ and maximum entry magnitude at most $1+|z|/\lfloor u^2/4\rfloor$. Indeed, move the first $r=\lfloor u/2\rfloor$ unit entries to another $r$-subset. The possible moment increases are every integer from zero to $r(u-r)$, by sliding the rightmost entry to its maximum, then the next rightmost, and so on. Reverse signs for decreases and stack such adjustments. This corrects the even moment exactly. The total ordinary moment of $g$ remains zero because $\sum h=0$. Both parity masses are zero, so the odd local moment also vanishes.

**Recursion and bounds.** Apply the same rule in the two parity fibers, doubling the global stride. At length at most two a zero-mass vector of ordinary moment zero vanishes. Without the moment constraint a length-two vector is a single difference. If the old entry bound was $d$, the new bound is at most $(1+C_0/m)d+C_0$. This follows from averaging, the two rounding errors, and the correction just estimated; only one even adjustment contributes at a given residual coordinate. Each local $h$ satisfies the same bound up to an absolute factor. The child length is at most $\lceil(m+1)/2\rceil$. There are $O(\log(2k))$ levels and $\sum 1/m=O(1)$ along each branch (at lengths at least four the ratio is at most $3/4$). Hence all factors $1+C_0/m$ have bounded product, and every entry is $O(D+J)$. The length recurrence gives at most $J$ different strides. At one stride the parity fibers occupy distinct integer positions. Their support is contained in the initial interval enlarged on the right by at most $1+2+\cdots+s$, so each cyclic residue collects only $O(1)$ entries on projection. This proves both versions of the decomposition.

## Supplies on paths of degree-two vertices

An available site consists of five consecutive degree-two vertices. Use the middle three for a specified pattern; the two outer vertices are free buffers. Sites are vertex disjoint. Assume a fixed positive fraction of an $n$-vertex tree can be used as such sites. In this paragraph all constants may depend on that fixed fraction. Then $n\ge CkJ^5$ suffices with **no degree hypothesis**.

Choose a provisional per-bin error allowance $D_0=C_1(\sqrt{nJ/k}+J)$ and take $R=\lceil C_2(D_0+J)\rceil$ copies of each choice below. The constants are chosen in the order $C_1,C_2,C$. There are $O(kJ^2R)$ sites needed, within the available fraction if $C$ is large enough. The two orientations of each operation have separate supplies.

- For a mixed vertex difference start two centers at $x,x+s+t$. Give the first center two neighbors labeled $p=x+z$, and the second two labeled $p-t$, for $z=0,1$. Moving the centers to $x+s,x+t$ exchanges their two pairs of incident weights, and changes the vertex histogram by $-D_sD_t e_x$. Also prepare the reverse orientation at every $x,s,t,z$.
- For a mixed edge difference with steps $s,t$, use two centers initially labeled $a=-x+z$ and $a+s$. Put $p=2x-z$. The first center has neighbors $p,p$ and the second has neighbors $p,p+t$. Swapping centers changes the edge vector by $-D_sD_t e_x$ and preserves the vertex vector. The reverse orientation starts with the center labels swapped. Again prepare every $x$ in both versions $z=0,1$.

Initially the planted vertices and edges internal to the triples each have an exactly uniform histogram. For the first operation all vertex lists are translates of $x$, and internal sums are $2x+z$ or $2x+z+s$. Across $z=0,1$ these are uniform even at even $k$. In the second operation the neighbor lists have the same doubled-coordinate property; every sum is a translate of $x$ and every center list a translate of $-x$.

Leave a further whole block unused for the moment adjustment. Label other vertices independently and uniformly. Free vertices are one list of independent observations. Edges with two free ends form a forest, so their sums are independent uniform residues, by propagation from the root of each component. Edges from a planted triple to a buffer use distinct free vertices and form another such list. A binomial tail estimate and a union bound over $k$ residues and the three lists give a realization with both histograms within $D_0$ per bin of their respective averages. Specifically each list of length $m$ has variance at most $m/k$ in each bin, and the bounded-variable Bernstein estimate gives deviation $O(\sqrt{mJ/k}+J)$ simultaneously. This last calculation uses only independence *within* a list.

Take any balanced target histograms, and let $A,B$ be the moments of the required vertex and edge changes, respectively, modulo $k$. Reserve one degree-two vertex away from the prepared blocks, and choose a leaf. Change their labels by $B-A$ and $2A-B$, respectively. The vertex moment increases by $A$ and the edge moment by $B$, since a vertex of degree $d$ contributes $d$ times its label to the sum of edge weights. These two changes affect only constantly many histogram entries and preserve every prepared operation. Both remaining corrections now have zero mass and zero moment. Their mixed decompositions have maximum coefficient $O(D_0+J)$ and fit their separate supplies. The vertex switches preserve edge counts, and the edge switches preserve vertex counts. This attains both targets.

The same argument works for a tree $B$ with $P$ extra leaves at one specified vertex $v$, with $n$ in this paragraph replaced everywhere by $b=|B|$, provided the path sites lie in $B$ and avoid $v$. Pin $v$ at zero and spread the extra leaves evenly among all residues. Their labels and weights each differ from their own average by at most one. Forest-sum independence on the free part of $B$ still holds with one root pinned; a buffer incident to a planted triple must itself be free, so exclude blocks containing $v$. A leaf for the final moment adjustment can be chosen from the whole tree. With $v$ pinned, an edge from $v$ to a planted triple would require $v$ as a buffer and is excluded.

## Supplies on leaves at different parents

Now assume $L\ge n/32$ leaves and $\Delta\le n/(CJ^2)$. Within each bipartition class, pair the leaf parents in decreasing order of their leaf counts. A pair with counts $a\ge b$ can supply $b$ leaf pairs. Within each sorted list the sum of even-indexed counts is at least half the sum after its largest count. Consequently at least $(L-2\Delta)/2$ leaf pairs are available. No paired parents are adjacent.

For each ordered pair of strides $s,t$, each sign and each of vertex or edge correction, assign a separate set of parent pairs, enough to supply $Rk$ pairs of leaves. Here $R=\lceil C_2(D_0+J)\rceil$ suffices. Take successive pairs up to the desired capacity and discard any surplus of the last pair from this supply. With $O(J^2)$ sets, at most $O(\Delta J^2)$ capacity is lost this way. The demand $O(kJ^2R)$ is a small fraction of $n$ under the stated order bound. With a sufficiently large absolute $C$ the required pairs exist and leave some unplanted leaves. Discarded capacity simply consists of unplanted leaves.

Within each set distribute the sequence $0,1,\ldots,k-1$ repeated $R$ times across the pairs in contiguous portions. Its entry $x$ specifies the following rectangle at two leaves. Draw an independent uniform base $P$ for each parent pair.

- For vertex correction give the parents labels $P,P-t$ and the leaves $x,x+s+t$. Replacing the leaf labels by $x+s,x+t$ swaps their edge weights, changing the vertex vector by $-D_sD_t e_x$.
- For edge correction give the parents labels $P,P+t$ and prescribe **weights** $x,x+s+t$, setting leaf labels by subtraction. Changing the weights to $x+s,x+t$ swaps their vertex labels, changing the edge vector by $-D_sD_t e_x$.

For the opposite sign start with the replacement values and reverse the move. Every set thus has $R$ available moves of its sign at every $x$.

The initially prescribed quantities are uniform over each complete set. At a single parent pair the other quantities (weights in the first construction and labels in the second) form, on each side, a consecutive list shifted by a uniform residue, since $P$ is uniform. If its length is $m$, the count at a given bin is a constant plus a Bernoulli variable with variance at most $m/k$. Distinct pairs are independent. Bounding the two sides separately, each sum of these counts has deviation $O(\sqrt{nJ/k}+J)$ simultaneously across bins, by Bernstein's inequality and a union bound. Pool all pairs of the same kind on each side for this bound.

Other nonleaves get independent uniform labels. The nonleaf vertex observations split into two lists, taking at most one occurrence of each independent variable per list. For edges between nonleaves, identify each paired set of parents, recording its fixed offsets. The resulting loopless multigraph is a union of three forests: any $m$ variables came from at most $2m$ vertices spanning at most $2m-1$ edges, so repeatedly remove a vertex of degree at most three and put its remaining incident edges in different classes. In each class the variable sums are independent and uniform; fixed offsets preserve this. Finally label unplanted leaves independently and uniformly. Conditional on the nonleaves the unplanted leaf weights themselves are independent uniform observations. These finitely many lists give both initial histograms within $D_0$ of uniform per bin, for a large enough absolute $C_1$.

Choose balanced targets so the two needed corrections $a,b$ have equal moments. At least one of $n,n-1$ has a nonzero remainder modulo $k$, and the sums of subsets of that size attain every residue. Change one unplanted leaf label by the common moment. Both residual moments now vanish. Apply the mixed decomposition separately to $a,b$, using their distinct supplies. This proves the leaf case.

## Consequences for unrestricted trees

If $L<n/32$, use the path construction. A tree with $L$ leaves has at least $n-2L$ degree-two vertices in at most $2L$ runs. Partition the runs into blocks of five, keeping at least $(n-10L)/5$ blocks. If $L\ge n/32$, the leaf case applies under the maximum degree hypothesis. Together these prove assertion 1.

A minimum counterexample has fewer than $k$ leaves by [Hall's reduction](../counterexample-bound.md#removing-leaves). Thus if its order were at least $CkJ^5$, the path case would already label it. This proves assertion 2 without a maximum degree restriction.

For assertion 3, apply the [protected star reduction](pruning-depth.md) at a vertex of maximum degree $\Delta$. It gives a core consisting of a rooted tree $B$ with at most $k-1$ nonroot terminals, and at least $\Delta-k+1$ added leaves at its root. If $b=|B|\ge CkJ^5$, the degree-two run estimate in $B$ gives a positive fraction of disjoint sites even after omitting the root and blocks containing it. Use the pinned-root variant of the path construction, then restore the deleted batches. If $b<CkJ^5$, the [depth-pruning lemma](pruning-depth.md) suffices as soon as $\Delta-k+1\ge k(5\lceil\sqrt b\rceil+2)$. Thus a counterexample must have $\Delta=O(k^{3/2}J^{5/2})$. By assertion 1 it must also have $n<CkJ^5$ or $n<C\Delta J^2$, proving the claimed order bound (since $J=O(k)$).

For the concentration estimates, an independent sum of Bernoulli terms with mean $\lambda$ satisfies $\mathbb E\exp(u(X-\lambda))\le\exp(\lambda(e^u-1-u))$, by multiplying the individual bounds $1+p(e^u-1)\le\exp(p(e^u-1))$. Applying this at both signs with $|u|\le1$ and $e^u-1-u\le u^2$ gives a tail of order $\exp[-c\min(t^2/\lambda,t)]$. The random parts of the consecutive lists have total mean at most $n/k$, after subtracting their deterministic full cycles. This justifies the common choice of $D_0$.

## Independent checks

The [integer checker](../large_order_dyadic.py) recombines two differences by direct cyclic subtraction, for 584 exhaustively enumerated small moment-zero vectors and 912 larger random inputs. The [tree checker](../large_order_switches.py) builds separate ordinary trees for the leaf-pair and degree-two constructions. It adjoins an unbalanced part, adjusts the moments, performs the prescribed relabelings and directly counts every original vertex and edge. It verifies twelve complete trees at moduli 5, 6, 8, 9, 10 and 13, reaching 183,488 vertices. The finite checks exercise the algebra and switches. The supply, concentration and order bounds are proved above.

~~~sh
python3 -B -m research.large_order_dyadic
python3 -B -m research.large_order_switches
~~~

Lean 4.14.0 checks the ordinary moment formula for interleaving arbitrary integer lists, the moment shift at the boundary, and both parity mass and moment cancellations after integer floor rounding. This verifies the conservation identities in the splitting step. [Lean source](DyadicSplit.lean)

~~~sh
lean research/large-order/DyadicSplit.lean
~~~

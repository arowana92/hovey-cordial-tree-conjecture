# Arbitrary leaf populations at boundedly many sites, at every tree order

**Theorem.** For every fixed $d$, every tree with at most $d$ distinct neighbors of leaves is $k$-cordial for every sufficiently large $k$ in terms of $d$, uniformly over all tree orders. Consequently every sequence of counterexamples with $k$ tending to infinity would require the number of distinct neighbors of leaves to tend to infinity.

We prove the following form. Fix integers $l,s\ge1$. For all sufficiently large $k$ in terms of $l,s$, take any finite tree $H$ with at most $l$ leaves, choose at most $s$ of its vertices, and add any nonnegative number of leaves at each chosen vertex. The resulting tree is $k$-cordial. Both tree orders, all branch lengths, all positions of the chosen sites and all leaf populations are unrestricted.

Equivalently one may allow any tree with all but at most $l$ leaves adjacent to at most $s$ chosen vertices. Remove the direct leaves except for chosen sites themselves. At most $s$ surviving sites become new core leaves, which changes the fixed bound by at most $s$. In particular choose all neighbors of leaves as sites, so there are no exceptional leaves and the remaining core has at most $d$ leaves. The trees of order one and two are immediate. Conversely the displayed two-parameter class has at most $l+s$ distinct neighbors of leaves. At order at least three, the number of distinct neighbors of leaves also equals the maximum number of pairwise vertex-disjoint pendant edges: choose one leaf at each such neighbor. For each fixed $l,s$, only finitely many tree–modulus pairs in this class can fail: for each of the finitely many remaining moduli the [unrestricted linear order theorem](../large-order/linear.md) bounds every counterexample's order. The threshold in this theorem is asymptotic. The [polynomial marked-site theorem](polynomial-marked.md) allows up to $k^\alpha$ exceptional leaves for every fixed $s$ and every $0<\alpha<1/6$.

## The sparse case left by the earlier reductions

Write $h=|H|$. The [positive-density theorem and its large-core extension](marked-subdivision.md#a-positive-density-core-at-every-order) cover all $h\ge\delta k$ for each fixed $\delta>0$ with arbitrary populations, since a largest site receives at least $1/s$ of the total. It suffices for now to prove the assertion at total order $k$. Suppose there were counterexamples of this order at $k\to\infty$. Then $h=o(k)$. Order the positive populations $m_1\ge\cdots\ge m_r$, passing to a subsequence of fixed $r\le s$. With at most one population the [one-site all-orders theorem](modular-injection.md) applies. Otherwise the [linear second-population theorem](marked-subdivision.md) gives $m_2=O_{l,s}(h)$, since its large-population regime is already super edge-magic. Thus
$$
m_1=k-O_{l,s}(h),\qquad m_1/(h+1)\longrightarrow\infty .
$$

After a further subsequence each of the finitely many ratios $m_i/\log(2h)$ either tends to infinity or is bounded. If $m_2=O(\log(2h))$, all but $l+O_s(\log(2h))$ original or added leaves lie at the largest site. The one-site theorem applies, since this exceptional count is at most $k^{1/15}$ for large $k$. Otherwise choose $j\ge2$ maximal with $m_j/\log(2h)\to\infty$. Then $h\to\infty$ and the counts after $j$ sum to $O(\log(2h))$. The following construction gives a contradiction by realizing the full interval labeling.

## Fixing the site labels before elongating the branches

Include every site among the endpoints used to split $H$ into segments, together with all vertices of degree different from two. Their number is bounded in terms of $l,s$. For $j\ge3$ designate a longest segment. For each other segment of length above twenty retain a length in $[9,20]$ congruent to the true length modulo twelve. On the longest retain a length in $[9,20]$ congruent to its true length minus two modulo twelve. Since $h\to\infty$ this segment has length $\Omega_{l,s}(h)$. The short cores and all choices of marks form a finite family.

Use the [marked seed theorem](marked-leaf-threshold.md#covering-the-three--and-four-site-geometries) on the short core, with only the first $j$ sites eligible to supply filler leaves. It gives a bounded interval seed with site labels $f_i$ and
$$
\min(W,M-W)\ge\eta m_j,\qquad W=\sum_{i\le j} f_i m_i,\qquad M=\sum_{i\le j}m_i
$$
for a uniform $\eta>0$. Each seed has available parents $-1,0,2$ or $-a,0,1,b$ as in that theorem. Since $W=f_1m_1+O(h)$, $0\le W\le M=m_1+O(h)$ and $m_1/(h+1)\to\infty$, the integer $f_1$ is zero or one. If it is one, reflect the labels by $x\mapsto1-x$. The reflected sums are $2-y$, and the two slacks exchange places. Reflection of a quadruple gives another allowed quadruple. Reflection of the triple gives $-1,1,2$, and the largest site now supplies zero, so the available parents include the quadruple $-1,0,1,2$. Thus the largest site is at zero, all available parents are among the first $j$ sites, and all $f_i$ remain bounded. Write $W,M$ for the oriented quantities from now on.

Choose one retained edge on the longest segment and orient its endpoints $d,e$ with $d\ne0$. Spend the two reserved vertices to prepare a strictly negative and a strictly positive endpoint. Use a sufficiently low child $q$ at $d$ and an upper child $p=d+e-q$ at $e$, and replace the original edge by the connection $q,p$. Choose $q<-|d|-1$ and $p>0$. The further edge $d,q$ is eligible for later neutral subdivisions. These positions are feasible by the [marked upper and lower insertion rules](marked-leaf-threshold.md#integer-intervals-and-three-available-parent-labels). There are finitely many starting seeds, so all labels at this stage have bounded magnitude. The other segments of length at least nine each have an edge with nonzero endpoints and nonzero sum: at most two edges on a path touch zero, and at most one weighs zero.

## A wide interval with few leaves away from zero

Write $[L,U]$, $[L+1,U]$ for the current vertex and weight intervals. Fix the negative endpoint $q$. Fix an upper insertion block for a child at $q$; let its length be $b$, its child slot $i\in[0,b-1]$, and put $e'=b-1-i$. All its other parents are among the available anchors and the block is fixed throughout. The interval can be extended freely at the upper end by leaves at zero.

On an edge with positive endpoint $p$ and fixed negative endpoint $q$ put
$$
x=L-p,\qquad y=p+q-x .
$$
Give $p$ its new child $x$ and fill $[x+1,L)$ with leaves at zero. Their sums, together with $p+x=L$, form exactly $[x+1,L]$. Put the upper block at start $y-i$, filling the gap from $U+1$ through $y-i-1$ with leaves at zero, and make $y$ the required child at $q$. Replace the old edge $p,q$ by $x,y$, retaining the two new child edges. Its sum is still $p+q$. The new intervals are $[x,y+e']$ and $[x+1,y+e']$. This uses at most $b-1$ leaves away from zero. Lean checks that the lower rotation, upper padding and upper permutation together give a bijection onto exactly the new weights. It also checks the restored middle sum and the inequalities for the next move. [Formal band and recurrence lemmas](MarkedBuffer.lean)

For the first move only, pad the lower end sufficiently to ensure $x\le q-b-2$ and $y-i>U$. Such padding is bounded on the finite seed family (take at least two extra positions if using triple padding). Repeat on the positive endpoint $y$ and the **same** negative endpoint $q$. Now the next lower value is $x'=x-y<x$. The next upper child satisfies $y'=2y+q-x>2y$, and $y'-(y+e')=y+q-x-e'>i$. Hence upper insertion remains feasible forever. The negative magnitude after the next move is at least $y$. Conversely each move multiplies $\max(|L|,U,1)$ by at most three plus a bounded additive cost, directly from the formulas.

Let $I$ be the current number of filler leaves away from zero, and $W_0$ a bound on all original magnitudes after the initial padding and preparation. Stop after a positive multiple of six moves when
$$
\min(-L,U)\ge16D+4W_0,\qquad D=100(h+I+1).
$$
After $t$ moves $I=O(1+t)$, and both endpoint magnitudes grow at least exponentially after the first two moves. Thus stopping takes $O(\log(2h))$ moves. The final width is $O(h)$ as well: after the first move $-x\ge p$, $y=-x+p+q$, and $x\le q-b-2$ gives $-x\le y+|q|\le 2(-x)+|q|$. The magnitudes of the two ends are within a fixed factor plus a fixed constant. Six moves before first stopping, the smaller magnitude was below $O(h+\log(2h))$, or the starting seed was bounded. The upper growth bound for six steps gives the claim. All implied constants in this section depend only on the finite seed family. There is space on the longest segment for the preparation and these subdivisions because its length is $\Omega(h)$.

The remaining increments are all multiples of twelve. On the distinguished segment use the eligible edge $d,q$ and on every other enlarged segment use its eligible short-core edge. In the [neutral twelve-vertex path](../large-order/FlexiblePath.lean) use parameters $u,4u$ with $1\le u\le D$. Forbid all current original-vertex labels, at most $h$, and all $I$ leaves at nonzero parents. At most $12(h+I)+66<D$ choices are excluded by collisions with these labels and among the affine rows. The first endpoints are bounded by $W_0$, and on later insertions are $u,4u$ from the preceding step; hence the row magnitudes are below $16D+4W_0$. They occupy leaves at zero. Replace those leaves by the new internal vertices, whose increase to the edge multiset is precisely their own labels. Iterate until all lengths are correct. This leaves all site labels fixed, completes the integer intervals, and consumes $O(h)$ leaves at zero and **only $O(\log(2h))$ leaves in total away from zero**.

## Paying the sites and passing from order k to every order

At $j\ge3$, deduct the seed leaves and include the remaining small populations. Nonzero site labels are bounded and every omitted population after $j$ totals only $O(\log(2h))$ together. Thus the remaining parent-label sum is at least $\eta m_j-O(\log(2h))\to\infty$. It is also $O(h)$, since $f_1=0$ and $m_2=O(h)$. The remaining mass is at least $m_1-O(h)$, so the upper slack tends to infinity too. Every available anchor retains arbitrarily many leaves, because each nonzero anchor started with at least $m_j$ and zero started with $m_1$. The [exact population block lemma](marked-leaf-threshold.md#realizing-the-exact-leaf-populations), with the bounded site labels as its support, finishes the desired labeling.

At $j=2$, put one leaf at every positive site into the ordinary core first. Shorten segments while marking every site. Apply the [two-site asymmetric construction](two-hub-all-orders.md) at the first two sites, oriented as zero and one. With the fixed bounds on sites and core leaves its cost is $O(h)$ at zero and $O(\log(2h))$ at one. Every smaller site's label is bounded, since each was retained on the finite short core. In the alternative in which no segment can fund the buffer, $h=O_{l,s}(1+\log(2h))$, inapplicable along $h\to\infty$. In a residual caterpillar all sites are now nonleaves and all further distributions preserve the caterpillar. Otherwise the remaining moment is $m_2+O(\log(2h))\to\infty$ and the remaining mass minus this moment is $m_1-O(h)\to\infty$. The zero-and-one exact completion applies, again with bounded site-label support. This finishes the contradiction at order $k$.

For $h\le k$ and lower total order, pad to order $k$ by temporary leaves and restrict the injective labeling; both labels and weights remain distinct. With higher total order induct, removing one added leaf at orders $1\bmod k$ and otherwise removing $t=(n-1)\bmod k$ added leaves. There are enough since $h\le k$. In the first case restore the deficient weight; in the second apply [Hall's distinct-leaf lemma](../counterexample-bound.md#removing-leaves) to the specified parents avoiding the surplus vertex residue. A tree without sites can be regarded as having one site of population zero. Finally for $h>k$ the [positive-density extension](marked-subdivision.md#a-positive-density-core-at-every-order) applies directly. This proves the theorem.

## Reproduction

The checker recovers all original edges and specified lengths by walking through the subdivided graph. It computes the entire vertex and edge frequency functions by range boundaries and checks every requested leaf population by decoding the remaining permutation blocks. Its 21 cases include triple and quadruple padding, both orientations, a largest core of order 24,010 and one interval with 986,431,713 positions. The proof of the asymptotic threshold uses the preceding estimates and the linked embedding theorems. [Asymmetric constructor](dominant_marked.py) · [Independent topology, interval and population checks](check_dominant_marked.py)

~~~sh
python3 -B -m research.hub.check_dominant_marked
python3 -B -m research.hub.check_marked_subdivision
python3 -B -m research.hub.check_permuted_pools
lean research/hub/MarkedBuffer.lean
~~~

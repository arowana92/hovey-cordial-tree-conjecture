# A 66-period test for every modulus

**Theorem.** At each fixed positive modulus $k$, it suffices to check the trees of order **strictly below $66k$** to decide $k$-cordiality of all finite trees. Every tree on more than $66k$ vertices with at most $k+1$ leaves is $k$-cordial. Independently of its degrees and leaf count, **every tree containing a path on $66k+1$ vertices is $k$-cordial**. Branches may occur at every vertex of that path.

There is also a prescribed-root conclusion. In the few-leaf theorem one may choose a leaf or branching vertex as root. Its label can be zero, with balanced vertex and edge histograms satisfying $E=V-\mathbf e_s$ for some $s$. Any number of further leaves at that root then extends the same labeling. With at most $k$ original leaves the root can be any vertex, including a degree-two vertex. These prescribed-label assertions use $k\ge5$.

The decision bound improves the [three-pool test at $2^{26}k$](hall-pools.md). It bounds a **smallest** counterexample. The [bound applying directly to every counterexample](linear.md) has a larger constant. The modulus still ranges over infinitely many integers.

## Packing blocks on the tree

Take $k\ge5$. Pin all $h$ vertices of degree different from two. Include the chosen root as an additional pin if necessary. The tree on the pins after suppressing the other degree-two vertices has $h-1$ edges. Its open segments contain all other vertices. The degree sum gives $h\le2k$ in the stated few-leaf cases. Label the pins by their consecutive breadth-first ranks modulo $k$, with the root first and siblings consecutive. Their vertex counts deviate from their mean by less than one. The actual edges from pin to pin form a subset of the skeleton edges. Their integer rank sums strictly increase in child order and belong to $[1,2h-3]$, so each weight occurs at most four times there.

Inside a segment, reserve a block with $r$ adjustable centers in alternating order
$$
 p,\ t_0,\ p+d,\ t_1,\ p+2d,\ldots,t_{r-1},\ p+rd .
$$
Keep a free buffer before the first block on each segment and after every block. The stride consumed by a block is $w=2r+2$. For each ordinary block size in the following table use **one block for each starting residue $p$**. Here $V$ means a pool adjusting vertex counts, and $H,G$ are pools adjusting edges. Take $d=0$ for $V,H$ and $d=1$ for $G$.

| Centers $r$ | Pool | Number of blocks | Cumulative stride |
| ---: | :--- | ---: | ---: |
| 9 | $H$ | $k$ | $20k$ |
| 4 | $V$ | $k$ | $30k$ |
| 3 | $V$ | $2k$ | $46k$ |
| 2 | $G$ | $k$ | $52k$ |
| 1 | $H$ | $k$ | $56k$ |
| 1 | two special triples | 2 | $56k+8$ |

Place the blocks in this order, using any segment with room. If a stride $w$ fails, each segment has at most $w$ unconsumed vertices including its initial or current buffer. If $U$ is the cumulative stride through that size, the already used stride is at most $U-w$. Hence
$$
 n\le h+(U-w)+w(h-1).
$$
At $h\le2k$ the five possible strides give $n\le66k$. At $h\le2k-2$ the inequality is strict. This calculation is verified in [Lean](ShortPools.lean). Paths themselves also satisfy the construction when long enough.

## A balanced starting point for the repairs

The left anchor of each center occurs $10,10,2$ times per residue in the three respective pools. The entire set of anchors in each ordinary block family is uniform because $p$ runs over all residues. Write $\lambda$ for the multiplicity of a pool. Give its centers labels $t$ so that both $t$ and the first incident weights $p+t$ are uniform. This follows from the [permutation lemma](hall-pools.md#permutations-for-a-prescribed-multiset) since $\lambda$ is even. The other incident weights are translates by $d$. These blocks are initially uniform separately on their vertices and internal edges. Here and below $p$ in the formula for an individual center means its actual left neighbor.

Give the two special triples labels $(2,-1,2)$ and $(2,-2,3)$. Together they add at most three vertices and at most three edges to any bin at $k\ge5$. Swapping their centers changes the edge vector by $D=\mathbf e_0-2\mathbf e_1+\mathbf e_2$, with no change to vertex counts.

All unassigned vertices lie in open paths between fixed vertices. On odd positions numbered from zero, each vertex has at most one fixed neighbor. The [one-neighbor construction](../census/euler-subdivision.md#a-bound-independent-of-the-original-order) gives an upper bound of its stage average plus one in **both** histograms. Indeed zero-sum full blocks are uniform, and each residual partial block contributes at most one to a bin; two partial blocks require at least $k$ remaining sites. Sites with no fixed neighbor can fill least-used vertex bins. On the remaining even positions the weighted group rounding from the same proof gives upper discrepancies four for vertices and eight for edges. This also counts buffer edges. Thus the initial vertex maximum is at most $n/k+9$, and the edge maximum is at most $(n-1)/k+16$. The estimates only use upper discrepancies.

Let $M(a)=\sum_i ia_i$ modulo $k$, and $s=M(V)-M(E)$. Choose a balanced vertex target with $s$ among its high bins whenever it has any. The edge target is that vector minus $\mathbf e_s$ and is balanced. Change an original leaf other than the prescribed root by the common moment change needed at the two targets. This changes one vertex and one edge and leaves every ordinary anchor and center available. The remaining vertex and edge corrections $v,f$ have mass and moment zero. By integrality and the two upper bounds, $v_i\ge-10$, $f_i\ge-17$.

## A cyclic edge decomposition with small negative coefficients

For any such $f$ there are $\epsilon\in\{0,1\}$ and integer vectors $h',g$ of mass and moment zero modulo $k$ (mass exactly zero) such that
$$
 f_i=\epsilon D_i+2h'_i+g_i+g_{i-1},\qquad
 g_i\ge-2,\quad g_i+g_{i-1}\le3,\quad
 2h'_i\ge\min f-4 .
$$
Use representatives $0,\ldots,k-1$. Write $J(a)=\sum_i ia_i$ as an ordinary integer. First solve $r_i+r_{i-1}=f_i\pmod2$ in bits around the cycle. There are two solutions, since $f$ has even total. At odd $k$ take the one of even cardinality and set $\epsilon=0$. At even $k$ require $r_{k-1}=J(f)/k\pmod2$. The support is even because $J(f)\equiv\sum_i r_i\pmod2$. If its ordinary moment is odd, toggle $r_0,r_1$ and set $\epsilon=1$. This makes the moment even, leaves the boundary bit fixed and changes the parity equations to those of $f-\epsilon D$.

Give the sorted support alternating signs $+1,-1$. The resulting $g^0$ has mass zero and $g^0_i+g^0_{i-1}\le1$, including at the wrap. Solve $2d=-J(g^0)\pmod k$, possible by the parity adjustment. Choose any $x$ with $g^0_x\ge0$ and put $g=g^0-2\mathbf e_x+2\mathbf e_{x+d}$. This gives the asserted bounds, preserves parity, and sets the moment to zero. The displayed formula now defines integral $h'$ with mass zero. At odd $k$, doubling its moment is zero modulo $k$ and so is the moment. At even $k$,
$$
 2J(h')=J(f)-2J(g)+kg_{k-1}.
$$
The chosen boundary bit makes this divisible by $2k$. Finally $\epsilon D_i\le1$ gives the stated lower bound on $h'_i$.

## Finishing the labeling

Use the special swap precisely when $\epsilon=1$. In the first pool keep the first edge weights uniform and prescribe center multiplicities $10\mathbf1+v$. To do this, realize the prescribed list of centers as sums of uniform lists $-p$ and $p+t$. In the second pool keep centers uniform and prescribe $p+t$ with multiplicities $10\mathbf1+h'$. This adds $2h'$ to the initial edge counts. In the last pool prescribe $2\mathbf1+g$ in the same way and get $g_i+g_{i-1}$ at weight $i$. All requested multisets have nonnegative multiplicities, size divisible by $k$, and sum zero. Indeed $h'_i\ge\lceil(-17-4)/2\rceil=-10$. Each multiset is realized by partition into zero-sum $k$-blocks and Hall's permutation theorem on each block. The anchors do not change. This yields the prescribed balanced counts. [Erdős–Ginzburg–Ziv (1961)](https://www.renyi.hu/~p_erdos/1961-25.pdf) · [Marshall Hall Jr. (1952)](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

At the zero root, each further leaf adds its own label to both histograms, preserving the one-unit difference. Choose a least-used vertex bin, taking $s$ first whenever vertex counts become uniform. Both histograms stay balanced after every leaf.

A smallest counterexample has fewer than $k$ leaves by [deletion and restoration](../counterexample-bound.md#removing-leaves), hence $h\le2k-2$ with no extra root pin. Its order must be strictly below $66k$. For the path conclusion, [protect the given path while deleting leaf batches](high-degree.md#preserving-a-connected-subtree-while-removing-leaves). The resulting tree has at most $k-1$ leaves outside the path, and only its two endpoints can be leaves on the path. It has more than $66k$ vertices, so our construction labels it. The deleted batches extend its labeling to the whole tree. The ordinary assertions at the four smallest moduli follow from the known all-tree theorems.

## Reproduction

The [constructor](../large_order_short_pools.py) works on actual rooted parent arrays and uses exact rational rounding. The [checker](../check_large_order_short_pools.py) tests the coefficient identity, bounds and both moments directly on 1,060 vectors, including 175 square corrections. It recounts all 9,570 vertices and all actual edges of 18 trees with concentrated, dispersed and randomly distributed degree-two vertices, and checks repeated leaf extensions at the specified root. The finite tests exercise the formulas; the proof and the packing inequalities supply the universal quantifiers.

~~~sh
python3 -B -m research.check_large_order_short_pools
python3 -B -m research.census.check_euler_subdivision
lean research/large-order/ShortPools.lean
~~~

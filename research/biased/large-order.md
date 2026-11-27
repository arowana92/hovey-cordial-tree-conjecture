# A near-quadratic order bound with arbitrary edge offsets

**Theorem.** There is an absolute $C$ such that, for every $k\ge2$, every tree on at least $Ck^2\log^3(2k)$ vertices is cordial modulo $k$ for **every assignment of independent additive edge offsets**. The vertex labels are freely chosen and edge $uv$ has weight $f(u)+f(v)+b_{uv}$. This includes composite moduli, where explicit offset assignments can fail at order $k$. Consequently each fixed modulus has only finitely many offset-decorated counterexamples, even if the edges may use the whole group. [Small composite obstructions](prime-powers.md)

The known linear bound in this repository concerns ordinary sums. Here large degree can bring many different offsets even on the leaves of one star. The proof uses two effective leaf shifts at a time, including shifts whose difference generates only a proper subgroup. All implied constants below are absolute.

## The number of nonleaf vertices

We first establish that every counterexample has fewer than $2^{40}k$ nonleaf vertices. We give the changes needed in the [ordinary degree-two and leaf pool proof](../large-order/hall-pools.md).

On a degree-two site with five consecutive degree-two vertices, let $b_L,b_R$ be the offsets of the two edges at its center. Choose a parameter $p$ and give its left and right neighbors actual labels $p-b_L,p+d-b_R$. The two weights at center label $t$ are then $p+t,p+d+t$. In each of the three collections of the ordinary proof use $(\lambda+6)k$ sites. Choose each site's parameter fractionally uniformly, charging one observation in each of three histograms for $p,p-b_L,p+d-b_R$. Each option has column mass three. The [group rounding lemma](../large-order/flexible-path.md#subdividing-edges-with-controlled-multiplicities) makes every bin differ from $\lambda+6$ by at most six in each histogram. Reserve exactly $\lambda$ sites at each $p$. Keep **all** these neighbor labels, including those of surplus sites. Give the surplus centers labels by another application of the same rounding bound to their vertex and two edge observations. Their per-bin discrepancies from their own averages are at most six. The reserved centers and their two weights are initially uniform by the Hall construction with $\lambda$ even. Across all three collections, all the fixed contributions therefore differ from their bin averages by at most $3(6+6+6)=54$. At the two exceptional sites subtract the incident offsets from the prescribed neighbor values as above. Their center swap makes exactly the original weight correction.

Each edge at a free vertex still contributes a translate of its candidate label, so the low-degree independent-layer rounding bounds are unchanged. Changing a spare degree-two label and a leaf label changes the two first moments by the same degree formulas as before. The bin discrepancies to correct are bounded by $D_0=\lceil3000(1+\log(2+n/k))\rceil$, including the additional 54. Use the smallest even $\lambda\ge4(D_0+10)$. The two-permutation and cyclic decomposition steps now apply on the reserved sites with the actual, biased edge weights. For $x=n/k\ge2^{30}$, $3(\lambda+6)+3<x/8$, by substitution at the endpoint and monotonicity of the difference thereafter. With fewer than $n/32$ leaves there are at least $(n-10L)/5>n/8$ disjoint five-vertex sites. This proves the large-order path-site assertion with arbitrary offsets.

The separate many-leaf-parents argument in the same proof also holds. At each distinct leaf parent designate one actual leaf edge and use the extra histogram observation $f(u)+b_e$ in place of $f(u)$. This is again one translated observation. It supplies the two uniform lists of effective shifts for the selected leaves. The ordinary rounding of all other leaf labels and the single spare leaf moment change remain valid. Thus $30000k(1+\log(2+n/k))$ distinct leaf parents suffice when $n\ge k$.

For clarity, let $H$ be the connected subtree of all $h$ nonleaf vertices and suppose $h\ge2^{40}k$. [Protected leaf deletion](../large-order/high-degree.md#preserving-a-connected-subtree-while-removing-leaves) works with offsets because restoring each leaf uses its parent label plus its actual offset as its displacement in Hall’s theorem. If $H$ has at most $h/64$ leaves, protect $H$. The resulting core has fewer than $k$ leaves outside $H$, hence fewer than a $1/32$ fraction of leaves, and the path-site assertion applies. Otherwise protect $H$ and one exterior leaf at each leaf of $H$. The core then has order at most $2h+k$ and more than $h/64$ distinct leaf parents. For $h/k\ge2^{40}$ this exceeds $30000k(1+\log(3+2h/k))$. In both cases reverse the deletions. This proves the asserted nonleaf bound.

## Completing a core with two leaf shifts

In the rest suppose $h<2^{40}k$. The cases of at most two total vertices are immediate. Put $H$ in parent order and label its vertices. An effective shift at a leaf is the parent label plus that leaf's offset. We may subtract a common constant from every edge offset, which translates all final edge weights. Work with effective shifts $0,d$, $d\ne0$. Write $g=\gcd(k,d)$ and $m=k/g$. The cycles of addition by $d$ are the $g$ residue classes modulo $g$, with $m$ positions in each.

Write $V,E$ for the two core histograms. Suppose that on summing each by cycle their difference is a single positive unit, on a cycle $C_*$. Suppose also that on every initial segment of each cycle in $d$-order, both histograms differ by at most $D$ from the linear interpolation of their own cycle totals. Either histogram has at most $h$ entries on one cycle. **At least**
$$
K(m)=k\big(\lceil h/m\rceil+6D+12\big)
$$
**available leaves of each of the two effective shifts suffice to complete the tree**, regardless of the offsets of the other leaves. We take $D$ to be a positive integer.

Use $j=(1-h)\bmod k$ spare leaves of shift zero and assign them distinct labels. Write $V',E'$ for the new counts. Then $V'-E'=V-E$ and $h+j=sk+1$. Index a cycle by $i=0,\ldots,m-1$, starting at the representative $r\in[0,g-1]$ and advancing by $d$. Choose $w\in C_*$ at index $\sum_{r,i}i(V-E)_{r+id}\bmod m$. Put $z=V-E-\mathbf e_w$. Every cycle has zero total $z$, and the sum of the index moments on the cycles is divisible by $m$.

There is a zero-total integer vector $J$ satisfying $(\tau^d-I)J=z$ and $\|J\|_\infty\le4D+4$, where $\tau$ shifts a histogram by one. On each cycle take the negatives of the successive prefixes of $z$. The last prefix is zero, so the cyclic difference is $z$. Each prefix has absolute value at most $2D+1$: the linear interpolation of $V-E$ there is zero or a fraction of one, and subtracting the single unit costs at most one relative to this interpolation. Summing the negative prefixes on a cycle gives its index moment modulo $m$. Add a constant on each cycle to place its mean in $[0,1)$. The total is then a multiple $jm$ with $0\le j<g$. Subtract one everywhere on any $j$ cycles. The total is zero, the differences are preserved, and the bound follows.

Put $a=s\mathbf1+\mathbf e_w-V'$. Take $\lambda=\lceil h/m\rceil+6D+10$. At shift zero give the leaves multiplicities $\lambda\mathbf1+a-J$. At shift $d$ give them $\lambda\mathbf1+J$. These are nonnegative. Subtracting two successive prefix estimates and allowing one spare leaf gives the individual bound $V'_x\le h/m+2D+1$, which suffices with the displayed $\lambda$. Each list uses exactly $\lambda k$ leaves. The final vertex histogram is $(s+2\lambda)\mathbf1+\mathbf e_w$. The final edge histogram is $(s+2\lambda)\mathbf1$, since $a+(\tau^d-I)J=s\mathbf1-E'$. The number of requested shift-zero leaves includes the $j<k$ spares and is below $K(m)$. Restore all remaining leaves in Hall batches starting from order $1\bmod k$. [Batch construction](../counterexample-bound.md#removing-leaves)

There is also a one-shift completion. If one parent $u$ has $(k-1)(h-1)$ leaves of one offset $c$, subtract $c$ from all offsets and root $H$ at $u$ with label zero. Write its vertices $v_0,\ldots,v_{h-1}$ in any parent-first order and set
$$
f(v_i)=f(v_{i-1})-f({\rm parent}(v_i))-b_i
$$
using the normalized internal offsets. Every incoming edge has the preceding vertex's label, so $E=V-\mathbf e_{f(v_{h-1})}$. Let $s=\max E_x\le h-1$. Give the appropriate zero-shift leaves labels with multiplicities $s\mathbf1-E$. There are $sk+1-h\le(k-1)(h-1)$ such leaves. Both targets are reached at order $1\bmod k$ and all remaining leaves can be restored.

## Keeping the prefix discrepancies small

Write $q=1+\lceil\log_2 k\rceil$ and $L=2+\lceil18\log(2+h)\rceil$. We can use $D=50q^2L+4$ in all applications above. With unrestricted effective shift $d=1$, at most two prescribed core labels are allowed. In the single-parent construction below, only the root label is fixed exactly and all other core labels may have prescribed residues modulo $g$.

Remove the at most two fixed vertices for the fine-label choices. Repeatedly remove an independent subset of current degree at most eight comprising at least $1/18$ of the current forest. At least half its vertices have degree at most eight and their induced graph has maximum degree eight. Restore in reverse layers. At most $L$ layers suffice. Charge every variable vertex, and each edge to an already labeled neighbor, to its choice. There are at most eleven observations per vertex, including the two possible prescribed neighbors. Edges wholly between prescribed vertices and the at most two prescribed vertex observations add at most two discrepancy per histogram.

Use uniform fractional choices of each vertex within its prescribed cycle. Each edge observation is uniform within its own predetermined cycle, regardless of the already chosen neighbor's fine label. In each histogram charge every observation to the dyadic intervals containing its cycle index, padding the index range to the next power of two. This costs at most $q$ rows per observation. Any initial segment is a disjoint union of at most $q$ such intervals. Each layer may be processed in two sublayers, since its vertices are mutually nonadjacent. The rounding lemma gives per-sublayer prefix error at most $22q^2$. Summing gives the claimed $D$.

We need one extra property of the same rounding argument. In each sublayer choose any linear objective in its option coefficients. In each floating-variable step, orient the nonzero direction so the objective does not decrease, then move to the next boundary. This choice preserves all the original coordinate and group equations. Thus the final objective is at least its fractional value with the same discrepancy bound. Its coefficients need no magnitude bound.

## Bounding the leaf populations

Let $u$ be a parent of largest total leaf population, and let $M$ count all original leaves outside that population. Distribute whole parents between two pools by putting each parent in the lighter pool. The final loads differ by at most the maximum parent population. Hence each pool has at least $M/2$ leaves. Use unrestricted core rounding with $d=1$. Split each layer according to the two pools. In the first sublayer maximize in the nondecreasing sense above the number of leaves of effective shift zero. In the other sublayer use shift one. These are linear objectives in each parent's label options. The uniform fractional choices yield exactly the sublayer's leaf population divided by $k$ in expectation for the desired shift. Summing the bounds gives at least $M/(2k)$ leaves of **each** effective shift, in the same labeling that has core prefix discrepancy $D$.

If $M\ge2kK(k)$, the leaf completion applies since the single cycle has mass difference one. In a counterexample we therefore have
$$
M<2kK(k)=O(kh+k^2D)=O(k^2\log^3(2k)).
$$

It remains to bound the leaves at the heaviest parent. Sort its offset populations as $c_1\ge\cdots\ge c_k\ge0$. The one-shift construction gives $c_1\le kh$. For $2\le t\le k$ with $c_t>0$, place the $t$ most frequent offsets around the residue circle. Some consecutive pair has a positive gap $d\le k/t$, so $m=k/\gcd(k,d)\ge t$. Subtract the first offset from all edges and root $H$ at $u$ with label zero. Use the predecessor formula modulo $g$ to fix the coarse labels. It gives exactly the required single coarse gap. Keep the root at zero, lift each other label within its cycle and use the prefix rounding. The two chosen offset groups now have effective shifts zero and $d$. Hence $c_t<K(m)\le k(\lceil h/t\rceil+6D+12)$. Summing over $t$ bounds the heaviest parent's total by $O(kh\log(2k)+k^2D)$. Adding $M$ and $h$ proves the theorem.

## Checks

The verifier performs the two-shift construction on actual decorated trees over every modulus from 2 through 41 and every nonzero shift difference, with both shared and separate parents. It checks all 1,640 completed histograms directly. A second test plants sites using the actual incident offsets, performs 16 path repairs on 219,328 vertices in total and recomputes all weights from scratch. A third enumerates 65,399 sets of distinct offsets and verifies the order of the circular gap. Lean proves that zero mass on each cycle and divisibility of the aggregate moment suffice for a zero-total integral primitive. The size bounds and the tree constructions are proved above. [Construction](large_order.py) · [Independent checks](check_large_order.py) · [Lean proof of the multiple-cycle identity](../large-order/CyclicCorrection.lean) · [Hall pool identities](../large-order/HallPools.lean)

~~~sh
python3 -B -m research.biased.check_large_order
lean research/large-order/CyclicCorrection.lean
~~~

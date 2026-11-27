# Absorbing the edge sums of an arbitrary tree on one path

**Theorem.** Let $T$ be any tree of order $h\ge2$. Subdivide any one of its edges with at least $77h-1$ internal vertices, giving a tree of order $N$. At any chosen original vertex, adding at least $830N$ leaves gives a super edge-magic tree. In particular a single integer labeling proves cordiality at every modulus. All other original edges and incidences can be retained, with no restriction on their degrees.

Equivalently, any tree of order $t$ can be completed by attaching a path of any length at least $77(t+1)$ at any vertex and then adding leaves at any prescribed original site. Apply the theorem to the original tree with one extra pendant edge. Taking the shortest allowed path and $830N$ leaves gives a host of order linear in $t$ in which all added vertices belong to that path or to the single leaf population. The general construction of [a small host by breadth-first levels](../census/level-hosts.md) gives another choice of added vertices.

## Using several subdivided edges

Let $J$ be any nonempty subset of the original edges and insert $L_e\ge76$ vertices on each $e\in J$. Give the original vertices distinct integers $A$, with zero at the chosen leaf site. Require distinct sums on the retained original edges and write $W$ for that set of sums. One automatic choice labels the original vertices in breadth-first order starting at the site. In the same order, excluding the root, the parent index is nondecreasing. Consequently the child-plus-parent indices strictly increase, even before omitting the edges of $J$.

Let $N=h+\sum L_e$ and
$$
M=\max\big(36N,\max_{x\in A\cup W}|x|\big).
$$
If
$$
\sum_{e\in J}\left\lfloor\frac{L_e-76}{77}\right\rfloor\ \ge\ |W\setminus A|+1,
$$
then the prescribed labels extend to the subdivided tree with distinct vertex labels of span at most $23M$ and with edge sums exactly those labels except their minimum. The same holds with a separately prescribed integer offset on every **retained** edge when its sum in $W$ includes the offset. The subdivided paths and the new leaves have ordinary endpoint sums.

To prove this, place each value of $W\setminus A$ at a separate internal vertex of a path in $J$. Place $g=-10M$ at one further such vertex. The displayed capacity is exact for placing these vertices while keeping at least 76 internal vertices on each resulting segment. In particular $g$ is outside $A\cup W$. Now all retained weights are labels. Give the new segments, in any order, the remaining labels among these prescribed vertices as targets, omitting $g$ and all of $W$. The counts agree because the tree on the prescribed vertices has one more vertex than edge, counting a segment as one edge.

Apply the [prescribed path construction](prescribed-paths.md) to each segment with its target, avoiding all prescribed labels and all previously used internal labels. Each segment contributes precisely its internal labels and its target to the edge multiset. The bounded parameter intervals have size $M$: indeed at most $N$ values are used including the current allocation, and zero is occupied. For a negative target take the final parameter negative and for a nonnegative one take it positive. Its complement in the target then also has magnitude at most $M$. Every ordinary list has labels of magnitude at most $9M$. Use the extreme preparation whenever leaving $g$, with its negative terminal parameter. The four preparation tables give all arrivals strictly above $g$ and at most $13M$. Thus $g$ is the minimum and the span is at most $23M$.

Fill the holes with leaves at zero, then continue upward for any remaining leaves. Both vertex labels and sums become consecutive. Translating to vertex labels starting at one gives a super edge-magic labeling in the ordinary case, by assigning the remaining labels to edges in reverse sum order. Reduction of the two intervals works also for the stated offsets.

For one subdivided edge, $|W|=h-2$. Breadth-first labels give $M=36N$. A length of at least $77h-1$ internal vertices suffices for $h-1$ designated positions. The span bound is $828N$, giving the first assertion. With arbitrary retained offsets of magnitude at most $B$, vertex labels can also be chosen greedily in $[0,2h]$. Give the site zero, then in parent-first order avoid used labels and choices producing a used biased sum. Fewer than $2h$ values are excluded at a step. This gives $M\le\max(36N,4h+B)$ and a linear bound in $N+B$ on the required leaf count.

## More edges than original vertices

There is a related host theorem when the coarse graph has cycles. Subdivide every edge of any finite connected multigraph with at least 92 internal vertices. With $N$ vertices after subdivision, adding at least $12{,}312N$ leaves at any original site gives a super edge-magic graph. For trees and connected unicyclic graphs the [earlier bound](prescribed-paths.md#linear-leaf-bound-for-long-subdivisions) requires only 76 internal vertices and $830N$ leaves.

For a coarse graph of order $h$ and size $m\ge h$, use distinct original labels $0,\ldots,h-1$, with the leaf site at zero. Set $M=36N$ and $H=160M$. Assign the original edges the $h$ original labels as targets together with $H+1,\ldots,H+m-h$. These extra targets are at most $H+M$. The aim is to keep all new vertex labels strictly below $H$. Use the ordinary two-ended path construction for the small targets.

For a large target $w$, reserve a length-eight followed by a length-nine list at **each** end. First grow a singleton at every zero endpoint. The remaining length after reserving the 34 vertices and removing the singletons is at least 56. It is a sum of eights and nines; grow these lists on the left with parameters in $[1,M]$. The two parents of the reserved preparations are now nonzero with magnitudes at most $M$.

In the notation of the path proof, choose the terminal parameters $U,V$ of the final preparations in $[-60M,-59M]$, and $T$ in $[80M,81M]$. The other terminal $w-T$ lies in $[79M,81M]$. The same linear exclusions as before admit a choice in these independently specified intervals. Direct evaluation of the eight-list with small parent and of the nine-list with parent in $[-60M,-59M]$ places every arrival in $[-182M,160M)$. [Lean proofs of both bounds](PrescribedPaths.lean)

Write $S$ for the final set of vertex labels. Its weights are exactly $S$ together with the upper interval $[H+1,H+m-h]$, empty when $m=h$. Fill the holes of $S$ through $H$ by leaves at zero, including $H$ itself when necessary. Now the two intervals have the same lower endpoint and their upper endpoints differ by $m-h$. Further leaves extend both intervals **downward**. At most $342M=12{,}312N$ leaves suffice to reach this stage. Loops or parallel edges cause no difficulty because different original edges have disjoint internal paths.

The checker independently reconstructs all subdivided paths and recalculates their endpoint sums, including any retained offsets. It checks 44 partial subdivisions, six prescribed-offset examples, 72 high-target paths and five multigraphs with more edges than vertices. For the multigraphs it verifies the full set of missing positions and the two consecutive intervals after completion. [Constructor](subdivision_hosts.py) · [Checker](check_subdivision_hosts.py)

~~~sh
python3 -B -m research.hub.check_subdivision_hosts
python3 -B -m research.hub.check_prescribed_paths
lean research/hub/PrescribedPaths.lean
~~~

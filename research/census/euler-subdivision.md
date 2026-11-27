# Exact completion on a long subdivided edge

Let $V_x$ denote the old vertex counts, $E_x$ the old edge counts, and $M(A)=\sum_x xA_x$ in $\mathbb Z_k$. Put $I=2M(V)-M(E)$ and $S=\sum_{x\in\mathbb Z_k}x$.

**Fixed labels.** Given any cordially labeled tree of order $n$, any chosen edge and any $t\ge3k$, one can insert $t$ vertices on that edge while preserving all old labels, subject to one necessary and sufficient condition. When $k$ is even and $n+t=qk+1$, one needs $I\equiv qS\pmod2$. Every other case works. The separate [one-period theorem](period-subdivision.md) handles $t=k$ and the [one-surplus-core theorem](cycle-subdivision.md) handles all lengths at old order one modulo $k$.

**Ordinary trees.** Subdividing any chosen edge of an arbitrary $n$-vertex tree by any $t\ge n+3k-3$ vertices gives a $k$-cordial tree. Uniformly in its order and degrees, **any tree containing a path with at least $35k$ internal vertices of degree two is $k$-cordial**. At odd $k$, **$25k$** such vertices suffice. These are sufficient bounds. The original tree and the path endpoints may have arbitrary degrees. No enumeration of tree shapes enters these conclusions.

## Realizing prescribed gains by an Euler circuit

Inserting a vertex of label $z$ between $a,b$ replaces the weight $a+b$ by $a+z,z+b$. Thus $I$ is invariant throughout any subdivision. For final order $N=qk+1$ the vertex bins must consist of $q$ copies of each residue and one extra $x$, while the edge bins must be uniform. This gives $2x=I-qS$, with precisely the stated parity condition. For every other final order, choose the prescribed number of high vertex bins among those with largest old count. The set of high edge bins has a size $r$ between 1 and $k-1$. Its sum can be any prescribed residue. Indeed the sums of $r$ distinct elements of $[0,k-1]$ take all integers from $\binom r2$ through $\binom r2+r(k-r)$ by increasing the rightmost entries first. This covers $k$ consecutive integers. Choose the sum that gives the required $I$.

Write $A,B$ for the target increments in the vertex and edge histograms. They have equal mass $t$, and $2M(A)=M(B)$. We seek a directed circuit of $t$ arcs on the residues with $A_x$ arrivals at $x$ and $B_w$ arcs of endpoint sum $w$. Starting at one old endpoint, insert the successive heads, including its final copy. Retaining the edge from that copy to the other old endpoint reproduces the old edge weight.

Let $c=\min A\ge1$. Reserve the directed cycle $x\mapsto x+1$ and add $A_x-c$ loops at $x$. Suppose their weights fit within $B$. The remaining arc counts must have constant incoming and outgoing margin $c-1$, and the residual weight list has sum zero modulo $k$. The Erdős–Ginzburg–Ziv theorem partitions this list into blocks of $k$ with sum zero. While at least two blocks remain, find a zero-sum $k$-subset, then use the already zero-sum last block. For each block, Hall's prescribed-differences theorem gives two permutations of the residues whose pointwise **sums** are the listed weights, by negating the sources in its differences formulation. Add the corresponding arcs from the first permutation to the second. Every vertex now has equal indegree and outdegree $A_x$. The reserved cycle ensures connectivity, so an Euler circuit traverses all arcs from the desired start. [Erdős, Ginzburg and Ziv (1961)](https://www.renyi.hu/~p_erdos/1961-25.pdf) · [Marshall Hall Jr. (1952)](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

At odd $k$ the cycle uses each weight once, and at most one vertex can add loops of a specified weight. At even $k$ the cycle uses each odd weight twice and only even weights occur on loops, with two possible sources per weight. Thus at vertex-increment spread $d$, a sufficient lower bound on each $B_w$ is $1+d$ at odd $k$, or $\max(2,2d)$ at even $k$.

For a cordial core and final order different from one modulo $k$, choosing the high vertex bins in descending order of old count gives $d\le1$. Each $B_w\ge\lfloor t/k\rfloor-1\ge2$. For final order one, $B_w\ge\lfloor t/k\rfloor\ge3$ because the final edge counts are integral multiples of the same unit count and the old counts are balanced. The spread of $A$ is at most two. A spread of two requires the unique new high bin $x$ to have been low, and only this one bin is two above the minimum. The maximum loop demand per weight at even $k$ is therefore three. At odd $k$ one cycle arc and at most two loops suffice. In both cases $c\ge1$. This proves the fixed-label assertion, including necessity.

## A bound depending on the original order

Root the tree and number its vertices $0,\ldots,n-1$ breadth first, with siblings consecutive. Label by rank modulo $k$. With child ranks strictly increasing and parent ranks nondecreasing, the integer edge sums are distinct in $[1,2n-3]$. Thus the vertex bins are balanced and no edge bin contains more than $\lceil(2n-3)/k\rceil$ edges. At $t\ge n+3k-3$, the final edge floor is at least two above this upper bound, since $k\lceil(2n-3)/k\rceil\le2n+k-4$. If $n+t\not\equiv1\pmod k$, choose high vertex bins as above, obtaining $d\le1$ and $c\ge1$. The circuit supplies the desired subdivision. For $k=1$ balance is automatic.

At final residue one, first remove any original leaf outside the two endpoints of the chosen edge. Such a leaf exists unless the tree consists only of that edge, in which case the result is an ordinary path. Apply the construction to the smaller tree, whose final order is divisible by $k$. Closing the missing edge weight uniquely labels the restored leaf.

## A bound independent of the original order

Assume $k\ge5$, as the smaller moduli are known. In a smallest counterexample **among trees containing the required path**, mark its whole maximal run of degree-two vertices. A path itself is cordial. At most one original leaf is an endpoint of the marked run. At order one modulo $k$ delete a leaf outside it, label the smaller tree and restore the missing weight. Otherwise put $s=(n-1)\bmod k$. If there are $s$ leaves outside the marked run, delete them, label the smaller tree and apply Hall's leaf extension at order one modulo $k$. Either deletion keeps the required path. Hence a counterexample in this family has at most $k-1$ leaves and order different from one modulo $k$. [Leaf extension](../counterexample-bound.md#removing-leaves)

Collapse the marked run to one edge, leaving a tree of order $b$ and at most $k-1$ leaves. Pin the $h$ vertices of degree different from two. The tree degree sum gives $h\le 2k-4$. Breadth-first number its suppressed skeleton and label the pins by their ranks modulo $k$. Their vertex counts have spread at most one. The edges directly joining pins are a subset of the skeleton edges. By the preceding rank argument their count in each bin is at most $C=\lceil(2h-3)/k\rceil\le4$.

Along each segment between pins number its remaining interior vertices $0,1,\ldots$ from either end. First label the odd positions. These form an independent set and each is adjacent to at most one pin. For the $m$ sites with a pin neighbor, use its label as a request. While at least $2k-1$ requests remain, extract a zero-sum $k$-block and apply Hall to label these sites with all vertex and edge residues once. Split the remainder into at most two blocks of size at most $k-1$. For each, pad its requests to length $k$ with sum zero and restrict Hall's permutations. Each partial block contributes at most one per vertex or edge bin. Two partial blocks are used only when the remainder has size at least $k$. Hence this stage has vertex spread at most two and edge-bin maximum at most $m/k+1$. Give the odd positions without pin neighbors least-used labels of this stage, preserving its vertex spread.

The remaining even positions are independent and now have two labeled neighbors each. At a site with neighbor labels $a,b$, a choice $x$ contributes a column with **two** units in vertex bin $x$ and one in each edge bin $a+x,b+x$, counting coincidences. A uniform choice has mean $2/k$ in every vertex and every edge bin. These columns have mass four. The [group rounding lemma](../large-order/flexible-path.md#subdividing-edges-with-controlled-multiplicities) chooses an option at each site with coordinate error at most eight, giving vertex error at most four after dividing by two. Altogether the compressed tree has vertex spread at most $1+2+8=11$ and edge-bin maximum at most
$$
(b-1)/k+C+1+8\le (b-1)/k+13 .
$$
Every edge was counted in exactly one stage.

Restore the $t$ marked vertices. The final order is different from one modulo $k$. Give priority to larger old vertex bins when choosing the final high bins. The increment spread is then at most 11, and its minimum is positive at the stated lengths. At $t\ge35k$ each weight increment is at least 22, by the edge-bin bound and integrality. At odd $k$ and $t\ge25k$ each is at least 12. These are exactly the sufficient cycle-and-loop budgets above. This contradicts the choice of the tree.

## Reproduction

The [constructor](euler_subdivision.py) builds the target counts, realizes them by an Euler walk, and implements both the breadth-first and suppressed-skeleton labelings. The [independent checker](check_euler_subdivision.py) recounts actual adjacent sums. It checks 91,520 subset sums, 1,736 compatible balanced histogram inputs, 64 parity rejections, 480 padded trees, 255 prescribed circuits, 288 one-neighbor lists and 54 complete trees using exact rational rounding. At small moduli it independently enumerates all possible final balanced moments. These finite checks exercise the constructions. The proofs above give the unrestricted size and modulus quantifiers.

~~~bash
python3 -B -m research.census.check_euler_subdivision
~~~

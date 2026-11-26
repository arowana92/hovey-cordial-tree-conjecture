# Completing an arbitrary tree by leaves at two specified vertices

**Theorem.** Fix distinct vertices $a,b$ of a finite tree $H$. If their distance is 1, 3, or at least 5, there are computable nonnegative integers $A,B$ such that adjoining **any** $m\ge A$ leaves to $a$ and **any** $n\ge B$ leaves to $b$ produces a tree cordial at every positive modulus. The same integer labeling works at all moduli. In particular, every specified edge of every tree can serve as the two attachment vertices.

The stronger conclusion is that the vertices receive precisely an integer interval $[L,U]$, with $a$ labeled 0 and $b$ labeled 1, and the edge sums receive precisely $[L+1,U]$. Translating the vertex interval to start at 1 gives the usual consecutive-sums characterization of a super edge-magic labeling. Consecutive integer intervals have balanced frequencies modulo every $k$. [Youssef, Theorem 4, *On k-cordial labelling*](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

## Growing a labeled subtree

Maintain the two intervals above. An extra leaf at $a$ can extend the upper end, using label and weight $U+1$. An extra leaf at $b$ can extend the lower end, using label $L-1$ and weight $L$. These operations may repeat independently.

To insert a required child at a parent of integer label $p$, use the following rules.

| Parent | Required child label | Additional leaf labels | Where the additional leaves attach |
|---|---|---|---|
| $p>0$ | $L-p$ | $L-p+1,\ldots,L-1$ | $a$ |
| $p=0$ | $U+1$ | none | |
| $p<0$ | $U+1-p$ | $U+1,\ldots,U-p$ | $b$ |

For positive $p$ the required edge supplies the old missing weight $L$. All gap labels supply themselves, leaving $L-p$ missing. For negative $p$ the required edge supplies $U+1$. The gap leaves then supply $U+2,\ldots,U+1-p$. Thus both enlarged sets have the prescribed interval form. Earlier labels are retained. One can force a child at a positive parent to have any sufficiently small label by first extending the lower end. A child at a negative parent can have any sufficiently large label by extending the upper end first.

At distance one start with the edge labeled $0,1$. Starting from any path between $a,b$ already completed to the two intervals with leaves at these vertices, grow the rest of $H$ in parent-before-child order by the table. The required thresholds are the total numbers of additional leaves used at the two hubs. Further leaves use the independent endpoint operations. At distance one there is also the simple a priori bound $A+B\le2^{h-1}-h$ for $h=|H|\ge2$. Both 0 and 1 stay in the interval. Its length at most doubles when a required child is inserted, since the increase is at most the old length. Start with length two and make $h-2$ insertions.

## Paths that start the construction

For distance $2s+1$, take a list $z_0,\ldots,z_s$ of $[0,s]$ beginning at zero with absolute consecutive differences $s,s-1,\ldots,1$. Alternating the smallest and largest remaining values gives such a list. Use the two copies $N(i)=-i$ and $P(i)=1+i$ of this interval. Visit the $z$ list starting with $N(z_0)$ and alternating copies. At $z_s$ cross to its other copy. Return through the list in reverse, always using the copy opposite the outbound visit. The path starts at 0 and ends at 1. Each outbound edge sum is 1 plus a directed difference, and its paired return edge has sum 1 minus that difference. The middle edge weighs 1. Thus the vertices are $[-s,s+1]$ and the weights are $[1-s,s+1]$, as claimed.

At distance six the path in order is
$$
0,\ 2,\ -1,\ 4,\ -4,\ 3,\ 1 .
$$
Add two leaves of labels $-3,-2$ at $a$. The vertices fill $[-4,4]$. The path weights are $2,1,3,0,-1,4$ and the two extra weights fill the rest of $[-3,4]$.

To go from an even distance $d\ge6$ to $d+2$, take a path edge with endpoint labels $p>0$ and $q<0$. The displayed path has such an edge. Add a required child with very negative label $x$ at $p$, then a required child with label $y=p+q-x$ at $q$. Choose $x$ sufficiently small that $y$ is above the threshold for the negative-parent rule. Growing the lower end in the first step leaves the upper end fixed. Replace the edge of weight $p+q$ by the edge between the two new children, which has the same weight. This subdivides the old connection into a path of three edges and leaves both interval identities intact. The new middle edge again has endpoints of opposite signs. Induction supplies every even distance at least six.

## Deciding the entire two-parameter family

For a fixed $H$ and eligible hubs, it is decidable whether *all* nonnegative pairs of leaf counts work at *all* moduli. The construction above covers $m\ge A,n\ge B$. For each $m<A$ absorb those $m$ leaves into the fixed core and apply the [finite one-hub decision theorem](rational.md) at $b$. For each $n<B$ do the same at $a$. This takes at most $A+B$ one-hub decisions. Each either supplies a finite bound on all remaining searches or yields ordinary counterexamples for all sufficiently large primes on the corresponding fixed-core slice.

## An exact criterion and the two excluded distances

A fixed injective integer assignment on $H$ with $a=0,b=1$ can be completed by such leaves to the required intervals exactly when its core labels $x_1<\cdots<x_h$ and its core edge sums $y_1<\cdots<y_{h-1}$ satisfy
$$
x_i<y_i\le x_{i+1}\qquad (1\le i<h).
$$
The condition requires distinct core edge sums. For sufficiency, in each gap between consecutive core labels use every missing integer $z$. Attach $z$ at $a$ if $z<y_i$ and at $b$ otherwise. The new weights complete $(x_i,x_{i+1}]$ and retain its unique core weight $y_i$.

For necessity, look at any occupied core position $j=x_i$ inside a completed interval $[L,U]$. All added vertices labeled at most $j$ have weights at most $j$: the last such leaf can be labeled at most $j-1$ and its increment is at most one. No added vertex labeled above $j$ can weigh at most $j$. Thus the numbers of added vertices and added weights through $j$ agree. There is one more vertex than edge weight through $j$ in the completed intervals, so exactly $i-1$ core weights are at most $x_i$. This proves the gap condition.

For the bare paths at distances 2 and 4 there is no such completion, even with arbitrarily many leaves at the designated hubs. The checker exhausts the orders of the core labels with 0 immediately preceding 1 and all orders of the path edges. In each case it imposes the necessary linear inequalities $y_i-x_i\ge1$ and $x_{i+1}-y_i\ge0$, fixing the endpoints at 0 and 1. Fourier–Motzkin elimination by integer row operations gives an inconsistency in all 4 and all 576 respective systems, already over the rationals. These obstructions concern the two prescribed labels and interval alignment. The two paths and their two-hub extensions are caterpillars and are cordial by Hovey's theorem. [Hovey, *A-cordial graphs*](https://doi.org/10.1016/0012-365X(91)90254-Y)

## Reproduction

The checker reconstructs the entire path and any added branches and leaves, and computes the vertex and edge multisets directly. It also checks the excluded path systems by exact elimination.

~~~sh
python3 -B -m research.hub.two_hubs
~~~

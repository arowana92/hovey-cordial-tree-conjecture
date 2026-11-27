# When two fixed cordial labelings can be joined across a bridge

Take cordial labelings on two trees of orders $-a,-h\bmod k$, with $a,h\ge1$ and $a+h+1\le k$. Mark a port in each and translate each labeling so that its own port is zero. Write $V,W$ for the low vertex and edge residues on either side. They have sizes $a,a+1$ on the core and $h,h+1$ on the piece. If a histogram is uniform at the end of a period, take the missing entries relative to the next full period.

**Exact criterion.** Suppose the least prime divisor of $k$ exceeds $2ah+\max(a,h)+1$. No affine permutation of the piece labeling yields a cordial join precisely when **both** sides satisfy
$$
0\in V\cap W,\qquad 2(W\setminus V)\subseteq W.
$$
All core labels stay fixed. A bridge offset can be absorbed into the old port in the normalization. The obstruction direction holds for every modulus when $a+h+1\le k$.

## Why these are the only obstructions

Perform the affine change $y\mapsto uy+x$ on the piece. Its vertex holes move to $uV+x$, its edge holes to $uW+2x$, and the bridge has weight $x$. The two vertex-hole sets must be disjoint. For edges the bridge must hit one of the two edge-hole sets, and their intersection must be contained in the single bridge weight. These conditions are necessary and sufficient: the final counts have deficits of one at exactly $a+h$ vertex residues and $a+h+1$ edge residues relative to full periods.

Write $V_0,W_0$ for the core sets. Prescribe that the bridge fills the hole from $w\in W$ by setting $x=-uw$. Each piece vertex hole must then avoid $V_0$, and the other piece edge holes must avoid $W_0$. A zero direction occurs among the vertex holes if $w\in V$ and among the remaining edge holes if $2w\in W\setminus\{w\}$. Thus the only forced collisions in this placement are
$$
(w\in V\ \text{and}\ 0\in V_0)\quad\text{or}\quad
(2w\in W\setminus\{w\}\ \text{and}\ 0\in W_0).
$$
In their absence choose a uniform unit. Every nonzero direction has orbit size at least the least prime divisor minus one, and there are $ha+h(a+1)$ forbidden values with multiplicity. Their total failure probability is less than one. The same statement holds on interchanging the sides, with $a(2h+1)$ forbidden values. An affine join obtained by changing the core instead can be composed with the inverse affine permutation on the entire ordinary joined tree, restoring the prescribed core labels. Equivalently, for a hole $z\in W_0$ set $x=z$ directly: the vertex holes must avoid $V_0$, and the edge holes need only avoid $W_0\setminus\{z\}$. This direct proof also permits fixed offsets inside the core.

If $0\notin W_0$, take any $w\in W\setminus V$, which exists by cardinality. Neither collision is forced. Failure therefore requires zero in both edge-hole sets. If $0\notin V_0$, then $w=0$ now works, so failure requires zero in both vertex-hole sets as well. With zero in all four sets, a hole from the piece is usable precisely when $w\in W\setminus V$ and $2w\notin W$. The same holds for the core. This gives the displayed criterion. When both sides satisfy it, every possible bridge placement forces a collision, independently of any orbit-size bound.

## Two missing vertices

If the least prime divisor exceeds three, a side with two vertex holes meets the obstruction condition exactly when its normalized profile is
$$
V=\{0,2t\},\qquad W=\{0,t,2t\},\qquad t\ne0.
$$
Indeed doubling permutes the nonzero residues. If both nonzero members of $W$ lay outside $V$, they would have to form a doubling two-cycle, requiring $3t=0$. Otherwise exactly one lies outside $V$, and doubles to the other.

For any $a,h\ge2$ and $k\ge a+h+1$, take each side of deficit $j\in\{a,h\}$ to have $V=\{0,2,3,\ldots,j\}$ and $W=\{0,1,2,\ldots,j\}$. Both satisfy the obstruction condition. These are actual cordial labelings of ordinary trees: start with a star containing every residue once, then append the outstanding vertices at parents realizing the assigned edge weights, starting with two or more uniform periods to ensure the initial star fits. The profiles obstruct joining these *fixed* labelings by affine maps. They provide no counterexample to Hovey's conjecture.

Thus for a minimum counterexample modulo a prime $p\ge13$, an internal cut with both component orders $-2\bmod p$ requires **every cordial labeling on either side** to have the displayed two-hole profile at its port. One side admitting any other profile would suffice to label the entire tree. For pieces with low vertex and edge residues in consecutive intervals, a separate [gluing theorem](interval-deficit-cut.md) gives bounds even over moduli with small prime factors.

## A forbidden interval of exact component orders

Let $T$ be a smallest ordinary counterexample modulo $k$, and write its order as $-H\bmod k$, $1\le H<k$. If the least prime divisor of $k$ exceeds $H(H+1)/2+1$, no edge of $T$ can cut off a component of any of the $H+1$ exact orders
$$
k-H,k-H+1,\ldots,k.
$$
The endpoints give a nonempty divisible component on one side or the other and are excluded by the [divisible cut rule](../divisible-cuts.md). For an interior order $k-h$ put $a=H-h$, so $a,h\ge1$. Both smaller trees admit cordial labelings. In the component of order strictly less than $k$ every vertex label is used at most once. Therefore the port's own residue is present and cannot be a low vertex residue. This component fails the necessary obstruction condition. The exact criterion applies since
$$
2ah+\max(a,h)\le H(H+1)/2,
$$
as follows from $(a-h)^2\ge|a-h|$. This proves the assertion for all tree orders. For example at 29 labels and order $23\bmod29$, the seven exact component orders 23 through 29 are forbidden. At order $2k-H$, every component after removal of an ordinary vertex centroid consequently has at most $k-H-1$ vertices.

## Reproduction

The [checker](check_sparse_profiles.cpp) constructs every pair of low sets of the given sizes, identifying independent unit multiples on each side. It tries all affine images of one side, checking the vertex intersections and the bridge-adjusted edge intersections directly. At $p=13$, $a=h=2$, the theorem predicts exactly $(13-1)^2=144$ obstructed normalized pairs among 497,646,864, as confirmed by the direct check. A [separate full-tree check](check_interval_deficits.py) realizes 90 pairs with the explicit obstruction at prime and composite moduli and rejects every affine image by recounting both histograms.

~~~sh
out=$(mktemp -d)
c++ -O3 -std=c++17 research/prime/check_sparse_profiles.cpp -o "$out/check"
"$out/check"
~~~

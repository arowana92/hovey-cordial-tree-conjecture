# When a depth-first order prevents cordial growth

**Theorem.** For every composite modulus $k$, there is a $k$-cordial tree and a specified depth-first preorder such that no labeling is cordial on every prefix of that order. If $p$ is the least prime divisor of $k$, the example has $k(p+2)$ vertices. In particular it has 32 vertices at eight labels and 45 at nine. At every even modulus with an odd factor, a caterpillar on $2k$ vertices suffices.

The [two-period construction](two-period-orders.md) gives a diameter-four example on $2k$ vertices at every composite modulus. It also determines the exact minimum orders at eight and nine.

## An obstruction at every composite modulus

Put $g=k/p$. Start the preorder with a path on $k$ vertices, oriented away from its first vertex. Choose distinct path vertices $v_1,\ldots,v_{p+1}$ in reverse path order, with $v_1$ its far end and $v_{p+1}$ its first vertex. Put $a_1=v_1$. For $i=1,\ldots,p+1$, append a star of order $g$ at $a_i$, then a star of order $k-g$ at $v_i$, in each case listing the new center and then its leaf children. Put $a_{i+1}$ equal to the second new center. The first star of the next block is the remaining child subtree of that center. After finishing it, the traversal backtracks to the next $v_i$. This is a depth-first preorder.

The [two-star congruence](growth-orders.md#a-prescribed-order-at-every-composite-modulus) applies independently of the shape of the starting $k$ vertices. Here is the argument on this path. At the start of a block write $A,B$ for the labels at $a_i,v_i$, and $D$ for the deficient edge weight. The first center has forced label $X=D-A$. All edge bins are now equal. After translating the surplus $X$ to zero, the remaining batch consists of singleton children at zero and a star of order $k-g$ with parent label $B-X$. To reach divisible order the new vertex labels must exhaust the nonzero residues and the new weights must be distinct. The [pinned-star criterion](../rainbow/pinned-star.md) forces $g\mid B-X$.

Let $Y$ denote the second center label and $D'$ the new deficit. The $k$ new vertices use each residue once. Writing $S=\sum_{x\in\mathbb Z_k}x$, their incident new edges sum to $S+D-D'$. Counting the same edges at their endpoints gives $S+A+B+(g-1)X+(k-g-1)Y$. Hence $D'\equiv X+Y\pmod g$. In the next block the first center is forced to $D'-Y$, which must agree modulo $g$ with the label at $v_{i+1}$. Thus all $p+1$ distinguished vertices have the same residue modulo $g$. The starting $k$ vertices have distinct labels, and each residue class modulo $g$ contains exactly $p$ of them. This proves impossibility.

**Ordinary cordiality of the same tree.** Pair the second star of each of the first $p$ blocks with the small star attached at its center in the next block. Deleting those pairs leaves a caterpillar on $2k$ vertices. The two unpaired stars are at the two ends of the original path. List the edges from all leaves at one end, through the spine, to all leaves at the other end. Within each bipartition class rank the vertices in order of first appearance. Give the classes consecutive disjoint integer intervals in those ranks. Each successive edge keeps one endpoint and changes the other to the next rank of its class. Thus the vertex labels and the edge sums each form a consecutive interval. Reduction modulo $k$ is cordial.

Each deleted pair adds $k$ vertices at an old parent. Normalize its label to zero. Give the outer center $g-1$, the inner center $g$, the inner leaves $0,\ldots,g-2$, and the outer leaves $g+1,\ldots,k-1$. The new labels exhaust the residues. Subtract $g-1$ from the new weights. The entering edge gives zero, the center edge gives $g$, the inner leaves give $1,\ldots,g-1$ and the outer leaves give $g+1,\ldots,k-1$. Translating the piece by the actual parent label only permutes the two histograms. Restoring all pairs therefore proves ordinary cordiality for every $k$ in the construction.

## A two-period caterpillar

Suppose $k$ is even and has an odd factor. Set $g$ equal to the largest power of two dividing $k$, so $1<g<k$ and $g\nmid S$. Start with the path $v_0,\ldots,v_k$ in that order. Append $k-1-g$ singleton leaves at $v_k$, then a star of order $g$ attached by its center to $v_0$. This is a depth-first order on a caterpillar with $2k$ vertices.

In any labeling cordial at the first $k$ vertices, those labels form a permutation. Its internal edges have total $2S-x_0-x_{k-1}$ and omit exactly one weight. The next edge must supply that weight, forcing $x_k=x_0-S$. Now the edge counts are uniform and $x_k$ is the surplus vertex label. The remaining $k-1$ vertices consist of singleton leaves at this surplus and a star of order $g$ at relative parent $S$. The pinned-star criterion would require $g\mid S$. This proves failure of the specified order. The ordinary labeling is given by the same consecutive-ranks caterpillar construction.

## Sharp fixed-core guarantees at eight and nine

At eight labels, if at most **two** terminal arms have length one, every depth-first preorder works. At nine labels, at most **four** suffice. Both conclusions hold starting from any fixed cordial prefix of order zero or one modulo $k$, and both numbers are sharp for this fixed-prefix property. An arm of length one is an original leaf adjacent to a branching vertex. Paths satisfy the conclusions as well.

The complete one-surplus classifications place every failed batch at size $k-1$, with exactly one internal vertex and hence $k-2$ rooted tips. The [preorder interval bound](../rainbow/terminal-arm-orders.md#what-a-preorder-interval-contains) supplies $k-4$ complete original arms between the two end tips. At eight, four middle arms with at most two of length one already require six vertices, in addition to the end tips. At nine, five middle arms with at most four of length one require at least six vertices. An eight-vertex interval attaining equality consists solely of paths, whereas both nine-label exceptional stars have a vertex with at least two children. Thus every required batch passes. At divisible order fill the unique deficient edge bin on the next vertex and continue. [Eight-label classification](surplus.md) · [Nine-label classification](../rainbow/surplus-nine.md)

For sharpness at $k=8,9$, start with a path of order $2k+1$, labeled cordially on every prefix, with both ends zero and the vertex at index two labeled one (indices start at zero). To construct it, let $P_{2j}=j$ and $P_{2j+1}=\lceil k/2\rceil+j$ for indices below $k$. The list $P$ is bijective and its adjacent sums form a consecutive interval. Use $P$, then $P-S$, then zero. The path calculation above gives the required joining label after each period, since $2S=0$. Its unique surplus at the end is zero.

Append a leaf at the far end, a star of order $k-6$ at index two, and four vertices attached to the original start. Give the last of those four one further child. This ordering is depth-first. Before reaching that final child the full batch consists of the star at relative parent one and five singletons at zero. Since $k-6$ is two at eight and three at nine, the divisibility condition fails in both cases. The completed eight-label tree has three one-edge terminal arms. The nine-label tree has five. This sharpness argument fixes the displayed initial labels.

## Independent verification

The [checker](check_dfs_obstructions.py) rebuilds the parent arrays, checks that a depth-first visit realizes the specified order, and recounts ordinary vertex and edge labels for all 153 composite moduli through 200. It also constructs the two-period caterpillars. At $k=4,6,8,9$ a separate exhaustive search tries every possible labeling of the initial path after fixing its first vertex to zero. It enumerates both center labels and all leaf label sets compatible with each next block, retaining every attainable deficit. The respective 2, 12, 112 and 360 initial path labelings all fail. Finally it exhausts all $7!$ and $8!$ remaining label permutations on the sharp fixed-prefix examples.

~~~bash
python3 -B -m research.eight.check_dfs_obstructions
~~~

# One full period on any chosen edge

**Theorem.** Let $k\ge5$ and prescribe any cordial labeling of any finite tree of order $n$. Exactly $k$ new vertices can be inserted on any chosen edge, preserving all old labels, unless **both** $k\equiv2\pmod4$ and $n\equiv1\pmod k$. In that exceptional case no edge admits such an extension. Consequently, outside the exception, arbitrary multiples of $k$ may be inserted independently on arbitrarily many edges.

**Ordinary cordiality consequence.** Start with any tree on at most 27 vertices. For every positive $k$, insert an independently chosen nonnegative multiple of $k$ vertices on each edge. The resulting tree is $k$-cordial. The modulus, final order, and distribution of subdivisions are unrestricted. More generally, this holds for any $k$-cordial starting tree outside the exception. In the exceptional residue it suffices that deleting one original leaf gives a $k$-cordial tree.

The [one-period constructions](edge-padding.md#a-whole-period-on-any-fixed-core) already give the result for odd $k$, for $4\mid k$, and for even $k$ whenever a low edge bin has a high antipode. The [weight-sum obstruction](cycle-subdivision.md#long-subdivisions-and-the-obstructions) proves the negative case, explicitly allowing the old vertex surplus to move. It remains to cover the other odd tree orders at $k=2m$ with $m$ odd.

## Two ways to move one vertex count

Let $X$ and $E$ denote the high vertex and edge bins, respectively, with “high” meaning one above the floor. Assume $E$ is invariant under translation by $m$. This makes $|E|$ even, so $n$ is odd. The exceptional case is $E=\varnothing$. Otherwise $|X|=|E|+1\ge3$. Put
$$
P=\{u:2u\in E\},\qquad L=\mathbb Z_k\setminus X.
$$
The set $P$ is also antipodally invariant and has $|E|$ elements. Indeed each antipodal pair in $E$ contains one even residue, and doubling reaches that residue twice. We seek a high vertex bin $y$ and a low vertex bin $z$.

**First construction.** When $y\in X\cap P$ and $z\in L\setminus P$, insert the $k-1$-vertex path avoiding $y$. Its net edge weights omit $2y+m$. Duplicate an occurrence of $z$ on the path, adding weight $2z$. Relative to uniform increments this moves one vertex from $y$ to $z$ and one weight from $2y+m$ to $2z$. Both moves are from high to low.

**Second construction.** Suppose $y\in X\setminus P$, $z\in L$ and $2y-z\in P$. Choose $y$ so the old endpoints are not both $y$. Subtract $y$ from their labels temporarily and put $\delta=z-y$. Use the cycle on the nonzero residues in this order:
$$
1,m+1,2,m+2,\ldots,m-1,2m-1,m .
$$
Its adjacent sums are distinct and omit $m$: before the closing edge the successive sums are the integers $m+2$ through $3m-1$, and the closing sum is $m+1$. It contains the edge joining $j$ and $j+m$ for each $1\le j<m$. Rotate the cycle at a nonzero old endpoint and traverse it back to its copy, retaining the far edge's old weight.

In this traversal insert one more vertex labeled $\delta$ on the edge joining $m-\delta$ and $-\delta$. Such an edge occurs because $\delta\not\equiv0\pmod m$, as follows from $y\notin P$ and $2y-z\in P$. Its old weight $m-2\delta$ is replaced by $m,0$. Undoing the translation, the net increments equal one in every bin, with one vertex transferred from $y$ to $z$ and one edge weight transferred from $4y-2z+m$ to $2y$. The former edge bin is high since $2y-z\in P$ and $E$ is antipodally invariant. The latter is low since $y\notin P$.

## Why the two constructions cover every histogram

If the first construction fails, either $X\cap P$ is empty or $L\subseteq P$.

If $X\cap P$ is empty and $X$ contains an antipodal pair, choose $y$ in such a pair. The set $2y-P$ has $|X|-1$ elements and misses both $y$ and $y+m$. It cannot lie inside $X$. If $X$ contains no antipodal pair, $2y-P$ still contains one and so cannot lie inside $X$ for any $y\in X$. In either case there are at least two choices for $y$, and a $z\in (2y-P)\setminus X$ supplies the second construction. At most one choice of $y$ is forbidden by the endpoints.

Suppose instead that $L\subseteq P$. Some $z\in L$ and $y\notin P$ must satisfy $2y-z\in P$. To prove this, project the antipodal classes to $\mathbb Z_m$, denoting images by bars. If no such pair existed then for every $z\in L$,
$$
2\overline P-\bar z=\overline P .
$$
Indeed the preimage of $\overline P$ under this affine map lies in $\overline P$, and the map is a permutation because $m$ is odd. Subtracting any two translation parameters shows that $P$ is invariant under each difference of two elements of $L$. Let $H$ be the subgroup of all translation periods of $P$ in $\mathbb Z_k$. It contains $m$ and has even order. All of $L$ lies in one coset of $H$. Since $|L|$ is odd, $|L|<|H|$. The complement of $P$ is a union of cosets and has size $|L|+1$, so it is exactly one coset, say $c+H$. The displayed affine map acts on $\mathbb Z_k/H$, an odd-order group, and fixes the sole missing coset. Hence $2c-z=c\pmod H$, putting $z$ outside $P$. This contradicts $L\subseteq P$.

Both lifts $y,y+m$ of the resulting witness lie outside $P$ and hence in $X$. Either one meets the same weight condition, so one can avoid the forbidden endpoint label. This finishes the fixed-label proof.

## Subdividing several edges

All period insertions preserve the order residue, so the theorem iterates outside the exception. In the exceptional case, delete an original leaf $v$ for which $T-v$ has a cordial labeling. Its order is divisible by $k$. Insert the requested periods on all remaining original edges. If the edge to $v$ needs $jk$ internal vertices, grow a pendant path of $jk$ vertices at its old neighbor; full pendant-path periods are uniform. The tree is still divisible. Attach $v$ at the far end with the label filling the deficient edge weight. This gives the required ordinary labeling. The [integer census](README.md) provides the base and its leaf deletion through order 27. At the four smallest moduli cordiality of every tree is known.

The [constructor](edge_padding.py) performs the actual exchanges, including along a prescribed monochromatic edge. The [independent histogram checker](check_edge_padding.py) tests 286,690 configurations with invariant edge bins. It exhausts the high vertex and edge sets at moduli 6, 10 and 14 in the nonempty invariant case and tries every monochromatic endpoint at 6 and 10. It also checks 11,231 general fixed-core periods through modulus 4,096.

~~~bash
python3 -B -m research.census.check_edge_padding
~~~

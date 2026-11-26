# A vertex of degree at least four times the squared modulus suffices

**Theorem.** Every tree of maximum degree at least $4k^2$ is $k$-cordial, at every positive modulus $k$. The rest of the tree can be arbitrary.

## Preserving a connected subtree while removing leaves

Fix a connected subtree $S$ of $T$. If $t=(|T|-1)\bmod k$ is positive and at least $t$ original leaves outside $S$ are available, delete $t$ of them. If that first deletion is impossible, stop. Once the order is 1 modulo $k$, repeatedly delete $k$ simultaneous leaves outside $S$ until fewer than $k$ are available. This produces a core $C$ containing $S$ with at most $k-1$ leaves outside $S$. Every cordial labeling of $C$ extends to $T$. Indeed, each deleted batch can be restored to a tree of order 1 modulo $k$. For a batch of size at most $k-1$, Hall's leaf extension gives distinct new labels avoiding the surplus vertex label and distinct new weights. For a batch of size $k$, first do this for $k-1$ leaves and then supply the unique deficient edge weight with the final leaf. All the parents survive their batch deletion. [Hall's theorem and leaf extension](../counterexample-bound.md#removing-leaves)

## Labeling segments with zero endpoints

For every odd length $d=2r+1$, there is a walk of $d$ edges from label zero back to zero whose arrival labels and edge sums each use every integer in $[-r,r]$ once. On the unshifted cyclic list take
$$
0,r+1,1,r+2,\ldots,r-1,2r,r
$$
and close back to zero. Its first $2r$ sums are $r+1,\ldots,3r$ and the closing sum is $r$. Subtract $r$ from every vertex and start the cycle at the vertex now labeled zero. This includes the one-edge walk $0,0$. For even $d$, take the walk of length $d-1$ and add a final $0,0$ step. Reducing modulo $k$ preserves the equality of the two histograms. The contribution of a single segment of length $d$ to any bin is at most $d/k+2$, by counting residues in one consecutive interval and at most one additional zero.

Take any tree $B$ with a specified vertex $v$. Mark $v$ and all vertices of degree other than two. If there are $a$ marks, there are $a-1$ segments between marks. Root at $v$, label every mark zero and use the walks on the segments away from $v$. The vertex vector is the edge vector plus $e_0$, since every nonroot vertex is counted exactly once as an arrival. The vertex count at any residue is at most
$$
1+(|B|-1)/k+2(a-1).
$$
The same statement holds for a single vertex with no segments. Thus at least $2k(a-1)+k$ additional leaves at the zero-labeled $v$ suffice: after their addition the floor of the average vertex count is at least every old count. Fill to a balanced vertex target with bin zero high if there is any high bin. The final edge vector differs only by subtracting $e_0$, so it too is balanced.

## The high-degree tree

Choose $v$ of degree $\Delta\ge4k^2$ and take $S$ to be $v$ and all its neighbors. Use the protected leaf deletion above, and let $e\le k-1$ count the leaves of $C$ outside $S$. Each neighbor of $v$ that still has a nontrivial descendant branch accounts for at least one different such leaf. Remove the $P\ge\Delta-e$ remaining leaf neighbors of $v$, obtaining $B$. If $e=0$ the core is a star. Otherwise $B$ has at most $e+1$ leaves, including $v$ if it becomes a leaf. A tree with $l$ leaves has at most $2l-2$ vertices of degree other than two, by the degree sum. Marking $v$ as well gives $a-1\le2e$. Now $P\ge4k^2-e\ge4ke+k\ge2k(a-1)+k$. The segment construction labels $C$, and restoring the deleted batches labels $T$.

The checker constructs the labeling on the reduced core and tests the closure of both segment walks for every length through 100 and modulus through 24. On small moduli it also restores the outside leaves and checks the whole original tree. [Direct construction checks](../large_order_degree.py)

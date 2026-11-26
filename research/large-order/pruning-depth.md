# Subquadratic maximum degree for every counterexample

**Theorem.** For every $\gamma>0$ and all sufficiently large $k$, a tree with a vertex of degree at least $k^{3/2+\gamma}$ is $k$-cordial. Equivalently, the maximum degree of any counterexample is at most $k^{3/2+o(1)}$. There is no hypothesis on its order.

**Pruning lemma.** Let $B$ be a rooted tree of order $b$ with at most $k$ rooted terminals different from its root. Adjoin $P$ leaves at the root. If
$$
P\ge k\big(5\lceil\sqrt b\rceil+2\big),
$$
the enlarged tree is $k$-cordial.

Set $H=\lceil\sqrt b\rceil$. First remove $(b+P-1)\bmod k$ of the added leaves. The remaining order is $1\bmod k$. In each of at most $H$ rounds remove all nonroot terminals of the current $B$, together with enough of the added leaves to make a batch of $k$. Stop if only the root of $B$ remains. Terminal counts cannot increase: each newly terminal nonroot parent had a different removed child. In every batch all parents survive, so [Hall's leaf extension](../counterexample-bound.md#removing-leaves) will restore the batches in reverse. The initial shorter batch is restored last.

If a nonroot vertex survives $H$ synchronous rounds then its original descendant subtree had height at least $H$, by induction on the rounds. Distinct residual terminals have disjoint original descendant trees. The number $e$ of nonroot terminals remaining is therefore at most $b/(H+1)\le H$. The root-alone case has $e=0$. Mark the root and every vertex of undirected degree different from two. There are at most $2e$ segments between marks: the tree has at most $e+1$ undirected leaves, and the root contributes at most one extra mark. The [closed segment walks](high-degree.md#labeling-segments-with-zero-endpoints) therefore give a cordial labeling as soon as at least $4ke+k$ added leaves are left. The pruning spent at most $(H+1)k$ of them, so the displayed hypothesis suffices. This proves the lemma, including restoration of the original tree.

**Proof of the theorem.** Protect the star consisting of a vertex of degree $\Delta$ and all its neighbors, and perform the [protected leaf deletion](high-degree.md#preserving-a-connected-subtree-while-removing-leaves). In the remaining core at most $k-1$ branches still have vertices beyond that star, since the total number of leaves outside it is less than $k$. Remove the $P\ge\Delta-(k-1)$ leaf neighbors at the vertex. The remaining rooted tree $B$ has at most $k-1$ nonroot terminals and $E_3(B)\le k$. It is a connected subtree of the original tree.

Fix $0<\eta<2\gamma$. If $b=|B|\ge k^{1+\eta}$, the [protected subtree proposition](balls.md#protecting-large-branches-with-small-total-degree-excess) already labels the entire tree: $E_3(B)\le k\le b^{1/(1+\eta)}$. Otherwise $k(5\lceil\sqrt b\rceil+2)=O(k^{3/2+\eta/2})$. For sufficiently large $k$ this is at most $\Delta-(k-1)$. The pruning lemma labels the core. Restoring the protected deletion batches finishes the whole tree.

The [construction check](../large_order_pruning.py) forms both labeling histograms on 105 entire trees after restoring 634 batches. In 83 cases the residual core after the depth cutoff still had nonroot vertices.

~~~sh
python3 -B -m research.large_order_pruning
~~~

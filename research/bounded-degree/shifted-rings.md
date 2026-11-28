# Exact shifted edge weights on a sparse perturbation of a unicyclic graph

**Theorem.** Fix $D\ge3$ and $0<\epsilon<1$. For every sufficiently large $k$, let $R$ be a simple connected unicyclic graph on $k$ vertices. Give each edge an offset $\delta_e\in G=\mathbb Z_k$, with at most $b$ exceptions to one common offset. Suppose $E_D(R)+b\le k^{1-\epsilon}$. Write $B=\sum_e\delta_e$, $S=\sum_{x\in G}x$ and $C=S+B$.

A bijection $x:V(R)\to G$ with every adjusted weight $x_u+x_v+\delta_{uv}$ occurring once exists exactly under the following conditions.

| Leaves of $R$ | Necessary and sufficient condition |
|---|---|
| None | $C=0$. |
| One | $C\ne0$. If the pendant path has length two, with junction $j$, middle vertex $z$ and leaf $y$, also require $C+\delta_{zy}-\delta_{jz}\ne0$. |
| At least two | $\gcd(k,\deg_R(v)-1:v\in V(R))$ divides $B$. |

At **every odd modulus $k\ge5$** the length-two obstruction already occurs with one nonzero offset. Take a cycle of length $k-2$, attach $jzy$ at $j$, and give only $jz$ a nonzero offset $d$. Then any bijection with all weights distinct would have $x_y=x_j+d$. The two edges incident to $z$ would have the same weight. This is an obstruction to a shifted unicyclic graph. The ordinary tree conjecture remains open.

## Necessary moments

The sum of the weights is $\sum_v d_R(v)x_v+B$. Subtract the vertex sum $S$ once or twice to obtain
$$
       \sum_v(d_R(v)-1)x_v=-B,\qquad
       \sum_v(d_R(v)-2)x_v=-C.
$$
The first identity gives the gcd test. On a cycle the second gives $C=0$. With one leaf there is one junction of degree three and all other vertices have degree two except the leaf. Thus $x_y=x_j+C$. Distinct vertices need $C\ne0$. On the two-edge tail, subtraction of its two edge weights gives the additional condition in the table. Since $R$ has $k$ edges, normalizing the common offset to zero preserves $B$ and every displayed condition.

## Reduction to a tree with a prescribed missing weight

Open an arbitrary cycle edge $e_0=uv$ of adjusted weight $W_0=X_u+X_v+\delta_{e_0}$. In the resulting spanning tree perform the [paired cut construction](sparse-offset-growth.md#a-bijective-rainbow-base-with-sparse-offsets). Cut its shifted edges and enough additional edges to cap its degrees at $D$. There are $c\le b+E_D(R)$ main cuts. Mark both ends of each main cut and of $e_0$. The additional marks and reserved vertices for the two cases below are chosen before cutting the private partners. The partners form an induced matching away from marks and reserves. Sites are independent and away from all these endpoints in the original graph. The closing edge already has marked endpoints, so taking the neighborhoods in the spanning tree makes the same exclusions at every eligible site.

Reconnect the pieces to a bounded-degree tree $U$ using the exchanged weights of each main cut and its private partner. The new sites carry the same three-variable affine labels as in the tree construction. Let $P$ include all marked vertices, private endpoints and used sites. For any assignment respecting the pins, the full adjusted weight multiset of $R$ equals the ordinary weight multiset of $U$ together with $W_0$. In particular, the induced weights of $U[P]$ together with $W_0$ are exactly the adjusted edges between the marked original vertices, including the private endpoints. The goal on $U$ is therefore a bijection with missing weight $W_0$.

### Reserving two free leaves

When at least two original leaves remain unmarked, reserve two. Some degree $d$ between two and $D$ occurs on $\Omega_D(k)$ vertices of $R$. Indeed $\sum(d_R-1)=k$, and vertices above $D$ contribute $O_D(E_D(R))=o(k)$. Put $g=\gcd(k,d-1)$. For each nonzero residue of $d_R(v)-1$ modulo $g$ choose one representative vertex and mark it. These representatives cannot be reserved leaves. Choose sites only from the abundant degree $d$. There are still $\Omega_D(k)$ independent eligible sites outside the forbidden neighborhoods and only $O(c+1)$ are used. In particular, an untouched unpinned degree-$d$ vertex remains in $U$.

Choose the representative labels modulo $g$ so that their weighted sum with coefficients $d_R(v)-1$ is $-B$ modulo $g$. This is possible by the stated gcd test, since the original coefficients include $d-1$ and their gcd with $g$ equals their gcd with $k$. Constrain every other independent marked variable to be zero modulo $g$. The affine site labels can take other residues, but each site has original coefficient $d-1$, divisible by $g$. It follows that $\sum_{v\in P}(d_R(v)-1)x_v+B=0\pmod g$.

Assign actual residues with all pins distinct and all induced adjusted weights, including $W_0$, distinct. The [parent-order greedy proof](sparse-offset-growth.md#a-bijective-rainbow-base-with-sparse-offsets) applies within the prescribed congruence classes. There are $O_D(c+1)$ forbidden values at each variable and $k/g$ available before exclusions. For the weights, the extra closing edge has just $O(c+1)$ comparisons in total. Its unordered endpoints differ from those of every other edge because $R$ is simple. All coefficients in these differences have absolute value at most two.

All changed degrees belong to $P$. By summing the edge replacement identities,
$$
  \sum_{v\in P}(d_U(v)-1)x_v+W_0
      =\sum_{v\in P}(d_R(v)-1)x_v+B.
$$
The gcd of $k$ and the unpinned coefficients $d_U(v)-1$ divides $g$, since an unpinned degree-$d$ vertex remains. The two reserved vertices are still leaves. The [two-free-leaf completion criterion](partial-gap.md) on $U$ is therefore satisfied with missing weight $W_0$.

### Exhausting the exceptional degrees

Otherwise $R$ has $O(c+1)$ leaves and at most as many branching vertices, since $\sum(d_R-2)=0$. Mark all of them. Private endpoints are now of original degree two, because they were chosen outside the marks. Every unpinned vertex of $U$ has degree two. The [exhausted-degree completion criterion](partial-gap.md#few-free-leaves-and-the-primitive-moment) requires $\sum_{v\in P}(d_U(v)-2)x_v=-S-W_0$. By the same replacement identity this is precisely $\sum_v(d_R(v)-2)x_v=-C$. Its coefficients are supported on original marks.

On a cycle this equation holds by hypothesis. With one leaf substitute $X_y=X_j+C$ in the label and edge expressions. The only potentially identical individual vertex forms are $X_j$ and $X_y$, and the nonzero $C$ separates them. Among ordinary edge forms, only the leaf edge changes its variables on substitution. It could have the same variable pair as another edge only when $y$ and $j$ have a common neighbor $z$. This is exactly the length-two tail. The additional condition distinguishes those two weights. A leaf adjacent directly to $j$ produces the unique doubled variable. All site expressions retain their private coefficients unchanged. The substituted leaf edge and closing edge contribute only $O(c+1)$ extra comparisons.

With at least two leaves, choose leaves $p,y$ and eliminate $X_y$ using the moment:
$$
        X_y=C-X_p+\sum_{v\ne p,y}(d_R(v)-2)X_v .
$$
Order the remaining independent variables first in parent-before-child order of the spanning tree, with private variables moved after the ordinary ones and $X_p$ placed last. Neither private variables nor sites occur in the sum above.

Every individual comparison of two original edge weights that involves $p$ or $y$ has a surviving coefficient $\pm1$ or $\pm2$ on $X_p$. Each leaf occurs in exactly one edge, and these two edges are distinct. All other edge comparisons have the earlier greedy bound, including the one extra closing edge. For vertices, each of $p,y$ occurs in only a bounded number of original label expressions before substitution: besides its own label, at most one main edge uses it and it is the child of at most one cut. Thus there are $O(c+1)$ comparisons involving these expressions. If the coefficient of $X_p$ cancels, a comparison involving a site still has a private variable, with final coefficient of absolute value at most two. Indeed the nonzero private coefficient vectors for one pair are $e_s,e_t,e_s+e_t,-e_t$, all distinct, and eliminating $X_y$ does not affect them. Without a site or private term, a comparison involving one of these two leaves against any different individual label has a nonzero coefficient on $X_p$. Hence large branching coefficients in the substituted sum never decide one of these comparisons. All remaining inequalities are the ordinary greedy ones. The same argument without elimination covers the cycle case. This constructs distinct pins and distinct original induced weights satisfying the moment.

In either case $U$ has maximum degree at most $D+2$ and $|P|=O_D(c+1)=O_D(k^{1-\epsilon}+1)$. The partial-labeling criterion gives the required full bijection for sufficiently large $k$. Restoring the cut edges and the closing edge supplies all $k$ adjusted weights. The external input in that criterion is [Müyesser and Pokrovskiy, Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4).

## Inserting a period into a tree with edge offsets

Open a cycle edge $uv$ of offset $\gamma$ in a graph with the bijection just proved. Replace an old edge $ab$ of offset $\delta$ by the opened graph, attaching $a$ to $u$ with offset $\alpha$ and $v$ to $b$ with offset $\beta$. If $\gamma=\alpha+\beta-\delta$, every old label is preserved and both histograms gain one in every bin. In fact translate the new graph by $x_a+\delta-\beta-x_v$. The edge at $b$ now has the old weight and the edge at $a$ has the translated cycle weight that was removed. All other new weights translate by twice the same constant. There is no restriction on degrees, offsets, label frequencies or attachment sites of the old graph.

The cycle criterion also extends to length $qk$ for any positive $q$. Partition the vertices cyclically into blocks of $k$. In each block suppose the $k-1$ internal offsets have at most $k^{1-\epsilon}$ exceptions to some constant, which may depend on the block. The offsets on the edges between blocks are unrestricted. Then both histograms can be uniform exactly when the total offset is $-qS$.

Indeed, the [sparse path base](sparse-offset-growth.md#a-bijective-rainbow-base-with-sparse-offsets) supplies a permutation with distinct internal weights on each block. To insert such a block between old ends $a,b$, translate the permutation until the first entering edge fills its translated missing weight. If the path offsets including the two outside edges are $d_1,\ldots,d_{k+1}$, summing its first $k$ weights shows that the final new vertex has label $x_a+S+\sum_{i=1}^kd_i$. Thus the last edge exactly replaces an old edge of offset $S+\sum_{i=1}^{k+1}d_i$. Compress $q-1$ blocks using this rule. The last $k$-cycle has total shift $-S$ and at most one extra exceptional edge beyond its internal path. Its bijection follows from the cycle case above (decrease the exponent slightly to absorb one extra edge). Reinsert the blocks in reverse. Necessity follows by summing all original degree-two incidences. [The same compression identity for arbitrary shifts at primes](../biased/prime-paths.md)

## Paths and simultaneous growth orders

For a path on at least $k+1$ vertices, suppose one fixed labeling is to be cordial on **every connected interval**, allowing independent edge offsets. Each window of $k$ vertices must be a permutation of $G$. Successive windows force the vertex sequence to be $k$-periodic. Each window of $k$ edges must also be a permutation, so the edge sequence and hence the offset sequence must repeat with period $k$ wherever both positions occur. Conversely, these periodicity conditions and a bijective rainbow labeling of the one-period shifted cycle suffice, since every interval of a repeated permutation has balanced counts. At all sufficiently large $k$, if one period has at most $k^{1-\epsilon}$ exceptions to a common offset, the criterion is exactly periodicity and $\sum_{i=1}^k\delta_i=-S$. At odd moduli ordinary paths have the explicit sequence $x_i=i\pmod k$.

For ordinary trees on at least $k+1$ vertices, $k\ge2$, one labeling works on every connected subtree exactly for **paths at odd modulus**. At even $k$ the ordinary cycle sum prevents such a path. For $k\ge3$ any branching tree has a connected $(k+1)$-vertex subtree containing a vertex of degree at least three within it: start with that vertex and three neighbors and grow the connected set. The subtree has exactly one repeated pair of labels, but deleting any of its three or more leaves must give a permutation. Every leaf would have to belong to that pair. At $k=2$ even a three-vertex path fails, since its two edge sums would agree. This simultaneous condition is stronger than choosing a labeling for a given growth order.

## Verification

~~~sh
python3 -B research/bounded-degree/check_shifted_ring.py
python3 -B research/bounded-degree/check_sparse_offsets.py
~~~

The [constructor](shifted_ring.py) builds the auxiliary tree and the small degree-core embedding. The [independent checker](check_shifted_ring.py) recomputes all changed edge weights and both embedding sums. It exercises cycles, pendant paths, adjacent branching vertices, degree gcds two and three, and graphs having an abundant degree with an exceptional residue at another degree. Across 260 large instances it verifies 204 degree cores and rejects 56 impossible targets. On small graphs through order eight it finds 635 actual bijections, confirms 232 forced failures, and verifies the histogram increments for 3,161 opened cycle edges. The small cases include additional failures below the asymptotic range.

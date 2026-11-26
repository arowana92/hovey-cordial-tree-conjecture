# A constant number of edge-weight corrections at every modulus

**Theorem.** Fix $D\ge3$ and $s\ge1$. There is a constant $C(D,s)$ such that for every positive integer $k$ and every tree with at most $s$ vertices of degree greater than $D$, there is a vertex labeling modulo $k$ with the following properties.

- The vertex label counts are balanced.
- One can change the recorded weights of at most $C(D,s)$ edges to make the edge counts balanced. Before a change each edge has its actual endpoint sum, and changing a recorded weight does not change any vertex label.

In particular, at order $k$ a bijection of the vertices gives at least $k-1-C(D,s)$ **distinct actual edge sums**. This includes prime $k$. The exceptional vertices can be arbitrarily far apart. The bound measures the remaining error in the ordinary cordiality problem. Exact cordiality requires that the actual sums already balance.

## A common set of intervals for the direct leaves

We use the following elementary sampling fact. Fix integers $A,B\ge1$ and $0<\eta<1$. There are an integer $M$ and $c>0$ depending only on these parameters such that for all large $k$ there is a union $S$ of at most $M$ cyclic intervals, of size at least $(1-\eta)k$, with the following property. For every list of at most $B$ maps $x\mapsto a_i x+b_i$ on $\mathbb Z_k$ with $1\le |a_i|\le A$, at least $ck$ choices of $x$ put **every image and its neighborhood of radius $\lfloor k/M\rfloor$** outside $S$.

For a proof divide the unit circle into $M$ equal half-open cells with indices in $\mathbb Z_M$. Independently mark each cell ordinary with probability $\eta/2$. The other cells will comprise $S$, interpreting a residue $y$ as the point $y/k$. For a given coefficient list record just the cells $c_i=\lfloor M b_i/k\rfloor$ of the intercepts. If the parameter is in cell $j$, all possible image cells, even after a perturbation of at most $1/M$ on the unit circle, have indices
$$
a_i j+c_i+e,\qquad |e|\le A+3 .
$$
It suffices that these at most $K=B(2A+7)$ cells are all ordinary. The probability is at least $(\eta/2)^K$. A specified cell occurs in at most $AK$ of the trials indexed by $j$, since a congruence with coefficient $a_i$ has at most $|a_i|$ solutions. Greedy disjoint selection leaves at least $M/(AK^2+1)$ independent trials. A binomial lower-tail bound gives a positive proportion of successful cells except with probability $\exp(-\Omega_{A,B,\eta}(M))$. There are at most $(1+2AM)^B$ coefficient and intercept-cell lists. Choose $M$ sufficiently large and use a union bound. At the same time the ordinary fraction is less than $3\eta/4$ with probability tending to one. Each cell contains $k/M+O(1)$ residues. This proves both assertions for large $k$. Removing boundedly many individual points from $S$ changes its number of intervals by a bounded amount and preserves the avoidance property.

## Many copies of a short branch in two intervals per vertex

Let $B_0$ be a fixed rooted branch of order $m$. For $2w$ equal copies, where $w=2u+1$ is odd, choose a [signed template](signed-tree.md) with nonzero integer labels $x_v$ of distinct magnitudes at most $81m$. Use the two signs and $w$ copies of each sign. At vertex $v$ use exactly the interval
$$
\sigma\lambda x_v+[-u,u]
$$
across copies with sign $\sigma$. At each edge this can be done so its weights also fill an interval of this same length, centered at $\sigma\lambda(x_v+x_{\rm parent})$. In fact, if the parent's offset is $i-u$ for $0\le i<w$, give the child offset $((i+u)\bmod w)-u$. Both offsets range bijectively over $[-u,u]$. Their ordinary integer sum ranges over $-u,-u+2,\ldots,u$ for $i\le u$ and the intervening parity for $i>u$. Recursing down the tree assigns all vertices, with any initial enumeration of the root offsets.

Both signs together now supply exactly the nonroot vertex intervals as the weights of the internal edges. At an external parent with label $p\in\{0,\ldots,s-1\}$, the two root intervals are translated by $p$ as edge weights. On each translated interval at most $p$ actual entries need changing to get back the unshifted interval. Thus all but at most $2p$ weights can be kept in a bijection of the new weights onto the new vertex labels, regardless of the multiplicity. This argument applies at every modulus once the vertex intervals have been placed disjointly.

Place all such collections before the other ordinary vertices. Their number and the number of intervals per collection below are bounded in terms of $D,s$. Apply the sampling fact to the finitely many maps $\lambda\mapsto\pm x_v\lambda$ for one collection. Take $w\le h<\delta k$ with $\delta<1/M$, where $h$ is the total ordinary order. The full intervals are outside $S$ on at least $ck$ choices of $\lambda$. Intersections of two intervals of lengths $w,w'$ require a difference of centers in a cyclic interval with at most $w+w'-1$ residues. For two new centers the slopes differ, and against an old interval the new slope is nonzero. Thus the number of parameters excluded by each comparison is at most $162m(w+w')$, including at composite $k$. Old site labels are singleton intervals. Summing the exclusions over boundedly many pairs costs $O_{D,s}(h+1)$ parameters. This is why all the interval collections are placed before any large set of scattered ordinary labels. Decrease $\delta$ further so some allowable parameter remains.

## Labeling the ordinary tree

Take the vertices above degree $D$ as the sites. If there are none, the bounded-degree theorem applies at large $k$. Strip all leaves adjacent to sites to obtain the ordinary tree $H$. For $h=|H|\ge\delta k$ the [positive-density theorem](concentrated-leaves.md) gives exact cordiality. Only sites can be high ordinary vertices or newly created leaves. An original leaf adjacent to an ordinary high vertex was removed. Thus the count of ordinary leaves at ordinary high vertices is at most $s$.

In the sparse range first take total order exactly $k$. Assign the sites distinct labels $0,\ldots,t-1$ for $t\le s$ sites, giving zero to a site of largest direct population. Partition $H$ by simultaneous breadth-first search from the sites, retaining the edge by which each nonsite is first reached. This gives $t$ rooted trees and leaves exactly $t-1$ actual edges between them. Every nonroot has bounded degree. At the end the crossing edges can be assigned the distinct reference weights of the nonzero sites at a cost of at most $t-1$ corrections.

In each rooted component consider the root branches of height below ten, measured in vertices excluding the site. Their orders and the number of their rooted shapes are bounded. For each site and shape put as many copies as possible in a single collection of size $2w$, $w$ odd, leaving at most three. Use the interval construction on all these collections. Choose the sampling parameters $A,B$ above large enough for the intervals and for the bounded affine batches below. Take $\eta<1/(2s)$, and remove the site labels from $S$.

In each component process the unassigned branches by the [ten-vertex neutral batch](linear-hub-batches.md#absorbing-an-entire-bounded-forest-at-once). If a branch has height at least ten, take ten vertices on a longest downward path from its top. Also take all currently exposed short branches in full. Initially only boundedly many short branches remain. At most $10D$ new short branches are exposed by each step, since none of the previous short ones remain. Thus each batch has bounded size. The batch identity handles arbitrary assigned parent labels and adds the same multiset to labels and actual weights. Its moving affine forms have nonzero slopes bounded by a constant in the batch size, with distinct intercepts for equal slopes. Apply the sampling fact to avoid $S$, and exclude any collisions with old labels or within the batch. Each unequal-slope comparison again excludes a bounded number of parameters. There are only $O_{D,s}(h+1)$ exclusions, so sufficiently small fixed $\delta$ suffices. The same common palette works for every batch and all the intervals.

When a component runs out of tall branches, only boundedly many vertices remain. Give them unused labels outside $S$ and assign their incoming edges their own labels as reference weights, costing at most one correction per vertex. The ordinary reference weights now comprise all ordinary vertex labels except zero. All costs so far are bounded in terms of $D,s$, independently of $h,k$ and of every leaf population.

## Restoring leaves and passing to every order

At order $k$ the nonzero sites together need at most $(1-1/s)(k-h)$ leaves, which fit inside $S$. In numerical order use a prefix of the available $S$ labels for each nonzero site's population in succession. Each site's assigned labels form a union of at most $M+s+2$ ordinary integer intervals. On each interval at most the site label, hence at most $s-1$, actual weights need changing to have the unshifted interval as reference weights. Give all remaining labels to the leaves at zero, for which the own-label reference weights are exact. This proves a bijection with $k-1$ distinct reference weights and only boundedly many changed actual weights.

At order below $k$ in the sparse range pad at a site, then restrict both the labeling and the distinct reference weights to the original tree. For $n>k$ remove one direct leaf at $n\equiv1\pmod k$ or otherwise $(n-1)\bmod k$ direct leaves. The remaining order is at least $k>h$, so there are enough direct leaves. Carry along the previously corrected weights. When the target order is $1\bmod k$, the prefix has order divisible by $k$, so its vertex counts are uniform and exactly one **reference** weight is deficient. Subtract the parent label from that weight to obtain the restored leaf label. In the other case the prefix has uniform reference frequencies and one surplus vertex label. The [distinct-leaf lemma](../counterexample-bound.md#removing-leaves) extends using the actual parent shifts. Every new reference weight equals its actual endpoint sum in both steps. Consequently the bound on the number of corrections never grows with the induction depth.

This proves the uniform bound at sufficiently large $k$. There are finitely many smaller moduli, and at each one the [general large-order theorem](../large-order/linear.md) gives exact cordiality for all sufficiently large orders. On the remaining finitely many trees use any balanced vertex labeling and correct as many weights as necessary. Taking one common constant proves the stated quantifiers.

## Reproduction

The checker compares actual vertex and weight multiplicities for 1,360 signed interval collections. It checks 43,248 fine-coordinate bounds for positive and negative slopes. It then builds 18 complete order-$k$ trees at prime, composite and power-of-two moduli with nonadjacent sites. It computes corrected weights directly from the original edges and verifies the predicted bound. These finite examples exercise the sparse construction. The common palette and the uniform correction bound for arbitrarily large trees follow from the proofs above. [Constructor](bounded_error.py) · [Independent verifier](check_bounded_error.py)

~~~sh
python3 -B -m research.hub.check_bounded_error
python3 -B -m research.hub.check_linear_hub_batches
~~~

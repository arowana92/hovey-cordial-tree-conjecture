# One more leaf beyond the three-group reduction

**Finite reduction.** Suppose the order-$k$ base and the ordered-cut forest certificate with at most $q$ tips are valid, where $q\ge2$ and $k\ge5$. Within trees with at most $2q+2$ leaves, a least counterexample has order at most $4k$ for odd $k$ and at most $5k$ for even $k$. If $q$ is even, a least counterexample above $2k$ in this class has exactly $2q+2$ leaves and a path of edges, each of which splits its leaves equally.

At 27 labels this gives 108 as an initial upper bound for fourteen leaves. With the [six-tip and numerical profile certificates](leaf-profile-cuts.md), a least failure among trees with at most fourteen leaves can occur only at orders **50–54 or 81**. The later [seven-tip theorem](../rainbow/seven-tip-27.md) excludes order 81 by the three-group argument, and [centroid profiles](leaf-profile-cuts.md) further narrow the range. The proof below separately excludes 104–108 using six tips alone.

## The edges splitting $2q+2$ leaves equally

The [three-group theorem](../rainbow/few-leaves.md#a-finite-reduction-for-eleven-leaves) handles at most $2q+1$ leaves beyond order $2k$. Consider a least failure with exactly $2q+2$ leaves and order $n=mk+1+t$, $1\le t<k$. The other order residue is covered by deleting one leaf. At any vertex, a union of whole branches with at most $q$ original leaves has fewer than $t$ vertices. Otherwise keep the vertex and the other branches, grow the core to $mk+1$ in size-ordered preorder, and restore the exterior using the $q$-tip certificate with padding.

First suppose no edge splits the leaves into two equal parts. At a leaf centroid, all branches have at most $q$ leaves. Merge groups as long as their combined leaf count is at most $q$. Any two final groups have at least $q+1$ leaves between them. Five groups would contain two disjoint pairs and an extra leaf, impossible. With exactly four, every pair and its complement must each have exactly $q+1$ leaves. Hence all four group counts are $(q+1)/2$, possible only for odd $q$. With three or fewer groups, $n-1\le3(t-1)$ gives $m<2$. With four, $n-1\le4(t-1)$ gives $m<3$.

Now suppose such an edge exists. The equally splitting edges form a connected path. Indeed, every edge between two of them has at least $q+1$ leaves on each side, and a branching of these edges would require three disjoint sets of $q+1$ leaves. An internal vertex of the path has degree two even in the original tree, since the two directions already account for all original leaves. At each endpoint the outward branches have exactly $q+1$ leaves together and at most $q$ individually. They can be merged down to two groups of at most $q$ leaves: three final groups would have one pair with at least $q+1$ and at least one further leaf. All four endpoint groups have fewer than $t$ vertices.

Put $p=k$ at odd modulus and $p=2k$ at even modulus. The path has at most $p$ edges, since otherwise its interior contains $p$ consecutive degree-two vertices that can be suppressed and restored with uniform increments. The smaller tree retains all its leaves. Thus
$$
                n\le 4(t-1)+p+1,\qquad mk\le3t-4+p.
$$
This gives $m\le3$ for odd $k$ and $m\le4$ for even $k$, proving the reduction. [Explicit period subdivisions](../counterexample-bound.md#shortening-paths)

## Fourteen leaves at 27

The [order residue bound](../rainbow/twenty-one-free.md#twenty-one-exterior-vertices-at-27-labels) leaves $t=22,23,24,25,26$. Within this leaf-limited class the reductions used for that bound still apply, since connected cores have at most as many leaves as the original tree. Above 54 it suffices to examine $n=55+t$ and $n=82+t$, each with an equally splitting path.

At either endpoint record the pairs $(s,j)$ of order and tip count of its outward branches. They have $\sum j=7$ and $1\le j\le6$. Write $S=\sum s$. Every proper subset of the branches has at most six tips. Consequently $S-\min s<t$. There are at least two branches, each with $s<t$ and $j\le\max(1,s-1)$. These conditions also give $S\le2(t-1)$.

Discard an endpoint profile whenever its outward branches admit a certified $t$-vertex cut using a set of whole branches and a suffix in one other branch. The untouched part of the tree, including the path and other endpoint, is part of the core. The [profile cut proof](leaf-profile-cuts.md#selecting-a-cut-from-the-numerical-branch-data) and its actual boundary inequalities apply for every core order one modulo 27.

Two remaining profiles of masses $a,b$ determine the number $h=n-a-b-2$ of internal vertices of the equally splitting path. Require $0\le h<27$. Its edge cuts give side orders $a+1,a+2,\ldots,a+h+1$. If any is congruent to $0$ or $n$ modulo 27, an edge splits off a divisible-order component. Both components are smaller trees in the class and the [divisible-cut theorem](../divisible-cuts.md) rules this out.

One more test uses the actual unicyclic certificates. At an endpoint of mass $S$ choose an outgoing branch $(s,j)$. Keep the other outgoing branches, the endpoint, and $i=26-S+s$ internal path vertices immediately following it. If $2\le i\le h$ this middle piece has exactly 27 vertices and two distinct ports at distance at least two. Closing the ports gives a simple unicyclic graph whose leaves are the $7-j$ original leaves on those retained outward branches. For $2\le7-j\le6$ the [ring theorem](few-leaf-rings.md) supplies an edge replacement with equal increments to all bins. The smaller tree again lies in the leaf class. Thus either endpoint can rule out a pair of profiles.

| $t$ | Possible endpoint profiles | After six-tip cuts alone | Possible endpoint pairs at $82+t$ | After available profile cuts | Possible endpoint pairs at $55+t$ |
|---:|---:|---:|---:|---:|---:|
| 22 | 12,252 | 11,098 | 0 | 10,535 | 0 |
| 23 | 15,393 | 14,036 | 0 | 13,161 | 0 |
| 24 | 19,120 | 17,533 | 0 | 16,240 | 0 |
| 25 | 23,572 | 21,727 | 0 | 20,013 | 0 |
| 26 | 28,782 | 26,649 | 0 | pending | pending |

The [checker](check_leaf_corridor.py) first generates the endpoint profiles in increasing tip counts. It independently regenerates the same complete sets by exact order and decreasing branch size with subset-mass masks. It tests each possible pair of masses and possible corridor length after all local reductions. On 800 actual trees with the relevant even leaf counts it also verifies the structure of the balanced path or the group count at a centroid. The published profile manifests can be regenerated and their label coverage verified by the [stream reproduction](leaf-profile-cuts.md#reproduction).

~~~sh
python3 -B -m research.census.check_leaf_corridor --through 53
~~~

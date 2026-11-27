# Attaching two-edge paths while avoiding a specified vertex residue

**Theorem.** At every odd modulus $k$, any number of two-edge paths can be attached at a single vertex of a prescribed cordial core of order one modulo $k$, preserving every old label. More precisely, at a common parent of label zero, $(k-1)/2$ such paths can use every vertex label except an arbitrarily specified $y$, with distinct weights on all their edges.

The [divisible-core construction](regular-joints.md) already covers cores of order zero modulo $k$ with at least three paths. One or two paths form a caterpillar with the joint and also satisfy the short constructions below when $k\ge5$. The core of order one has a prescribed surplus vertex label and uniform edge counts. The omitted label must consequently be available at every relative position with respect to the parent.

## Choosing the omitted vertex

Use the [two-site construction](two-site-arms.md) and its notation for the center and tip labels on each path. Modulus one is immediate. At $y=0$ the nonzero-residue construction there supplies all paths, except at $k=3$. At three use the path with labels $(1,2)$ and weights $1,0$.

Suppose $y$ is a unit. If $k=4h-1$, the coincident-parent block has singleton label $3h-1=-h\pmod k$, which is a unit. Delete this singleton. If $k=4h+1$, use intermediate labels $I=[1-h,h]$ and complementary interval $J=[h+1,3h+1]$. On its indices use $j\mapsto (2j+1)\bmod(2h+1)$. The displacements range over $[-h,h]$. Indeed, for $0\le j<h$ they are $j+1$, and for $h\le j\le2h$ they are $j-2h$. Delete the slot $j=h$ of displacement $-h$. The surviving slots and displacements give the paths and their distinct weights, and the omitted vertex label is $2h+1$, a unit. In either case multiplication by a unit gives the requested $y$.

Write $g=\gcd(k,y)$ for nonzero $y$. If $g\ne3$, use the unit construction modulo $k/g$ with omitted label $y/g$. Multiply by $g$ and fill all nonzero cosets modulo $g$ with the complete two-edge arm blocks from the two-site theorem. Precisely one vertex label is still omitted and all the weights are distinct.

For $g=3$ scale the prescribed hole to three. Two integer seeds have the following paths.

| Interval | Paths $(\text{intermediate},\text{tip})$ | Missing weight |
| --- | --- | ---: |
| $[-3,3]$ | $(-2,-1),\ (0,1),\ (2,-3)$ | 3 |
| $[-4,4]$ | $(-4,1),\ (0,-2),\ (2,-3),\ (4,-1)$ | 1 |

Each vertex interval omits three. The signed Langford enlargement fills exactly the same new interval positions for the vertices and the weights. It leaves both old holes available, even when they differ. As before this covers $7+4s$ for $s\ge7$, $9+4s$ for $s\ge9$, and the seed at nine. The [explicit rows](two-site-arm-seeds.json) handle 15, 21, 27 and 33. Scaling back completes the proof of the omitted-vertex assertion.

## An arbitrary number of paths

Subtract the old parent label for the duration of the proof. Every group of $k$ paths can use $(j,j)$ for $j\in\mathbb Z_k$ and adds two copies of every vertex and edge residue. Fewer than $k$ paths remain. Write $b=(k-1)/2$. For at most $b$ paths use a subset of the omitted-vertex construction, avoiding the old vertex surplus. All added labels and weights are distinct.

If more than $b$ remain, first use all $b$ paths. The core is now divisible, with a unique deficient edge weight $D$. For any $1\le r\le b$ further paths it suffices to give distinct vertex labels and distinct weights including $D$. There are two full $b$-path rows with different omitted weights. At $k=4h-1$, delete the singleton in the coincident-parent row and in its negative. Their omitted weights are $-h$ and $h$. At $k=4h+1$, the nonzero row omits zero. The original doubling row with singleton parent $-h$ and singleton label $2h+2$ omits $h+2\not\equiv0\pmod k$ upon deleting the singleton. One of the two rows hits $D$. Keep the path hitting it and any $r-1$ others. Restoring the translation proves the theorem.

## A restriction at each order residue

Let a smallest counterexample at an odd modulus have order $qk+s$, $2\le s\le k$. At each vertex it has at most **$\lfloor(s-2)/2\rfloor$ pendant paths of length two**, each with a degree-two intermediate vertex and a leaf tip. For odd $s$, removing $(s-1)/2$ paths leaves a smaller tree of order one modulo $k$. Restore them by the omitted-vertex theorem. For even $s$, removing $s/2$ paths leaves a divisible core. Restore them by the short construction hitting its edge deficit. All removals retain the joint. This sharpens the modulus-only restriction whenever the order residue is smaller.

There is also a sufficient bound for constructing larger trees. Start with any $n$-vertex tree and attach at least $(n-1)(k-1)/2$ two-edge paths at one vertex. The result is $k$-cordial for every odd $k$ satisfying this inequality. Begin at that vertex alone. Add the $n-1$ original vertices in parent-before-child order, accompanying each by $(k-1)/2$ paths at the joint using the two-site theorem. The resulting order is one modulo $k$. The surplus extension adds all remaining paths.

The [constructor](two_site_arms.py) labels the full graft. The [checker](check_surplus_arms.py) tests 2,656 prescribed holes and 7,854 complete trees, with old path and star cores, recomputing all bins and checking that the core labels stay fixed. Its large-modulus cases include modulus 65,535.

~~~bash
python3 -B -m research.census.check_surplus_arms
~~~

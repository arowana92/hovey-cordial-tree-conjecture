# Near-perfect matchings at 26 labels and cordial labelings on every prefix

**Theorem.** Every finite tree with a matching leaving at most one vertex uncovered is 26-cordial, at every tree order. More generally, let $m\in\{3,5,7,11,13\}$, let $\nu$ be the maximum matching size of a tree on $n$ vertices, and put $d=n-2\nu$ and $S=n-\nu$. Let $r$ be the representative of $S\bmod m$ in $\{1,\ldots,m\}$. Whenever $d\le r$, the tree is $2m$-cordial. The case $d=1$ includes every residue of the tree order.

For example, at 26 labels every even-order tree with a matching missing two vertices is covered unless its order is a multiple of 26. More generally write the order of a smallest 26-label counterexample as $26q-H$ with $0\le H\le5$, using the [order restrictions](rainbow/short-forests.md). It would need $d\ge H+2$. Indeed $d$ and $H$ have the same parity, and $d\le H$ would give $r=13-(H-d)/2\ge d$. In particular a 47-vertex counterexample would need every matching to miss at least seven vertices.

## Every connected prefix

Suppose that, at modulus $m$, each tree of order $m$ admits a bijection with distinct edge sums even with any independently prescribed additive edge offsets. This holds at $m=2,3,5,7,11,13$ by the [signed-moment certificates](biased/README.md). Take an arbitrary tree with any vertex ordering in which every prefix is connected, and prescribe offsets on all edges. **A single labeling makes every prefix cordial.** Each consecutive block of $m$ vertices starting at positions $1,m+1,2m+1,\ldots$ receives distinct residues, including the final partial block.

Start with an arbitrary label at the first vertex. At every later block start the old vertex counts are uniform, and exactly one edge bin is deficient. Label the new vertex so its edge to the prefix fills this bin. Its label $h$ is the unique surplus vertex residue of the resulting prefix, and edge counts are uniform.

For the remaining $t\le m-1$ vertices of the block, subtract $h$ from old vertex labels as a coordinate change. Each free component meets the prefix in one edge. Replace the old boundary parents by one dummy vertex, and add the normalized old parent label to the offset on each corresponding edge. Pad this auxiliary tree to order $m$, use the hypothesis, and translate its labels so the dummy has label zero. Restrict to the actual free vertices, undo the coordinate change and attach. Their labels are distinct and avoid $h$. Their new weights, including all boundary edges, are distinct. These facts hold on every intervening prefix, as every vertex arrives after its parent. At the end of a full block the old and new vertex counts are uniform again. This proves the prefix assertion and applies also to a tree consisting of just one vertex.

In particular choose any collection of at most $r$ leaves of an $S$-vertex tree, where $1\le r\le m$ represents its order. Put them last in a connected vertex ordering, by starting in their connected complement. If the tree consists entirely of the specified leaves it has at most two vertices and either order works. All chosen leaves then have distinct labels of maximum frequency. The other full blocks each use every residue once.

## Completing and lifting a maximum matching

In a nonsingleton tree a maximum matching can leave only leaves exposed after exchanges. From an exposed internal vertex walk along a nonmatching edge, then along its other endpoint's matching edge. Another exposed endpoint would give an augmenting path, contradicting maximal size. Continue without turning back until the walk reaches a leaf at even distance. A tree prevents revisits. Toggling the alternating path moves the exposure to that leaf. Repeating for the remaining exposed internal vertices reduces their number each time and leaves the matching size unchanged.

Add a new leaf to each of the $d$ exposed leaves and match each new edge. The completed tree has $S=\nu+d$ matched pairs. Contract them to obtain a tree of order $S$. The $d$ new pairs are pendant quotient vertices. By the prefix result they can receive distinct maximum-frequency labels when $d\le r$. Apply the [perfect-matching lift](matching-expansion.md) to this particular labeling.

In the doubled tree each of the two parity classes of vertex labels reproduces the quotient vertex counts. Matching edges use odd weights and the class at weight $4x+m$ has exactly the vertex count of $x$ in the quotient. Nonmatching edges have even weights and reproduce the quotient edge counts. The counted residues are modulo $2m$. The map from quotient labels $x$ to their odd matching weights is a bijection because $m$ is odd.

Delete the $d$ added leaves and their matching edges. The deleted vertex labels are all distinct, since they belong to distinct quotient labels. The deleted odd weights are also distinct. When $r<m$, every deleted vertex and edge comes from a high bin, reducing its count from $\lfloor S/m\rfloor+1$ to $\lfloor S/m\rfloor$. All bins therefore remain balanced. When $r=m$, both vertex parities and the odd weights have the constant count $S/m$, and the even weights have counts $S/m$ or $S/m-1$. Deletion from distinct bins again preserves balance. The singleton is immediate. This proves the theorem.

## Verification

The [constructor](near_matching.py) takes the original tree, finds a maximum matching, moves exposures to leaves, labels the quotient, lifts and restricts. The [independent checker](check_near_matching.py) computes the maximum matching size by a separate tree recurrence, checks the exposed degrees, and counts every vertex and edge residue in the original tree. Tests include 2,175 small trees at the stated moduli, 457 additional eligible trees, and 483 near-perfect examples spanning every order residue that occurs for this odd-order family. It also checks every one of 15,097 connected prefixes with independently chosen edge offsets. The all-orders conclusion follows from the prefix and matching arguments.

~~~sh
python3 -B -m research.check_near_matching
~~~

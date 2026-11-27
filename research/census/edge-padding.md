# Cordiality from subdivisions on one chosen edge

**One-edge padding theorem.** Fix a modulus $k$ and any edge $e$ of an $n$-vertex tree. Subdividing just $e$ by **any** number $P\ge(k-1)(n-2)$ of vertices produces a $k$-cordial tree. More generally, for any path through $e$ on $d$ vertices, $P\ge(k-1)(n-d)$ suffices.

**Bound independent of tree order.** At $k\ge5$, **every tree containing a path with at least $2(k-3)(k-1)^2$ internal vertices of degree two is $k$-cordial**. The endpoints, degrees elsewhere, and total tree order are unrestricted. The earlier [bare-path repair theorem](../hub/bare-path-repair.md) instead gives a threshold uniform over moduli for trees in specified degree classes.

**One-period subdivisions on an arbitrary fixed core.** At every odd $k$, and at every $k\ge8$ divisible by four, one can subdivide any chosen edge of **any cordially labeled tree** by exactly $k$ vertices while keeping all old labels. At $k\equiv2\pmod4$, $k\ge6$, this holds for every cordial core of even order and for some odd orders as described below. Repeated applications may use different edges.

## One new leaf and one old edge

Let $k\ge5$ and allow **arbitrary old vertex labels**. Attach a leaf at any old vertex of label $p$ and insert $k-1$ vertices on any old edge. There is a labeling increasing every vertex and weight count by exactly one. The leaf parent may be an endpoint of the edge.

Write $S=\sum_{x\in\mathbb Z_k}x$. The leaf label is forced. If it is $l$, the inserted path labels must sum to $S-l$. On the path the net change in weight sum after deleting the old edge is twice the sum of the inserted labels. Thus $S=2(S-l)+p+l$, or $l=p+S$. Use the [short edge subdivision](cycle-subdivision.md#a-short-cycle-inserted-at-an-endpoint) with forbidden vertex label $l$. Its $k-1$ path labels cover all other residues. After canceling the replaced edge its $k-1$ net weights are also distinct. If $D$ is the missing weight, then $S-D=2(S-l)$, giving $D=2l-S=p+l$. The new leaf supplies it. This uses only the specified endpoint and parent labels. No cordiality assumption on their original tree enters the calculation.

Now begin with the path through $e$, already subdividing $e$ by the excess $P-(k-1)(n-d)$. Label this ordinary path cordially. Add the remaining $n-d$ original vertices in parent-before-child order. At each step use the new leaf and put its $k-1$ subdivisions on any edge of the path representing $e$. This constructs exactly the specified tree. Choosing the original endpoints alone gives the bound in terms of $n$. At $k\le4$ ordinary cordiality of every tree is already known. The same argument works with any initially cordial subtree whose chosen edge tolerates the excess subdivision, including an edge on the spine of a caterpillar. [Hovey's caterpillar theorem](https://doi.org/10.1016/0012-365X(91)90254-Y)

## A bound uniform over trees at fixed modulus

Suppose otherwise and choose a smallest counterexample **among trees containing the stated bare path**. Paths are cordial. In the tree obtained by suppressing all degree-two vertices, the distinguished path lies in one edge. Mark the whole corresponding segment in the original tree. At most one of its two endpoints is an original leaf, since the tree itself is not a path.

Put $t=(n-1)\bmod k$. At $t=0$ remove any original leaf outside the marked segment. The segment still exists, and the smaller tree has divisible order. Its deficient edge weight determines a label for the leaf. At $t>0$, if there are $t$ outside leaves, remove them. The marked path retains all its internal degree-two vertices and the smaller core has order one modulo $k$. [Hall's leaf extension](../counterexample-bound.md#removing-leaves) restores all the leaves. Hence there are at most $t-1$ outside leaves, at most $t\le k-1$ leaves in total, and $t\ge2$.

Every unmarked segment between vertices of degree different from two has at most $t-1$ internal vertices. Otherwise suppress $t$ of them. The smaller tree still has the marked path, and the [short subdivision theorem](cycle-subdivision.md) restores the edge from an order-one-residue core. The suppressed skeleton has at most $2L-3$ edges at $L$ leaves, since it has at most $L-2$ branching vertices. Apart from the marked segment there are therefore at most $2k-6$ segments of length at most $k-1$. Contract the marked segment to a single edge. The resulting tree has at most $2+(2k-6)(k-1)$ vertices. The first theorem now restores the marked segment, proving the claimed bound. Minimality here only compares trees that still contain the required path.

## A whole period on any fixed core

Odd $k$ allows the natural full cycle starting just after one endpoint label and ending at a copy of it. This gives uniform increments and retains the old edge weight. For even $k\ge6$, write $m=k/2$. A high bin in a balanced histogram means one occurring once more than its floor count. A uniform histogram has no high bins.

If a low edge bin $D$ has high antipode $D+m$, follow the full cycle that repeats $D$ and omits $D+m$. This fills the low bin, moves the high bin and gives uniform vertex increments. Such a pair always exists when the set of high bins has odd size, in particular when the old tree order is even. [Construction of both parities of repeated weight](cycle-subdivision.md#an-even-hamilton-cycle-with-prescribed-repeated-weight)

Now suppose $4\mid k$ and the high edge bins are invariant under the antipodal map. Their count is even. The old order is odd, so the number of high vertex bins is odd. Translation by $k/4$ partitions the residues into orbits of length four. Thus some high vertex label $y$ has low translate $z=y+k/4$. Use the $k-1$-vertex subdivision with hole $y$. Its missing weight is $2y-S=2z$ by the sum calculation above. The path contains $z$. Duplicating it next to itself supplies that weight, so the edge increments are uniform. The vertex increments are one per bin except for a transfer from $y$ to $z$, which preserves cordiality. This proves the fixed-core theorem. At two modulo four an order-one-residue core has the proved parity obstruction to a one-period subdivision.

The [constructor](edge_padding.py) gives the labels along the chosen edge and on each original vertex. The [checker](check_edge_padding.py) counts the actual old and new edge weights in 10,850 uniform leaf-and-edge packets, tests 11,228 fixed-core period insertions including antipodally invariant high sets, and verifies 1,224 padded trees through modulus 4,096.

~~~bash
python3 -B -m research.census.check_edge_padding
~~~

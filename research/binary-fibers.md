# Exact binary lifts and a family at every twice-odd modulus

Write a residue modulo $2m$ as $a+mh$, with $0\le a<m$ and $h\in\mathbb F_2$. We allow a prescribed integer offset $b_e$ in the sum on edge $e$. Zero offsets give the original cordiality problem.

**Order $2m$.** Fix the low vertex labels of a tree. A bijective lift requires two occurrences of each low label. All low weight classes must contain two edges except for one singleton. When these conditions hold, feasibility and the exact number of lifts follow from one linear system over $\mathbb F_2$.

In each vertex fiber give one vertex tag $t_v=0$ and the other tag one. The high bits are $t_v+X_a$ at vertices of low label $a$. On an edge $e=uv$ the high bit is the sum in $\mathbb F_2$ of
$$
 X_{a_u}+X_{a_v}+t_u+t_v+\left\lfloor(a_u+a_v+b_e)/m\right\rfloor.
$$
For each two-edge weight class require the two high bits to differ. These are exactly the $m-1$ necessary and sufficient equations. If they are consistent with rank $r$, there are $2^{m-r}$ lifts. The equation masks depend only on the two endpoint low labels of each edge in the pair. In particular redistributing incidences between the two vertices in a low fiber changes only the right-hand sides. Adding $m$ to an edge offset also changes only a right-hand side. A full row rank certificate therefore covers all these choices at once.

In the ordered-cut test one may join every exterior component to a common dummy vertex and use its prescribed boundary color as an offset on that edge. A bijective rainbow labeling of this $2m$-vertex tree translates to make the dummy label zero. Its other labels and its edge sums then give the required witness. The same system consequently tests lifts for boundary colors with prescribed low digits. [Ordered-cut theorem](rainbow/ordered-cut.md) · [Earlier examples of fixed labelings with no lift](cyclic-lifts.md)

## A family with full rank

Let $m\ge3$ be odd. Start with the low vertices $a\in\mathbb Z_m$. For each $a$ put in the two undirected edges $(a-r,a+r)$ and $(a-s,a+s)$, where $0\le r<s$. Delete the second edge at any one midpoint. Split each low vertex into two vertices and assign each incident edge end to either one. Whenever the result is a tree, it is $2m$-cordial for **every** split if $\gcd(m,s-r)=\gcd(m,s+r)=1$. Even arbitrary independent offsets of zero or $m$ on its edges are allowed. In particular **$r=1,s=3$ works at every odd $m$**.

Indeed the low weight is $2a$, which indexes the classes bijectively. Before deleting one equation, the row at $a$ is the sum of the four coordinate vectors at $a-r,a+r,a-s,a+s$. The sum of all rows is zero, so deleting any row leaves their span unchanged. Identify vectors with polynomials modulo $z^m-1$ over $\mathbb F_2$. The cyclic row shifts span the image of multiplication by
$$
 z^{-s}(1+z^{s-r})(1+z^{s+r}).
$$
For multiplication by $P$ the kernel has dimension $\deg\gcd(P,z^m-1)$, by dividing $P$ and $z^m-1$ by their common factor. Since $m$ is odd, $z^m-1$ has no repeated root. The gcd with $z^h-1$ is $z^{\gcd(h,m)}-1$. Counting roots in the union of the two factors gives the exact row rank
$$
 m-\gcd(m,s-r)-\gcd(m,s+r)+\gcd(m,s-r,s+r).
$$
Under the displayed coprimality hypotheses the rank is $m-1$. Every right-hand side has two solutions, differing by a global high-bit flip. At $m=11$ Lean directly checks the full permutation of ten-bit syndromes after one vertex bit is fixed. [Lean proof](BinaryFibers22.lean)

These blocks also give trees of unbounded order. At modulus $k$, attach a cordial block of order divisible by $k$ to any already cordial tree by a single edge at arbitrary vertices. In its own labeling the block has uniform vertices and a unique deficient weight $w$. If the old and new port labels are $c,f$ and the joining edge has offset $b$, translate the block by $c+f+b-w$. The joining edge then supplies exactly the translated deficit. This adds a uniform histogram to both vertices and edges and can be iterated along a tree of blocks.

## Counting lifts at arbitrary order

For an arbitrary fixed low assignment, let $s$ run through the counts in a vertex or edge histogram modulo $m$. A successful lift splits each count into $\lfloor s/2\rfloor,\lceil s/2\rceil$. First require the resulting possible counts to have combined range at most one separately for the vertex and edge histograms. This check is automatic for a cordial low assignment.

Within each vertex fiber and each edge fiber, choose disjoint pairs covering all but at most one occurrence. Set one high-bit variable at every vertex. Require opposite high bits on every paired pair of vertices, and opposite high weight bits on every paired pair of edges, using the known carries. Write $r(P)$ for the rank of these equations for the choice of pairs $P$. Then the number of full cordial lifts is
$$
 \frac{\sum_{P\ {\rm consistent}}2^{|V|-r(P)}}
 {\prod_{\text{vertex and edge fibers of size }s} \lceil s/2\rceil!}.
$$
Each solution for $P$ is balanced within every fiber. Conversely a balanced lift admits $j!$ compatible pairings in a fiber of size $2j$, and $(j+1)!$ in a fiber of size $2j+1$. In the odd case match the smaller side injectively to the larger. The denominator therefore counts the multiplicity of every lift exactly.

The checker compares elimination with exhaustive high-bit enumeration in 2,400 order-equals-modulus systems and checks the pairing count independently on 280 arbitrary-order inputs. It also verifies 1,098 circulant ranks and reconstructs 317 connected split trees with half-turn edge offsets. [Implementation](binary_fibers.py) · [Independent checks](check_binary_fibers.py)

~~~sh
python3 -B -m research.check_binary_fibers
lean research/BinaryFibers22.lean
~~~

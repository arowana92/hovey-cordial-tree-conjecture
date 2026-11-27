# Connecting stars at prescribed leaves, with one labeling for every modulus

Let $Q$ be an odd-order tree with a bijection onto $\mathbb Z_q$ and distinct edge sums, where $q=|Q|\ge3$. Replace each vertex of $Q$ by a star with $a$ leaves. For each quotient edge, join **any specified leaf** in one star to **any specified leaf** in the other. Several joining edges can use the same leaf. The result is a tree on $q(a+1)$ vertices.

**Theorem.** The resulting tree is super edge-magic, and hence cordial at every positive modulus, if
$$
a\ \ge\ g+\left\lceil D/2\right\rceil .
$$
Here $g$ is the maximum number of different attachment leaves used in one star. To define $D$, retain only the joining edges and their endpoints, and take the largest diameter of a resulting component. In particular $a\ge\Delta(Q)+\lceil\operatorname{diam}(Q)/2\rceil$ works for **every choice of leaves**. The [integer census](README.md) supplies the quotient hypothesis for every odd-order tree through 25 vertices. The theorem has no order bound on quotients admitting the stated bijection.

Two specializations give simpler families.

- If every incidence uses a different leaf in its star, $a\ge\Delta(Q)+1$ suffices. Equivalently, subdivide every edge of $Q$ twice, then attach enough leaves to each original vertex to bring its degree to $a$.
- If $Q$ is any odd path, **three leaves per star suffice**, including arbitrary reuse of leaves. This holds for every $a\ge3$ independently of the path length.

## The interval of joining weights

Write $q=2t+1$. Translate the quotient labeling to $x$ so its missing edge residue is $t$. This is possible since adding a constant to all labels translates all weights by twice that constant. In the star at $v$, give its center label $qa+((x_v+t)\bmod q)$ and its leaves labels
$$
qj+x_v,\qquad 0\le j<a.
$$
The latter indices will be assigned to the actual leaves below. These labels fill $[0,q(a+1)-1]$. For fixed $j$, as $x$ runs from zero to $2t$, the small part $x+((x+t)\bmod q)$ runs through $[t,3t]$ exactly once. The part $x\le t$ gives $t,t+2,\ldots,3t$, and $x>t$ gives $t+1,t+3,\ldots,3t-1$. Thus the original spoke sums fill the integer interval starting at $qa+t$, of length $qa$.

For a joining edge $uv$, take the representative $z_{uv}\in[-t,t-1]$ of $x_u+x_v$ modulo $q$. The joining weights we seek are the $q-1$ consecutive integers $qa+z_{uv}$ just below the spoke interval. Define
$$
c_{uv}=\left\lfloor(x_u+x_v+t)/q\right\rfloor,\qquad \epsilon_{uv}=1-c_{uv}\in\{-1,0,1\}.
$$
The quotient input ensures $x_u+x_v-qc_{uv}=z_{uv}$. If the two actual leaves receive indices $j,j'$, their required equation is exactly $j+j'=a-1+\epsilon_{uv}$.

The use of odd copies and consecutive digit sums is related to constructions for super edge-magic disjoint unions. Here the joining edges must fill a further interval, with prescribed identifications of their endpoints. [Figueroa-Centeno, Ichishima and Muntaner-Batle on odd disjoint unions](https://www.researchgate.net/publication/268891852_On_edge-magic_labelings_of_certain_disjoint_unions_of_graphs) · [An odd product for unions of nonisomorphic graphs](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/C101DA32955C38EF1F4F6102BABED198/S0004972711002292a.pdf/enumerating-super-edge-magic-labelings-for-the-union-of-nonisomorphic-graphs.pdf)

## Assigning indices to the prescribed leaves

Call each used leaf a port. In a connected component $C$ of the joining edges alone, no two ports project to the same quotient vertex. Otherwise their path would project to a nonempty closed trail in a tree, since every quotient edge has just one joining edge. Thus the components project to connected edge-disjoint subtrees of $Q$.

Fix the two sides $U,V$ of $Q$. On each component choose integer potentials $d$ with $d_u-d_v=\epsilon_{uv}$ for each edge from $U$ to $V$. A unique choice exists up to a componentwise constant. For some integer $s_C$, give each port the index $s_C+d$ on side $U$ and $a-1-(s_C+d)$ on side $V$. These satisfy every joining equation. If $w_C=\max d-\min d$, exactly $a-w_C$ choices of $s_C$ keep all indices in $[0,a-1]$ when $a>w_C$.

On a two-edge path the difference between endpoint potentials is the difference of two carries, up to sign. The adjacent numerators in the carry formula share a label and differ by less than $q$, so their floors differ by at most one. On one edge the difference is also at most one. Pairing steps on the path between the minimum and maximum gives $w_C\le\lceil\operatorname{diam}(C)/2\rceil$.

Start with any component and grow a connected union of its projected subtrees. Each new component intersecting the union meets it at exactly one vertex, since a second meeting would create a cycle. At that star at most $g-1$ previous indices are forbidden. Each excludes at most one choice of $s_C$, so $a-w_C\ge g$ suffices. Assign unused indices to the remaining leaves in any order. This proves the theorem, including the potentially stronger input-specific bound $a\ge g+\max_C w_C$.

## Three-leaf stars on paths with any odd number of vertices

Number the $q$ path vertices $i=0,\ldots,q-1$. The initial labels $i$ miss edge weight $-1$. The normalized labels are $x_i=(i+c)\bmod q$ with $2c=t+1\pmod q$. Consider potentials on the unsplit path before choosing ports. Set $d_0=0$, using even positions for $U$. Across edge $i,i+1$ the increment is $-\epsilon_i$ for even $i$ and $+\epsilon_i$ for odd $i$.

Substitution in the floor formula gives these sequences, where powers denote repetitions, including zero repetitions.

| Order | $c$ | Successive $\epsilon_i$ |
| :--- | :--- | :--- |
| $q=4u+1$, $u\ge1$ | $3u+1$ | $(-1)^{u-1},0,(+1)^u,0^{2u}$ |
| $q=4u+3$, $u\ge0$ | $u+1$ | $0^{2u+1},(-1)^u,0,(+1)^u$ |

For example the exceptional single zero between the two constant nonzero runs is the edge on which the normalized vertex labels wrap from $q-1$ to zero. Within each run the increments alternate. The intervening single zero reverses the position parity at the same time that the sign of the run reverses, so both runs use the same two potential values. In the first row these are $0,1$ and in the second row they are $-1,0$. Splitting vertices into different ports restricts these potentials to shorter paths. Thus every $w_C\le1$ and $g\le2$, proving the three-leaf assertion.

## Pieces with more than one center-side vertex

There is also an extension to nonisomorphic pieces. In each position take a tree of the same order $n$ with a bijection to $[0,n-1]$. Suppose every edge crosses from $[0,a-1]$ to $[a,n-1]$ and the sums are distinct. They necessarily fill $[a,a+n-2]$. This hypothesis is the sum form of an $\alpha$-labeling. Prescribe at each piece which incidences must use the same port and which must use different ports. Under the theorem's bound one can choose the ports from the first part to make the joined tree super edge-magic.

Indeed, at a vertex with local label $j$ use full label $qj+x_v$ in the first part and $qj+((x_v+t)\bmod q)$ in the second. Each internal sum block still uses $[t,3t]$ as its small part, since each piece realizes each macro sum once. The same assignment of port indices fills the joining interval. In a star the interchangeable leaves realize any prescribed actual endpoints. For general pieces the construction selects the vertices with the calculated labels.

## Independent checks

The constructor takes the actual quotient parents and leaf indices. The checker rebuilds the stars and joins from those inputs, checks every integer label and sum, and separately counts residues. It checks 690 instances across all rooted tree shapes of orders 3, 5, 7 and 9, all 43,690 incidence partitions along odd paths through 17 stars with three leaves per star, and long paths through 255 stars. Lean proves the digit interval, its uniqueness, and the shared-endpoint carry bound for arbitrary parameters. [Constructor](star_joins.py) · [Whole-tree checks](check_star_joins.py) · [Lean arithmetic](StarDigits.lean)

~~~sh
python3 -B -m research.census.check_star_joins
lean research/census/StarDigits.lean
~~~

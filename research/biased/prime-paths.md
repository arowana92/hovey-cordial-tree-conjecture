# Every path allows independently prescribed edge offsets at every prime

**Theorem.** Let $p$ be prime. Give each edge $uv$ of any finite path its own residue $b_{uv}$. There are vertex labels in $\mathbb F_p$ such that the vertex labels and the weights $f(u)+f(v)+b_{uv}$ are both balanced, including zero-frequency bins. At every odd prime, a cycle of length any positive multiple of $p$ admits uniform histograms with prescribed offsets **if and only if their sum is zero**.

More generally, replace every edge of any tree by a path of length at least $p-1$. Give independent offsets to **all** resulting edges. The tree is $p$-cordial with those offsets, for arbitrary original degree and arbitrary order. The lengths need not have the same remainder modulo $p$.

## A permutation theorem for prime circulants

Let $p$ be odd, index both variables and outputs by $\mathbb F_p$, and let
$$
y_i=b_i+\sum_{j\in\mathbb F_p}a_j x_{i+j}.
$$
Suppose $A=\sum_j a_j\ne0$. For every $b$ with $\sum_i b_i=0$, there is a permutation $x$ of the field with $x_0=0$ for which $y$ is also a permutation. In fact the signed count is
$$
\sum_{x:\ x_0=0,\ x,y\ \mathrm{permutations}}
   \operatorname{sgn}(x)\operatorname{sgn}(y)
   \equiv -\operatorname{sgn}(t\mapsto At)\pmod p .
$$
Both signs treat a list as a map from its fixed index set to the field. The zero total on $b$ is necessary by summing the output. The result includes adjacent sums, longer cyclic sums with arbitrary coefficients, and the prime cyclic permutation-with-prescribed-differences problem when only one coefficient is nonzero. Hall's theorem treats the latter problem in every finite abelian group. [Hall (1952)](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

**Independence of the offsets.** Work over the field and delete position zero in both lists. Write $D=\mathbb F_p^\times$, $r=p-1$, $Q(X)=\prod_{t\in D}(X-t)$ and $V(z)=\prod_{i<j}(z_j-z_i)$ on the remaining $r$ coordinates. Apply the grid sum
$$
\sum_{x_1,\ldots,x_r\in D}
   \frac{V(x_1,\ldots,x_r)V(y_1,\ldots,y_r)}{\prod_{i=1}^r Q'(x_i)} .
$$
The summand vanishes unless the retained input and output entries are separately distinct. Then $x$ is a permutation. All $p$ outputs sum to zero, so $y_0$ equals the unique missing residue and $y$ is also a permutation. Prepending zero and $y_0$ to the two Vandermondes multiplies each by the product of the nonzero residues. Their ratio is thus $\operatorname{sgn}(x)\operatorname{sgn}(y)$. The remaining factor $V(x_1,\ldots,x_r)^2/\prod Q'(x_i)$ is fixed and nonzero on permutations. The grid sum gives a fixed nonzero multiple of the signed count.

Univariate interpolation yields $\sum_{t\in D}t^j/Q'(t)=0$ for $j<r-1$. Every numerator term involving a positive power of any $b_i$ has degree in $x$ less than $r(r-1)$, hence some $x_i$ has exponent below $r-1$. It contributes zero. This proves independence, including when a coefficient $a_j$ is zero or many coincide. [Related grid-sum calculation for tree offsets](README.md#signed-counts-and-first-moments)

**Evaluation at zero offsets.** Act on normalized permutations by $x'_i=x_{i+1}-x_1$. This gives a group action of order $p$. At zero offsets $y'_i=y_{i+1}-Ax_1$. Thus the valid permutations are a union of orbits and the signed summand is constant on each. The index shift is common to both lists. Each nonzero translation of the field is a $p$-cycle and has positive sign. Nonfixed orbits contribute zero modulo $p$.

A fixed permutation satisfies $x_{i+1}=x_i+d$, hence $x_i=di$ for one of the $p-1$ nonzero $d$. Its outputs are $A x_i+d\sum_j j a_j$. They form a permutation and the sign product is that of multiplication by $A$. The $p-1$ fixed contributions give the displayed congruence. In particular the signed count is nonzero for every permissible offset vector.

## Paths, cycles and prescribed terminals

Use coefficients one at positions zero and minus one, so $y_i=x_{i-1}+x_i+b_i$. At odd $p$ their sum is two. An arbitrary set of $p-1$ path offsets can be completed by one closing offset to have sum zero. The theorem gives a permutation on the path vertices with $p-1$ distinct weights, and also proves the cycle assertion at length $p$. At $p=2$ a two-vertex path labeled $0,1$ works for either offset.

Let $S=\sum_{i\in\mathbb F_p}i$, which is zero for odd $p$ and one at $p=2$. Given any parent of actual label $c$, a path adding $p$ vertices with edge offsets $b_1,\ldots,b_p$ can be labeled with **each vertex label and each edge weight occurring once**. Apply the path result on the $p$ free vertices using the last $p-1$ offsets. If the first vertex has label $z$ and the missing internal weight is $w$, translate the free labels by $c+z+b_1-w$. The edge back to the parent then fills the translated deficit. Summing all $p$ new weights shows that the final vertex necessarily has label
$$
c+\sum_{i=1}^p b_i-S.
$$
This terminal identity permits subdivisions of any chosen edge by $p$ new vertices. With offsets $b_1,\ldots,b_{p+1}$ along the resulting path, use effective offset $\sum b_i-S$ on the compressed edge. The replacement adds one full period to both histograms. It applies at prescribed endpoints and can be iterated. For odd $p$, contraction preserves the total offset, which gives the cycle theorem at every multiple of $p$ by reducing to length $p$. Necessity there follows by summing all weights when both histograms are uniform.

For an arbitrary path, take its first block of between one and $p$ vertices such that the number left is a multiple of $p$. Pad that first block to $p$, then restrict, retaining distinct vertex and edge labels. Attach the remaining full blocks using the parent construction. More generally a tree assembled from disjoint $p$-vertex paths and one path of order at most $p$ by bridges at arbitrary ports works with independent offsets: label the short piece first and add the full pieces outwards. A full piece can be translated at any incoming port by the same missing-weight argument.

## Two paths on a prescribed core

Suppose a core has order one modulo $p$, uniform edge counts and one surplus vertex color $u$. Attach at most two paths, each at an endpoint, with at most $p-1$ free vertices altogether. Their parents may have any labels and every edge may have its own offset. Join the arms at a single dummy vertex. The result is a path. On each dummy edge add the actual parent's label minus $u$ to that edge's offset. Pad the path to $p$ vertices, give it a bijective rainbow labeling, and translate it to put the dummy at $u$. The two actual arms have distinct free labels avoiding $u$ and distinct weights, since their boundary weights agree with the dummy edges. This proves the extension.

On a cordial core of order zero modulo $p$, at most two such paths with up to $p$ free vertices can be attached. Choose the first vertex on one arm to supply the core's deficient weight. The new core has the preceding surplus and uniform-edge form, and the remaining parts are still at most two arms. After a full $p$-vertex attachment the core order is divisible by $p$ again.

For the tree subdivision theorem, root the coarse tree and list its edge paths in parent-before-child order, reading each away from the root. Start with the first $p$ vertices, possible along its first path. They admit a full path labeling. Take the remaining free vertices in successive batches of $p$ with a possibly shorter last batch. Each batch uses at most two coarse edges: even if its first edge supplies only one vertex, the next has length at least $p-1$. If the second arm starts at a newly reached endpoint, the two pieces form one path. Otherwise both arms attach to already labeled vertices. The divisible-core extension completes every batch. The one-vertex tree is immediate.

## Verification

The direct checker sums signs over every normalized permutation in 2,085 tests. These include every circulant with nonzero coefficient sum and every zero-sum offset vector at three, all zero-sum vectors for three circulants at five, and further stencils at seven. A separate path constructor searches with vertex and edge bit sets. Tests recalculate the actual histograms on 54 paths, 96 prime cycles, 108 edge replacements and 96 subdivided trees. The largest tested prime is 23. The orbit and interpolation proof applies to all odd primes. [Constructor](prime_paths.py) · [Direct signed counts and independent histogram checks](check_prime_paths.py)

~~~sh
python3 -B -m research.biased.check_prime_paths
~~~

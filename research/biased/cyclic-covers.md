# Lifting trees obtained by opening a prime-sheeted cyclic cover

Let $B$ be a connected unicyclic multigraph with $m$ vertices and $m$ edges, whose unique cycle has length $\ell$. A loop counts as length one, a pair of parallel edges as length two. Suppose the base vertices are labeled bijectively modulo $m$ and the base edge weights are also a permutation. A fixed integer offset $c_e$ on each base edge is allowed.

Replace every vertex by $p$ copies and every base edge by a perfect matching of its two endpoint fibers, taking $p$ an odd prime. For a loop this means a permutation between the two copies of its incidence fiber. Suppose the cover is connected. Remove any one edge from its cycle, giving a tree. Give each surviving copy of $e$ an independent offset $c_e+m b_{e,i}$ modulo $mp$.

**Theorem.** Set $h=(p-1)/2$ and
$$
F_{p,\ell}=\sum_{j=0}^{h}\binom hj^{\ell}\pmod p.
$$
If $F_{p,\ell}\ne0$, a bijective rainbow labeling of the tree modulo $mp$, preserving all prescribed low vertex labels modulo $m$, exists **exactly when** $\sum_i b_{e,i}=0\pmod p$ on every intact edge fiber. There is no condition on the fiber with the deleted edge. The result does not require coprimality of $m$ and $p$. It works for every base cycle length congruent to $0,1$ or $2$ modulo $p-1$.

The necessity follows directly: in each vertex fiber the high digits must permute the field. All weights on an intact edge fiber have their own distinct low class, so their high digits must permute the field as well. Summing along its perfect matching eliminates both endpoint sums and the repeated base carry. This leaves the stated condition. To prove sufficiency, restore the absent edge with the unique high offset that gives sum zero on that fiber too.

Number the sheets along a spanning tree of $B$ so its matchings preserve the sheet index. The remaining edge has one matching permutation. Connectedness means that this permutation is a single $p$-cycle, since its orbits are exactly the components after contracting the $p$ lifted spanning trees. Thus a common renumbering puts every directed matching into the form $(u,i)(v,i+t_e)$. This also shows that removing an actual lifted cycle edge leaves a connected tree. The high digits of its sums are the sums of the high endpoint digits, $b_{e,i}$ and a fixed carry. The carry has total zero over an edge fiber.

## Several cyclic arrays over the prime field

The following coefficient formula explains the criterion and applies beyond graph incidence matrices. Take $s$ input rows and $s$ output rows, each of length $p$. For field coefficients $a_{trj}$ and rowwise zero-sum offsets $b$, put
$$
y_{t,i}=b_{t,i}+\sum_{r,j}a_{trj} x_{r,i+j},\qquad S_{tr}=\sum_j a_{trj}.
$$
Normalize $x_{r,0}=0$ for every input row. Among the choices making every input and output row a permutation, sum the product of the signs of all $2s$ permutations. Its residue modulo $p$ is
$$
(-1)^s[z_1^h\cdots z_s^h]\prod_{t=1}^s\left(\sum_r S_{tr}z_r\right)^h.
$$
In particular a nonzero coefficient proves existence for **every** allowed offset array. This extends the [single-row circulant theorem](prime-paths.md#a-permutation-theorem-for-prime-circulants).

For the proof, take the product of the input and output Vandermondes with position zero deleted in each. Apply the grid sum on the $s(p-1)$ nonzero input positions as in the single-row proof. If all the retained entries are distinct within each row, the missing input in each row is zero and the missing output is its position zero: the output sum is zero by the cyclic form and the row sums of $b$. The denominator and the squared input Vandermondes give one nonzero constant factor. Any term involving $b$ has total input degree below $s(p-1)(p-2)$ and vanishes on integration over the grid. Thus we may evaluate at zero.

Shift the sheet index in every row and subtract its new initial entry in each input row. This shifts the output rows and translates each of them by a constant. The signed contribution is invariant, so only fixed points of this order-$p$ action contribute modulo $p$. These have $x_{r,i}=d_r i$ with every $d_r$ nonzero. The slope of output row $t$ is $(Sd)_t$. The sign of multiplication by $u\ne0$ in $\mathbb F_p$ equals $u^h$ as a field element. Indeed scaling the full $p$-coordinate Vandermonde multiplies it by $u^{p(p-1)/2}=u^h$. Extend this expression by zero at $u=0$ to automatically discard invalid rows. The fixed contribution summed over $d$ is therefore the sum over $\mathbb F_p^s$ of $\prod_r d_r^h\prod_t (Sd)_t^h$.

Every monomial has total degree $s(p-1)$ and positive exponent in every variable. Summing over the field kills it unless every exponent is divisible by $p-1$, so all exponents must equal $p-1$. Each surviving power sum is $-1$. Removing the initial $d_r^h$ factors gives the stated coefficient.

## Computing the coefficient on the base graph

The graph polynomial is $\prod_{uv\in E(B)}(z_u+z_v)^h$. A leaf variable occurs only in its one edge factor. Extracting its $h$th power removes it and that factor with coefficient one. On the remaining cycle, orient it consistently. In a term contributing $h$ at every vertex the exponent chosen at the tail must be the same $j$ on every edge. Each edge contributes $\binom hj$. This includes parallel edges. For a loop the result is $2^h$, which is the same formula at $\ell=1$. This gives the claimed signed count $(-1)^m F_{p,\ell}$. It ensures the restored cover has permutations in all fibers. Deleting the selected edge then gives the required tree.

Each binomial coefficient is a unit modulo $p$. For $\ell\equiv0$ the sum is $h+1$. For $\ell\equiv1$ it is $2^h$. For $\ell\equiv2$ it is $\binom{2h}{h}=\binom{p-1}{h}\equiv(-1)^h$ by the binomial convolution. All three are nonzero. In other classes the formula is still directly decidable. A zero coefficient only makes the signed test inconclusive.

For an ordinary example at every odd $m\ge3$, the cycle on base vertices $i$ in cyclic order has distinct low weights $2i+1$. Its connected cover opened at one edge is a path. For a branched example, take any bijectively rainbow tree at order $m$ with unused ordinary sum $w$. Choose a vertex of label $a$ and add an edge to the vertex of label $w-a$, allowing a loop. This completes both base permutations. Whenever its cycle length passes the test, the theorem applies to all connected covers with the indicated high offsets. In the ordinary case the fixed-point slopes can also simply all be one. The coefficient proves robustness under independent edge changes and gives exact impossibility for the specified low labels when an intact offset sum fails.

The checker separately enumerates actual row permutations in 147 block-circulant instances, compares 90 character sums against the formula and constructs 73 actual lifted trees. Its last check follows the lifted incidences, tests connectedness and recomputes all vertex labels and edge sums modulo $mp$. [High-digit search](cyclic_covers.py) · [Independent computations](check_cyclic_covers.py)

~~~sh
python3 -B -m research.biased.check_cyclic_covers
~~~

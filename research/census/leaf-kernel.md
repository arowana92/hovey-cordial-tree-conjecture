# Exact counts for a growing leaf population at a prescribed joint

Fix a rooted tree $R$ with $s\ge1$ edges and mark any vertex $v$. At modulus $n\ge s$, add $n-s$ leaves at $v$, giving $n$ free vertices besides the root. In a **uniform extension** the free labels and all new weights both permute $\mathbb Z_n$. At a prescribed cordial core of order divisible by $n$, a second possibility is to repeat its deficient weight $d$ while omitting one weight. Translate the root to zero and adjust $d$ by the same translation on edge sums.

**Theorem.** For every fixed $(R,v)$ the number of normalized uniform labelings, divided by $(n-s)!$, is an effectively computable quasipolynomial in $n$. There is also an exact finite arithmetic test for the existence of an extension for each $(n,d)$. The set of moduli admitting an extension for **every** $d$ is effectively ultimately periodic.

## Removing all the additional leaf variables

Write $x$ for the labels of the $s$ original free vertices, $x_r=0$, $S$ for the set of free labels in this kernel, and $a=x_v$. Require the $s$ entries of $x$ to be distinct. The new leaves receive the complement of $S$, in any of $(n-s)!$ orders. After subtracting $a$ from every weight, the added leaf weights occupy precisely this complement.

For a uniform extension, choose a bijection $\pi$ from the original edges to the original free vertices. On each edge $ij$ impose $x_i+x_j-a=x_{\pi(ij)}$. For a solution with distinct entries the bijection is unique. The count $N(n)$ sums over all $s!$ bijections.

For the second test, distinguish an original edge $h$ and replace its equation by $x_i+x_j=d$. Keep the other $s-1$ equations. Count these **marked** solutions as $M(n,d)$. Removing the distinguished edge leaves $n-1$ distinct weights. Conversely, if the repeated weight is $d$, at least one of its occurrences is an original edge because the added leaf weights are distinct. Deleting such an occurrence leaves a unique omitted element of $S$ in the shifted kernel, determining $\pi(h)$. Thus a full block can extend the given deficit exactly when $N(n)+M(n,d)>0$. The marked count can count the same labeling more than once.

For each system, impose injectivity by summing over partitions $P$ of the free vertices. Merge coordinates within each block and multiply by $\prod_{B\in P}(-1)^{|B|-1}(|B|-1)!$. This is Möbius inversion on the partition lattice. The resulting integer system has the form $Az=b d$, with $b=0$ in the uniform count. Diagonalize $A$ by invertible integer row and column operations and transform $b$ by the row operations. Write $a_i$ for the nonzero diagonal entries in absolute value and $c_i$ for the transformed right-hand coefficients. The contribution before its Möbius factor is zero unless

* $\gcd(n,a_i)\mid c_i d$ for every nonzero diagonal entry, and
* $n\mid c_i d$ in each zero row.

Otherwise it is $n^{u}\prod_i\gcd(n,a_i)$, where $u$ is the number of columns minus the rank. This follows by solving each scalar congruence. No divisibility order on the diagonal entries is needed. The finite sum proves the quasipolynomial assertion for $N$. The role of integer elementary divisors in modular arrangement counts is classical. [Kamiya, Takemura and Terao](https://arxiv.org/abs/math/0703904) · [Integer diagonalization and counts](leaf_kernel.py)

## Deciding all deficits at once

Let $L$ be the lcm of the nonzero diagonal entries across the finite calculation. In each summand combine the zero-row coefficients into their nonnegative gcd $b$ (zero for no restriction). The additive order $h$ of $d$ must divide $b$ when $b>0$. Let $H$ be the finite set of positive divisors of all such $b$.

Multiplication by a unit identifies deficits of equal order. For $h\in H$ with $h\mid n$, take $d=n/h$. Whether the summand contributes and its gcd factors then depend only on $h$ and $\gcd(n/h,L)$. For $h\notin H$ discard terms with $b>0$. The remaining factors depend only on $g=\gcd(n,L)$ and $f=\gcd(d,g)$. This yields finitely many ordinary polynomials in $n$. The sum of the neutral and marked counts is nonnegative on each realizable type.

Once $n>L\max(H\cup\{1\})$, every $f\mid g$ occurs in the latter group: take $d=f\bmod n$, whose order is $n/f$. The available small orders and all their gcd types depend only on $n$ modulo $L\operatorname{lcm}(H)$ (empty lcm one). Each polynomial is identically zero or eventually has a fixed sign, with computable cutoff. This proves effective ultimate periodicity. The verifier can certify positivity earlier by shifting the polynomial origin to an integer threshold and checking that all coefficients are nonnegative and the constant term is positive. Smaller moduli are checked individually.

## Three edges on one side of the joint

Let the root have two neighbors. One has $n-4$ leaf children. The other starts a path of length three from the root. This gives $n$ free vertices for $n\ge4$.

**Exact obstruction.** A uniform extension at this root exists exactly when $4\mid n$ or $5\mid n$. Nevertheless, at every modulus a prescribed cordial core of divisible order extends across every tree in this family.

Write $x$ for the leaf parent's label and $y,z,t$ along the other path. After subtracting $x$, the four kernel weights are
$$
0,\quad y-x,\quad y+z-x,\quad z+t-x .
$$
They must permute $x,y,z,t$. Summing gives $y+z=4x$. One of $x,y,z,t$ equals zero. If $z=0$, two weights coincide. If $x=0$, the remaining two weights $y+z,z+t$ must permute $z,t$. As $y\ne0$ this forces $y+z=t$ and then $t=0$, impossible.

If $y=0$, then $z=4x$. The weight $-x$ cannot be $x$, since that would imply $z=0$. If it were $t$, the weight $3x$ would have to be $x$ or $4x$, again impossible. Thus $-x=z$ and $x$ has order five. The remaining weights force $t=-2x$, which works for every such $x$. If $t=0$, the weight $3x$ must be one of $x,y,z$. Equality with $y$ or $z$ would make the other equal $x$. Therefore $2x=0$, $z=-y$, and subtracting $x$ interchanges $y$ and $z$. This is equivalent to $2y=x$ with $y$ of order four. Every such choice works. The exact count is $2\mathbf1_{4\mid n}+4\mathbf1_{5\mid n}$ before ordering the additional leaves.

**Prescribed deficit.** Set $x=0$, choose $z$, and put $y=d-2z$, $t=d-z$. The four vertex labels are distinct if $z\notin\{0,d\}$, $2z\ne d$ and $3z\ne d$. Their edge weights are $0,y,t,d$. The other leaves copy their own labels, so the complete weights replace one occurrence of $z$ by $d$. At most $2+\gcd(2,n)+\gcd(3,n)\le7$ choices of $z$ are excluded. This proves existence for $n\ge8$. At $n=4,5$ a uniform extension always works. At $n=6,7$ direct substitution of $z=0,\ldots,n-1$ gives an allowed value for every $d$.

At a modulus $k\ge4$ below the attachment size, first retain $k-4$ leaves at $x$ and use the full block. Every omitted leaf now has a labeled parent. For a smaller attachment with a leaf at $x$, pad up to $k$ there. If a dummy leaf supplies $d$, exchange its label with a real leaf at $x$ before restriction. Distinct free labels and the prescribed deficiency condition survive the restriction. With no leaf at $x$ the attachment is a path. The short caterpillar theorem applies. At $k\le3$ use the two-label extension or the prime caterpillar theorem. [Leaf batches](../counterexample-bound.md#removing-leaves) · [Short caterpillars](caterpillar-joints.md) · [Prime extension](prime-joints.md)

For $n\ge6$ the four nonleaves ensure that the total degree equation and parallel-edge test admit a repeated partner even at the excluded moduli. This yields infinitely many failures of uniform gluing on trees which are themselves cordial. [Degree classification](repeated-moment.md)

The independent checker enumerates injections and reconstructs every original edge and every additional leaf weight. It compares both the unmarked count and every marked deficit count for all rooted kernels with up to four edges, every site, and four successive moduli per kernel. It also checks the entire four-variable neutral expression and its values through modulus 4,999. [Direct verifier](check_leaf_kernel.py)

~~~sh
python3 -B -m research.census.check_leaf_kernel
~~~

## Arbitrary additions at one site on a kernel with at most six edges

**Theorem.** Start with any tree of order at most seven and add any number of leaves at any one vertex. At every positive modulus, a prescribed cordial labeling on a core of divisible order extends across this entire tree, with **any specified shared vertex**. The number of added leaves, the modulus and the core order are unbounded.

First take the joint in the original tree. For each rooted kernel and site the checker tries an integer solution of the uniform equations in an interval of length $s$. Such a solution reduces injectively at every $k\ge s$. For the other kernels it computes the exact uniform count and tries positivity for all $k\ge s$. When needed, it adds the marked count and performs the positivity test for all deficit orders as above.

| Kernel edges | Consecutive integer witness | Uniform count suffices | Marked count used | Largest polynomial cutoff | Small-modulus inputs |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 2 | 0 | 0 | — | 0 |
| 2 | 4 | 1 | 0 | 2 | 5 |
| 3 | 10 | 2 | 1 | 3 | 65 |
| 4 | 25 | 4 | 6 | 8 | 490 |
| 5 | 74 | 10 | 11 | 20 | 2,850 |
| 6 | 224 | 19 | 19 | 24 | 14,410 |

Each row counts isomorphism types with an ordered root and site, allowing coincidence. Independently, the path from root to site decomposes such a tree into a nonempty ordered sequence of rooted trees, one per path vertex with its off-path branches. If $R$ counts ordinary rooted trees, $R/(1-R)$ gives the type counts. The checker compares against that series using a separate integer-partition enumeration. Whenever a marked count is used it also evaluates both polynomials at $s$ and $s+1$ and independently enumerates the original edge weights for every deficit at both moduli.

At $k\ge s$ the calculation handles a full $k$-edge attachment. A larger one first uses this prefix, then adds the remaining leaves at the site. A smaller one with an added leaf can be padded at the same site. Exchange that real leaf with a dummy twin if necessary to retain the deficient weight, then restrict. With no added leaves, pad at the parent of any nonroot leaf of the kernel instead. The calculation included every site. At $k<s$ it is enough to keep the number of added leaves modulo $k$, as a batch of $k$ sibling leaves always permits uniform increments. The final column gives the number of actual small rooted extensions checked by an independent finite search and recount. A singleton kernel is a star.

Finally, a joint among the added leaves meets the free tree by a single edge. The free tree has a cordial labeling at every modulus by the one-site integer theorem. Translate that labeling until the joining edge fills the old deficient weight. The old vertices then contribute uniform counts, as do the old edges together with the joining edge. [One-site theorem](../hub/one-hub-interval.md) · [Bridge rule](two-branch-joint.md#other-joints-and-arbitrary-size) · [Whole verification](check_kernel_families.py)

~~~sh
python3 -B -m research.census.check_kernel_families
~~~

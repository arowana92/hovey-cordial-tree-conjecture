# A finite test over all moduli for each rooted core

The [subsequent integer construction](universal-hub.md) proves the rational criterion for every rooted tree. In particular, the conditional obstruction below never occurs, and there are only finitely many exceptional tree–modulus pairs for each bound on the number of nonleaf vertices.

Let $H$ have $h$ vertices, rooted at $o$. Write $T_\ell$ for the tree obtained by adjoining $\ell$ new leaves at $o$, and let $m$ be the number of edges of $H$ not incident to $o$. The following test concerns ordinary trees, with no vertex labels prescribed.

**Theorem.** The following are equivalent.

1. There are distinct rational labels on $H$, with $x_o=0$, whose $h-1$ edge sums are distinct members of the vertex label set.
2. For every sufficiently large integer $k$, every $T_\ell$ is $k$-cordial.
3. For some prime $p\ge h$ with $p>5^{m/2}$, the ordinary tree $T_{p-h}$ is $p$-cordial.

If the rational condition fails, **every** prime in the range of condition 3 gives a counterexample $T_{p-h}$ on exactly $p$ vertices. The test has found no such core here. It gives a route for certifying an obstruction or proving an infinite family.

## Proof

Multiply rational labels by a common positive denominator to obtain integers. For every $k$ greater than their span, reduction retains distinct vertex labels and distinct edge sums in the vertex label set. The [periodic leaf extension](README.md) proves 1 implies 2. Unboundedness of the primes proves 2 implies 3.

For 3 implies 1, start with a cordial labeling of the $p$-vertex tree and translate to put zero at $o$. Exactly one vertex has each label and every edge has a distinct weight. Each new leaf uses its own label as its edge weight. On deleting these leaves, the sums on the remaining edges are therefore distinct members of the remaining vertex label set.

Index the positions by vertices of $H$. Each nonroot position $i$ has one parent edge, with some weight $x_{\pi(i)}$. Map the root position to the unique remaining unused weight. This defines a permutation $\pi$ of the $h$ positions. It fixes the neighbors of $o$, since their edge weights equal their labels. It permutes only the root and the $m$ positions whose parents are different from $o$. For each such position impose the equation
$$
x_{\pi(i)}-x_i-x_{\operatorname{parent}(i)}=0,\qquad x_o=0.
$$
Write $A$ for the resulting integer matrix with $m$ rows and $h-1$ columns, omitting the identically zero coordinate. Its kernel modulo $p$ contains the distinct labels just obtained.

If the rational kernel had no point with all $h$ coordinates distinct (including $x_o=0$), it would lie in the union of the pairwise equality hyperplanes. A vector space over an infinite field cannot be covered by finitely many proper linear subspaces. Equivalently, the product of finitely many nonzero linear forms in a basis of that vector space cannot vanish identically. Hence some single equality $x_i=x_j$ would hold throughout the rational kernel. The corresponding difference row would be in the rational row span of $A$.

Let $d$ be the rational rank of $A$. Each row has Euclidean norm at most $\sqrt5$ as it is a sum of one positive and two negative unit coordinates, possibly with identifications or omission of $o$. Every nonzero $d$-minor is bounded in absolute value by $5^{d/2}\le5^{m/2}$. Thus $A$ has the same rank $d$ modulo $p$, including the case $d=0$. Appending the difference row leaves the rational rank $d$, so all augmented $(d+1)$-minors are zero integers. The augmented rank modulo $p$ is also $d$. The equality would therefore hold throughout the modular kernel as well, contradicting the distinct modular labels. This proves 1.

## Deciding the whole family

There are only $(m+1)!$ candidate permutations. For each, rational elimination describes all coordinate functions on the kernel. Reject it if two such functions coincide. Otherwise choose a point off the finitely many equality hyperplanes and clear its denominators. This gives either an explicit integer witness or an exhaustive obstruction checked using only rational linear algebra. The program uses the free-parameter curve $(1,t,t^2,\ldots)$ and tries integer values of $t$. Two distinct coordinate functions become distinct polynomials, so only finitely many $t$ are excluded.

If a witness with span $S$ is found, only $1\le k\le S$ require any more work to decide whether **every** $T_\ell$ is cordial for **every** $k$. For each such $k$, it suffices to test $0\le\ell<k$. From any cordial labeling, attaching $k$ more leaves at the root and using all residues once adds one to every vertex and edge count. For $k\ge h$ it suffices to test just $T_{k-h}$. The preceding restriction argument on $k$ vertices works for composite $k$ as well, and the periodic leaf extension then gives every $T_\ell$ at this modulus.

There is also an explicit bound before the computation. For $h\ge2$ put
$$
M=\max(h,\lceil5^{m/2}\rceil),\quad J=\binom h2,\quad K=2(h-1)MJ.
$$
If the rational condition holds, it has an integer witness of span at most $K$. Indeed, choose a nonsingular $d$-minor of $A$ for a successful permutation, using determinant 1 at rank zero. Put the free coordinates equal to the determinant times free integer parameters. Cramer's rule expresses all coordinates as integer linear forms with coefficients bounded by $M$, since each coefficient is a minor of the same row-restricted matrix up to sign. The product of the $J$ coordinate differences is a nonzero polynomial in the parameters of degree $J$. It cannot vanish on the whole grid $\{0,\ldots,J\}^{h-1-d}$, by repeated univariate interpolation. At a nonvanishing grid point each coordinate has absolute value at most $(h-1)MJ$.

If the rational condition fails, a prime strictly between $M$ and $2M$ exists by Bertrand's postulate, giving a counterexample with modulus at most $K$. Thus, for each individual core, testing $k\le K$ and $0\le\ell<k$ is a sufficient finite test of the entire two-parameter family. For $h=1$ the trees are stars and a periodic list of all residues on the leaves works directly. The bound is for a fixed core and grows with its order.

For example, the following computes an integer witness for a seven-vertex core. The input gives the parent of each vertex, with $-1$ for the root. The concrete output is $[0,-7,3,-4,-1,1,2]$, with edge sums $-7,-4,-1,2,1,3$. It works at every $k>10$ and permits arbitrarily many added leaves.

~~~sh
python3 -B -m research.hub.rational -1 0 1 2 2 0 5
~~~

[Exact rational search](rational.py)

## Attaching paths and stars of unbounded sizes

The rational condition admits direct constructions on cores of unbounded order. Suppose a core already has integer vertex label set $A$, root zero, and edge weights $A\setminus\{s\}$. Either of the following operations at the root preserves this property, with a possibly different missing weight.

- **A new neighbor with $d\ge1$ leaf children.** Label the neighbor $b$ and its children $s-b,s-2b,\ldots,s-db$. Their edges use $s,s-b,\ldots,s-(d-1)b$, and the root edge uses $b$. The new missing weight is $s-db$.
- **A path of $t\ge2$ new vertices.** Call their labels $x_1,\ldots,x_t$ in order away from the old root. Set $x_{t-1}=b$, $x_t=s-b$, then solve backwards by $x_{i-1}=x_{i+1}-x_i$ for $i=t-1,\ldots,2$. The root edge uses $x_1$, the last edge uses $s$, and the other edges use $x_3,\ldots,x_t$. The new missing weight is $x_2$.

In the first construction the coefficients of $b$ on the new vertices are $1,-1,-2,\ldots,-d$. In the second, read backwards from the tip, they are $-1,1,-2,3,-5,\ldots$ by the recurrence. In either case the coefficients are nonzero and pairwise distinct. Consequently only finitely many integers $b$ give a collision between new labels or with any old label. A single new leaf can always take any fresh integer label, keeping $s$ as the missing weight.

Starting with just the root and repeating proves condition 1 for any mixture of such branches. In particular, fix the lengths of arbitrarily many paths sharing an endpoint, or fix arbitrarily many stars joined by their centers to one root. For every sufficiently large modulus, any number of further leaves can then be added at the root. The threshold depends only on the fixed branches.

A direct bound also works for composite moduli. Let $h$ be the order of the fixed core formed from these branches. In each construction include coefficient zero for the old vertices, and let $D$ be the largest absolute difference between two distinct coefficients in any step (take at least one). At a new step each possible collision involving a new vertex excludes at most $D$ choices of $b$ modulo $k$, since a congruence $ab=c\bmod k$ with $a\ne0$ has at most $\gcd(|a|,k)\le |a|$ solutions. There are at most $\binom h2$ pairs per step. Hence every $k>D\binom h2$ works directly, uniformly over the number of further root leaves.

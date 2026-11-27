# Extending any nine-vertex forest at a prime

**List theorem.** Let $p\ge11$ be prime. Add nine new vertices to a labeled core as a rooted forest, with exactly one edge from each component to the core at its root. Each new vertex has its own list of at least $(p+9)/2$ allowable residues. Prescribe arbitrary additive offsets on the new edges and forbid any common set of at most $(p-11)/2$ edge weights. The nine vertices can receive distinct labels from their lists with all nine new weights distinct and outside the forbidden set.

**Consequence.** At any odd prime $p\ge5$, the order of a smallest counterexample to Hovey's conjecture, written $mp+s$ with $1\le s\le p$, must have $s\ge(p+11)/2$. The same restriction applies if the edge weights include independently prescribed offsets. In particular every tree of order at most $\min(p,(p+9)/2)$ has a labeling with distinct vertex labels and distinct edge weights even with these offsets.

At 29 it raises the first possible residue to 20. The full conjecture concerns all order residues and every modulus.

## The coefficient test

Put $r=9$ and $e=(p-11)/2$. Enlarge the forbidden set to size $e$. Write $X_i$ for each new vertex label, $Y_i$ for its edge weight to its parent, and $V$ for the Vandermonde polynomial. The top homogeneous part of
$$
V(X)V(Y)\prod_i\prod_{w\text{ forbidden}}(Y_i-w)
$$
is $V(X)V(Z)\prod_i Z_i^e$, where $Z_i=X_i+X_{p(i)}$ at internal edges and $Z_i=X_i$ at component roots. The parent label in the core and all prescribed offsets only affect lower degrees. A nonzero coefficient at exponents summing to the total degree supplies distinct labels and weights if each input list has more entries than its vertex exponent. This is the finite-grid coefficient lemma. [Alon, *Additive Latin Transversals*](https://www.cs.tau.ac.il/~nogaa/PDFS/alt2.pdf) · [Grid interpolation proof](../rainbow/prime-star.md#a-signed-count-independent-of-the-boundary-modulo-p)

Use the following three choices of monomial.

1. At forbidden size $e$, take all vertex exponents equal to $r+e-1$.
2. Enlarge the forbidden set to size $e+1$ and take all vertex exponents equal to $r+e$.
3. At size $e$, start with the first monomial, increasing one exponent and decreasing another by one.

All three respect the available list size $r+e+1=(p+9)/2$. When a choice is nonzero, the constructed weights avoid the original forbidden set.

## Evaluating a forest exactly

Allow any number $r$ of rows for the recurrence. Use an exponent adjustment $d_i$ at row $i$, with $\sum d_i=0$. The uniform coefficient has all $d_i=0$. Expand the two Vandermondes. After reversing the exponent order in the first determinant, the still required powers are $e+t_i+d_i$, and the offered powers are $e+z_i$, where both $t$ and $z$ permute $0,\ldots,r-1$. For each vertex $v$, let $T_v$ be its subtree. The power transferred to its parent is forced to equal
$$
a_v=\sum_{i\in T_v}(z_i-t_i-d_i).
$$
Indeed the power available at $v$ is $e+z_v$ plus the transfers from its children. Reject negative transfers and require zero at every component root. For an integer $e\ge0$, any transfer exceeding $e+z_v$ contributes zero as a binomial. The coefficient is the sum over the surviving permutation pairs of
$$
(-1)^{\binom r2}\operatorname{sgn}(t)\operatorname{sgn}(z)
\prod_v \binom{e+z_v}{a_v}.
$$
The same expression with generalized binomials defines a polynomial in $e$ over the rationals. Subtree sums of two equally large subsets of $0,\ldots,r-1$ differ by at most $|T_v|(r-|T_v|)$. At $r=9$ the uniform evaluations consequently have transfer at most 20. Their polynomial denominators are units at every prime $p>20$.

The calculation groups permutation pairs by the two exponent subsets on each subtree. Splitting a forest across components contributes the signs of the two shuffles. Removing the root of a component leaves its child forest, with the two singleton exponents of the root and its forced binomial factor. This gives an exact recurrence with the empty forest contributing one. The independent implementation runs the expansion forward. It multiplies child tables, appends each possible unused pair of indices to insert the parent, and sums equal exterior monomials with their signs. It builds its rooted-forest representatives by growing a dummy-rooted tree one leaf at a time. Both computations use integer arithmetic after clearing the dyadic denominators. The denominator of $\binom{x}{a}$ divides $4^a$ for half-integral $x$, by multiplying the expansion of $(1+z)^{-1/2}$ by an integral power of $1+z$. [Backward subset calculation](forest_subsets.py) · [Independent forward expansion](forest_exterior.py)

## The 719 forests

At $p>20$, the two uniform coefficients reduce from the rational evaluations at $e=-11/2$ and $e=-9/2$. For every rooted forest on nine vertices compute the greatest common divisor of their reduced numerators. The gcd is nonzero in all 719 cases. The only primes above 20 dividing a gcd are 23, 29 and 31, each in exactly one shape. At smaller primes evaluate the same coefficients at the actual nonnegative integer forbidden sizes. Each remaining shape has a nonzero coefficient of the third type.

| Prime | 11 | 13 | 17 | 19 | 23 | 29 | 31 | Other primes above 20 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Forests requiring the shifted monomial | 9 | 2 | 1 | 0 | 1 | 1 | 1 | 0 |

For example, at 23 take the parent vector $(-1,0,1,0,3,4,0,6,7)$, where $-1$ means attachment to the core. Raising the exponent at vertex 0 and lowering the exponent at vertex 1 gives coefficient 3 at $e=6$. The corresponding parent vectors at 29 and 31 are $(-1,-1,-1,2,3,4,4,6,6)$ and $(-1,0,1,2,0,4,5,6,7)$. The same two exponent changes give 22 and 17 respectively. These numbers refer to zero-based vertex indices in precisely the order displayed.

## The order of a smallest counterexample

For $p\ge17$, suppose a smallest counterexample has $10\le s\le(p+9)/2$. Delete nine vertices by successively removing leaves, retaining a connected tree. Starting from a cordial labeling of that smaller tree, its high vertex bins number $s-9$ and its high weight bins number $s-10$. There are $p-s+9\ge(p+9)/2$ allowable vertex residues per row and at most $(p-11)/2$ forbidden weights. By the list theorem the new labels and weights increment only distinct low bins. The restored tree is cordial.

At $s=1$ the smaller tree after deleting a leaf has uniform vertex bins. Assigning the unique label that gives the deficient weight extends it. For $2\le s\le9$, deleting a single leaf leaves $s-1$ high vertex bins and $s-2$ high weight bins. At most $2s-3\le15<p$ labels are forbidden, even after accounting for its edge offset. The primes through 13 are already settled with arbitrary offsets. For the assertion about distinct labels and weights at small orders, apply the same induction up to $(p+9)/2$, which is below $p$ for $p\ge11$. At $p=5,7$ the distinct-label conclusion applies only through order $p$ by cardinality. [Small-prime offset theorem](README.md)

## Reproduction

From the repository root run

~~~sh
python3 -B -m research.biased.check_nine_row_lists
~~~

The default checks all 719 pairs of rational coefficients in both directions, repeats the complete integer evaluations at 11, 13, 17 and 19, and reproduces every shifted exception with both algorithms. A direct double-permutation sum also checks every rooted forest through five vertices at two integer forbidden sizes. The universal prime statement follows by exact gcds and the denominator bound. [Proof replay](check_nine_row_lists.py)

# A list coefficient for a star with forbidden edge weights

**Consequence for ordinary trees.** At any odd prime $p\ge5$, write the order of a smallest counterexample as $mp+s$ with $1\le s\le p$. Then
$$
s\ge (p+7)/2.
$$
At $p=29$, a smallest counterexample must therefore have $18\le s\le29$. For ten of the thirteen residues from 17 through 29 the upper leaf bound $L\le 2s-p-2$ can also be decreased by one. The remaining three residues impose a local restriction on the leaf parents. The arguments below concern a hypothetical *smallest* counterexample at a fixed modulus.

## The list theorem

Over $\mathbb F_p$, attach $r$ new vertices to a labeled core. One new vertex has $j$ new children, and the center and the other $r-j-1$ vertices each have one edge to the core. All boundary labels and all edge offsets are arbitrary. Prescribe an independent input list of size at least $r+e$ for each new vertex and a common set of $e$ forbidden edge weights. Assume $1\le r\le r+e\le p$.

Define
$$
H_{r,e}(q)=\sum_{t=e}^{e+r-1}\sum_{i=e}^t {t\choose i}q^{t-i},\qquad
A_{r,j,e}=\sum_{q=0}^j(-1)^q{r\choose j-q}H_{r,e}(q).
$$
If $A_{r,j,e}\ne0\pmod p$, distinct labels in the prescribed lists give distinct weights outside the forbidden set. No restriction is imposed on coincidences among the incoming shifts. A zero coefficient leaves the extension undecided.

Write $X_i$ for the vertex variables and $Y_i$ for the actual new edge weights. With $V$ the Vandermonde and $W$ the forbidden set, use
$$
P=V(X)V(Y)\prod_i\prod_{w\in W}(Y_i-w).
$$
Its degree is at most $r(r+e-1)$. The coefficient of $\prod_i X_i^{r+e-1}$ equals
$$
(-1)^{\binom r2}j!(r-j-1)!A_{r,j,e}.
$$
Only the homogeneous linear parts of $Y_i$ and the top part of the forbidden-weight factors contribute. They are $X_i$ except at the children, where they are $X_i+X_c$ for the center $c$. A nonzero coefficient guarantees a point of the list grid where $P$ is nonzero, by multivariate interpolation. Both factorials are units even at $r=p$. [Grid coefficient lemma and proof](../rainbow/prime-star.md#a-signed-count-independent-of-the-boundary-modulo-p) · [Alon, *Additive Latin Transversals*](https://www.cs.tau.ac.il/~nogaa/PDFS/alt2.pdf)

To calculate the coefficient, expand $V(X)$ as a determinant. The still-required powers $t_i$ permute $I=\{e,\ldots,e+r-1\}$ in the reverse exponent order, explaining the common sign. The second determinant times $\prod Y_i^e$ supplies another permutation $z_i$ of $I$. At every singleton $z_i=t_i$. For a child the multiplier is $\binom{z_i}{t_i}$, with out-of-range binomials zero. The remaining exponent at the center is automatic by total degree.

Put $B_{it}=\binom{t}{i}$ on $I$, and let $J$ be the all-ones matrix. Fix the subset $S$ of $j+1$ exponents at the active vertices. For a choice of the center exponent, summing over the second permutation gives the determinant of $B_{S,S}$ with its center row replaced by ones. The other target assignments contribute $j!(r-j-1)!$ identical terms after relabeling. Summing over center exponents replaces the determinant by the derivative at $v=0$ of $\det(B_{S,S}+vJ_{S,S})$, by multilinearity. Consequently the reduced coefficients $A_{r,j,e}$, in order $j=0,\ldots,r-1$, are the coefficients of
$$
\left.u^{-1}\frac{\partial}{\partial v}\det(I_r+uB+uvJ)\right|_{v=0}
=(1+u)^r\mathbf{1}^{T}(I_r+uB)^{-1}\mathbf{1}.
$$
Here the principal-minor expansion collects all $S$ and $B$ is unit triangular. The binomial identity for two successive translations gives $(B^q)_{it}=\binom{t}{i}q^{t-i}$ for $i\le t$, also at $q=0$ with $0^0=1$. The intermediate indices range only from $i$ to $t$, so truncation to $I$ preserves that identity. Expanding the inverse as a formal power series gives the stated formula. For exact evaluation the coefficient of $q^d$ in $H$ is $\binom{e+r}{d+1}-\binom{e+d}{d+1}$ by summing a diagonal.

## Closed cases without forbidden weights

For $e=0$, $H(q)=\sum_{t=0}^{r-1}(1+q)^t$. The same rational generating function expanded at infinity has two highest coefficients $\mathbf 1^TB^{-1}\mathbf 1$ and $r\mathbf 1^TB^{-1}\mathbf 1-\mathbf 1^TB^{-2}\mathbf 1$. These use translations $-1,-2$. Thus $A_{r,r-1,0}=1$, and for $r\ge2$ we have $A_{r,r-2,0}=r-(r\bmod2)$. In particular a star with one additional singleton admits arbitrary separate lists of size $r$ whenever $p>r$.

- For $r=p-1$, $A_{r,j,0}=(-1)^{j+1}\pmod p$ for every $j$. All geometric sums with $1\le q\le j$ vanish and $H(0)=p-1$. This permits a different forbidden input at each row in the [prime star extension](../rainbow/prime-star.md).
- For $r=p-2$ at an odd prime, $A_{r,j,0}=(-1)^{j+1}(j+2)\sum_{i=1}^{j+1}1/i\pmod p$. Here $H(0)=-2$ and $H(q)=-1/(q+1)$ for $1\le q\le j$, while $\binom{p-2}{m}=(-1)^m(m+1)$ in the field.
- For $r=p$ and $1\le j<p$, only $q=j$ contributes and $A_{p,j,0}=(-1)^j\pmod p$. At arbitrary composite moduli and any number of full periods, the [exact center congruence](pinned-periods.md#exact-uniform-increments-with-one-free-parent) also applies.

## Excluding an order residue

The [leaf argument](spare-lists.md#restoring-leaves-on-a-cordial-core-of-arbitrary-order) gives $L\le 2s-p-2$ in any smallest counterexample. A path is cordial, so $L\ge3$ and consequently $s\ge(p+5)/2$. At the smallest remaining residue $s=(p+5)/2$, there must be exactly three leaves. Delete them. The remaining tree has at least two vertices and at least two terminal vertices. Each terminal had at least one original leaf child, so some terminal has exactly one. Delete that terminal as well. The four removed vertices form a two-vertex rooted star and two singletons.

The retained tree is cordial by minimality. Its order is $mp+u$ with $u=s-4\ge1$. Its $u$ high vertex bins are forbidden inputs, and its $e=u-1=(p-5)/2$ high weight bins are forbidden outputs. Each list contains $p-u=4+e$ entries, so the four-row theorem applies. For $r=4$, $A_{4,j,e}$ is a polynomial in $e$ of degree at most three, as follows by summing the four rows of binomials of degree at most three. Substitution of $e=-5/2$ gives
$$
A_{4,1,-5/2}=211/16,\qquad A_{4,2,-5/2}=61/4.
$$
The denominators are units and the polynomial evaluation agrees with $e=(p-5)/2$ in every field of prime order $p\ge5$. Thus the one-child reduction works except at $p=211$. At 211, if any terminal has two original leaf children the second coefficient works instead.

It remains to treat $p=211$ with all terminals supporting one original leaf. Delete two distinct terminals after the three leaves. The remainder is connected and has order $211m+103$ since $s=108$. The five removed rows are two disjoint two-vertex paths and a singleton; the common forbidden output size is 102. Lists have size $211-103=108\ge5+102$. The exact top grid coefficient for this forest is $66\pmod{211}$. It follows that this case also extends and the claimed lower bound on $s$ holds.

Here is a finite certificate for the last scalar. Take the parent array $(-1,0,-1,2,-1)$ and expand the two determinants as above. For each pair of permutations $t,z$ of $\{0,1,2,3,4\}$, visit vertices from last to first. At $v$, the exponent transferred to its parent must equal $a_v=z_v-t_v+\sum_{w\text{ child of }v}a_w$. Discard the term if $a_v<0$, if $a_v>102+z_v$, or if $a_v\ne0$ at a component root. Otherwise multiply its two permutation signs by $\prod_{v\text{ nonroot}}\binom{102+z_v}{a_v}$. The reversal sign is $(-1)^{10}=1$. Summing the $120^2$ terms with the stated rejections yields 66 modulo 211. An independent calculation multiplies the linear factors at $e=0,\ldots,8$ and interpolates: each of the two children can transfer at most four powers, so the exact coefficient has degree at most eight in $e$. [Finite sum](forest_grid.py) · [Independent polynomial check](check_star_lists.py)

## A test at the extremal leaf count

Suppose $L=2s-p-2\ge3$. Delete all leaves and one terminal of the remaining tree, obtaining a star with $j$ children and singleton rows, where $j$ is the number of original leaves there. The surviving tree has $u=s-r$ high vertex bins and $e=u-1=p-s$ high edge bins, where $r=L+1$. Its $p-u=r+e$ available input labels meet the list theorem. Every terminal of the tree left by the first deletion must therefore have $A_{r,j,e}=0$ modulo $p$ in a minimum counterexample. If the first deletion leaves only one vertex, the original tree was a star.

At $p=29$, evaluating the formula at every $17\le s\le29$ leaves the following possible values for $j$. For the other ten residues there are none, so $L\le2s-32$ there. These conditions only concern a tree attaining the previous upper bound $L=2s-31$.

| Order residue $s$ | Child counts $j$ surviving the coefficient |
| ---: | --- |
| 20 | 1 |
| 26 | 10, 16 |
| 28 | 9, 25 |

The [two-terminal extension](two-star-lists.md) eliminates the equality case also at these three residues, and at every residue for each prime from 29 through 61.

## Verification

From the repository root run

~~~sh
python3 -B -m research.biased.check_star_lists
~~~

The checker multiplies linear factors to verify 98 exact integer coefficients for varying $r,j,e$. A separate backtracking search checks the actual list constraints, offsets and forbidden weights in 2,070 examples through modulus 17. It also checks the closed forms through prime 127, the table at 29, and both evaluations of the exceptional forest at 211. [Formula and finite table](star_lists.py) · [Checker](check_star_lists.py)

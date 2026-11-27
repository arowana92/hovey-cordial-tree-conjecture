# Two leaf populations in a prime signed count

Give each edge an independently prescribed additive offset. At prime order $p$, the [degree lemma](README.md#signed-counts-and-first-moments) makes the signed number of rainbow labelings modulo $p$ independent of these offsets. A nonzero scalar computed at zero offsets proves existence for **every** offset assignment. All results below use this implication.

**Theorem.** At every prime modulus and every tree order, arbitrary offsets are possible for the following trees. Start with a path of length two or three and attach any numbers of leaves at its two ends. At length two one may also attach one leaf at its middle vertex.

Another family starts with adjacent vertices $A,D$, any populations of leaves attached there, and one extra two-edge path at $A$. It works for every prime $p$ at every order different from $p$. At order $p\ge5$ there are at most two possible exceptional populations at $D$, specified below. In particular every order works for $p\equiv5,19\bmod24$. The possible exceptions concern the signed test.

## A determinant for any fixed core

Take a fixed tree $B$ of order $h\ge2$, with distinct marked vertices $A,D$. Add $a$ labeled leaves at $A$ and $b$ at $D$ where $h+a+b=p$. Root the core at $A$. Translate to set $f(A)=0$ and dilate to put $f(D)=1$. The latter normalization divides the signed count at zero offsets by $p-1$, since scaling conjugates the permutation defining its sign. For each injection $x:V(B)\to\mathbb F_p$ with these two values, write $w_v=x_v+x_{\rm parent(v)}$ for nonroot core vertices. Write $[t]_p$ for the least nonnegative residue. Then the **integer** signed count in the root-zero normalization is
$$
(p-1)a!b!(-1)^b\!
\sum_{x,\pi} {\rm sgn}(\pi)\,
 {\bf1}\!\left\{\sum_{v\ne A}[x_{\pi(v)}-w_v]_p\le b\right\},
$$
where $\pi$ ranges over permutations of the $h$ core vertices. Only the core labels and a finite permutation appear.

To prove this, use rows indexed by vertex residues and columns by weight residues. In the unpinned rows use $C=I+tS$, with $S_{i,i+1}=1$ cyclically. Replace row zero by ones, so it supplies the missing weight. Replace row $x_v$ for each other core vertex by the unit row at $w_v$. The coefficient of $t^b$ in the determinant sums the signs for anonymous leaves at fixed core labels. The $b$ translated rows are the leaves at $D$, and the untranslated rows are the leaves at $A$. Multiplying by the two factorials restores the labeled vertices.

Multiply the modified matrix on the right by $C^{-1}$. Noncore rows become identity rows, so only the principal minor of the core rows and columns remains. The original determinant is this minor times $\det C=1-(-t)^p$. The new all-ones row is constant $1/(1+t)$. Each entry in new row $x_v$, column $x_j$, is $(-t)^{[x_j-w_v]_p}/(1-(-t)^p)$ by the cyclic geometric series. Since $b<p$, all factors $1-(-t)^p$ may be replaced by one in extracting the coefficient. Expanding the small determinant and $1/(1+t)$ gives exactly the formula.

There is an arithmetic consequence for fixed $B,A,D$. After removing the factorials, the dilation factor and $(-1)^b$, the sum is a piecewise quasipolynomial in $(p,b)$. Indeed even at composite integer parameters the normalized sum itself is defined. For each $\pi$ represent each least residue by adding $mp$ to the ordinary difference, requiring the result to lie in $[0,p-1]$. Only finitely many integer carries $m$ are possible. The injection, carries and sum bound now have a Presburger description, so the finite solution counts are piecewise quasipolynomial. This argument concerns the normalized sum at an arbitrary integer parameter and uses its interpretation as a full scalar only at primes. [Woods, Theorem 1.10](https://arxiv.org/abs/1211.0020)

In particular, along $b=\lfloor\beta p\rfloor+c$ for fixed rational $\beta$ and integer $c$ in the feasible range, the test becomes periodic for all sufficiently large primes. On each eventual residue class the normalized sum is a rational polynomial $P(p)$, so for primes avoiding its denominator, divisibility by $p$ is decided by $P(0)$ apart from the finitely many prime divisors of a nonzero numerator. More generally, on each polynomial piece and coordinate residue class in two variables, either $P(0,b)$ vanishes identically or only a bounded number of feasible $b$ can make the scalar vanish at any sufficiently large prime. In the second case use the degree bound on the number of roots of a nonzero polynomial in $\mathbb F_p$, since $0\le b<p$.

## Counting the short paths directly

The leaves at $A$ have their own labels as weights. The leaves at $D$ send each of their labels $z$ to $z+1$ in the sign permutation. Their consecutive runs must terminate at available core labels or zero. Compressing $b$ such translations changes the sign by $(-1)^b$, since each inserted letter subdivides an arrow in a permutation cycle. In all cases retain the factor $(p-1)a!b!$. Take $p\ge5$, and by symmetry $b\le a$ for the path families.

* For $A-X-D$, write $x=f(X)$. The row $x$ is fixed and row $1$ goes to $1+x$. No leaf run can end at $1$, since its predecessor is zero. The leaves at $D$ are exactly $-b,\ldots,-1$. The target $1+x$ must be $-b$, because $x\ne0$. The resulting compressed permutation interchanges zero and one. The remaining signed factor is $(-1)^{b+1}$, including at $b=0$.
* For $A-X-Y-D$, let $x,y$ be the labels on $X,Y$. The free translations form a run of length $i$ ending at zero and one of length $j$ ending at $y$, with $i+j=b$. Empty runs are allowed. Thus $j+2\le y\le p-i-1$, and $x$ lies in $[2,y-j-1]\cup[y+1,p-i-1]$. The three available targets are $-i,1,y-j$, leading after compression to $0,1,y$ respectively. Row $1$ sends to $1+y$, which can only equal $-i$, giving $y=p-i-1$. Row $y$ sends to $y+x$. The target $y-j$ would give $x=-j$ outside its range. The target $1$ gives $x=i+2$, valid since $i\le b\le a=p-b-4$. This gives one positive compressed three-cycle for each split. The remaining signed factor is $(-1)^b(b+1)$.
* For $A-X-D$ with one additional leaf $Y$ at $X$, use the same $x,y,i,j$ and ranges. The two special targets now are $1+x$ and $y+x$. The table lists every possible assignment of those rows in order. Its signs refer to the compressed permutation on $0,1,y$.

| Targets | Conditions | Number for this split | Sign |
| --- | --- | ---: | ---: |
| $-i,1$ | $x=p-i-1,\ y=i+2,\ i\ge j$ | 1 | $+$ |
| $-i,y-j$ | $x=p-i-1,\ j=i+1$ | $p-b-3$ | $-$ |
| $y-j,-i$ | $x=y-j-1,\ 2y\equiv j+1-i$ | 1 if $b$ is even | $+$ |
| $y-j,1$ | $x=y-j-1,\ 2y\equiv j+2$ | 1 if $j$ is odd | $-$ |

Here $1+x\ne1$. In the second row, $j+2\le y\le p-i-2$. In the last two rows $j+3\le y\le p-i-1$ and the only possible multiple of $p$ in the congruence for $2y$ after subtraction is $p$ itself. The bounds include that multiple because $2b\le p-4$ and $p$ is odd. The parity conditions then give the listed counts. Summing with signs leaves $b+2$ for even $b$, or $b+3-p$ for odd $b$, before multiplication by $(-1)^b$. Both are nonzero modulo $p$.

## An additional two-edge arm at adjacent hubs

Write the arm as $A-X-Y$ and let $D$ be adjacent to $A$. Again $x=f(X)$ and $y=f(Y)$. Rows $1,x$ are fixed. The $b$ translations lead in runs of lengths $i,j$ to zero and $y$, so $i+j=b$, $j+2\le y\le p-i-1$ and $x\in[2,y-j-1]\cup[y+1,p-i-1]$. The last ordinary row $y$ sends to $x+y$. A target $y-j$ gives positive compressed sign and $x=p-j$, which is feasible exactly for $j>i$ and $j+2\le y\le p-j-1$. A target $-i$ has negative sign and requires $x=p-i-y$. Counting $x<y-j$ gives $\lfloor(p-b-3)/2\rfloor$ choices for every split. Counting $x>y$ gives $\max(0,\lfloor(p-b-j-3)/2\rfloor)$. Thus after removing $(p-1)a!b!(-1)^b$ the signed count is
$$
H=\sum_{j>b/2}^b (p-2j-2)_+
 -(b+1)\lfloor(p-b-3)/2\rfloor
 -\sum_{j=0}^b \bigl(\lfloor(p-b-j-3)/2\rfloor\bigr)_+ .
$$

Put $P=(p-1)/2$, $L=\lfloor b/2\rfloor$, $U=\min(b,P-1)$ and $J=p-b-3$. The first sum is $(U-L)(2P-2-U-L)$ and the last is $\lfloor J^2/4\rfloor-\lfloor ((J-b-1)_+)^2/4\rfloor$. Substituting $P\equiv-1/2\bmod p$ gives the following exact residues for $2H$.

| Population $b$ | Even $b$ | Odd $b$ |
| --- | --- | --- |
| $b\le(p-3)/2$ | $(b+3)^2-3$ | $(b+1)(b+5)$ |
| $b\ge(p-1)/2$ | $(b+1)(b+3)$ | $(b+2)^2-2$ |

The linear factors are nonzero in their indicated parity and range $0\le b\le p-4$. Hence exceptions require a square root of 3 in the lower even range or of 2 in the upper odd range. Two distinct lower roots would have even sum congruent to $-6$, impossible in the interval. Two distinct upper roots would have sum between $p-1$ and $2p-8$, incompatible with $-4$. The endpoints $b=0,p-4$ have nonzero residues, and two exceptions cannot be consecutive: at the transition the lower formula for an even $b=(p-3)/2$ equals $-3/4$. Quadratic reciprocity also shows that 2 and 3 are both nonsquares at primes $5,19\bmod24$.

## Passing to every tree order

At order below $p$, pad with leaves at a marked hub and restrict a bijective rainbow labeling. At order above $p$, retain the core and enough leaves to make order $p$. All omitted leaves have their parents already retained. Starting from a multiple of $p$, add one leaf to supply the deficient edge weight, then add up to $p-1$ further leaves with distinct new weights and distinct labels avoiding the surplus. Each effective parent shift includes the prescribed leaf offset. Repeat these batches. [Leaf extension proof](../counterexample-bound.md#removing-leaves)

For the adjacent-hub arm, below order $p$ padding at either hub allows at least two consecutive choices of $b$ at order $p$. Above order $p$, the attainable choices form $[\max(0,p-4-a),\min(b,p-4)]$. This interval has two consecutive choices unless it is an endpoint singleton. Thus one can always use a base with nonzero scalar. The cases $p=2,3$ already follow from the [unrestricted offset result](README.md).

## Checks

A direct checker chooses every set of translated leaf labels, computes weights on the actual edges and counts signs by inversions. It agrees with the small determinant on 940 coefficients, including composite integer parameters in the fixed $0,1$ normalization. The determinant also independently verifies 1,644 exact integer counts for the four families through prime 73. The modular exceptional-population bounds are checked through prime 5,000. [Determinant calculation](two_sites.py) · [Independent verifier](check_two_sites.py)

~~~sh
python3 -B -m research.biased.check_two_sites
~~~

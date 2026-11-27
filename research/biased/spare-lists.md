# Leaf extensions with one extra available residue

**Theorem.** At every modulus $k$, give $r$ leaves arbitrary individual lists of at least $r+1$ available residues. If the leaves have at most two distinct effective shifts $s_i$, they can receive distinct labels $x_i$ with all $x_i+s_i$ distinct. The effective shift includes the label of the parent and any prescribed edge offset. With lists of size $r$, the earlier [two-shift classification](leaf-lists.md#exact-two-shift-criterion-for-all-lists) gives the exact exceptions. Thus one extra residue per list suffices in every exceptional case.

This also gives a necessary condition on every smallest ordinary counterexample. Write its order as $mk+s$ with $1\le s\le k$. If $B$ is the total number of leaves at the two parents with the most leaf neighbors, counting a single parent only once, then
$$
B < 2s-k .
$$
At a prime modulus $p$ there is a stronger restriction on the **total** number $L$ of leaves,
$$
L < 2s-p-1 .
$$
In particular a smallest counterexample at an odd prime can only occur at remainders $s\ge(p+5)/2$. The convention $s=p$ denotes order divisible by $p$.

## An extra row in the coefficient calculation

Represent residues by complex $k$th roots of unity. Subtract a common shift and write the two multiplicative shifts as $1,z$, with $z$ a primitive $d$th root. Let their multiplicities be $a,b$, and put $r=a+b$. If $b\bmod d\le r\bmod d$, lists of size $r$ already suffice. A single shift can also be handled directly by choosing distinct representatives greedily.

In the remaining case write $r=qd+s$ and $b=md+h$ with $0\le s<h<d$. Then $q\ge1$ and $m<q$. Append one artificial variable with multiplier $\beta$, free to take any nonzero complex value. On the $r+1$ variables use the product of two Vandermondes, one in the input variables and one in their multiplied values. The coefficient of the product of the $r$th powers of all variables is, up to sign, the permanent of the matrix with rows $(1,\alpha,\ldots,\alpha^r)$ at the $r+1$ multipliers $\alpha$. This follows from pairing each exponent permutation in the first determinant with its reversal in the second. The same coefficient argument underlies the multiplicative proof for Latin transversals. [Dasgupta, Károlyi, Serra and Szegedy](https://services.math.duke.edu/~dasgupta/papers/finallatin.pdf)

Choose $j=s+1$. The coefficient of $\beta^j$ in the permanent is $a!b!$ times
$$
[u^b]\prod_{0\le i\le r,\ i\ne j}(1+uz^i)
=[u^b](1-(-u)^d)^q\frac{F(u)}{1+cu},
\qquad F(u)=\prod_{i=0}^{s}(1+uz^i),\quad c=z^j .
$$
For $v\ge s+1$, the coefficient of $u^v$ in $F(u)/(1+cu)$ is $(-c)^vF(-1/c)$. Since $b-\ell d\ge h>s$ for every $0\le\ell\le m$, expanding the first factor gives
$$
(-c)^b F(-1/c)\sum_{\ell=0}^m(-1)^\ell\binom q\ell
= (-c)^b F(-1/c)(-1)^m\binom{q-1}{m}.
$$
Here $c^d=1$. The value $c$ differs from $z^0,\ldots,z^s$, so the display is nonzero. Some choice of $\beta$ makes the permanent nonzero. Combinatorial Nullstellensatz applies because every real leaf has at least $r+1$ candidates, and the artificial variable can receive any list of that size. Discard its value after making the distinct selections. This proves the theorem. [Alon's grid theorem and transversal argument](https://www.cs.tau.ac.il/~nogaa/PDFS/alt2.pdf)

## More than two shifts in an arithmetic progression

Suppose the shifts of $r$ leaves are contained in $c+\{0,\delta,\ldots,(t-1)\delta\}$. Write $d$ for the additive order of $\delta$. If
$$
m=r+t-1\le d
$$
then individual lists of size $m$ always suffice. Multiplicities and omissions inside the progression are arbitrary.

Normalize the common shift and take $z$ primitive of order $d$. For $0\le j<m$ use linear forms $\ell_j(Y)=\sum_{i=0}^{t-1}Y_i z^{ij}$. Products of any $r$ distinct forms constitute a basis for the homogeneous polynomials of degree $r$ in $t$ variables. In fact, for each set $J$ of $t-1$ indices take $Y$ to be the coefficients of $\prod_{j\in J}(X-z^j)$. Exactly the forms indexed by $J$ vanish at this point. Only the complementary product survives. This proves linear independence, and the dimension is $\binom{r+t-1}{r}$.

For the required multiplicities $a_i$, at least one basis product has nonzero coefficient of $\prod Y_i^{a_i}$, since this monomial is in the space. Multiplying by $\prod a_i!$ gives the permanent on those $r$ exponent columns. Append $t-1$ artificial rows with independent multipliers, as in the two-shift proof. Assign to them the omitted exponent columns in a fixed order. The resulting monomial in their multipliers has that nonzero minor as its coefficient. Choose the multipliers to give a nonzero enlarged permanent and apply the grid theorem on $m$ variables. This proves the progression result.

For an ordinary tree with $n\ge3$ vertices and $h\ge2$ nonleaves, this yields distinct labels and sums at every $k\ge n+2h-3$. Number the nonleaf core $0,\ldots,h-1$ in breadth-first order, with siblings consecutive. In the edge leading to the next child its child index increases and its parent index never decreases. Thus the $h-1$ core sums are distinct, and their span is smaller than $k$. Each leaf parent has a core neighbor. For its shift $v$, the forbidden core labels and the forbidden core weights minus $v$ intersect in at least the label of that neighbor. At most $2h-2$ residues are excluded. The $r=n-h$ leaves therefore have lists of size at least $r+h-1$, and the $h$ core shifts lie in a progression of step one. This proof allows the leaf choices to be restricted separately to any lists of the stated size in the available sets. Stars have a direct labeling at every modulus.

## Restoring leaves on a cordial core of arbitrary order

Suppose the core has order $mk+h$ with $1\le h<k$. Its labeling has $h$ vertex bins and $h-1$ edge bins strictly above $m$. To add $r\le k-h$ leaves, exclude those high vertex bins from each list and exclude each high edge bin translated back by the leaf's shift. There are at least $k-2h+1$ available entries in each list. Distinct choices with distinct weights increment only bins of size $m$ and hence preserve cordiality. In particular two shifts suffice when $k\ge 2h+r$, and arbitrary shifts at a prime suffice when $p\ge 2h+r-1$ by the [prime leaf-list theorem](leaf-lists.md). These statements use the actual histograms on any prescribed cordial core.

For the smallest-counterexample assertions, $s=1$ is already excluded by filling the deficient edge weight with one leaf. For $s>1$, Hall's prescribed-differences theorem excludes trees with at least $s-1$ leaves, by removing that many and restoring them on a core of order one modulo $k$. [Leaf-deletion proof](../counterexample-bound.md#removing-leaves)

Consequently $L<s-1$. Delete the $B$ leaves at the two busiest parents. The smaller tree has a cordial labeling by minimality and its residue is $h=s-B\ge2$. Its two parent labels give at most two shifts. If $B\ge2s-k$, then $k\ge2h+B$ and the extension succeeds, proving the first restriction. At a prime delete all $L$ leaves and apply the prime extension with $h=s-L$. If $L\ge2s-p-1$, it succeeds. The lower bound on $s$ follows since every nontrivial tree has at least two leaves. At $p=2$ the ordinary theorem is known.

## Verification

Direct backtracking checked 26,653 families of separate lists at moduli through six, identifying reorderings within either shift class. An independent integer subset count, reduced by the cyclotomic polynomial, checked 4,560 nonzero deleted-column coefficients for all relevant multiplicities at $2\le d\le20$ and $d\le r\le3d$. Direct assignments checked 2,176 progression instances and 620 ordinary trees with zero through three full periods in the core. The tree checks rebuilt both frequency histograms from the original edges. [Checker](check_spare_lists.py)

~~~sh
python3 -B -m research.biased.check_spare_lists
~~~

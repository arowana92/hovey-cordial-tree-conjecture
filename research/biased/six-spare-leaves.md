# One spare label for up to six leaves, at every modulus

**List theorem.** Suppose $1\le r\le6$ and the $r$ rows have arbitrary shifts $b_i$ modulo $k$. Give each row its own list of at least $r+1$ residues. One can choose an entry $x_i$ from each list so that the $x_i$ are distinct and the $x_i+b_i$ are also distinct. The shifts may repeat, the lists may differ, and $k$ may be composite.

The bound is sharp as a statement uniform in the modulus for $r\ge2$. At $k=r$, give every row the entire group and take one shift equal to 1 and the others zero. Distinct inputs and outputs would both permute the group, but their sums would differ by 1.

**Consequence for Hovey's conjecture.** At any modulus $k$, write the order of a smallest ordinary counterexample as $mk+s$, $1\le s\le k$, and let $L$ be its number of leaves. Then
$$
2s-k\ \ge\ 1+\min(L,6)\ \ge\ 6.
$$
In particular $s\ge\lceil(k+6)/2\rceil$. At an even modulus, a minimum counterexample at the first remaining residue $s=k/2+3$ has exactly five leaves. At 26 these restrictions give $s\ge16$, with precisely five leaves required at $s=16$. The [prime residue theorem](pruned-forests.md) gives the stronger condition $s\ge(p+13)/2$ at odd primes.

## A polynomial certificate valid for all the shifts

More generally, let $a_1,\ldots,a_r$ be arbitrary nonzero complex numbers. From any $r$ finite lists in $\mathbb C$ of size at least $r+1$, one can choose distinct $x_i$ with all $a_ix_i+c_i$ distinct, for arbitrary constants $c_i$. For the cyclic statement embed residue $j$ as $\exp(2\pi i j/k)$, use the roots of unity corresponding to the shifts as the $a_i$, and set the $c_i$ equal to zero. Earlier polynomial methods give related transversal results for cyclic groups, including results with distinct shifts of odd order. [Sun, *On Snevily's conjecture and restricted sumsets*](https://arxiv.org/abs/math/0610893) · [Arbitrary row count with two shifts](spare-lists.md)

Let $V(X)=\prod_{i<j}(X_j-X_i)$, and form $V(X)V(a_iX_i+c_i)$. Its top homogeneous part is $V(X)V(a_iX_i)$. It suffices to find a nonzero coefficient $C_b(a)$ of a monomial $X^b$ with $0\le b_i\le r$ and $\sum b_i=r(r-1)$. The finite-grid interpolation lemma then gives a nonzero value on the lists. [Grid coefficient lemma](../rainbow/prime-star.md#a-signed-count-independent-of-the-boundary-modulo-p)

For $p$ ranging over the permutations of $0,\ldots,r-1$, determinant expansion gives
$$
C_b(a)=
\sum_{p:\ b-p\text{ is a permutation}}
\operatorname{sgn}(p)\operatorname{sgn}(b-p)\prod_i a_i^{p_i}.
$$
When this polynomial has terms, let $m_i(b)$ be the least exponent of $a_i$ among them and write $H_b=C_b/a^{m(b)}$. This removes a nonzero factor at every allowed multiplier tuple. For $r=3$ the pattern $(0,3,3)$ gives $H_b=-(a_2+a_3)$. If this and its row permutations vanished, all three pair sums would be zero, which is impossible for three nonzero complex numbers.

For all five row counts $2\le r\le6$, the integer certificates supply an identity
$$
\sum_{(b,g,h)} h\,\mathrm{Sym}\big(a^g H_b(a)\big)
   =D\,(a_1\cdots a_r)^M,\qquad D>0.
$$
Here $\mathrm{Sym}$ averages over all $r!$ permutations of the multiplier variables. Jointly permuting the $X_i$ and $a_i$ leaves the product of Vandermondes invariant. Consequently a permuted $H_b$ differs only by a nonzero monomial factor from an admissible coefficient with permuted target indices. If every admissible coefficient vanished at some allowed tuple, the left side would vanish there and the right side could not. This proves the common list theorem, including arbitrary affine intercepts. The single-row case is immediate.

| Rows $r$ | 2 | 3 | 4 | 5 | 6 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Exponent $M$ | 1 | 1 | 2 | 3 | 4 |
| Terms in the identity | 1 | 2 | 6 | 33 | 239 |

The certificate file contains $D,M$ and every triple $(b,g,h)$. The identities can be found by enumerating sorted exponent patterns $b$, forming the normalized coefficients above, and solving a rational linear system for the orbit sums of the shifted monomials of total degree $rM$. Checking the identities only requires integer arithmetic. [Five integer identities](spare-leaf-identities.json)

## Restoring leaves

The [leaf-deletion argument](../counterexample-bound.md#removing-leaves) gives $L<s-1$ in a minimum counterexample. Let $r=\min(L,6)$ and delete $r$ original leaves. The core is connected and its smaller order gives a cordial labeling. Its order residue is $u=s-r\ge2$. Each new leaf has to avoid the $u$ high vertex bins and the $u-1$ high edge bins translated back by its own parent's label. Its list contains at least
$$
k-2u+1=2r-(2s-k)+1
$$
residues. If $2s-k\le r$, every list has at least $r+1$ entries. The list theorem lets these leaves occupy distinct low vertex bins and distinct low edge bins. This restores cordiality, so $2s-k\ge r+1$. The [four-leaf theorem](../census/four-leaves.md) gives $L\ge5$ for ordinary trees. At equality $2s-k=6$, this forces $L=5$.

## Reproduction

~~~sh
python3 -B -m research.biased.check_spare_leaf_identities
~~~

One verifier uses permutation signs and groups coefficients by sorted exponent vectors. The other multiplies the Vandermonde's linear factors, constructs the unsymmetrized integer polynomial and explicitly adds every variable permutation. The resulting polynomial has exactly one monomial, with coefficient $r!D$. The checker also constructs and validates 3,600 assignments on separate lists through modulus 40. The exact identities establish the result at every modulus. [Independent expansions and assignment checks](check_spare_leaf_identities.py)

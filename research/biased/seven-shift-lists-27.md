# Seven arbitrary shifts and one extra list entry at 27 labels

**Theorem (computer-assisted).** Prescribe $r$ shifts $s_i$ modulo 27 taking at most seven distinct values. Give each row its own list of at least $r+1$ residues. One can choose distinct $x_i$ from their lists with all $x_i+s_i$ distinct. The finite calculation also applies, for $r\le25$, to elements of any abelian group when the shifts lie in one coset of a cyclic subgroup of order 27.

**Tree consequence.** In a least 27-label counterexample of order $27m+s$ with $1\le s\le27$, let $B$ be the number of leaves attached to the seven busiest parents, using all parents if there are fewer. Then $B<2s-27$. Thus $B\le18,20,22$ at residues 23, 24 and 25 respectively. In particular, a counterexample on 52 vertices with 23 leaves would need **at least eight different leaf parents**.

Indeed the leaf-deletion bound gives $B\le L\le s-2$. Remove those $B$ leaves and cordially label the smaller core. Its order is $27m+h$ with $h=s-B\ge2$. At each of the $B$ rows exclude the $h$ high vertex labels and the $h-1$ high weights translated back by the row's shift. Each list has at least $28-2h$ elements. If $B\ge2s-27$, this is at least $B+1$ and the theorem restores the leaves. At most seven different old parent colors occur. [Leaf-deletion bound](../counterexample-bound.md#removing-leaves) · [Separate leaf lists](leaf-lists.md)

## The coefficient

Represent residues by powers of $z$, a primitive 27th root of unity, so that shifting row $i$ multiplies its input by $\alpha_i=z^{s_i}$. In a larger group first subtract the common shift and represent each relevant input coset by its own scaled copy of the 27th roots. Distinct cosets have disjoint images. With $N=r+1$, adjoin an artificial row with multiplier $b$. In the product of a Vandermonde in the $N$ inputs and a Vandermonde in the multiplied inputs, the coefficient of $\prod_i X_i^{N-1}$ is, up to sign, the permanent with row $i$ equal to the powers $0,\ldots,N-1$ of its multiplier. Expanding both determinants pairs each exponent permutation with its reversal, giving the same sign throughout. [Two-Vandermonde formula](spare-lists.md) · [Dasgupta, Károlyi, Serra and Szegedy](https://services.math.duke.edu/~dasgupta/papers/finallatin.pdf)

Suppose shift $a$ occurs $c_a$ times among the real rows. The coefficient of $b^j$ in this permanent, after dividing by $\prod_a c_a!$, is
$$
 [\prod_a T_a^{c_a}]\prod_{\substack{0\le i\le r\\ i\ne j}}
           \left(\sum_a z^{ia}T_a\right).
$$
A nonzero coefficient for any $j$ permits a choice of $b$ for which the original permanent is nonzero. Grid interpolation then gives distinct inputs and distinct outputs on the specified lists, using any $N$ distinct complex numbers for the dummy's list. Discard the dummy. A single shift also works by choosing distinct representatives directly. At $r=26$ in modulus 27 all lists are the full group. Append one shift making the total zero, use Hall's theorem and discard its row. [Grid interpolation](https://web.math.princeton.edu/~nalon/PDFS/alt2.pdf) · [Hall's prescribed-differences theorem](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

## Exhausting the multisets

Translation of all shifts scales the coefficient by one nonzero factor. Multiplication by a unit acts by a cyclotomic field automorphism. Enumerate every shift-set orbit under these actions, then every assignment of positive multiplicities to a representative through $r=25$. The checker counts the entire orbit of each representative and compares the sum to $\binom{27}{m}$ at each support size $m$. At fixed $r,m$ it verifies $\binom{r-1}{m-1}$ assignments per representative.

| Shift values | Support orbits | Representative assignments | Multisets before symmetry |
|---:|---:|---:|---:|
| 2 | 3 | 900 | 105,300 |
| 3 | 9 | 20,700 | 6,727,500 |
| 4 | 44 | 556,600 | 222,007,500 |
| 5 | 176 | 9,350,880 | 4,289,184,900 |
| 6 | 634 | 112,281,400 | 52,423,371,000 |
| 7 | 1,856 | 892,179,200 | 426,876,021,000 |

All **1,014,389,680** representative inputs have a nonzero coefficient. Evaluation at $z=19$ in $\mathbb F_{487}$ certified all but seven, for which $z=3$ in $\mathbb F_{109}$ sufficed. Both roots have order 27, so a nonzero reduction proves nonvanishing over the complex numbers. One implementation computes the full product and removes a selected linear factor by polynomial division. A second calculation multiplies the products on the two intervals on either side of the deleted exponent, evaluating the resulting coefficient by convolution. They agree on all counts. [C++ verifier](check_spare_cofactors.cpp)

For the multiplicities $(3,4,4,3,1,2)$ at shifts $(0,3,6,9,12,18)$, every tested deletion vanishes modulo 487. An exact calculation counted assignments by their exponent modulo 27. Reduction by $\Phi_{27}(z)=1+z^9+z^{18}$ confirmed nonvanishing for all 18 deletions. A separate test chose physical leaf labels from individually restricted lists and rebuilt all endpoints on 280 trees of orders 48 through 52. [Integer arithmetic and whole-tree examples](check_spare_cofactor_examples.py)

## A prime-power result at full list size

Let $Q$ be a prime power. Suppose the shifts lie in a coset of a cyclic group of order $Q$ in an abelian ambient group. Arbitrary separate lists of size at least $Q$ suffice for **every $r<Q$**, regardless of the number of different shifts. They also suffice for $r=Q$ if the shifts sum to zero in normalized cyclic coordinates. To normalize, subtract a common coset representative and identify the subgroup with $\mathbb Z_Q$. For $r=Q$ the zero-sum condition is independent of the chosen representative.

Pad to $Q$ rows with a zero-sum list of shifts. This is always possible when $r<Q$. The rows then have multipliers which are $Q$th roots of unity. For a primitive $Q$th root $\zeta$, the eigenvalue product of the generic circulant determinant is $\prod_{j=0}^{Q-1}(\sum_a T_a\zeta^{ja})$. As above, its coefficient at the prescribed multiplicities coincides with the Fourier permanent needed for grid interpolation, up to the nonzero row factorials and a possible overall sign. Hall's theorem places every zero-sum multiset of shifts on a permutation of $\mathbb Z_Q$. Its monomial therefore occurs in the **circulant permanent**. Thomas proved that at prime-power order the generic circulant determinant and permanent have the same monomial support, so the determinant coefficient is nonzero. Apply interpolation to the $Q$ rows and discard the dummies. The exact checker compared signed circulant coefficients with all zero-sum multisets at $Q=2,3,4,5,7,8,9$, covering 3,802 nonzero monomials. [Hugh Thomas, *The Number of Terms in the Permanent and the Determinant of a Generic Circulant Matrix*](https://arxiv.org/abs/math/0301048) · [Independent checker](check_spare_cofactor_examples.py)

~~~bash
set -euo pipefail
out=$(mktemp -d)
c++ -O3 -std=c++17 research/biased/check_spare_cofactors.cpp -o "$out/check"
for mode in divide split; do
    for m in {2..7}; do "$out/check" "$mode" "$m" 1 25; done > "$out/$mode"
done
cmp "$out/divide" "$out/split"
cat "$out/split"
python3 -B -m research.biased.check_spare_cofactor_examples
~~~

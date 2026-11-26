# Checking a proposed polynomial route to the order-equals-modulus case

The base case of the forest induction asks for a bijection from an $n$-vertex tree to $\mathbb Z_n$ with distinct edge sums. Gnang and Williams study this question for odd $n$ using a rooted parent map with a loop at its root. Two auxiliary statements in their 2022 preprint can be tested on the three-vertex path. A separate calculation below evaluates the symmetrized leading term in their composition argument and gives a normalization that counts valid labelings. [Gnang and Williams, version 1, Propositions 4 and 9 and Lemma 10](https://arxiv.org/pdf/2201.02240) · [Müyesser and Pokrovskiy, Conjecture 1.3 and the bounded-degree theorem](https://arxiv.org/html/2509.05280v2#S1)

## Translating a partial assignment

Take $n=3$, $f(0)=f(1)=0$, $f(2)=1$, and omit index 0. On indices 1 and 2, the values $i+f(i)$ are 1 and 0 modulo 3. For $g(i)=f(i+1)$ the corresponding values are 2 and 2. This contradicts the fixed-omission assertion of Proposition 4. In general $i+g(i)=(i+c)+f(i+c)-c$ for $g(i)=f(i+c)$, so an omitted set $T$ for $f$ gives the omitted set $T-c$ for $g$.

## The polynomial remembers the unrooted tree

For variables $x_v$ and ordinary tree edges $e=uv$, put $m_e=x_ux_v$. The polynomial in Proposition 9 is
$$
P_T(x)=\prod_{i\ne j}(x_j-x_i)\prod_{e\ne f}(m_f-m_e).
$$
Both products use ordered pairs. On the path $0,1,2$ rooted at its end 0, exchanging 0 and 2 preserves the first product and exchanges the two edge monomials. It therefore preserves $P_T$. The exchange moves the unique loop of the directed parent graph, contradicting the asserted equality of stabilizers.

**Corrected stabilizer.** For every finite tree $T$, the variable permutations preserving $P_T$ are exactly the automorphisms of the unrooted tree. To recover a specified root $o$, the polynomial $x_oP_T$ has precisely the rooted automorphism group and the same nonvanishing set on roots of unity.

Every tree automorphism permutes both sets of factors. For the converse, use unique factorization over $\mathbb Q$. The exponent of $x_v$ in $P_T$ is $d(v)(d(v)-1)$: precisely the ordered pairs of different edges at $v$ contribute one factor $x_v$. This recovers every vertex degree for a nontrivial tree, since its degrees are positive. For two disjoint edges $ij,ab$, the factor $x_i x_j-x_a x_b$ is irreducible. Indeed it is primitive and linear in $x_i$ over the ring of the remaining variables. Its two monomials recover the two edges. Incident edges contribute only linear or monomial factors. Thus the polynomial recovers all edges that have a disjoint edge.

At diameter at least four every edge has a disjoint edge, since an edge meeting every other edge would give diameter at most three. At diameter three the tree is a double star. Each pendant edge has a disjoint pendant edge, and the two vertices of degree at least two determine the remaining edge. A star is determined by its center, and the cases of one or two vertices are immediate. This proves the converse. All variable exponents in the monomial factor are even, so multiplying by $x_o$ singles out $o$ by an odd exponent.

In particular, an automorphism of the squared parent map that fixes the root and fails to preserve the original rooted tree also fails to preserve its unrooted tree. The corrected stabilizer still detects this formal asymmetry.

## What survives evaluation on roots of unity

Let $\mu_n$ be the complex $n$-th roots of unity. Assign them bijectively to the vertices. The edge products $m_e$ encode the edge sums modulo $n$. Each monomial of $P_T$ has total degree
$$
d=n(n-1)+2(n-1)(n-2)\equiv4\pmod n .
$$
For every $n\nmid4$, the sum of $P_T$ over all bijective assignments is zero. Indeed, multiplying all assigned roots by a primitive $n$-th root $\zeta$ permutes the assignments and multiplies every value by $\zeta^4\ne1$. The same vanishing holds for the sum over labeled copies modulo the rooted automorphisms, since stabilizer repetitions all have the same multiplicity.

This applies in particular to the leading $P_{f^2}$ term symmetrized over cosets in the proof of Lemma 10. For the three-vertex endpoint-rooted path above, $f^2$ is constant and gives a star. All bijections give it distinct ordinary edge products. Summing over the three possible centers still gives zero. Thus the asserted nonzero constant from that leading orbit sum is unavailable even when the squared tree has a witness. Formal asymmetry alone also cannot certify variation on this grid: for example $x_0^n-1$ is formally asymmetric and vanishes throughout the grid.

**A normalization with no cancellation.** Write $D=\prod_{a\ne b\in\mu_n}(b-a)$, $\eta=\prod_{a\in\mu_n}a$, and $M=\prod_e m_e=\prod_v x_v^{d(v)}$. If two edge products coincide, $P_T=0$. Otherwise write $z$ for the missing root. Removing from $D$ the ordered pairs involving $z$ divides it by
$$
(-1)^{n-1}\left(\prod_{a\ne z}(z-a)\right)^2
=(-1)^{n-1} n^2 z^{-2},
$$
by differentiating $X^n-1$. Since $Mz=\eta$, the normalized value
$$
\frac{(-1)^{n-1}n^2}{D^2\eta^2}\;M^2P_T
$$
is exactly 1 on rainbow assignments and 0 on all the others. Its orbit sum over bijective assignments counts ordinary base witnesses. Showing that this count is positive for every tree is still required. These computations address auxiliary claims in the proposed proof. The path itself has a cordial labeling.

The same constant-magnitude identity works directly for a forest with $n-1$ prescribed-parent edges: if all edge products are in $\mu_n$, then $\prod_{i<j}|m_i-m_j|^2$ is zero when any coincide and is $n^{n-2}$ otherwise. This follows by removing the factors involving the missing root from the full squared Vandermonde of magnitude $n^n$. It applies for composite as well as prime moduli.

[Exact three-vertex checks](check_orbit.py)

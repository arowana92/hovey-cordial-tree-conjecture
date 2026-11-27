# Arbitrary leaf offsets on a subgroup star

Let $k=qs$, with $q,s\ge2$. Take a central star on $s$ vertices and attach $m_v$ labeled leaves at each star vertex $v$, where $\sum m_v=(q-1)s$. Keep ordinary endpoint sums on the central star; each leaf edge $e$ independently has prescribed offset $q\epsilon_e$ in $\mathbb Z_k$. Seek a bijection on all $k$ vertices with distinct edge weights, mapping the central star onto $q\mathbb Z_k$. Put $E=\sum_e\epsilon_e\pmod s$.

**Theorem.** The entire dependence on the leaf offsets is through $E$. Set $S=s(s-1)/2$ and $g=\gcd(s, m_v-m_1:v\in V)$. The required bijection exists exactly when
$$
-E\equiv S m_1\pmod g,
$$
with one exceptional form for $s\ge3$. If, modulo $s$, the populations are $s-2$ copies of $c$ together with $c+u,c-u$ for a unit $u$, the criterion is instead $-E\not\equiv S c\pmod s$. In particular, outside that form and when $g=1$, **every** choice of all leaf offsets works.

Indeed, write the star labels as $qh_v$. The $h_v$ must permute $\mathbb Z_s$. The internal star sums are distinct for every such permutation. Each other coset modulo $q$ must appear once in full on vertices and on weights, since only leaf edges reach those cosets. Subtracting the total leaf labels from the total leaf weights gives the necessary equation
$$
\sum_v m_v h_v=-E\pmod s.
$$
Conversely, for such a permutation, make a list of the effective shifts $h_{v(e)}+\epsilon_e$ of the leaves. Its sum is zero. Partition it into $q-1$ zero-sum groups of size $s$ using Erdős–Ginzburg–Ziv repeatedly and taking the last group by subtraction. Give one group to each nonzero coset $j\pmod q$. In that group Hall's displacement theorem supplies digits $t_e$ with both $t_e$ and $t_e+h_{v(e)}+\epsilon_e$ running through $\mathbb Z_s$. The labels $j+qt_e$ now fill both the vertex and weight coset. [Ordinary subgroup construction](../hub/even-radius.md) · [Erdős, Ginzburg and Ziv (1961)](https://www.renyi.hu/~p_erdos/1961-25.pdf) · [Marshall Hall Jr. (1952)](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

For $s\ge3$, the exact image of the permutation sum in the displayed equation is the arithmetic-progression-weighted sumset described by Grynkiewicz, Philipp and Ponomarenko in equations (4.2) and (4.3). Applying it to the coefficient list $m_v$ gives exactly the criterion above. At $s=2$ the two orders of the digits give the first formula directly. In the exceptional case the sum is $Sc+u(h_i-h_j)$; the difference of the two exceptional digits takes precisely the nonzero residues. [Grynkiewicz, Philipp and Ponomarenko, *Arithmetic-progression-weighted subsequence sums*, §4](https://arxiv.org/pdf/1102.5351)

For example, for every $s\ge6$ start with populations $1,1,s-2,0,\ldots,0$, and add $(q-2)s$ at any one star vertex. These populations have $g=1$ and lack the exceptional form. All leaf offsets in the subgroup are possible even if $k$ has several distinct prime factors. At orders beyond this core one may attach arbitrarily many further leaves at its vertices, with arbitrary individual offsets modulo $k$. Choose the first such leaf to fill the deficient weight, and use Hall's partial permutation lemma on successive leaves with their effective parent shifts. Failure of the displayed criterion excludes the prescribed subgroup placement; it does not decide an unrestricted labeling. [Leaf extension](../counterexample-bound.md#removing-leaves) · [All-tree offset obstructions](prime-powers.md)

An independent permutation enumeration verified the scalar-product image for 2,157 population multisets. Separately, direct enumeration over vertex labels constrained to the designated subgroup checked 750 decorated trees by computing their original edge weights. [Arithmetic test and independent exhaustive checks](subgroup_offsets.py)

~~~sh
python3 -B -m research.biased.subgroup_offsets
~~~
